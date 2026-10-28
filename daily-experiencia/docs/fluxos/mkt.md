# Especificação do fluxo `Daily - Experiencia BR - MKT.tfl`

Gerado por `ferramentas/especificar_fluxo_prep.py`. Etapas em ordem de execução; `←` indica de onde vêm os dados.

## [1] MKT Historico — LoadSql

Arquivo: `MKT Reativos - Historico ate Out25.xlsx` · aba `[Sheet1$]`

Campos: `Protocolo`:string, `Empresa`:string, `Nome`:string, `CPF/CNPJ`:string, `Número do Contrato`:string, `Valor do Contrato`:string, `CODIGO`:string, `GV`:string, `FUNÇÃO`:string, `PEDIDO FINALIZADO`:string, `CONTATO DE SOLUÇÃO`:string, `CHAMADO`:string, `Fornecedor`:string, `Qtd Atendimentos`:integer, `testeLis`:string, `Função do Sistema`:string, `Ciclo - Health Check`:string, `Recebidos - Health Check`:string, `CATEGORIA 1 (WR TRANSP)`:string, `CATEGORIA 2 (WR TRANSP)`:string, `SOLUÇÃO APLICADA`:string, `Origem Health Check?`:string, `Está em Fechamento?`:string, `Código do Impactado`:string, `Ciclo Vigente`:string, `SETOR`:string, `MERCADO`:string, `E-mail`:string, `Data Contato`:datetime, `Responsável`:string, `Tempo até ser atendido`:string, `Tempo do atendimento`:string, `Primeiro Tempo de Espera`:string, `Tempo Médio de Espera`:string, `Tempo de Operação`:string, `Fone Cliente`:string, `Canal de Entrada`:string, `Setor Entrada`:string, `Setor Fim`:string, `Qtde Mensagens`:integer, `Status de Classificação`:string, `Status de finalização`:string, `Encerrado em`:datetime, `Observações`:string, `Campos adicionais Web Chat`:string, `Source_id CTWA`:string, `Resposta pedido duplicado`:string, `Dados bancarios`:string, `Ticket`:string

→ [24] Limpar 20

## [2] Tickets Brasil — LoadSql

Arquivo: `Tickets Brasil.xlsx` · aba `[Planilha1$]`

Campos: `ID do Ticket`:string, `Protocolo do Atendimento`:string, `Setor do Atendimento`:string, `Data de Criação do Atendimento`:datetime, `Estado`:string, `Status de Classificação`:string, `Status de Finalização`:string, `Data de Finalização`:datetime, `Usuário Responsável`:string, `Data de Criação do Ticket`:datetime, `Protocolo do Atendimento Convertido`:string, `Data de Conversão do Atendimento`:datetime, `PEDIDO FINALIZADO`:string, `CHAMADO`:string, `Qtd Atendimentos`:integer, `Função do Sistema`:string, `Está em Fechamento?`:string, `Código do Impactado`:string, `Ciclo Vigente`:integer, `Observações`:string

→ [32] União de colunas 25

## [3] Tribos MKT — LoadSql

Arquivo: `Mapeamento: Assunto / Função do sistema x Jornada (Tribo)` · aba `[Base_MKT_1309$]`

Campos: `Função do Sistema`:string, `Plataforma`:string, `Tribo`:string, `Macro`:string

→ [25] Aggregate 1; [81] Join 2

## [4] MKT Reativos — LoadSql

Arquivo: `MKT_Reativos.xlsx` · aba `[Sheet1$]`

Campos: `Protocolo`:string, `Empresa`:string, `Nome`:string, `CPF/CNPJ`:string, `Número do Contrato`:string, `Valor do Contrato`:string, `CODIGO`:string, `GV`:string, `FUNÇÃO`:string, `PEDIDO FINALIZADO`:string, `CONTATO DE SOLUÇÃO`:string, `CHAMADO`:string, `Fornecedor`:string, `Qtd Atendimentos`:integer, `testeLis`:string, `Função do Sistema`:string, `Ciclo - Health Check`:string, `Recebidos - Health Check`:string, `CATEGORIA 1 (WR TRANSP)`:string, `CATEGORIA 2 (WR TRANSP)`:string, `SOLUÇÃO APLICADA`:string, `Origem Health Check?`:string, `Está em Fechamento?`:string, `Código do Impactado`:string, `Ciclo Vigente`:string, `SETOR`:string, `MERCADO`:string, `Resposta pedido duplicado`:string, `Dados bancarios`:string, `E-mail`:string, `Data Contato`:datetime, `Responsável`:string, `Tempo até ser atendido`:string, `Tempo do atendimento`:string, `Primeiro Tempo de Espera`:string, `Tempo Médio de Espera`:string, `Tempo de Operação`:string, `Fone Cliente`:string, `Canal de Entrada`:string, `Setor Entrada`:string, `Setor Fim`:string, `Qtde Mensagens`:integer, `Status de Classificação`:string, `Status de finalização`:string, `Encerrado em`:datetime, `Observações`:string, `Campos adicionais Web Chat`:string, `Quantidade de Tickets`:integer

→ [158] União de colunas 17

## [5] Healthcheck — LoadSql

Arquivo: `Healthcheck 2025` · aba `[Página1$]`

Campos: `Data`:date, `Ciclo`:string, `Qtde Agendamento`:integer, `Qtde Recebidos`:integer, `Qtde Protocolos`:integer

→ [26] Limpar 12

## [6] Tribo — LoadSql

Arquivo: `Mapeamento: Assunto / Função do sistema x Jornada (Tribo)` · aba `[Base_MKT_1309$]`

Campos: `Função do Sistema`:string, `Plataforma`:string, `Tribo`:string, `Macro`:string

→ [27] Tribo

## [7] ServiceNow — LoadSql

Arquivo: `Servicenow - Incidentes Experiencia Brasil.xlsx` · aba `['incident (1)$']`

Campos: `number`:string, `opened_by`:string, `opened_at`:datetime, `short_description`:string, `caller_id`:string, `priority`:string, `state`:string, `category`:string, `assignment_group`:string, `assigned_to`:string, `sys_updated_on`:datetime, `sys_updated_by`:string, `contact_type`:string, `close_code`:string, `description`:string, `subcategory`:string, `work_end`:string, `work_start`:string, `reopened_time`:datetime, `closed_at`:datetime, `resolved_at`:datetime, `resolved_by`:string, `u_sla.business_percentage`:string, `hold_reason`:string, `business_service`:string, `u_jira`:string, `u_external_ticket`:string, `problem_id`:string, `due_date`:datetime, `close_notes`:string, `F31`:real, `F32`:real, `F33`:string, `F34`:string

→ [28] Remoção de colunas

## [8] Dynamics Nivel (4. DATASOURCES) — LoadSqlProxy

Arquivo: `https://prod-useast-a.online.tableau.com` · aba `[sqlproxy]`

Campos: `Data`:datetime, `Função do Sistema`:string, `Nivel`:string, `Qtd Atendimentos`:integer, `Responsavel Dynamics`:string, `Status de Classificação`:string, `Status de finalização`:string, `Ticket`:string, `Tipo`:string

→ [29] Dynamcis

## [9] MKT Reativos — LoadSql

Arquivo: `MKT_Reativos.xlsx` · aba `[Sheet1$]`

Campos: `Protocolo`:string, `Empresa`:string, `Nome`:string, `CPF/CNPJ`:string, `Número do Contrato`:string, `Valor do Contrato`:string, `CODIGO`:string, `GV`:string, `FUNÇÃO`:string, `PEDIDO FINALIZADO`:string, `CONTATO DE SOLUÇÃO`:string, `CHAMADO`:string, `Fornecedor`:string, `Qtd Atendimentos`:integer, `testeLis`:string, `Função do Sistema`:string, `Ciclo - Health Check`:string, `Recebidos - Health Check`:string, `CATEGORIA 1 (WR TRANSP)`:string, `CATEGORIA 2 (WR TRANSP)`:string, `SOLUÇÃO APLICADA`:string, `Origem Health Check?`:string, `Está em Fechamento?`:string, `Código do Impactado`:string, `Ciclo Vigente`:string, `SETOR`:string, `MERCADO`:string, `Resposta pedido duplicado`:string, `Dados bancarios`:string, `E-mail`:string, `Data Contato`:datetime, `Responsável`:string, `Tempo até ser atendido`:string, `Tempo do atendimento`:string, `Primeiro Tempo de Espera`:string, `Tempo Médio de Espera`:string, `Tempo de Operação`:string, `Fone Cliente`:string, `Canal de Entrada`:string, `Setor Entrada`:string, `Setor Fim`:string, `Qtde Mensagens`:integer, `Status de Classificação`:string, `Status de finalização`:string, `Encerrado em`:datetime, `Observações`:string, `Campos adicionais Web Chat`:string, `Quantidade de Tickets`:integer

→ [30] Limpar 27

## [10] Analitico Chamado — LoadSql

Arquivo: `MKT_Reativos.xlsx` · aba `[Sheet1$]`

Campos: `Protocolo`:string, `Empresa`:string, `Nome`:string, `CPF/CNPJ`:string, `Número do Contrato`:string, `Valor do Contrato`:string, `CODIGO`:string, `GV`:string, `FUNÇÃO`:string, `PEDIDO FINALIZADO`:string, `CONTATO DE SOLUÇÃO`:string, `CHAMADO`:string, `Fornecedor`:string, `Qtd Atendimentos`:integer, `testeLis`:string, `Função do Sistema`:string, `Ciclo - Health Check`:string, `Recebidos - Health Check`:string, `CATEGORIA 1 (WR TRANSP)`:string, `CATEGORIA 2 (WR TRANSP)`:string, `SOLUÇÃO APLICADA`:string, `Origem Health Check?`:string, `Está em Fechamento?`:string, `Código do Impactado`:string, `Ciclo Vigente`:string, `SETOR`:string, `MERCADO`:string, `Resposta pedido duplicado`:string, `Dados bancarios`:string, `E-mail`:string, `Data Contato`:datetime, `Responsável`:string, `Tempo até ser atendido`:string, `Tempo do atendimento`:string, `Primeiro Tempo de Espera`:string, `Tempo Médio de Espera`:string, `Tempo de Operação`:string, `Fone Cliente`:string, `Canal de Entrada`:string, `Setor Entrada`:string, `Setor Fim`:string, `Qtde Mensagens`:integer, `Status de Classificação`:string, `Status de finalização`:string, `Encerrado em`:datetime, `Observações`:string, `Campos adicionais Web Chat`:string, `Quantidade de Tickets`:integer

→ [31] Remoção de colunas

## [11] Aux Ticktes — LoadSql

Arquivo: `Auxiliar Brasil` · aba `[Página1$]`

Campos: `Função do Sistema - Tickets`:string, `Função do Sistema - Analitico`:string

→ [32] União de colunas 25

## [12] Ticket Medio — LoadSql

Arquivo: `Ticket Medio` · aba `[Página1$]`

Campos: `Mês`:date, `Ticket Médio`:real

Ações na leitura:

- Mudar tipo: `Mês` → date

→ [33] Mes

## [13] Resenhas EXP BR AppSheets (4. DATASOURCES) 2 — LoadSqlProxy

Arquivo: `https://prod-useast-a.online.tableau.com` · aba `[sqlproxy]`

Campos: `Aplicativo`:string, `App Nome`:string, `Categoria da Resposta 2`:string, `Categoria da Resposta`:string, `Classificação da Resposta`:string, `Classificação de Estrelas`:string, `Classificação do Ofensor`:string, `Comentário Postado`:string, `Data Avaliação`:datetime, `Data da Resposta EXP`:datetime, `Data da Resposta`:datetime, `IDIOMA`:string, `ID`:string, `Início da Contagem SLA (Brasil)`:datetime, `Loja`:string, `Nome Aplicativo`:string, `Nome do Respondente`:string, `OBSERVACAO`:string, `Prazo SLA (Brasil)`:datetime, `Resp. pela resposta`:string, `Resposta Fornecida`:string, `Star Rating`:integer, `Status SLA`:string, `_Dia da Semana da Resposta`:integer, `_Hora da Resposta`:integer

→ [34] Adequar colunas

## [14] MKT Brasil 5 — LoadSql

Arquivo: `Base MKT` · aba `['MKT Brasil$']`

Campos: `Protocolo`:string, `Ticket`:string, `Empresa`:string, `Nome`:string, `CPF/CNPJ`:string, `Número do Contrato`:string, `Valor do Contrato`:string, `CODIGO`:string, `GV`:string, `FUNÇÃO`:string, `PEDIDO FINALIZADO`:string, `CONTATO DE SOLUÇÃO`:string, `CHAMADO`:string, `Fornecedor`:string, `Qtd Atendimentos`:integer, `testeLis`:string, `Função do Sistema`:string, `Ciclo - Health Check`:string, `Recebidos - Health Check`:string, `CATEGORIA 1 (WR TRANSP)`:string, `CATEGORIA 2 (WR TRANSP)`:string, `SOLUÇÃO APLICADA`:string, `Origem Health Check?`:string, `Está em Fechamento?`:string, `Código do Impactado`:string, `Ciclo Vigente`:integer, `SETOR`:string, `MERCADO`:string, `Resposta pedido duplicado`:string, `Dados bancarios`:string, `E-mail`:string, `Data Contato`:datetime, `Responsável`:string, `Tempo até ser atendido`:string, `Tempo do atendimento`:datetime, `Primeiro Tempo de Espera`:string, `Tempo Médio de Espera`:string, `Tempo de Operação`:string, `Fone Cliente`:string, `Canal de Entrada`:string, `Setor Entrada`:string, `Setor Fim`:string, `Qtde Mensagens`:string, `Status de Classificação`:string, `Status de finalização`:string, `Encerrado em`:datetime, `Observações`:string, `Campos adicionais Web Chat`:string, `Quantidade de Tickets`:string

→ [35] 16 e 17/03

## [15] Dynatrace — LoadSql

Arquivo: `Monitoração Dynatrace` · aba `[Página1$]`

Campos: `Função do sistema`:string, `ID`:string, `Data`:datetime, `Analista`:string, `Você selecionou "CAPTAÇÃO - OUTROS". Qual é essa função?`:string, `Plataforma de Acesso`:string, `Sistema Operacional`:string, `Versão`:string, `IP`:string, `Código CB`:integer, `Conseguiu Contato?`:string, `Pedido finalizado?`:string, `Hora do erro`:datetime, `Hora INÍCIO do Atendimento`:datetime, `Hora FIM do Atendimento`:datetime, `Solução Aplicada`:string, `Erro perceptível ao usuário?`:string, `Qual erro identificado?`:string, `Observações`:string

→ [36] Limpar 6

## [16] Registro Acionamento — LoadSql

Arquivo: `Registros de Acionamentos` · aba `[Página1$]`

Campos: `ID`:string, `Data do contato`:date, `Analista`:string, `Canal de Entrada`:string, `Protocolo`:string, `Código do Impactado`:string, `Qtde de Atendimentos`:integer, `Pedido finalizado`:string, `Função do Sistema`:string, `Status de Organização`:string, `Status de Finalização`:string, `Chamado`:string

→ [162] União de colunas 19

## [17] ServiceCloud Analistas — LoadSql

Arquivo: `Salesforce CF Encerrados Analistas.xlsx` · aba `[Base$]`

Campos: `Data/Hora de abertura`:datetime, `Número do caso`:string, `Nome de Histórico do caso`:string, `Id Caso Completo`:string, `Primeira categoria`:string, `Segunda categoria`:string, `Motivo`:string, `Etapa`:string, `Solução`:string, `Data/Hora de fechamento`:datetime, `Classificação do problema sistêmico`:string, `Aplicativo com problemas`:string, `Data alvo SLA`:datetime, `Proprietário`:string, `Status do caso`:string, `Chamado`:string, `Caso pai: Número do caso`:string, `Origem do caso`:string, `Marca`:string, `Central`:string, `Ticket externo`:string, `Nome da conta: Nome da conta`:string, `CPF`:string, `Nome do usuário que realizou alteração`:string, `Data da última modificação`:date, `Modificado pela última vez por: Nome completo`:string, `Status`:string

→ [37] ID e Analista

## [18] MKT Reativos — LoadSql

Arquivo: `MKT_Reativos.xlsx` · aba `[Sheet1$]`

Campos: `Protocolo`:string, `Empresa`:string, `Nome`:string, `CPF/CNPJ`:string, `Número do Contrato`:string, `Valor do Contrato`:string, `CODIGO`:string, `GV`:string, `FUNÇÃO`:string, `PEDIDO FINALIZADO`:string, `CONTATO DE SOLUÇÃO`:string, `CHAMADO`:string, `Fornecedor`:string, `Qtd Atendimentos`:integer, `testeLis`:string, `Função do Sistema`:string, `Ciclo - Health Check`:string, `Recebidos - Health Check`:string, `CATEGORIA 1 (WR TRANSP)`:string, `CATEGORIA 2 (WR TRANSP)`:string, `SOLUÇÃO APLICADA`:string, `Origem Health Check?`:string, `Está em Fechamento?`:string, `Código do Impactado`:string, `Ciclo Vigente`:string, `SETOR`:string, `MERCADO`:string, `Resposta pedido duplicado`:string, `Dados bancarios`:string, `E-mail`:string, `Data Contato`:datetime, `Responsável`:string, `Tempo até ser atendido`:string, `Tempo do atendimento`:string, `Primeiro Tempo de Espera`:string, `Tempo Médio de Espera`:string, `Tempo de Operação`:string, `Fone Cliente`:string, `Canal de Entrada`:string, `Setor Entrada`:string, `Setor Fim`:string, `Qtde Mensagens`:integer, `Status de Classificação`:string, `Status de finalização`:string, `Encerrado em`:datetime, `Observações`:string, `Campos adicionais Web Chat`:string, `Quantidade de Tickets`:integer

Ações na leitura:

- Mudar tipo: `Tempo de Operação` → string
- Mudar tipo: `Data Contato` → datetime
- Mudar tipo: `Encerrado em` → datetime

→ [38] Remover dados de 16 e 17/03

## [19] MKT Brasil — LoadSql

Arquivo: `MKT Brasil Completo.xlsx` · aba `[Sheet1$]`

Campos: `Protocol`:string, `Nome`:string, `'Atendimentos'(first_message_at)`:datetime, `Data criação`:datetime, `Início Atendimento`:datetime, `Atendido`:datetime, `Data conclusão`:datetime, `Última mensagem`:datetime, `Tipo Canal`:string, `Canal`:string, `Setor`:string, `Operador`:string, `Telefone`:string, `Situação`:string, `Status`:string, `Tempo médio até ser atendidos`:string, `Tempo médio primeira espera`:string, `Tempo médio atendimento`:string, `Tempo médio espera`:string, `Tempo médio operacional`:string, `Qtde Mensagens`:integer

Ações na leitura:

- Mudar tipo: `Data criação` → datetime
- Mudar tipo: `Data conclusão` → datetime
- Mudar tipo: `Início Atendimento` → datetime
- Mudar tipo: `Atendido` → datetime
- Mudar tipo: `Última mensagem` → datetime
- Mudar tipo: `'Atendimentos'(first_message_at)` → datetime

→ [39] Expurgo Solicitado

## [20] Expurgo — LoadSql

Arquivo: `Base Expurgo` · aba `[MKT$]`

Campos: `Chamado/Protocolo`:string, `Autorizado Gestao Natura`:string, `Referencia`:string, `Data`:datetime, `Justificativa`:string

→ [40] Limpar 4

## [21] Dynatrace ate Julho — LoadSql

Arquivo: `Registros Ate Julho` · aba `[Página1$]`

Campos: `Data`:date, `Mes`:string, `Analista`:string, `Monitoração`:string, `Sistema`:string, `Função do sistema`:string, `Plataforma de Acesso`:string, `Sist Operacional`:string, `IP`:string, `Código CB`:integer, `Conseguiu contato ?  ☎️`:string, `Pedido finalizado ?`:string, `Hora do Alarme`:string, `Data e Hora Início do Atendimento`:string, `Hora Fim do Atendimento`:string, `Solução Aplicada`:string, `Erro Perceptível ao Usuário?`:string, `Observações`:string

→ [41] Limpar 7

## [22] RE - AppSheet — LoadSql

Arquivo: `AppSheets Consolidado - Registros Experiência CB` · aba `[Registro$]`

Campos: `ID`:string, `Data`:datetime, `Analista`:string, `Canal de entrada`:string, `Data do retorno`:date, `Protocolo`:string, `Ocorrência`:string, `Origem`:string, `Horário`:string, `Nome GN/ GV/ Supervisor`:string, `Nome da CB`:string, `Nome CND`:string, `Nome do impactado`:string, `Código do impactado`:string, `Qtde de Atendimentos`:string, `CB é Diamante+?`:string, `Data do SLA`:string, `Papel do impactado`:string, `Código`:string, `GV`:string, `Mercado`:string, `Setor`:string, `Está em fechamento?`:string, `Ciclo`:string, `Espaço envolvido`:string, `Pedido`:string, `Data do Pedido`:datetime, `CPF ou E-mail (CF)`:string, `Descrição do Erro`:string, `Impersonando`:string, `Detalhe`:string, `Sistema Impactado`:string, `Assunto / Função do sistema`:string, `Ação Espaço Digital - ATENÇÃO é possivel selecionar mais de uma ação`:string, `Status solução (Dynamics)`:string, `Motivo do Retrabalho`:string, `Status de Finalização`:string, `Responsável pela Tratativa (negocio)`:string, `N° do Chamado N2`:string, `Grupo do Chamado`:string, `Status do Chamado`:string, `Associado a Jira? Qual Jira?`:string, `Status do Jira`:string, `Follow up - realizado após 04 dias?`:string, `Data 1° follow`:date, `Realizado ativo p/ validação da solução final?`:string, `n° protocolo (caso tenha sido em ligação, coloque "ativo realizado")`:string, `Data de Finalização`:string, `Analista que Finalizou`:string, `Observação`:string

