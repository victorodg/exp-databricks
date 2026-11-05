# Especificação do fluxo `GovEXP - Metricas de Excelencia - CSAT.tflx`

Gerado por `ferramentas/especificar_fluxo_prep.py`. Etapas em ordem de execução; `←` indica de onde vêm os dados.

## [1] NCC (1) — LoadSql

Arquivo: `Enquete Malasia.xlsx` · aba `[Base$]`

Campos: `Data do Contato`:datetime, `Enviado em`:datetime, `Respondido em`:string, `Protocolo`:string, `Nome`:string, `Canal`:string, `Contato`:string, `ResponsÃ¡vel`:string, `Nota`:string

→ [12] Remover protocolo de teste

## [2] MTK Historico — LoadSql

Arquivo: `BASE MTK Historico.xlsx` · aba `[Base$]`

Campos: `Protocolo`:string, `Empresa`:string, `Nome`:string, `CPF/CNPJ`:string, `Número do Contrato`:string, `Valor do Contrato`:string, `Código da Gerente`:string, `GV`:string, `Código CN`:string, `Sistema`:string, `Função do Sistema`:string, `Detalhe do Sistema`:string, `Solução Aplicada`:integer, `Pedido finalizado`:string, `AlineWEL`:string, `Status de Classificação`:string, `Status de Finalização`:string, `Função do Sistema 1`:string, `E-mail`:string, `Data Contato`:datetime, `Responsável`:string, `Tempo até ser atendido`:string, `Tempo do atendimento`:string, `Primeiro Tempo de Espera`:string, `Tempo Médio de Espera`:string, `Tempo de Operação`:string, `Fone Cliente`:string, `Canal de Entrada`:string, `Setor Entrada`:string, `Setor Fim`:string, `Qtde Mensagens`:integer, `Status de Classificação 1`:string, `Status de finalização`:string, `Encerrado em`:datetime, `Observações`:string, `Campos adicionais Web Chat`:string, `Pedidos Finalizados`:string, `Quantidade de Tickets`:string, `Ticket`:string, `Cant. de Atendimientos`:string, `Llamado`:string

→ [14] União de linhas 2

## [3] Enquete CES — LoadSql

Arquivo: `Enquete CES.xlsx` · aba `[CES$]`

Campos: `Data do Contato`:datetime, `Enviado em`:datetime, `Respondido em`:string, `Protocolo`:string, `Nome`:string, `Canal`:string, `Contato`:string, `ResponsÃ¡vel`:string, `Nota`:string

→ [20] f_Enquetes (1)

## [4] Base MTK — LoadSql

Arquivo: `BASE MTK.xlsx` · aba `[Base$]`

Campos: `Protocolo`:string, `Empresa`:string, `Nome`:string, `CPF/CNPJ`:string, `Número do Contrato`:string, `Valor do Contrato`:string, `Código da Gerente`:string, `GV`:string, `Código CN`:string, `Sistema`:string, `Função do Sistema`:string, `Detalhe do Sistema`:string, `Solução Aplicada`:integer, `Pedido finalizado`:string, `AlineWEL`:string, `Status de Classificação`:string, `Status de Finalização`:string, `Função do Sistema 1`:string, `Pedidos Finalizados`:string, `Cant. de Atendimientos`:string, `Llamado`:string, `ORIGEN HEALTH CHECK?`:string, `E-mail`:string, `Data Contato`:datetime, `Responsável`:string, `Tempo até ser atendido`:string, `Tempo do atendimento`:string, `Primeiro Tempo de Espera`:string, `Tempo Médio de Espera`:string, `Tempo de Operação`:string, `Fone Cliente`:string, `Canal de Entrada`:string, `Setor Entrada`:string, `Setor Fim`:string, `Qtde Mensagens`:integer, `Status de Classificação 1`:string, `Status de finalização`:string, `Encerrado em`:datetime, `Observações`:string, `Campos adicionais Web Chat`:string, `Quantidade de Tickets`:string

