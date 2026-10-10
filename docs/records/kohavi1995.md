# Fichamento — Kohavi (1995) — Validação cruzada e bootstrap

| | |
|---|---|
| **Referência (ABNT)** | KOHAVI, R. A study of cross-validation and bootstrap for accuracy estimation and model selection. In: INTERNATIONAL JOINT CONFERENCE ON ARTIFICIAL INTELLIGENCE, 14., 1995, Montreal. *Proceedings*. 1995. p. 1137–1143. |
| **DOI / acesso** | (anais; sem DOI) |
| **Chave no `.bib`** | `kohavi1995` |
| **Arquivo** | não versionado (PDFs ficam em `docs/articles/`, fora do Git) |
| **Fichado por** | Claude Code (assistente de IA), a pedido do grupo |
| **Revisado por** | André Maiolini (sessão de trabalho) |
| **Última atualização** | 2026-10-10 |
| **Por que ler** | Estudo de referência sobre estimar acurácia e selecionar modelos por validação cruzada. |

> **Origem deste fichamento.** Redigido com assistência de IA (Claude Code), a partir do
> conhecimento estabelecido sobre a obra, sem acesso ao texto completo nesta sessão.
> Por isso **não há citações diretas nem números de página**: tudo é paráfrase. Antes
> de citar algo específico no relatório, conferir no original (DOI abaixo) e registrar
> a página. Ver `docs/uso_de_ia.md`.

---

## Ideias principais

1. Compara empiricamente validação cruzada, leave-one-out e bootstrap.
2. Recomenda validação cruzada estratificada com 10 partições como bom compromisso entre viés e variância.

## Pontos relevantes para o projeto

- → Projeto: usamos validação cruzada para seleção, mas **não** a estratificada embaralhada: nossos dados têm grupos (janelas da mesma gravação), o que viola a independência suposta no estudo. Ver Roberts et al. (2017).

## Onde é usado no relatório

- Seção 3.3.4 (seleção de modelos).

## Cuidados ao citar

- A recomendação de k-fold estratificado vale para amostras independentes; não se aplica a janelas sobrepostas.

## Pendências

- [ ] Nenhuma.
