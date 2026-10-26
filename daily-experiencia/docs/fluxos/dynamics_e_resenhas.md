# Especificação do fluxo `Daily Experiencia BR - Dynamics e Resenhas.tfl`

Gerado por `ferramentas/especificar_fluxo_prep.py`. Etapas em ordem de execução; `←` indica de onde vêm os dados.

## [1] Criados CF Service Cloud  2026 — LoadSql

Arquivo: `Salesforce CF Criados.xlsx` · aba `[Base$]`

Campos: `Usuário que realizou alteração: Nome completo`:string, `Número do caso`:string, `Primeira Categoria`:string, `Segunda Categoria`:string, `Motivo`:string, `Etapa`:string, `Classificação do problema sistêmico`:string, `Aplicativo com problemas`:string, `Data/Hora de abertura`:datetime, `Data alvo SLA`:datetime, `Data/Hora de fechamento`:datetime, `Solução`:string, `Proprietário`:string, `Etapa 1`:string, `Status`:string, `Chamado`:string, `Caso pai: Chamado`:string, `Nome da conta: CPF`:string, `Id Caso Completo`:string, `Modificado pela última vez por: Nome completo`:string, `Data início`:datetime, `Data fim`:datetime, `Tipo de registro do caso`:string

Ações na leitura:

- Renomear `Número do caso` → `Número da Ocorrência (Referente) (Ocorrência)`
- Renomear `Status` → `Status da Atividade`
- Renomear `Primeira Categoria` → `Primeira Categoria (Referente) (Ocorrência)`
- Renomear `Segunda Categoria` → `Segunda Categoria (Referente) (Ocorrência)`
- Renomear `Motivo` → `Motivo (Referente) (Ocorrência)`
- Renomear `Data/Hora de abertura` → `Data de Criação`
- Renomear `Data/Hora de fechamento` → `Término Real`
- Renomear `Data alvo SLA` → `Data do SLA`
- Renomear `Classificação do problema sistêmico` → `Experience`

→ [17] Dados a partir de 2026

## [2] Encerrados CF Service Cloud  2026 — LoadSql

Arquivo: `Salesforce CF Encerrados.xlsx` · aba `[Base$]`

Campos: `Usuário que realizou alteração: Nome completo`:string, `Número do caso`:string, `Primeira Categoria`:string, `Segunda Categoria`:string, `Motivo`:string, `Etapa`:string, `Classificação do problema sistêmico`:string, `Aplicativo com problemas`:string, `Data/Hora de abertura`:datetime, `Data alvo SLA`:datetime, `Data/Hora de fechamento`:datetime, `Solução`:string, `Proprietário`:string, `Etapa 1`:string, `Status`:string, `Chamado`:string, `Caso pai: Chamado`:string, `Nome da conta: CPF`:string, `Id Caso Completo`:string, `Modificado pela última vez por: Nome completo`:string, `Data início`:datetime, `Data fim`:datetime, `Tipo de registro do caso`:string

Ações na leitura:

- Renomear `Número do caso` → `Número da Ocorrência (Referente) (Ocorrência)`
- Renomear `Primeira Categoria` → `Primeira Categoria (Referente) (Ocorrência)`
- Renomear `Segunda Categoria` → `Segunda Categoria (Referente) (Ocorrência)`
- Renomear `Motivo` → `Motivo (Referente) (Ocorrência)`
- Renomear `Data/Hora de abertura` → `Data de Criação`
- Renomear `Data alvo SLA` → `Data do SLA`
- Renomear `Data/Hora de fechamento` → `Término Real`
- Renomear `Status` → `Status da Atividade`
- Renomear `Classificação do problema sistêmico` → `Experience`

→ [18] Dados a partir 2026

## [3] Base_GruposServiceNow_2209 2 — LoadSql

Arquivo: `Mapeamento: Assunto / Função do sistema x Jornada (Tribo)` · aba `[Base_GruposServiceNow_2209$]`

Campos: `Grupo de atribuição - no SErvice Now`:string, `Nomenclatura para criar Aba no Service Now`:string, `Nomenclatura para criar Aba no Service Now 1`:string, `Tribo`:string, `Responsável`:string, `Gerente Responsável`:string, `F7`:string

→ [19] Limpar 11

## [4] Tribos Dynamics — LoadSql

Arquivo: `Mapeamento: Assunto / Função do sistema x Jornada (Tribo)` · aba `['Base Dynamics_1309$']`

Campos: `Experience`:string, `Plataforma`:string, `Tribo`:string, `Macro`:string, `F5`:string

Ações na leitura:

- Renomear `Experience` → `Experience Tribos`

→ [64] União de colunas 3; [60] Join 1

## [5] Resenhas AppSheets — LoadSql (grupo Resenhas AppSheets)

Arquivo: `Resenhas` · aba `[BaseDados$]`

Campos: `F1`:string, `Aplicativo`:string, `Loja`:string, `Nome do Respondente`:string, `Classificação de Estrelas`:string, `Data da Resposta`:date, `Categoria da Resposta`:string, `Categoria da Resposta 2`:string, `Classificação da Resposta`:string, `Comentário Postado`:string, `Resposta Fornecida`:string, `Classificação do Ofensor`:string, `IDIOMA`:string, `Resp. pela resposta`:string, `Data da Resposta EXP`:datetime, `OBSERVACAO`:string

Ações na leitura:

- Renomear `F1` → `ID`

→ [20] Limpar 3

## [6] Expurgo — LoadSql

Arquivo: `Expurgo` · aba `[Página1$]`

Campos: `Número da Ocorrência (Referente) (Ocorrência)`:string, `Nivel de Atendimento`:string, `Data Expurgo`:date, `Mês de Expurgo`:string, `Motivo`:string

→ [21] Limpar 9

## [7] Criados ServiceCloud — LoadSql

Arquivo: `Salesforce CF Criados.xlsx` · aba `[Base$]`

Campos: `Usuário que realizou alteração: Nome completo`:string, `Número do caso`:string, `Primeira Categoria`:string, `Segunda Categoria`:string, `Motivo`:string, `Etapa`:string, `Classificação do problema sistêmico`:string, `Aplicativo com problemas`:string, `Data/Hora de abertura`:datetime, `Data alvo SLA`:datetime, `Data/Hora de fechamento`:datetime, `Solução`:string, `Proprietário`:string, `Etapa 1`:string, `Status`:string, `Chamado`:string, `Caso pai: Chamado`:string, `Nome da conta: CPF`:string, `Id Caso Completo`:string, `Modificado pela última vez por: Nome completo`:string, `Data início`:datetime, `Data fim`:datetime, `Tipo de registro do caso`:string

Ações na leitura:

- Renomear `Número do caso` → `Número da Ocorrência (Referente) (Ocorrência)`
- Renomear `Status` → `Status da Atividade`
- Renomear `Primeira Categoria` → `Primeira Categoria (Referente) (Ocorrência)`
- Renomear `Segunda Categoria` → `Segunda Categoria (Referente) (Ocorrência)`
- Renomear `Motivo` → `Motivo (Referente) (Ocorrência)`
- Renomear `Data alvo SLA` → `Data do SLA`
- Renomear `Data/Hora de fechamento` → `Término Real`
- Renomear `Data/Hora de abertura` → `Data de Criação`

→ [22] Limpar 10

## [8] CF Salesforce — LoadSql

Arquivo: `Salesforce CF.xlsx` · aba `[Base$]`

Campos: `Número do caso`:string, `Primeira Categoria`:string, `Segunda Categoria`:string, `Motivo`:string, `Etapa`:string, `Classificação do problema sistêmico`:string, `Aplicativo com problemas`:string, `Data/Hora de abertura`:datetime, `Data alvo SLA`:datetime, `Data/Hora de fechamento`:datetime, `Solução`:string, `Proprietário`:string, `Etapa 1`:string, `Status`:string, `Chamado`:string, `Caso pai: Chamado`:string

Ações na leitura:

- Renomear `Número do caso` → `Número da Ocorrência (Referente) (Ocorrência)`
- Renomear `Status` → `Status da Atividade`
- Renomear `Primeira Categoria` → `Primeira Categoria (Referente) (Ocorrência)`
- Renomear `Segunda Categoria` → `Segunda Categoria (Referente) (Ocorrência)`
- Renomear `Motivo` → `Motivo (Referente) (Ocorrência)`
- Renomear `Data alvo SLA` → `Data do SLA`
- Renomear `Data/Hora de fechamento` → `Término Real`
- Renomear `Data/Hora de abertura` → `Data de Criação`

→ [23] Remover Duplicada

## [9] Criados em  - Dynamics — LoadSql

Arquivo: `Criados em.xlsx` · aba `['Criados em  - Tarefas Exper###$']`

Campos: `(Não Modificar) Tarefa`:string, `(Não Modificar) Soma de Verificação da Linha`:string, `(Não Modificar) Data de Modificação`:datetime, `Data de Criação`:datetime, `Data do SLA`:datetime, `Término Real`:datetime, `Modificado Por`:string, `Proprietário`:string, `Status da Atividade`:string, `Solução`:string, `Referente`:string, `Etapa`:string, `Número da Ocorrência (Referente) (Ocorrência)`:string, `Assunto`:string, `Primeira Categoria (Referente) (Ocorrência)`:string, `Segunda Categoria (Referente) (Ocorrência)`:string, `Motivo (Referente) (Ocorrência)`:string, `Central de Atendimento (Referente) (Ocorrência)`:string, `Código Natura (Cliente) (Contato)`:string, `Número do documento (Cliente) (Contato)`:string, `Problema de Sistema (Referente) (Ocorrência)`:string, `Experience`:string, `Ticket Externo`:string, `Opção Menu (Referente) (Ocorrência)`:string, `Problema de Sistema FV (Referente) (Ocorrência)`:string, `Problema Site Natura (Referente) (Ocorrência)`:string

