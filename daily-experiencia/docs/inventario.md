# Inventário dos fluxos atuais

Levantado em 23/10/2026 a partir de `logic\tableau\Daily - Experiencia BR - MKT.tfl`, `logic\tableau\Daily Experiencia BR - Dynamics e Resenhas.tfl` e `logic\tableau\Daily Experiencia BR.twb`.

Caminhos relativos a `G:\Drives compartilhados\REPÓSITORIOS - DOCUMENTAÇÕES\Dashboards - Tableau\Central de EXP e Serviços\Fontes de Dados`.
O ID é o `cloudFileId` gravado no fluxo: IDs de 33 caracteres são arquivos .xlsx; os de 44 caracteres são Google Sheets nativas.

## Ordem de execução

```
Dynamics e Resenhas ──(Dynamics Nivel)──► MKT
```

## Fontes – fluxo Dynamics e Resenhas

| Fonte | Tipo | Aba | Local | ID |
|---|---|---|---|---|
| Criados em | xlsx | Criados em - Tarefas Exper... | `EXP BR\DYNAMICS\Report Diario` | `1B-itioG8JopDYgYtoyLerxglPFbgkgY1` |
| Termino Real | xlsx | Termino Real - Tarefas Expe... | `EXP BR\DYNAMICS\Report Diario` | `1V7ZkFc7gyfclwOwYRTOfqqz3ySHqoLOO` |
| Salesforce CF | xlsx | Base | `EXP BR\Salesforce` (sem alteração desde 02/12/2025) | `1wuwG20En--_Q1ssIYS0LUiVdb5Y4-6ti` |
| Salesforce CF Criados | xlsx | Base | `EXP BR\Salesforce` | `1QKBeBp9uxOalkMOBRf-tuWj5E0a8Zlj-` |
| Salesforce CF Encerrados | xlsx | Base | `EXP BR\Salesforce` | `1vjEjIlxJ71A5lFljFtMgD9cH6Nmjv0yS` |
| Servicenow - Incidentes Experiencia Brasil | xlsx | incident (1) | `EXP BR\Service Now` | `1Xg1FieiV9engpS1T2KXjz4twpWclpUxA` |
| App Natura | xlsx | | `EXP BR\Resenhas` | `17fNDVkXVlhggmZybz8diaiklXKpjU4i1` |
| App_Avon | xlsx | | `EXP BR\Resenhas` | `1PXHgELzJ5yqNgcgHLNW9TeKEAnaAv2Ve` |
| Consultoria Natura | xlsx | | `EXP BR\Resenhas` | `1vlsRtExSmTZPwGx2gXMwhKa9sY0L1IYx` |
| Forca de Vendas | xlsx | | `EXP BR\Resenhas` | `1bMwOdxhHoizvbQ036QPso3Va-amt_ZVj` |
| Mapeamento: Assunto / Função do sistema x Jornada (Tribo) | gsheet | Base Dynamics_1309, Base_GruposServiceNow_2209 | `EXP BR\Auxiliar` | `1y4uGJ1ik89sDJ4qYKJgtgduGfHbn6jnbvukCzGYNjWE` |
| Expurgo | gsheet | Página1 | `EXP BR\DYNAMICS\Expurgo` | `15TkEO9bS5D6W1_DYJ2VeoDiYVVUQN729P6H5YgdlzJo` |
| Resenhas | gsheet | | não localizado em Fontes de Dados | `1RAFYqizyyX6H7FCzWZdog2vTS3Hbh3TOfkwt2pdHTUA` |

## Fontes – fluxo MKT