→ [42] Nível

## [23] Registro de Acionamentos — LoadSql

Arquivo: `Registros de Acionamentos` · aba `[Página1$]`

Campos: `ID`:string, `Data do contato`:date, `Analista`:string, `Canal de Entrada`:string, `Protocolo`:string, `Código do Impactado`:string, `Qtde de Atendimentos`:integer, `Pedido finalizado`:string, `Função do Sistema`:string, `Status de Organização`:string, `Status de Finalização`:string, `Chamado`:string

→ [43] AppSheets

## [24] Limpar 20 — Container

← [1] MKT Historico

→ [48] União de linhas 17

## [25] Aggregate 1 — SuperAggregate

← [3] Tribos MKT

**Agregar** agrupando por `Função do Sistema`, `Macro`, `Plataforma`, `Tribo`: 

→ [82] União de colunas 5

## [26] Limpar 12 — Container

← [5] Healthcheck

→ [44] HC Exp Brasil

## [27] Tribo — Container

← [6] Tribo

→ [59] União de colunas 23

## [28] Remoção de colunas — Container

← [7] ServiceNow

1. Remover colunas: `opened_by`
2. Remover colunas: `opened_at`
3. Remover colunas: `short_description`
4. Remover colunas: `caller_id`
5. Remover colunas: `priority`
6. Remover colunas: `category`
7. Remover colunas: `assignment_group`
8. Remover colunas: `assigned_to`
9. Remover colunas: `sys_updated_on`
10. Remover colunas: `sys_updated_by`
11. Remover colunas: `contact_type`
12. Remover colunas: `close_code`
13. Remover colunas: `description`
14. Remover colunas: `subcategory`
15. Remover colunas: `work_end`
16. Remover colunas: `work_start`
17. Remover colunas: `reopened_time`
18. Remover colunas: `closed_at`
19. Remover colunas: `resolved_at`
20. Remover colunas: `resolved_by`
21. Remover colunas: `u_sla.business_percentage`
22. Remover colunas: `business_service`
23. Remover colunas: `problem_id`
24. Remover colunas: `due_date`
25. Remover colunas: `close_notes`

→ [99] União de colunas 27

## [29] Dynamcis — Container

← [8] Dynamics Nivel (4. DATASOURCES)

→ [153] União de linhas 11

## [30] Limpar 27 — Container

← [9] MKT Reativos

1. Manter só: `Protocolo`, `Função do Sistema`, `Status de Classificação`
2. Renomear `Status de Classificação` → `Status de Classificação3`

→ [170] União de colunas 27

## [31] Remoção de colunas — Container

← [10] Analitico Chamado

1. Renomear `Protocolo` → `Protocolo Analitico`
2. Manter só: `Protocolo Analitico`, `CHAMADO`, `Função do Sistema`, `Observações`
3. Renomear `Função do Sistema` → `Função do Sistema Analitico`

→ [92] União de colunas 27

## [32] União de colunas 25 — SuperJoin

← [2] Tickets Brasil (Right); [11] Aux Ticktes (Left)

**Join right**: esquerda = [11] Aux Ticktes, direita = [2] Tickets Brasil

Condição: `esq.[Função do Sistema - Tickets] == dir.[Função do Sistema]`

→ [45] Expurgo Solicitado

## [33] Mes — Container

← [12] Ticket Medio

1. Renomear `Mês` → `Data`
2. Calcular `Mes`:

```
RIGHT("0" + STR(MONTH([Data])), 2) + "/" + STR(YEAR([Data]))
```

→ [159] União de colunas 3

## [34] Adequar colunas — Container

← [13] Resenhas EXP BR AppSheets (4. DATASOURCES) 2

1. Remover colunas: `Status SLA`
2. Remover colunas: `Prazo SLA (Brasil)`
3. Remover colunas: `Início da Contagem SLA (Brasil)`
4. Renomear `ID` → `Ticket`
5. Remover colunas: `Loja`
6. Remover colunas: `Nome Aplicativo`
7. Remover colunas: `Nome do Respondente`
8. Remover colunas: `Classificação de Estrelas`, `Star Rating`
9. Remover colunas: `Aplicativo`
10. Remover colunas: `_Hora da Resposta`
11. Remover colunas: `_Dia da Semana da Resposta`
12. Remover colunas: `Categoria da Resposta`
13. Remover colunas: `Categoria da Resposta 2`
14. Remover colunas: `Comentário Postado`
15. Renomear `Classificação da Resposta` → `Status de Classificação`
16. Remover colunas: `Resposta Fornecida`
17. Remover colunas: `Classificação do Ofensor`, `IDIOMA`
18. Renomear `Resp. pela resposta` → `Analista Resenha`
19. Remover colunas: `Data da Resposta`
20. Renomear `Analista Resenha` → `Responsavel`
21. Remover colunas: `App Nome`
22. Remover colunas: `Status de Classificação`
23. Calcular `Qtd Atendimentos`:

```
1
```
24. Calcular `Mes`:

```
// Pega o número do mês, adiciona um zero à esquerda se necessário, e une com o ano.
RIGHT("0" + STR(MONTH([Data Avaliação])), 2) + "/" + STR(YEAR([Data Avaliação]))
```
25. Calcular `Tipo`:

```
"Resenhas"
```
26. Remapear `Ticket`: "Resenha ID" ← null
27. Remover colunas: `Data Avaliação`
28. Renomear `Data da Resposta EXP` → `Data`

→ [168] Adição Resenhas

## [35] 16 e 17/03 — Container

← [14] MKT Brasil 5

→ [78] União de colunas 15

## [36] Limpar 6 — Container

← [15] Dynatrace

→ [46] Remoção de colunas; [49] União de linhas 13

## [37] ID e Analista — Container

← [17] ServiceCloud Analistas

1. Manter só: `Número do caso`, `Nome do usuário que realizou alteração`
2. Renomear `Nome do usuário que realizou alteração` → `Analista`
3. Renomear `Número do caso` → `ID SC`
4. Renomear `Analista` → `Analista SC`

→ [47] Analista ServiceCloud

## [38] Remover dados de 16 e 17/03 — Container

← [18] MKT Reativos

1. Calcular `Manter`:

```
IF DATE([Data Contato]) = #2026-03-16# OR DATE([Data Contato]) = #2026-03-17# THEN 
    "Remover"
ELSE 
    "Manter"
END
```
2. Excluir `Manter` em ['"Remover"']
3. Remover colunas: `Manter`

→ [48] União de linhas 17

## [39] Expurgo Solicitado — Container

_Descrição:_ Solicitado em 13/10 a alteração de Status N2 MKT para N3 MKT

← [19] MKT Brasil

1. Calcular `Status`:

```
IF [Protocol] = '27-1886943591851'
OR [Protocol] = '27-1906665748101'
OR [Protocol] = '27-878815962363'
OR [Protocol] = '27-3578724695830'
OR [Protocol] = '27-3672754412312'
OR [Protocol] = '27-551306272144'
OR [Protocol] = '27-2568007020714'
OR [Protocol] = '27-3893347478845'
THEN 'Resolvido N3 MKT'
ELSE [Status]
END
```

→ [67] União de linhas 25

## [40] Limpar 4 — Container

← [20] Expurgo

1. Renomear `Chamado/Protocolo` → `Protocolo`
2. Renomear `Autorizado Gestao Natura` → `Expurgo`

→ [94] União de colunas 1

## [41] Limpar 7 — Container

← [21] Dynatrace ate Julho

1. Remover colunas: `Mes`
2. Renomear `Conseguiu contato ?  ☎️` → `Conseguiu Contato?`
3. Renomear `Pedido finalizado ?` → `Pedido finalizado?`
4. Remover colunas: `Monitoração`
5. Remover colunas: `Sistema`
6. Remover colunas: `Hora do Alarme`
7. Remover colunas: `Data e Hora Início do Atendimento`
8. Renomear `Sist Operacional` → `Sistema Operacional`

→ [49] União de linhas 13

## [42] Nível — Container

← [22] RE - AppSheet

1. Calcular `Nível`:

```
// 1. Verifica primeiro se existe um ticket de N2 (INC, REQ, RITM)
IF CONTAINS(UPPER([N° do Chamado N2]), "INC") 
   OR CONTAINS(UPPER([N° do Chamado N2]), "REQ") 
   OR CONTAINS(UPPER([N° do Chamado N2]), "RITM") 
THEN "N2"

// 2. Se não tiver ticket N2, avalia a regra nova para 2026 em diante
ELSEIF YEAR([Data]) >= 2026 THEN
    
    IF ISNULL([Status de Finalização]) THEN "Não mapeado"

    // CLASSIFICAÇÃO: N1
    ELSEIF UPPER(TRIM([Status de Finalização])) == "ATUALIZAÇÃO DO APP" THEN "N1"
    ELSEIF UPPER(TRIM([Status de Finalização])) == "ENCERRADO PELO EXPCB - ATUALIZAÇÃO DO APP/ NAVEGADOR" THEN "N1"
    ELSEIF UPPER(TRIM([Status de Finalização])) == "EXCLUSÃO DE PEDIDO EM RASCUNHO" THEN "N1"
    ELSEIF UPPER(TRIM([Status de Finalização])) == "LIMPEZA DE CACHE/ NAVEGAÇÃO EM GUIA ANÔNIMA/ TROCA DE NAVEGADOR" THEN "N1"
    ELSEIF UPPER(TRIM([Status de Finalização])) == "ENCERRADO PELO EXPCB - LIMP. DE CACHE/ GUIA ANÔNIMA/ NAVEGADOR" THEN "N1"
    ELSEIF UPPER(TRIM([Status de Finalização])) == "ORIENTADA PROCESSO|REGRA" THEN "N1"
    ELSEIF UPPER(TRIM([Status de Finalização])) == "ENCERRADO PELO EXPCB - ORIENTADA PROCESSO | REGRA" THEN "N1"
    ELSEIF UPPER(TRIM([Status de Finalização])) == "REENVIO DOS TERMOS" THEN "N1"
    ELSEIF UPPER(TRIM([Status de Finalização])) == "REESTÍMULO NO AGREEMENTS" THEN "N1"
    ELSEIF UPPER(TRIM([Status de Finalização])) == "REESTÍMULO NO SALESFORCE" THEN "N1"
    ELSEIF UPPER(TRIM([Status de Finalização])) == "REPROCESSAMENTO DE CADASTRO" THEN "N1"
    ELSEIF UPPER(TRIM([Status de Finalização])) == "ENCERRADO PELO EXPCB - REPROCESSAMENTO DE CADASTRO" THEN "N1"
    ELSEIF UPPER(TRIM([Status de Finalização])) == "RESET DE SENHA" THEN "N1"

    // CLASSIFICAÇÃO: N2
    ELSEIF UPPER(TRIM([Status de Finalização])) == "CHAMADO" THEN "N2"
    ELSEIF UPPER(TRIM([Status de Finalização])) == "INCIDENTE CRÍTICO" THEN "N2"
    ELSEIF UPPER(TRIM([Status de Finalização])) == "REABERTURA DE CHAMADO" THEN "N2"

    // CLASSIFICAÇÃO: NEUTRO
    ELSEIF UPPER(TRIM([Status de Finalização])) == "AGUARD. RETORNO FV" THEN "NEUTRO"
    ELSEIF UPPER(TRIM([Status de Finalização])) == "CONTATO SEM INTERAÇÃO" THEN "NEUTRO"
    ELSEIF UPPER(TRIM([Status de Finalização])) == "CONTATO SEM SUCESSO" THEN "NEUTRO"
    ELSEIF UPPER(TRIM([Status de Finalização])) == "DIRECIONADO PARA O ATENDIMENTO" THEN "NEUTRO"
    ELSEIF UPPER(TRIM([Status de Finalização])) == "DIRECIONADO PARA O SERVICE DESK" THEN "NEUTRO"
    ELSEIF UPPER(TRIM([Status de Finalização])) == "DIRECIONADO PARA O TRANSPORTE" THEN "NEUTRO"
    ELSEIF UPPER(TRIM([Status de Finalização])) == "DIRECIONADO PARA TERCEIROS" THEN "NEUTRO"
    ELSEIF UPPER(TRIM([Status de Finalização])) == "FOLLOWUP" THEN "NEUTRO"
    ELSEIF UPPER(TRIM([Status de Finalização])) == "INCIDENTE CRÍTICO - EM ANDAMENTO" THEN "NEUTRO"
    ELSEIF UPPER(TRIM([Status de Finalização])) == "INCIDENTE CRÍTICO RESOLVIDO" THEN "NEUTRO"
    ELSEIF UPPER(TRIM([Status de Finalização])) == "INCIDENTE EM ANDAMENTO" THEN "NEUTRO"
    ELSEIF UPPER(TRIM([Status de Finalização])) == "INCIDENTE RESOLVIDO" THEN "NEUTRO"
    ELSEIF UPPER(TRIM([Status de Finalização])) == "JÁ ESTAVA RESOLVIDO" THEN "NEUTRO"
    ELSEIF UPPER(TRIM([Status de Finalização])) == "RESOLVIDO E-MAIL N3" THEN "NEUTRO"
    ELSEIF UPPER(TRIM([Status de Finalização])) == "RESOLVIDO MKT N3" THEN "NEUTRO"
    ELSEIF UPPER(TRIM([Status de Finalização])) == "RESOLVIDO N2 E-MAIL" THEN "NEUTRO"
    ELSEIF UPPER(TRIM([Status de Finalização])) == "RESOLVIDO N2 MKT" THEN "NEUTRO"
    ELSEIF UPPER(TRIM([Status de Finalização])) == "RESOLVIDO SEM ATUAÇÃO DO EXP" THEN "NEUTRO"

    // CLASSIFICAÇÃO: NÃO CONSIDERAR
    ELSEIF UPPER(TRIM([Status de Finalização])) == "AÇÕES EM MASSA" THEN "NÃO CONSIDERAR"
    ELSEIF UPPER(TRIM([Status de Finalização])) == "AGRADECIMENTOS" THEN "NÃO CONSIDERAR"
    ELSEIF UPPER(TRIM([Status de Finalização])) == "CARD EM BRANCO" THEN "NÃO CONSIDERAR"
    ELSEIF UPPER(TRIM([Status de Finalização])) == "EXPCN" THEN "NÃO CONSIDERAR"
    ELSEIF UPPER(TRIM([Status de Finalização])) == "FINALIZADO FORA DO HORÁRIO" THEN "NÃO CONSIDERAR"
    ELSEIF UPPER(TRIM([Status de Finalização])) == "FINALIZADO PELO BOT DURAÇÃO 1 HORA" THEN "NÃO CONSIDERAR"
    ELSEIF UPPER(TRIM([Status de Finalização])) == "HEALTH CHECK" THEN "NÃO CONSIDERAR"
    ELSEIF UPPER(TRIM([Status de Finalização])) == "TESTE" THEN "NÃO CONSIDERAR"

    ELSE "Não mapeado"
    END

// 3. Se for antes de 2026, aplica a regra antiga
ELSE
    IF UPPER([Status de Finalização]) == "CHAMADO" THEN "N2" 
    ELSEIF UPPER([Status de Finalização]) == "INCIDENTE CRÍTICO" THEN "N2"
    ELSEIF UPPER([Status de Finalização]) == "INCIDENTE EM ANDAMENTO" THEN "NEUTRO"
    ELSEIF UPPER([Status de Finalização]) == "INCIDENTE RESOLVIDO" THEN "NEUTRO"
    ELSE "N1" 
    END

END
```

→ [50] Manter Apenas Protocolo e Data Contato; [51] Requisição Eventual

## [43] AppSheets — Container

← [23] Registro de Acionamentos

1. Renomear `Protocolo` → `Protocolo Relacionado`
2. Renomear `ID` → `Protocolo`
3. Renomear `Data do contato` → `Data Contato`
4. Renomear `Analista` → `Responsável`
5. Renomear `Código do Impactado` → `CODIGO`
6. Renomear `Qtde de Atendimentos` → `Qtd Atendimentos`
7. Renomear `Pedido finalizado` → `PEDIDO FINALIZADO`
8. Renomear `Status de Organização` → `Status de Classificação`
9. Renomear `Status de Finalização` → `Status de finalização`
10. Calcular `Origem`:

```
"AppSheets"
```
11. Renomear `Chamado` → `CHAMADO`
12. Calcular `Setor Fim`:

```
IF [Canal de Entrada] = "E-mail - EXPCB (Gerentes)" THEN "E-mail - Experiência CB"

ELSEIF [Canal de Entrada] = "TD -  GV Antecipada" 
    OR [Canal de Entrada] = "TD - GV Antecipada" 
THEN "TD -  GV Antecipada"

ELSEIF [Canal de Entrada] = "Whats Franquia" THEN "Whats Franquias"
ELSEIF [Canal de Entrada] = "Whats GN" THEN "Whats GN"
ELSEIF [Canal de Entrada] = "Whats GV" THEN "Whats GV"

// Mantém o valor original caso não seja nenhum dos listados acima
ELSE [Canal de Entrada] 
END
```
13. Duplicar `Canal de Entrada-1`:

```
[Canal de Entrada]
```
14. Remapear `Canal de Entrada`: "E-mail - Experiência CB" ← "E-mail - EXPCB (Gerentes)"; "Whatsapp Enterprise - Natura CN" ← "TD -  GV Antecipada", "Whats Franquia", "TD - GV Antecipada", "Whats GV", "Whats GN"
15. Renomear `Canal de Entrada-1` → `Setor Entrada`

→ [52] Limpar 15

## [44] HC Exp Brasil — PublishExtract

← [26] Limpar 12

**Saída:** `4. DATASOURCES/HC Exp Brasil`

## [45] Expurgo Solicitado — Container

_Descrição:_ Solicitado em 13/10 a alteração de Status N2 MKT para N3 MKT

← [32] União de colunas 25

→ [53] Limpar 23

## [46] Remoção de colunas — Container

← [36] Limpar 6

1. Renomear `ID` → `Ticket`
2. Renomear `Pedido finalizado?` → `Pedido Finalizado`
3. Calcular `Tipo`:

```
"Dynatrace"
```
4. Calcular `Nivel`:

```
NULL
```
5. Calcular `Contato de Solução`:

```
NULL
```
6. Manter só: `Tipo`, `Nivel`, `Contato de Solução`, `Ticket`, `Data`, `Pedido Finalizado`
7. Calcular `Qtd Atendimentos`:

```
1
```

→ [153] União de linhas 11

## [47] Analista ServiceCloud — SuperAggregate

← [37] ID e Analista

**Agregar** agrupando por `ID SC`: MAX(`Analista SC`)

→ [166] União de colunas 23

## [48] União de linhas 17 — SuperUnion

← [38] Remover dados de 16 e 17/03; [24] Limpar 20

**Union** das entradas acima (colunas com o mesmo nome se juntam; cria `Table Names`).

→ [54] MKT

## [49] União de linhas 13 — SuperUnion

← [36] Limpar 6; [41] Limpar 7

**Union** das entradas acima (colunas com o mesmo nome se juntam; cria `Table Names`).

1. Remover colunas: `Table Names`

→ [55] Limpar 8

## [50] Manter Apenas Protocolo e Data Contato — Container

_Descrição:_ "Canal de Entrada" = "RE"

← [42] Nível

1. Manter só `Canal de entrada` em ['"RE"']
2. Calcular `Setor Fim`:

```
IF ISNULL([ID]) THEN "" ELSE "RE" END
```
3. Calcular `Protocolo1`:

```
IF ISNULL([ID]) THEN "" ELSE "Protocolo-RE" END
```
4. Manter só: `Nível`, `Setor Fim`, `Protocolo1`, `Data`, `Mercado`
5. Renomear `Protocolo1` → `Protocolo`
6. Renomear `Data` → `Data Contato`
7. Calcular `SLA do Primeiro Contato`:

```
IF ISNULL([Protocolo])THEN "" ELSE "Dentro do SLA" END
```
8. Calcular `Qtd Atendimentos`:

```
IF ISNULL([Protocolo])THEN "" ELSE "1" END
```
9. Mudar tipo: `Qtd Atendimentos` → integer

→ [56] Data Corte Ate 30/09/25; [57] Data Corte Franquias; [58] Data Corte a Partir 01/10/25

## [51] Requisição Eventual — Container

← [42] Nível

1. Manter só `Canal de entrada` em ['"Requisição Eventual"']
2. Mudar tipo: `Data de Finalização` → datetime
3. Remapear `Qtde de Atendimentos`: "1" ← null
4. Mudar tipo: `Qtde de Atendimentos` → integer

