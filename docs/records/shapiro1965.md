# Fichamento — Shapiro & Wilk (1965) — Teste de normalidade

| | |
|---|---|
| **Referência (ABNT)** | SHAPIRO, S. S.; WILK, M. B. An analysis of variance test for normality (complete samples). *Biometrika*, v. 52, n. 3/4, p. 591–611, 1965. |
| **DOI / acesso** | [10.1093/biomet/52.3-4.591](https://doi.org/10.1093/biomet/52.3-4.591) |
| **Chave no `.bib`** | `shapiro1965` |
| **Arquivo** | não versionado (PDFs ficam em `docs/articles/`, fora do Git) |
| **Fichado por** | Claude Code (assistente de IA), a pedido do grupo |
| **Revisado por** | André Maiolini (sessão de trabalho) |
| **Última atualização** | 2026-10-10 |
| **Por que ler** | Teste de normalidade usado para verificar o pressuposto do limiar qui-quadrado do Mahalanobis. |

> **Origem deste fichamento.** Redigido com assistência de IA (Claude Code), a partir do
> conhecimento estabelecido sobre a obra, sem acesso ao texto completo nesta sessão.
> Por isso **não há citações diretas nem números de página**: tudo é paráfrase. Antes
> de citar algo específico no relatório, conferir no original (DOI abaixo) e registrar
> a página. Ver `docs/uso_de_ia.md`.

---

## Ideias principais

1. A estatística W compara a variância estimada pelos quantis ordenados com a variância amostral; valores baixos indicam não normalidade.
2. É um dos testes de normalidade com maior poder para amostras pequenas e médias.

## Pontos relevantes para o projeto

- → Projeto: rejeita a normalidade em 5 de 8 features normais; o limiar qui-quadrado daria 6,2% de alarmes no treino em vez de 1%, o que justifica o limiar empírico.

## Onde é usado no relatório

- Seções 3.3.5, 4.6 e 5.4 (pressupostos do Mahalanobis).

## Cuidados ao citar

- Com amostras grandes e correlacionadas, rejeita desvios pequenos; aqui a consequência prática (6,2% contra 1%) é que importa.

## Pendências

- [ ] Nenhuma.