→ [52] União de linhas 8

## [10] INC Servicenow — LoadSql

_Descrição:_ Incidentes Experiência Brasil

Arquivo: `Servicenow - Incidentes Experiencia Brasil.xlsx` · aba `['incident (1)$']`

Campos: `number`:string, `opened_by`:string, `opened_at`:datetime, `short_description`:string, `caller_id`:string, `priority`:string, `state`:string, `category`:string, `assignment_group`:string, `assigned_to`:string, `sys_updated_on`:datetime, `sys_updated_by`:string, `contact_type`:string, `close_code`:string, `description`:string, `subcategory`:string, `work_end`:string, `work_start`:string, `reopened_time`:datetime, `closed_at`:datetime, `resolved_at`:datetime, `resolved_by`:string, `u_sla.business_percentage`:string, `hold_reason`:string, `business_service`:string, `u_jira`:string, `u_external_ticket`:string, `problem_id`:string, `due_date`:datetime, `close_notes`:string, `F31`:real, `F32`:real, `F33`:string, `F34`:string

→ [24] Tradução

## [11] Encerrados ServiceCloud — LoadSql

Arquivo: `Salesforce CF Encerrados.xlsx` · aba `[Base$]`

Campos: `Usuário que realizou alteração: Nome completo`:string, `Número do caso`:string, `Primeira Categoria`:string, `Segunda Categoria`:string, `Motivo`:string, `Etapa`:string, `Classificação do problema sistêmico`:string, `Aplicativo com problemas`:string, `Data/Hora de abertura`:datetime, `Data alvo SLA`:datetime, `Data/Hora de fechamento`:datetime, `Solução`:string, `Proprietário`:string, `Etapa 1`:string, `Status`:string, `Chamado`:string, `Caso pai: Chamado`:string, `Nome da conta: CPF`:string, `Id Caso Completo`:string, `Modificado pela última vez por: Nome completo`:string, `Data início`:datetime, `Data fim`:datetime, `Tipo de registro do caso`:string

Ações na leitura:

- Renomear `Número do caso` → `Número da Ocorrência (Referente) (Ocorrência)`
- Renomear `Status` → `Status da Atividade`
- Renomear `Primeira Categoria` → `Primeira Categoria (Referente) (Ocorrência)`
- Renomear `Segunda Categoria` → `Segunda Categoria (Referente) (Ocorrência)`
- Renomear `Motivo` → `Motivo (Referente) (Ocorrência)`
- Renomear `Data alvo SLA` → `Data do SLA`
- Renomear `Data/Hora de fechamento` → `Término Real`
- Renomear `Data/Hora de abertura` → `Data de Criação`

→ [25] Data Corte

## [12] Termino Real -Dynamics — LoadSql

Arquivo: `Termino Real.xlsx` · aba `['Termino Real - Tarefas Expe###$']`

Campos: `(Não Modificar) Tarefa`:string, `(Não Modificar) Soma de Verificação da Linha`:string, `(Não Modificar) Data de Modificação`:datetime, `Data de Criação`:datetime, `Data do SLA`:datetime, `Término Real`:datetime, `Modificado Por`:string, `Proprietário`:string, `Status da Atividade`:string, `Solução`:string, `Referente`:string, `Etapa`:string, `Número da Ocorrência (Referente) (Ocorrência)`:string, `Assunto`:string, `Primeira Categoria (Referente) (Ocorrência)`:string, `Segunda Categoria (Referente) (Ocorrência)`:string, `Motivo (Referente) (Ocorrência)`:string, `Central de Atendimento (Referente) (Ocorrência)`:string, `Código Natura (Cliente) (Contato)`:string, `Número do documento (Cliente) (Contato)`:string, `Experience`:string, `Ticket Externo`:string

→ [26] Clean 1

## [13] App Natura — LoadSql (grupo Resenhas Google)

Arquivo: `App Natura.xlsx` · aba `[reviews_reviews_net#natura#semp$]`

Campos: `Package Name`:string, `App Version Code`:integer, `App Version Name`:string, `Reviewer Language`:string, `Device`:string, `Review Submit Date and Time`:string, `Review Submit Millis Since Epoch`:integer, `Review Last Update Date and Time`:string, `Review Last Update Millis Since Epoch`:integer, `Star Rating`:integer, `Review Title`:string, `Review Text`:string, `Developer Reply Date and Time`:string, `Developer Reply Millis Since Epoch`:integer, `Developer Reply Text`:string, `Review Link`:string

→ [27] App Natura + App Avon

## [14] App Avon — LoadSql (grupo Resenhas Google)

Arquivo: `App_Avon.xlsx` · aba `[reviews_reviews_com#naturaeco#a$]`

Campos: `Package Name`:string, `App Version Code`:integer, `App Version Name`:string, `Reviewer Language`:string, `Device`:string, `Review Submit Date and Time`:string, `Review Submit Millis Since Epoch`:integer, `Review Last Update Date and Time`:string, `Review Last Update Millis Since Epoch`:integer, `Star Rating`:integer, `Review Title`:string, `Review Text`:string, `Developer Reply Date and Time`:string, `Developer Reply Millis Since Epoch`:integer, `Developer Reply Text`:string, `Review Link`:string

→ [27] App Natura + App Avon

## [15] Consultoria Natura — LoadSql (grupo Resenhas Google)

Arquivo: `Consultoria Natura.xlsx` · aba `[reviews_reviews_net#natura#cn_2$]`

Campos: `Package Name`:string, `App Version Code`:integer, `App Version Name`:string, `Reviewer Language`:string, `Device`:string, `Review Submit Date and Time`:string, `Review Submit Millis Since Epoch`:integer, `Review Last Update Date and Time`:string, `Review Last Update Millis Since Epoch`:integer, `Star Rating`:integer, `Review Title`:string, `Review Text`:string, `Developer Reply Date and Time`:string, `Developer Reply Millis Since Epoch`:integer, `Developer Reply Text`:string, `Review Link`:string

→ [39] App Natura + App Avon + CN

## [16] Força de Vendas — LoadSql (grupo Resenhas Google)

Arquivo: `Forca de Vendas.xlsx` · aba `[reviews_reviews_net#natura#fv_2$]`

Campos: `Package Name`:string, `App Version Code`:integer, `App Version Name`:string, `Reviewer Language`:string, `Device`:string, `Review Submit Date and Time`:string, `Review Submit Millis Since Epoch`:integer, `Review Last Update Date and Time`:string, `Review Last Update Millis Since Epoch`:integer, `Star Rating`:integer, `Review Title`:string, `Review Text`:string, `Developer Reply Date and Time`:string, `Developer Reply Millis Since Epoch`:integer, `Developer Reply Text`:string, `Review Link`:string

→ [49] App Natura + App Avon + CN + FV

## [17] Dados a partir de 2026 — SuperTransform

← [1] Criados CF Service Cloud  2026

1. Filtro de data `Data de Criação` (datetime): **a partir de 2026-01-01 00:00:00**, sem nulos

→ [28] Remover Duplicadas

## [18] Dados a partir 2026 — SuperTransform

← [2] Encerrados CF Service Cloud  2026

1. Filtro de data `Término Real` (datetime): **a partir de 2026-01-01 00:00:00**, sem nulos
2. Remapear `Status da Atividade`: "Finalizado" ← "✅ Finalizado"; "Cancelado" ← "❌ Cancelado"

→ [29] N1; [30] N2; [31] Retrabalho

## [19] Limpar 11 — SuperTransform

← [3] Base_GruposServiceNow_2209 2

→ [47] União de colunas 5

## [20] Limpar 3 — SuperTransform (grupo Resenhas AppSheets)

← [5] Resenhas AppSheets

1. Remapear `Aplicativo`: "Sempre Presente" ← "Natura CF"
2. Calcular `Data da Resposta New`:

```
MAKEDATETIME(
    DATE([Data da Resposta]), 
    MAKETIME(23, 59, 59)
)
```
3. Remover colunas: `Data da Resposta`
4. Renomear `Data da Resposta New` → `Data da Resposta`

→ [32] Regras do SLA

## [21] Limpar 9 — SuperTransform

← [6] Expurgo

1. Remover colunas: `Data Expurgo`, `Mês de Expurgo`, `Motivo`
2. Renomear `Número da Ocorrência (Referente) (Ocorrência)` → `Número`
3. Renomear `Nivel de Atendimento` → `Nivel Expurgo`

→ [70] União de colunas 7

## [22] Limpar 10 — SuperTransform

← [7] Criados ServiceCloud

1. Renomear `Classificação do problema sistêmico` → `Experience`
2. Remapear `Solução`: "Erro operacional Criado Em" ← "Erro operacional"
3. Remapear `Status da Atividade`: "Finalizado" ← "✅ Finalizado"; "Interface" ← "🔀 Interface"
4. Excluir `Status da Atividade` em ['"🤖 Sistema"', '"❌ Cancelado"', '"🔺Backoffice"']

→ [33] Remoção de Duplicadas

## [23] Remover Duplicada — SuperAggregate

← [8] CF Salesforce