→ [59] União de colunas 23

## [52] Limpar 15 — Container

← [43] AppSheets

→ [61] Analitico

## [53] Limpar 23 — Container

← [45] Expurgo Solicitado

1. Remover colunas: `Função do Sistema`, `Função do Sistema - Tickets`
2. Renomear `Função do Sistema - Analitico` → `Função do Sistema`
3. Remapear `Qtd Atendimentos`: 1 ← null, 33923426

→ [60] Campos Calculados

## [54] MKT — Container

← [48] União de linhas 17

1. Calcular `Origem`:

```
"MKT"
```
2. Calcular `Protocolo Relacionado`:

```
""
```

→ [61] Analitico

## [55] Limpar 8 — Container

← [49] União de linhas 13

1. RangeFilter: `{"ranges": {"Data": [{"startValue": null, "includeStart": true, "endValue": null, "includeEnd": true}]}, "exclude": true}`
2. Excluir `Conseguiu Contato?` em [None]

→ [62] Exp Brasil Dynatrace

## [56] Data Corte Ate 30/09/25 — Container

← [50] Manter Apenas Protocolo e Data Contato

1. Filtro de data `Data Contato` (datetime): **até 2025-09-30 00:00:00**, sem nulos

→ [113] União MKT + RE (AppSheet)

## [57] Data Corte Franquias — Container

_Descrição:_ "Mercado" = "Empresarias"

← [50] Manter Apenas Protocolo e Data Contato

1. Filtro de data `Data Contato` (datetime): **a partir de 2025-10-01 00:00:00**, com nulos
2. Manter só `Mercado` em ['"EMPRESARIAS"']

→ [125] União de linhas 15

## [58] Data Corte a Partir 01/10/25 — Container

_Descrição:_ "Mercado" = "Cerrado" ou "Amazônia" ou "Araucária" ou "Atlântica" ou "Caatinga"

← [50] Manter Apenas Protocolo e Data Contato

1. Filtro de data `Data Contato` (datetime): **a partir de 2025-10-01 00:00:00**, sem nulos
2. Excluir `Mercado` em [None, '"EMPRESARIAS"']

→ [113] União MKT + RE (AppSheet)

## [59] União de colunas 23 — SuperJoin

← [51] Requisição Eventual (Right); [27] Tribo (Left)

**Join right**: esquerda = [27] Tribo, direita = [51] Requisição Eventual

Condição: `esq.[Função do Sistema] == dir.[Assunto / Função do sistema]`

→ [63] Requisição Eventual EXP BR

## [60] Campos Calculados — Container

← [53] Limpar 23

1. Calcular `Tipo`:

```
IF [Setor do Atendimento] = "EXPERIÊNCIA CB" THEN "Email"

ELSEIF [Setor do Atendimento] = "TD - GV Antecipada" 
    OR [Setor do Atendimento] = "Whats GN" 
    OR [Setor do Atendimento] = "Whats Franquia" 
    OR [Setor do Atendimento] = "Whats GV" THEN "WhatsApp"

ELSE NULL
END
```
2. Renomear `Status de Finalização` → `Status de finalização`
3. Duplicar `Data de Criação do Ticket-1`:

```
[Data de Criação do Ticket]
```
4. Renomear `Data de Criação do Ticket-1` → `Data Contato`

→ [64] WhtasAPP T; [65] Email

## [61] Analitico — SuperUnion

← [52] Limpar 15; [54] MKT

**Union** das entradas acima (colunas com o mesmo nome se juntam; cria `Table Names`).

1. Remover colunas: `Table Names-1`

→ [66] União de linhas 24

## [62] Exp Brasil Dynatrace — PublishExtract

← [55] Limpar 8

**Saída:** `4. DATASOURCES/Exp Brasil Dynatrace`

## [63] Requisição Eventual EXP BR — PublishExtract

← [59] União de colunas 23

**Saída:** `4. DATASOURCES/Requisição Eventual EXP BR`

## [64] WhtasAPP T — Container

← [60] Campos Calculados

1. Renomear `Setor do Atendimento` → `Setor Fim`
2. Remover colunas: `Tipo`
3. Renomear `ID do Ticket` → `Protocolo`
4. Remover colunas: `Data de Criação do Atendimento`
5. Remover colunas: `Estado`
6. Renomear `Data de Finalização` → `Encerrado em`
7. Renomear `Usuário Responsável` → `Responsável`
8. Remapear `PEDIDO FINALIZADO`: "SIM" ← "sim"; "NÃO SE APLICA" ← "nao_se_aplica"; "NÃO" ← "nao"
9. Calcular `Qtd Atendimentos2`:

```
// 1. Se o valor for válido e estiver no intervalo de 1 a 100, mantém o original
IF [Qtd Atendimentos] >= 1 AND [Qtd Atendimentos] <= 100 THEN 
    [Qtd Atendimentos]

// 2. Se for nulo, acima de 100, menor que 1 (ou qualquer outra inconsistência), força para 1
ELSE 
    1
END
```
10. Remover colunas: `Qtd Atendimentos`
11. Renomear `Qtd Atendimentos2` → `Qtd Atendimentos`
12. Remapear `Está em Fechamento?`: "NÃO" ← "nao"; "SIM" ← "sim"
13. Calcular `Canal de Entrada`:

```
"Whatsapp Enterprise - Natura CN"
```

→ [66] União de linhas 24

## [65] Email — Container

← [60] Campos Calculados

1. Duplicar `Setor do Atendimento-1`:

```
[Setor do Atendimento]
```
2. Renomear `Setor do Atendimento-1` → `Canal de Entrada`
3. Renomear `Canal de Entrada` → `Canal`
4. Remapear `Canal`: "Experiência CB" ← "EXPERIÊNCIA CB"
5. Duplicar `Estado-1`:

```
[Estado]
```
6. Renomear `Estado-1` → `Situação`
7. Remapear `Situação`: "Concluído" ← "Finalizado"
8. Renomear `ID do Ticket` → `Protocol`
9. Renomear `Data de Criação do Ticket` → `Data criação`
10. Renomear `Data de Finalização` → `Data Conclusão`
11. Renomear `Tipo` → `Tipo Canal`
12. Duplicar `Setor do Atendimento-1`:

```
[Setor do Atendimento]
```
13. Renomear `Setor do Atendimento-1` → `Setor`
14. Renomear `Usuário Responsável` → `Operador`
15. Renomear `Status de finalização` → `Status`
16. Renomear `Status de Classificação` → `Status de Classificação1`
17. Renomear `Data Conclusão` → `Data conclusão`
18. Renomear `Qtd Atendimentos` → `Qtd Atendimentos Tickets`

→ [67] União de linhas 25

## [66] União de linhas 24 — SuperUnion

← [64] WhtasAPP T; [61] Analitico

**Union** das entradas acima (colunas com o mesmo nome se juntam; cria `Table Names`).

→ [68] Limpar 18

## [67] União de linhas 25 — SuperUnion

← [39] Expurgo Solicitado; [65] Email

**Union** das entradas acima (colunas com o mesmo nome se juntam; cria `Table Names`).

→ [69] Limpar 24

## [68] Limpar 18 — Container

← [66] União de linhas 24

1. Duplicar `Função do Sistema-1`:

```
[Função do Sistema]
```
2. Remapear `Função do Sistema-1`: "CADASTRO" ← "CADASTRO - ZONEAMENTO DE CEP", "CADASTRO - ALTERAÇÃO CADASTRAL", "CADASTRO - APROVAÇÃO", "CADASTRO - BLOQUEIO", "CADASTRO - CESSADO", "CADASTRO - DIVERGÊNCIA DE ENDEREÇO", "CADASTRO - DUPLICADO", "CADASTRO - ESTRUTURA COMERCIAL", "CADASTRO - NOME DIVERGENTE", "CADASTRO - NOVO CADASTRO - CEP", "CADASTRO - REINÍCIO", "CADASTRO - REJEITADO", "CADASTRO - STATUS", "CADASTRO - TEMPO DE CASA"; "CAPTAÇÃO" ← "CAPTAÇÃO - VITRINE", "CAPTAÇÃO - BRINDE", "CAPTAÇÃO - COMPRA GARANTIDA", "CAPTAÇÃO - CONQUISTE PRODUTOS", "CAPTAÇÃO - COTAS DE PEDIDOS NO DIA", "CAPTAÇÃO - EXCLUSÃO DE RASCUNHO", "CAPTAÇÃO - INCORPORAÇÃO DE ITEM", "CAPTAÇÃO - ITEM INDISPONÍVEL", "CAPTAÇÃO - PAG EMANA PAY", "CAPTAÇÃO - PARCELAMENTO", "CAPTAÇÃO - PEDIDO MÍNIMO", "CAPTAÇÃO - PIX", "CAPTAÇÃO - PONTUAÇÃO", "CAPTAÇÃO - PRÉ VENDA", "CAPTAÇÃO - PRODUTO", "CAPTAÇÃO - PROMOÇÃO", "CAPTAÇÃO - RETROATIVO", "CAPTAÇÃO - SARRAFOS", "CAPTAÇÃO - SEGMENTAÇÃO", "CAPTAÇÃO - SESSÃO CONCORRENTE", "CAPTAÇÃO - TELA DE CHECKOUT", "CAPTAÇÃO - TELA DE ENDEREÇO", "CAPTAÇÃO - TELA DE OPORTUNIDADES", "CAPTAÇÃO - VALE PONTOS", "CAPTA&#199;&#195;O"; "CARTÃO DE CRÉDITO" ← "CART&#195;O DE CR&#201;DITO"; "COBRANÇA" ← "COBRAN&#199;A"; "COMISSÃO / LUCRATIVIDADE" ← "COMISS&#195;O/ LUCRATIVIDADE"; "CONTRATAÇÃO DE LÍDER" ← "CONTRATA&#199;&#195;O DE L&#205;DER"; "ESPAÇO DIGITAL" ← "espaco_digital_-_falta_aceite_de_termos", "ESPA&#199;O DIGITAL - CESSADO", "ESPA&#199;O DIGITAL - FALTA ACEITE DE TERMOS", "ESPA&#199;O DIGITAL - MINHA DIVULGA&#199;&#195;O", "ESPA&#199;O DIGITAL - MINHAS VENDAS", "ESPA&#199;O DIGITAL - SUSPENSO", "ESPA&#199;O DIGITAL - URL", "ESPAÇO DIGITAL - AGUARDANDO PRIMEIRO PEDIDO", "ESPAÇO DIGITAL - BLOQUEADO", "ESPAÇO DIGITAL - CESSADO", "ESPAÇO DIGITAL - COMPARTILHAR LINK", "ESPAÇO DIGITAL - DIVERGÊNCIA DE DADOS CADASTRAIS", "ESPAÇO DIGITAL - ESPAÇO DUPLICADO", "ESPAÇO DIGITAL - FALTA ACEITE DE TERMOS", "ESPAÇO DIGITAL - INDISPONÍVEL", "ESPAÇO DIGITAL - MEUS CLIENTES", "ESPAÇO DIGITAL - MEUS SERVIÇOS DIGITAIS", "ESPAÇO DIGITAL - MINHA DIVULGAÇÃO", "ESPAÇO DIGITAL - MINHAS VENDAS", "ESPAÇO DIGITAL - NATURA ENTREGA", "ESPAÇO DIGITAL - PAY - CONTA PAY REPROVADA", "ESPAÇO DIGITAL - PAYMENT ACCOUNTS", "ESPAÇO DIGITAL - PAYMENT ACCOUNTS (PENDENCIA)", "ESPAÇO DIGITAL - PEDIDO DEFAULT", "ESPAÇO DIGITAL - PERSONALIZAÇÃO", "ESPAÇO DIGITAL - REGISTER ACTIVE", "ESPAÇO DIGITAL - STATUS PEDIDO CF", "ESPAÇO DIGITAL - SUSPENSO", "ESPAÇO DIGITAL - URL", "ESPAÇO DIGITAL - URL INDISPONÍVEL", "ESPAÇO DIGITAL - VISITAS"; "EXTINÇÃO DE GRUPO" ← "EXTIN&#199;&#195;O DE GRUPO"; "MINHA LOJA" ← "MINHA LOJA - ACESSO", "MINHA LOJA - ATIVAÇÃO", "MINHA LOJA - DIVERGÊNCIA DE DADOS CADASTRAIS", "MINHA LOJA - FALTA ACEITE DE TERMOS", "MINHA LOJA - INDISPONÍVEL", "MINHA LOJA - MEUS CLIENTES", "MINHA LOJA - MEUS SERVIÇOS DIGITAIS", "MINHA LOJA - MINHA DIVULGAÇÃO", "MINHA LOJA - MINHAS VENDAS", "MINHA LOJA - NATURA ENTREGA", "MINHA LOJA - PAINEL DE VENDAS", "MINHA LOJA - PAYMENT ACCOUNTS (PENDENCIA)", "MINHA LOJA - PEDIDO DEFAULT", "MINHA LOJA - PERSONALIZAÇÃO", "MINHA LOJA - PRODUTO", "MINHA LOJA - REGISTER ACTIVE", "MINHA LOJA - RELATÓRIOS", "MINHA LOJA - STATUS PEDIDO CF"; "MOVIMENTAÇÃO" ← "MOVIMENTA&#199;&#195;O"; "NÃO ESPECIFICADO" ← "N&#195;O ESPECIFICADO"; "PAINEL DE INDICADORES" ← "PAINEL DE INDICADORES - VOLUME DE PONTOS", "PAINEL DE INDICADORES - ACELERADOR", "PAINEL DE INDICADORES - ATIVAS", "PAINEL DE INDICADORES - ATIVAS PRATA +", "PAINEL DE INDICADORES - ATIVIDADE SEMENTE + BRONZE", "PAINEL DE INDICADORES - CADASTRO", "PAINEL DE INDICADORES - CONTABILIZAÇÃO DE PEDIDO", "PAINEL DE INDICADORES - CRER PARA VER", "PAINEL DE INDICADORES - ESPAÇO DIGITAL", "PAINEL DE INDICADORES - INÍCIO", "PAINEL DE INDICADORES - RECEITA BRUTA", "PAINEL DE INDICADORES - SALDO DE CADASTRO"; "PLANO DE CRESCIMENTO" ← "PLANO DE CRESCIMENTO - CONTABILIZAÇÃO DE PEDIDO", "PLANO DE CRESCIMENTO - DIVERGÊNCIA NO NÍVEL"; "PROMOÇÃO" ← "PROMO&#199;&#195;O"; "RELATÓRIO" ← "RELATÓRIO - TODOS OS CADASTROS", "RELATÓRIO - ACOMPANHAMENTO DE PEDIDOS", "RELATÓRIO - ANÁLISE DE CANAL", "RELATÓRIO - ANÁLISE DE RESULTADOS", "RELATÓRIO - BALDINHO", "RELATÓRIO - CBs AGUARDANDO PRIMEIRO PEDIDO", "RELATÓRIO - CBs SEM PEDIDO NO CICLO", "RELATÓRIO - ESPAÇO DIGITAL COM VENDAS", "RELATÓRIO - IAP", "RELATÓRIO - INADIMPLENTES", "RELATÓRIO - INÍCIO", "RELATÓRIO - MINHA REDE", "RELATÓRIO - PLANO DE CRESCIMENTO", "RELATÓRIO - RANKING DE POTENCIAIS LÍDERES", "RELATÓRIO - RECUPERADAS", "RELATÓRIO - SUGERIDAS PARA INÍCIO", "RELATÓRIO - TODAS AS CBs"; "REMUNERAÇÃO" ← "REMUNERA&#199;&#195;O"; "RESCISÃO LÍDER" ← "RESCIS&#195;O L&#205;DER"; "VERSÃO APP" ← "VERS&#195;O APP"; "RELATÓRIO ACOMPANHAMENTO DE PEDIDO" ← "RELAT&#211;RIO ACOMPANHAMENTO DE PEDIDO"; "RELATÓRIO ANÁLISE DE RESULTADOS" ← "RELAT&#211;RIO AN&#193;LISE DE RESULTADOS"; "RELATÓRIO BEM-VINDAS" ← "RELAT&#211;RIO BEM-VINDAS"; "RELATÓRIO INADIMPLENTES" ← "RELAT&#211;RIO INADIMPLENTES"; "RELATÓRIO MINHA REDE" ← "RELAT&#211;RIO MINHA REDE"; "RELATÓRIO TODOS OS CADASTROS" ← "RELAT&#211;RIO TODOS OS CADASTROS"; "INDICADOR DE ESPAÇO DIGITAL" ← "INDICADOR DE ESPA&#199;O DIGITAL"; "INDICADOR DE ESPAÇO DIGITAL COM VENDAS" ← "INDICADOR DE ESPA&#199;O DIGITAL COM VENDAS"; "ANÁLISE DE CRÉDITO" ← "AN&#193;LISE DE CR&#201;DITO"
3. Remapear `Qtd Atendimentos`: 1 ← 0

→ [70] Remover protocolos de 16/01/26; [71] Join MKT Completo

## [69] Limpar 24 — Container

← [67] União de linhas 25

→ [72] Situação = Concluído; [73] Situação = Concluído; [74] Em Aberto

## [70] Remover protocolos de 16/01/26 — Container

← [68] Limpar 18

1. Remover colunas: `Table Names`
2. Calcular `Remover`:

```
//Protocolos de 16/01/2026 das 15h às 17h que foram expurgados pela Val, pois a operação estava em treinamento.
IF [Protocolo] = '27-3339074528343'
OR [Protocolo] = '27-2731512014957'
OR [Protocolo] = '27-2904318350282'
OR [Protocolo] = '27-3274191871250'
OR [Protocolo] = '27-1017172412942'
OR [Protocolo] = '27-1323454360836'
OR [Protocolo] = '27-840233661631'
OR [Protocolo] = '27-1658180827597'
OR [Protocolo] = '27-4171539501612'
OR [Protocolo] = '27-697880995829'
OR [Protocolo] = '27-987849004968'
OR [Protocolo] = '27-2243631648863'
OR [Protocolo] = '27-121511041945'
OR [Protocolo] = '27-59784361352'
OR [Protocolo] = '27-960421944528'
OR [Protocolo] = '27-2371832047246'
OR [Protocolo] = '27-68034162771'
OR [Protocolo] = '27-819572025631'
OR [Protocolo] = '27-2813678340549'
OR [Protocolo] = '27-3976328987274'
OR [Protocolo] = '27-2901829995249'
OR [Protocolo] = '27-2981151663445'
OR [Protocolo] = '27-3911544075322'
OR [Protocolo] = '27-567578650620'
OR [Protocolo] = '27-1841675204173'
OR [Protocolo] = '27-2433323861609'
THEN "Excluir"
ELSE "Manter"
END
```
3. Excluir `Remover` em ['"Excluir"']
4. Remover colunas: `Remover`

→ [75] Histórico < 202610; [76] A partir de 202610

## [71] Join MKT Completo — Container

← [68] Limpar 18

→ [80] União de colunas 7; [77] Protocolo e Qtd Atendimento e Responsavel

## [72] Situação = Concluído — Container

← [69] Limpar 24

1. Manter só `Situação` em ['"Concluído"']
2. Manter só `Canal` em ['"Experiência CB"', '"APP AVON CF"', '"APP NATURA"', '"MINHA CONSULTORIA"']
3. Renomear `Protocol` → `Protocolo`

→ [78] União de colunas 15

## [73] Situação = Concluído — Container

_Descrição:_ TMO em segundos e Status = EXPCN

← [69] Limpar 24

1. Manter só `Situação` em ['"Concluído"']
2. Calcular `Tempo Medio em Segundos`:

```
DATEDIFF('second', [Data criação], [Data conclusão])
```
3. Calcular `Status2`:

```
// 1. Se o status NÃO for "Expcn", retorna o valor original (as outras duas opções).
IF [Status] <> "EXPCN" THEN
    [Status]

// 2. Se FOR "Expcn", verifica a data de corte (01/Nov/2025).
ELSEIF [Data conclusão] < MAKEDATE(2025, 11, 1) THEN
    "EXPCN"

// 3. Se for "Expcn" E a data for 01/Nov/2025 ou posterior.
ELSE
    "EXPCN Desconsiderar"
END
```
4. Manter só `Status` em ['"EXPCN"', '"Resolvido N2 MKT"', '"Resolvido N2 e-mail"', '"Resolvido MKT N3"', '"Resolvido E-mail N3"']
5. Remover colunas: `Status`
6. Renomear `Status2` → `Status`

→ [79] MKT Brasil Completo

## [74] Em Aberto — Container

← [69] Limpar 24

1. Manter só `Situação` em ['"Em aberto"']
2. Calcular `Tempo Medio em Segundos`:

```
DATEDIFF('second', [Data criação], NOW())

```
3. Calcular `Faixa de Aging`:

```
IF ([Tempo Medio em Segundos] / 86400) <= 1 THEN "1 - Até 24 horas"
ELSEIF ([Tempo Medio em Segundos] / 86400) <= 3 THEN "2 - 01 a 03 dias"
ELSEIF ([Tempo Medio em Segundos] / 86400) <= 7 THEN "3 - 04 a 07 dias"
ELSEIF ([Tempo Medio em Segundos] / 86400) <= 15 THEN "4 - 08 a 15 dias"
ELSEIF ([Tempo Medio em Segundos] / 86400) <= 30 THEN "5 - 16 a 30 dias"
ELSE "6 - Mais de 30 dias"
END
```
4. Calcular `Aging`:

