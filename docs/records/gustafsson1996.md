# Fichamento — Gustafsson (1996) — Filtragem forward-backward

| | |
|---|---|
| **Referência (ABNT)** | GUSTAFSSON, F. Determining the initial states in forward-backward filtering. *IEEE Transactions on Signal Processing*, v. 44, n. 4, p. 988–992, 1996. |
| **DOI / acesso** | [10.1109/78.492552](https://doi.org/10.1109/78.492552) |
| **Chave no `.bib`** | `gustafsson1996` |
| **Arquivo** | não versionado (PDFs ficam em `docs/articles/`, fora do Git) |
| **Fichado por** | Claude Code (assistente de IA), a pedido do grupo |
| **Revisado por** | _preencher_ |
| **Última atualização** | 2026-10-10 |
| **Por que ler** | Fundamenta a filtragem de fase zero (filtfilt), usada na decimação e na banda comum. É a referência do próprio `scipy.signal.filtfilt`. |

> **Origem deste fichamento.** Redigido com assistência de IA (Claude Code), a partir do
> conhecimento estabelecido sobre a obra, sem acesso ao texto completo nesta sessão.
> Por isso **não há citações diretas nem números de página**: tudo é paráfrase. Antes
> de citar algo específico no relatório, conferir no original (DOI abaixo) e registrar
> a página. Ver `docs/uso_de_ia.md`.

---

## Ideias principais

1. Filtrar o sinal para frente e depois para trás cancela a fase do filtro e dá resposta de fase zero, com magnitude ao quadrado.
2. Propõe como escolher os estados iniciais para minimizar os transitórios nas bordas do sinal.

## Pontos relevantes para o projeto

- → Projeto: a decimação (`decimate`, zero_phase) e a banda comum (`sosfiltfilt`) usam essa técnica, o que preserva a forma dos impactos.

## Onde é usado no relatório

- Seção 3.3.1 (fase do filtro).

## Cuidados ao citar

- A contribuição central do artigo é a inicialização; a ideia de fase zero por filtragem dupla é anterior a ele.

## Pendências

- [ ] Nenhuma.
