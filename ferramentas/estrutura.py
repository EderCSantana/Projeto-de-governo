#!/usr/bin/env python3
"""Cria e atualiza a estrutura do Projeto de Governo.

- Cria cargos/<cargo>/<area>.md quando ainda não existe, com as seções de
  curto, médio e longo prazo.
- Atualiza o cabeçalho de cada arquivo (o que o cargo faz na área) sem tocar
  nas medidas escritas abaixo do marcador.
- Gera o índice de cada cargo, a matriz de competências e o índice do README.

Uso:
    python ferramentas/estrutura.py           # cria e atualiza
    python ferramentas/estrutura.py --check   # só confere (sai com 1 se algo mudaria)
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent

FEDERAL, ESTADUAL, MUNICIPAL = "federal", "estadual", "municipal"
ESFERAS = {FEDERAL: "União", ESTADUAL: "Estado", MUNICIPAL: "Município"}

CARGOS = [
    dict(id="presidente", nome="Presidente da República", esfera=FEDERAL, poder="executivo", mandato=4),
    dict(id="governador", nome="Governador(a)", esfera=ESTADUAL, poder="executivo", mandato=4),
    dict(id="prefeito", nome="Prefeito(a)", esfera=MUNICIPAL, poder="executivo", mandato=4),
    dict(id="senador", nome="Senador(a)", esfera=FEDERAL, poder="legislativo", mandato=8),
    dict(id="deputado-federal", nome="Deputado(a) federal", esfera=FEDERAL, poder="legislativo", mandato=4),
    dict(id="deputado-estadual", nome="Deputado(a) estadual ou distrital", esfera=ESTADUAL, poder="legislativo", mandato=4),
    dict(id="vereador", nome="Vereador(a)", esfera=MUNICIPAL, poder="legislativo", mandato=4),
]

PAPEL_EXECUTIVO = {
    FEDERAL: "Chefia o governo federal: executa as políticas nacionais, propõe o orçamento da União, "
    "nomeia ministros, edita decretos e medidas provisórias, sanciona ou veta leis.",
    ESTADUAL: "Chefia o governo do estado: executa as políticas estaduais, propõe o orçamento, "
    "nomeia secretários, comanda as polícias e sanciona ou veta leis estaduais.",
    MUNICIPAL: "Chefia a prefeitura: executa os serviços locais, propõe o orçamento, nomeia "
    "secretários e sanciona ou veta leis municipais.",
}

PAPEL_LEGISLATIVO = {
    FEDERAL: "Propõe e vota leis federais e emendas à Constituição, aprova o orçamento da União e "
    "indica emendas parlamentares (individuais e de bancada, de execução obrigatória) e fiscaliza o "
    "governo federal com CPIs, convocação de ministros e apoio do Tribunal de Contas da União.",
    ESTADUAL: "Propõe e vota leis estaduais e emendas à Constituição do estado, aprova o orçamento "
    "estadual e indica emendas e fiscaliza o governador com CPIs e apoio do Tribunal de Contas do Estado.",
    MUNICIPAL: "Propõe e vota leis municipais (assuntos de interesse local), incluindo o plano diretor, "
    "aprova o orçamento do município e indica emendas, faz indicações à prefeitura e fiscaliza o "
    "prefeito com apoio do Tribunal de Contas.",
}

PAPEL_EXTRA = {
    "senador": "Só o Senado: aprova autoridades (ministros do STF, diretoria do Banco Central, "
    "embaixadores), fixa limites de endividamento de estados e municípios e julga crimes de "
    "responsabilidade do presidente. Representa o estado: são três senadores por estado.",
    "deputado-federal": "Só a Câmara: autoriza a abertura de processo contra o presidente, e os "
    "projetos do Executivo começam a tramitar por ela. Representa a população: o número de "
    "deputados varia conforme o estado.",
    "deputado-estadual": "No Distrito Federal, o deputado distrital acumula as competências "
    "estaduais e municipais.",
    "vereador": "Também aprova a Lei Orgânica do Município e suas mudanças.",
}

CUIDADO_LEGISLATIVO = (
    "Leis que criam órgãos ou cargos, mudam a estrutura do Executivo ou o regime dos servidores "
    "são de iniciativa privativa do chefe do Executivo (art. 61, §1º, da Constituição, repetido nas "
    "constituições estaduais e leis orgânicas). Leis de iniciativa parlamentar que só geram despesa "
    "podem ser válidas (STF, Tema 917), mas devem indicar de onde sai o dinheiro. Quando a medida "
    "depende do Executivo, prefira indicações, emendas ao orçamento e fiscalização."
)

# Áreas públicas e o que cada esfera faz nelas. None = não é competência daquela esfera.
AREAS = [
    dict(
        id="saude",
        nome="Saúde",
        federal="Coordena o SUS, financia estados e municípios, compra vacinas e medicamentos "
        "estratégicos, regula planos de saúde (ANS) e a vigilância sanitária (Anvisa) e mantém "
        "hospitais federais e universitários.",
        estadual="Hospitais regionais e de alta complexidade, hemocentros, laboratórios centrais, "
        "regulação de leitos, assistência farmacêutica especializada e apoio aos municípios.",
        municipal="Atenção básica (UBS e Estratégia Saúde da Família), UPAs, vigilância "
        "epidemiológica e sanitária local, combate a endemias e saúde bucal e mental na rede municipal.",
    ),
    dict(
        id="educacao",
        nome="Educação",
        federal="Universidades e institutos federais, ensino superior (ProUni, Fies, Capes), Base "
        "Nacional Comum Curricular, Enem, complementação do Fundeb e programas de merenda (PNAE), "
        "livro didático e transporte escolar.",
        estadual="Ensino médio, parte do ensino fundamental, ensino técnico e universidades "
        "estaduais e formação dos professores da rede.",
        municipal="Creches, pré-escola e ensino fundamental, alfabetização, educação de jovens e "
        "adultos, merenda e transporte escolar.",
    ),
    dict(
        id="seguranca-publica",
        nome="Segurança pública",
        federal="Polícia Federal, Polícia Rodoviária Federal, Força Nacional, controle de fronteiras, "
        "armas e crimes interestaduais e internacionais, presídios federais, Fundo Nacional de "
        "Segurança Pública e legislação penal.",
        estadual="Polícia Militar, Polícia Civil, Corpo de Bombeiros, polícia científica e sistema "
        "prisional. É o principal responsável pela segurança no dia a dia.",
        municipal="Guarda municipal, videomonitoramento, iluminação pública, ocupação de espaços "
        "públicos e prevenção da violência. O município não comanda polícia.",
    ),
    dict(
        id="transporte-e-mobilidade",
        nome="Transporte e mobilidade",
        federal="Rodovias, ferrovias e hidrovias federais, portos e aeroportos (diretamente ou por "
        "concessão), agências reguladoras (ANTT, Antaq, Anac), Código de Trânsito e transporte "
        "interestadual.",
        estadual="Rodovias estaduais, transporte intermunicipal e metropolitano (metrô, trens, "
        "ônibus) e Detran.",
        municipal="Transporte coletivo urbano, trânsito e sinalização, ciclovias, calçadas, táxi e "
        "transporte por aplicativo.",
    ),
    dict(
        id="infraestrutura-e-obras",
        nome="Infraestrutura e obras públicas",
        federal="Grandes obras de interesse nacional, transferências para obras de estados e "
        "municípios e parcerias público-privadas federais.",
        estadual="Obras estaduais (estradas, prédios, barragens), parcerias público-privadas "
        "estaduais e apoio a obras municipais.",
        municipal="Pavimentação, drenagem, pontes, prédios públicos, manutenção urbana e zeladoria.",
    ),
    dict(
        id="saneamento",
        nome="Saneamento básico",
        federal="Marco legal do saneamento, normas de referência (ANA), financiamento (Caixa, BNDES) "
        "e metas nacionais de universalização.",
        estadual="Companhias estaduais de saneamento, prestação regionalizada e saneamento nas "
        "regiões metropolitanas.",
        municipal="É o titular do serviço: água, esgoto, coleta e destinação do lixo e drenagem. "
        "Presta diretamente ou contrata e faz o plano municipal de saneamento.",
    ),
    dict(
        id="habitacao",
        nome="Habitação",
        federal="Programas nacionais de moradia, financiamento habitacional e regularização "
        "fundiária em terras da União.",
        estadual="Companhias estaduais de habitação, programas estaduais e contrapartidas aos "
        "programas federais.",
        municipal="Cadastro e seleção das famílias, terrenos, regularização fundiária urbana, "
        "urbanização de favelas e aluguel social.",
    ),
    dict(
        id="urbanismo",
        nome="Urbanismo e planejamento urbano",
        federal="Diretrizes nacionais (Estatuto da Cidade), política de desenvolvimento urbano e "
        "regional e financiamento.",
        estadual="Planejamento das regiões metropolitanas e aglomerações urbanas.",
        municipal="Plano diretor, zoneamento e uso do solo, licenciamento de obras, praças e "
        "parques.",
    ),
    dict(
        id="meio-ambiente",
        nome="Meio ambiente e clima",
        federal="Política nacional de meio ambiente e clima, Ibama e ICMBio, florestas e unidades "
        "de conservação federais, licenciamento de grandes empreendimentos, metas climáticas e "
        "águas da União (ANA).",
        estadual="Órgão ambiental estadual, licenciamento, unidades de conservação estaduais e "
        "gestão dos recursos hídricos do estado.",
        municipal="Licenciamento de impacto local, arborização, áreas verdes, fiscalização local e "
        "educação ambiental.",
    ),
    dict(
        id="defesa-civil",
        nome="Defesa civil e desastres",
        federal="Sistema Nacional de Proteção e Defesa Civil, recursos para resposta e reconstrução "
        "e alertas e monitoramento (Cemaden).",
        estadual="Defesa civil estadual, Corpo de Bombeiros e apoio aos municípios em desastres.",
        municipal="Defesa civil municipal, mapeamento de áreas de risco, planos de contingência, "
        "alertas e abrigos.",
    ),
    dict(
        id="assistencia-social",
        nome="Assistência social",
        federal="Bolsa Família, Benefício de Prestação Continuada (BPC), Cadastro Único e "
        "cofinanciamento do SUAS.",
        estadual="Cofinanciamento e apoio técnico aos municípios e serviços regionais de média e "
        "alta complexidade.",
        municipal="CRAS e CREAS, abrigos, acompanhamento de famílias, inscrição no Cadastro Único e "
        "atendimento à população em situação de rua.",
    ),
    dict(
        id="direitos-humanos",
        nome="Direitos humanos e cidadania",
        federal="Políticas nacionais para mulheres, igualdade racial, pessoas com deficiência, "
        "pessoas idosas, crianças e adolescentes e pessoas LGBTQIA+, Disque 100 e legislação de "
        "direitos civis.",
        estadual="Programas de proteção (testemunhas, defensores de direitos humanos), delegacias e "
        "casas da mulher e conselhos estaduais.",
        municipal="Conselhos tutelares, centros de referência, acessibilidade e políticas locais "
        "para mulheres, juventude, pessoas idosas e igualdade racial.",
    ),
    dict(
        id="povos-indigenas-e-tradicionais",
        nome="Povos indígenas e comunidades tradicionais",
        federal="Demarcação de terras indígenas, Funai, saúde indígena (Sesai) e titulação de "
        "territórios quilombolas (Incra).",
        estadual="Titulação de territórios quilombolas em terras estaduais, educação escolar "
        "indígena e quilombola e apoio às comunidades.",
        municipal=None,
    ),
    dict(
        id="trabalho-e-renda",
        nome="Trabalho, emprego e renda",
        federal="Legislação trabalhista, salário mínimo, seguro-desemprego, FGTS e fiscalização do "
        "trabalho.",
        estadual="Qualificação profissional, postos do Sine e programas de primeiro emprego.",
        municipal="Intermediação de mão de obra, qualificação local, apoio a microempreendedores e "
        "economia solidária.",
    ),
    dict(
        id="previdencia",
        nome="Previdência social",
        federal="INSS e Regime Geral de Previdência Social: regras de aposentadoria, pensões e "
        "benefícios.",
        estadual=None,
        municipal=None,
    ),
    dict(
        id="financas-publicas",
        nome="Economia e finanças públicas",
        federal="Orçamento da União, tributos federais, reforma tributária (CBS e IBS), dívida "
        "pública, repasses aos estados e municípios (FPE, FPM) e política fiscal. A política "
        "monetária é do Banco Central, que é autônomo.",
        estadual="Orçamento do estado, ICMS (em transição para o IBS), IPVA, ITCMD, dívida "
        "estadual e previdência dos servidores do estado.",
        municipal="Orçamento do município, IPTU, ISS (em transição para o IBS), ITBI, taxas e "
        "previdência dos servidores municipais.",
    ),
    dict(
        id="desenvolvimento-economico",
        nome="Desenvolvimento econômico, indústria e comércio",
        federal="Política industrial e de comércio exterior, BNDES, crédito para pequenas empresas, "
        "defesa da concorrência (Cade) e do consumidor.",
        estadual="Atração de investimentos, agências e bancos de fomento estaduais e Procon "
        "estadual.",
        municipal="Alvarás e ambiente de negócios local, Sala do Empreendedor, feiras e comércio "
        "local e Procon municipal.",
    ),
    dict(
        id="agricultura",
        nome="Agricultura, pecuária e abastecimento",
        federal="Plano Safra, crédito rural (Pronaf), Embrapa, defesa agropecuária, reforma agrária "
        "(Incra) e Conab.",
        estadual="Assistência técnica e extensão rural, defesa sanitária animal e vegetal e "
        "estradas rurais estaduais.",
        municipal="Estradas vicinais, compra da agricultura familiar para a merenda, feiras, "
        "mercados municipais e hortas urbanas.",
    ),
    dict(
        id="ciencia-tecnologia-e-inovacao",
        nome="Ciência, tecnologia e inovação",
        federal="CNPq, Finep, institutos de pesquisa e política nacional de inovação e de governo "
        "digital.",
        estadual="Fundação de amparo à pesquisa, parques tecnológicos e universidades estaduais.",
        municipal="Inclusão digital (internet pública, telecentros), apoio a empresas inovadoras "
        "locais e governo digital municipal.",
    ),
    dict(
        id="cultura",
        nome="Cultura",
        federal="Lei Rouanet, Lei Aldir Blanc, patrimônio histórico (Iphan), Ancine e museus e "
        "bibliotecas federais.",
        estadual="Equipamentos culturais estaduais, editais, festivais e patrimônio do estado.",
        municipal="Centros culturais, bibliotecas, festas populares, editais locais e patrimônio "
        "do município.",
    ),
    dict(
        id="esporte-e-lazer",
        nome="Esporte e lazer",
        federal="Lei de Incentivo ao Esporte, Bolsa Atleta, grandes eventos e programas nacionais "
        "de esporte educacional.",
        estadual="Equipamentos e programas estaduais e jogos escolares.",
        municipal="Quadras, praças esportivas, escolinhas, eventos e ligas locais.",
    ),
    dict(
        id="turismo",
        nome="Turismo",
        federal="Embratur, promoção internacional, cadastro de prestadores (Cadastur) e "
        "financiamento (Fungetur).",
        estadual="Promoção do estado, rotas regionais e infraestrutura turística.",
        municipal="Calendário de eventos, sinalização turística e conservação dos atrativos locais.",
    ),
    dict(
        id="energia-e-mineracao",
        nome="Energia e mineração",
        federal="Setor elétrico (Aneel, ONS), petróleo, gás e biocombustíveis (ANP), mineração "
        "(ANM), transição energética e tarifa social de energia.",
        estadual="Distribuição de gás canalizado e incentivo a energia solar, eólica e "
        "biocombustíveis no estado.",
        municipal=None,
    ),
    dict(
        id="comunicacoes",
        nome="Comunicações e conectividade",
        federal="Telecomunicações (Anatel), radiodifusão, Correios e conectividade de escolas e "
        "regiões sem internet.",
        estadual=None,
        municipal=None,
    ),
    dict(
        id="defesa-nacional",
        nome="Defesa nacional",
        federal="Forças Armadas, indústria de defesa e proteção das fronteiras, do mar e do espaço "
        "aéreo.",
        estadual=None,
        municipal=None,
    ),
    dict(
        id="relacoes-exteriores",
        nome="Relações exteriores",
        federal="Política externa, diplomacia, acordos internacionais, Mercosul e atendimento a "
        "brasileiros no exterior.",
        estadual=None,
        municipal=None,
    ),
    dict(
        id="gestao-publica",
        nome="Gestão pública, transparência e combate à corrupção",
        federal="Servidores federais, compras públicas, Controladoria-Geral da União, transparência "
        "e relação com estados e municípios.",
        estadual="Servidores do estado, compras, controladoria, transparência e atendimento ao "
        "cidadão.",
        municipal="Servidores municipais, compras, ouvidoria, transparência e atendimento ao "
        "cidadão.",
    ),
]

PRAZOS = [
    ("Curto prazo", "Primeiro ano de mandato."),
    ("Médio prazo", "Até o fim do mandato ({mandato} anos)."),
    ("Longo prazo", "Além do mandato: políticas de Estado, de 8 a 20 anos."),
]

MARCADOR = "<!-- Fim do cabeçalho gerado. Escreva as medidas abaixo seguindo o MODELO.md. -->"
INDICE_INICIO = "<!-- inicio:indice (gerado por ferramentas/estrutura.py) -->"
INDICE_FIM = "<!-- fim:indice -->"


def areas_de(cargo):
    return [a for a in AREAS if a[cargo["esfera"]]]


def executivo(cargo):
    return cargo["poder"] == "executivo"


def cabecalho(cargo, area):
    texto = area[cargo["esfera"]]
    linhas = [
        f"# {area['nome']} · {cargo['nome']}",
        "",
        f"[← {cargo['nome']}](README.md) · [Modelo de medida](../../MODELO.md) · "
        "[Quem faz o quê](../../COMPETENCIAS.md)",
        "",
    ]
    if executivo(cargo):
        linhas.append(f"> **O que este cargo faz nesta área:** {texto}")
    else:
        linhas += [
            f"> **Esta área na esfera {cargo['esfera']}:** {texto}",
            ">",
            "> **Como o mandato atua aqui:** com leis, emendas ao orçamento e fiscalização. "
            "Veja os limites no [índice do cargo](README.md).",
        ]
    linhas += ["", MARCADOR, ""]
    return "\n".join(linhas)


def corpo(cargo):
    partes = []
    for titulo, descricao in PRAZOS:
        partes += [
            f"## {titulo}",
            "",
            f"_{descricao.format(mandato=cargo['mandato'])}_",
            "",
            "<!-- Adicione as medidas aqui, cada uma começando com ### -->",
            "",
        ]
    return "\n".join(partes)


def contar(texto):
    """Medidas (títulos ###) em cada prazo."""
    contagem = {titulo: 0 for titulo, _ in PRAZOS}
    atual = None
    for linha in texto.splitlines():
        if linha.startswith("## "):
            atual = next((t for t, _ in PRAZOS if linha[3:].startswith(t)), None)
        elif linha.startswith("### ") and atual:
            contagem[atual] += 1
    return contagem


def indice_cargo(cargo, contagens):
    esfera = cargo["esfera"]
    linhas = [
        f"# {cargo['nome']}",
        "",
        "[← Projeto de Governo](../../README.md) · [Quem faz o quê](../../COMPETENCIAS.md)",
        "",
        f"**Esfera:** {ESFERAS[esfera]} · **Poder:** {cargo['poder']} · "
        f"**Mandato:** {cargo['mandato']} anos",
        "",
        "## O que o cargo faz",
        "",
        (PAPEL_EXECUTIVO if executivo(cargo) else PAPEL_LEGISLATIVO)[esfera],
    ]
    if cargo["id"] in PAPEL_EXTRA:
        linhas += ["", PAPEL_EXTRA[cargo["id"]]]
    if not executivo(cargo):
        linhas += ["", f"> **Atenção:** {CUIDADO_LEGISLATIVO}"]
    linhas += [
        "",
        "## Áreas",
        "",
        "| Área | Curto | Médio | Longo |",
        "|---|:-:|:-:|:-:|",
    ]
    for area in areas_de(cargo):
        c = contagens[area["id"]]
        linhas.append(
            f"| [{area['nome']}]({area['id']}.md) | "
            + " | ".join(str(c[t]) for t, _ in PRAZOS)
            + " |"
        )
    fora = [a["nome"] for a in AREAS if not a[esfera]]
    if fora:
        linhas += [
            "",
            "## Fora da competência",
            "",
            f"Estas áreas não são da esfera {esfera}, por isso não têm seção aqui: "
            + ", ".join(fora)
            + ".",
        ]
    return "\n".join(linhas) + "\n"


def competencias():
    linhas = [
        "# Quem faz o quê",
        "",
        "[← Projeto de Governo](README.md)",
        "",
        "Nem todo cargo pode agir em toda área. A Constituição divide as competências entre "
        "União, estados e municípios. Dentro de cada esfera, quem **executa** é o Executivo "
        "(presidente, governador, prefeito) e quem **legisla e fiscaliza** é o Legislativo "
        "(senadores e deputados federais, deputados estaduais, vereadores).",
        "",
        "| Área | União | Estado | Município |",
        "|---|:-:|:-:|:-:|",
    ]
    for area in AREAS:
        linhas.append(
            f"| {area['nome']} | "
            + " | ".join("✅" if area[e] else "—" for e in ESFERAS)
            + " |"
        )
    linhas += [
        "",
        "✅ a esfera atua na área · — não é competência da esfera",
        "",
        "## Por cargo",
        "",
        "| Cargo | Esfera | Executa | Legisla e fiscaliza |",
        "|---|---|:-:|:-:|",
    ]
    for cargo in CARGOS:
        e = executivo(cargo)
        linhas.append(
            f"| [{cargo['nome']}](cargos/{cargo['id']}/README.md) | {ESFERAS[cargo['esfera']]} | "
            f"{'✅' if e else '—'} | {'—' if e else '✅'} |"
        )
    linhas += [
        "",
        "## O que cada esfera faz em cada área",
        "",
    ]
    for area in AREAS:
        linhas += [f"### {area['nome']}", ""]
        for esfera, nome in ESFERAS.items():
            linhas.append(f"- **{nome}:** {area[esfera] or 'não é competência desta esfera.'}")
        linhas.append("")
    linhas += [
        "> Resumo para orientar as propostas, não é parecer jurídico. Há competências comuns "
        "(art. 23 da Constituição) e concorrentes (art. 24) em que mais de uma esfera atua. "
        "Na dúvida, confira a Constituição e a lei orgânica do município.",
    ]
    return "\n".join(linhas) + "\n"


def indice_readme(contagens_por_cargo):
    linhas = [
        INDICE_INICIO,
        "| Cargo | Esfera | Áreas | Medidas |",
        "|---|---|:-:|:-:|",
    ]
    for cargo in CARGOS:
        contagens = contagens_por_cargo[cargo["id"]]
        total = sum(sum(c.values()) for c in contagens.values())
        linhas.append(
            f"| [{cargo['nome']}](cargos/{cargo['id']}/README.md) | {ESFERAS[cargo['esfera']]} | "
            f"{len(contagens)} | {total} |"
        )
    linhas.append(INDICE_FIM)
    return "\n".join(linhas)


def planejar():
    """Conteúdo esperado de cada arquivo gerado ou atualizado."""
    saida: dict[Path, str] = {}
    avisos = []
    contagens_por_cargo = {}
    for cargo in CARGOS:
        contagens = {}
        for area in areas_de(cargo):
            caminho = RAIZ / "cargos" / cargo["id"] / f"{area['id']}.md"
            if caminho.exists():
                atual = caminho.read_text(encoding="utf-8")
                if MARCADOR not in atual:
                    avisos.append(f"{caminho.relative_to(RAIZ)}: marcador não encontrado, arquivo mantido")
                    contagens[area["id"]] = contar(atual)
                    continue
                medidas = atual.split(MARCADOR, 1)[1].lstrip("\n")
            else:
                medidas = corpo(cargo)
            saida[caminho] = cabecalho(cargo, area) + "\n" + medidas
            contagens[area["id"]] = contar(medidas)
        contagens_por_cargo[cargo["id"]] = contagens
        saida[RAIZ / "cargos" / cargo["id"] / "README.md"] = indice_cargo(cargo, contagens)
    saida[RAIZ / "COMPETENCIAS.md"] = competencias()

    readme = RAIZ / "README.md"
    texto = readme.read_text(encoding="utf-8")
    padrao = re.compile(re.escape(INDICE_INICIO) + ".*?" + re.escape(INDICE_FIM), re.S)
    if not padrao.search(texto):
        avisos.append("README.md: marcadores do índice não encontrados")
    else:
        saida[readme] = padrao.sub(lambda _: indice_readme(contagens_por_cargo), texto)

    conhecidos = {(c["id"], a["id"]) for c in CARGOS for a in areas_de(c)}
    for arquivo in sorted((RAIZ / "cargos").glob("*/*.md")):
        if arquivo.name != "README.md" and (arquivo.parent.name, arquivo.stem) not in conhecidos:
            avisos.append(f"{arquivo.relative_to(RAIZ)}: área ou cargo fora da lista em ferramentas/estrutura.py")
    return saida, avisos


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--check", action="store_true", help="só confere, não grava")
    args = parser.parse_args()

    saida, avisos = planejar()
    mudados = [
        p for p, texto in saida.items()
        if not p.exists() or p.read_text(encoding="utf-8") != texto
    ]
    for aviso in avisos:
        print(f"aviso: {aviso}")
    if args.check:
        for p in mudados:
            print(f"desatualizado: {p.relative_to(RAIZ)}")
        sys.exit(1 if mudados or avisos else 0)
    for p in mudados:
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(saida[p], encoding="utf-8", newline="\n")
    print(f"{len(mudados)} arquivo(s) atualizados.")


if __name__ == "__main__":
    main()
