# Fichamento — Cortes & Vapnik (1995) — Support-vector networks

| | |
|---|---|
| **Referência (ABNT)** | CORTES, C.; VAPNIK, V. Support-vector networks. *Machine Learning*, v. 20, n. 3, p. 273–297, 1995. |
| **DOI / acesso** | [10.1007/BF00994018](https://doi.org/10.1007/BF00994018) |
| **Chave no `.bib`** | `cortes1995` |
| **Arquivo** | não versionado (PDFs ficam em `docs/articles/`, fora do Git) |
| **Fichado por** | Claude Code (assistente de IA), a pedido do grupo |
| **Revisado por** | _preencher_ |
| **Última atualização** | 2026-10-10 |
| **Por que ler** | Artigo original da SVM de margem suave. |

> **Origem deste fichamento.** Redigido com assistência de IA (Claude Code), a partir do
> conhecimento estabelecido sobre a obra, sem acesso ao texto completo nesta sessão.
> Por isso **não há citações diretas nem números de página**: tudo é paráfrase. Antes
> de citar algo específico no relatório, conferir no original (DOI abaixo) e registrar
> a página. Ver `docs/uso_de_ia.md`.

---

## Ideias principais

1. Classificador de margem máxima com variáveis de folga (margem suave, parâmetro C).
2. Uso de kernels para fronteiras não lineares sem mapear explicitamente as features.

## Pontos relevantes para o projeto

- → Projeto: SVM RBF com C e γ ajustados por GridSearchCV (C = 10, γ = 0,1 com tempo+envelope).

## Onde é usado no relatório

- Seção 3.3.4.

## Cuidados ao citar

- Nenhum.

## Pendências

- [ ] Nenhuma.
