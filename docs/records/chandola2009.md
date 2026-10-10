# Fichamento — Chandola, Banerjee & Kumar (2009) — Anomaly detection: a survey

| | |
|---|---|
| **Referência (ABNT)** | CHANDOLA, V.; BANERJEE, A.; KUMAR, V. Anomaly detection: a survey. *ACM Computing Surveys*, v. 41, n. 3, art. 15, 2009. |
| **DOI / acesso** | [10.1145/1541880.1541882](https://doi.org/10.1145/1541880.1541882) |
| **Chave no `.bib`** | `chandola2009` |
| **Arquivo** | não versionado (PDFs ficam em `docs/articles/`, fora do Git) |
| **Fichado por** | Claude Code (assistente de IA), a pedido do grupo |
| **Revisado por** | _preencher_ |
| **Última atualização** | 2026-10-10 |
| **Por que ler** | Survey de referência em detecção de anomalias; enquadra a detecção one-class do projeto. |

> **Origem deste fichamento.** Redigido com assistência de IA (Claude Code), a partir do
> conhecimento estabelecido sobre a obra, sem acesso ao texto completo nesta sessão.
> Por isso **não há citações diretas nem números de página**: tudo é paráfrase. Antes
> de citar algo específico no relatório, conferir no original (DOI abaixo) e registrar
> a página. Ver `docs/uso_de_ia.md`.

---

## Ideias principais

1. Organiza as técnicas por modo de aprendizado (supervisionado, semi-supervisionado com só a classe normal, não supervisionado) e por família (estatísticas, vizinhança, classificação, agrupamento, espectrais).
2. Destaca o cenário semi-supervisionado — treinar só com dados normais — como o mais aplicável quando anomalias rotuladas são raras.
3. Discute a saída como escore versus rótulo e a necessidade de um limiar.

## Pontos relevantes para o projeto

- → Projeto: nosso cenário é exatamente o semi-supervisionado com só normais (regra 3 do CLAUDE.md); a saída é um escore com limiar no percentil 99 dos normais.

## Onde é usado no relatório

- Seção 3.3.3 (detecção one-class).

## Cuidados ao citar

- É um survey: usar para enquadrar, e as referências próprias para cada detector.

## Pendências

- [ ] Nenhuma.