**Agregar** agrupando por `Número da Ocorrência (Referente) (Ocorrência)`: MAX(`Aplicativo com problemas`), MAX(`Classificação do problema sistêmico`), MAX(`Data de Criação`), MAX(`Data do SLA`), MAX(`Etapa`), MAX(`Etapa 1`), MAX(`Motivo (Referente) (Ocorrência)`), MIN(`Primeira Categoria (Referente) (Ocorrência)`), MAX(`Proprietário`), MAX(`Segunda Categoria (Referente) (Ocorrência)`), MAX(`Solução`), MAX(`Status da Atividade`), MAX(`Término Real`), MAX(`Número de linhas (agregado)`), MIN(`Chamado`)

→ [34] Remoção de Emoji e duplicadas

## [24] Tradução — SuperTransform

← [10] INC Servicenow

1. Renomear `number` → `Número`
2. Renomear `opened_by` → `Aberto por`
3. Renomear `opened_at` → `Aberto em`
4. Renomear `short_description` → `Descrição Resumida`
5. Renomear `caller_id` → `Solicitante`
6. Renomear `priority` → `Prioridade`
7. Renomear `state` → `Status`
8. Renomear `category` → `Categoria`
9. Renomear `assignment_group` → `Grupo de Atribuição`
10. Renomear `assigned_to` → `Atribuído a`
11. Renomear `sys_updated_on` → `Atualizado em`
12. Renomear `sys_updated_by` → `Atualizado por`
13. Renomear `contact_type` → `Canal`
14. Renomear `close_code` → `Código de Resolução`
15. Renomear `description` → `Descrição`
16. Renomear `subcategory` → `Subcategoria`
17. Renomear `work_end` → `Término Real`
18. Renomear `work_start` → `Início Real`
19. Renomear `reopened_time` → `Última reabertura em`
20. Renomear `closed_at` → `Encerrado`
21. Renomear `resolved_at` → `Resolvido`
22. Renomear `resolved_by` → `Resolvido por`
23. Renomear `u_sla.business_percentage` → `% de tempo de neg. decorrido`
24. Renomear `hold_reason` → `Motivo para estar em espera`
25. Renomear `business_service` → `Serviço`
26. Renomear `u_jira` → `JIRA`
27. Renomear `u_external_ticket` → `Ticket Externo`
28. Renomear `problem_id` → `Problema`
29. Renomear `due_date` → `Prazo`
30. Renomear `close_notes` → `Anotações de Resolução`

→ [35] Faixa de Chamados

## [25] Data Corte — SuperTransform

_Descrição:_ A partir de Nov.25

← [11] Encerrados ServiceCloud

1. Renomear `Classificação do problema sistêmico` → `Experience`
2. Filtro de data `Término Real` (datetime): **a partir de 2025-11-01 00:00:00**, sem nulos
3. Excluir `Status da Atividade` em ['"❌ Cancelado"']
4. Remapear `Status da Atividade`: "Finalizado" ← "✅ Finalizado"

→ [36] Erro Operacional; [37] Remover Erro Operacional; [38] Clean 2

## [26] Clean 1 — SuperTransform

← [12] Termino Real -Dynamics

→ [61] União de linhas 6

## [27] App Natura + App Avon — SuperUnion (grupo Resenhas Google)

← [13] App Natura; [14] App Avon

**Union** das entradas acima (colunas com o mesmo nome se juntam; cria `Table Names`).

→ [39] App Natura + App Avon + CN

## [28] Remover Duplicadas — SuperAggregate

← [17] Dados a partir de 2026

**Agregar** agrupando por `Número da Ocorrência (Referente) (Ocorrência)`: MIN(`Aplicativo com problemas`), MIN(`Caso pai: Chamado`), MIN(`Chamado`), MIN(`Experience`), MIN(`Data de Criação`), MIN(`Data do SLA`), MIN(`Etapa`), MIN(`Etapa 1`), MIN(`Id Caso Completo`), MIN(`Motivo (Referente) (Ocorrência)`), MIN(`Primeira Categoria (Referente) (Ocorrência)`), MIN(`Proprietário`), MIN(`Segunda Categoria (Referente) (Ocorrência)`), MIN(`Solução`), MIN(`Status da Atividade`), MIN(`Término Real`), MAX(`Tipo de registro do caso`)

→ [40] Ajuste Status e Atividade

## [29] N1 — SuperTransform

← [18] Dados a partir 2026

1. Manter só `Chamado` em [None]
2. Manter só `Solução` em ['"Caso resolvido"', '"Resolvido"']
3. Calcular `Situação`:

```
STR("N1")
```

→ [41] Remover Duplicadas

## [30] N2 — SuperTransform

← [18] Dados a partir 2026

1. Manter só `Solução` em ['"Abrir chamado"']
2. Calcular `Situação`:

```
STR("N2")
```

→ [50] Unir Bases

## [31] Retrabalho — SuperTransform

← [18] Dados a partir 2026

1. Manter só `Solução` em ['"Erro operacional"']
2. Manter só `Status da Atividade` em ['"Finalizado"']
3. Calcular `Situação`:

```
STR("Retrabalho")
```

→ [42] Remover Duplicados

## [32] Regras do SLA — SuperTransform (grupo Resenhas AppSheets)

← [20] Limpar 3

1. Calcular `_Dia da Semana da Resposta`:

```
DATEPART('weekday', [Data da Resposta])
```
2. Calcular `_Hora da Resposta`:

```
DATEPART('hour', [Data da Resposta])
```
3. Calcular `Início da Contagem SLA (Brasil)`:

```
// Cenário 1: Fim de semana (Domingo=1 ou Sábado=7)
// Vai para a próxima Segunda às 08:00
IF [_Dia da Semana da Resposta] = 1 OR [_Dia da Semana da Resposta] = 7 THEN
    MAKEDATETIME(
        DATE(DATEADD('day', IF [_Dia da Semana da Resposta] = 1 THEN 1 ELSE 2 END, [Data da Resposta])),
        MAKETIME(8,0,0)
    )

// Cenário 2: Dia útil, mas antes das 08:00 (Madrugada)
// Vai para as 08:00 do mesmo dia
ELSEIF [_Hora da Resposta] < 8 THEN
    MAKEDATETIME(
        DATE([Data da Resposta]),
        MAKETIME(8,0,0)
    )

// Cenário 3: Dia útil, dentro do horário (08:00 em diante)
// Mantém a data original
ELSE
    DATETIME([Data da Resposta])
END
```
4. Calcular `Prazo SLA (Brasil)`:

```
// Adiciona 1 dia (24h). Se o início for Sexta, adiciona 3 dias para pular Sábado e Domingo.

IF DATEPART('weekday', [Início da Contagem SLA (Brasil)]) = 6 THEN
    // Se for Sexta-feira (6), soma 3 dias (Sáb, Dom, Seg)
    DATEADD('day', 3, [Início da Contagem SLA (Brasil)])
ELSE
    // Para qualquer outro dia, soma apenas 1 dia
    DATEADD('day', 1, [Início da Contagem SLA (Brasil)])
END
```
5. Calcular `Status SLA`:

```
// Lógica final: Compara a resposta (ou o momento atual) com o Prazo calculado.

// 1. Se a operação JÁ RESPONDEU (A data existe)
IF NOT ISNULL([Data da Resposta EXP]) THEN
    // Compara a data da resposta real com o Prazo
    IF [Data da Resposta EXP] <= [Prazo SLA (Brasil)] THEN
        "Dentro do SLA"
    ELSE
        "Fora do SLA"
    END

// 2. Se a operação AINDA NÃO respondeu (A data é nula)
ELSE
    // Verifica se o prazo já estourou em relação a AGORA (NOW)
    IF NOW() > [Prazo SLA (Brasil)] THEN
        "Fora do SLA" // Já passou do tempo e não responderam
    ELSE
        "Dentro do SLA" // Ainda não responderam, mas ainda têm tempo (está no prazo)
    END
END
```
6. Duplicar `Data da Resposta-1`:

```
[Data da Resposta]
```
7. Renomear `Data da Resposta-1` → `Data Avaliação`
8. Duplicar `Aplicativo-1`:

```
[Aplicativo]
```
9. Renomear `Aplicativo-1` → `Nome Aplicativo`
10. Duplicar `Classificação de Estrelas-1`:

```
[Classificação de Estrelas]
```
11. Renomear `Classificação de Estrelas-1` → `Star Rating`
12. Mudar tipo: `Star Rating` → integer

→ [43] Ajuste Nome App

## [33] Remoção de Duplicadas — SuperAggregate

← [22] Limpar 10

**Agregar** agrupando por `Número da Ocorrência (Referente) (Ocorrência)`: MIN(`Aplicativo com problemas`), MIN(`Caso pai: Chamado`), MIN(`Chamado`), MIN(`Data de Criação`), MIN(`Data do SLA`), MIN(`Etapa`), MIN(`Etapa 1`), MIN(`Experience`), MIN(`Motivo (Referente) (Ocorrência)`), MIN(`Primeira Categoria (Referente) (Ocorrência)`), MIN(`Proprietário`), MIN(`Segunda Categoria (Referente) (Ocorrência)`), MIN(`Solução`), MIN(`Status da Atividade`), MIN(`Término Real`), MAX(`Tipo de registro do caso`)

→ [44] Data Corte

## [34] Remoção de Emoji e duplicadas — SuperTransform

← [23] Remover Duplicada

1. Remapear `Status da Atividade`: "Finalizado" ← "✅ Finalizado"; "Cancelado" ← "❌ Cancelado"; "Interface" ← "🔀 Interface"; "Sistema" ← "🤖 Sistema"; "Backoffice" ← "🔺Backoffice"; "Cliente" ← "👤 Cliente"
2. Calcular `Tipo de registro do caso`:

