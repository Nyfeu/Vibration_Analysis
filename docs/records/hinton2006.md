# Fichamento — Hinton & Salakhutdinov (2006) — Autoencoders profundos

| | |
|---|---|
| **Referência (ABNT)** | HINTON, G. E.; SALAKHUTDINOV, R. R. Reducing the dimensionality of data with neural networks. *Science*, v. 313, n. 5786, p. 504–507, 2006. |
| **DOI / acesso** | [10.1126/science.1127647](https://doi.org/10.1126/science.1127647) |
| **Chave no `.bib`** | `hinton2006` |
| **Arquivo** | não versionado (PDFs ficam em `docs/articles/`, fora do Git) |
| **Fichado por** | Claude Code (assistente de IA), a pedido do grupo |
| **Revisado por** | _preencher_ |
| **Última atualização** | 2026-10-10 |
| **Por que ler** | Referência clássica de autoencoders para redução de dimensionalidade. |

> **Origem deste fichamento.** Redigido com assistência de IA (Claude Code), a partir do
> conhecimento estabelecido sobre a obra, sem acesso ao texto completo nesta sessão.
> Por isso **não há citações diretas nem números de página**: tudo é paráfrase. Antes
> de citar algo específico no relatório, conferir no original (DOI abaixo) e registrar
> a página. Ver `docs/uso_de_ia.md`.

---

## Ideias principais

1. Mostra que redes com uma camada central estreita, treinadas para reconstruir a entrada, aprendem representações compactas melhores que PCA.
2. Propõe pré-treinamento camada a camada para viabilizar redes profundas (na época).

## Pontos relevantes para o projeto

- → Projeto: nosso autoencoder é raso (6-3-6) e treinado direto, sem pré-treinamento; a ideia usada é a de reconstrução por gargalo.

## Onde é usado no relatório

- Seção 3.3.3.

## Cuidados ao citar

- O artigo não trata de detecção de anomalia; para esse uso, ver Sakurada e Yairi (2014).

## Pendências

- [ ] Nenhuma.
