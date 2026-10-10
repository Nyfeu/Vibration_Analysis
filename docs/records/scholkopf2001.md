# Fichamento — Schölkopf et al. (2001) — One-Class SVM

| | |
|---|---|
| **Referência (ABNT)** | SCHÖLKOPF, B.; PLATT, J. C.; SHAWE-TAYLOR, J.; SMOLA, A. J.; WILLIAMSON, R. C. Estimating the support of a high-dimensional distribution. *Neural Computation*, v. 13, n. 7, p. 1443–1471, 2001. |
| **DOI / acesso** | [10.1162/089976601750264965](https://doi.org/10.1162/089976601750264965) |
| **Chave no `.bib`** | `scholkopf2001` |
| **Arquivo** | não versionado (PDFs ficam em `docs/articles/`, fora do Git) |
| **Fichado por** | Claude Code (assistente de IA), a pedido do grupo |
| **Revisado por** | André Maiolini (sessão de trabalho) |
| **Última atualização** | 2026-10-10 |
| **Por que ler** | Artigo original do One-Class SVM. |

> **Origem deste fichamento.** Redigido com assistência de IA (Claude Code), a partir do
> conhecimento estabelecido sobre a obra, sem acesso ao texto completo nesta sessão.
> Por isso **não há citações diretas nem números de página**: tudo é paráfrase. Antes
> de citar algo específico no relatório, conferir no original (DOI abaixo) e registrar
> a página. Ver `docs/uso_de_ia.md`.

---

## Ideias principais

1. Estima uma região que contém a maior parte dos dados de treino, separando-os da origem no espaço de kernel com margem máxima.
2. O parâmetro ν limita a fração de pontos de treino fora da região e a fração de vetores de suporte.

## Pontos relevantes para o projeto

- → Projeto: kernel RBF, ν = 0,05. Teve a fronteira mais justa e a maior FPR no normal de teste (até 0,81): o limiar não se transfere para a quarta gravação normal.

## Onde é usado no relatório

- Seção 3.3.3.

## Cuidados ao citar

- Sensível a γ e ν; não ajustamos por falta de falhas rotuladas no cenário one-class.

## Pendências

- [ ] Nenhuma.