| Fonte | Tipo | Aba | Local | ID |
|---|---|---|---|---|
| MKT_Reativos (Analítico MKTZap Brasil) | xlsx | Sheet1 | `EXP BR\MKT` (oficial; `auto\mktzap\27 - Brasil` é o destino da automação) | `1n3X3Njk37qoH0Mprf8SH2fr2AVIBVJYE` |
| MKT Reativos - Historico ate Out25 | xlsx | Sheet1 | `EXP BR\MKT` | `1owprt-DlQNngTKerXeXwWLv0p2A6lKmI` |
| Tickets Brasil (MKTZap) | xlsx | Planilha1 | `EXP BR\MKT` | `13VyrKDCu1POwQFYwZJe9WnAYLejUYX15` |
| MKT Brasil Completo | xlsx | Sheet1 | `EXP BR\MKT` (cópia também em `auto\mktzap\27 - Brasil`) | `1Wb3UV8OKS983YvrTAIknEdTqzyTjDtQC` |
| Servicenow - Incidentes Experiencia Brasil | xlsx | incident (1) | `EXP BR\Service Now` | `1Xg1FieiV9engpS1T2KXjz4twpWclpUxA` |
| Salesforce CF Encerrados Analistas | xlsx | Base | `EXP BR\Salesforce` | `18qiuWdDhRZ2knH5ZmY_t0xgNiL64covs` |
| Base Expurgo | gsheet | MKT | `EXP BR\MKT` | `1Xxq8GLBU4qDf5yw1_w3F6LKDg-SPSBZUUa6Hgol0nA8` |
| Auxiliar Brasil | gsheet | Página1 | `EXP BR\MKT\Auxiliares` | `1bboKHWs4Nni5XLxSKQXIt7dFhRPG9SQVVWzADq9NeYA` |
| Base MKT | gsheet | MKT Brasil | `EXP BR\MKT\Auxiliares` | `1Huh-FLUWQ9yH21EhyvhX9GbT3F5D1N3jcHtGo2PKfe0` |
| Mapeamento: Assunto / Função do sistema x Jornada (Tribo) | gsheet | Base_MKT_1309 | `EXP BR\Auxiliar` | `1y4uGJ1ik89sDJ4qYKJgtgduGfHbn6jnbvukCzGYNjWE` |
| Monitoração Dynatrace | gsheet | Página1 | `EXP BR\Dynatrace` | `1TUhzUExoiv-3b835EJ3BehDPzBeNTrKER4vvMmnjdvA` |
| Registros Ate Julho | gsheet | Página1 | `EXP BR\Dynatrace` | `1nECQI_RirnwWPaNOw1NMGBMLl-H9mFvBRkw8P1Yv6TA` |
| AppSheets Consolidado - Registros Experiência CB | gsheet | Registro | `EXP BR\AppSheets` | `1KoUKxm5LF5x5pgUXouQFfftr4ftnQBA_PuB95N4LPJA` |
| Registros de Acionamentos | gsheet | Página1 | não localizado em Fontes de Dados | `1QId6xiTda8zlnVdBwKsczLqowpxifk2jiAWfxJ9OeO0` |
| Ticket Medio | gsheet | Página1 | `EXP BR\Ticket Medio` | `1A_VHAujNp0oYAnAnNA_xuWBjT6GsWKJ-jhIC6d4a06s` |
| Healthcheck 2025 | gsheet | Página1 | `EXP BR\Heatlhcheck` | `1j_CTBASV-2p_WWwZTnMY_MlizYPanlu4mMBm20zhD7g` |
| Dynamics Nivel | Tableau Cloud | | saída do fluxo Dynamics | |
| Resenhas EXP BR AppSheets | Tableau Cloud | | saída do fluxo Dynamics | |

## Saídas (24 extracts em `4. DATASOURCES` no Tableau Cloud)

**Fluxo Dynamics e Resenhas (6):** Dynamics Nivel · Dynamics - Base para Rechamada · Dynamics - Termino Real · EXPBR - Chamados Servicenow · Resenhas EXP BR AppSheets · Resenhas Brasil

**Fluxo MKT (18):** Experiencia Brasil Nivel · MKT Brasil Completo · MKT Brasil Completo Nivel · MKT Brasil Backlog · Histórico Backlog Diário · MKT BRASIL - WhatsApp · MKT BRASIL - Email · MKT - CBCOM · MKT Whats GV · MKT Whats GV Antecipada · MKT Whats GN · MKT Whats Franquia · MKT Email Experiencia CB · MKT Emails de Lojas · Requisição Eventual EXP BR · Exp Brasil Dynatrace · Ticket Medio Exp Br · HC Exp Brasil

**Usadas pelo workbook, mas fora destes fluxos (continuam como estão):** Backlog Dynamics · Backlog_Servicecloud_Dynamics · Dynamics - Criados em · Enquetes C-SAT · Página1 (Notificação de Incidentes)

## Regras fixas a preservar (detalhar na migração de cada saída)

| Fluxo | Etapa no Prep |
|---|---|
| MKT | Remover protocolos de 16/01/26 |
| MKT | 16 e 17/03 · Ajuste dias 16 e 17/03 · Remover dados de 16 e 17/03 |
| MKT | Data Corte Até 30/09/25 · Data Corte a Partir 01/10/25 · Data Corte Franquias |
| MKT | Histórico < 202610 · A partir de 202610 |
| Dynamics | Data Corte (Nov a Dez/2025) · Até 2025 · Dados a partir de 2026 |
| Dynamics | Ajuste dos dias 24, 25 e 31 (feriados de dez/2025 no cálculo de horas úteis) |

## Tamanho dos fluxos

| | MKT | Dynamics e Resenhas |
|---|---|---|
| Entradas | 21 | 16 |
| Campos calculados | 86 | 63 |
| Joins / Unions | 15 / 17 | 5 / 8 |
| Saídas | 18 | 6 |
