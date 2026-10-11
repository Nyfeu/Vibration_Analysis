# Fichamento — Fawcett (2006) — An introduction to ROC analysis

| | |
|---|---|
| **Referência (ABNT)** | FAWCETT, T. An introduction to ROC analysis. *Pattern Recognition Letters*, v. 27, n. 8, p. 861–874, 2006. |
| **DOI / acesso** | [10.1016/j.patrec.2005.10.010](https://doi.org/10.1016/j.patrec.2005.10.010) |
| **Chave no `.bib`** | `fawcett2006` |
| **Arquivo** | não versionado (PDFs ficam em `docs/articles/`, fora do Git) |
| **Fichado por** | Claude Code (assistente de IA), a pedido do grupo |
| **Revisado por** | André Maiolini (sessão de trabalho) |
| **Última atualização** | 2026-10-11 |
| **Por que ler** | Tutorial de referência sobre curvas ROC e AUC, as métricas principais da detecção. |

> **Origem deste fichamento.** Redigido com assistência de IA (Claude Code), a partir do
> conhecimento estabelecido sobre a obra, sem acesso ao texto completo nesta sessão.
> Por isso **não há citações diretas nem números de página**: tudo é paráfrase. Antes
> de citar algo específico no relatório, conferir no original (DOI abaixo) e registrar
> a página. Ver `docs/uso_de_ia.md`.

---

## Ideias principais

1. Um classificador que produz um *score* gera um ponto (FPR, TPR) para cada limiar; a curva ROC liga esses pontos, de (0, 0) a (1, 1).
2. A diagonal corresponde a um classificador aleatório; quanto mais a curva se aproxima do canto superior esquerdo, melhor a separação.
3. A AUC equivale à probabilidade de um exemplo positivo sorteado receber *score* maior que um negativo sorteado (estatística de Wilcoxon–Mann–Whitney).
4. A curva ROC não depende da proporção de classes; precisão e medidas derivadas dependem.

## Pontos relevantes para o projeto

- → Projeto: a AUC compara detectores independentemente do limiar, e o ponto de operação (limiar p99) é marcado nas curvas.
- → Projeto: como 90% das janelas de teste são de falha, TPR, FPR e AUC são preferidas à precisão.

## Onde é usado no relatório

- Seções 3.3.3 (detecção one-class) e 5.4 (detecção).

## Cuidados ao citar

- A AUC resume todos os limiares; o desempenho real depende do limiar escolhido, que deve ser reportado à parte.

## Pendências

- [ ] Nenhuma.
