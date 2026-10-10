# Fichamento — Razali & Wah (2011) — Poder de testes de normalidade

| | |
|---|---|
| **Referência (ABNT)** | RAZALI, N. M.; WAH, Y. B. Power comparisons of Shapiro-Wilk, Kolmogorov-Smirnov, Lilliefors and Anderson-Darling tests. *Journal of Statistical Modeling and Analytics*, v. 2, n. 1, p. 21–33, 2011. |
| **DOI / acesso** | (sem DOI) |
| **Chave no `.bib`** | `razali2011` |
| **Arquivo** | não versionado (PDFs ficam em `docs/articles/`, fora do Git) |
| **Fichado por** | Claude Code (assistente de IA), a pedido do grupo |
| **Revisado por** | _preencher_ |
| **Última atualização** | 2026-10-10 |
| **Por que ler** | Compara por simulação o poder dos testes de normalidade usuais; segunda referência do Shapiro–Wilk. |

> **Origem deste fichamento.** Redigido com assistência de IA (Claude Code), a partir do
> conhecimento estabelecido sobre a obra, sem acesso ao texto completo nesta sessão.
> Por isso **não há citações diretas nem números de página**: tudo é paráfrase. Antes
> de citar algo específico no relatório, conferir no original (DOI abaixo) e registrar
> a página. Ver `docs/uso_de_ia.md`.

---

## Ideias principais

1. Compara Shapiro–Wilk, Kolmogorov–Smirnov, Lilliefors e Anderson–Darling em várias distribuições alternativas e tamanhos de amostra.
2. O Shapiro–Wilk tem o maior poder na maioria dos cenários; o Kolmogorov–Smirnov, o menor.

## Pontos relevantes para o projeto

- → Projeto: justifica usar o Shapiro–Wilk para verificar a normalidade das features normais antes do limiar qui-quadrado.

## Onde é usado no relatório

- Seção 3.3.8.

## Cuidados ao citar

- Resultados de simulação com amostras independentes; nossas janelas são correlacionadas.

## Pendências

- [ ] Nenhuma.