```
DATEDIFF('day', [Data criação], TODAY())
```

→ [80] União de colunas 7

## [75] Histórico < 202610 — Container

← [70] Remover protocolos de 16/01/26

1. Filtro:

```
[Data Contato] < #2026-10-01# OR ISNULL([Data Contato])
```

→ [81] Join 2

## [76] A partir de 202610 — Container

← [70] Remover protocolos de 16/01/26

1. Filtro:

```
[Data Contato] >= #2026-10-01#
```

→ [82] União de colunas 5

## [77] Protocolo e Qtd Atendimento e Responsavel — Container

← [71] Join MKT Completo

1. Manter só: `Protocolo`, `Qtd Atendimentos`, `Responsável`

→ [91] União de colunas 13

## [78] União de colunas 15 — SuperJoin

← [35] 16 e 17/03 (Left); [72] Situação = Concluído (Right)

**Join right**: esquerda = [35] 16 e 17/03, direita = [72] Situação = Concluído

Condição: `esq.[Protocolo2] == dir.[Protocolo]`

1. (antes do join, lado esquerdo) Remover colunas: `Ticket`, `Empresa`, `Nome`, `CPF/CNPJ`, `Número do Contrato`, `Valor do Contrato`, `CODIGO`, `GV`, `FUNÇÃO`
2. (antes do join, lado esquerdo) Remover colunas: `PEDIDO FINALIZADO`, `CONTATO DE SOLUÇÃO`, `CHAMADO`, `Fornecedor`, `testeLis`, `Ciclo - Health Check`, `Recebidos - Health Check`, `CATEGORIA 1 (WR TRANSP)`, `CATEGORIA 2 (WR TRANSP)`, `Origem Health Check?`, `Está em Fechamento?`, `Código do Impactado`, `Ciclo Vigente`, `SETOR`, `MERCADO`, `Resposta pedido duplicado`, `Dados bancarios`, `E-mail`, `Data Contato`, `Responsável`, `Tempo até ser atendido`, `Tempo do atendimento`, `Primeiro Tempo de Espera`, `Tempo Médio de Espera`, `Tempo de Operação`
3. (antes do join, lado esquerdo) Remover colunas: `Fone Cliente`, `Canal de Entrada`, `Setor Entrada`, `Setor Fim`, `Qtde Mensagens`, `Encerrado em`, `Observações`, `Campos adicionais Web Chat`, `Quantidade de Tickets`
4. (antes do join, lado esquerdo) Renomear `Protocolo` → `Protocolo2`

→ [83] Ajuste dias 16 e 17/03

## [79] MKT Brasil Completo — PublishExtract

← [73] Situação = Concluído

**Saída:** `4. DATASOURCES/MKT Brasil Completo`

## [80] União de colunas 7 — SuperJoin

← [71] Join MKT Completo (Right); [74] Em Aberto (Left)

**Join left**: esquerda = [74] Em Aberto, direita = [71] Join MKT Completo

Condição: `esq.[Protocol] == dir.[Protocolo]`

1. (antes do join, lado direito) Remover colunas: `Origem`
2. (antes do join, lado direito) Remover colunas: `Table Names`
3. (antes do join, lado direito) Remover colunas: `Empresa`, `Source_id CTWA`
4. (antes do join, lado direito) Remover colunas: `Nome`
5. (antes do join, lado direito) Remover colunas: `CPF/CNPJ`
6. (antes do join, lado direito) Remover colunas: `Número do Contrato`
7. (antes do join, lado direito) Remover colunas: `Valor do Contrato`
8. (antes do join, lado direito) Remover colunas: `GV`
9. (antes do join, lado direito) Remover colunas: `FUNÇÃO`
10. (antes do join, lado direito) Remover colunas: `CONTATO DE SOLUÇÃO`
11. (antes do join, lado direito) Remover colunas: `Fornecedor`, `testeLis`
12. (antes do join, lado direito) Remover colunas: `Ciclo - Health Check`, `Recebidos - Health Check`
13. (antes do join, lado direito) Remover colunas: `CATEGORIA 1 (WR TRANSP)`, `CATEGORIA 2 (WR TRANSP)`
14. (antes do join, lado direito) Remover colunas: `SOLUÇÃO APLICADA`
15. (antes do join, lado direito) Remover colunas: `Origem Health Check?`
16. (antes do join, lado direito) Remover colunas: `Está em Fechamento?`
17. (antes do join, lado direito) Remover colunas: `Código do Impactado`
18. (antes do join, lado direito) Remover colunas: `Ciclo Vigente`
19. (antes do join, lado direito) Remover colunas: `SETOR`
20. (antes do join, lado direito) Remover colunas: `MERCADO`
21. (antes do join, lado direito) Remover colunas: `E-mail`
22. (antes do join, lado direito) Remover colunas: `Tempo até ser atendido`
23. (antes do join, lado direito) Remover colunas: `Tempo do atendimento`
24. (antes do join, lado direito) Remover colunas: `Primeiro Tempo de Espera`
25. (antes do join, lado direito) Remover colunas: `Tempo Médio de Espera`, `Tempo de Operação`, `Fone Cliente`, `Qtde Mensagens`, `Encerrado em`, `Observações`
26. Remover colunas: `Protocolo`, `CODIGO`, `PEDIDO FINALIZADO`, `Data Contato`, `Responsável`, `Campos adicionais Web Chat`, `Resposta pedido duplicado`, `Dados bancarios`, `Protocolo Relacionado`

→ [84] Backlog; [85] Data Hoje

## [81] Join 2 — SuperJoin

← [3] Tribos MKT (Right); [75] Histórico < 202610 (Left)

**Join left**: esquerda = [75] Histórico < 202610, direita = [3] Tribos MKT

Condição: `esq.[Função do Sistema] == dir.[Função do Sistema]`

→ [86] Union 1

## [82] União de colunas 5 — SuperJoin

← [25] Aggregate 1 (Left); [76] A partir de 202610 (Right)

**Join right**: esquerda = [25] Aggregate 1, direita = [76] A partir de 202610

Condição: `esq.[Função do Sistema] == dir.[Função do Sistema]`

→ [86] Union 1

## [83] Ajuste dias 16 e 17/03 — Container

← [78] União de colunas 15

1. Calcular `Status F`:

```
IF (DATE([Data criação]) = #2026-03-16# OR DATE([Data criação]) = #2026-03-17#)
OR (DATE([Data conclusão]) = #2026-03-16# OR DATE([Data conclusão]) = #2026-03-17#)
THEN 

	IF ISNULL([Status de finalização]) OR [Status de finalização] = ""
		THEN [Status]
	ELSE
		[Status de finalização]
	END

ELSE 

	[Status]

END

```
2. Renomear `Status` → `Status Fin`
3. Renomear `Status F` → `Status`
4. Remover colunas: `Status Fin`

→ [87] Nivel

## [84] Backlog — Container

← [80] União de colunas 7

1. Cálculo rápido `CHAMADO`:

```
TRIM(REGEXP_REPLACE([CHAMADO], '[[:space:]]+', ' '))
```

→ [88] Adequação Nomes Colunas

## [85] Data Hoje — Container

← [80] União de colunas 7

1. Calcular `Data Hoje`:

```
TODAY()
```
2. Calcular `Carimbo Tempo`:

```
NOW()
```

→ [89] Volume Backlog

## [86] Union 1 — SuperUnion

← [81] Join 2; [82] União de colunas 5

**Union** das entradas acima (colunas com o mesmo nome se juntam; cria `Table Names`).

→ [90] Limpar 13

## [87] Nivel — Container

← [83] Ajuste dias 16 e 17/03

1. Calcular `Nivel`:

```
IF YEAR([Data conclusão]) >= 2026 THEN
    // --- INÍCIO DA REGRA NOVA (2026 em diante) ---
    IF ISNULL([Status]) THEN "Não mapeado"

    // 1. CLASSIFICAÇÃO: N1
    ELSEIF UPPER(TRIM([Status])) == "ATUALIZAÇÃO DO APP" THEN "N1"
    ELSEIF UPPER(TRIM([Status])) == "ENCERRADO PELO EXPCB - ATUALIZAÇÃO DO APP/ NAVEGADOR" THEN "N1"
    ELSEIF UPPER(TRIM([Status])) == "EXCLUSÃO DE PEDIDO EM RASCUNHO" THEN "N1"
    ELSEIF UPPER(TRIM([Status])) == "LIMPEZA DE CACHE/ NAVEGAÇÃO EM GUIA ANÔNIMA/ TROCA DE NAVEGADOR" THEN "N1"
    ELSEIF UPPER(TRIM([Status])) == "ENCERRADO PELO EXPCB - LIMP. DE CACHE/ GUIA ANÔNIMA/ NAVEGADOR" THEN "N1"
    ELSEIF UPPER(TRIM([Status])) == "ORIENTADA PROCESSO|REGRA" THEN "N1"
    ELSEIF UPPER(TRIM([Status])) == "ENCERRADO PELO EXPCB - ORIENTADA PROCESSO | REGRA" THEN "N1"
    ELSEIF UPPER(TRIM([Status])) == "REENVIO DOS TERMOS" THEN "N1"
    ELSEIF UPPER(TRIM([Status])) == "REESTÍMULO NO AGREEMENTS" THEN "N1"
    ELSEIF UPPER(TRIM([Status])) == "REESTÍMULO NO SALESFORCE" THEN "N1"
    ELSEIF UPPER(TRIM([Status])) == "REPROCESSAMENTO DE CADASTRO" THEN "N1"
    ELSEIF UPPER(TRIM([Status])) == "ENCERRADO PELO EXPCB - REPROCESSAMENTO DE CADASTRO" THEN "N1"
    ELSEIF UPPER(TRIM([Status])) == "RESET DE SENHA" THEN "N1"

    // 2. CLASSIFICAÇÃO: N2
    ELSEIF UPPER(TRIM([Status])) == "CHAMADO" THEN "N2"
    ELSEIF UPPER(TRIM([Status])) == "INCIDENTE CRÍTICO" THEN "N2"
    ELSEIF UPPER(TRIM([Status])) == "REABERTURA DE CHAMADO" THEN "N2"

    // 3. CLASSIFICAÇÃO: NEUTRO
    ELSEIF UPPER(TRIM([Status])) == "AGUARD. RETORNO FV" THEN "NEUTRO"
    ELSEIF UPPER(TRIM([Status])) == "CONTATO SEM INTERAÇÃO" THEN "NEUTRO"
    ELSEIF UPPER(TRIM([Status])) == "CONTATO SEM SUCESSO" THEN "NEUTRO"
    ELSEIF UPPER(TRIM([Status])) == "DIRECIONADO PARA O ATENDIMENTO" THEN "NEUTRO"
    ELSEIF UPPER(TRIM([Status])) == "DIRECIONADO PARA O SERVICE DESK" THEN "NEUTRO"
    ELSEIF UPPER(TRIM([Status])) == "DIRECIONADO PARA O TRANSPORTE" THEN "NEUTRO"
    ELSEIF UPPER(TRIM([Status])) == "DIRECIONADO PARA TERCEIROS" THEN "NEUTRO"
    ELSEIF UPPER(TRIM([Status])) == "FOLLOWUP" THEN "NEUTRO"
    ELSEIF UPPER(TRIM([Status])) == "INCIDENTE CRÍTICO - EM ANDAMENTO" THEN "NEUTRO"
    ELSEIF UPPER(TRIM([Status])) == "INCIDENTE CRÍTICO RESOLVIDO" THEN "NEUTRO"
    ELSEIF UPPER(TRIM([Status])) == "INCIDENTE EM ANDAMENTO" THEN "NEUTRO"
    ELSEIF UPPER(TRIM([Status])) == "INCIDENTE RESOLVIDO" THEN "NEUTRO"
    ELSEIF UPPER(TRIM([Status])) == "JÁ ESTAVA RESOLVIDO" THEN "NEUTRO"
    ELSEIF UPPER(TRIM([Status])) == "RESOLVIDO E-MAIL N3" THEN "NEUTRO"
    ELSEIF UPPER(TRIM([Status])) == "RESOLVIDO MKT N3" THEN "NEUTRO"
    ELSEIF UPPER(TRIM([Status])) == "RESOLVIDO N2 E-MAIL" THEN "NEUTRO"
    ELSEIF UPPER(TRIM([Status])) == "RESOLVIDO N2 MKT" THEN "NEUTRO"
    ELSEIF UPPER(TRIM([Status])) == "RESOLVIDO SEM ATUAÇÃO DO EXP" THEN "NEUTRO"

    // 4. CLASSIFICAÇÃO: NÃO CONSIDERAR
    ELSEIF UPPER(TRIM([Status])) == "AÇÕES EM MASSA" THEN "NÃO CONSIDERAR"
    ELSEIF UPPER(TRIM([Status])) == "AGRADECIMENTOS" THEN "NÃO CONSIDERAR"
    ELSEIF UPPER(TRIM([Status])) == "CARD EM BRANCO" THEN "NÃO CONSIDERAR"
    ELSEIF UPPER(TRIM([Status])) == "EXPCN" THEN "NÃO CONSIDERAR"
    ELSEIF UPPER(TRIM([Status])) == "FINALIZADO FORA DO HORÁRIO" THEN "NÃO CONSIDERAR"
    ELSEIF UPPER(TRIM([Status])) == "FINALIZADO PELO BOT DURAÇÃO 1 HORA" THEN "NÃO CONSIDERAR"
    ELSEIF UPPER(TRIM([Status])) == "HEALTH CHECK" THEN "NÃO CONSIDERAR"
    ELSEIF UPPER(TRIM([Status])) == "TESTE" THEN "NÃO CONSIDERAR"

    // Retorno para novos status que ainda não estão mapeados
    ELSE "Não mapeado"
    END

ELSE
    // --- INÍCIO DA REGRA ANTIGA (Antes de 2026) ---
    IF UPPER([Status]) == "CHAMADO" THEN "N2" 
    ELSEIF UPPER([Status]) == "INCIDENTE CRÍTICO" THEN "N2"
    ELSEIF UPPER([Status]) == "INCIDENTE EM ANDAMENTO" THEN "NEUTRO"
    ELSEIF UPPER([Status]) == "INCIDENTE RESOLVIDO" THEN "NEUTRO"
    ELSE "N1" 
    END
END
```

→ [91] União de colunas 13

## [88] Adequação Nomes Colunas — Container

← [84] Backlog

→ [92] União de colunas 27

## [89] Volume Backlog — SuperAggregate

← [85] Data Hoje

**Agregar** agrupando por `Data Hoje`: COUNT(`Protocol`), MAX(`Carimbo Tempo`)

→ [93] Histórico Backlog Diário

## [90] Limpar 13 — Container

← [86] Union 1

1. Remover colunas: `Função do Sistema`
2. Renomear `Função do Sistema-1` → `Função do Sistema`

→ [94] União de colunas 1

## [91] União de colunas 13 — SuperJoin

← [87] Nivel (Left); [77] Protocolo e Qtd Atendimento e Responsavel (Right)

**Join left**: esquerda = [87] Nivel, direita = [77] Protocolo e Qtd Atendimento e Responsavel

Condição: `esq.[Protocolo2] == dir.[Protocolo]`

→ [95] Ajuste Qtd Atendimento

## [92] União de colunas 27 — SuperJoin

← [31] Remoção de colunas (Left); [88] Adequação Nomes Colunas (Right)

**Join right**: esquerda = [31] Remoção de colunas, direita = [88] Adequação Nomes Colunas

Condição: `esq.[Protocolo Analitico] == dir.[Protocol]`

→ [96] Limpar 28

## [93] Histórico Backlog Diário — PublishExtract

← [89] Volume Backlog

**Saída:** `4. DATASOURCES/Histórico Backlog Diário`

## [94] União de colunas 1 — SuperJoin

← [40] Limpar 4 (Left); [90] Limpar 13 (Right)

**Join right**: esquerda = [40] Limpar 4, direita = [90] Limpar 13

Condição: `esq.[Protocolo] == dir.[Protocolo]`

1. Remover colunas: `Protocolo`, `Referencia`, `Data`

→ [97] Alterações Comuns MKT

## [95] Ajuste Qtd Atendimento — Container

← [91] União de colunas 13

1. Remover colunas: `Protocolo-1`

→ [98] Limpar 25

## [96] Limpar 28 — Container

← [92] União de colunas 27

1. Renomear `CHAMADO` → `CHAMADO1`
2. Calcular `CHAMADO`:

```
IF ISNULL([CHAMADO-1]) THEN
	[CHAMADO1]
ELSE
	[CHAMADO-1]
END
```
3. Remover colunas: `CHAMADO-2`, `CHAMADO-1`, `CHAMADO1`
4. Remover colunas: `Observações-1`
5. Remover colunas: `Função do Sistema`
6. Calcular `Função do Sistema`:

```
IF NOT ISNULL([Função do Sistema Analitico]) THEN 
    [Função do Sistema Analitico]

ELSEIF NOT ISNULL([Função do Sistema-1]) THEN 
    [Função do Sistema-1]

ELSE 
    [Função do Sistema-2]
END
```
7. Remover colunas: `Função do Sistema-2`, `Função do Sistema-1`, `Função do Sistema Analitico`
8. Remover colunas: `Table Names-1`, `Table Names`

→ [99] União de colunas 27

## [97] Alterações Comuns MKT — Container

_Descrição:_ Remoção em "Status Classificação" de "Helthcheck". Remoção de opções em "Status Classificação". Substituição em "Qtd Atendimento".

← [94] União de colunas 1

1. RichDiscreteValueFilter: `{"exclude": true, "values": {"Status de Classificação": ["\"HEALTH CHECK - CLASSIFICAÇÃO\""]}, "datatype": "string", "fieldId": "b747af6a-ebb2-4600-bb2c-587b8e9ddba5-Status de Classificação", "outOfSampleValues": null}`
2. RichDiscreteValueFilter: `{"exclude": true, "values": {"Status de finalização": ["\"AGRADECIMENTOS\"", "\"EXPCN\"", "\"TESTE\"", "\"FINALIZADO FORA DO HORÁRIO\"", "\"CENTRAL DE COMANDO\"", "\"Finalizado pelo Bot duração 1 hora\"", "\"HEALTH CHECK\"", "\"Feriado 01/05/2025\"", "\"AÃ‡Ã•ES EM MASSA\"", "\"Ações em massa\"", "\"Card Em Branco\"", "\"EXPCN - CLASSIFICAÇÃO\"", "\"FINALIZADO FORA DO HORÃRIO\"", "\"Finalizado pelo Bot duraÃ§Ã£o 1 hora\"", "\"HEALTHCHECK\""]}, "datatype": "string", "fieldId": "97bf6475-239e-46ca-b6cc-805db3e785bd-Status de Finalização-ca220788-c690-435b-92fb-cb414099bd40-Status de finalização", "outOfSampleValues": null}`
3. Remapear `Qtd Atendimentos`: 1 ← null, 683, 500, 496, 490, 485, 477, 473, 436, 336, 324, 323, 263, 163, 159, 154, 153, 121, 120, 105
4. Cálculo rápido `Status de Classificação`:

```
REPLACE([Status de Classificação], " - CLASSIFICAÇÃO", "")
```
5. Calcular `Tempo Medio - Segundos`:

```
DATEDIFF('second', [Data Contato], [Encerrado em])
```
6. Calcular `Data Contato Ajustada`:

```
// Campo: Data Contato Ajustada
// Objetivo: Jogar inícios fora do expediente para o próximo horário útil (08:00)

IF DATEPART('weekday', [Data Contato]) = 1 THEN 
    // Domingo -> Joga para Segunda 08:00
    MAKEDATETIME(DATE(DATEADD('day', 1, [Data Contato])), MAKETIME(8,0,0))

ELSEIF DATEPART('weekday', [Data Contato]) = 7 THEN 
    // Sábado -> Joga para Segunda 08:00
    MAKEDATETIME(DATE(DATEADD('day', 2, [Data Contato])), MAKETIME(8,0,0))

ELSEIF DATEPART('hour', [Data Contato]) < 8 THEN 
    // Madrugada (00h-07h59) -> Joga para hoje às 08:00
    MAKEDATETIME(DATE([Data Contato]), MAKETIME(8,0,0))

ELSEIF DATEPART('hour', [Data Contato]) >= 20 THEN 
    // Opcional: Se houver regra para depois das 20h ou 23h, ajuste aqui. 
    // Se não, o cálculo de segundos vai parar na hora limite automaticamente.
    [Data Contato]
    
ELSE 
    // Horário Comercial -> Mantém original
    [Data Contato]
END
```
7. Calcular `Encerrado em Ajustado`:

