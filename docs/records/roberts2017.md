# Fichamento — Roberts et al. (2017) — Validação cruzada com dados estruturados

| | |
|---|---|
| **Referência (ABNT)** | ROBERTS, D. R. et al. Cross-validation strategies for data with temporal, spatial, hierarchical, or phylogenetic structure. *Ecography*, v. 40, n. 8, p. 913–929, 2017. |
| **DOI / acesso** | [10.1111/ecog.02881](https://doi.org/10.1111/ecog.02881) |
| **Chave no `.bib`** | `roberts2017` |
| **Arquivo** | não versionado (PDFs ficam em `docs/articles/`, fora do Git) |
| **Fichado por** | Claude Code (assistente de IA), a pedido do grupo |
| **Revisado por** | André Maiolini (sessão de trabalho) |
| **Última atualização** | 2026-10-10 |
| **Por que ler** | Fundamenta a validação cruzada agrupada (LeaveOneGroupOut por carga e por diâmetro). |

> **Origem deste fichamento.** Redigido com assistência de IA (Claude Code), a partir do
> conhecimento estabelecido sobre a obra, sem acesso ao texto completo nesta sessão.
> Por isso **não há citações diretas nem números de página**: tudo é paráfrase. Antes
> de citar algo específico no relatório, conferir no original (DOI abaixo) e registrar
> a página. Ver `docs/uso_de_ia.md`.

---

## Ideias principais

1. Mostra que a validação cruzada aleatória superestima o desempenho quando há dependência entre observações (temporal, espacial, hierárquica).
2. Recomenda validação em blocos/grupos, deixando grupos inteiros de fora, alinhada ao objetivo de generalização.

## Pontos relevantes para o projeto

- → Projeto: justifica o LeaveOneGroupOut por carga na seleção de modelos e por diâmetro no teste entre montagens. A diferença entre CV embaralhada e por carga (1,5–2,8 p.p.) e o colapso entre montagens ilustram o argumento.

## Onde é usado no relatório

- Seções 3.3.6, 4.5.2, 4.6, 5.6 (montagens) e 5.7 (inferência).

## Cuidados ao citar

- Artigo de ecologia; citar pelo princípio estatístico, que é geral.

## Pendências

- [ ] Nenhuma.