```
"Atendimento CF"
```

→ [45] Criado em; [46] Termino real

## [35] Faixa de Chamados — SuperTransform

← [24] Tradução

1. Calcular `Dias Corridos`:

```
IF [Status] = "Cancelado" THEN
    DATEDIFF('day', [Aberto em], [Encerrado])
ELSEIF [Status] = "Resolvido" OR [Status] = "Encerrado" THEN
    DATEDIFF('day', [Aberto em], [Resolvido])
ELSE
    DATEDIFF('day', [Aberto em], TODAY())
END

```
2. Calcular `Faixa Dias`:

```
IF ISNULL([Dias Corridos]) THEN NULL
ELSEIF [Dias Corridos] < 1 THEN "NO MESMO DIA"
ELSEIF [Dias Corridos] < 2 THEN "01 DIA"
ELSEIF [Dias Corridos] < 3 THEN "02 DIAS"
ELSEIF [Dias Corridos] < 4 THEN "03 DIAS"
ELSEIF [Dias Corridos] < 11 THEN "04 A 10 DIAS"
ELSEIF [Dias Corridos] < 21 THEN "11 A 20 DIAS"
ELSEIF [Dias Corridos] < 31 THEN "21 A 30 DIAS"
ELSE "MAIS DE 30 DIAS"
END

```

→ [47] União de colunas 5

## [36] Erro Operacional — SuperTransform

← [25] Data Corte

1. Manter só `Solução` em ['"Erro operacional"']

→ [54] União de linhas 10

## [37] Remover Erro Operacional — SuperTransform

← [25] Data Corte

1. Excluir `Solução` em ['"Erro operacional"']

→ [48] Remover Duplicadas

## [38] Clean 2 — SuperTransform

← [25] Data Corte

1. Filtro:

```
[Número da Ocorrência (Referente) (Ocorrência)] = '03313681'
```

## [39] App Natura + App Avon + CN — SuperUnion (grupo Resenhas Google)

← [15] Consultoria Natura; [27] App Natura + App Avon

**Union** das entradas acima (colunas com o mesmo nome se juntam; cria `Table Names`).

→ [49] App Natura + App Avon + CN + FV

## [40] Ajuste Status e Atividade — SuperTransform

← [28] Remover Duplicadas

1. Remapear `Status da Atividade`: "Finalizado" ← "✅ Finalizado"; "Cancelado" ← "❌ Cancelado"; "Interface" ← "🔀 Interface"; "Backoffice" ← "🔺Backoffice"; "Sistema" ← "🤖 Sistema"
2. Remapear `Solução`: "Erro operacional Criado Em" ← "Erro operacional"
3. Calcular `Fonte`:

```
STR('Salesforce')
```

→ [52] União de linhas 8

## [41] Remover Duplicadas — SuperAggregate

← [29] N1

**Agregar** agrupando por `Número da Ocorrência (Referente) (Ocorrência)`: MIN(`Aplicativo com problemas`), MIN(`Caso pai: Chamado`), MIN(`Chamado`), MIN(`Data de Criação`), MIN(`Data do SLA`), MIN(`Etapa`), MIN(`Etapa 1`), MIN(`Experience`), MIN(`Id Caso Completo`), MIN(`Motivo (Referente) (Ocorrência)`), MIN(`Primeira Categoria (Referente) (Ocorrência)`), MIN(`Proprietário`), MIN(`Segunda Categoria (Referente) (Ocorrência)`), MIN(`Situação`), MIN(`Solução`), MIN(`Status da Atividade`), MIN(`Término Real`), MAX(`Tipo de registro do caso`)

→ [50] Unir Bases

## [42] Remover Duplicados — SuperAggregate

← [31] Retrabalho

**Agregar** agrupando por `Número da Ocorrência (Referente) (Ocorrência)`: MIN(`Aplicativo com problemas`), MIN(`Caso pai: Chamado`), MIN(`Chamado`), MIN(`Data de Criação`), MIN(`Data do SLA`), MIN(`Etapa`), MIN(`Etapa 1`), MIN(`Experience`), MIN(`Id Caso Completo`), MIN(`Motivo (Referente) (Ocorrência)`), MIN(`Primeira Categoria (Referente) (Ocorrência)`), MIN(`Proprietário`), MIN(`Segunda Categoria (Referente) (Ocorrência)`), MIN(`Situação`), MIN(`Solução`), MIN(`Status da Atividade`), MIN(`Término Real`), MAX(`Tipo de registro do caso`)

→ [50] Unir Bases

## [43] Ajuste Nome App — SuperTransform (grupo Resenhas AppSheets)

← [32] Regras do SLA

1. Calcular `App Nome`:

```
IF ([Aplicativo] = "Google Play" OR [Aplicativo] = "Applestore") AND ([Loja] = "Google Play" OR [Loja] = "Applestore")
THEN "Não Identificado"

ELSEIF ([Aplicativo] = "Google Play" OR [Aplicativo] = "Applestore")
THEN 
    IF ISNULL([Loja]) OR [Loja] = "" OR [Loja] = "Google Play" OR [Loja] = "Applestore" 
    THEN "Não Identificado" 
    ELSE [Loja] 
    END

ELSEIF ([Loja] = "Google Play" OR [Loja] = "Applestore")
THEN 
    IF ISNULL([Aplicativo]) OR [Aplicativo] = "" OR [Aplicativo] = "Google Play" OR [Aplicativo] = "Applestore" 
    THEN "Não Identificado" 
    ELSE [Aplicativo] 
    END

ELSE "Não Identificado"
END
```
2. Remapear `App Nome`: "Sempre Presente" ← "Natura CF"

→ [51] Resenhas EXP BR AppSheets

## [44] Data Corte — SuperTransform

_Descrição:_ A partir de Nov.2025 até Dez2025

← [33] Remoção de Duplicadas

1. Filtro de data `Data de Criação` (datetime): **entre 2025-11-01 00:00:00 e 2025-12-31 00:00:00**, sem nulos

→ [52] União de linhas 8

## [45] Criado em — SuperTransform

_Descrição:_ Até 31/10/25

← [34] Remoção de Emoji e duplicadas

1. Renomear `Classificação do problema sistêmico` → `Experience`
2. Remapear `Solução`: "Erro operacional Criado Em" ← "Erro operacional"
3. Filtro de data `Data de Criação` (datetime): **até 2025-10-31 00:00:00**, sem nulos

→ [52] União de linhas 8

## [46] Termino real — SuperTransform

_Descrição:_ Até 31/10/2025

← [34] Remoção de Emoji e duplicadas

1. Excluir `Status da Atividade` em ['"Interface"']
2. Renomear `Classificação do problema sistêmico` → `Experience`
3. Filtro de data `Término Real` (datetime): **até 2025-10-31 00:00:00**, sem nulos

→ [61] União de linhas 6

## [47] União de colunas 5 — SuperJoin

← [19] Limpar 11 (Left); [35] Faixa de Chamados (Right)

**Join right**: esquerda = [19] Limpar 11, direita = [35] Faixa de Chamados

Condição: `esq.[Grupo de atribuição - no SErvice Now] == dir.[Grupo de Atribuição]`

→ [53] EXPBR - Chamados Servicenow

## [48] Remover Duplicadas — SuperAggregate

← [37] Remover Erro Operacional

**Agregar** agrupando por `Número da Ocorrência (Referente) (Ocorrência)`: MIN(`Aplicativo com problemas`), MIN(`Caso pai: Chamado`), MIN(`Chamado`), MIN(`Data de Criação`), MIN(`Data do SLA`), MIN(`Etapa`), MIN(`Etapa 1`), MIN(`Experience`), MIN(`Motivo (Referente) (Ocorrência)`), MIN(`Primeira Categoria (Referente) (Ocorrência)`), MIN(`Proprietário`), MIN(`Segunda Categoria (Referente) (Ocorrência)`), MIN(`Solução`), MIN(`Status da Atividade`), MIN(`Término Real`), MIN(`Número de linhas (agregado)`), MAX(`Tipo de registro do caso`)

→ [54] União de linhas 10

## [49] App Natura + App Avon + CN + FV — SuperUnion (grupo Resenhas Google)

← [39] App Natura + App Avon + CN; [16] Força de Vendas

**Union** das entradas acima (colunas com o mesmo nome se juntam; cria `Table Names`).

→ [55] SLA Resenhas

## [50] Unir Bases — SuperUnion

← [42] Remover Duplicados; [30] N2; [41] Remover Duplicadas

**Union** das entradas acima (colunas com o mesmo nome se juntam; cria `Table Names`).

1. Remover colunas: `Table Names`

→ [56] Limpar 11

## [51] Resenhas EXP BR AppSheets — PublishExtract (grupo Resenhas AppSheets)

← [43] Ajuste Nome App

**Saída:** `4. DATASOURCES/Resenhas EXP BR AppSheets`

## [52] União de linhas 8 — SuperUnion

← [44] Data Corte; [45] Criado em; [9] Criados em  - Dynamics; [40] Ajuste Status e Atividade

**Union** das entradas acima (colunas com o mesmo nome se juntam; cria `Table Names`).

1. Renomear `Table Names` → `Fonte`
2. Remapear `Fonte`: "Dynamics" ← "Criados em  - Tarefas Exper###"; "Salesforce" ← "report1757960791997"
3. Remapear `Fonte`: "Salesforce" ← "Base"
4. Remover colunas: `Número de linhas (agregado)`
5. Remapear `Fonte`: "Salesforce" ← "Base-1"

→ [57] SLA CLIENTE, SLA EXPERIENCIA