```
// Campo: Encerrado em Ajustado
// Objetivo: Jogar fins fora do expediente para o início do expediente útil

IF DATEPART('weekday', [Encerrado em]) = 1 THEN 
    // Domingo -> Segunda 08:00
    MAKEDATETIME(DATE(DATEADD('day', 1, [Encerrado em])), MAKETIME(8,0,0))

ELSEIF DATEPART('weekday', [Encerrado em]) = 7 THEN 
    // Sábado -> Segunda 08:00
    MAKEDATETIME(DATE(DATEADD('day', 2, [Encerrado em])), MAKETIME(8,0,0))

ELSEIF DATEPART('hour', [Encerrado em]) < 8 THEN 
    // Madrugada -> Hoje 08:00
    MAKEDATETIME(DATE([Encerrado em]), MAKETIME(8,0,0))

ELSE 
    [Encerrado em]
END
```
8. Calcular `Segundos Úteis`:

```
// Campo: Segundos Úteis
// Lógica: Se mesmo dia, dif simples. Se dias diferentes, soma blocos de tempo.

IF DATETRUNC('day', [Data Contato Ajustada]) = DATETRUNC('day', [Encerrado em Ajustado]) THEN
    // Cenário Simples: Mesmo dia
    DATEDIFF('second', [Data Contato Ajustada], [Encerrado em Ajustado])

ELSE
    // Cenário Complexo: Dias diferentes
    (
        // 1. Dias inteiros no meio (excluindo Fim de Semana aprox.)
        (
            DATEDIFF('day', DATEADD('day', 1, DATETRUNC('day', [Data Contato Ajustada])), DATETRUNC('day', [Encerrado em Ajustado]))
            -
            (FLOOR(DATEDIFF('day', DATEADD('day', 1, DATETRUNC('day', [Data Contato Ajustada])), DATETRUNC('day', [Encerrado em Ajustado])) / 7) * 2)
        ) * 57600 
    )
    +
    // 2. Saldo do Primeiro Dia (Das X horas até as 24:00)
    DATEDIFF('second', 
        [Data Contato Ajustada], 
        MAKEDATETIME(DATE(DATEADD('day', 1, [Data Contato Ajustada])), MAKETIME(0,0,0)) 
    )
    +
    // 3. Saldo do Último Dia (Das 08:00 até Y horas)
    DATEDIFF('second', 
        MAKEDATETIME(DATE([Encerrado em Ajustado]), MAKETIME(8,0,0)), 
        [Encerrado em Ajustado]
    )
END
```
9. Calcular `SLA 5 Horas`:

```
IF [Segundos Úteis] <= 18000 THEN "Dentro do SLA" ELSE "Fora do SLA" END

```
10. Calcular `SLA 10 Horas`:

```
IF [Segundos Úteis] <= 36000 THEN "Dentro do SLA" ELSE "Fora do SLA" END

```
11. Calcular `SLA 15 Horas`:

```
IF [Segundos Úteis] <= 54000 THEN "Dentro do SLA" ELSE "Fora do SLA" END

```
12. Calcular `SLA 24 Horas`:

```
IF [Tempo Medio - Segundos] <= 86400 THEN "Dentro do SLA" ELSE "Fora do SLA" END
```
13. Renomear `Protocolo-1` → `Protocolo`
14. Calcular `SLA 4 Dias Uteis`:

```
// 1. Verifica se o campo de segundos está vazio (protocolo em aberto)
IF ISNULL([Segundos Úteis]) THEN
    "Em Andamento"

// 2. Se não estiver vazio, aplica a lógica de SLA
ELSEIF [Segundos Úteis] <= 230400 THEN
    "Dentro do SLA"
ELSE
    "Fora do SLA"
END
```
15. Calcular `Desconsiderar Tickets`:

```
IF STARTSWITH([Protocolo], "T-") THEN
	"Desconsiderar"
ELSE
	"Considerar"
END
```

→ [100] Canal: Whatsapp Enterprise - Natura CN; [101] Remoção em comum aos Emails; [102] CBCOM

## [98] Limpar 25 — Container

← [95] Ajuste Qtd Atendimento

1. Calcular `Validação Tickets`:

```
STARTSWITH([Protocolo], "T-")
```

→ [103] Ajuste no Status de Finalização

## [99] União de colunas 27 — SuperJoin

← [28] Remoção de colunas (Left); [96] Limpar 28 (Right)

**Join right**: esquerda = [28] Remoção de colunas, direita = [96] Limpar 28

Condição: `esq.[number] == dir.[CHAMADO]`

→ [104] Limpar 29

## [100] Canal: Whatsapp Enterprise - Natura CN — Container

_Descrição:_ Filtragem apenas do Canal "Whatsapp Enterprise - Natura CN" e remoção em "Setor Fim" de "Ativos" ou "Triagem".

← [97] Alterações Comuns MKT

1. Manter só `Canal de Entrada` em ['"Whatsapp Enterprise - Natura CN"']
2. Excluir `Setor Fim` em ['"ATIVOS"', '"Triagem"']

→ [105] SLA Primeiro Contato e Nivel

## [101] Remoção em comum aos Emails — Container

_Descrição:_ Remoção de 4 opções em "Status de Classificação", SLA Tempo Medio Operacional de 1 hora, Nivel

← [97] Alterações Comuns MKT

1. Filtro:

```
NOT ((([Status de Classificação] == "N2 - CB COM - Em acomp TD") AND NOT (ISNULL([Status de Classificação]))))
```
2. Excluir `Status de Classificação` em ['"N2 - E.mail - EM ACOMPANHAMENTO - TD"']
3. Filtro:

```
NOT ((([Status de Classificação] == "N2 - WhatsApp - EM ACOMPANHAMENTO - TD") AND NOT (ISNULL([Status de Classificação]))))
```
4. Filtro:

```
NOT ((([Status de Classificação] == "N3 - CB COM - Pendentes - JIRA") AND NOT (ISNULL([Status de Classificação]))))
```
5. Filtro:

```
NOT ((([Status de Classificação] == "N3 - WhatsAPP - Pendentes - JIRA") AND NOT (ISNULL([Status de Classificação]))))
```
6. Calcular `Tempo Operação em Segundos`:

```
INT(SPLIT([Tempo de Operação], ":", 1)) * 3600 +
INT(SPLIT([Tempo de Operação], ":", 2)) * 60 +
INT(SPLIT([Tempo de Operação], ":", 3))

```
7. Calcular `SLA Tempo Medio Operacional`:

```
IF ISNULL([Tempo Operação em Segundos]) THEN
    "Sem informação"
ELSEIF [Tempo Operação em Segundos] < 3600 THEN
    "Dentro do SLA"
ELSE
    "Fora do SLA"
END

```
8. Calcular `Nível`:

```
IF YEAR([Data Contato]) >= 2026 THEN
    // --- INÍCIO DA REGRA NOVA (2026 em diante) ---
    IF ISNULL([Status de finalização]) THEN "Não mapeado"

    // 1. CLASSIFICAÇÃO: N1
    ELSEIF UPPER(TRIM([Status de finalização])) == "ATUALIZAÇÃO DO APP" THEN "N1"
    ELSEIF UPPER(TRIM([Status de finalização])) == "ENCERRADO PELO EXPCB - ATUALIZAÇÃO DO APP/ NAVEGADOR" THEN "N1"
    ELSEIF UPPER(TRIM([Status de finalização])) == "EXCLUSÃO DE PEDIDO EM RASCUNHO" THEN "N1"
    ELSEIF UPPER(TRIM([Status de finalização])) == "LIMPEZA DE CACHE/ NAVEGAÇÃO EM GUIA ANÔNIMA/ TROCA DE NAVEGADOR" THEN "N1"
    ELSEIF UPPER(TRIM([Status de finalização])) == "ENCERRADO PELO EXPCB - LIMP. DE CACHE/ GUIA ANÔNIMA/ NAVEGADOR" THEN "N1"
    ELSEIF UPPER(TRIM([Status de finalização])) == "ORIENTADA PROCESSO|REGRA" THEN "N1"
    ELSEIF UPPER(TRIM([Status de finalização])) == "ENCERRADO PELO EXPCB - ORIENTADA PROCESSO | REGRA" THEN "N1"
    ELSEIF UPPER(TRIM([Status de finalização])) == "REENVIO DOS TERMOS" THEN "N1"
    ELSEIF UPPER(TRIM([Status de finalização])) == "REESTÍMULO NO AGREEMENTS" THEN "N1"
    ELSEIF UPPER(TRIM([Status de finalização])) == "REESTÍMULO NO SALESFORCE" THEN "N1"
    ELSEIF UPPER(TRIM([Status de finalização])) == "REPROCESSAMENTO DE CADASTRO" THEN "N1"
    ELSEIF UPPER(TRIM([Status de finalização])) == "ENCERRADO PELO EXPCB - REPROCESSAMENTO DE CADASTRO" THEN "N1"
    ELSEIF UPPER(TRIM([Status de finalização])) == "RESET DE SENHA" THEN "N1"

    // 2. CLASSIFICAÇÃO: N2
    ELSEIF UPPER(TRIM([Status de finalização])) == "CHAMADO" THEN "N2"
    ELSEIF UPPER(TRIM([Status de finalização])) == "INCIDENTE CRÍTICO" THEN "N2"
    ELSEIF UPPER(TRIM([Status de finalização])) == "REABERTURA DE CHAMADO" THEN "N2"

    // 3. CLASSIFICAÇÃO: NEUTRO
    ELSEIF UPPER(TRIM([Status de finalização])) == "AGUARD. RETORNO FV" THEN "NEUTRO"
    ELSEIF UPPER(TRIM([Status de finalização])) == "CONTATO SEM INTERAÇÃO" THEN "NEUTRO"
    ELSEIF UPPER(TRIM([Status de finalização])) == "CONTATO SEM SUCESSO" THEN "NEUTRO"
    ELSEIF UPPER(TRIM([Status de finalização])) == "DIRECIONADO PARA O ATENDIMENTO" THEN "NEUTRO"
    ELSEIF UPPER(TRIM([Status de finalização])) == "DIRECIONADO PARA O SERVICE DESK" THEN "NEUTRO"
    ELSEIF UPPER(TRIM([Status de finalização])) == "DIRECIONADO PARA O TRANSPORTE" THEN "NEUTRO"
    ELSEIF UPPER(TRIM([Status de finalização])) == "DIRECIONADO PARA TERCEIROS" THEN "NEUTRO"
    ELSEIF UPPER(TRIM([Status de finalização])) == "FOLLOWUP" THEN "NEUTRO"
    ELSEIF UPPER(TRIM([Status de finalização])) == "INCIDENTE CRÍTICO - EM ANDAMENTO" THEN "NEUTRO"
    ELSEIF UPPER(TRIM([Status de finalização])) == "INCIDENTE CRÍTICO RESOLVIDO" THEN "NEUTRO"
    ELSEIF UPPER(TRIM([Status de finalização])) == "INCIDENTE EM ANDAMENTO" THEN "NEUTRO"
    ELSEIF UPPER(TRIM([Status de finalização])) == "INCIDENTE RESOLVIDO" THEN "NEUTRO"
    ELSEIF UPPER(TRIM([Status de finalização])) == "JÁ ESTAVA RESOLVIDO" THEN "NEUTRO"
    ELSEIF UPPER(TRIM([Status de finalização])) == "RESOLVIDO E-MAIL N3" THEN "NEUTRO"
    ELSEIF UPPER(TRIM([Status de finalização])) == "RESOLVIDO MKT N3" THEN "NEUTRO"
    ELSEIF UPPER(TRIM([Status de finalização])) == "RESOLVIDO N2 E-MAIL" THEN "NEUTRO"
    ELSEIF UPPER(TRIM([Status de finalização])) == "RESOLVIDO N2 MKT" THEN "NEUTRO"
    ELSEIF UPPER(TRIM([Status de finalização])) == "RESOLVIDO SEM ATUAÇÃO DO EXP" THEN "NEUTRO"

    // 4. CLASSIFICAÇÃO: NÃO CONSIDERAR
    ELSEIF UPPER(TRIM([Status de finalização])) == "AÇÕES EM MASSA" THEN "NÃO CONSIDERAR"
    ELSEIF UPPER(TRIM([Status de finalização])) == "AGRADECIMENTOS" THEN "NÃO CONSIDERAR"
    ELSEIF UPPER(TRIM([Status de finalização])) == "CARD EM BRANCO" THEN "NÃO CONSIDERAR"
    ELSEIF UPPER(TRIM([Status de finalização])) == "EXPCN" THEN "NÃO CONSIDERAR"
    ELSEIF UPPER(TRIM([Status de finalização])) == "FINALIZADO FORA DO HORÁRIO" THEN "NÃO CONSIDERAR"
    ELSEIF UPPER(TRIM([Status de finalização])) == "FINALIZADO PELO BOT DURAÇÃO 1 HORA" THEN "NÃO CONSIDERAR"
    ELSEIF UPPER(TRIM([Status de finalização])) == "HEALTH CHECK" THEN "NÃO CONSIDERAR"
    ELSEIF UPPER(TRIM([Status de finalização])) == "TESTE" THEN "NÃO CONSIDERAR"

    // Retorno para novos status que ainda não estão mapeados
    ELSE "Não mapeado"
    END

ELSE
    // --- INÍCIO DA REGRA ANTIGA (Antes de 2026) ---
    IF UPPER([Status de finalização]) == "CHAMADO" THEN "N2" 
    ELSEIF UPPER([Status de finalização]) == "INCIDENTE CRÍTICO" THEN "N2"
    ELSEIF UPPER([Status de finalização]) == "INCIDENTE EM ANDAMENTO" THEN "NEUTRO"
    ELSEIF UPPER([Status de finalização]) == "INCIDENTE RESOLVIDO" THEN "NEUTRO"
    ELSE "N1" 
    END
END
```
9. Excluir `Status de Classificação` em ['"N3 - E.mail - Pendentes - JIRA"']

→ [106] Canal Email EXP CB, SLA: Tempo Médio Operacional,; [107] Filtro Setor Fim

## [102] CBCOM — Container

_Descrição:_ Setor Fim = CBCOM

← [97] Alterações Comuns MKT

1. Manter só `Setor Fim` em ['"CB Commerce"']

→ [108] SLA Primeiro Contato  e Nível

## [103] Ajuste no Status de Finalização — Container

_Descrição:_ os registros de 16 e 17/03 não listados estão com a coluna Status sem preenchimento. Esse ajuste corrige esse ponto.

← [98] Limpar 25

1. Calcular `Status2`:

```
IF (DATE([Data criação]) = #2026-03-16# OR DATE([Data criação]) = #2026-03-17#)
OR (DATE([Data conclusão]) = #2026-03-16# OR DATE([Data conclusão]) = #2026-03-17#)
THEN 
    // --- INÍCIO DA VALIDAÇÃO DO "SIM" (Dias 16 ou 17) ---
    IF ISNULL([Status]) OR [Status] = "" THEN
        [Status de finalização]
    ELSE
        [Status]
    END

ELSE 
    // --- O QUE ACONTECE NOS OUTROS DIAS ("Não") ---
    [Status]
END
```
2. Renomear `Status` → `Status3`
3. Renomear `Status2` → `Status`
4. Remover colunas: `Status de finalização`
5. Remover colunas: `Status3`

→ [109] Remoção de Status  Neutros

## [104] Limpar 29 — Container

← [99] União de colunas 27

1. Renomear `u_jira` → `Jira Incidente`
2. Renomear `u_external_ticket` → `Ticket Externo Incidente`
3. Renomear `hold_reason` → `Motivo Em Espera Incidente`
4. Renomear `Motivo Em Espera Incidente` → `Motivo Em Espera Incidente`
5. Renomear `state` → `Estado Incidente`
6. Remover colunas: `number`

→ [110] MKT Brasil Backlog

## [105] SLA Primeiro Contato e Nivel — Container

_Descrição:_ Criação de SLA do Primeiro Contato e Nível (N1 e N2)

← [100] Canal: Whatsapp Enterprise - Natura CN

1. Calcular `Primeiro Tempo de Espera - Segundos`:

```
(INT(SPLIT([Primeiro Tempo de Espera], ":", 1)) * 3600) +
(INT(SPLIT([Primeiro Tempo de Espera], ":", 2)) * 60) +
INT(SPLIT([Primeiro Tempo de Espera], ":", 3))

```
2. Calcular `SLA do Primeiro Contato`:

```
IF [Expurgo] = "Sim" THEN
	"Dentro do SLA"
ELSEIF [Origem] = "AppSheets" THEN
	NULL
ELSEIF [Primeiro Tempo de Espera - Segundos] <= 359 THEN 	"Dentro do SLA"
ELSE 
	"Fora do SLA"
END
```
3. Calcular `Nível`:

```
IF YEAR([Data Contato]) >= 2026 THEN
    // --- INÍCIO DA REGRA NOVA (2026 em diante) ---
    IF ISNULL([Status de finalização]) THEN "Não mapeado"

    // 1. CLASSIFICAÇÃO: N1
    ELSEIF UPPER(TRIM([Status de finalização])) == "ATUALIZAÇÃO DO APP" THEN "N1"
    ELSEIF UPPER(TRIM([Status de finalização])) == "EXCLUSÃO DE PEDIDO EM RASCUNHO" THEN "N1"
    ELSEIF UPPER(TRIM([Status de finalização])) == "LIMPEZA DE CACHE/ NAVEGAÇÃO EM GUIA ANÔNIMA/ TROCA DE NAVEGADOR" THEN "N1"
    ELSEIF UPPER(TRIM([Status de finalização])) == "ORIENTADA PROCESSO|REGRA" THEN "N1"
    ELSEIF UPPER(TRIM([Status de finalização])) == "REENVIO DOS TERMOS" THEN "N1"
    ELSEIF UPPER(TRIM([Status de finalização])) == "REESTÍMULO NO AGREEMENTS" THEN "N1"
    ELSEIF UPPER(TRIM([Status de finalização])) == "REESTÍMULO NO SALESFORCE" THEN "N1"
    ELSEIF UPPER(TRIM([Status de finalização])) == "REPROCESSAMENTO DE CADASTRO" THEN "N1"
    ELSEIF UPPER(TRIM([Status de finalização])) == "RESET DE SENHA" THEN "N1"

    // 2. CLASSIFICAÇÃO: N2
    ELSEIF UPPER(TRIM([Status de finalização])) == "CHAMADO" THEN "N2"
    ELSEIF UPPER(TRIM([Status de finalização])) == "INCIDENTE CRÍTICO" THEN "N2"
    ELSEIF UPPER(TRIM([Status de finalização])) == "REABERTURA DE CHAMADO" THEN "N2"

    // 3. CLASSIFICAÇÃO: NEUTRO (Não considerado em Retenção)
    ELSEIF UPPER(TRIM([Status de finalização])) == "AGUARD. RETORNO FV" THEN "NEUTRO"
    ELSEIF UPPER(TRIM([Status de finalização])) == "CONTATO SEM INTERAÇÃO" THEN "NEUTRO"
    ELSEIF UPPER(TRIM([Status de finalização])) == "CONTATO SEM SUCESSO" THEN "NEUTRO"
    ELSEIF UPPER(TRIM([Status de finalização])) == "DIRECIONADO PARA O ATENDIMENTO" THEN "NEUTRO"
    ELSEIF UPPER(TRIM([Status de finalização])) == "DIRECIONADO PARA O SERVICE DESK" THEN "NEUTRO"
    ELSEIF UPPER(TRIM([Status de finalização])) == "DIRECIONADO PARA O TRANSPORTE" THEN "NEUTRO"
    ELSEIF UPPER(TRIM([Status de finalização])) == "DIRECIONADO PARA TERCEIROS" THEN "NEUTRO"
    ELSEIF UPPER(TRIM([Status de finalização])) == "FOLLOWUP" THEN "NEUTRO"
    ELSEIF UPPER(TRIM([Status de finalização])) == "INCIDENTE CRÍTICO - EM ANDAMENTO" THEN "NEUTRO"
    ELSEIF UPPER(TRIM([Status de finalização])) == "INCIDENTE CRÍTICO RESOLVIDO" THEN "NEUTRO"
    ELSEIF UPPER(TRIM([Status de finalização])) == "INCIDENTE EM ANDAMENTO" THEN "NEUTRO"
    ELSEIF UPPER(TRIM([Status de finalização])) == "INCIDENTE RESOLVIDO" THEN "NEUTRO"
    ELSEIF UPPER(TRIM([Status de finalização])) == "JÁ ESTAVA RESOLVIDO" THEN "NEUTRO"
    ELSEIF UPPER(TRIM([Status de finalização])) == "RESOLVIDO E-MAIL N3" THEN "NEUTRO"
    ELSEIF UPPER(TRIM([Status de finalização])) == "RESOLVIDO MKT N3" THEN "NEUTRO"
    ELSEIF UPPER(TRIM([Status de finalização])) == "RESOLVIDO N2 E-MAIL" THEN "NEUTRO"
    ELSEIF UPPER(TRIM([Status de finalização])) == "RESOLVIDO N2 MKT" THEN "NEUTRO"
    ELSEIF UPPER(TRIM([Status de finalização])) == "RESOLVIDO SEM ATUAÇÃO DO EXP" THEN "NEUTRO"

    // 4. CLASSIFICAÇÃO: NÃO CONSIDERAR (Desconsiderado)
    ELSEIF UPPER(TRIM([Status de finalização])) == "AÇÕES EM MASSA" THEN "NÃO CONSIDERAR"
    ELSEIF UPPER(TRIM([Status de finalização])) == "AGRADECIMENTOS" THEN "NÃO CONSIDERAR"
    ELSEIF UPPER(TRIM([Status de finalização])) == "CARD EM BRANCO" THEN "NÃO CONSIDERAR"
    ELSEIF UPPER(TRIM([Status de finalização])) == "EXPCN" THEN "NÃO CONSIDERAR"
    ELSEIF UPPER(TRIM([Status de finalização])) == "FINALIZADO FORA DO HORÁRIO" THEN "NÃO CONSIDERAR"
    ELSEIF UPPER(TRIM([Status de finalização])) == "FINALIZADO PELO BOT DURAÇÃO 1 HORA" THEN "NÃO CONSIDERAR"
    ELSEIF UPPER(TRIM([Status de finalização])) == "HEALTH CHECK" THEN "NÃO CONSIDERAR"
    ELSEIF UPPER(TRIM([Status de finalização])) == "TESTE" THEN "NÃO CONSIDERAR"

    // Retorno para novos status que ainda não estão mapeados
    ELSE "Não mapeado"
    END

ELSE
    // --- INÍCIO DA REGRA ANTIGA (Antes de 2026) ---
    IF UPPER([Status de finalização]) == "CHAMADO" THEN "N2" 
    ELSEIF UPPER([Status de finalização]) == "INCIDENTE CRÍTICO" THEN "N2"
    ELSEIF UPPER([Status de finalização]) == "INCIDENTE EM ANDAMENTO" THEN "NEUTRO"
    ELSEIF UPPER([Status de finalização]) == "INCIDENTE RESOLVIDO" THEN "NEUTRO"
    ELSE "N1" 
    END
END
```

