# Fichamento — Antoni (2006) — Curtose espectral

| | |
|---|---|
| **Referência (ABNT)** | ANTONI, J. The spectral kurtosis: a useful tool for characterising non-stationary signals. *Mechanical Systems and Signal Processing*, v. 20, n. 2, p. 282–307, 2006. |
| **DOI / acesso** | [10.1016/j.ymssp.2004.09.001](https://doi.org/10.1016/j.ymssp.2004.09.001) |
| **Chave no `.bib`** | `antoni2006sk` |
| **Arquivo** | não versionado (PDFs ficam em `docs/articles/`, fora do Git) |
| **Fichado por** | Claude Code (assistente de IA), a pedido do grupo |
| **Revisado por** | _preencher_ |
| **Última atualização** | 2026-10-10 |
| **Por que ler** | Define formalmente a curtose espectral (SK), base do nosso kurtograma. |

> **Origem deste fichamento.** Redigido com assistência de IA (Claude Code), a partir do
> conhecimento estabelecido sobre a obra, sem acesso ao texto completo nesta sessão.
> Por isso **não há citações diretas nem números de página**: tudo é paráfrase. Antes
> de citar algo específico no relatório, conferir no original (DOI abaixo) e registrar
> a página. Ver `docs/uso_de_ia.md`.

---

## Ideias principais

1. Define a SK como o momento de quarta ordem normalizado das componentes de frequência de um sinal, dependente da frequência.
2. Mostra que a SK é próxima de zero para ruído estacionário gaussiano e cresce em faixas onde há transitórios.
3. Apresenta estimadores, entre eles o baseado na STFT, e discute o compromisso entre resolução em frequência e detecção de transitórios.

## Pontos relevantes para o projeto

- → Projeto: usamos o estimador por STFT, SK(f) = ⟨|X|⁴⟩/⟨|X|²⟩² − 2 (`curtose_espectral` em `src/features.py`). O valor ~0,1 na gravação 197 indica ausência de banda impulsiva.

## Onde é usado no relatório

- Seção 3.3.2 e 4.4.3 (kurtograma).

## Cuidados ao citar

- A constante −2 vale para sinais complexos (STFT); conferir a convenção no artigo.

## Pendências

- [ ] Conferir a definição e a normalização do estimador por STFT.
