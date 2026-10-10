# Fichamento — Kruskal & Wallis (1952) — Teste de Kruskal–Wallis

| | |
|---|---|
| **Referência (ABNT)** | KRUSKAL, W. H.; WALLIS, W. A. Use of ranks in one-criterion variance analysis. *Journal of the American Statistical Association*, v. 47, n. 260, p. 583–621, 1952. |
| **DOI / acesso** | [10.1080/01621459.1952.10483441](https://doi.org/10.1080/01621459.1952.10483441) |
| **Chave no `.bib`** | `kruskal1952` |
| **Arquivo** | não versionado (PDFs ficam em `docs/articles/`, fora do Git) |
| **Fichado por** | Claude Code (assistente de IA), a pedido do grupo |
| **Revisado por** | André Maiolini (sessão de trabalho) |
| **Última atualização** | 2026-10-10 |
| **Por que ler** | Artigo original do teste de Kruskal–Wallis, usado na análise exploratória. |

> **Origem deste fichamento.** Redigido com assistência de IA (Claude Code), a partir do
> conhecimento estabelecido sobre a obra, sem acesso ao texto completo nesta sessão.
> Por isso **não há citações diretas nem números de página**: tudo é paráfrase. Antes
> de citar algo específico no relatório, conferir no original (DOI abaixo) e registrar
> a página. Ver `docs/uso_de_ia.md`.

---

## Ideias principais

1. Generaliza o teste de Mann–Whitney para k grupos, usando só os postos das observações.
2. A estatística H tem distribuição aproximadamente qui-quadrado com k−1 graus de liberdade sob a hipótese nula de distribuições iguais.
3. Não supõe normalidade, o que o torna adequado a dados assimétricos.

## Pontos relevantes para o projeto

- → Projeto: aplicado às medianas por gravação (n = 30) de cada feature; o escore de BSF é a única sem diferença significativa entre classes (p = 0,071).

## Onde é usado no relatório

- Seções 3.3.5, 4.6 e 5.2 (Tabela de Kruskal–Wallis).

## Cuidados ao citar

- Supõe observações independentes — por isso a unidade é a gravação, não a janela.

## Pendências

- [ ] Nenhuma.