→ [14] União de linhas 2

## [5] Exp Brasil (1) — LoadSql

Arquivo: `Enquete MKT REATIVOS.xlsx` · aba `[Base$]`

Campos: `Data do Contato`:datetime, `Enviado em`:datetime, `Respondido em`:string, `Protocolo`:string, `Nome`:string, `Canal`:string, `Contato`:string, `ResponsÃ¡vel`:string, `Nota`:string

→ [20] f_Enquetes (1)

## [6] Analistas Enquetes — LoadSql

Arquivo: `Analistas Enquetes.xlsx` · aba `[Planilha1$]`

Campos: `Analista para considerar nas Enquetes`:string, `Time`:string, `Data de Inclusão na Lista`:date

→ [13] Limpar 6 (1)

## [7] Hispana (1) — LoadSql

Arquivo: `Enquete BASE MTK.xlsx` · aba `[Base$]`

Campos: `Data do Contato`:datetime, `Enviado em`:datetime, `Respondido em`:string, `Protocolo`:string, `Nome`:string, `Canal`:string, `Contato`:string, `ResponsÃ¡vel`:string, `Nota`:string

→ [20] f_Enquetes (1)

## [8] MKT Hispana Analitico — LoadSql

Arquivo: `MKT Analitico Hispana.xlsx` · aba `[Planilha1$]`

Campos: `Protocolo`:string, `Empresa`:string, `Nome`:string, `Código da Gerente`:string, `GV`:string, `Código CN`:string, `Função do Sistema`:string, `Pedidos Finalizados`:string, `Cant. de Atendimientos`:integer, `Llamado`:string, `ORIGEN HEALTH CHECK?`:string, `E-mail`:string, `Data Contato`:datetime, `Responsável`:string, `Tempo até ser atendido`:string, `Tempo do atendimento`:string, `Primeiro Tempo de Espera`:string, `Tempo Médio de Espera`:string, `Tempo de Operação`:string, `Fone Cliente`:string, `Canal de Entrada`:string, `Setor Entrada`:string, `Setor Fim`:string, `Qtde Mensagens`:integer, `Status de Classificação`:string, `Status de finalização`:string, `Encerrado em`:datetime, `Observações`:string, `Campos adicionais Web Chat`:string, `Quantidade de Tickets`:integer

→ [14] União de linhas 2

## [9] BASE MALASIA 2 — LoadSql

Arquivo: `BASE MALASIA.xlsx` · aba `['BASE MALASIA$']`

Campos: `Protocolo`:string, `Empresa`:string, `Nome`:string, `CPF/CNPJ`:string, `Número do Contrato`:string, `Valor do Contrato`:string, `CODE`:string, `BM CODE`:string, `BC CODE`:string, `FUNCTION`:string, `SOLUTION APPLIED`:string, `FINISHED ORDER`:string, `CHAMADO`:string, `TICKET`:string, `FINISHED ORDER_`:string, `QUANTITY`:string, `SM`:string, `Nome completo (usuário):`:string, `E-mail (usuário):`:string, `Colaborador ou terceirizado?`:string, `Área (usuário)`:string, `País (usuário)`:string, `Colaborador/Terceirizado`:string, `Empresa:`:string, `Localidade:`:string, `Nome 1`:string, `Email`:string, `E-mail`:string, `Data Contato`:datetime, `Responsável`:string, `Tempo até ser atendido`:string, `Tempo do atendimento`:string, `Primeiro Tempo de Espera`:string, `Tempo Médio de Espera`:string, `Tempo de Operação`:string, `Fone Cliente`:string, `Canal de Entrada`:string, `Setor Entrada`:string, `Setor Fim`:string, `Qtde Mensagens`:integer, `Status de Classificação`:string, `Status de finalização`:string, `Encerrado em`:datetime, `Observações`:string, `Campos adicionais Web Chat`:string

→ [15] Manter Apenas Colunas para Join (1)

## [10] Modelo Gauge — LoadExcel