→ [111] Whats GN; [112] Whats GV Antecipada; [113] União MKT + RE (AppSheet); [114] Limpar 13

## [106] Canal Email EXP CB, SLA: Tempo Médio Operacional, — Container

_Descrição:_ Canal Email Experiencia CB

← [101] Remoção em comum aos Emails

1. Manter só `Canal de Entrada` em ['"E-mail - Experiência CB"']

→ [115] Remoção de Colunas Não utilizadas; [116] Limpar 21

## [107] Filtro Setor Fim — Container

← [101] Remoção em comum aos Emails

1. Manter só `Setor Fim` em ['"APP AVON CF"', '"APP NATURA"', '"NATURA EXPCB"', '"NATURA EXPCN"']

→ [117] Emails de Loja

## [108] SLA Primeiro Contato  e Nível — Container

_Descrição:_ Criação de SLA do Primeiro Contato e Nível (N1 e N2)

← [102] CBCOM

1. Calcular `Primeiro Tempo de Espera - Segundos`:

```
(INT(SPLIT([Primeiro Tempo de Espera], ":", 1)) * 3600) +
(INT(SPLIT([Primeiro Tempo de Espera], ":", 2)) * 60) +
INT(SPLIT([Primeiro Tempo de Espera], ":", 3))
```
2. Calcular `SLA do Primeiro Contato`:

```
IF [Expurgo] = "Sim" THEN
	"Dentro do SLA"
ELSEIF [Origem] = "AppSheets" THEN
	NULL
ELSEIF [Primeiro Tempo de Espera - Segundos] <= 359 THEN 	"Dentro do SLA"
ELSE 
	"Fora do SLA"
END
```
3. Calcular `Nível`:

```
IF YEAR([Data Contato]) >= 2026 THEN
    // --- INÍCIO DA REGRA NOVA (2026 em diante) ---
    IF ISNULL([Status de finalização]) THEN "Não mapeado"

    // 1. CLASSIFICAÇÃO: N1
    ELSEIF UPPER(TRIM([Status de finalização])) == "ATUALIZAÇÃO DO APP" THEN "N1"
    ELSEIF UPPER(TRIM([Status de finalização])) == "EXCLUSÃO DE PEDIDO EM RASCUNHO" THEN "N1"
    ELSEIF UPPER(TRIM([Status de finalização])) == "LIMPEZA DE CACHE/ NAVEGAÇÃO EM GUIA ANÔNIMA/ TROCA DE NAVEGADOR" THEN "N1"
    ELSEIF UPPER(TRIM([Status de finalização])) == "ORIENTADA PROCESSO|REGRA" THEN "N1"
    ELSEIF UPPER(TRIM([Status de finalização])) == "REENVIO DOS TERMOS" THEN "N1"
    ELSEIF UPPER(TRIM([Status de finalização])) == "REESTÍMULO NO AGREEMENTS" THEN "N1"
    ELSEIF UPPER(TRIM([Status de finalização])) == "REESTÍMULO NO SALESFORCE" THEN "N1"
    ELSEIF UPPER(TRIM([Status de finalização])) == "REPROCESSAMENTO DE CADASTRO" THEN "N1"
    ELSEIF UPPER(TRIM([Status de finalização])) == "RESET DE SENHA" THEN "N1"

    // 2. CLASSIFICAÇÃO: N2
    ELSEIF UPPER(TRIM([Status de finalização])) == "CHAMADO" THEN "N2"
    ELSEIF UPPER(TRIM([Status de finalização])) == "INCIDENTE CRÍTICO" THEN "N2"
    ELSEIF UPPER(TRIM([Status de finalização])) == "REABERTURA DE CHAMADO" THEN "N2"

    // 3. CLASSIFICAÇÃO: NEUTRO (Não considerado em Retenção)
    ELSEIF UPPER(TRIM([Status de finalização])) == "AGUARD. RETORNO FV" THEN "NEUTRO"
    ELSEIF UPPER(TRIM([Status de finalização])) == "CONTATO SEM INTERAÇÃO" THEN "NEUTRO"
    ELSEIF UPPER(TRIM([Status de finalização])) == "CONTATO SEM SUCESSO" THEN "NEUTRO"
    ELSEIF UPPER(TRIM([Status de finalização])) == "DIRECIONADO PARA O ATENDIMENTO" THEN "NEUTRO"
    ELSEIF UPPER(TRIM([Status de finalização])) == "DIRECIONADO PARA O SERVICE DESK" THEN "NEUTRO"
    ELSEIF UPPER(TRIM([Status de finalização])) == "DIRECIONADO PARA O TRANSPORTE" THEN "NEUTRO"
    ELSEIF UPPER(TRIM([Status de finalização])) == "DIRECIONADO PARA TERCEIROS" THEN "NEUTRO"
    ELSEIF UPPER(TRIM([Status de finalização])) == "FOLLOWUP" THEN "NEUTRO"
    ELSEIF UPPER(TRIM([Status de finalização])) == "INCIDENTE CRÍTICO - EM ANDAMENTO" THEN "NEUTRO"
    ELSEIF UPPER(TRIM([Status de finalização])) == "INCIDENTE CRÍTICO RESOLVIDO" THEN "NEUTRO"
    ELSEIF UPPER(TRIM([Status de finalização])) == "INCIDENTE EM ANDAMENTO" THEN "NEUTRO"
    ELSEIF UPPER(TRIM([Status de finalização])) == "INCIDENTE RESOLVIDO" THEN "NEUTRO"
    ELSEIF UPPER(TRIM([Status de finalização])) == "JÁ ESTAVA RESOLVIDO" THEN "NEUTRO"
    ELSEIF UPPER(TRIM([Status de finalização])) == "RESOLVIDO E-MAIL N3" THEN "NEUTRO"
    ELSEIF UPPER(TRIM([Status de finalização])) == "RESOLVIDO MKT N3" THEN "NEUTRO"
    ELSEIF UPPER(TRIM([Status de finalização])) == "RESOLVIDO N2 E-MAIL" THEN "NEUTRO"
    ELSEIF UPPER(TRIM([Status de finalização])) == "RESOLVIDO N2 MKT" THEN "NEUTRO"
    ELSEIF UPPER(TRIM([Status de finalização])) == "RESOLVIDO SEM ATUAÇÃO DO EXP" THEN "NEUTRO"

    // 4. CLASSIFICAÇÃO: NÃO CONSIDERAR (Desconsiderado)
    ELSEIF UPPER(TRIM([Status de finalização])) == "AÇÕES EM MASSA" THEN "NÃO CONSIDERAR"
    ELSEIF UPPER(TRIM([Status de finalização])) == "AGRADECIMENTOS" THEN "NÃO CONSIDERAR"
    ELSEIF UPPER(TRIM([Status de finalização])) == "CARD EM BRANCO" THEN "NÃO CONSIDERAR"
    ELSEIF UPPER(TRIM([Status de finalização])) == "EXPCN" THEN "NÃO CONSIDERAR"
    ELSEIF UPPER(TRIM([Status de finalização])) == "FINALIZADO FORA DO HORÁRIO" THEN "NÃO CONSIDERAR"
    ELSEIF UPPER(TRIM([Status de finalização])) == "FINALIZADO PELO BOT DURAÇÃO 1 HORA" THEN "NÃO CONSIDERAR"
    ELSEIF UPPER(TRIM([Status de finalização])) == "HEALTH CHECK" THEN "NÃO CONSIDERAR"
    ELSEIF UPPER(TRIM([Status de finalização])) == "TESTE" THEN "NÃO CONSIDERAR"

    // Retorno para novos status que ainda não estão mapeados
    ELSE "Não mapeado"
    END

ELSE
    // --- INÍCIO DA REGRA ANTIGA (Antes de 2026) ---
    IF UPPER([Status de finalização]) == "CHAMADO" THEN "N2" 
    ELSEIF UPPER([Status de finalização]) == "INCIDENTE CRÍTICO" THEN "N2"
    ELSEIF UPPER([Status de finalização]) == "INCIDENTE EM ANDAMENTO" THEN "NEUTRO"
    ELSEIF UPPER([Status de finalização]) == "INCIDENTE RESOLVIDO" THEN "NEUTRO"
    ELSE "N1" 
    END
END
```

→ [118] Tempo Medio - Segundos

## [109] Remoção de Status  Neutros — Container

← [103] Ajuste no Status de Finalização

1. Filtro:

```
NOT ((([Status] == "AÇÕES EM MASSA" OR [Status] == "AGRADECIMENTOS" OR [Status] == "EXPCN") AND NOT (ISNULL([Status]))))
```
2. Filtro:

```
NOT ((([Status] == "HEALTH CHECK" OR [Status] == "N2 - E.mail - EM ACOMPANHAMENTO - TD" OR [Status] == "TESTE") AND NOT (ISNULL([Status]))))
```

→ [119] Remoção de SF

## [110] MKT Brasil Backlog — PublishExtract

← [104] Limpar 29

**Saída:** `4. DATASOURCES/MKT Brasil Backlog`

## [111] Whats GN — Container

_Descrição:_ Setor Fim = Whats GN. SLAs 5h, 10h, 15h e 24h

← [105] SLA Primeiro Contato e Nivel

1. Calcular `Tempo Atendimento WhatsApp`:

```
DATEDIFF('second', [Data Contato], [Encerrado em])

```
2. Mudar tipo: `Tempo Atendimento WhatsApp` → real
3. Calcular `Tempo Formatado WhatsApp`:

```
RIGHT('0' + STR(INT([Tempo Atendimento WhatsApp] / 3600)), 2) +
':' +
RIGHT('0' + STR(INT(([Tempo Atendimento WhatsApp] % 3600) / 60)), 2) +
':' +
RIGHT('0' + STR([Tempo Atendimento WhatsApp] % 60), 2)

```
4. Manter só `Setor Fim` em ['"Whats GN"']
5. Remover colunas: `testeLis`

→ [120] MKT Whats GN; [121] Remoção de Colunas Não utilizadas

## [112] Whats GV Antecipada — Container

_Descrição:_ Setor Fim = Whats GV Antecipada

← [105] SLA Primeiro Contato e Nivel

1. Manter só `Setor Fim` em ['"Atend. -  GV Antecipada"', '"TD -  GV Antecipada"']
2. Calcular `Tipo Setor`:

```
IF [Setor Fim] = "Atend. -  GV Antecipada" THEN "Atendimento" ELSEIF [Setor Fim] = "TD -  GV Antecipada" THEN "TD" END
```
3. Manter só `Setor Fim` em ['"TD -  GV Antecipada"']

→ [122] Whtas GV Antecipada; [123] Remoção de Colunas Não utilizadas

## [113] União MKT + RE (AppSheet) — SuperUnion

← [58] Data Corte a Partir 01/10/25; [56] Data Corte Ate 30/09/25; [105] SLA Primeiro Contato e Nivel

**Union** das entradas acima (colunas com o mesmo nome se juntam; cria `Table Names`).

1. Remover colunas: `Table Names`

→ [124] Whats GV

## [114] Limpar 13 — Container

← [105] SLA Primeiro Contato e Nivel

1. Manter só `Setor Fim` em ['"Whats Franquia"']
2. Calcular `Tempo Atendimento WhatsApp`:

```
DATEDIFF('second', [Data Contato], [Encerrado em])
```
3. Calcular `Tempo Formatado WhatsApp`:

```
RIGHT('0' + STR(INT([Tempo Atendimento WhatsApp] / 3600)), 2) +
':' +
RIGHT('0' + STR(INT(([Tempo Atendimento WhatsApp] % 3600) / 60)), 2) +
':' +
RIGHT('0' + STR([Tempo Atendimento WhatsApp] % 60), 2)
```

→ [125] União de linhas 15

## [115] Remoção de Colunas Não utilizadas — Container

← [106] Canal Email EXP CB, SLA: Tempo Médio Operacional,

1. Remover colunas: `Tempo Medio - Segundos`, `Tempo Operação em Segundos`, `Empresa`, `Nome`, `CPF/CNPJ`, `Número do Contrato`
2. Remover colunas: `Valor do Contrato`, `CODIGO`, `GV`, `FUNÇÃO`
3. Remover colunas: `testeLis`, `Ciclo - Health Check`, `Recebidos - Health Check`, `E-mail`
4. Remover colunas: `Responsável`, `Tempo até ser atendido`, `Tempo do atendimento`, `Primeiro Tempo de Espera`, `Tempo Médio de Espera`
5. Remover colunas: `Setor Entrada`
6. Remover colunas: `Qtde Mensagens`, `Observações`, `Campos adicionais Web Chat`
7. Remover colunas: `SLA 24 Horas`
8. Remover colunas: `Fone Cliente`
9. Calcular `Setor`:

```
IF ISNULL([Protocolo]) THEN NULL ELSE "Experiência CB" END
```
10. Remover colunas: `CHAMADO`
11. Remover colunas: `Fornecedor`

→ [136] União de linhas 4

## [116] Limpar 21 — Container

← [106] Canal Email EXP CB, SLA: Tempo Médio Operacional,

1. Calcular `Nivel Considerar`:

```
IF [Nível]="NEUTRO" THEN "Desconsiderar" ELSE "Considerar" END
```

→ [126] MKT Email Experiencia CB

## [117] Emails de Loja — Container

_Descrição:_ Canal de Entrada: Email App Natura, Email App Avon CF, Emalil Natura EXPCN, SLA Tempo Medio Operacional de 24 Horas

← [107] Filtro Setor Fim

1. Remover colunas: `SLA Tempo Medio Operacional`
2. Calcular `SLA Tempo Medio Operacional`:

```
IF ISNULL([Tempo Operação em Segundos]) THEN "Sem informação"
ELSEIF [Tempo Operação em Segundos] <= 86400 THEN "Dentro do SLA"
ELSE "Fora do SLA"
END
```
3. Calcular `Setor`:

```
IF [Setor Fim]= "APP AVON CF" THEN "APP AVON CF" 
ELSEIF [Setor Fim] = "APP NATURA" THEN "APP NATURA"
ELSEIF [Setor Fim]="NATURA EXPCN" THEN "NATURA EXPCB"
ELSEIF [Setor Fim]="NATURA EXPCB" THEN "NATURA EXPCB"
END
```
4. Excluir `Status de finalização` em ['"Card Em Branco"']
5. Calcular `Status SLA Email`:

```
IF NOT ISNULL([Encerrado em]) THEN
    // --- CENÁRIO 1: CHAMADO FECHADO ---
    // Simplesmente checa se gastou menos de 16h úteis (57.600 seg)
    IF [Segundos Úteis] <= 57600 THEN "Dentro do SLA" ELSE "Fora do SLA" END

ELSE
    // --- CENÁRIO 2: CHAMADO ABERTO ---
    // Como não tem "Segundos totais" ainda, verificamos o calendário.
    // Se "AGORA" for antes de "Data Ajustada + 1 dia útil", está no prazo.
    
    IF NOW() <= 
        (CASE DATEPART('weekday', [Data Contato Ajustada])
            WHEN 6 THEN DATEADD('day', 3, [Data Contato Ajustada]) // Sexta -> Segunda
            WHEN 7 THEN DATEADD('day', 2, [Data Contato Ajustada]) // Sábado -> Segunda
            ELSE DATEADD('day', 1, [Data Contato Ajustada])        // Outros -> Dia Seguinte
        END)
    THEN "Dentro do SLA" 
    ELSE "Fora do SLA" 
    END
END
```

→ [127] MKT Emails de Lojas; [128] Remoção de Colunas Não utilizadas

## [118] Tempo Medio - Segundos — Container

← [108] SLA Primeiro Contato  e Nível

1. Calcular `Tempo Medio - Segundos`:

```
DATEDIFF('second', [Data Contato], [Encerrado em])
```

→ [129] MKT CBCOM; [130] Remoção de Colunas Não utilizadas

## [119] Remoção de SF — Container

← [109] Remoção de Status  Neutros

1. Filtro:

```
NOT ((([Status] == "FINALIZADO FORA DO HORÁRIO") AND NOT (ISNULL([Status]))))
```
2. Excluir `Status` em ['"PROTOCOLO"']

→ [131] Tratar Responsavel

## [120] MKT Whats GN — PublishExtract

← [111] Whats GN

**Saída:** `4. DATASOURCES/MKT Whats GN`

## [121] Remoção de Colunas Não utilizadas — Container

_Descrição:_ Adição da coluna Setor

← [111] Whats GN

1. Remover colunas: `Tempo Atendimento WhatsApp`, `Tempo Formatado WhatsApp`, `Responsável`, `Tempo até ser atendido`, `Tempo do atendimento`, `Primeiro Tempo de Espera`, `Tempo Médio de Espera`, `Fone Cliente`, `Setor Entrada`, `Qtde Mensagens`
2. Remover colunas: `SLA 24 Horas`, `Observações`, `Campos adicionais Web Chat`
3. Calcular `Setor`:

```
IF ISNULL([Protocolo]) THEN NULL ELSE "WHATS GN" END
```
4. Remover colunas: `Primeiro Tempo de Espera - Segundos`
5. Remover colunas: `Empresa`
6. Remover colunas: `Nome`
7. Remover colunas: `CPF/CNPJ`
8. Remover colunas: `Número do Contrato`
9. Remover colunas: `Valor do Contrato`
10. Remover colunas: `CODIGO`
11. Remover colunas: `GV`
12. Remover colunas: `FUNÇÃO`
13. Remover colunas: `CHAMADO`
14. Remover colunas: `Fornecedor`
15. Remover colunas: `Ciclo - Health Check`
16. Remover colunas: `Recebidos - Health Check`
17. Remover colunas: `E-mail`
18. Remover colunas: `Tempo Medio - Segundos`

→ [138] União CBCOM e WHATS GN

## [122] Whtas GV Antecipada — PublishExtract

← [112] Whats GV Antecipada

**Saída:** `4. DATASOURCES/MKT Whats GV Antecipada`

## [123] Remoção de Colunas Não utilizadas — Container

_Descrição:_ Adição da coluna Setor

← [112] Whats GV Antecipada

1. Remover colunas: `Tempo Medio - Segundos`, `Primeiro Tempo de Espera - Segundos`, `Empresa`, `Nome`, `CPF/CNPJ`, `Número do Contrato`, `Valor do Contrato`, `CODIGO`
2. Remover colunas: `CHAMADO`, `Fornecedor`, `testeLis`
3. Remover colunas: `Ciclo - Health Check`, `Recebidos - Health Check`, `E-mail`
4. Remover colunas: `Responsável`, `Tempo até ser atendido`, `Tempo do atendimento`, `Primeiro Tempo de Espera`
5. Remover colunas: `Tempo Médio de Espera`, `Fone Cliente`
6. Remover colunas: `Setor Entrada`
7. Remover colunas: `Qtde Mensagens`, `Observações`, `Campos adicionais Web Chat`
8. Remover colunas: `SLA 24 Horas`
9. Calcular `Setor`:

```
IF ISNULL([Protocolo]) THEN NULL ELSE "WHATS GV ANTECIPADA" END
```
10. Remover colunas: `GV`
11. Remover colunas: `FUNÇÃO`
12. Remover colunas: `Tipo Setor`

→ [147] União Whats GV Antecipada

## [124] Whats GV — Container

_Descrição:_ Setor Fim = Whats GV, Tempo Medio - Segundos

← [113] União MKT + RE (AppSheet)

1. Filtro:

```
([Setor Fim] == "Whats GV" OR [Setor Fim]=="RE")
```
2. Calcular `Tempo Atendimento WhatsApp`:

```
DATEDIFF('second', [Data Contato], [Encerrado em])
```
3. Calcular `Tempo Formatado WhatsApp`:

