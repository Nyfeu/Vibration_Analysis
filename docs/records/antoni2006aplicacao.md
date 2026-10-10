# Fichamento — Antoni & Randall (2006) — SK aplicada a máquinas rotativas

| | |
|---|---|
| **Referência (ABNT)** | ANTONI, J.; RANDALL, R. B. The spectral kurtosis: application to the vibratory surveillance and diagnostics of rotating machines. *Mechanical Systems and Signal Processing*, v. 20, n. 2, p. 308–331, 2006. |
| **DOI / acesso** | [10.1016/j.ymssp.2004.09.002](https://doi.org/10.1016/j.ymssp.2004.09.002) |
| **Chave no `.bib`** | `antoni2006aplicacao` |
| **Arquivo** | não versionado (PDFs ficam em `docs/articles/`, fora do Git) |
| **Fichado por** | Claude Code (assistente de IA), a pedido do grupo |
| **Revisado por** | _preencher_ |
| **Última atualização** | 2026-10-10 |
| **Por que ler** | Mostra como usar a SK para escolher a banda de demodulação em diagnóstico de rolamentos. |

> **Origem deste fichamento.** Redigido com assistência de IA (Claude Code), a partir do
> conhecimento estabelecido sobre a obra, sem acesso ao texto completo nesta sessão.
> Por isso **não há citações diretas nem números de página**: tudo é paráfrase. Antes
> de citar algo específico no relatório, conferir no original (DOI abaixo) e registrar
> a página. Ver `docs/uso_de_ia.md`.

---

## Ideias principais

1. Aplica a SK a sinais de máquinas rotativas e propõe o kurtograma: a SK calculada para várias resoluções, para escolher frequência central e largura de banda.
2. A banda escolhida serve de filtro antes da análise de envelope, melhorando a detecção de defeitos incipientes.
3. Discute o efeito de componentes determinísticos fortes, que podem mascarar a SK.

## Pontos relevantes para o projeto

- → Projeto: fundamenta a escolha da banda pela SK e a observação de que, sem remover componentes discretos (DRS), a SK pode não indicar a banda certa — o que vimos na 197.

## Onde é usado no relatório

- Seção 3.3.2 (kurtograma).

## Cuidados ao citar

- Nossa implementação é uma versão simplificada (3 resoluções, STFT), não o kurtograma completo.

## Pendências

- [ ] Conferir o procedimento de escolha da banda e o papel da separação de componentes discretos.