→ [16] Chave Join

## [11] MKT_Reativos — LoadSql

Arquivo: `MKT_Reativos.xlsx` · aba `[Sheet1$]`

Campos: `Protocolo`:string, `Empresa`:string, `Nome`:string, `CPF/CNPJ`:string, `Número do Contrato`:string, `Valor do Contrato`:string, `CODIGO`:string, `GV`:string, `FUNÇÃO`:string, `PEDIDO FINALIZADO`:string, `CONTATO DE SOLUÇÃO`:string, `CHAMADO`:string, `Fornecedor`:string, `Qtd Atendimentos`:integer, `testeLis`:string, `Função do Sistema`:string, `Ciclo - Health Check`:string, `Recebidos - Health Check`:string, `CATEGORIA 1 (WR TRANSP)`:string, `CATEGORIA 2 (WR TRANSP)`:string, `SOLUÇÃO APLICADA`:string, `Origem Health Check?`:string, `Está em Fechamento?`:string, `Código do Impactado`:string, `Ciclo Vigente`:string, `SETOR`:string, `MERCADO`:string, `Resposta pedido duplicado`:string, `Dados bancarios`:string, `E-mail`:string, `Data Contato`:datetime, `Responsável`:string, `Tempo até ser atendido`:string, `Tempo do atendimento`:string, `Primeiro Tempo de Espera`:string, `Tempo Médio de Espera`:string, `Tempo de Operação`:string, `Fone Cliente`:string, `Canal de Entrada`:string, `Setor Entrada`:string, `Setor Fim`:string, `Qtde Mensagens`:integer, `Status de Classificação`:string, `Status de finalização`:string, `Encerrado em`:datetime, `Observações`:string, `Campos adicionais Web Chat`:string, `Quantidade de Tickets`:integer

→ [17] Manter Apenas Colunas para Join (1)

## [12] Remover protocolo de teste — Container

← [1] NCC (1)

1. Excluir `Protocolo` em ['"1990-1509513108473"']

→ [18] Agregar 5

## [13] Limpar 6 (1) — Container

← [6] Analistas Enquetes

→ [28] União de colunas 7 (1)

## [14] União de linhas 2 — SuperUnion

← [2] MTK Historico; [4] Base MTK; [8] MKT Hispana Analitico

**Union** das entradas acima (colunas com o mesmo nome se juntam; cria `Table Names`).

→ [19] Limpar 10

## [15] Manter Apenas Colunas para Join (1) — Container

← [9] BASE MALASIA 2

1. Manter só: `Protocolo`, `FUNCTION`, `SOLUTION APPLIED`, `Canal de Entrada`, `Setor Entrada`, `Setor Fim`, `Status de Classificação`, `Status de finalização`

→ [26] União de colunas 5 (1)

## [16] Chave Join — Container

← [10] Modelo Gauge

1. Calcular `Chave Join`:

```
1
```

→ [31] Join Gauge

## [17] Manter Apenas Colunas para Join (1) — Container

← [11] MKT_Reativos

1. Manter só: `Protocolo`, `GV`, `FUNÇÃO`, `CHAMADO`, `Qtd Atendimentos`, `Função do Sistema`, `MERCADO`, `Primeiro Tempo de Espera`, `Setor Fim`, `Status de Classificação`, `Status de finalização`
2. Remapear `MERCADO`: "ARAUCÁRIA" ← "ARAUCARIA"

→ [23] União de colunas 1 (1)

## [18] Agregar 5 — SuperAggregate

← [12] Remover protocolo de teste

**Agregar** agrupando por `Protocolo`: MIN(`Canal`), MIN(`Contato`), MIN(`Data do Contato`), MIN(`Enviado em`), MIN(`Nome`), MIN(`Nota`), MIN(`Respondido em`), MIN(`ResponsÃ¡vel`), MIN(`Número de linhas (agregado)`)

1. Remover colunas: `Número de linhas (agregado)`