```
RIGHT('0' + STR(INT([Tempo Atendimento WhatsApp] / 3600)), 2) +
':' +
RIGHT('0' + STR(INT(([Tempo Atendimento WhatsApp] % 3600) / 60)), 2) +
':' +
RIGHT('0' + STR([Tempo Atendimento WhatsApp] % 60), 2)
```

→ [132] Whats GV; [133] Remoção de Colunas Não utilizadas

## [125] União de linhas 15 — SuperUnion

← [114] Limpar 13; [57] Data Corte Franquias

**Union** das entradas acima (colunas com o mesmo nome se juntam; cria `Table Names`).

→ [134] MKT Whats Franquia; [135] Remoção de Colunas Não utilizadas

## [126] MKT Email Experiencia CB — PublishExtract

← [116] Limpar 21

**Saída:** `4. DATASOURCES/MKT Email Experiencia CB`

## [127] MKT Emails de Lojas — PublishExtract

← [117] Emails de Loja

**Saída:** `4. DATASOURCES/MKT Emails de Lojas`

## [128] Remoção de Colunas Não utilizadas — Container

← [117] Emails de Loja

1. Remover colunas: `Tempo Medio - Segundos`, `Tempo Operação em Segundos`
2. Remover colunas: `Empresa`, `Nome`, `CPF/CNPJ`
3. Remover colunas: `Número do Contrato`, `Valor do Contrato`, `CODIGO`, `GV`
4. Remover colunas: `Fornecedor`, `testeLis`
5. Remover colunas: `Ciclo - Health Check`, `Recebidos - Health Check`, `E-mail`
6. Remover colunas: `Responsável`, `Tempo até ser atendido`, `Tempo do atendimento`, `Primeiro Tempo de Espera`, `Tempo Médio de Espera`
7. Remover colunas: `Fone Cliente`, `Setor Entrada`
8. Remover colunas: `Qtde Mensagens`
9. Remover colunas: `Observações`, `Campos adicionais Web Chat`
10. Remover colunas: `SLA 24 Horas`
11. Remover colunas: `FUNÇÃO`
12. Remover colunas: `CHAMADO`

→ [136] União de linhas 4

## [129] MKT CBCOM — PublishExtract

← [118] Tempo Medio - Segundos

**Saída:** `4. DATASOURCES/MKT - CBCOM`

## [130] Remoção de Colunas Não utilizadas — Container

_Descrição:_ Adição da coluna Setor

← [118] Tempo Medio - Segundos

1. Remover colunas: `Tempo Medio - Segundos`
2. Remover colunas: `Primeiro Tempo de Espera - Segundos`
3. Remover colunas: `Empresa`
4. Remover colunas: `testeLis`, `Ciclo - Health Check`
5. Remover colunas: `Recebidos - Health Check`, `E-mail`, `Responsável`, `Tempo até ser atendido`, `Tempo do atendimento`, `Primeiro Tempo de Espera`, `Tempo Médio de Espera`
6. Remover colunas: `Fone Cliente`, `Setor Entrada`, `Qtde Mensagens`, `Observações`, `Campos adicionais Web Chat`
7. Remover colunas: `SLA 24 Horas`
8. Calcular `Setor`:

```
IF ISNULL([Protocolo]) THEN NULL ELSE "CBCOM" END
```
9. Remover colunas: `Número do Contrato`
10. Remover colunas: `Valor do Contrato`
11. Remover colunas: `CODIGO`
12. Remover colunas: `GV`
13. Remover colunas: `FUNÇÃO`
14. Remover colunas: `CHAMADO`
15. Remover colunas: `Fornecedor`
16. Remover colunas: `Nome`
17. Remover colunas: `CPF/CNPJ`

→ [138] União CBCOM e WHATS GN

## [131] Tratar Responsavel — Container

← [119] Remoção de SF

1. Renomear `Responsável` → `Responsável1`
2. Calcular `Responsável`:

```
IF ISNULL([Responsável1]) THEN [Operador]
ELSE [Responsável1]
END
```
3. Remover colunas: `Responsável1`

→ [137] Responsavel

## [132] Whats GV — PublishExtract

← [124] Whats GV

**Saída:** `4. DATASOURCES/MKT Whats GV`

## [133] Remoção de Colunas Não utilizadas — Container

_Descrição:_ Adição da coluna Setor

← [124] Whats GV

1. Remover colunas: `Tempo Medio - Segundos`, `Primeiro Tempo de Espera - Segundos`, `Tempo Atendimento WhatsApp`, `Tempo Formatado WhatsApp`
2. Remover colunas: `testeLis`
3. Remover colunas: `Ciclo - Health Check`, `Recebidos - Health Check`, `E-mail`, `Responsável`, `Tempo até ser atendido`, `Tempo do atendimento`
4. Remover colunas: `Primeiro Tempo de Espera`, `Tempo Médio de Espera`
5. Remover colunas: `Fone Cliente`, `Setor Entrada`
6. Remover colunas: `SLA 24 Horas`, `Qtde Mensagens`, `Observações`, `Campos adicionais Web Chat`
7. Calcular `Setor`:

```
IF ISNULL([Protocolo]) THEN NULL ELSE "WHATS GV" END
```
8. Remapear `SLA 5 Horas`: "Dentro do SLA" ← null
9. Remapear `SLA 10 Horas`: "Dentro do SLA" ← null
10. Remapear `SLA 15 Horas`: "Dentro do SLA" ← null
11. Remover colunas: `CPF/CNPJ`
12. Remover colunas: `Número do Contrato`
13. Remover colunas: `Valor do Contrato`
14. Remover colunas: `CODIGO`
15. Remover colunas: `GV`
16. Remover colunas: `FUNÇÃO`
17. Remover colunas: `CHAMADO`
18. Remover colunas: `Fornecedor`
19. Remover colunas: `Empresa`
20. Remover colunas: `Nome`

→ [145] União Whats GV

## [134] MKT Whats Franquia — PublishExtract

← [125] União de linhas 15

**Saída:** `4. DATASOURCES/MKT Whats Franquia`

## [135] Remoção de Colunas Não utilizadas — Container

_Descrição:_ Adição da coluna Setor

← [125] União de linhas 15

1. Remover colunas: `Tempo Atendimento WhatsApp`
2. Remover colunas: `Tempo Formatado WhatsApp`
3. Remover colunas: `Responsável`
4. Remover colunas: `Tempo até ser atendido`
5. Remover colunas: `Tempo do atendimento`
6. Remover colunas: `Primeiro Tempo de Espera`
7. Remover colunas: `Tempo Médio de Espera`
8. Remover colunas: `Fone Cliente`
9. Remover colunas: `Setor Entrada`
10. Remover colunas: `Qtde Mensagens`
11. Remover colunas: `Campos adicionais Web Chat`
12. Remover colunas: `SLA 24 Horas`
13. Remover colunas: `Observações`
14. Remover colunas: `Empresa`
15. Remover colunas: `Nome`
16. Remover colunas: `Primeiro Tempo de Espera - Segundos`
17. Remover colunas: `CPF/CNPJ`
18. Remover colunas: `Número do Contrato`
19. Remover colunas: `Valor do Contrato`
20. Remover colunas: `CODIGO`
21. Remover colunas: `GV`
22. Remover colunas: `FUNÇÃO`
23. Remover colunas: `CHAMADO`
24. Remover colunas: `Fornecedor`
25. Remover colunas: `Ciclo - Health Check`
26. Remover colunas: `Recebidos - Health Check`
27. Remover colunas: `E-mail`
28. Remover colunas: `Tempo Medio - Segundos`
29. Calcular `Setor`:

```
IF ISNULL([Protocolo]) THEN NULL ELSE "WHATS FRANQUIA" END
```
30. Remover colunas: `testeLis`

→ [138] União CBCOM e WHATS GN

## [136] União de linhas 4 — SuperUnion

← [115] Remoção de Colunas Não utilizadas; [128] Remoção de Colunas Não utilizadas

**Union** das entradas acima (colunas com o mesmo nome se juntam; cria `Table Names`).

1. Remover colunas: `Table Names`

→ [139] MKT BRASIL - Email; [140] Nivel Email

## [137] Responsavel — Container

← [131] Tratar Responsavel

1. Calcular `Nome Responsavel`:

```
CASE REPLACE(REPLACE(UPPER(TRIM([Responsável])), " - INATIVO", ""), "  ", " ")

    WHEN "ADRIANA BORBA" THEN "Adriana Borba"
    WHEN "ADRIANA CONCEIÇÃO" THEN "Adriana Conceição"
    WHEN "ADRIELLE CRISTINA" THEN "Adrielle Cristina"
    WHEN "ADRIELLE CRISTINA PEREIRA SILVA" THEN "Adrielle Cristina Pereira Silva"
    WHEN "ALESSANDRO LINS" THEN "Alessandro Lins"
    WHEN "ALEX BARBOSA SILVA VIDO" THEN "Alex Barbosa Silva Vido"
    WHEN "ALEXANDRE CESAR DA SILVA" THEN "Alexandre Cesar da Silva"
    WHEN "AMANDA DA SILVA MACHADO" THEN "Amanda da Silva Machado"
    WHEN "ANDERSON DE OLIVEIRA LIMA" THEN "Anderson de Oliveira Lima"
    WHEN "ANDREA CHAUD JORGE" THEN "Andrea Chaud Jorge"
    WHEN "ANDRESSA BRITO" THEN "Andressa Brito"
    WHEN "ANTONIO ALEFF PALHANO DE SOUSA" THEN "Antonio Aleff Palhano de Sousa"
    WHEN "ARTUR FERREIRA FAUSTINO" THEN "Artur Ferreira Faustino"
    WHEN "BIANCA ARAUJO" THEN "Bianca Araujo"
    WHEN "BIANCA MARIA ALVES SALES" THEN "Bianca Maria Alves Sales"
    WHEN "BRENDA TONINATO DOS SANTOS" THEN "Brenda Toninato dos Santos"
    WHEN "BRENO NICOLAS DE SOUSA LEME" THEN "Breno Nicolas de Sousa Leme"
    WHEN "BRUNA BRITTO CSU" THEN "Bruna Britto CSU"
    WHEN "BRUNA ELAINE DE DEUS SOUZA" THEN "Bruna Elaine de Deus Souza"
    WHEN "BRUNA SAMANTHA NASCIMENTO DA CRUZ" THEN "Bruna Samantha Nascimento da Cruz"
    WHEN "BRUNO GALDINO DA SILVA" THEN "Bruno Galdino da Silva"
    WHEN "CAROLINE PACIFICO DE ALMEIDA" THEN "Caroline Pacifico de Almeida"
    WHEN "CATIA DA SILVA ALVES" THEN "Catia da Silva Alves"
    WHEN "CHARLENE VIEIRA DE SOUSA CORREIA" THEN "Charlene Vieira de Sousa Correia"
    WHEN "CLAUDIA CARMO" THEN "Claudia Carmo"
    WHEN "CRISTIANE BEDIAS" THEN "Cristiane Bedias"
    WHEN "CRISTINA DE OLIVEIRA PACHECO" THEN "Cristina de Oliveira Pacheco"
    WHEN "DÃ©BORA OLIVEIRA SILVA" THEN "Débora Oliveira Silva"
    WHEN "DÉBORA OLIVEIRA SILVA" THEN "Débora Oliveira Silva"
    WHEN "DANIELE REGINA RODRIGUES DE OLIVEIRA COELHO" THEN "Daniele Regina Rodrigues de Oliveira Coelho"
    WHEN "DANIELLY BRITO" THEN "Danielly Brito"
    WHEN "DANILA SOARES DE OLIVEIRA" THEN "Danila Soares de Oliveira"
    WHEN "DAVID DIAS DE SOUZA" THEN "David Dias de Souza"
    WHEN "DENER MOURA" THEN "Dener Moura"
    WHEN "DIANA AMORIM" THEN "Diana Amorim"
    WHEN "EDILENE SILVA" THEN "Edilene Silva"
    WHEN "ELIANE PADRE" THEN "Eliane Padre"
    WHEN "ELISIA SANTOS" THEN "Elisia Santos"
    WHEN "ERIKA DEL VALLE" THEN "Erika Del Valle"
    WHEN "EULA ADRIELLI MANTOANI ALVES" THEN "Eula Adrielli Mantoani Alves"
    WHEN "EXPERIÊNCIA CN" THEN "Experiência CN"
    WHEN "FABIANA FELIX" THEN "Fabiana Felix"
    WHEN "FABIANA MAGALHAES" THEN "Fabiana Magalhaes"
    WHEN "FÁVIA CHARRO QUISPE MACHACA" THEN "Fávia Charro Quispe Machaca"
    WHEN "FRAN FREITAS" THEN "Fran Freitas"
    WHEN "FRANCIELLE SIVA" THEN "Francielle Siva"
    WHEN "FRANCIELLEN FREITAS SOUSA" THEN "Franciellen Freitas Sousa"
    WHEN "FRANKLIN JAVIER" THEN "Franklin Javier"
    WHEN "GABRIEL BAZILIO MEDEIROS DE CARVALHO" THEN "Gabriel Bazilio Medeiros de Carvalho"
    WHEN "GABRIEL MACEDO SILVA" THEN "Gabriel Macedo Silva"
    WHEN "GABRIEL SILVA" THEN "Gabriel Silva"
    WHEN "GABRIELLA BARROS" THEN "Gabriella Barros"
    WHEN "GABRIELLA GRASIELLI DO VALE" THEN "Gabriella Grasielli do Vale"
    WHEN "GABRIELLE TENORIO" THEN "Gabrielle Tenorio"
    WHEN "GESSICA MACEDO MIURA" THEN "Gessica Macedo Miura"
    WHEN "GIOVANNA PAOLIELLO DOS SANTOS" THEN "Giovanna Paoliello dos Santos"
    WHEN "GLEYZE ELAYNE ESCORCIO SILVA" THEN "Gleyze Elayne Escorcio Silva"
    WHEN "HAMONA CHISTIAN" THEN "Hamona Chistian"
    WHEN "HARYSSA NAYANNE DA SILVA SANTANA" THEN "Haryssa Nayanne da Silva Santana"
    WHEN "IARA DOS SANTOS" THEN "Iara dos Santos"
    WHEN "IGOR ROCHA DOS SANTOS" THEN "Igor Rocha dos Santos"
    WHEN "ISADORA SANDES" THEN "Isadora Sandes"
    WHEN "JANAINA" THEN "Janaina"
    WHEN "JAQUELINE DA SILVA SOUZA" THEN "Jaqueline da Silva Souza"
    WHEN "JESSICA MORAES MOURA" THEN "Jessica Moraes Moura"
    WHEN "JHENNIFER GODOI DA SILVA" THEN "Jhennifer Godoi da Silva"
    WHEN "JHONNY CLEBER DA PAZ SANTANA" THEN "Jhonny Cleber da Paz Santana"
    WHEN "JOÃO LUCAS VIEIRA DE CARVALHO" THEN "João Lucas Vieira de Carvalho"
    WHEN "JOEL TORRES" THEN "Joel Torres"
    WHEN "JORGE" THEN "Jorge"
    WHEN "JUCILENE SANTOS OLIVEIRA" THEN "Jucilene Santos Oliveira"
    WHEN "JULIA DOS SANTOS ANDRADE" THEN "Julia dos Santos Andrade"
    WHEN "JULIANA CARVALHO DE FREITAS" THEN "Juliana Carvalho de Freitas"
    WHEN "JULIANA MOISÉS" THEN "Juliana Moisés"
    WHEN "JULIANA SILVA" THEN "Juliana Silva"
    WHEN "JULIANA TENÓRIO JOAQUIM" THEN "Juliana Tenório Joaquim"
    WHEN "KELLY RODRIGUES" THEN "Kelly Rodrigues"
    WHEN "KENNEDY VARELA" THEN "Kennedy Varela"
    WHEN "KETHELYN JESUS" THEN "Kethelyn Jesus"
    WHEN "KETY PEREIRA DA SILVA" THEN "Kety Pereira da Silva"
    WHEN "KEVIN SILVA - NEW WAY" THEN "Kevin Silva - New Way"
    WHEN "LAILA DE LOURDES SILVA GUERRA" THEN "Laila de Lourdes Silva Guerra"
    WHEN "LAIS SANTOS" THEN "Lais Santos"
    WHEN "LARISSA GONCALVES MOTA" THEN "Larissa Goncalves Mota"
    WHEN "LETICIA BONFIM DA SILVA" THEN "Leticia Bonfim da Silva"
    WHEN "LETICIA MAIARA RODRIGUES FREIRE" THEN "Leticia Maiara Rodrigues Freire"
    WHEN "LETICIA MAIRA RODRIGUES FREIRE" THEN "Leticia Maiara Rodrigues Freire"
    WHEN "LETICIA SILVA" THEN "Leticia Silva"
    WHEN "LIDIANE DA SILVA" THEN "Lidiane da Silva"
    WHEN "LISLAINE" THEN "Lislaine"
    WHEN "LISLAINE GOMES" THEN "Lislaine Gomes"
    WHEN "LUCIA SILVA" THEN "Lucia Silva"
    WHEN "LUCIMARA MENDES" THEN "Lucimara Mendes"
    WHEN "LUIS GUILHERME" THEN "Luis Guilherme"
    WHEN "LUISA RODRIGUES DE CASTRO GRACIANO" THEN "Luisa Rodrigues de Castro Graciano"
    WHEN "MARCIO MIRANDA ALVES DOS SANTOS" THEN "Márcio Miranda Alves dos Santos"
    WHEN "MÁRCIO MIRANDA ALVES DOS SANTOS" THEN "Márcio Miranda Alves dos Santos"
    WHEN "MARCOS02" THEN "Marcos02"
    WHEN "MARIA CARLEUSA CONCEIÃ‡AO" THEN "Maria Carleusa Conceiçao"
    WHEN "MARIA CARLEUSA CONCEIÇAO" THEN "Maria Carleusa Conceiçao"
    WHEN "MARIANA MOTA DE MATOS" THEN "Mariana Mota de Matos"
    WHEN "MATEUS CORDEIRO" THEN "Mateus Cordeiro"
    WHEN "MATHEUS CRUZ" THEN "Matheus Cruz"
    WHEN "MATHEUS GOUVEIA DA SILVA" THEN "Matheus Gouveia da Silva"
    WHEN "MATHEUS VERGILIO" THEN "Matheus Vergilio"
    WHEN "MAURO JORGE ANDRADE MARQUES" THEN "Mauro Jorge Andrade Marques"
    WHEN "MAVIANE SILVA" THEN "Maviane Silva"
    WHEN "MAYARA TEODORO DE LIMA" THEN "Mayara Teodoro de Lima"
    WHEN "MAYSA SANTOS" THEN "Maysa Santos"
    WHEN "MILENA SILVA" THEN "Milena Silva"
    WHEN "MONIQUE JESUS" THEN "Monique Jesus"
    WHEN "NATALY DA SILVA COELHO" THEN "Nataly da Silva Coelho"
    WHEN "NATHALIA G. SOUZA" THEN "Nathalia G. Souza"
    WHEN "NICANOR CARDOSO" THEN "Nicanor Cardoso"
    WHEN "NIVIA MARIA AQUINO DOS SANTOS" THEN "Nivia Maria Aquino dos Santos"
    WHEN "PALOMA ALMEIDA DE OLIVEIRA" THEN "Paloma Almeida de Oliveira"
    WHEN "PAMELA BUENO" THEN "Pamela Bueno"
    WHEN "PAMELA EMILLY DE FREITAS BUENO" THEN "Pamela Emilly de Freitas Bueno"
    WHEN "PATRICIA CRUZ" THEN "Patricia Cruz"
    WHEN "PATRICIA GOMES RODRIGUES" THEN "Patricia Gomes Rodrigues"
    WHEN "PEDRO DO CANTO" THEN "Pedro do Canto"
    WHEN "RAFAELLA CRISTINY JACINTO" THEN "Rafaella Cristiny Jacinto Camilo"
    WHEN "RAFAELLA CRISTINY JACINTO CAMILO" THEN "Rafaella Cristiny Jacinto Camilo"
    WHEN "RAQUEL LEIA" THEN "Raquel Leia"
    WHEN "RAQUEL RODRIGUES DE MIRANDA" THEN "Raquel Rodrigues de Miranda"
    WHEN "REBECA" THEN "Rebeca"
    WHEN "REBECA LIBERATO BORGES" THEN "Rebeca Liberato Borges"
    WHEN "RENATA DA SILVA" THEN "Renata da Silva"
    WHEN "RHANA BRAGA" THEN "Rhana Braga"
    WHEN "ROBSON RIBEIRO DA COSTA" THEN "Robson Ribeiro da Costa"
    WHEN "RODRIGO CRISTIANO" THEN "Rodrigo Cristiano"
    WHEN "ROGERIO PEREIRA SANTOS" THEN "Rogerio Pereira Santos"
    WHEN "ROSANA SIQUEIRA DE MIRANDA" THEN "Rosana Siqueira de Miranda"
    WHEN "SAMANTA SILVA" THEN "Samanta Silva"
    WHEN "SAMARA ROMAO MINEIRO" THEN "Samara Romao Mineiro"
    WHEN "SILVANA JAGUSZEWSKI" THEN "Silvana Jaguszewski"
    WHEN "SINILZA SANTOS" THEN "Sinilza Santos"
    WHEN "STEPHANY DA SILVA OLIVEIRA" THEN "Stephany da Silva Oliveira"
    WHEN "SUELEN ALMEIDA" THEN "Suelen Almeida"
    WHEN "SUELEN RESENDE" THEN "Suelen Resende"
    WHEN "THADEU MACIEL" THEN "Thadeu Maciel"
    WHEN "THAIS CAMARGO" THEN "Thais Camargo"
    WHEN "THAIS CRISTINA" THEN "Thais Cristina"
    WHEN "THAIS CRISTINA ARAÃºJO DE SOUSA" THEN "Thais Cristina Araújo de Sousa"
    WHEN "THAIS CRISTINA ARAÚJO DE SOUSA" THEN "Thais Cristina Araújo de Sousa"
    WHEN "THALITA INACIA RODRIGUES DE SANTANA" THEN "Thalita Inacia Rodrigues de Santana"
    WHEN "THIAGO CARDOSO VIEIRA" THEN "Thiago Cardoso Vieira"
    WHEN "THIAGO PELUSO" THEN "Thiago Peluso"
    WHEN "VALERIA APARECIDA PEREIRA DO LAGO" THEN "Valeria Aparecida Pereira do Lago"
    WHEN "VALERIA BENTO" THEN "Valeria Bento"
    WHEN "VALQUIRIA SANTIAGO" THEN "Valquiria Santiago"
    WHEN "VANESSA DUARTE" THEN "Vanessa Duarte"
    WHEN "VANESSA DUARTE GARRIDO" THEN "Vanessa Duarte Garrido"
    WHEN "VICTORIA FERRACIN DA CONCEIÇÃO" THEN "Victoria Ferracin da Conceição"
    WHEN "VITOR LUCAS FABRICIO MARQUES" THEN "Vitor Lucas Fabricio Marques"
    WHEN "VITOR SECHI" THEN "Vitor Sechi"
    WHEN "VITORIA ALVES" THEN "Vitoria Alves"
    WHEN "VITORIA PABLINE GOMES DA SILVA" THEN "Vitoria Pabline Gomes da Silva"
    WHEN "VITORIA RODRIGUES" THEN "Vitoria Rodrigues"
    WHEN "VIVIANE SILVA" THEN "Viviane Silva"
    WHEN "WILLIANE BORGES" THEN "Williane Borges"
    WHEN "YRIS FERREIRA" THEN "Yris Ferreira"

    // Rede de segurança: Remove o "- INATIVO" de qualquer nome novo que entrar no futuro
    ELSE REPLACE([Responsável], " - INATIVO", "")

END
```
2. Remapear `Qtd Atendimentos-1`: 1 ← null
3. Remover colunas: `Qtd Atendimentos`
4. Remover colunas: `Qtd Atendimentos Tickets`
5. Renomear `Qtd Atendimentos-1` → `Qtd Atendimentos`
6. RichRelativeDateFilter: `{"columnName": "Data conclusão", "fieldId": "ebf58d2c-9eb7-41f9-9779-af834fc7da8a-Data conclusão-abd9d1d9-5a3a-42fe-93c7-e365b19cdab3-Data conclusão", "timeIntervalDiscretization": 0, "filterSelection": 1, "lastTimeIntervalAmount": 3, "nextTimeIntervalAmount": 3, "isAnchoredRelativeToTimeInterval": false, "timeIntervalAnchor": "1787765474828", "isIncludingNullValues": false}`
7. Excluir `Status` em ['"Card Em Branco"']
8. Excluir `Status` em ['"EXPCB"']