## [53] EXPBR - Chamados Servicenow — PublishExtract

← [47] União de colunas 5

**Saída:** `4. DATASOURCES/EXPBR - Chamados Servicenow`

## [54] União de linhas 10 — SuperUnion

← [48] Remover Duplicadas; [36] Erro Operacional

**Union** das entradas acima (colunas com o mesmo nome se juntam; cria `Table Names`).

1. Remover colunas: `Table Names`
2. Remover colunas: `Número de linhas (agregado)`

→ [58] Até 2025

## [55] SLA Resenhas — SuperTransform (grupo Resenhas Google)

← [49] App Natura + App Avon + CN + FV

1. Calcular `Elegibilidade SLA`:

```
// Verifica se o campo de texto da resenha está vazio ou nulo.
IF ISNULL([Review Text]) OR [Review Text] = "" THEN
    'Não Aplicável'
ELSE
    'Aplicável'
END
```
2. Remover colunas: `Table Names-2`, `Table Names-1`, `Table Names`
3. Calcular `Data Avaliação`:

```
DATETIME(
    MID([Review Submit Date and Time], 1, 10) + " " +
    MID([Review Submit Date and Time], 12, 8)
)

```
4. Calcular `Data da Resposta EXP`:

```
DATETIME(
    MID([Developer Reply Date and Time], 1, 10) + " " +
    MID([Developer Reply Date and Time], 12, 8)
)

```
5. Calcular `Data Atualização da Avaliação`:

```
DATETIME(
    MID([Review Last Update Date and Time], 1, 10) + " " +
    MID([Review Last Update Date and Time], 12, 8)
)

```
6. Calcular `Prazo SLA`:

```
IF [Star Rating] >= 1 AND [Star Rating] <= 3 THEN 1
ELSEIF [Star Rating] >= 4 AND [Star Rating] <= 5 THEN 5
ELSE 0
END
```
7. Calcular `Status SLA`:

```
// FÓRMULA DEFINITIVA COM CASE/WHEN PARA DIAS DA SEMANA
IF ISNULL([Data da Resposta EXP]) THEN
    // Caso 1: Sem resposta do EXP
    IF [Star Rating] >= 1 AND [Star Rating] <= 3 THEN
        IF DATEDIFF('day', DATE([Data Avaliação]), TODAY()) > 
           CASE DATEPART('weekday', [Data Avaliação])
               WHEN 6 THEN 2  // Sábado
               WHEN 7 THEN 1  // Domingo
               ELSE 1         // Dias úteis
           END THEN
            "Fora do SLA"
        ELSE
            "Dentro do SLA"
        END
    ELSEIF [Star Rating] >= 4 AND [Star Rating] <= 5 THEN
        IF DATEDIFF('day', DATE([Data Avaliação]), TODAY()) > 5 THEN
            "Fora do SLA"
        ELSE
            "Dentro do SLA"
        END
    ELSE
        "Dentro do SLA"
    END
ELSE
    // Caso 2: Com resposta do EXP
    IF NOT ISNULL([Data Atualização da Avaliação]) AND [Data Atualização da Avaliação] > [Data da Resposta EXP] THEN
        // Subcaso 2.1: Usuário replicou
        IF [Star Rating] >= 1 AND [Star Rating] <= 3 THEN
            IF DATEDIFF('day', DATE([Data Atualização da Avaliação]), TODAY()) > 1 THEN
                "Fora do SLA"
            ELSE
                "Dentro do SLA"
            END
        ELSEIF [Star Rating] >= 4 AND [Star Rating] <= 5 THEN
            IF DATEDIFF('day', DATE([Data Atualização da Avaliação]), TODAY()) > 5 THEN
                "Fora do SLA"
            ELSE
                "Dentro do SLA"
            END
        ELSE
            "Dentro do SLA"
        END
    ELSE
        // Subcaso 2.2: Última interação foi do EXP
        IF [Star Rating] >= 1 AND [Star Rating] <= 3 THEN
            IF [Data da Resposta EXP] > 
   DATETRUNC('day',
       DATEADD('day', 
           CASE DATEPART('weekday', [Data Avaliação])
               WHEN 6 THEN 2
               WHEN 7 THEN 1
               ELSE 1
           END, 
       [Data Avaliação])
   ) + 86399 THEN
    "Fora do SLA"

            ELSE
                "Dentro do SLA"
            END
        ELSEIF [Star Rating] >= 4 AND [Star Rating] <= 5 THEN
            IF DATE([Data da Resposta EXP]) > DATEADD('day', 5, DATE([Data Avaliação])) THEN
                "Fora do SLA"
            ELSE
                "Dentro do SLA"
            END
        ELSE
            "Dentro do SLA"
        END
    END
END
```
8. Calcular `Status SLA 2`:

```
// Passo 1: Primeiro, verifica se o SLA é aplicável (se tem comentário).
IF [Elegibilidade SLA] = 'Não Aplicável' THEN
    'Não Aplicável'

// Passo 2: Se for aplicável, executa toda a lógica de SLA original.
ELSEIF ISNULL([Data da Resposta EXP]) THEN
    // Caso 1: Sem resposta do EXP
    IF [Star Rating] >= 1 AND [Star Rating] <= 3 THEN
        IF DATEDIFF('day', DATE([Data Avaliação]), TODAY()) > 
            CASE DATEPART('weekday', [Data Avaliação])
                WHEN 6 THEN 2  // Sábado
                WHEN 7 THEN 1  // Domingo
                ELSE 1          // Dias úteis
            END THEN
            "Fora do SLA"
        ELSE
            "Dentro do SLA"
        END
    ELSEIF [Star Rating] >= 4 AND [Star Rating] <= 5 THEN
        IF DATEDIFF('day', DATE([Data Avaliação]), TODAY()) > 5 THEN
            "Fora do SLA"
        ELSE
            "Dentro do SLA"
        END
    ELSE
        "Dentro do SLA"
    END
ELSE
    // Caso 2: Com resposta do EXP
    IF NOT ISNULL([Data Atualização da Avaliação]) AND [Data Atualização da Avaliação] > [Data da Resposta EXP] THEN
        // Subcaso 2.1: Usuário replicou
        IF [Star Rating] >= 1 AND [Star Rating] <= 3 THEN
            IF DATEDIFF('day', DATE([Data Atualização da Avaliação]), TODAY()) > 1 THEN
                "Fora do SLA"
            ELSE
                "Dentro do SLA"
            END
        ELSEIF [Star Rating] >= 4 AND [Star Rating] <= 5 THEN
            IF DATEDIFF('day', DATE([Data Atualização da Avaliação]), TODAY()) > 5 THEN
                "Fora do SLA"
            ELSE
                "Dentro do SLA"
            END
        ELSE
            "Dentro do SLA"
        END
    ELSE
        // Subcaso 2.2: Última interação foi do EXP
        IF [Star Rating] >= 1 AND [Star Rating] <= 3 THEN
            IF [Data da Resposta EXP] > 
DATETRUNC('day',
    DATEADD('day', 
        CASE DATEPART('weekday', [Data Avaliação])
            WHEN 6 THEN 2
            WHEN 7 THEN 1
            ELSE 1
        END, 
    [Data Avaliação])
) + 86399 THEN
 "Fora do SLA"

            ELSE
                "Dentro do SLA"
            END
        ELSEIF [Star Rating] >= 4 AND [Star Rating] <= 5 THEN
            IF DATE([Data da Resposta EXP]) > DATEADD('day', 5, DATE([Data Avaliação])) THEN
                "Fora do SLA"
            ELSE
                "Dentro do SLA"
            END
        ELSE
            "Dentro do SLA"
        END
    END
END
```

→ [59] Nome Apps

## [56] Limpar 11 — SuperTransform

← [50] Unir Bases

1. Calcular `Fonte`:

```
STR("Salesforce")
```

→ [61] União de linhas 6

## [57] SLA CLIENTE, SLA EXPERIENCIA — SuperTransform

← [52] União de linhas 8

1. Calcular `DIAS CORRIDOS CLIENTE`:

```
DATEDIFF('day', [Término Real], [Data do SLA])
```
2. Calcular `SEGUNDOS CORRIDOS EXPERIENCIA`:

```
DATEDIFF('second', [Data de Criação], [Término Real])

```
3. Calcular `SLA Cliente`:

```
IF ISNULL([Término Real]) THEN "BACKLOG"
ELSEIF [DIAS CORRIDOS CLIENTE] >= 0 THEN "DENTRO DO PRAZO"
ELSE "FORA DO PRAZO" END
```
4. Calcular `SLA Experiência 24 Horas`:

```
IF ISNULL([Término Real]) THEN "BACKLOG"
ELSEIF [SEGUNDOS CORRIDOS EXPERIENCIA] <= 86400 THEN "DENTRO DO PRAZO"
ELSE "FORA DO PRAZO" END
```
5. Calcular `Nivel de Atendimento`:

