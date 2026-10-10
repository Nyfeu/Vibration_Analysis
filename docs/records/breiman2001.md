# Fichamento — Breiman (2001) — Random Forests

| | |
|---|---|
| **Referência (ABNT)** | BREIMAN, L. Random forests. *Machine Learning*, v. 45, n. 1, p. 5–32, 2001. |
| **DOI / acesso** | [10.1023/A:1010933404324](https://doi.org/10.1023/A:1010933404324) |
| **Chave no `.bib`** | `breiman2001` |
| **Arquivo** | não versionado (PDFs ficam em `docs/articles/`, fora do Git) |
| **Fichado por** | Claude Code (assistente de IA), a pedido do grupo |
| **Revisado por** | _preencher_ |
| **Última atualização** | 2026-10-10 |
| **Por que ler** | Artigo original do Random Forest, nosso classificador selecionado. |

> **Origem deste fichamento.** Redigido com assistência de IA (Claude Code), a partir do
> conhecimento estabelecido sobre a obra, sem acesso ao texto completo nesta sessão.
> Por isso **não há citações diretas nem números de página**: tudo é paráfrase. Antes
> de citar algo específico no relatório, conferir no original (DOI abaixo) e registrar
> a página. Ver `docs/uso_de_ia.md`.

---

## Ideias principais

1. Conjunto de árvores treinadas em amostras bootstrap e com subconjuntos aleatórios de features em cada divisão; previsão por voto.
2. O erro de generalização converge com o número de árvores e depende da força das árvores e da correlação entre elas.
3. Propõe a estimativa out-of-bag e medidas de importância de variáveis.

## Pontos relevantes para o projeto

- → Projeto: a importância das features (RMS + pico = 56%) foi o primeiro indício do atalho de amplitude.

## Onde é usado no relatório

- Seção 3.3.4; resultados 5.4.

## Cuidados ao citar

- A importância por impureza favorece features contínuas e correlacionadas; é indício, não prova — a prova veio das ablações e do teste entre montagens.

## Pendências

- [ ] Nenhuma.