→ [141] MKT Brasil Completo Nivel; [142] Nivel Email MKT Completo

## [138] União CBCOM e WHATS GN — SuperUnion

← [130] Remoção de Colunas Não utilizadas; [135] Remoção de Colunas Não utilizadas; [121] Remoção de Colunas Não utilizadas

**Union** das entradas acima (colunas com o mesmo nome se juntam; cria `Table Names`).

→ [143] Limpar 13

## [139] MKT BRASIL - Email — PublishExtract

← [136] União de linhas 4

**Saída:** `4. DATASOURCES/MKT BRASIL - Email`

## [140] Nivel Email — Container

← [136] União de linhas 4

1. Renomear `Nível` → `Nivel`
2. Manter só: `Status de Classificação`, `Nivel`, `Setor`, `Protocolo`, `PEDIDO FINALIZADO`, `CONTATO DE SOLUÇÃO`, `Qtd Atendimentos`, `Função do Sistema`, `Data Contato`, `Status de finalização`
3. Renomear `PEDIDO FINALIZADO` → `Pedido Finalizado`
4. Remapear `Pedido Finalizado`: "NÃO" ← "nao", "N&#195;O"; "NÃO SE APLICA" ← "nao_se_aplica", "N&#195;O SE APLICA"
5. Renomear `CONTATO DE SOLUÇÃO` → `Contato de Solução`
6. Renomear `Protocolo` → `Ticket`
7. Renomear `Data Contato` → `Data`
8. Renomear `Setor` → `Tipo`
9. Calcular `Origem`:

```
"MKT Analitico"
```

→ [144] União de linhas 21

## [141] MKT Brasil Completo Nivel — PublishExtract

← [137] Responsavel

**Saída:** `4. DATASOURCES/MKT Brasil Completo Nivel`

## [142] Nivel Email MKT Completo — Container

← [137] Responsavel

1. Renomear `Status` → `Status de finalização`
2. Calcular `Origem`:

```
"MKT Completo"
```
3. Renomear `Canal` → `Tipo`
4. Calcular `Contato de Solução`:

```
NULL
```
5. Calcular `Pedido Finalizado`:

```
NULL
```
6. Remover colunas: `Qtde Mensagens`
7. Renomear `Protocolo` → `Ticket`
8. Renomear `Qtd Atendimentos` → `Qtd Atendimentos`
9. Renomear `Data conclusão` → `Data`
10. Remover colunas: `SOLUÇÃO APLICADA`
11. Remover colunas: `Protocolo2`
12. Remover colunas: `Responsável`
13. Remover colunas: `Tempo médio operacional`
14. Remover colunas: `Tempo médio espera`
15. Remover colunas: `Tempo médio atendimento`
16. Remover colunas: `Tempo médio primeira espera`
17. Remover colunas: `Tempo médio até ser atendidos`
18. Remover colunas: `Situação`
19. Remover colunas: `Telefone`
20. Remover colunas: `Operador`
21. Remover colunas: `Setor`
22. Remover colunas: `Tipo Canal`
23. Remover colunas: `Última mensagem`
24. Remover colunas: `Atendido`
25. Remover colunas: `Início Atendimento`
26. Remover colunas: `Data criação`
27. Remover colunas: `'Atendimentos'(first_message_at)`
28. Remover colunas: `Nome`
29. Remover colunas: `Nome Responsavel`

→ [144] União de linhas 21

## [143] Limpar 13 — Container

← [138] União CBCOM e WHATS GN

1. Remover colunas: `Table Names`

→ [145] União Whats GV

## [144] União de linhas 21 — SuperUnion

← [142] Nivel Email MKT Completo; [140] Nivel Email

**Union** das entradas acima (colunas com o mesmo nome se juntam; cria `Table Names`).

1. Remover colunas: `Table Names`

→ [150] União de linhas 7

## [145] União Whats GV — SuperUnion

← [143] Limpar 13; [133] Remoção de Colunas Não utilizadas

**Union** das entradas acima (colunas com o mesmo nome se juntam; cria `Table Names`).

→ [146] Limpar 14

## [146] Limpar 14 — Container

← [145] União Whats GV

1. Remover colunas: `Table Names`

→ [147] União Whats GV Antecipada

## [147] União Whats GV Antecipada — SuperUnion

← [146] Limpar 14; [123] Remoção de Colunas Não utilizadas

**Union** das entradas acima (colunas com o mesmo nome se juntam; cria `Table Names`).

1. Remover colunas: `Table Names`

→ [148] Nivel WhatsApp; [149] Limpar 16

## [148] Nivel WhatsApp — Container

← [147] União Whats GV Antecipada

1. Renomear `Nível` → `Nivel`
2. Manter só: `Status de Classificação`, `Nivel`, `Setor`, `Protocolo`, `PEDIDO FINALIZADO`, `CONTATO DE SOLUÇÃO`, `Qtd Atendimentos`, `Função do Sistema`, `Data Contato`, `Status de finalização`
3. Renomear `PEDIDO FINALIZADO` → `Pedido Finalizado`
4. Renomear `CONTATO DE SOLUÇÃO` → `Contato de Solução`
5. Renomear `Setor` → `Tipo`
6. Renomear `Protocolo` → `Ticket`
7. Renomear `Data Contato` → `Data`

→ [150] União de linhas 7

## [149] Limpar 16 — Container

← [147] União Whats GV Antecipada

1. Remapear `Origem`: "AppSheets" ← null

→ [151] MKT BRASIL - WhatsApp

## [150] União de linhas 7 — SuperUnion

← [148] Nivel WhatsApp; [144] União de linhas 21

**Union** das entradas acima (colunas com o mesmo nome se juntam; cria `Table Names`).

→ [152] União de linhas 9

## [151] MKT BRASIL - WhatsApp — PublishExtract

← [149] Limpar 16

**Saída:** `4. DATASOURCES/MKT BRASIL - WhatsApp`

## [152] União de linhas 9 — SuperUnion

← [150] União de linhas 7

**Union** das entradas acima (colunas com o mesmo nome se juntam; cria `Table Names`).

1. Remover colunas: `Table Names-1`, `Table Names`

→ [153] União de linhas 11

## [153] União de linhas 11 — SuperUnion

← [46] Remoção de colunas; [29] Dynamcis; [152] União de linhas 9

**Union** das entradas acima (colunas com o mesmo nome se juntam; cria `Table Names`).

→ [154] Limpar 9

## [154] Limpar 9 — Container

← [153] União de linhas 11

1. Calcular `Int Pedido Finalizado`:

```
IF
	[Pedido Finalizado] = "Sim"
THEN
	1
ELSE
	0
END
```
2. Calcular `Mes`:

```
// Pega o número do mês, adiciona um zero à esquerda se necessário, e une com o ano.
RIGHT("0" + STR(MONTH([Data])), 2) + "/" + STR(YEAR([Data]))
```

→ [155] Remoção do Dynamics; [156] Remoção Dynatrace

## [155] Remoção do Dynamics — Container

← [154] Limpar 9

1. Remover colunas: `Status de Classificação`, `Status de finalização`
2. Excluir `Origem` em ['"MKT Completo"']
3. Remover colunas: `Origem`
4. Remover colunas: `Responsavel Dynamics`
5. Excluir `Tipo` em ['"Protocolos CB"', '"Protocolos CF"']

→ [157] Limpar 10

## [156] Remoção Dynatrace — Container

← [154] Limpar 9

1. Excluir `Origem` em ['"MKT Analitico"']
2. Remover colunas: `Origem`
3. Remover colunas: `Table Names`
4. Excluir `Tipo` em ['"Dynatrace"']

→ [158] União de colunas 17

## [157] Limpar 10 — Container

← [155] Remoção do Dynamics

1. Manter só: `Int Pedido Finalizado`, `Mes`

→ [159] União de colunas 3

## [158] União de colunas 17 — SuperJoin

← [4] MKT Reativos (Left); [156] Remoção Dynatrace (Right)

**Join right**: esquerda = [4] MKT Reativos, direita = [156] Remoção Dynatrace

Condição: `esq.[Protocolo] == dir.[Ticket]`

1. (antes do join, lado esquerdo) Remover colunas: `Empresa`, `Nome`, `CPF/CNPJ`, `Número do Contrato`, `Valor do Contrato`, `CODIGO`, `GV`, `FUNÇÃO`, `PEDIDO FINALIZADO`, `CONTATO DE SOLUÇÃO`, `CHAMADO`, `Fornecedor`, `Qtd Atendimentos`, `testeLis`, `Função do Sistema`, `Ciclo - Health Check`, `Recebidos - Health Check`, `CATEGORIA 1 (WR TRANSP)`, `CATEGORIA 2 (WR TRANSP)`, `SOLUÇÃO APLICADA`, `Origem Health Check?`, `Está em Fechamento?`, `Código do Impactado`, `Ciclo Vigente`, `SETOR`, `MERCADO`, `Resposta pedido duplicado`, `Dados bancarios`, `E-mail`, `Data Contato`
2. (antes do join, lado esquerdo) Remover colunas: `Tempo até ser atendido`, `Tempo do atendimento`, `Primeiro Tempo de Espera`, `Tempo Médio de Espera`, `Tempo de Operação`, `Fone Cliente`, `Canal de Entrada`, `Setor Entrada`, `Setor Fim`, `Qtde Mensagens`, `Status de Classificação`, `Status de finalização`, `Encerrado em`, `Observações`, `Campos adicionais Web Chat`, `Quantidade de Tickets`
3. Remover colunas: `Protocolo`

→ [160] Responsavel

## [159] União de colunas 3 — SuperJoin

← [33] Mes (Left); [157] Limpar 10 (Right)

**Join inner**: esquerda = [33] Mes, direita = [157] Limpar 10

Condição: `esq.[Mes] == dir.[Mes]`

1. Remover colunas: `Mes-1`

→ [161] Limpar 11

## [160] Responsavel — Container

_Descrição:_ Ajuste das colunas de Responsavel entre MKT e Dynamics

← [158] União de colunas 17

1. Calcular `New Responsavel`:

```
IF ISNULL([Responsavel Dynamics]) THEN
	[Responsável]
ELSE [Responsavel Dynamics]
END
```
2. Remover colunas: `Responsável`
3. Remover colunas: `Responsavel Dynamics`
4. Renomear `New Responsavel` → `Responsavel`

→ [162] União de colunas 19

## [161] Limpar 11 — Container

← [159] União de colunas 3

→ [163] Ticket Medio Exp Br

## [162] União de colunas 19 — SuperJoin

← [16] Registro Acionamento (Left); [160] Responsavel (Right)

**Join right**: esquerda = [16] Registro Acionamento, direita = [160] Responsavel

Condição: `esq.[ID] == dir.[Ticket]`

1. (antes do join, lado esquerdo) Remover colunas: `Data do contato`, `Canal de Entrada`, `Protocolo`
2. (antes do join, lado esquerdo) Remover colunas: `Código do Impactado`, `Qtde de Atendimentos`, `Pedido finalizado`, `Função do Sistema`, `Status de Organização`, `Status de Finalização`, `Chamado`

→ [164] Responsavel

## [163] Ticket Medio Exp Br — PublishExtract

← [161] Limpar 11

**Saída:** `4. DATASOURCES/Ticket Medio Exp Br`

## [164] Responsavel — Container

_Descrição:_ Adequação com a base de Registro de Acionamento

← [162] União de colunas 19

1. Calcular `New Responsavel`:

```
IF ISNULL([Responsavel]) THEN
	[Analista]
ELSE
	[Responsavel]
END
```
2. Remover colunas: `Analista`
3. Remover colunas: `Responsavel`
4. Renomear `New Responsavel` → `Responsavel`
5. Remapear `Responsavel`: "Adriana Conceicao De Oliveira" ← "adrianaoliveira.sonda@natura.net"; "Adrielle Cristina" ← "adriellesilva.sonda@natura.net"; "Andrea Chaud Jorge" ← "ANDREA jorge"; "Bruno Galdino da Silva" ← "brunogaldino.sonda@natura.net"; "Caroline Pacifico de Almeida" ← "CAROLINE PACIFICO DE ALMEIDA"; "Bruna Souza" ← "Bruna souza"; "Daniele Coelho" ← "Daniele coelho"; "Gabrielle tenorio" ← "gabrielletenorio.sonda@natura.net"; "Haryssa Nayanne Da Silva Santana" ← "haryssasantana.sonda@natura.net"; "Luis Guilherme" ← "Luis Guilherme Teodoro Dos Santos", "luissantos.sonda@natura.net"; "Marcio Miranda Alves dos Santos" ← "marcioalves.sonda@natura.net"; "Mayara Teodoro De Lima" ← "mayaralima.sonda@natura.net"; "Rafaella Cristiny Jacinto Camilo" ← "rafaellacamilo.sonda@natura.net"; "Suelen Resende De Almeida" ← "Suelen Almeida", "suelenalmeida.sonda@natura.net"; "Vanessa Duarte Garrido" ← "Vanessa Duarte", "vanessagarrido.sonda@natura.net"; "Williane Borges" ← "willianeassis.sonda@natura.net"; "Danila Soares de Oliveira" ← "danilaferreira.sonda@natura.net"

→ [165] Responsavel

## [165] Responsavel — Container

← [164] Responsavel

1. Renomear `Responsavel` → `Responsavel1`

→ [166] União de colunas 23

## [166] União de colunas 23 — SuperJoin

← [165] Responsavel (Right); [47] Analista ServiceCloud (Left)

**Join right**: esquerda = [47] Analista ServiceCloud, direita = [165] Responsavel

Condição: `esq.[ID SC] == dir.[Ticket]`

→ [167] Responsavel

## [167] Responsavel — Container

_Descrição:_ Adição do Responsável oriundo do Service Cloud

← [166] União de colunas 23

1. Calcular `Responsavel`:

```
IF ISNULL([Responsavel1]) THEN [Analista SC] ELSE [Responsavel1] END
```
2. Remover colunas: `Responsavel1`
3. Remover colunas: `ID SC`
4. Remover colunas: `Analista SC`

→ [168] Adição Resenhas

## [168] Adição Resenhas — SuperUnion

← [167] Responsavel; [34] Adequar colunas

**Union** das entradas acima (colunas com o mesmo nome se juntam; cria `Table Names`).

1. Remover colunas: `Table Names`

→ [169] Responsavel

## [169] Responsavel — Container

_Descrição:_ Ajustar nome dos analistas

← [168] Adição Resenhas

1. Remapear `Responsavel`: "Adriana Conceição" ← "Adriana Conceicao De Oliveira"; "Andrea Chaud Jorge" ← "andreachaud.sonda@natura.net"; "Cristiane bedias" ← "Cristiane Bedias - INATIVO"; "Daniele Coelho" ← "Daniele Regina Rodrigues de Oliveira Coelho"; "Gabrielle tenorio" ← "gabrielletenorio.sonda@natura.net"; "Kethelyn Ellen Oliveira De Jesus" ← "Kethelyn Jesus - INATIVO", "kethelynjesus.sonda@natura.net"; "Milena Cordeiro Da Silva" ← "Milena Silva", "milenasilva.sonda@natura.net"; "Patricia rodrigues" ← "patriciarodrigues.sonda@natura.net"; "Renata Silva" ← "renatasilva1.sonda@natura.net"; "Rhana Braga" ← "rhanabraga.sonda@natura.net"; "Thadeu Rocha" ← "thadeurocha.sonda@natura.net"; "Vanessa Duarte Garrido" ← "vanessagarrido.sonda@natura.net"; "Viviane Da Silva" ← "Viviane Silva"; "Danila Soares de Oliveira" ← "Danila Ferreira", "danilaferreira.sonda@natura.net"

→ [170] União de colunas 27

## [170] União de colunas 27 — SuperJoin

← [169] Responsavel (Right); [30] Limpar 27 (Left)

**Join right**: esquerda = [30] Limpar 27, direita = [169] Responsavel

Condição: `esq.[Protocolo] == dir.[Ticket]`

→ [171] Limpar 22

## [171] Limpar 22 — Container

← [170] União de colunas 27

1. Remover colunas: `Protocolo`
2. Renomear `Função do Sistema` → `Função do Sistema-3`
3. Calcular `Função do Sistema`:

```
IF NOT ISNULL([Função do Sistema-1]) THEN 
    [Função do Sistema-1]

ELSEIF NOT ISNULL([Função do Sistema-2]) THEN 
    [Função do Sistema-2]

ELSE 
    [Função do Sistema-3]
END
```
4. Remover colunas: `Função do Sistema-3`, `Função do Sistema-1`, `Função do Sistema-2`
5. Renomear `Status de Classificação` → `Status de Classificação2`
6. Calcular `Status de Classificação`:

```
IF NOT ISNULL([Status de Classificação1]) THEN 
    [Status de Classificação1]

ELSEIF NOT ISNULL([Status de Classificação2]) THEN 
    [Status de Classificação2]

ELSE 
    [Status de Classificação3]
END
```
7. Remover colunas: `Status de Classificação3`, `Status de Classificação2`, `Status de Classificação1`

→ [172] Limpar 27

## [172] Limpar 27 — Container

← [171] Limpar 22

1. Remapear `Responsavel`: "Adriana Conceição" ← "adrianaoliveira.sonda@natura.net"; "Bruna Elaine De Deus Souza" ← "Bruna Souza"; "Daniele Coelho" ← "danielecoelho.sonda@natura.net"; "Joao Lucas Vieira De Carvalho" ← "joaocarvalho.sonda@natura.net"; "Leticia silva" ← "leticiasilva.sonda@natura.net"; "Robson  Ribeiro da Costa" ← "Robson Ribeiro Da Costa"; "Taina Pereira Galdino Da Silva" ← "Taina Pereira Galdino"

→ [173] Experiencia Brasil Nivel

## [173] Experiencia Brasil Nivel — PublishExtract

← [172] Limpar 27

**Saída:** `4. DATASOURCES/Experiencia Brasil Nivel`
