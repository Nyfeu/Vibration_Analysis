# Fichamento — Virtanen et al. (2020) — SciPy 1.0

| | |
|---|---|
| **Referência (ABNT)** | VIRTANEN, P. et al. SciPy 1.0: fundamental algorithms for scientific computing in Python. *Nature Methods*, v. 17, p. 261–272, 2020. |
| **DOI / acesso** | [10.1038/s41592-019-0686-2](https://doi.org/10.1038/s41592-019-0686-2) |
| **Chave no `.bib`** | `virtanen2020` |
| **Arquivo** | não versionado (PDFs ficam em `docs/articles/`, fora do Git) |
| **Fichado por** | Claude Code (assistente de IA), a pedido do grupo |
| **Revisado por** | André Maiolini (sessão de trabalho) |
| **Última atualização** | 2026-10-10 |
| **Por que ler** | Citação oficial do SciPy, cujas funções de sinal (`decimate`, `welch`, `hilbert`, `stft`, filtros) usamos. |

> **Origem deste fichamento.** Redigido com assistência de IA (Claude Code), a partir do
> conhecimento estabelecido sobre a obra, sem acesso ao texto completo nesta sessão.
> Por isso **não há citações diretas nem números de página**: tudo é paráfrase. Antes
> de citar algo específico no relatório, conferir no original (DOI abaixo) e registrar
> a página. Ver `docs/uso_de_ia.md`.

---

## Ideias principais

1. Descreve a biblioteca SciPy, seus módulos e o processo de desenvolvimento.
2. É a referência recomendada pelos mantenedores para citar o SciPy.

## Pontos relevantes para o projeto

- → Projeto: a configuração padrão de `scipy.signal.decimate` (Chebyshev I ordem 8, corte 0,8×Nyquist, fase zero) foi conferida no código-fonte da versão instalada, não neste artigo.

## Onde é usado no relatório

- Seção 4.1.2 (decimação).

## Cuidados ao citar

- Detalhes de implementação mudam entre versões; citar a versão usada (requirements.txt).

## Pendências

- [ ] Nenhuma.
