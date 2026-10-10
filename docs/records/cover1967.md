# Fichamento — Cover & Hart (1967) — Nearest neighbor

| | |
|---|---|
| **Referência (ABNT)** | COVER, T. M.; HART, P. E. Nearest neighbor pattern classification. *IEEE Transactions on Information Theory*, v. 13, n. 1, p. 21–27, 1967. |
| **DOI / acesso** | [10.1109/TIT.1967.1053964](https://doi.org/10.1109/TIT.1967.1053964) |
| **Chave no `.bib`** | `cover1967` |
| **Arquivo** | não versionado (PDFs ficam em `docs/articles/`, fora do Git) |
| **Fichado por** | Claude Code (assistente de IA), a pedido do grupo |
| **Revisado por** | André Maiolini (sessão de trabalho) |
| **Última atualização** | 2026-10-10 |
| **Por que ler** | Referência clássica do classificador por vizinhos mais próximos (KNN), um dos candidatos da seleção de modelos. |

> **Origem deste fichamento.** Redigido com assistência de IA (Claude Code), a partir do
> conhecimento estabelecido sobre a obra, sem acesso ao texto completo nesta sessão.
> Por isso **não há citações diretas nem números de página**: tudo é paráfrase. Antes
> de citar algo específico no relatório, conferir no original (DOI abaixo) e registrar
> a página. Ver `docs/uso_de_ia.md`.

---

## Ideias principais

1. Analisa a regra do vizinho mais próximo e mostra que, com amostras infinitas, seu erro é no máximo o dobro do erro de Bayes.

## Pontos relevantes para o projeto

- → Projeto: KNN com k = 3 e k = 9 entrou na seleção (como nas aulas); no teste entre montagens, o KNN (k = 9) com tempo+envelope foi o melhor modelo treinado (0,54), ainda abaixo da regra física.

## Onde é usado no relatório

- Seção 3.3.4.

## Cuidados ao citar

- KNN depende da escala: por isso está dentro do Pipeline com StandardScaler.

## Pendências

- [ ] Nenhuma.
