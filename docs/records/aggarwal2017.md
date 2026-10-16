# Fichamento — Aggarwal (2017) — Outlier Analysis

| | |
|---|---|
| **Referência (ABNT)** | AGGARWAL, C. C. *Outlier Analysis*. 2. ed. Cham: Springer, 2017. |
| **DOI / acesso** | [10.1007/978-3-319-47578-3](https://doi.org/10.1007/978-3-319-47578-3) |
| **Chave no `.bib`** | `aggarwal2017` |
| **Arquivo** | não versionado (PDFs ficam em `docs/articles/`, fora do Git) |
| **Fichado por** | Claude Code (assistente de IA), a pedido do grupo |
| **Revisado por** | André Maiolini (sessão de trabalho) |
| **Última atualização** | 2026-10-16 |
| **Por que ler** | Livro-texto geral de detecção de anomalias; segunda referência de base da área. |

> **Origem deste fichamento.** Redigido com assistência de IA (Claude Code), a partir do
> conhecimento estabelecido sobre a obra, sem acesso ao texto completo nesta sessão.
> Por isso **não há citações diretas nem números de página**: tudo é paráfrase. Antes
> de citar algo específico no relatório, conferir no original e registrar a página.
> Ver `docs/uso_de_ia.md`.

---

## Ideias principais

1. Organiza os métodos de detecção de anomalias em famílias: probabilísticos e estatísticos (incluindo a distância de Mahalanobis), baseados em distância e densidade, baseados em isolamento (Isolation Forest), em fronteiras de uma classe (One-Class SVM) e em reconstrução (autoencoders).
2. Discute a escolha do limiar sobre o *score* de anomalia e a avaliação por curvas ROC.
3. Trata de *ensembles* de detectores e do caso de alta dimensão.

## Pontos relevantes para o projeto

- → Projeto: fundamenta os quatro detectores one-class comparados (Mahalanobis, Isolation Forest, One-Class SVM e autoencoder).

## Onde é usado no relatório

- Seção 3.3 (áreas de referência) e 3.3.3 (detecção one-class, Isolation Forest).

## Pendências

- [ ] Conferir no original os capítulos citados no relatório.
