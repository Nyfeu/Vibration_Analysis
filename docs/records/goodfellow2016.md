# Fichamento — Goodfellow, Bengio & Courville (2016) — Deep Learning

| | |
|---|---|
| **Referência (ABNT)** | GOODFELLOW, I.; BENGIO, Y.; COURVILLE, A. *Deep Learning*. Cambridge: MIT Press, 2016. |
| **DOI / acesso** | sem DOI (livro); versão aberta em deeplearningbook.org |
| **Chave no `.bib`** | `goodfellow2016` |
| **Arquivo** | não versionado (PDFs ficam em `docs/articles/`, fora do Git) |
| **Fichado por** | Claude Code (assistente de IA), a pedido do grupo |
| **Revisado por** | André Maiolini (sessão de trabalho) |
| **Última atualização** | 2026-10-16 |
| **Por que ler** | Livro-texto geral de aprendizado profundo; base para a CNN 1D e o autoencoder. |

> **Origem deste fichamento.** Redigido com assistência de IA (Claude Code), a partir do
> conhecimento estabelecido sobre a obra, sem acesso ao texto completo nesta sessão.
> Por isso **não há citações diretas nem números de página**: tudo é paráfrase. Antes
> de citar algo específico no relatório, conferir no original e registrar a página.
> Ver `docs/uso_de_ia.md`.

---

## Ideias principais

1. Redes convolucionais: convolução, compartilhamento de pesos, *pooling* e por que funcionam bem em sinais com estrutura local (cap. 9).
2. Autoencoders: reconstrução da entrada por uma representação comprimida, e o papel do gargalo para impedir a cópia trivial (cap. 14).
3. Regularização e otimização de redes profundas.

## Pontos relevantes para o projeto

- → Projeto: fundamenta a CNN 1D sobre o sinal bruto e o autoencoder usado como detector.

## Onde é usado no relatório

- Seções 3.3 (áreas de referência), 3.3.3 (autoencoder) e 3.3.7 (CNN 1D).

## Pendências

- [ ] Conferir no original os capítulos citados no relatório.