```
// 1. Primeiro, verifica as condições da coluna [Etapa] que resultam em N1
IF [Etapa] = "Análise Aplicativo Consultoria"
OR [Etapa] = "Análise Aplicativo Força de Vendas"
OR [Etapa] = "Análise Aplicativo Natura Vendas"
OR [Etapa] = "Análise de espaço digital"
OR [Etapa] = "Analise de liberação do espaço"
OR [Etapa] = "Análise de senha"
OR [Etapa] = "Análise de Vale-Troca"
OR [Etapa] = "Análise pedido espaço default"
OR [Etapa] = "Análise Plano de crescimento"
OR [Etapa] = "Análise Site Consultoria"
OR [Etapa] = "Análise Site Força de Vendas"
OR [Etapa] = "Análise Site Natura"
OR [Etapa] = "Cancelamento de Pedido"
OR [Etapa] = "Aguardando N3 Experiência"
THEN "N1"

// 2. Verifica as condições da coluna [Etapa] que resultam em N2
ELSEIF [Etapa] = "Acompanhamento tecnologia - espaço digital"
OR [Etapa] = "Análise Correção Sistema - SM"
OR [Etapa] = "Abertura do chamado"
THEN "N2"

// 3. Se nenhuma condição da [Etapa] for atendida, verifica a coluna [Solução]
ELSEIF [Solução] = "Abrir chamado"
OR [Solução] = "Card criado no Jira"
THEN "N2"

// 4. Se nenhuma das condições acima for atendida, o resultado padrão é "N1"
ELSE "N1"
END
```
6. Calcular `Faixa Tempo Solucao SLA Experiencia`:

```
IF [SEGUNDOS CORRIDOS EXPERIENCIA] <= 18000 THEN "ATÉ 5 HORAS"
ELSEIF [SEGUNDOS CORRIDOS EXPERIENCIA] <= 86400 THEN "ATÉ 24 HORAS"
ELSE "ACIMA DE 24 HORAS" END
```
7. Calcular `SLA 5 Horas`:

```
IF ISNULL([Término Real]) THEN "BACKLOG"
ELSEIF [SEGUNDOS CORRIDOS EXPERIENCIA] <= 18000 THEN "DENTRO DO PRAZO"
ELSE "FORA DO PRAZO" END
```
8. Remapear `Solução`: "Solicitação não procedente - Desvio operacional Criados Em" ← "Solicitação não procedente - Desvio operacional"
9. Remapear `Fonte`: "Salesforce" ← "Base-2"

→ [60] Join 1

## [58] Até 2025 — SuperTransform

← [54] União de linhas 10

1. Filtro de data `Término Real` (datetime): **entre 2025-10-27 00:00:00 e 2025-12-31 00:00:00**, sem nulos

→ [61] União de linhas 6

## [59] Nome Apps — SuperTransform (grupo Resenhas Google)

← [55] SLA Resenhas

1. Remapear `Package Name`: "App Avon" ← "com.naturaeco.app.avon"; "App Consultoria Natura" ← "Consultoria Natura", "net.natura.cn"; "App Força de Vendas" ← "Força de Vendas", "net.natura.fv"; "App Sempre Presente" ← "Sempre Presente", "net.natura.semprepresente"
2. Renomear `Package Name` → `Nome Aplicativo`

→ [62] Resenhas Brasil

## [60] Join 1 — SuperJoin

← [4] Tribos Dynamics (Left); [57] SLA CLIENTE, SLA EXPERIENCIA (Right)

**Join right**: esquerda = [4] Tribos Dynamics, direita = [57] SLA CLIENTE, SLA EXPERIENCIA

Condição: `esq.[Experience Tribos] == dir.[Experience]`

→ [63] Fase, Tipo Protocolo

## [61] União de linhas 6 — SuperUnion

← [56] Limpar 11; [58] Até 2025; [46] Termino real; [26] Clean 1

**Union** das entradas acima (colunas com o mesmo nome se juntam; cria `Table Names`).

1. Renomear `Table Names` → `Fonte`
2. Remapear `Fonte`: "Dynamics" ← "Termino Real - Tarefas Expe###"; "Salesforce" ← "report1757960791997", "Base"
3. Remover colunas: `Número de linhas (agregado)`
4. Remapear `Fonte`: "Salesforce" ← "Base-1", "Base-2"

→ [64] União de colunas 3

## [62] Resenhas Brasil — PublishExtract (grupo Resenhas Google)

← [59] Nome Apps

**Saída:** `4. DATASOURCES/Resenhas Brasil`

## [63] Fase, Tipo Protocolo — SuperTransform

← [60] Join 1

1. Calcular `Fase`:

```
// 1. Primeiro, verifica as condições da coluna [Etapa]
IF [Etapa] = "Análise Aplicativo Consultoria"
OR [Etapa] = "Análise Aplicativo Força de Vendas"
OR [Etapa] = "Análise Aplicativo Natura Vendas"
OR [Etapa] = "Análise de espaço digital"
OR [Etapa] = "Analise de liberação do espaço"
OR [Etapa] = "Análise de senha"
OR [Etapa] = "Análise de Vale-Troca"
OR [Etapa] = "Análise pedido espaço default"
OR [Etapa] = "Análise Plano de crescimento"
OR [Etapa] = "Análise Site Consultoria"
OR [Etapa] = "Análise Site Força de Vendas"
OR [Etapa] = "Análise Site Natura"
OR [Etapa] = "Cancelamento de Pedido"
OR [Etapa] = "Aguardando N3 Experiência"
THEN "Fase 1"

ELSEIF [Etapa] = "Acompanhamento tecnologia - espaço digital"
OR [Etapa] = "Análise Correção Sistema - SM"
OR [Etapa] = "Abertura do chamado"
THEN "Fase 2"

// 2. Se nenhuma condição da [Etapa] for atendida, verifica a coluna [Solução]
ELSEIF [Solução] = "Abrir chamado"
OR [Solução] = "Card criado no Jira"
THEN "Fase 2"

// 3. Se nenhuma das condições acima for atendida, o resultado padrão é "Fase 1"
ELSE "Fase 1"
END
```
2. Calcular `Tipo Protocolo`:

```
IF [Central de Atendimento (Referente) (Ocorrência)] = "MÍDIAS SOCIAIS"
OR [Central de Atendimento (Referente) (Ocorrência)] = "REDE NATURA"
OR [Central de Atendimento (Referente) (Ocorrência)] = "Avon Ecomm"
OR [Central de Atendimento (Referente) (Ocorrência)] = "SNAC"
THEN "Protocolos CF"

ELSEIF [Central de Atendimento (Referente) (Ocorrência)] = "Ato - Atendimento Líder"
OR [Central de Atendimento (Referente) (Ocorrência)] = "CAN"
OR [Central de Atendimento (Referente) (Ocorrência)] = "CIN"
OR [Central de Atendimento (Referente) (Ocorrência)] = "Varejo"
THEN "Protocolos CB"

ELSEIF [Fonte] = "Salesforce" AND [Tipo de registro do caso] = "Atendimento CF"
THEN "Protocolos CF"

ELSEIF [Fonte] = "Salesforce" AND [Tipo de registro do caso] = "Atendimento Franquias"
THEN "Franquias"

ELSE "Outro"
END
```

→ [65] Limpar 5

## [64] União de colunas 3 — SuperJoin

← [4] Tribos Dynamics (Left); [61] União de linhas 6 (Right)

**Join right**: esquerda = [4] Tribos Dynamics, direita = [61] União de linhas 6

Condição: `esq.[Experience Tribos] == dir.[Experience]`

→ [66] Ajuste dos dias 24, 25 e 31

## [65] Limpar 5 — SuperTransform

← [63] Fase, Tipo Protocolo

→ [67] Limpar 2

## [66] Ajuste dos dias 24, 25 e 31 — SuperTransform

← [64] União de colunas 3

1. Calcular `Data de Criação2`:

```
// Ajuste Feriados 2025 (Apenas Criação - Mantendo Horário)
IF YEAR([Data de Criação]) = 2025 AND MONTH([Data de Criação]) = 12 AND (DAY([Data de Criação]) = 24 OR DAY([Data de Criação]) = 25) THEN
    // Se criado dia 24 ou 25, move para dia 26 mantendo a hora exata
    DATEADD('day', DATEDIFF('day', DATETRUNC('day', [Data de Criação]), #2025-12-26#), [Data de Criação])

ELSEIF YEAR([Data de Criação]) = 2025 AND MONTH([Data de Criação]) = 12 AND DAY([Data de Criação]) = 31 THEN
    // Se criado dia 31, move para dia 02/01/2026 mantendo a hora exata
    DATEADD('day', DATEDIFF('day', DATETRUNC('day', [Data de Criação]), #2026-01-02#), [Data de Criação])

ELSE
    // Mantém dia 30 e todos os outros dias inalterados
    [Data de Criação]
END
```
2. Remover colunas: `Data de Criação`
3. Renomear `Data de Criação2` → `Dia Data de Criação`
4. Renomear `Término Real` → `Dia Término Real`
5. Renomear `Dia Data de Criação` → `Data de Criação`
6. Renomear `Dia Término Real` → `Término Real`

→ [68] SLA CLIENTE, SLA EXPERIENCIA

## [67] Limpar 2 — SuperTransform

← [65] Limpar 5

1. Remover colunas: `Problema de Sistema (Referente) (Ocorrência)`
2. Remover colunas: `Opção Menu (Referente) (Ocorrência)`
3. Remover colunas: `Problema de Sistema FV (Referente) (Ocorrência)`
4. Remover colunas: `Problema Site Natura (Referente) (Ocorrência)`
5. Calcular `Base`:

```
IF ISNULL([Número da Ocorrência (Referente) (Ocorrência)]) THEN "" ELSE "Criado em" END
```
6. Calcular `Data`:

```
[Data de Criação]
```

→ [73] União de linhas 1

## [68] SLA CLIENTE, SLA EXPERIENCIA — SuperTransform

← [66] Ajuste dos dias 24, 25 e 31

1. Calcular `DIAS CORRIDOS CLIENTE`:

```
DATEDIFF('day', [Término Real], [Data do SLA])

```
2. Calcular `SEGUNDOS CORRIDOS EXPERIENCIA`:

