# Fichamento — Zhang et al. (2017) — WDCNN

| | |
|---|---|
| **Referência (ABNT)** | ZHANG, W.; PENG, G.; LI, C.; CHEN, Y.; ZHANG, Z. A new deep learning model for fault diagnosis with good anti-noise and domain adaptation ability on raw vibration signals. *Sensors*, v. 17, n. 2, art. 425, 2017. |
| **DOI / acesso** | [10.3390/s17020425](https://doi.org/10.3390/s17020425) |
| **Chave no `.bib`** | `zhang2017` |
| **Arquivo** | não versionado (PDFs ficam em `docs/articles/`, fora do Git) |
| **Fichado por** | Claude Code (assistente de IA), a pedido do grupo |
| **Revisado por** | _preencher_ |
| **Última atualização** | 2026-10-10 |
| **Por que ler** | Arquitetura WDCNN, base da nossa CNN 1D; avaliada no próprio CWRU. |

> **Origem deste fichamento.** Redigido com assistência de IA (Claude Code), a partir do
> conhecimento estabelecido sobre a obra, sem acesso ao texto completo nesta sessão.
> Por isso **não há citações diretas nem números de página**: tudo é paráfrase. Antes
> de citar algo específico no relatório, conferir no original (DOI abaixo) e registrar
> a página. Ver `docs/uso_de_ia.md`.

---

## Ideias principais

1. CNN 1D com primeira camada de kernel largo (banco de filtros aprendido) seguida de camadas pequenas, sobre o sinal bruto de vibração.
2. Avaliada no CWRU com alta acurácia, robustez a ruído e adaptação entre cargas.

## Pontos relevantes para o projeto

- → Projeto: copiamos a ideia do kernel largo inicial. O artigo reporta generalização entre cargas no CWRU — nosso teste entre montagens mostra que essa generalização não garante diagnóstico do defeito, pois cada montagem aparece em todas as cargas.

## Onde é usado no relatório

- Seções 3.3.4 e 4.5.3.

## Cuidados ao citar

- Conferir o protocolo de divisão do artigo (por carga? por janela?) antes de comparar números com os nossos.

## Pendências

- [ ] **Conferir o split usado no artigo** — é um bom exemplo para a discussão se ele não separar montagens.
