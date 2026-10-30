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
| Expurgo (SLA por tarefa) | gsheet | Expurgo SLA | `EXP BR\DYNAMICS\Expurgo` | `15TkEO9bS5D6W1_DYJ2VeoDiYVVUQN729P6H5YgdlzJo` |
| Resenhas | gsheet | | não localizado em Fontes de Dados | `1RAFYqizyyX6H7FCzWZdog2vTS3Hbh3TOfkwt2pdHTUA` |

## Fontes – fluxo MKT

| Fonte | Tipo | Aba | Local | ID |
|---|---|---|---|---|
| MKT_Reativos (Analítico MKTZap Brasil) | xlsx | Sheet1 | `EXP BR\MKT` (oficial; desde 30/10/2026 é também o destino da automação, antes `auto\mktzap\27 - Brasil`) | `1n3X3Njk37qoH0Mprf8SH2fr2AVIBVJYE` |
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

## Daily Hispana (levantado em 30/10/2026, migração em andamento)

Fluxo `logic\tableau\Daily Experiencia OIS.tfl`, especificação em `docs/fluxos/hispana.md`. Painel `logic\tableau\Experiência Hispana - Daily.twbx` (98 planilhas, 14 painéis). Na produção, os extracts foram atualizados por volta das 9h20 em 30/10.

### Fontes

Caminhos relativos a `Fontes de Dados`.

| Fonte | Tipo | Aba | Local | ID | Etapas |
|---|---|---|---|---|---|
| MKT Analitico Hispana | xlsx | Planilha1 | `EXP OIS\MKT` | `19hVZLPMuvfwfJzI9SMpGvy5gvGpyoOml` | [3] [11] |
| MKT Hispana Completo | xlsx | Sheet1 | `EXP OIS\MKT` | `1uc2dNuJTPvBkeOcJkqFw0C6UNylwiAzJ` | [1] |
| Tickets Hispana | xlsx | Planilha1 | `EXP OIS\MKT` | `1o54zZFpWqP1jVsn0EjvXv7bMZ9W64T6j` | [9] |
| BASE MTK | xlsx | Base | `EXP OIS\MKT` | `1oH0JZAsPaIxeWTD3IQPZcZ9btOMGJ2SY` | [8] [14] |
| BASE MTK Historico | xlsx (108 MB) | Base | `EXP OIS\MKT` | `1PYQSCpV-9LWXj8ceYRcorWFZvF9AwhG6` | [7] [12] |
| BASE SN OIS | xlsx | Page 1 | `EXP OIS\SERVICE NOW` | `1Iuo1gldMiYWMunv8-MwZ3lEyoM3rYuJU` | [19] |
| Resenhas Latam | xlsx | in | `EXP OIS\Resenhas` | `1cgHX2ukjgLEJu69i1jNPEhk-qI20j52Q` | [17] |
| Mi Negocio | xlsx | reviews_reviews_net.natura.mine | `EXP OIS\Resenhas` | `1SxY9VozokY6gDbHNmF8V4mZDDukjrpWF` | [18] |
| App Natura | xlsx | reviews_reviews_net.natura.semp | `EXP BR\Resenhas` (já no pipeline) | `17fNDVkXVlhggmZybz8diaiklXKpjU4i1` | [6] |
| App_Avon | xlsx | reviews_reviews_com.naturaeco.a | `EXP BR\Resenhas` (já no pipeline) | `1PXHgELzJ5yqNgcgHLNW9TeKEAnaAv2Ve` | [13] |
| Auxiliar Hispana | gsheet | Funcao do Sistema | | `1zjTNpqmyoAWu-WLqV2nLzYNJp0Las6u_mMQf3zgLf3c` | [2] |
| Consolidado - Registro de Grupos | gsheet | Página1 | `EXP OIS\MKT` | `1LVISJ8GsoVgBizLomMHWkKmFIur8MfFmoFZFuY3YX7U` | [4] |
| Resenhas OIs | gsheet | BaseDados | | `1FEqQXMCU10tqtJyAd5gULEQD24ZZV1BKOwZyJID7SAE` | [5] |
| Ticket Medio Hispana | gsheet | Ticket Medio | `EXP OIS\Ticket Medio` | `1l9B0QkiZiOXAn545u1Js3gligsA8iOW2HbfSwUpwZZE` | [10] |
| Ticket Medio por Pais | gsheet | Ticket Medio | `EXP OIS\Ticket Medio` | `1CGjLnV4zgf3toikmBZwt6iXxND9HzQUVy6PxJpHJpAU` | [15] |
| Base Exento | gsheet | Página1 | `EXP OIS\MKT` | `1XjUlJog7movWv6pm3YKhkkI_zcqVeY8bTex9xbFCwpA` | [16] |

App Natura e App_Avon são os mesmos arquivos do fluxo Brasil, mas nas etapas [6] e [13] há filtro de idioma (`[Reviewer Language]="es"` em [6]).

### Saídas (extracts em `4. DATASOURCES`, linhas em 30/10/2026)

| Saída | Etapa | Linhas | Colunas | Planilhas do painel |
|---|---|---|---|---|
| Base MKT OIS | [106] | 254.072 | 67 | 43 |
| Resenhas OIS | [54] | 443.362 | 25 | 11 |
| Experiencia Hispana Produtividade | [114] | 245.702 | 15 | Não usada |
| MKT Hispana Completo | [82] | 42.441 | 31 | 2 |
| Experiencia Hispana - Chamados Servicenow | [60] | 31.222 | 37 | 18 |
| Base MKT HC OIS | [105] | 5.513 | 67 | 4 |
| AppSheets Resenhas OIs | [43] | 2.611 | 20 | 8 |
| Base MKT Lojas OIS | [103] | 935 | 67 | 15 |
| Ticket Medio Hispana | [38] | 147 | 3 | 1 |

O painel também lê direto a Google Sheet `Healthcheck Paises Consolidado` (`EXP OIS\Healthcheck`), que fica como está. Os extracts usados como gabarito estão em `validacao\extracts_hispana\`.

### Tamanho

114 etapas: 19 entradas, 68 limpezas, 13 uniões, 5 joins, 9 saídas.

## Tamanho dos fluxos

| | MKT | Dynamics e Resenhas |
|---|---|---|
| Entradas | 21 | 16 |
| Campos calculados | 86 | 63 |
| Joins / Unions | 15 / 17 | 5 / 8 |
| Saídas | 18 | 6 |