```
DATEDIFF('second', [Data de Criação], [Término Real])

```
3. Calcular `SLA Cliente`:

```
IF ISNULL([Término Real]) THEN "BACKLOG"
ELSEIF [Término Real] > [Data do SLA] THEN "FORA DO PRAZO"
ELSE "DENTRO DO PRAZO" END

```
4. Calcular `SLA Experiência`:

```
IF ISNULL([Término Real]) THEN "BACKLOG"
ELSEIF [SEGUNDOS CORRIDOS EXPERIENCIA] <= 86400 THEN "DENTRO DO PRAZO"
ELSE "FORA DO PRAZO" END

```
5. Calcular `Nivel de Atendimento`:

```
// 1. Primeiro, verifica as condições da coluna [Etapa] que resultam em N1
IF [Etapa] = "Análise Aplicativo Consultoria"
OR [Etapa] = "Análise Aplicativo Força de Vendas"
OR [Etapa] = "Análise Aplicativo Natura Vendas"
OR [Etapa] = "Análise de espaço digital"
OR [Etapa] = "Analise de liberação do espaço"
OR [Etapa] = "Análise de senha"
OR [Etapa] = "Análise de Vale-Troca"
OR [Etapa] = "Análise pedido espaço default"
OR [Etapa] = "Análise Plano de crescimento"
OR [Etapa] = "Análise Site Consultoria"
OR [Etapa] = "Análise Site Força de Vendas"
OR [Etapa] = "Análise Site Natura"
OR [Etapa] = "Cancelamento de Pedido"
OR [Etapa] = "Aguardando N3 Experiência"
THEN "N1"

// 2. Verifica as condições da coluna [Etapa] que resultam em N2
ELSEIF [Etapa] = "Acompanhamento tecnologia - espaço digital"
OR [Etapa] = "Análise Correção Sistema - SM"
OR [Etapa] = "Abertura do chamado"
THEN "N2"

// 3. Se nenhuma condição da [Etapa] for atendida, verifica a coluna [Solução]
ELSEIF [Solução] = "Abrir chamado"
OR [Solução] = "Card criado no Jira"
THEN "N2"

// 4. Verificação da coluna [Chamado]
// Se [Chamado] estiver preenchida (não for nula e não for vazia), retorna "N2"
ELSEIF NOT ISNULL([Chamado]) AND [Chamado] <> "" THEN
    "N2"

// 5. Se nenhuma das condições acima for atendida, o resultado padrão é "N1"
ELSE "N1"
END
```
6. Calcular `Faixa Tempo Solucao SLA Experiencia`:

```
IF [SEGUNDOS CORRIDOS EXPERIENCIA] <= 18000 THEN "ATÉ 5 HORAS"
ELSEIF [SEGUNDOS CORRIDOS EXPERIENCIA] <= 86400 THEN "ATÉ 24 HORAS"
ELSE "ACIMA DE 24 HORAS" END

```
7. Calcular `SLA 5 Horas`:

```
IF ISNULL([Término Real]) THEN "BACKLOG"
ELSEIF [SEGUNDOS CORRIDOS EXPERIENCIA] <= 18000 THEN "DENTRO DO PRAZO"
ELSE "FORA DO PRAZO" END
```

→ [69] Ajuste Horas Uteis

## [69] Ajuste Horas Uteis — SuperTransform

← [68] SLA CLIENTE, SLA EXPERIENCIA

1. Calcular `_Dia da Semana Criação`:

```
DATEPART('weekday', [Data de Criação])
```
2. Calcular `_Dia da Semana Termino`:

```
DATEPART('weekday', [Término Real])
```
3. Calcular `_Data Fim Referência`:

```
IF ISNULL([Término Real]) THEN NOW()
ELSE [Término Real]
END
```
4. Calcular `_Início Útil`:

```
// Ajusta a data de criação para o início do próximo período útil, se necessário

// CENÁRIO 1: Tarefa criada em um fim de semana (Sábado ou Domingo)
IF [_Dia da Semana Criação] = 1 OR [_Dia da Semana Criação] = 7 THEN
    MAKEDATETIME(
        DATE(DATEADD('day', IF [_Dia da Semana Criação] = 1 THEN 1 ELSE 2 END, [Data de Criação])),
        MAKETIME(8,0,0)
    )

// CENÁRIO 2: Tarefa criada em dia de semana, mas ANTES das 08:00
ELSEIF DATEPART('hour', [Data de Criação]) < 8 THEN
    MAKEDATETIME(DATE([Data de Criação]), MAKETIME(8,0,0))

// CENÁRIO 3: Tarefa criada em dia de semana, mas DEPOIS das 22:00
ELSEIF DATEPART('hour', [Data de Criação]) >= 22 THEN
    MAKEDATETIME(
        DATE(DATEADD('day', IF [_Dia da Semana Criação] = 6 THEN 3 ELSE 1 END, [Data de Criação])),
        MAKETIME(8,0,0)
    )

// CENÁRIO 4: Tarefa criada dentro do horário de trabalho
ELSE
    [Data de Criação]
END
```
5. Calcular `_Término Útil`:

```
// Ajusta a data de término para o fim do período útil anterior, se necessário

// CENÁRIO 1: Tarefa terminada em um fim de semana (Sábado ou Domingo)
IF [_Dia da Semana Termino] = 1 OR [_Dia da Semana Termino] = 7 THEN
    MAKEDATETIME(
        DATE(DATEADD('day', IF [_Dia da Semana Termino] = 1 THEN -2 ELSE -1 END, [Término Real])),
        MAKETIME(22,0,0)
    )

// CENÁRIO 2: Tarefa terminada em dia de semana, mas ANTES das 08:00

ELSEIF DATEPART('hour', [Término Real]) < 8 THEN
    MAKEDATETIME(
        DATE(DATEADD('day', IF [_Dia da Semana Termino] = 2 THEN -3 ELSE -1 END, [Término Real])),
        MAKETIME(22,0,0)
    )

// CENÁRIO 3: Tarefa terminada em dia de semana, mas DEPOIS das 22:00
ELSEIF DATEPART('hour', [Término Real]) >= 22 THEN
    // Se terminou depois das 22h, consideramos o "teto" das 22h do mesmo dia
    MAKEDATETIME(DATE([Término Real]), MAKETIME(22,0,0))

// CENÁRIO 4: Tarefa terminada dentro do horário de trabalho
ELSE
    [Término Real]
END
```
6. Calcular `Segundos Úteis Decorridos`:

```
// CASO 1: Tarefa iniciou e terminou no MESMO DIA.
IF DATE([_Início Útil]) = DATE([_Término Útil]) THEN
    DATEDIFF('second', [_Início Útil], [_Término Útil])

// CASO 2: Tarefa durou VÁRIOS DIAS.
ELSE
    // Parte A: Segundos trabalhados no primeiro dia
    (DATEDIFF('second',
              [_Início Útil],
              MAKEDATETIME(DATE([_Início Útil]), MAKETIME(22,0,0)))
    )
    +
    // Parte B: Segundos trabalhados no último dia
    (DATEDIFF('second',
              MAKEDATETIME(DATE([_Término Útil]), MAKETIME(8,0,0)),
              [_Término Útil])
    )
    +
    // Parte C: Segundos de todos os dias úteis inteiros entre o início e o fim
    (
     // Esta parte calcula o número de dias úteis inteiros
     (DATEDIFF('day', [_Início Útil], [_Término Útil]) - 1)
     -
     (DATEDIFF('week', [_Início Útil], [_Término Útil]) * 2)
     -
     (IF DATEPART('weekday', [_Início Útil]) = 1 THEN 1 ELSE 0 END) // Corrige se começou Domingo
     +
     (IF DATEPART('weekday', [_Término Útil]) = 1 THEN 1 ELSE 0 END)  // Corrige se terminou Domingo

    ) * (14 * 3600) // Multiplica os dias úteis por 14 horas * 3600 segundos
END
```
7. Renomear `SLA 5 Horas` → `SLA 5 Horas - OLD`
8. Renomear `SLA Experiência` → `SLA Experiência - OLD`
9. Calcular `SLA Experiência`:

```
IF ISNULL([Término Real]) THEN "BACKLOG"
ELSEIF [Segundos Úteis Decorridos] <= 86400 THEN "DENTRO DO PRAZO"
ELSE "FORA DO PRAZO" END

```
10. Calcular `SLA 5 Horas`:

```
IF ISNULL([Término Real]) THEN "BACKLOG"
ELSEIF [Segundos Úteis Decorridos] <= 18000 THEN "DENTRO DO PRAZO"
ELSE "FORA DO PRAZO" END
```

→ [70] União de colunas 7

## [70] União de colunas 7 — SuperJoin

← [69] Ajuste Horas Uteis (Left); [21] Limpar 9 (Right)

**Join left**: esquerda = [69] Ajuste Horas Uteis, direita = [21] Limpar 9

Condição: `esq.[Número da Ocorrência (Referente) (Ocorrência)] == dir.[Número]`

→ [71] Limpar 10

## [71] Limpar 10 — SuperTransform

← [70] União de colunas 7

1. Calcular `Nivel`:

```
IF ISNULL([Nivel Expurgo]) THEN
	[Nivel de Atendimento]
ELSE
	[Nivel Expurgo] 
END
```
2. Renomear `Nivel de Atendimento` → `Nivel de Atendimento old`
3. Renomear `Nivel` → `Nivel de Atendimento`
4. Remover colunas: `Nivel de Atendimento old`
5. Remover colunas: `Nivel Expurgo`

→ [72] FASE, Tipo Protocolo

