# Fichamento — Field & Welsh (2007) — Bootstrapping clustered data

| | |
|---|---|
| **Referência (ABNT)** | FIELD, C. A.; WELSH, A. H. Bootstrapping clustered data. *Journal of the Royal Statistical Society: Series B*, v. 69, n. 3, p. 369–390, 2007. |
| **DOI / acesso** | [10.1111/j.1467-9868.2007.00593.x](https://doi.org/10.1111/j.1467-9868.2007.00593.x) |
| **Chave no `.bib`** | `field2007` |
| **Arquivo** | não versionado (PDFs ficam em `docs/articles/`, fora do Git) |
| **Fichado por** | Claude Code (assistente de IA), a pedido do grupo |
| **Revisado por** | André Maiolini (sessão de trabalho) |
| **Última atualização** | 2026-10-10 |
| **Por que ler** | Fundamenta o bootstrap por grupos (cluster bootstrap), usado para respeitar a dependência entre janelas da mesma gravação. |

> **Origem deste fichamento.** Redigido com assistência de IA (Claude Code), a partir do
> conhecimento estabelecido sobre a obra, sem acesso ao texto completo nesta sessão.
> Por isso **não há citações diretas nem números de página**: tudo é paráfrase. Antes
> de citar algo específico no relatório, conferir no original (DOI abaixo) e registrar
> a página. Ver `docs/uso_de_ia.md`.

---

## Ideias principais

1. Analisa formas de reamostrar dados agrupados: reamostrar os grupos, as observações dentro dos grupos, ou ambos.
2. Mostra quando cada esquema estima corretamente a variância sob diferentes modelos de dependência.
3. Reamostrar grupos inteiros preserva a correlação interna e é consistente quando o número de grupos cresce.

## Pontos relevantes para o projeto

- → Projeto: reamostramos gravações inteiras (e montagens, no teste de generalização), estratificadas por classe. Com poucas unidades (10 gravações, 9 montagens) os intervalos são largos — e isso é o resultado honesto.

## Onde é usado no relatório

- Seções 3.3.5, 4.6 e 5.7.

## Cuidados ao citar

- As garantias são assintóticas no número de grupos; com 9 a 10 grupos, os intervalos são aproximados.

## Pendências

- [ ] Conferir a recomendação para poucos grupos.
