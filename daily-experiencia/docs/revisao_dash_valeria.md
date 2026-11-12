# Revisão dos dash no Tableau (Valéria) × versão Databricks

Documento de origem: **"Revisão dos Dash no Tableau"** (Google Docs, 13 abas), escrito pela Valéria no card
[CDES-2708](https://natura.atlassian.net/browse/CDES-2708). As anotações são de 06/04 e 03/06/2026. Ele foi a base da
reunião de 12/11/2026 sobre o Métricas da Excelência, e vai ser revisado no fórum semanal da Experiência.

Situação em 12/11/2026, comparada com o workbook **Daily Experiência BR - Databricks**, que ainda não está em
produção:
- **Feito:** já está na versão Databricks. Entra na produção quando ela substituir a versão atual.
- **Parcial:** atende uma parte do pedido.
- **Pendente:** ainda não foi feito.
- **Decidir:** depende de uma decisão da Experiência.

## Geral (aba "Indicadores 2026")

| Pedido | Situação | Onde / observação |
|---|---|---|
| Trocar abas que repetem o mesmo canal por um resultado geral com filtro | **Feito** | `unificar_paineis_tableau.py`: Dynamics CB e CF → Dynamics Consolidado (filtro Tipo Protocolo); 3 painéis de e-mail → "Email Lojas - Detalhes" (parâmetro Setor do e-mail); 5 de WhatsApp → "Whats - Detalhes" (parâmetro Painel). Das 25 abas listadas, ficam 17 |
| Organizar os temas em pastas: indicadores vivos (daily), produtividade, excelência, overview (backlog + Service Now) | **Decidir** | É o mesmo pedido da reunião de 12/11 (blocos eficiência, produtividade, qualidade, monitoramento e contratuais). O Tableau não tem pasta dentro de um workbook: ou são workbooks separados numa pasta do projeto, ou uma aba de navegação com botões. Depende da planilha de categorização |
| Atualizar com os indicadores de 2026 | **Pendente** | Conferir a aba Indicadores 2026 contra a Matriz de Indicadores (Brasil_2026) |
| Data da última atualização em todas as abas (rodapé) | **Pendente** | O exemplo do documento (atualização "às 21:19" vista às 18:36) é uma diferença de 3 horas: a data provavelmente aparece em UTC, não no horário de Brasília. Corrigir junto |

## MKT Whats e MKT Email

| Pedido | Situação | Onde / observação |
|---|---|---|
| Histórico dos últimos meses (3, ou 2 fechados + o parcial) nos gráficos principais | **Parcial** | `redesenho_tableau.py`: volumes passam a mostrar 6 meses. Os indicadores com meta mostram 2 barras: o mês atual e um mês de comparação |
| Cores de semáforo para a saúde do indicador | **Feito** | `redesenho_tableau.py`: verde-água dentro da meta, laranja até 10 pontos abaixo e vermelho abaixo disso; o laranja deixa de ser cor de série |
| Comparar com o mesmo mês do ano anterior (abril de 2025 × abril de 2026) | **Feito** | `mes_de_comparacao_tableau.py`: parâmetro "Mês de comparação" ao lado do filtro de mês |
| Mostrar a meta no gráfico (ex.: 95% em 5 min) | **Parcial** | Há linha pontilhada na meta. Falta o nome da meta no título ou rótulo |
| Um gráfico de ofensores dinâmico (N1/N2 por filtro) no lugar de 3 | **Pendente** | |
| Ofensores só de protocolos finalizados; explicar as categorias NULL | **Pendente** | Conferir a regra na gold do MKT antes de mexer no gráfico |
| Mesmo formato de ofensores e de retenção no WhatsApp e no e-mail | **Parcial** | `6cbd7ea`: a Retenção do e-mail entrou nos indicadores com meta. Falta igualar os ofensores |
| Padronizar os painéis de subcanal do WhatsApp | **Feito** | Um painel só, "Whats - Detalhes" |
| Subcanais de e-mail por filtro | **Feito** | "Email Lojas - Detalhes" |
| TMO em dias | **Pendente** | |
| TMO por canal (e-mail e MKT separados) e por finalização (Jira, N2) | **Pendente** | |
| Filtro por Mercado | **Pendente** | No Painel C-SAT (Apps Script) o filtro de Mercado já existe |
| Outra forma de filtrar por tribo | **Decidir** | Pedido sem detalhe |
| Volume de entrada e saída por dia, como no Dynamics | **Pendente** | |
| Avaliar o gráfico de volume de atendimentos × protocolos (e-mail) | **Decidir** | |

## CRM Atendimento (Dynamics Consolidado)

| Pedido | Situação | Onde / observação |
|---|---|---|
| Renomear para "CRM Atendimento" (Dynamics e Service Cloud) | **Pendente** | Simples. Lembrar que o Dynamics deixa de existir em fevereiro de 2027 |
| Histórico de 3 meses na retenção, como o de protocolos recebidos | **Parcial** | Volumes já em 6 meses. Conferir se a retenção entrou |
| Retenção em N2 repetida | **Decidir** | |
| Visão por tribo ou frente, como no book, no lugar do top ofensor por sistema | **Decidir** | |
| Retrabalho junto do volume de entrada × saída, como no book | **Pendente** | |
| Tirar o gráfico de rechamada até revisar a lógica | **Pendente** | A lógica mudou com o Service Cloud |

## Outras abas

| Aba | Pedido | Situação |
|---|---|---|
| Service Now | Acompanhar chamados em aberto por tribo: histórico de registro, aging (mais de 5, 10 e 20 dias), volume por fila e top ofensor pelo resumo | **Pendente**. É uma visão nova, de chamados em aberto, não de abertos no mês |
| Solicitações | Nome melhor para a visão consolidada | **Decidir** |
| Backlog | Data de corte | **Pendente**. Igual ao item geral |
| Retrabalho | Histórico de volume dos últimos meses | **Parcial**. Volumes em 6 meses no redesenho; conferir esta aba |
| Resenhas | "Não está trazendo as informações" | **Conferir** na versão Databricks |
| C-Sat | Filtro por Mercado | **Feito** no Painel C-SAT (Apps Script) |
| C-Sat | Agrupar o filtro de Canal (ativo, reativo etc.) | **Pendente**. Falta a regra de agrupamento |
| Dynamics - CB, Service Cloud | (abas vazias no documento) | |