→ [20] f_Enquetes (1)

## [19] Limpar 10 — Container

← [14] União de linhas 2

1. Calcular `Função do Sistema2`:

```
IF ISNULL([Função do Sistema]) THEN
	[Função do Sistema 1]
ELSE
	[Função do Sistema]
END
```
2. Remover colunas: `Função do Sistema 1`
3. Remover colunas: `Função do Sistema`
4. Renomear `Função do Sistema2` → `Função do Sistema 1`

→ [21] Manter Apenas Colunas para Join (1)

## [20] f_Enquetes (1) — SuperUnion

← [3] Enquete CES; [5] Exp Brasil (1); [18] Agregar 5; [7] Hispana (1)

**Union** das entradas acima (colunas com o mesmo nome se juntam; cria `Table Names`).

1. Renomear `Table Names` → `Fonte`
2. Remapear `Fonte`: "Hispana" ← "Enquete BASE MTK.xlsx/Base"; "NCC" ← "Enquete Malasia.xlsx/Base"; "Experiencia Brasil" ← "Enquete MKT REATIVOS.xlsx/Base"
3. Duplicar `Enviado em-1`:

```
[Enviado em]
```
4. Renomear `Enviado em-1` → `Data`
5. Remapear `Fonte`: "CES" ← "Enquete CES.xlsx/CES"; "Experiencia Brasil" ← "Base"; "Hispana" ← "Base-2"; "NCC" ← "Base-1"

→ [22] Limpar 1 (1)

## [21] Manter Apenas Colunas para Join (1) — Container

← [19] Limpar 10

1. Manter só: `Protocolo`, `Sistema`, `Função do Sistema 1`, `Detalhe do Sistema`, `Solução Aplicada`, `Status de Classificação`, `Função do Sistema 1`, `Tempo até ser atendido`, `Tempo do atendimento`, `Primeiro Tempo de Espera`, `Tempo Médio de Espera`, `Tempo de Operação`, `Canal de Entrada`, `Setor Entrada`, `Setor Fim`, `Status de Classificação 1`, `Status de finalização`, `Observações`
2. Remover colunas: `Status de Classificação`
3. Renomear `Status de Classificação 1` → `Status de Classificação`
4. Renomear `Função do Sistema 1` → `Função do Sistema`
5. Calcular `Pais`:

```
IF [Setor Fim] = "APP NATURA" THEN "Latam"
ELSEIF [Setor Fim] = "APP Natura Latam" THEN "Latam"
ELSEIF [Setor Fim] = "AR" THEN "Argentina"
ELSEIF [Setor Fim] = "AR- Email" THEN "Argentina"
ELSEIF [Setor Fim] = "AR GV" THEN "Argentina"
ELSEIF [Setor Fim] = "ATENCIÓN" THEN "Latam"
ELSEIF [Setor Fim] = "ATENDIMIENTO" THEN "Latam"
ELSEIF [Setor Fim] = "CL" THEN "Chile"
ELSEIF [Setor Fim] = "CL GV" THEN "Chile"
ELSEIF [Setor Fim] = "CL - Email" THEN "Chile"
ELSEIF [Setor Fim] = "CL - CELULAR" THEN "Latam"
ELSEIF [Setor Fim] = "CO" THEN "Colombia"
ELSEIF [Setor Fim] = "CO GV" THEN "Colombia"
ELSEIF [Setor Fim] = "CO - Email" THEN "Colombia"
ELSEIF [Setor Fim] = "CO-CELULAR" THEN "Colombia"
ELSEIF [Setor Fim] = "CO-SOPORTE" THEN "Colombia"
ELSEIF [Setor Fim] = "EC" THEN "Ecuador"
ELSEIF [Setor Fim] = "EC GV" THEN "Ecuador"
ELSEIF [Setor Fim] = "EC - Email" THEN "Ecuador"
ELSEIF [Setor Fim] = "EX" THEN "Latam"
ELSEIF [Setor Fim] = "FV-AYUDA" THEN "Latam"
ELSEIF [Setor Fim] = "GV CL" THEN "Chile"
ELSEIF [Setor Fim] = "GVs CHILE" THEN "Chile"
ELSEIF [Setor Fim] = "MI NEGOCIO" THEN "Latam"
ELSEIF [Setor Fim] = "MX" THEN "Mexico"
ELSEIF [Setor Fim] = "MX - Email" THEN "Mexico"
ELSEIF [Setor Fim] = "MX GV" THEN "Mexico"
ELSEIF [Setor Fim] = "PE" THEN "Peru"
ELSEIF [Setor Fim] = "PE- Email" THEN "Peru"
ELSEIF [Setor Fim] = "PE GV" THEN "Peru"
ELSEIF [Setor Fim] = "PE-CELULAR" THEN "Peru"
ELSEIF [Setor Fim] = "PE-LIDER" THEN "Peru"
ELSEIF [Setor Fim] = "APP AVON" THEN "Latam"
ELSEIF [Setor Fim] = "EX" THEN "Latam"
ELSEIF [Setor Fim] = "LNN EC" THEN "Ecuador"
ELSEIF [Setor Fim] = "LNN EC - Email" THEN "Ecuador"
ELSE NULL
END
```

