# Fichamento — Mahalanobis (1936) — Distância generalizada

| | |
|---|---|
| **Referência (ABNT)** | MAHALANOBIS, P. C. On the generalized distance in statistics. *Proceedings of the National Institute of Sciences of India*, v. 2, n. 1, p. 49–55, 1936. |
| **DOI / acesso** | (sem DOI) |
| **Chave no `.bib`** | `mahalanobis1936` |
| **Arquivo** | não versionado (PDFs ficam em `docs/articles/`, fora do Git) |
| **Fichado por** | Claude Code (assistente de IA), a pedido do grupo |
| **Revisado por** | André Maiolini (sessão de trabalho) |
| **Última atualização** | 2026-10-10 |
| **Por que ler** | Artigo original da distância de Mahalanobis, nosso detector baseline. |

> **Origem deste fichamento.** Redigido com assistência de IA (Claude Code), a partir do
> conhecimento estabelecido sobre a obra, sem acesso ao texto completo nesta sessão.
> Por isso **não há citações diretas nem números de página**: tudo é paráfrase. Antes
> de citar algo específico no relatório, conferir no original (DOI abaixo) e registrar
> a página. Ver `docs/uso_de_ia.md`.

---

## Ideias principais

1. Define uma distância entre populações/observações que leva em conta a covariância das variáveis, invariante a mudanças de escala.
2. Para uma observação x e uma população de média μ e covariância Σ: d² = (x−μ)ᵀ Σ⁻¹ (x−μ).

## Pontos relevantes para o projeto

- → Projeto: o detector `Mahalanobis` usa a média e a covariância empírica das 144 janelas normais de treino (após padronização).

## Onde é usado no relatório

- Seção 3.3.3.

## Cuidados ao citar

- A distância supõe uma nuvem aproximadamente elíptica; com poucas gravações normais a covariância reflete a montagem.

## Pendências

- [ ] Nenhuma.
