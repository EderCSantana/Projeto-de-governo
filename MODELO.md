# Modelo de medida

O jeito mais fácil de escrever uma medida é pelo formulário **Nova proposta**
do [site do projeto](https://edercsantana.github.io/Projeto-de-governo/#/propor).
Ele monta o texto abaixo para você.

Cada medida fica na página da área, dentro do prazo certo (curto, médio ou
longo), e começa com um título de nível 3 (`###`). Os campos curtos são itens
de lista e os longos são seções `####`. Apague as seções que ficarem vazias:
só a solução em uma frase, o relator, o problema e a descrição da solução são
obrigatórios.

```markdown
### Título curto da medida

- **Solução em uma frase:** a medida, de forma direta.
- **Relator(a):** nome e núcleo, ou @usuario-do-github
- **Situação:** proposta

#### Problema a ser resolvido

Qual é o problema e quem ele atinge.

#### Por que é um problema: referências

- Dados, estudos e reportagens que comprovam o problema, com links.

#### Impacto do problema na vida dos cidadãos

#### Impacto do problema na economia

#### Impacto do problema em outras áreas

#### Descrição da solução proposta

O que muda, para quem e quem executa.

#### Como fazer

O instrumento (lei, decreto, programa, emenda ao orçamento, parceria,
concessão...) e os passos principais.

#### Onde já foi feito

- Cidade, estado ou país, com os resultados e links.

#### Comprovação científica

- Estudos e avaliações que mostram que a solução funciona.

#### Como testar a proposta

Se não houver comprovação científica: um projeto piloto, dizendo onde, por
quanto tempo, comparado com quê e qual resultado decide se a medida continua.

#### Impacto esperado

#### Como medir

Indicador e meta (ex.: "fila de cirurgias de 120 para 30 dias em 2 anos").

#### Impacto positivo na vida dos cidadãos

#### Impacto na economia

#### Impacto em outras áreas

#### Custo estimado e fonte dos recursos

Quanto custa e de onde sai o dinheiro.

#### Prós

- ...

#### Contras

- ...
```

Medidas mais antigas, escritas só com itens (`- **O que é:**`,
`- **Como fazer:**`...), continuam valendo.

## Situação

| Situação | Significado |
|---|---|
| `proposta` | Acabou de entrar e ainda não foi discutida |
| `em discussão` | Sendo debatida na issue ou no pull request |
| `aprovada` | Aprovada pela coordenação do programa |
| `descartada` | Não entra no programa. Deixe registrado o motivo em uma linha |

## Boas práticas

- **Uma medida por título.** Se forem duas ações diferentes, escreva duas medidas.
- **Confira se o cargo pode fazer isso.** Veja o cabeçalho da página e o
  [COMPETENCIAS.md](COMPETENCIAS.md). Se depende de outra esfera, diga como o
  cargo vai articular (convênio, emenda, pressão política).
- **Nos cargos do Legislativo, diga qual é o instrumento:** projeto de lei,
  emenda ao orçamento, indicação, CPI ou fiscalização. Leia o aviso sobre
  iniciativa no índice do cargo.
- **Toda medida com custo precisa de fonte.** Medidas sem fonte não são aprovadas.
- **Seja verificável.** Prefira metas com número e prazo a intenções gerais.
- **Mostre os contras.** Uma proposta que reconhece riscos e custos é mais
  fácil de defender.
- **Sem prova, proponha um teste.** Se não há estudos mostrando que funciona,
  comece por um piloto com meta clara.