→ [25] União de colunas 3 (1)

## [22] Limpar 1 (1) — Container

← [20] f_Enquetes (1)

1. Remapear `Nota`: "Nao respondido" ← "NÃ£o respondido"
2. Remapear `Respondido em`: "Não respondido" ← "NÃ£o respondido"
3. Calcular `C-SAT`:

```
// C-SAT (por nota de 1 a 5)
IF 
	LEFT(TRIM([Nota]), 1) = '5' OR LEFT(TRIM([Nota]), 1) = '4' 
THEN 
	'PROMOTOR'
ELSEIF 
	LEFT(TRIM([Nota]), 1) = '3' 
THEN 
	'NEUTRO'
ELSEIF 
	LEFT(TRIM([Nota]), 1) = '2' OR LEFT(TRIM([Nota]), 1) = '1' 
THEN 
	'DETRATOR'
ELSE 
	'Não respondido'
END

```
4. Calcular `Enquete Respondida`:

```
//1 Se a enquete foi respondida e 0 se não foi respondida

IF 
	[C-SAT] = "Não respondido"
THEN
	0
ELSE
	1
END
```
5. Remapear `Respondido em`: null ← "Não respondido"
6. Renomear `ResponsÃ¡vel` → `Responsavel`
7. Remapear `Responsavel`: "Robson Ribeiro da Costa" ← "Robson  Ribeiro da Costa"; "Cristiane dos Santos Bedias" ← "Cristiane Bedias"; "Caroline Pacifico de Almeida" ← "CAROLINE PACIFICO DE ALMEIDA"; "Cristian Jesus Aliaga Cutti" ← "Cristian JesÃºs Aliaga Cutti", "Cristian Jesús Aliaga Cutti"; "Diego da Conceição Felix" ← "Diego Da ConceiÃ§Ã£o Felix", "Diego Da Conceição Felix"; "Felipe dos Santos Flor" ← "Felipe Flor"; "Raissa de Assis Jesus" ← "RaÃ­ssa de Assis Jesus", "Raíssa de Assis Jesus"; "Rodrigo Ferreira Magalhaes" ← "Rodrigo Ferreira MagalhÃ£es", "Rodrigo Ferreira Magalhães"; "Thadeu Maciel Rocha" ← "Thadeu Maciel", "Thadeu Rocha"

→ [23] União de colunas 1 (1)

## [23] União de colunas 1 (1) — SuperJoin

← [22] Limpar 1 (1) (Left); [17] Manter Apenas Colunas para Join (1) (Right)

**Join left**: esquerda = [22] Limpar 1 (1), direita = [17] Manter Apenas Colunas para Join (1)

Condição: `esq.[Protocolo] == dir.[Protocolo]`

