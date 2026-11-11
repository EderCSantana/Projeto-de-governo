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
    "indica emendas parlamentares (individuais e de bancada, de execução obrigatória), além de "
    "fiscalizar o governo federal com CPIs, convocação de ministros e apoio do Tribunal de Contas da União.",
    ESTADUAL: "Propõe e vota leis estaduais e emendas à Constituição do estado, aprova o orçamento "
    "estadual e indica emendas, além de fiscalizar o governador com CPIs e apoio do Tribunal de Contas do Estado.",
    MUNICIPAL: "Propõe e vota leis municipais (assuntos de interesse local), incluindo o plano diretor, "
    "aprova o orçamento do município e indica emendas e faz indicações à prefeitura, além de fiscalizar o "
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

# Áreas públicas, eixos e o que cada esfera faz em cada área: ver ferramentas/areas.py.
sys.path.insert(0, str(Path(__file__).resolve().parent))
from areas import AREAS, EIXOS  # noqa: E402

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
    linhas += ["", "## Áreas"]
    for eixo, nome_eixo in EIXOS:
        do_eixo = [a for a in areas_de(cargo) if a["eixo"] == eixo]
        if not do_eixo:
            continue
        linhas += [
            "",
            f"### {nome_eixo}",
            "",
            "| Área | Curto | Médio | Longo |",
            "|---|:-:|:-:|:-:|",
        ]
        for area in do_eixo:
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
    ]
    for eixo, nome_eixo in EIXOS:
        linhas += [
            "",
            f"### {nome_eixo}",
            "",
            "| Área | União | Estado | Município |",
            "|---|:-:|:-:|:-:|",
        ]
        for area in (a for a in AREAS if a["eixo"] == eixo):
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
    for eixo, nome_eixo in EIXOS:
        linhas += [f"### {nome_eixo}", ""]
        for area in (a for a in AREAS if a["eixo"] == eixo):
            linhas += [f"#### {area['nome']}", ""]
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

    # Lista de áreas do formulário de nova medida.
    formulario = RAIZ / ".github" / "ISSUE_TEMPLATE" / "nova-medida.yml"
    if formulario.exists():
        texto = formulario.read_text(encoding="utf-8")
        padrao = re.compile(r"( *)# inicio:areas[^\n]*\n.*?# fim:areas\n", re.S)
        m = padrao.search(texto)
        if not m:
            avisos.append(f"{formulario.relative_to(RAIZ)}: marcadores da lista de áreas não encontrados")
        else:
            recuo = m.group(1)
            opcoes = "".join(f'{recuo}- "{a["nome"]}"\n' for a in AREAS)
            bloco = f"{recuo}# inicio:areas (gerado por ferramentas/estrutura.py)\n{opcoes}{recuo}# fim:areas\n"
            saida[formulario] = texto[: m.start()] + bloco + texto[m.end():]

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
