# Fichamento — McFadden & Smith (1984) — Modelo de vibração de defeito pontual

| | |
|---|---|
| **Referência (ABNT)** | McFADDEN, P. D.; SMITH, J. D. Model for the vibration produced by a single point defect in a rolling element bearing. *Journal of Sound and Vibration*, v. 96, n. 1, p. 69–82, 1984. |
| **DOI / acesso** | [10.1016/0022-460X(84)90595-9](https://doi.org/10.1016/0022-460X(84)90595-9) |
| **Chave no `.bib`** | `mcfadden1984` |
| **Arquivo** | não versionado (PDFs ficam em `docs/articles/`, fora do Git) |
| **Fichado por** | Claude Code (assistente de IA), a pedido do grupo |
| **Revisado por** | André Maiolini (sessão de trabalho) |
| **Última atualização** | 2026-10-10 |
| **Por que ler** | Modelo clássico que explica a forma do sinal de um defeito pontual e as bandas laterais do envelope. Smith e Randall baseiam nele a tabela de componentes esperados (nossa Tabela 5). |

> **Origem deste fichamento.** Redigido com assistência de IA (Claude Code), a partir do
> conhecimento estabelecido sobre a obra, sem acesso ao texto completo nesta sessão.
> Por isso **não há citações diretas nem números de página**: tudo é paráfrase. Antes
> de citar algo específico no relatório, conferir no original (DOI abaixo) e registrar
> a página. Ver `docs/uso_de_ia.md`.

---

## Ideias principais

1. Modela o sinal como a resposta de uma ressonância a uma sequência periódica de impulsos.
2. A amplitude dos impulsos é modulada pela distribuição de carga no rolamento (zona de carga) e pela variação do caminho de transmissão até o sensor quando o defeito gira.
3. Disso resultam as bandas laterais previstas: espaçadas de f_r para pista interna e de FTF para elementos rolantes; pista externa estacionária sem modulação.

## Pontos relevantes para o projeto

- → Projeto: explica por que a pista externa a 6 h (na zona de carga) tem a assinatura mais limpa e por que a posição do defeito importa (nosso conjunto de generalização).

## Onde é usado no relatório

- Seção 3.1 (assinatura vibratória).

## Cuidados ao citar

- Modelo para defeito pontual único; não descreve defeitos distribuídos nem folga mecânica, que Smith e Randall encontram no CWRU.

## Pendências

- [ ] Conferir a formulação da modulação pela zona de carga.