→ [24] Limpar 3 (1)

## [24] Limpar 3 (1) — Container

← [23] União de colunas 1 (1)

1. Renomear `GV` → `Exp Br GV`
2. Renomear `FUNÇÃO` → `Exp Br FUNÇÃO`
3. Renomear `CHAMADO` → `Exp Br CHAMADO`
4. Renomear `Qtd Atendimentos` → `Exp Br  Qtd Atendimentos`
5. Renomear `Função do Sistema` → `Exp Br Função do Sistema`
6. Renomear `Primeiro Tempo de Espera` → `Exp Br Primeiro Tempo de Espera`
7. Renomear `Setor Fim` → `Exp Br Setor Fim`
8. Renomear `Status de Classificação` → `Exp Br Status de Classificação`
9. Renomear `Status de finalização` → `Exp Br Status de finalização`
10. Remover colunas: `Protocolo-1`
11. Renomear `MERCADO` → `Exp Br MERCADO`

→ [25] União de colunas 3 (1)

## [25] União de colunas 3 (1) — SuperJoin

← [24] Limpar 3 (1) (Left); [21] Manter Apenas Colunas para Join (1) (Right)

**Join left**: esquerda = [24] Limpar 3 (1), direita = [21] Manter Apenas Colunas para Join (1)

Condição: `esq.[Protocolo] == dir.[Protocolo]`

1. (antes do join, lado direito) Renomear `Sistema` → `OIS Sistema`
2. (antes do join, lado direito) Renomear `Detalhe do Sistema` → `OIS Detalhe do Sistema`
3. (antes do join, lado direito) Renomear `Solução Aplicada` → `OIS Solução Aplicada`
4. (antes do join, lado direito) Renomear `Função do Sistema` → `Função do Sistema 1`
5. (antes do join, lado direito) Renomear `Função do Sistema 1` → `OIS Função do Sistema`
6. (antes do join, lado direito) Renomear `Tempo até ser atendido` → `OIS Tempo até ser atendido`
7. (antes do join, lado direito) Renomear `Tempo do atendimento` → `OIS Tempo do atendimento`
8. (antes do join, lado direito) Renomear `Primeiro Tempo de Espera` → `OIS Primeiro Tempo de Espera`
9. (antes do join, lado direito) Renomear `Tempo Médio de Espera` → `OIS Tempo Médio de Espera`
10. (antes do join, lado direito) Renomear `Tempo de Operação` → `OIS Tempo de Operação`
11. (antes do join, lado direito) Renomear `Canal de Entrada` → `OIS Canal de Entrada`
12. (antes do join, lado direito) Renomear `Setor Entrada` → `OIS Setor Entrada`
13. (antes do join, lado direito) Renomear `Setor Fim` → `OIS Setor Fim`
14. (antes do join, lado direito) Renomear `Status de Classificação` → `OIS Status de Classificação`
15. (antes do join, lado direito) Renomear `Status de finalização` → `OIS Status de finalização`
16. (antes do join, lado direito) Renomear `Observações` → `OIS Observações`
17. Remover colunas: `Protocolo-1`

→ [26] União de colunas 5 (1)

## [26] União de colunas 5 (1) — SuperJoin

← [15] Manter Apenas Colunas para Join (1) (Right); [25] União de colunas 3 (1) (Left)

**Join left**: esquerda = [25] União de colunas 3 (1), direita = [15] Manter Apenas Colunas para Join (1)

Condição: `esq.[Protocolo] == dir.[Protocolo]`

1. (antes do join, lado direito) Renomear `FUNCTION` → `NCC FUNCTION`
2. (antes do join, lado direito) Renomear `SOLUTION APPLIED` → `NCC SOLUTION APPLIED`
3. (antes do join, lado direito) Renomear `Canal de Entrada` → `NCC Canal de Entrada`
4. (antes do join, lado direito) Renomear `Setor Entrada` → `NCC Setor Entrada`
5. (antes do join, lado direito) Renomear `Setor Fim` → `NCC Setor Fim`
6. (antes do join, lado direito) Renomear `Status de Classificação` → `NCC Status de Classificação`
7. (antes do join, lado direito) Renomear `Status de finalização` → `NCC Status de finalização`
8. Remover colunas: `Protocolo-1`

