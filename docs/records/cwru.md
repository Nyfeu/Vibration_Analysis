# Fichamento — CWRU Bearing Data Center — documentação oficial do dataset

| | |
|---|---|
| **Referência (ABNT)** | CASE WESTERN RESERVE UNIVERSITY. *Bearing Data Center: Seeded Fault Test Data*. 2026. Disponível em: https://engineering.case.edu/bearingdatacenter. Acesso em: 6 out. 2026. |
| **DOI / acesso** | https://engineering.case.edu/bearingdatacenter |
| **Chave no `.bib`** | `cwru` |
| **Arquivo** | não versionado (PDFs ficam em `docs/articles/`, fora do Git) |
| **Fichado por** | Claude Code (assistente de IA), a pedido do grupo |
| **Revisado por** | André Maiolini (sessão de trabalho) |
| **Última atualização** | 2026-10-10 |
| **Por que ler** | Fonte primária do dataset. Todo número do capítulo 2 vem dela ou de Smith e Randall (2015). Conferida diretamente pelo grupo (ver `data/raw/README.md`). |

> **Origem deste fichamento.** Redigido com assistência de IA (Claude Code), a partir das
> páginas oficiais do CWRU **conferidas diretamente** em 2026-10-06 e registradas em
> `data/raw/README.md` (issue #3), onde está a evidência de cada inconsistência.

---

## Ideias principais

1. Bancada: motor de 2 HP, transdutor de torque/encoder e dinamômetro; rolamentos SKF 6205 (DE) e 6203 (FE).
2. Defeitos pontuais por eletroerosão com 0,007" a 0,040"; cargas de 0 a 3 HP (1797 a 1730 rpm nominais).
3. Aquisição a 12 kHz e, para parte dos defeitos no DE, a 48 kHz; arquivos .mat com canais DE, FE e BA.
4. Página 'Bearing Specifications': diâmetros da esfera (0,3126 in) e primitivo (1,537 in) do DE e multiplicadores de frequência de defeito.

## Pontos relevantes para o projeto

- Inconsistências verificadas pelo grupo: os normais (97–100) estão a 48 kHz, embora a página não declare; `99.mat` traz as variáveis de `98.mat`; 98 e 99 não têm rotação medida; a página se contradiz sobre a posição da zona de carga (3 h × 6 h).
- O multiplicador 'Rolling Element' (4,7135 × f_r) é 2 × BSF (convenção adotada: BSF de Smith e Randall).
- → Projeto: decimação 48 → 12 kHz, leitura da variável pelo número do arquivo e posição @6 vêm dessas verificações.

## Onde é usado no relatório

- Cap. 2 inteiro, Tabelas 1 e 2, Figura 1 (foto da bancada), Seção 4.4.2 (geometria).

## Cuidados ao citar

- Site muda de estrutura com o tempo; manter a data de acesso. Não copiar números deste fichamento sem conferir `data/raw/README.md`.

## Pendências

- [ ] Nenhuma: conferido em 2026-10-06 (issue #3).
