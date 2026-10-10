# Fichamento — Sakurada & Yairi (2014) — Autoencoders para detecção de anomalias

| | |
|---|---|
| **Referência (ABNT)** | SAKURADA, M.; YAIRI, T. Anomaly detection using autoencoders with nonlinear dimensionality reduction. In: WORKSHOP ON MACHINE LEARNING FOR SENSORY DATA ANALYSIS (MLSDA), 2., 2014, Gold Coast. *Proceedings*. ACM, 2014. p. 4–11. |
| **DOI / acesso** | [10.1145/2689746.2689747](https://doi.org/10.1145/2689746.2689747) |
| **Chave no `.bib`** | `sakurada2014` |
| **Arquivo** | não versionado (PDFs ficam em `docs/articles/`, fora do Git) |
| **Fichado por** | Claude Code (assistente de IA), a pedido do grupo |
| **Revisado por** | André Maiolini (sessão de trabalho) |
| **Última atualização** | 2026-10-10 |
| **Por que ler** | Aplica autoencoders à detecção de anomalias pelo erro de reconstrução; segunda referência do detector. |

> **Origem deste fichamento.** Redigido com assistência de IA (Claude Code), a partir do
> conhecimento estabelecido sobre a obra, sem acesso ao texto completo nesta sessão.
> Por isso **não há citações diretas nem números de página**: tudo é paráfrase. Antes
> de citar algo específico no relatório, conferir no original (DOI abaixo) e registrar
> a página. Ver `docs/uso_de_ia.md`.

---

## Ideias principais

1. Treina autoencoders só com dados normais e usa o erro de reconstrução como *score* de anomalia.
2. Compara com PCA linear e kernel PCA em dados de sensores (incluindo telemetria de espaçonave).

## Pontos relevantes para o projeto

- → Projeto: é exatamente o uso do nosso `Autoencoder` (*score* = erro quadrático médio de reconstrução).

## Onde é usado no relatório

- Seção 3.3.3.

## Cuidados ao citar

- Conferir os dados usados no artigo antes de citar detalhes.

## Pendências

- [ ] Conferir conjunto de dados e conclusões.