→ [27] remover teste NCC

## [27] remover teste NCC — Container

← [26] União de colunas 5 (1)

1. Remapear `Responsavel`: "João Lucas Vieira de Carvalho" ← "JoÃ£o Lucas Vieira de Carvalho"; "João Gabriel Paulino de Souza" ← "JoÃ£o Gabriel Paulino de Souza"; "Rafaella Cristiny Jacinto Camilo" ← "RAFAELLA CRISTINY JACINTO"; "Marcio Miranda Alves dos Santos" ← "MÃ¡rcio Miranda Alves dos Santos"; "Adrielle Cristina" ← "Adrielle Cristina Pereira Silva"; "Elianny Marielis Rodriguez Barrios" ← "ELIANNY MARIELIS RODRIGUEZ BARRIOS"; "Ghandy Giovanny Gautiet Gomez" ← "Ghandy Giovanny Gautier Gomez"; "Grefanny Mercedes Rodríguez Berro" ← "Grefanny Mercedes RodrÃ­guez berro"; "Ivan Moralez Diaz" ← "Ivan Moralez DÃ­az"; "María Inés Ovalles" ← "MarÃ­a InÃ©s Ovalles"; "Saulo Moises Jimenez Ordaz" ← "Saulo Jimenez"; "Cristian Jesus Aliaga Cutti" ← "Cristian JesÃºs Aliaga Cutti"; "Diego da Conceição Felix" ← "Diego Da ConceiÃ§Ã£o Felix"; "Felipe dos Santos Flor" ← "Felipe Flor"; "Raissa de Assis Jesus" ← "RaÃ­ssa de Assis Jesus"; "Rodrigo Ferreira Magalhaes" ← "Rodrigo Ferreira MagalhÃ£es"; "Thadeu Maciel Rocha" ← "Thadeu Maciel", "Thadeu Rocha"; "Cristian Alejandro Lopez Torres" ← "Cristian Torres"; "Luis Ernesto Antolines Garcia" ← "Luis Antolines"; "Adriana Conceição de Oliveira" ← "Adriana Conceição", "Adriana ConceiÃ§Ã£o"
2. Excluir `NCC Status de finalização` em ['"Teste NCC"']
3. Remapear `Responsavel`: "Ivan Moralez Diaz" ← "Ivan Moralez Díaz"; "Taina Pereira Galdino Da Silva" ← "Taina Pereira Galdino"

→ [28] União de colunas 7 (1)

## [28] União de colunas 7 (1) — SuperJoin

← [27] remover teste NCC (Left); [13] Limpar 6 (1) (Right)

**Join inner**: esquerda = [27] remover teste NCC, direita = [13] Limpar 6 (1)

Condição: `esq.[Responsavel] == dir.[Analista para considerar nas Enquetes]`

→ [29] Limpar 7 (1)

## [29] Limpar 7 (1) — Container

← [28] União de colunas 7 (1)

1. Remapear `Exp Br  Qtd Atendimentos`: 1 ← null
2. Remapear `OIS Solução Aplicada`: 1 ← 6256, null
3. Calcular `Nota CSAT`:

```
IF [C-SAT] = "PROMOTOR" THEN 1 ELSE 0 END
```
4. Calcular `Nota CSAT SIMPLE`:

```
IF 
	[C-SAT] = "PROMOTOR" OR [C-SAT] = "NEUTRO" 
THEN 
	1 
ELSE 
	0 
END
```
5. MergeColumns: `{"mergedColumnName": "Analista para considerar nas Enquetes", "mergeColumnsList": ["Analista para considerar nas Enquetes", "Nota CSAT SIMPLE"]}`
6. Calcular `Nota CSAT Simple`:

