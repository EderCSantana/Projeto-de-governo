# Projeto de Governo

Documento colaborativo para construir o programa de governo do partido. Para
cada **cargo** em disputa há uma seção, e para cada **área pública** que esse
cargo pode gerir há propostas de **curto, médio e longo prazo**. Qualquer
filiado pode sugerir medidas, e elas são discutidas e aprovadas aqui mesmo.

## Como está organizado

```
cargos/
  presidente/          Executivo federal
  governador/          Executivo estadual
  prefeito/            Executivo municipal
  senador/             Legislativo federal
  deputado-federal/    Legislativo federal
  deputado-estadual/   Legislativo estadual (e distrital)
  vereador/            Legislativo municipal
    README.md          o que o cargo faz e o índice das áreas
    saude.md           uma página por área, com curto, médio e longo prazo
    educacao.md
    ...
COMPETENCIAS.md        quem faz o quê: áreas × esferas × cargos
MODELO.md              como escrever uma medida
COMO-CONTRIBUIR.md     passo a passo para participar
```

**Nem todo cargo pode agir em toda área.** Um prefeito não comanda a polícia e
um governador não faz política externa. Cada cargo só tem páginas para as áreas
da sua esfera. Veja a tabela em [COMPETENCIAS.md](COMPETENCIAS.md). Nos cargos
do Legislativo, as medidas são leis, emendas ao orçamento e fiscalização, e o
índice de cada um explica o que o mandato pode e não pode propor.

## Prazos

| Prazo | Horizonte |
|---|---|
| **Curto** | Primeiro ano de mandato |
| **Médio** | Até o fim do mandato (4 anos, ou 8 para senador) |
| **Longo** | Além do mandato: políticas de Estado, de 8 a 20 anos |

## Cargos

<!-- inicio:indice (gerado por ferramentas/estrutura.py) -->
| Cargo | Esfera | Áreas | Medidas |
|---|---|:-:|:-:|
| [Presidente da República](cargos/presidente/README.md) | União | 27 | 0 |
| [Governador(a)](cargos/governador/README.md) | Estado | 23 | 0 |
| [Prefeito(a)](cargos/prefeito/README.md) | Município | 21 | 0 |
| [Senador(a)](cargos/senador/README.md) | União | 27 | 0 |
| [Deputado(a) federal](cargos/deputado-federal/README.md) | União | 27 | 0 |
| [Deputado(a) estadual ou distrital](cargos/deputado-estadual/README.md) | Estado | 23 | 0 |
| [Vereador(a)](cargos/vereador/README.md) | Município | 21 | 0 |
<!-- fim:indice -->

## Como participar

- **Sem conhecimento técnico:** abra uma [issue](../../issues/new/choose) com o
  formulário **Nova medida**. A coordenação transforma a sugestão em texto no
  documento.
- **Editando direto:** abra a página da área, clique no lápis, escreva a medida
  seguindo o [MODELO.md](MODELO.md) e envie como *pull request*.

Detalhes em [COMO-CONTRIBUIR.md](COMO-CONTRIBUIR.md).

## Manutenção

As áreas, os cargos e os textos de competência ficam em
[`ferramentas/estrutura.py`](ferramentas/estrutura.py). Depois de mudar essa
lista, rode:

```bash
python ferramentas/estrutura.py
```

O script cria as páginas que faltam, atualiza os cabeçalhos sem mexer nas
medidas e refaz os índices e contagens. A cada push na branch `main`, um GitHub
Action roda o mesmo script e faz commit dos índices atualizados.
