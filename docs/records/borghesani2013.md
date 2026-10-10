# Fichamento — Borghesani et al. (2013) — Pré-branqueamento cepstral com rotação variável

| | |
|---|---|
| **Referência (ABNT)** | BORGHESANI, P.; PENNACCHI, P.; RANDALL, R. B.; SAWALHI, N.; RICCI, R. Application of cepstrum pre-whitening for the diagnosis of bearing faults under variable speed conditions. *Mechanical Systems and Signal Processing*, v. 36, n. 2, p. 370–384, 2013. |
| **DOI / acesso** | [10.1016/j.ymssp.2012.11.001](https://doi.org/10.1016/j.ymssp.2012.11.001) |
| **Chave no `.bib`** | `borghesani2013` |
| **Arquivo** | não versionado (PDFs ficam em `docs/articles/`, fora do Git) |
| **Fichado por** | Claude Code (assistente de IA), a pedido do grupo |
| **Revisado por** | _preencher_ |
| **Última atualização** | 2026-10-10 |
| **Por que ler** | Segunda referência do pré-branqueamento cepstral (Smith e Randall, ref. [7]). |

> **Origem deste fichamento.** Redigido com assistência de IA (Claude Code), a partir do
> conhecimento estabelecido sobre a obra, sem acesso ao texto completo nesta sessão.
> Por isso **não há citações diretas nem números de página**: tudo é paráfrase. Antes
> de citar algo específico no relatório, conferir no original (DOI abaixo) e registrar
> a página. Ver `docs/uso_de_ia.md`.

---

## Ideias principais

1. Formaliza o pré-branqueamento cepstral (CPW) como alternativa simples à separação de componentes discretos e à escolha de banda.
2. Mostra que o CPW funciona mesmo com variação de rotação, onde métodos baseados em frequências discretas fixas falham.
3. Compara o espectro de envelope antes e depois do CPW em casos de rolamentos.

## Pontos relevantes para o projeto

- → Projeto: sustenta usar o CPW sem escolha de banda. Nossos dados têm rotação constante, então o benefício principal aqui é remover picos discretos fortes.

## Onde é usado no relatório

- Seção 3.3.2 (pré-branqueamento).

## Cuidados ao citar

- O foco do artigo é rotação variável; citar pela formulação do CPW, não pelo cenário.

## Pendências

- [ ] Conferir a equação do CPW e anotar página.