```
IF
	[C-SAT] = "NEUTRO" OR [C-SAT] = "PROMOTOR"
THEN
	1
ELSE
	0
END
```
7. Remapear `Nota`: "1 - Muito Difícil" ← "1 - Muito DifÃ­cil"; "2 - Difícil" ← "2 - DifÃ­cil"; "3 - Neutro | Razoável" ← "3 - Neutro | RazoÃ¡vel"; "4 - Fácil" ← "4 - FÃ¡cil"; "5 - Muito Fácil" ← "5 - Muito FÃ¡cil"
8. Calcular `Nota CES`:

```
IF 
	[Nota] = "1 - Muito Difícil" 
THEN 
	1
ELSEIF 
	[Nota]= "2 - Difícil" 
THEN 
	2
ELSEIF 
	[Nota] = "3 - Neutro | Razoável"
THEN 
	3
ELSEIF 
	[Nota] = "4 - Fácil" 
THEN 
	4
ELSEIF 
	[Nota] = "5 - Muito Fácil" 
THEN 
	5
END



```

→ [30] Chave Join  e Notas

## [30] Chave Join  e Notas — Container

← [29] Limpar 7 (1)

1. Calcular `Chave Join`:

```
1
```
2. Calcular `Nota da CSAT`:

```
IF [C-SAT] = "PROMOTOR" THEN 1 ELSE 0 END
```
3. Calcular `Nota da CSAT Simple`:

```
IF [C-SAT] = "PROMOTOR" OR [C-SAT] = "NEUTRO" THEN 1 ELSE 0 END
```

→ [31] Join Gauge

## [31] Join Gauge — SuperJoin

← [30] Chave Join  e Notas (Right); [16] Chave Join (Left)

**Join inner**: esquerda = [16] Chave Join, direita = [30] Chave Join  e Notas

Condição: `esq.[Chave Join] == dir.[Chave Join]`

→ [32] Turno IM

## [32] Turno IM — Container

← [31] Join Gauge

1. Calcular `Turno`:

```
IF 
	[Time] = "NCC - Turno A Dia"
THEN
	"NCC - Turno A Dia"
ELSEIF 
	[Time] = "NCC - Turno A Noite"
THEN
	"NCC - Turno A Noite"
ELSEIF
	[Time] = "NCC - Turno B Dia"
THEN
	"NCC - Turno B Dia"
ELSEIF
	[Time] = "NCC - Turno B Noite"
THEN
	"NCC - Turno B Noite"
END
```
2. Remapear `Time`: "IM" ← "NCC - Turno B Noite", "NCC - Turno A Dia", "NCC - Turno A Noite", "NCC - Turno B Dia"

→ [33] Limpar 9

## [33] Limpar 9 — Container

← [32] Turno IM

1. Calcular `Exp Br MERCADO`:

```
IF UPPER(TRIM([Exp Br MERCADO])) = "AT" THEN "ATLÂNTICA"
ELSEIF UPPER(TRIM([Exp Br MERCADO])) = "AM" THEN "AMAZÔNIA"
ELSEIF CONTAINS(UPPER([Exp Br MERCADO]), "AMA") THEN "AMAZÔNIA"
ELSEIF CONTAINS(UPPER([Exp Br MERCADO]), "ARA") THEN "ARAUCÁRIA"
ELSEIF CONTAINS(UPPER([Exp Br MERCADO]), "ATL") THEN "ATLÂNTICA"
ELSEIF CONTAINS(UPPER([Exp Br MERCADO]), "CAA") THEN "CAATINGA"
ELSEIF CONTAINS(UPPER([Exp Br MERCADO]), "CER") THEN "CERRADO"
ELSE [Exp Br MERCADO]
END
```

→ [34] Enquetes C-SAT

## [34] Enquetes C-SAT — PublishExtract

← [33] Limpar 9

**Saída:** `4. DATASOURCES/Enquetes C-SAT`
