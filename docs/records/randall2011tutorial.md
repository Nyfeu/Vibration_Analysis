# Fichamento — Randall & Antoni (2011) — Rolling element bearing diagnostics: a tutorial

| | |
|---|---|
| **Referência (ABNT)** | RANDALL, R. B.; ANTONI, J. Rolling element bearing diagnostics — A tutorial. *Mechanical Systems and Signal Processing*, v. 25, n. 2, p. 485–520, 2011. |
| **DOI / acesso** | [10.1016/j.ymssp.2010.07.017](https://doi.org/10.1016/j.ymssp.2010.07.017) |
| **Chave no `.bib`** | `randall2011tutorial` |
| **Arquivo** | não versionado (PDFs ficam em `docs/articles/`, fora do Git) |
| **Fichado por** | Claude Code (assistente de IA), a pedido do grupo |
| **Revisado por** | _preencher_ |
| **Última atualização** | 2026-10-10 |
| **Por que ler** | Tutorial de referência sobre diagnóstico de rolamentos; base da fundamentação física e da análise de envelope. Fonte original da Figura 2 do relatório (reproduzida por Smith e Randall). |

> **Origem deste fichamento.** Redigido com assistência de IA (Claude Code), a partir do
> conhecimento estabelecido sobre a obra, sem acesso ao texto completo nesta sessão.
> Por isso **não há citações diretas nem números de página**: tudo é paráfrase. Antes
> de citar algo específico no relatório, conferir no original (DOI abaixo) e registrar
> a página. Ver `docs/uso_de_ia.md`.

---

## Ideias principais

1. Explica por que defeitos localizados geram séries de impactos que excitam ressonâncias, e por que a informação está na modulação (envelope), não no espectro bruto.
2. Apresenta as frequências características (BPFO, BPFI, BSF, FTF) e o efeito do escorregamento, que torna o sinal pseudocíclico (cicloestacionário).
3. Propõe um procedimento semiautomático: separar componentes discretos (engrenagens, eixo), escolher a banda pela curtose espectral/kurtograma e fazer o espectro do envelope ao quadrado.
4. Discute o espectro do envelope ao quadrado como ferramenta principal e suas relações com a análise cicloestacionária.

## Pontos relevantes para o projeto

- O escorregamento das esferas borra os harmônicos de alta ordem no espectro bruto, mas o envelope preserva a taxa de repetição.
- Smith e Randall (2015) observam que a equação da BSF neste tutorial omite o fator f_r — usar a forma corrigida (como fizemos em `src/features.py`).
- → Projeto: o 'método de referência' de Smith e Randall deriva deste tutorial; nossa ausência de DRS explica por que o kurtograma não recuperou as gravações 121 e 197.

## Onde é usado no relatório

- Seções 3.1, 3.2 e 3.3.2 (assinatura, frequências e envelope).
- Fonte da Figura 2.

## Cuidados ao citar

- Não usar a fórmula da BSF do tutorial sem a correção apontada por Smith e Randall (2015).

## Pendências

- [ ] Conferir a seção sobre o procedimento semiautomático e anotar páginas para a Seção 3.3.2.
