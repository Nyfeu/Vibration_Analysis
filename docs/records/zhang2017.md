# Fichamento — Zhang et al. (2017) — WDCNN

| | |
|---|---|
| **Referência (ABNT)** | ZHANG, W.; PENG, G.; LI, C.; CHEN, Y.; ZHANG, Z. A new deep learning model for fault diagnosis with good anti-noise and domain adaptation ability on raw vibration signals. *Sensors*, v. 17, n. 2, art. 425, 2017. |
| **DOI / acesso** | [10.3390/s17020425](https://doi.org/10.3390/s17020425) |
| **Chave no `.bib`** | `zhang2017` |
| **Arquivo** | não versionado (PDFs ficam em `docs/articles/`, fora do Git) |
| **Fichado por** | Claude Code (assistente de IA), a pedido do grupo |
| **Revisado por** | André Maiolini (sessão de trabalho) |
| **Última atualização** | 2026-10-10 |
| **Por que ler** | Arquitetura WDCNN, base da nossa CNN 1D; avaliada no próprio CWRU. |

> **Origem deste fichamento.** Redigido com assistência de IA (Claude Code), a partir do
> conhecimento estabelecido sobre a obra, com o texto completo consultado no PubMed Central (PMC5336047) para o protocolo de avaliação.
> Por isso **não há citações diretas nem números de página**: tudo é paráfrase. Antes
> de citar algo específico no relatório, conferir no original (DOI abaixo) e registrar
> a página. Ver `docs/uso_de_ia.md`.

---

## Ideias principais

1. CNN 1D com primeira camada de kernel largo (banco de filtros aprendido) seguida de camadas pequenas, sobre o sinal bruto de vibração.
2. Avaliada no CWRU com alta acurácia, robustez a ruído e adaptação entre cargas.

## Pontos relevantes para o projeto

- → Projeto: copiamos a ideia do kernel largo inicial.
- **Verificado no texto completo (PMC5336047, 2026-10-10):** as amostras de treino são janelas de 2048 pontos cortadas com sobreposição dos sinais (seção 3.4), e as de teste, sem sobreposição, dos mesmos sinais (seções 4.1 e 4.3). Na adaptação de domínio, treina-se numa carga (1, 2 ou 3 HP) e testa-se nas outras (seção 4.4.1, Tabela 3).
- → Projeto: o teste entre cargas do artigo é o mesmo tipo de teste do nosso split por carga, que não separa montagens: no CWRU, cada defeito foi ensaiado numa única montagem, presente em todas as cargas. Nossa CNN no estilo WDCNN chega a 99,7% nesse teste e cai para ~50% com uma montagem nova (seção 5.6 do relatório).

## Onde é usado no relatório

- Seções 3.3.4 e 4.5.3.

## Cuidados ao citar

- O protocolo foi conferido: treino e teste vêm das mesmas gravações, e a generalização é avaliada entre cargas.

## Pendências

- [x] Split conferido no texto completo (2026-10-10) e usado na discussão crítica do relatório.
