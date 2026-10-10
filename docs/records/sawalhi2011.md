# Fichamento — Sawalhi & Randall (2011) — Pré-branqueamento por edição do cepstro

| | |
|---|---|
| **Referência (ABNT)** | SAWALHI, N.; RANDALL, R. B. Signal pre-whitening using cepstrum editing (liftering) to enhance fault detection in rolling element bearings. In: INTERNATIONAL CONGRESS ON CONDITION MONITORING AND DIAGNOSTICS ENGINEERING MANAGEMENT (COMADEM), 24., 2011, Stavanger. *Proceedings*. 2011. |
| **DOI / acesso** | (anais de congresso; sem DOI conhecido) |
| **Chave no `.bib`** | `sawalhi2011` |
| **Arquivo** | não versionado (PDFs ficam em `docs/articles/`, fora do Git) |
| **Fichado por** | Claude Code (assistente de IA), a pedido do grupo |
| **Revisado por** | André Maiolini (sessão de trabalho) |
| **Última atualização** | 2026-10-10 |
| **Por que ler** | Origem do pré-branqueamento cepstral, segundo Smith e Randall (2015, ref. [6]). Fundamenta o 'método 2'. |

> **Origem deste fichamento.** Redigido com assistência de IA (Claude Code), a partir do
> conhecimento estabelecido sobre a obra, sem acesso ao texto completo nesta sessão.
> Por isso **não há citações diretas nem números de página**: tudo é paráfrase. Antes
> de citar algo específico no relatório, conferir no original (DOI abaixo) e registrar
> a página. Ver `docs/uso_de_ia.md`.

---

## Ideias principais

1. Propõe pré-branquear o sinal editando o cepstro real: zerar o cepstro (exceto a origem) equivale a igualar a magnitude do espectro a 1, mantendo a fase.
2. Com todas as faixas de mesmo peso, as que contêm impulsos passam a dominar o sinal no tempo.
3. Remove também componentes discretas fortes e ressonâncias que mascaram o defeito.

## Pontos relevantes para o projeto

- → Projeto: é exatamente `prebranquear` em o notebook. Recuperou o BSF nas gravações 222 e 223, como no método 2 do artigo.

## Onde é usado no relatório

- Seção 3.3.2 (pré-branqueamento).

## Cuidados ao citar

- Texto de anais pode ser difícil de obter; a descrição do método também está em Borghesani et al. (2013) e em Smith e Randall (2015).

## Pendências

- [ ] Tentar obter o texto para confirmar a formulação.
