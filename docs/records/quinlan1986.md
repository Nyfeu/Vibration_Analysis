# Fichamento — Quinlan (1986) — Induction of decision trees (ID3)

| | |
|---|---|
| **Referência (ABNT)** | QUINLAN, J. R. Induction of decision trees. *Machine Learning*, v. 1, n. 1, p. 81–106, 1986. |
| **DOI / acesso** | [10.1007/BF00116251](https://doi.org/10.1007/BF00116251) |
| **Chave no `.bib`** | `quinlan1986` |
| **Arquivo** | não versionado (PDFs ficam em `docs/articles/`, fora do Git) |
| **Fichado por** | Claude Code (assistente de IA), a pedido do grupo |
| **Revisado por** | André Maiolini (sessão de trabalho) |
| **Última atualização** | 2026-10-10 |
| **Por que ler** | Artigo clássico que introduz o ID3 e o ganho de informação como critério de divisão de árvores de decisão — conteúdo visto em aula. |

> **Origem deste fichamento.** Redigido com assistência de IA (Claude Code), a partir do
> conhecimento estabelecido sobre a obra, sem acesso ao texto completo nesta sessão.
> Por isso **não há citações diretas nem números de página**: tudo é paráfrase. Antes
> de citar algo específico no relatório, conferir no original (DOI abaixo) e registrar
> a página. Ver `docs/uso_de_ia.md`.

---

## Ideias principais

1. Constrói árvores de decisão de cima para baixo, escolhendo em cada nó o atributo que mais reduz a entropia das classes.
2. Define o ganho de informação: entropia antes do corte menos a entropia média ponderada depois.
3. Discute o viés do ganho de informação a favor de atributos com muitos valores e trata de ruído e valores ausentes.

## Pontos relevantes para o projeto

- → Projeto: calculamos o ganho de informação de cada feature no nó raiz e uma árvore de profundidade 3 com critério de entropia. Pico e RMS dão o maior ganho; o escore de BSF, o menor. A árvore define a esfera como uma faixa de amplitude.

## Onde é usado no relatório

- Seção 3.3.5 (árvores e ganho de informação), Seção 4.5.2 e resultados de classificação (Tabela de ganho de informação, Figura da árvore).

## Cuidados ao citar

- O ID3 original trata atributos discretos; para features contínuas usamos cortes binários por limiar (como no C4.5/CART).

## Pendências

- [ ] Nenhuma.
