#!/usr/bin/env python3
"""Gera um site (um único HTML) para navegar pelo Projeto de Governo no navegador.

Lê as páginas de cargos/ e os documentos da raiz, separa cada medida nos seus
campos e grava site/index.html, que abre direto no navegador, sem servidor.

Uso:
    python ferramentas/gerar_site.py           # gera site/index.html
    python ferramentas/gerar_site.py --abrir   # gera e abre no navegador
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import webbrowser
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import estrutura as e  # noqa: E402

RAIZ = e.RAIZ
SAIDA = RAIZ / "site" / "index.html"
MODELO_HTML = Path(__file__).resolve().parent / "site_modelo.html"

CAMPO = re.compile(r"^-\s+\*\*(.+?):\*\*\s*(.*)$")


def repositorio():
    """URL do GitHub a partir do remote origin, para os links de edição."""
    try:
        url = subprocess.run(
            ["git", "-C", str(RAIZ), "remote", "get-url", "origin"],
            capture_output=True, text=True, check=True,
        ).stdout.strip()
    except (OSError, subprocess.CalledProcessError):
        return ""
    url = re.sub(r"^git@github\.com:", "https://github.com/", url)
    return re.sub(r"\.git$", "", url)


def medidas_do_arquivo(texto):
    """Lista as medidas de uma página de área: prazo, título, campos e notas.

    Campos curtos são itens "- **Nome:** valor". Campos longos são seções
    "#### Nome" com texto livre em markdown até o próximo título.
    """
    if e.MARCADOR in texto:
        texto = texto.split(e.MARCADOR, 1)[1]
    texto = re.sub(r"<!--.*?-->", "", texto, flags=re.S)
    medidas, prazo, atual, secao = [], None, None, False
    for linha in texto.splitlines():
        if linha.startswith("## "):
            prazo = next((i for i, (t, _) in enumerate(e.PRAZOS) if linha[3:].startswith(t)), None)
            atual, secao = None, False
        elif linha.startswith("### ") and prazo is not None:
            atual = dict(prazo=prazo, titulo=linha[4:].strip(), campos=[], notas="")
            medidas.append(atual)
            secao = False
        elif atual is None:
            continue
        elif linha.startswith("#### "):
            atual["campos"].append([linha[5:].strip(), ""])
            secao = True
        elif secao:
            atual["campos"][-1][1] += linha + "\n"
        else:
            m = CAMPO.match(linha)
            if m:
                atual["campos"].append([m.group(1).strip(), m.group(2).strip()])
            elif linha.strip() and atual["campos"] and linha.startswith((" ", "\t")):
                atual["campos"][-1][1] += "\n" + re.sub(r"^(  |\t)", "", linha)
            elif linha.strip():
                atual["notas"] += linha + "\n"
    for m in medidas:
        m["campos"] = [[k, v.strip()] for k, v in m["campos"] if v.strip()]
        campos = dict((k.lower(), v) for k, v in m["campos"])
        m["situacao"] = campos.get("situação", "proposta").strip("`. ").lower() or "proposta"
        m["autor"] = campos.get("proposta por", "")
        m["notas"] = m["notas"].strip()
    return medidas


def dados():
    cargos, medidas = [], []
    for c in e.CARGOS:
        esfera = c["esfera"]
        papel = (e.PAPEL_EXECUTIVO if e.executivo(c) else e.PAPEL_LEGISLATIVO)[esfera]
        areas = [a["id"] for a in e.areas_de(c)]
        cargos.append(dict(
            id=c["id"], nome=c["nome"], esfera=esfera, esferaNome=e.ESFERAS[esfera],
            poder=c["poder"], mandato=c["mandato"], papel=papel,
            extra=e.PAPEL_EXTRA.get(c["id"], ""),
            cuidado="" if e.executivo(c) else e.CUIDADO_LEGISLATIVO,
            areas=areas,
        ))
        for area in areas:
            arquivo = RAIZ / "cargos" / c["id"] / f"{area}.md"
            if not arquivo.exists():
                continue
            for m in medidas_do_arquivo(arquivo.read_text(encoding="utf-8")):
                m.update(cargo=c["id"], area=area)
                medidas.append(m)
    areas = [
        dict(id=a["id"], nome=a["nome"], eixo=a["eixo"], federal=a["federal"],
             estadual=a["estadual"], municipal=a["municipal"])
        for a in e.AREAS
    ]
    docs = {
        nome: (RAIZ / arquivo).read_text(encoding="utf-8")
        for nome, arquivo in [("contribuir", "COMO-CONTRIBUIR.md"), ("modelo", "MODELO.md")]
        if (RAIZ / arquivo).exists()
    }
    prazos = [dict(nome=t, descricao=d) for t, d in e.PRAZOS]
    return dict(cargos=cargos, areas=areas, medidas=medidas, prazos=prazos,
                esferas=e.ESFERAS, eixos=[dict(id=i, nome=n) for i, n in e.EIXOS], docs=docs, repo=repositorio())


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--abrir", action="store_true", help="abre o site no navegador")
    args = parser.parse_args()

    conteudo = json.dumps(dados(), ensure_ascii=False).replace("</", "<\\/")
    html = MODELO_HTML.read_text(encoding="utf-8").replace("/*__DADOS__*/null", conteudo)
    SAIDA.parent.mkdir(parents=True, exist_ok=True)
    SAIDA.write_text(html, encoding="utf-8", newline="\n")
    print(f"Site gerado em {SAIDA.relative_to(RAIZ)}")
    if args.abrir:
        webbrowser.open(SAIDA.as_uri())


if __name__ == "__main__":
    main()
