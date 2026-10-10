# Fichamento — Breiman et al. (1984) — Classification and Regression Trees (CART)

| | |
|---|---|
| **Referência (ABNT)** | BREIMAN, L.; FRIEDMAN, J. H.; OLSHEN, R. A.; STONE, C. J. *Classification and Regression Trees*. Belmont: Wadsworth, 1984. |
| **DOI / acesso** | (livro; ISBN 0-534-98053-8) |
| **Chave no `.bib`** | `breiman1984` |
| **Arquivo** | não versionado (PDFs ficam em `docs/articles/`, fora do Git) |
| **Fichado por** | Claude Code (assistente de IA), a pedido do grupo |
| **Revisado por** | André Maiolini (sessão de trabalho) |
| **Última atualização** | 2026-10-10 |
| **Por que ler** | Livro que define o CART, com cortes binários e o índice de Gini — o critério padrão do scikit-learn e das árvores do Random Forest. |

> **Origem deste fichamento.** Redigido com assistência de IA (Claude Code), a partir do
> conhecimento estabelecido sobre a obra, sem acesso ao texto completo nesta sessão.
> Por isso **não há citações diretas nem números de página**: tudo é paráfrase. Antes
> de citar algo específico no relatório, conferir no original (DOI abaixo) e registrar
> a página. Ver `docs/uso_de_ia.md`.

---

## Ideias principais

1. Árvores binárias para classificação e regressão, com cortes por limiar em variáveis contínuas.
2. Índice de Gini como medida de impureza para classificação; poda por custo-complexidade.
3. Importância de variáveis pela redução de impureza.

## Pontos relevantes para o projeto

- → Projeto: as árvores do nosso Random Forest usam Gini (padrão do scikit-learn); a árvore interpretativa usa entropia. Os dois critérios costumam escolher cortes parecidos.

## Onde é usado no relatório

- Seção 3.3.4 (Gini e árvores).

## Cuidados ao citar

- Livro; citar pelo método (CART, Gini), sem página.

## Pendências

- [ ] Nenhuma.
