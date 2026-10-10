# Fichamento — Efron & Tibshirani (1993) — An Introduction to the Bootstrap

| | |
|---|---|
| **Referência (ABNT)** | EFRON, B.; TIBSHIRANI, R. J. *An Introduction to the Bootstrap*. New York: Chapman & Hall, 1993. |
| **DOI / acesso** | [10.1201/9780429246593](https://doi.org/10.1201/9780429246593) |
| **Chave no `.bib`** | `efron1993` |
| **Arquivo** | não versionado (PDFs ficam em `docs/articles/`, fora do Git) |
| **Fichado por** | Claude Code (assistente de IA), a pedido do grupo |
| **Revisado por** | André Maiolini (sessão de trabalho) |
| **Última atualização** | 2026-10-10 |
| **Por que ler** | Referência clássica do bootstrap, base dos intervalos de confiança do projeto. |

> **Origem deste fichamento.** Redigido com assistência de IA (Claude Code), a partir do
> conhecimento estabelecido sobre a obra, sem acesso ao texto completo nesta sessão.
> Por isso **não há citações diretas nem números de página**: tudo é paráfrase. Antes
> de citar algo específico no relatório, conferir no original (DOI abaixo) e registrar
> a página. Ver `docs/uso_de_ia.md`.

---

## Ideias principais

1. O bootstrap aproxima a distribuição amostral de uma estatística reamostrando os dados observados com reposição.
2. Permite estimar erro-padrão e intervalos de confiança sem fórmula fechada nem suposição de normalidade.
3. Apresenta os intervalos de percentis (usados aqui) e variantes corrigidas (BCa).

## Pontos relevantes para o projeto

- → Projeto: intervalos de 95% por percentis com 2000 reamostragens para acurácia, recall, TPR e diferenças entre modelos.

## Onde é usado no relatório

- Seções 3.3.8 (estatística aplicada), 4.6 (análise estatística) e 5.7 (inferência).

## Cuidados ao citar

- O bootstrap supõe unidades independentes; com dados agrupados, reamostrar os grupos (ver Field e Welsh, 2007).

## Pendências

- [ ] Nenhuma.