## [72] FASE, Tipo Protocolo — SuperTransform

← [71] Limpar 10

1. Calcular `Fase`:

```
// 1. Primeiro, verifica as condições da coluna [Etapa]
IF [Etapa] = "Análise Aplicativo Consultoria"
OR [Etapa] = "Análise Aplicativo Força de Vendas"
OR [Etapa] = "Análise Aplicativo Natura Vendas"
OR [Etapa] = "Análise de espaço digital"
OR [Etapa] = "Analise de liberação do espaço"
OR [Etapa] = "Análise de senha"
OR [Etapa] = "Análise de Vale-Troca"
OR [Etapa] = "Análise pedido espaço default"
OR [Etapa] = "Análise Plano de crescimento"
OR [Etapa] = "Análise Site Consultoria"
OR [Etapa] = "Análise Site Força de Vendas"
OR [Etapa] = "Análise Site Natura"
OR [Etapa] = "Cancelamento de Pedido"
OR [Etapa] = "Aguardando N3 Experiência"
THEN "Fase 1"

ELSEIF [Etapa] = "Acompanhamento tecnologia - espaço digital"
OR [Etapa] = "Análise Correção Sistema - SM"
OR [Etapa] = "Abertura do chamado"
THEN "Fase 2"

// 2. Se nenhuma condição da [Etapa] for atendida, verifica a coluna [Solução]
ELSEIF [Solução] = "Abrir chamado"
OR [Solução] = "Card criado no Jira"
THEN "Fase 2"

// 3. Nova verificação da coluna [Chamado]
// Se [Chamado] estiver preenchida (não for nula e não for vazia), retorna "Fase 2"
ELSEIF NOT ISNULL([Chamado]) AND [Chamado] <> "" THEN
    "Fase 2"

// 4. Se nenhuma das condições acima for atendida, o resultado padrão é "Fase 1"
ELSE "Fase 1"
END
```
2. Calcular `Tipo Protocolo`:

```
IF [Central de Atendimento (Referente) (Ocorrência)] = "MÍDIAS SOCIAIS"
OR [Central de Atendimento (Referente) (Ocorrência)] = "REDE NATURA"
OR [Central de Atendimento (Referente) (Ocorrência)] = "Avon Ecomm"
OR [Central de Atendimento (Referente) (Ocorrência)] = "SNAC"
THEN "Protocolos CF"

ELSEIF [Central de Atendimento (Referente) (Ocorrência)] = "Ato - Atendimento Líder"
OR [Central de Atendimento (Referente) (Ocorrência)] = "CAN"
OR [Central de Atendimento (Referente) (Ocorrência)] = "CIN"
OR [Central de Atendimento (Referente) (Ocorrência)] = "Varejo"
THEN "Protocolos CB"

ELSEIF [Fonte] = "Salesforce" AND [Tipo de registro do caso] = "Atendimento CF"
THEN "Protocolos CF"

ELSEIF [Fonte] = "Salesforce" AND [Tipo de registro do caso] = "Atendimento Franquias"
THEN "Franquias"

ELSE "Outro"
END
```
3. Calcular `Base`:

```
IF ISNULL([Número da Ocorrência (Referente) (Ocorrência)]) THEN "" ELSE "Encerrado em" END
```
4. Calcular `Data`:

```
[Término Real]
```

→ [73] União de linhas 1

## [73] União de linhas 1 — SuperUnion

← [72] FASE, Tipo Protocolo; [67] Limpar 2

**Union** das entradas acima (colunas com o mesmo nome se juntam; cria `Table Names`).

1. Remover colunas: `SLA Experiência 24 Horas`

→ [74] Limpar 4

## [74] Limpar 4 — SuperTransform

← [73] União de linhas 1

1. Remapear `Status da Atividade`: "Finalizado" ← "✅ Finalizado"
2. Calcular `Retrabalho`:

```
IF 
	[Solução] = "Erro Operacional" THEN "Retrabalho"
ELSEIF
	[Solução] = "Solicitação não procedente - Desvio operacional" THEN "Retrabalho" ELSE
    "Normal"
END
```
3. Remapear `Fonte`: "Salesforce" ← "Base-2"
4. Remover colunas: `F5`

→ [75] Rechamada; [76] Deixar colunas para MKT; [77] Limpar 12

## [75] Rechamada — SuperTransform

← [74] Limpar 4

1. Excluir `Base` em ['"Criado em"']
2. Excluir `Fonte` em ['"Salesforce"']
3. Excluir `Solução` em ['"Solicitação não procedente - Desvio operacional"']
4. Excluir `Fase` em ['"Fase 1"']
5. Excluir `Experience Tribos` em ['"Incluir / Excluir membro"']
6. Calcular `Número da Ocorrência (Limpo)`:

```
// Remove espaços extras do início e do fim do texto e converte para maiúsculas
TRIM(UPPER([Número da Ocorrência (Referente) (Ocorrência)]))
```

→ [78] Agregar 1

## [76] Deixar colunas para MKT — SuperTransform

_Descrição:_ Adequação de colunas para unir com a base do MKT para gerar a retenção unificada

← [74] Limpar 4

1. Manter só `Base` em ['"Encerrado em"']
2. Manter só: `Nivel de Atendimento`, `Tipo Protocolo`, `Número da Ocorrência (Referente) (Ocorrência)`, `Motivo (Referente) (Ocorrência)`, `Experience`, `Término Real`, `Solução`, `Modificado Por`
3. Renomear `Número da Ocorrência (Referente) (Ocorrência)` → `Tarefa`
4. Renomear `Tipo Protocolo` → `Tipo`
5. Renomear `Nivel de Atendimento` → `Nivel`
6. Renomear `Tarefa` → `Ticket`
7. Calcular `Qtd Atendimentos`:

```
1
```
8. Renomear `Motivo (Referente) (Ocorrência)` → `Status de Classificação`
9. Renomear `Experience` → `Função do Sistema`
10. Renomear `Término Real` → `Data`
11. Renomear `Solução` → `Status de finalização`
12. Renomear `Modificado Por` → `Responsavel Dynamics`
13. Excluir `Status de finalização` em ['"Erro operacional"']
14. Excluir `Status de finalização` em ['"Solicitação não procedente - Desvio operacional"']

→ [79] Dynamics Nivel

## [77] Limpar 12 — SuperTransform

← [74] Limpar 4

→ [80] Dynamics - Termino Real

## [78] Agregar 1 — SuperAggregate

← [75] Rechamada

**Agregar** agrupando por `Número da Ocorrência (Limpo)`: MIN(`Experience Tribos`), MAX(`Código Natura (Cliente) (Contato)`), MIN(`Fase`), MIN(`Solução`), MAX(`Tipo Protocolo`), MAX(`Término Real`)

→ [81] Mes Ano

## [79] Dynamics Nivel — PublishExtract

← [76] Deixar colunas para MKT

**Saída:** `4. DATASOURCES/Dynamics Nivel`

## [80] Dynamics - Termino Real — PublishExtract

← [77] Limpar 12

**Saída:** `4. DATASOURCES/Dynamics - Termino Real`

## [81] Mes Ano — SuperTransform

← [78] Agregar 1

1. Calcular `Mes/Ano`:

```
DATETRUNC('month', [Término Real])
```
2. Calcular `Mes`:

```
MONTH([Término Real])
```
3. Calcular `ID Rechamada`:

```
// Concatena o código da consultora e o problema para criar um ID único.
STR([Código Natura (Cliente) (Contato)]) + "-" + [Experience Tribos]
```
4. Calcular `Mês Seguinte`:

```
DATEADD('month', 1, [Mes/Ano])
```

→ [84] União de colunas 1; [82] Limpar 6

## [82] Limpar 6 — SuperTransform

← [81] Mes Ano

→ [83] Agregar 3

## [83] Agregar 3 — SuperAggregate

← [82] Limpar 6

**Agregar** agrupando por `ID Rechamada`, `Mes/Ano`: MAX(`Mês Seguinte`)

→ [84] União de colunas 1

## [84] União de colunas 1 — SuperJoin

← [81] Mes Ano (Right); [83] Agregar 3 (Left)

**Join right**: esquerda = [83] Agregar 3, direita = [81] Mes Ano

Condição: `esq.[ID Rechamada] == dir.[ID Rechamada] AND esq.[Mês Seguinte] == dir.[Mes/Ano V]`

1. (antes do join, lado direito) Renomear `Mes/Ano` → `Mes/Ano V`
2. (antes do join, lado esquerdo) Renomear `Mes/Ano` → `Mes/Ano A`

→ [85] Limpar 7

## [85] Limpar 7 — SuperTransform

← [84] União de colunas 1

1. Calcular `Flag de Rechamada`:

```
// Se o campo ID Rechamada da tabela da direita (mês anterior) NÃO for nulo,
// então a tarefa é uma rechamada.

IF NOT ISNULL([ID Rechamada-1]) THEN 1 ELSE 0 END
```
2. Calcular `Tarefa Status`:

```
IF NOT ISNULL([ID Rechamada-1]) THEN 'Rechamada' ELSE 'Comum' END

```
3. Remover colunas: `Mês Seguinte-1`
4. Renomear `Número da Ocorrência (Limpo)` → `Número da Ocorrência`
5. Remover colunas: `Mes/Ano A`
6. Renomear `Mes/Ano V` → `Mes/Ano`

→ [86] Dynamics - Base para Rechamada

## [86] Dynamics - Base para Rechamada — PublishExtract

← [85] Limpar 7

**Saída:** `4. DATASOURCES/Dynamics - Base para Rechamada`
