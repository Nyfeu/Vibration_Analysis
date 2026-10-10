# Fichamento — Randall (2011) — Vibration-based Condition Monitoring

| | |
|---|---|
| **Referência (ABNT)** | RANDALL, R. B. *Vibration-based Condition Monitoring: Industrial, Aerospace and Automotive Applications*. Chichester: John Wiley & Sons, 2011. |
| **DOI / acesso** | [10.1002/9780470977668](https://doi.org/10.1002/9780470977668) |
| **Chave no `.bib`** | `randall2011livro` |
| **Arquivo** | não versionado (PDFs ficam em `docs/articles/`, fora do Git) |
| **Fichado por** | Claude Code (assistente de IA), a pedido do grupo |
| **Revisado por** | _preencher_ |
| **Última atualização** | 2026-10-10 |
| **Por que ler** | Livro-texto de referência em monitoramento por vibração, indicado no enunciado. Sustenta a escolha dos indicadores do domínio do tempo e o contexto geral. |

> **Origem deste fichamento.** Redigido com assistência de IA (Claude Code), a partir do
> conhecimento estabelecido sobre a obra, sem acesso ao texto completo nesta sessão.
> Por isso **não há citações diretas nem números de página**: tudo é paráfrase. Antes
> de citar algo específico no relatório, conferir no original (DOI abaixo) e registrar
> a página. Ver `docs/uso_de_ia.md`.

---

## Ideias principais

1. Apresenta o monitoramento de condição por vibração de ponta a ponta: medição, processamento de sinais, diagnóstico e prognóstico.
2. Trata dos indicadores escalares clássicos (RMS, pico, fator de crista, curtose) e de suas limitações: são simples, mas pouco específicos.
3. Dedica capítulos à análise de envelope, ao cepstro e à curtose espectral aplicados a rolamentos e engrenagens.
4. Enfatiza que o diagnóstico confiável vem de relacionar o sinal à cinemática da máquina (frequências características).

## Pontos relevantes para o projeto

- A curtose e o fator de crista medem impulsividade e crescem com impactos de defeitos localizados; o RMS mede nível global e é sensível a qualquer mudança de amplitude.
- → Projeto: justifica as cinco features de tempo e, ao mesmo tempo, antecipa o problema que encontramos — o RMS separa classes por amplitude, não por defeito.

## Onde é usado no relatório

- Cap. 1 (Introdução): contexto do monitoramento por vibração.
- Seção 4.4.1: justificativa das features de tempo.

## Cuidados ao citar

- É um livro extenso; citar o capítulo específico quando a afirmação for pontual.

## Pendências

- [ ] Conferir os capítulos sobre indicadores escalares e envelope e anotar páginas.
