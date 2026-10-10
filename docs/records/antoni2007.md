# Fichamento — Antoni (2007) — Fast kurtogram

| | |
|---|---|
| **Referência (ABNT)** | ANTONI, J. Fast computation of the kurtogram for the detection of transient faults. *Mechanical Systems and Signal Processing*, v. 21, n. 1, p. 108–124, 2007. |
| **DOI / acesso** | [10.1016/j.ymssp.2005.12.002](https://doi.org/10.1016/j.ymssp.2005.12.002) |
| **Chave no `.bib`** | `antoni2007` |
| **Arquivo** | não versionado (PDFs ficam em `docs/articles/`, fora do Git) |
| **Fichado por** | Claude Code (assistente de IA), a pedido do grupo |
| **Revisado por** | André Maiolini (sessão de trabalho) |
| **Última atualização** | 2026-10-10 |
| **Por que ler** | Algoritmo do kurtograma rápido, o padrão de fato para escolha automática da banda de demodulação; citado por Smith e Randall. |

> **Origem deste fichamento.** Redigido com assistência de IA (Claude Code), a partir do
> conhecimento estabelecido sobre a obra, sem acesso ao texto completo nesta sessão.
> Por isso **não há citações diretas nem números de página**: tudo é paráfrase. Antes
> de citar algo específico no relatório, conferir no original (DOI abaixo) e registrar
> a página. Ver `docs/uso_de_ia.md`.

---

## Ideias principais

1. Propõe calcular o kurtograma com um banco de filtros em árvore (decomposição 1/3-binária), com custo comparável a uma FFT.
2. Torna prático varrer muitas combinações de frequência central e largura de banda.
3. Valida em sinais de rolamentos e engrenagens com transitórios.

## Pontos relevantes para o projeto

- → Projeto: citado como a forma usual do kurtograma. Não implementamos o banco de filtros em árvore; usamos a STFT com três resoluções. Registrado como simplificação.

## Onde é usado no relatório

- Seções 3.3.2 e 4.4.3; trabalhos futuros.

## Cuidados ao citar

- Não dizer que implementamos o 'fast kurtogram': implementamos uma SK por STFT.

## Pendências

- [ ] Nenhuma referência de página usada no relatório.
