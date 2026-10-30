# Especificação do fluxo `Daily Experiencia OIS.tfl`

Gerado por `ferramentas/especificar_fluxo_prep.py`. Etapas em ordem de execução; `←` indica de onde vêm os dados.

## [1] Completo — LoadSql

Arquivo: `MKT Hispana Completo.xlsx` · aba `[Sheet1$]`

Campos: `Protocol`:string, `Nome`:string, `'Atendimentos'(first_message_at)`:datetime, `Data criação`:datetime, `Início Atendimento`:datetime, `Atendido`:datetime, `Data conclusão`:datetime, `Última mensagem`:datetime, `Tipo Canal`:string, `Canal`:string, `Setor`:string, `Operador`:string, `Telefone`:string, `Situação`:string, `Status`:string, `Tempo médio até ser atendidos`:string, `Tempo médio primeira espera`:string, `Tempo médio atendimento`:string, `Tempo médio espera`:string, `Tempo médio operacional`:string, `Qtde Mensagens`:integer

→ [20] 16 17/03/26

## [2] Funcao do Sistema — LoadSql

Arquivo: `Auxiliar Hispana` · aba `['Funcao do Sistema$']`

Campos: `Função do Sistema - Ticket`:string, `Função do Sistema - Analitico`:string

→ [21] Limpar 17

## [3] Novo Analitico — LoadSql

Arquivo: `MKT Analitico Hispana.xlsx` · aba `[Planilha1$]`

Campos: `Protocolo`:string, `Empresa`:string, `Nome`:string, `Código da Gerente`:string, `GV`:string, `Código CN`:string, `Função do Sistema`:string, `Pedidos Finalizados`:string, `Cant. de Atendimientos`:integer, `Llamado`:string, `ORIGEN HEALTH CHECK?`:string, `E-mail`:string, `Data Contato`:datetime, `Responsável`:string, `Tempo até ser atendido`:string, `Tempo do atendimento`:string, `Primeiro Tempo de Espera`:string, `Tempo Médio de Espera`:string, `Tempo de Operação`:string, `Fone Cliente`:string, `Canal de Entrada`:string, `Setor Entrada`:string, `Setor Fim`:string, `Qtde Mensagens`:integer, `Status de Classificação`:string, `Status de finalização`:string, `Encerrado em`:datetime, `Observações`:string, `Campos adicionais Web Chat`:string, `Quantidade de Tickets`:integer

→ [30] União de linhas 23

## [4] AppSheets Registro de Grupos — LoadSql

Arquivo: `Consolidado - Registro de Grupos` · aba `[Página1$]`

Campos: `ID`:string, `Fecha del contacto`:date, `Analista`:string, `Grupo de WhatsApp`:string, `País Afectado`:string, `Usuario Afectado`:string, `Solución aplicada`:integer, `Plataforma`:string, `Función del sistema`:string, `Pedido Finalizado`:string, `Status de finalización`:string, `F12`:string, `F13`:string

→ [22] Renomear colunas

## [5] AppSheets Resenhas OIS — LoadSql

Arquivo: `Resenhas OIs` · aba `[BaseDados$]`

Campos: `F1`:string, `Tienda`:string, `Aplicación`:string, `Nombre del Usuario Respondente`:string, `Clasificación de Estrellas`:string, `Fecha de la Respuesta`:date, `Categoría de la Respuesta`:string, `Categoría de la Respuesta 2`:string, `Clasificación de la Respuesta`:string, `Comentario Publicado`:string, `Respuesta Proporcionada`:string, `Clasificación del Ofensor`:string, `Pais`:string, `Responsable de la Respuesta`:string, `Fecha de la Respuesta EXP`:datetime, `OBSERVACIÓN`:string

→ [23] Limpar 3

## [6] App Natura — LoadSql

Arquivo: `App Natura.xlsx` · aba `[reviews_reviews_net#natura#semp$]`

Campos: `Package Name`:string, `App Version Code`:integer, `App Version Name`:string, `Reviewer Language`:string, `Device`:string, `Review Submit Date and Time`:string, `Review Submit Millis Since Epoch`:integer, `Review Last Update Date and Time`:string, `Review Last Update Millis Since Epoch`:integer, `Star Rating`:integer, `Review Title`:string, `Review Text`:string, `Developer Reply Date and Time`:string, `Developer Reply Millis Since Epoch`:integer, `Developer Reply Text`:string, `Review Link`:string

Ações na leitura:

- Filtro:

```
[Reviewer Language]="es"
```

→ [32] União das Bases

## [7] MKT Historico — LoadSql

Arquivo: `BASE MTK Historico.xlsx` · aba `[Base$]`

Campos: `Protocolo`:string, `Empresa`:string, `Nome`:string, `CPF/CNPJ`:string, `Número do Contrato`:string, `Valor do Contrato`:string, `Código da Gerente`:string, `GV`:string, `Código CN`:string, `Sistema`:string, `Função do Sistema`:string, `Detalhe do Sistema`:string, `Solução Aplicada`:integer, `Pedido finalizado`:string, `AlineWEL`:string, `Status de Classificação`:string, `Status de Finalização`:string, `Função do Sistema 1`:string, `E-mail`:string, `Data Contato`:datetime, `Responsável`:string, `Tempo até ser atendido`:string, `Tempo do atendimento`:string, `Primeiro Tempo de Espera`:string, `Tempo Médio de Espera`:string, `Tempo de Operação`:string, `Fone Cliente`:string, `Canal de Entrada`:string, `Setor Entrada`:string, `Setor Fim`:string, `Qtde Mensagens`:integer, `Status de Classificação 1`:string, `Status de finalização`:string, `Encerrado em`:datetime, `Observações`:string, `Campos adicionais Web Chat`:string, `Pedidos Finalizados`:string, `Quantidade de Tickets`:string, `Ticket`:string, `Cant. de Atendimientos`:string, `Llamado`:string

→ [24] Manter apenas dia 16 e 17

## [8] BASE MTK — LoadSql

Arquivo: `BASE MTK.xlsx` · aba `[Base$]`

Campos: `Protocolo`:string, `Empresa`:string, `Nome`:string, `CPF/CNPJ`:string, `Número do Contrato`:string, `Valor do Contrato`:string, `Código da Gerente`:string, `GV`:string, `Código CN`:string, `Sistema`:string, `Função do Sistema`:string, `Detalhe do Sistema`:string, `Solução Aplicada`:integer, `Pedido finalizado`:string, `AlineWEL`:string, `Status de Classificação`:string, `Status de Finalização`:string, `Função do Sistema 1`:string, `Pedidos Finalizados`:string, `Cant. de Atendimientos`:string, `Llamado`:string, `ORIGEN HEALTH CHECK?`:string, `E-mail`:string, `Data Contato`:datetime, `Responsável`:string, `Tempo até ser atendido`:string, `Tempo do atendimento`:string, `Primeiro Tempo de Espera`:string, `Tempo Médio de Espera`:string, `Tempo de Operação`:string, `Fone Cliente`:string, `Canal de Entrada`:string, `Setor Entrada`:string, `Setor Fim`:string, `Qtde Mensagens`:integer, `Status de Classificação 1`:string, `Status de finalização`:string, `Encerrado em`:datetime, `Observações`:string, `Campos adicionais Web Chat`:string, `Quantidade de Tickets`:string

→ [25] Remover dia 16 e 17

## [9] MKT TICKETS — LoadSql

Arquivo: `Tickets Hispana.xlsx` · aba `[Planilha1$]`

Campos: `ID do Ticket`:string, `Protocolo do Atendimento`:string, `Setor do Atendimento`:string, `Data de Criação do Atendimento`:datetime, `Estado`:string, `Status de Classificação`:string, `Status de Finalização`:string, `Data de Finalização`:datetime, `Usuário Responsável`:string, `Data de Criação do Ticket`:datetime, `Protocolo do Atendimento Convertido`:string, `Data de Conversão do Atendimento`:string, `Código CN`:string, `Função do Sistema`:string, `PEDIDOS FINALIZADOS`:string, `Cant. de Atendimientos`:integer, `Llamado`:string, `Observações`:string

→ [26] Limpar 15

## [10] Ticket Medio Hispana — LoadSql

Arquivo: `Ticket Medio Hispana` · aba `['Ticket Medio$']`

Campos: `Pais`:string, `Valor por pedido`:real, `Data Contato`:date

→ [27] Limpar 6

## [11] Analitico — LoadSql

Arquivo: `MKT Analitico Hispana.xlsx` · aba `[Planilha1$]`

Campos: `Protocolo`:string, `Empresa`:string, `Nome`:string, `Código da Gerente`:string, `GV`:string, `Código CN`:string, `Função do Sistema`:string, `Pedidos Finalizados`:string, `Cant. de Atendimientos`:integer, `Llamado`:string, `ORIGEN HEALTH CHECK?`:string, `E-mail`:string, `Data Contato`:datetime, `Responsável`:string, `Tempo até ser atendido`:string, `Tempo do atendimento`:string, `Primeiro Tempo de Espera`:string, `Tempo Médio de Espera`:string, `Tempo de Operação`:string, `Fone Cliente`:string, `Canal de Entrada`:string, `Setor Entrada`:string, `Setor Fim`:string, `Qtde Mensagens`:integer, `Status de Classificação`:string, `Status de finalização`:string, `Encerrado em`:datetime, `Observações`:string, `Campos adicionais Web Chat`:string, `Quantidade de Tickets`:integer

→ [28] Substitui por 1

## [12] MKT Histórico — LoadSql

Arquivo: `BASE MTK Historico.xlsx` · aba `[Base$]`

Campos: `Protocolo`:string, `Empresa`:string, `Nome`:string, `CPF/CNPJ`:string, `Número do Contrato`:string, `Valor do Contrato`:string, `Código da Gerente`:string, `GV`:string, `Código CN`:string, `Sistema`:string, `Função do Sistema`:string, `Detalhe do Sistema`:string, `Solução Aplicada`:integer, `Pedido finalizado`:string, `AlineWEL`:string, `Status de Classificação`:string, `Status de Finalização`:string, `Função do Sistema 1`:string, `E-mail`:string, `Data Contato`:datetime, `Responsável`:string, `Tempo até ser atendido`:string, `Tempo do atendimento`:string, `Primeiro Tempo de Espera`:string, `Tempo Médio de Espera`:string, `Tempo de Operação`:string, `Fone Cliente`:string, `Canal de Entrada`:string, `Setor Entrada`:string, `Setor Fim`:string, `Qtde Mensagens`:integer, `Status de Classificação 1`:string, `Status de finalização`:string, `Encerrado em`:datetime, `Observações`:string, `Campos adicionais Web Chat`:string, `Pedidos Finalizados`:string, `Quantidade de Tickets`:string, `Ticket`:string, `Cant. de Atendimientos`:string, `Llamado`:string

→ [29] 

## [13] App_Avon — LoadSql

Arquivo: `App_Avon.xlsx` · aba `[reviews_reviews_com#naturaeco#a$]`

Campos: `Package Name`:string, `App Version Code`:integer, `App Version Name`:string, `Reviewer Language`:string, `Device`:string, `Review Submit Date and Time`:string, `Review Submit Millis Since Epoch`:integer, `Review Last Update Date and Time`:string, `Review Last Update Millis Since Epoch`:integer, `Star Rating`:integer, `Review Title`:string, `Review Text`:string, `Developer Reply Date and Time`:string, `Developer Reply Millis Since Epoch`:integer, `Developer Reply Text`:string, `Review Link`:string

Ações na leitura:

- Filtro:

```
[Reviewer Language]="es"
```

→ [32] União das Bases

## [14] MKT Analitico — LoadSql

Arquivo: `BASE MTK.xlsx` · aba `[Base$]`

Campos: `Protocolo`:string, `Empresa`:string, `Nome`:string, `CPF/CNPJ`:string, `Número do Contrato`:string, `Valor do Contrato`:string, `Código da Gerente`:string, `GV`:string, `Código CN`:string, `Sistema`:string, `Função do Sistema`:string, `Detalhe do Sistema`:string, `Solução Aplicada`:integer, `Pedido finalizado`:string, `AlineWEL`:string, `Status de Classificação`:string, `Status de Finalização`:string, `Função do Sistema 1`:string, `Pedidos Finalizados`:string, `Cant. de Atendimientos`:string, `Llamado`:string, `ORIGEN HEALTH CHECK?`:string, `E-mail`:string, `Data Contato`:datetime, `Responsável`:string, `Tempo até ser atendido`:string, `Tempo do atendimento`:string, `Primeiro Tempo de Espera`:string, `Tempo Médio de Espera`:string, `Tempo de Operação`:string, `Fone Cliente`:string, `Canal de Entrada`:string, `Setor Entrada`:string, `Setor Fim`:string, `Qtde Mensagens`:integer, `Status de Classificação 1`:string, `Status de finalização`:string, `Encerrado em`:datetime, `Observações`:string, `Campos adicionais Web Chat`:string, `Quantidade de Tickets`:string

→ [30] União de linhas 23

## [15] Ticket Medio — LoadSql

Arquivo: `Ticket Medio por Pais` · aba `['Ticket Medio$']`

Campos: `Pais`:string, `Valor por pedido`:real

→ [92] União de colunas 2

## [16] Expurgo MKT — LoadSql

Arquivo: `Base Exento` · aba `[Página1$]`

Campos: `Protocolo`:string, `Pais`:string, `Exento`:string, `Justificación`:string, `Autorizado por Natura`:date

→ [31] Limpar 1

## [17] Resenhas Latam — LoadSql

Arquivo: `Resenhas Latam.xlsx` · aba `[in$]`

Campos: `Package Name`:string, `App Version Code`:integer, `App Version Name`:string, `Reviewer Language`:string, `Device`:string, `Review Submit Date and Time`:string, `Review Submit Millis Since Epoch`:integer, `Review Last Update Date and Time`:string, `Review Last Update Millis Since Epoch`:integer, `Star Rating`:integer, `Review Title`:string, `Review Text`:string, `Developer Reply Date and Time`:string, `Developer Reply Millis Since Epoch`:integer, `Developer Reply Text`:string, `Review Link`:string

→ [32] União das Bases

## [18] Mi Negocio — LoadSql

Arquivo: `Mi Negocio.xlsx` · aba `[reviews_reviews_net#natura#mine$]`

Campos: `Package Name`:string, `App Version Code`:integer, `App Version Name`:string, `Reviewer Language`:string, `Device`:string, `Review Submit Date and Time`:string, `Review Submit Millis Since Epoch`:integer, `Review Last Update Date and Time`:string, `Review Last Update Millis Since Epoch`:integer, `Star Rating`:integer, `Review Title`:string, `Review Text`:string, `Developer Reply Date and Time`:string, `Developer Reply Millis Since Epoch`:integer, `Developer Reply Text`:string, `Review Link`:string

Ações na leitura:

- Filtro:

```
[Reviewer Language]="es"
```

→ [32] União das Bases

## [19] SN — LoadSql

Arquivo: `BASE SN OIS.xlsx` · aba `['Page 1$']`

Campos: `Número`:string, `Aberto`:datetime, `Solicitante`:string, `Prioridade`:string, `Estado`:string, `Categoria`:string, `Grupo de atribuição`:string, `Atribuído a`:string, `Atualizado em`:datetime, `Atualizado por`:string, `Em qual país ocorre o incidente?`:string, `Nome do Solicitante`:string, `Quem está sendo impactado?`:string, `Qual a marca impactada?`:string, `Número de CPF`:string, `Qual é a localidade?`:string, `Criado por`:string, `Encerrado`:datetime, `Início real`:string, `Resolvido`:datetime, `Término real`:string, `Tipo de tarefa`:string, `Subcategoria`:string, `Serviço`:string, `Motivo para estar em espera`:string, `JIRA`:string, `Contagem de reaberturas`:integer, `Última reabertura em`:datetime, `Descrição resumida`:string, `Código de resolução`:string, `Número 1`:string, `Descrição`:string, `Declaração do problema`:string, `Local`:string

Ações na leitura:

- Remover colunas: `Número de CPF`
- Remover colunas: `Qual é a localidade?`
- Remover colunas: `Término real`
- Remover colunas: `Início real`

→ [33] Aging e Faixa de Aging

## [20] 16 17/03/26 — Container

_Descrição:_ Remoção dos casos abertos de 16 e 17 de Março 2026

← [1] Completo

1. Calcular `MANTER`:

```
IF DATE([Data criação]) = #2026-03-16# OR DATE([Data criação]) = #2026-03-17# THEN 
    "Remover"
ELSE 
    "Manter"
END
```
2. Manter só `MANTER` em ['"Manter"']
3. Remover colunas: `MANTER`

→ [36] União de linhas 8

## [21] Limpar 17 — Container

← [2] Funcao do Sistema

→ [37] União de colunas 8

## [22] Renomear colunas — Container

← [4] AppSheets Registro de Grupos

1. Renomear `Fecha del contacto` → `Data Contato Fuso`
2. Mudar tipo: `Data Contato Fuso` → datetime
3. Renomear `ID` → `Protocolo`
4. Renomear `Analista` → `Responsável`
5. Renomear `Grupo de WhatsApp` → `Origem`
6. Renomear `País Afectado` → `Pais`
7. Remapear `Pais`: "Chile" ← "CHILE"; "Colombia" ← "COLOMBIA"; "Mexico" ← "MEXICO"; "Peru" ← "PERU"
8. Renomear `Usuario Afectado` → `Código CN`
9. Renomear `Solución aplicada` → `Solução Aplicada`
10. Renomear `Pedido Finalizado` → `Pedidos Finalizados`
11. Renomear `Status de finalización` → `Status de finalização`
12. Renomear `Plataforma` → `Status de Classificação`
13. Renomear `Función del sistema` → `Função do Sistema`
14. Calcular `Nivel`:

```
IF [Data Contato Fuso] < #2026-03-01# THEN
    // --- REGRA PARA DATAS ANTERIORES A MARÇO 2026 (Base: Nivel) ---
    CASE [Status de finalização]
        // CATEGORIA N2
        WHEN "DIRECCIONADO - PLCOM" THEN "N2"
        WHEN "DIRECCIONADO - TD LOCAL" THEN "N2"
        WHEN "INCIDENTE CRITICO" THEN "N2"
        WHEN "INCIDENTE CRÍTICO" THEN "N2"
        WHEN "INCIDENTE CRÃTICO" THEN "N2"
        WHEN "LLAMADO ABIERTO PARA N2" THEN "N2"
        WHEN "REAPERTURA DE LLAMADO" THEN "N2"

        // CATEGORIA NEUTRO
        WHEN "AJUSTE/ CORRECCION REALIZADO POR PLCOM" THEN "Neutro"
        WHEN "BUEN DIA/AGRADECIMIENTOS" THEN "Neutro"
        WHEN "CERRADO DESPUÉS DE HORAS" THEN "Neutro"
        WHEN "CONSULTA - TD LOCAL" THEN "Neutro"
        WHEN "CONSULTA CON PLCOM" THEN "Neutro"
        WHEN "CONTACTO SIN EXITO" THEN "Neutro"
        WHEN "DIRECCIONADO - ATENCION" THEN "Neutro"
        WHEN "DIRECCIONADO - CRÉDITO" THEN "Neutro"
        WHEN "EXPCN" THEN "Neutro"
        WHEN "FINALIZADO FUERA DE HORÁRIO" THEN "Neutro"
        WHEN "FINALIZADO SIN INTERACCION" THEN "Neutro"
        WHEN "INCIDENTE EN ANDAMIENTO" THEN "Neutro"
        WHEN "INCIDENTE RESUELTO" THEN "Neutro"
        WHEN "REPORTE DIARIO EXP" THEN "Neutro"
        WHEN "Resuelto MKT N3" THEN "Neutro"
        WHEN "Resuelto N2 E-mail" THEN "Neutro"
        WHEN "Resuelto N2 MKT" THEN "Neutro"
        WHEN "Resuelto N3 E-mail" THEN "Neutro"
        WHEN "VALIDACION - TD LOCAL" THEN "Neutro"
        WHEN "VALIDACION DE LLAMADO" THEN "Neutro"
        WHEN "VALIDACION PLCOM" THEN "Neutro"

        ELSE "N1"
    END

ELSEIF [Data Contato Fuso] < #2026-10-01# THEN
    // --- REGRA DE MARÇO DE 2026 ATÉ SETEMBRO DE 2026 (Base: Nivel) ---
    CASE [Status de finalização]
        // CATEGORIA N2
        WHEN "DIRECCIONADO - PLCOM" THEN "N2"
        WHEN "DIRECCIONADO - TD LOCAL" THEN "N2"
        WHEN "INCIDENTE CRITICO" THEN "N2"
        WHEN "INCIDENTE CRÍTICO" THEN "N2"
        WHEN "INCIDENTE CRÃTICO" THEN "N2"
        WHEN "LLAMADO ABIERTO PARA N2" THEN "N2"
        WHEN "REAPERTURA DE LLAMADO" THEN "N2"

        // CATEGORIA NEUTRO
        WHEN "AJUSTE/ CORRECCION REALIZADO POR PLCOM" THEN "Neutro"
        WHEN "BUEN DIA/AGRADECIMIENTOS" THEN "Neutro"
        WHEN "CERRADO DESPUÉS DE HORAS" THEN "Neutro"
        WHEN "CONSULTA - TD LOCAL" THEN "Neutro"
        WHEN "CONSULTA CON PLCOM" THEN "Neutro"
        WHEN "CONTACTO SIN EXITO" THEN "Neutro"
        WHEN "DIRECCIONADO - ATENCION" THEN "Neutro"
        WHEN "DIRECCIONADO - CRÉDITO" THEN "Neutro"
        WHEN "EXPCN" THEN "Neutro"
        WHEN "FINALIZADO FUERA DE HORÁRIO" THEN "Neutro"
        WHEN "FINALIZADO SIN INTERACCION" THEN "Neutro"
        WHEN "INCIDENTE EN ANDAMIENTO" THEN "Neutro"
        WHEN "INCIDENTE RESUELTO" THEN "Neutro"
        WHEN "REPORTE DIARIO EXP" THEN "Neutro"
        WHEN "Resuelto MKT N3" THEN "Neutro"
        WHEN "Resuelto N2 E-mail" THEN "Neutro"
        WHEN "Resuelto N2 MKT" THEN "Neutro"
        WHEN "Resuelto N3 E-mail" THEN "Neutro"
        WHEN "VALIDACION - TD LOCAL" THEN "Neutro"
        WHEN "VALIDACION DE LLAMADO" THEN "Neutro"
        WHEN "VALIDACION PLCOM" THEN "Neutro"

        // CATEGORIA N1
        WHEN "ACTUALIZACION DE LA APP" THEN "N1"
        WHEN "ACTUALIZACIÓN DEL CARRITO" THEN "N1"
        WHEN "ACTUALIZACION DEL NAVEGADOR" THEN "N1"
        WHEN "BIOMETRIA V2 AUTOREGISTRO" THEN "N1"
        WHEN "CADASTRO DUPLICADO" THEN "N1"
        WHEN "CAMBIO DE EMAIL VOL" THEN "N1"
        WHEN "CAMBIO O REINICIO DE CELULAR/PC/NAVEGADOR" THEN "N1"
        WHEN "CREACION DE SU ESPACIO-CND" THEN "N1"
        WHEN "LIMPIEZA DE CACHE/HISTORIAL" THEN "N1"
        WHEN "LINK ENVIADO" THEN "N1"
        WHEN "REGISTRO CESADO/BLOQUEADO O DESACTIVADO" THEN "N1"
        WHEN "REGISTRO RECHAZADO" THEN "N1"
        WHEN "REHABILITAR TIENDA DIGITAL" THEN "N1"
        WHEN "REPORTE DE MOROSIDAD" THEN "N1"
        WHEN "RESET DE CONTRASENA" THEN "N1"
        WHEN "RESILIÊNCIA EN GSP" THEN "N1"
        WHEN "VALIDACION DE DATOS - REGISTRO" THEN "N1"
        WHEN "VALIDACIÓN DE DATOS- INDICADORES" THEN "N1"
        WHEN "VALIDACIÓN DE DATOS-BRM" THEN "N1"
        WHEN "VALIDACIÓN DE DATOS-CND" THEN "N1"
        WHEN "VALIDACION-CAMINO DE CRECIMIENTO" THEN "N1"
        WHEN "VALIDADO SIN INCONVENIENTES" THEN "N1"

        ELSE "Não considerar"
    END

ELSE
    // --- REGRA PARA OUTUBRO DE 2026 EM DIANTE (Base: Nivel Validar) ---
    CASE [Status de finalização]
        // CATEGORIA N2
        WHEN "DIRECCIONADO - PLCOM" THEN "N2"
        WHEN "DIRECCIONADO - TD LOCAL" THEN "N2"
        WHEN "INCIDENTE CRITICO" THEN "N2"
        WHEN "INCIDENTE CRÍTICO" THEN "N2"
        WHEN "INCIDENTE CRÃTICO" THEN "N2"
        WHEN "LLAMADO ABIERTO PARA N2" THEN "N2"
        WHEN "REAPERTURA DE LLAMADO" THEN "N2"

        // CATEGORIA NEUTRO
        WHEN "AJUSTE/ CORRECCION REALIZADO POR PLCOM" THEN "Neutro"
        WHEN "CONSULTA - TD LOCAL" THEN "Neutro"
        WHEN "CONSULTA CON PLCOM" THEN "Neutro"
        WHEN "DIRECCIONADO - ATENCION" THEN "Neutro"
        WHEN "DIRECCIONADO - CRÉDITO" THEN "Neutro"
        WHEN "FINALIZADO SIN INTERACCION" THEN "Neutro"
        WHEN "INCIDENTE EN ANDAMIENTO" THEN "Neutro"
        WHEN "Resuelto E-mail N3" THEN "Neutro"
        WHEN "Resuelto MKT N3" THEN "Neutro"
        WHEN "Resuelto N2 E-mail" THEN "Neutro"
        WHEN "Resuelto N2 MKT" THEN "Neutro"
        WHEN "Resuelto N3 E-mail" THEN "Neutro"
        WHEN "VALIDACION - TD LOCAL" THEN "Neutro"
        WHEN "VALIDACION DE LLAMADO" THEN "Neutro"
        WHEN "VALIDACION PLCOM" THEN "Neutro"
        WHEN "VALIDACION  PLCOM" THEN "Neutro"

        // CATEGORIA N1
        WHEN "ACTUALIZACION DE LA APP" THEN "N1"
        WHEN "ACTUALIZACIÓN DEL CARRITO" THEN "N1"
        WHEN "ACTUALIZACION DEL NAVEGADOR" THEN "N1"
        WHEN "BIOMETRIA V2 AUTOREGISTRO" THEN "N1"
        WHEN "BLANQUEO DEL REGISTRO" THEN "N1"
        WHEN "CADASTRO DUPLICADO" THEN "N1"
        WHEN "CAMBIO DE EMAIL VOL" THEN "N1"
        WHEN "CAMBIO O REINICIO DE CELULAR/PC/NAVEGADOR" THEN "N1"
        WHEN "CREACION DE SU ESPACIO-CND" THEN "N1"
        WHEN "LIMPIEZA DE CACHE/HISTORIAL" THEN "N1"
        WHEN "LINK ENVIADO" THEN "N1"
        WHEN "REGISTRO CESADO/BLOQUEADO O DESACTIVADO" THEN "N1"
        WHEN "REGISTRO RECHAZADO" THEN "N1"
        WHEN "REHABILITAR TIENDA DIGITAL" THEN "N1"
        WHEN "REPORTE DE MOROSIDAD" THEN "N1"
        WHEN "RESET DE CONTRASENA" THEN "N1"
        WHEN "RESILIÊNCIA EN GSP" THEN "N1"
        WHEN "SOLICITUD DE DATOS - APPS" THEN "N1"
        WHEN "VALIDACION DE DATOS - REGISTRO" THEN "N1"
        WHEN "VALIDACIÓN DE DATOS- INDICADORES" THEN "N1"
        WHEN "VALIDACIÓN DE DATOS-BRM" THEN "N1"
        WHEN "VALIDACIÓN DE DATOS-CND" THEN "N1"
        WHEN "VALIDACION-CAMINO DE CRECIMIENTO" THEN "N1"
        WHEN "VALIDADO SIN INCONVENIENTES" THEN "N1"

        // CATEGORIA NÃO CONSIDERAR
        WHEN "BUEN DIA/AGRADECIMIENTOS" THEN "Não considerar"
        WHEN "CERRADO DESPUÉS DE HORAS" THEN "Não considerar"
        WHEN "CONTACTO SIN EXITO" THEN "Não considerar"
        WHEN "EXPCN" THEN "Não considerar"
        WHEN "FINALIZADO FUERA DE HORÁRIO" THEN "Não considerar"
        WHEN "HEALTHCHECK" THEN "Não considerar"
        WHEN "INCIDENTE RESUELTO" THEN "Não considerar"
        WHEN "REPORTE DIARIO EXP" THEN "Não considerar"

        ELSE "Não mapeado"
    END
END
```
15. Excluir `Status de finalização` em ['"VALIDACION DE LLAMADO"']

→ [34] Limpar 8

## [23] Limpar 3 — Container

← [5] AppSheets Resenhas OIS

1. Remapear `Aplicación`: "App_Avon" ← "Avon"; "Resenhas Latam" ← "Resenhas LATAM", "Natura LATAM"; "App Natura" ← " Natura: Perfumes y Cosméticos"
2. Calcular `Fecha de la Respuesta 2`:

```
MAKEDATETIME(
    DATE(DATEADD('day', 1, [Fecha de la Respuesta])), 
    MAKETIME(2, 59, 59)
)
```
3. Renomear `Fecha de la Respuesta` → `Fecha de la Respuesta Original`
4. Renomear `Fecha de la Respuesta 2` → `Fecha de la Respuesta`

→ [35] Regra SLA

## [24] Manter apenas dia 16 e 17 — Container

_Descrição:_ Manter casos abertos em 16 e 17/03/2026

← [7] MKT Historico

1. Filtro de data `Data Contato` (datetime): **a partir de 2026-03-01 00:00:00**, sem nulos
2. Calcular `Manter`:

```
IF DATE([Data Contato]) = #2026-03-16# OR DATE([Data Contato]) = #2026-03-17# THEN 
    "Manter"
ELSE 
    "Remover"
END
```
3. Renomear `Protocolo` → `Protocol`
4. Remover colunas: `Empresa`
5. Remover colunas: `Nome`
6. Remover colunas: `CPF/CNPJ`, `Número do Contrato`, `Valor do Contrato`, `Código da Gerente`, `GV`, `Código CN`, `Sistema`
7. Remover colunas: `AlineWEL`
8. Remover colunas: `Detalhe do Sistema`
9. Remover colunas: `Setor Entrada`
10. Remover colunas: `Fone Cliente`
11. Remover colunas: `Tempo até ser atendido`, `Tempo do atendimento`, `Primeiro Tempo de Espera`, `Tempo Médio de Espera`, `Tempo de Operação`
12. Renomear `Setor Fim` → `Setor`
13. Remover colunas: `Qtde Mensagens`
14. Remover colunas: `Status de Classificação 1`
15. Renomear `Canal de Entrada` → `Canal`
16. Renomear `Data Contato` → `Data criação`
17. Remover colunas: `E-mail`
18. Remover colunas: `Observações`
19. Renomear `Encerrado em` → `Data conclusão`
20. Remover colunas: `Quantidade de Tickets`
21. Remover colunas: `Pedidos Finalizados`
22. Remover colunas: `Campos adicionais Web Chat`
23. Remover colunas: `Ticket`
24. Remover colunas: `Llamado`
25. Remover colunas: `Função do Sistema`
26. Remover colunas: `Solução Aplicada`
27. Remover colunas: `Pedido finalizado`
28. Remover colunas: `Status de Classificação`
29. Remover colunas: `Função do Sistema 1`
30. Renomear `Responsável` → `Operador`
31. Remover colunas: `Status de Finalização`
32. Renomear `Status de finalização` → `Status`
33. Remover colunas: `Cant. de Atendimientos`

→ [36] União de linhas 8

## [25] Remover dia 16 e 17 — Container

← [8] BASE MTK

1. Calcular `MANTER`:

```
IF DATE([Data Contato]) = #2026-03-16# OR DATE([Data Contato]) = #2026-03-17# THEN 
    "Remover"
ELSE 
    "Manter"
END
```
2. Excluir `MANTER` em ['"Remover"']
3. Remover colunas: `MANTER`
4. Excluir `Status de finalização` em ['"PROTOCOLO"']

→ [39] União de linhas 4

## [26] Limpar 15 — Container

← [9] MKT TICKETS

1. Remapear `PEDIDOS FINALIZADOS`: "SI" ← "si"; "NO" ← "no"; "" ← "no_se_aplica"

→ [37] União de colunas 8

## [27] Limpar 6 — Container

← [10] Ticket Medio Hispana

→ [38] Ticket Medio Hispana

## [28] Substitui por 1 — Container

← [11] Analitico

1. Remapear `Cant. de Atendimientos`: 1 ← null

→ [59] União de linhas 13

## [29]  — Container

← [12] MKT Histórico

→ [39] União de linhas 4

## [30] União de linhas 23 — SuperUnion

← [3] Novo Analitico; [14] MKT Analitico

**Union** das entradas acima (colunas com o mesmo nome se juntam; cria `Table Names`).

→ [40] Limpar 13

## [31] Limpar 1 — Container

← [16] Expurgo MKT

→ [88] Expurgo

## [32] União das Bases — SuperUnion

← [6] App Natura; [13] App_Avon; [17] Resenhas Latam; [18] Mi Negocio

**Union** das entradas acima (colunas com o mesmo nome se juntam; cria `Table Names`).

1. Remapear `Table Names`: "Mi Negocio" ← "reviews_reviews_net#natura#mine"; "App Natura" ← "reviews_reviews_net#natura#semp"

→ [41] SLA

## [33] Aging e Faixa de Aging — Container

← [19] SN

1. Calcular `Aging Encerrado`:

```
DATEDIFF('day', [Aberto], [Encerrado])
```
2. Calcular `Aging Abertura`:

```
DATEDIFF('day', [Aberto], TODAY())
```
3. Calcular `Faixa Aging Encerrado`:

```
IF [Aging Encerrado] = 0 THEN "EN EL DIA"
ELSEIF [Aging Encerrado] = 1 THEN "01 DIA"
ELSEIF [Aging Encerrado] = 2 THEN "02 DIAS"
ELSEIF [Aging Encerrado] = 3 THEN "03 DIAS"
ELSEIF [Aging Encerrado] >= 4 AND [Aging Encerrado] <= 10 THEN "04 A 10 DIAS"
ELSEIF [Aging Encerrado] >= 11 AND [Aging Encerrado] <= 20 THEN "11 A 20 DIAS"
ELSEIF [Aging Encerrado] >= 21 AND [Aging Encerrado] <= 30 THEN "21 A 30 DIAS"
ELSE "MAS QUE 30 DIAS"
END

```
4. Calcular `Faixa Aging Aberto`:

```
IF [Aging Abertura] = 0 THEN "EN EL DIA"
ELSEIF [Aging Abertura] = 1 THEN "01 DIA"
ELSEIF [Aging Abertura] = 2 THEN "02 DIAS"
ELSEIF [Aging Abertura] = 3 THEN "03 DIAS"
ELSEIF [Aging Abertura] >= 4 AND [Aging Abertura] <= 10 THEN "04 A 10 DIAS"
ELSEIF [Aging Abertura] >= 11 AND [Aging Abertura] <= 20 THEN "11 A 20 DIAS"
ELSEIF [Aging Abertura] >= 21 AND [Aging Abertura] <= 30 THEN "21 A 30 DIAS"
ELSE "MAS QUE 30 DIAS"
END

```

→ [42] Tradução

## [34] Limpar 8 — Container

← [22] Renomear colunas

→ [73] União de linhas 2

## [35] Regra SLA — Container

← [23] Limpar 3

1. Calcular `Início da Contagem SLA (Hispana)`:

```
// Se for Sábado (7) ou Domingo (1), joga para Segunda às 08:00.
// Nos outros dias, mantém 08:00 do mesmo dia.

IF DATEPART('weekday', [Fecha de la Respuesta]) = 7 THEN
    // Sábado -> Pula 2 dias para Segunda
    MAKEDATETIME(DATE(DATEADD('day', 2, [Fecha de la Respuesta])), MAKETIME(8,0,0))

ELSEIF DATEPART('weekday', [Fecha de la Respuesta]) = 1 THEN
    // Domingo -> Pula 1 dia para Segunda
    MAKEDATETIME(DATE(DATEADD('day', 1, [Fecha de la Respuesta])), MAKETIME(8,0,0))

ELSE
    // Dia Útil -> Mantém dia às 08:00
    MAKEDATETIME(DATE([Fecha de la Respuesta]), MAKETIME(8,0,0))
END
```
2. Calcular `Prazo SLA (Hispana)`:

```
// Se a contagem iniciar na Sexta (6), soma 3 dias (Sáb, Dom, Seg).
// Para qualquer outro dia (Seg a Qui), soma apenas 1 dia (24h).

CASE DATEPART('weekday', [Início da Contagem SLA (Hispana)])
    WHEN 6 THEN DATEADD('day', 3, [Início da Contagem SLA (Hispana)]) // Sexta -> Segunda
    ELSE DATEADD('day', 1, [Início da Contagem SLA (Hispana)])        // Outros -> Dia Seguinte
END
```
3. Calcular `Status SLA (Hispana)`:

```
IF NOT ISNULL([Fecha de la Respuesta EXP]) THEN
    // Cenário 1: Já responderam. Compara data real com prazo.
    IF [Fecha de la Respuesta EXP] <= [Prazo SLA (Hispana)] THEN "Dentro do SLA" ELSE "Fora do SLA" END
ELSE
    // Cenário 2: Ainda não responderam. Compara agora com prazo.
    IF NOW() <= [Prazo SLA (Hispana)] THEN "Dentro do SLA" ELSE "Fora do SLA" END
END
```
4. Renomear `F1` → `ID`

→ [43] AppSheets Resenhas OIS; [44] Resenhas

## [36] União de linhas 8 — SuperUnion

← [20] 16 17/03/26; [24] Manter apenas dia 16 e 17

**Union** das entradas acima (colunas com o mesmo nome se juntam; cria `Table Names`).

→ [45] Limpar 10

## [37] União de colunas 8 — SuperJoin

← [26] Limpar 15 (Left); [21] Limpar 17 (Right)

**Join left**: esquerda = [26] Limpar 15, direita = [21] Limpar 17

Condição: `esq.[Função do Sistema] == dir.[Função do Sistema - Ticket]`

→ [46] Limpar 18

## [38] Ticket Medio Hispana — PublishExtract

← [27] Limpar 6

**Saída:** `4. DATASOURCES/Ticket Medio Hispana`

## [39] União de linhas 4 — SuperUnion

← [25] Remover dia 16 e 17; [29] 

**Union** das entradas acima (colunas com o mesmo nome se juntam; cria `Table Names`).

1. Remover colunas: `Table Names`

→ [47] Corrigir Colunas

## [40] Limpar 13 — Container

← [30] União de linhas 23

1. Renomear `Função do Sistema` → `Função do Sistema 2`
2. Renomear `Status de Classificação` → `Status de Classificação 2`
3. Calcular `Status de Classificação`:

```
IF ISNULL([Status de Classificação 1]) THEN
	[Status de Classificação 2]
ELSE
	[Status de Classificação 1]
END
```
4. Calcular `Função do Sistema`:

```
IF ISNULL([Função do Sistema 1]) THEN
	[Função do Sistema 2]
ELSE
	[Função do Sistema 1]
END
```
5. Renomear `Protocolo` → `Protocolo analitico`
6. Manter só: `Status de Classificação`, `Função do Sistema`, `Protocolo analitico`

→ [61] União de linhas 17

## [41] SLA — Container

← [32] União das Bases

1. Mudar tipo: `Developer Reply Date and Time` → datetime
2. Mudar tipo: `Review Last Update Date and Time` → datetime
3. Mudar tipo: `Review Submit Date and Time` → datetime
4. Calcular `_Dia da Semana da Resenha`:

```
DATEPART('weekday', [Review Last Update Date and Time])
```
5. Calcular `_Hora da Resenha`:

```
DATEPART('hour', [Review Last Update Date and Time])
```
6. Calcular `Início da Contagem SLA`:

```
// Cenário 1: Resenha recebida no fim de semana (Sábado após 03:00 ou Domingo o dia todo)
// A contagem deve iniciar na próxima Segunda-feira às 08:00.
IF ([_Dia da Semana da Resenha] = 7 AND [_Hora da Resenha] >= 3) OR [_Dia da Semana da Resenha] = 1 THEN
    MAKEDATETIME(
    DATE(DATEADD('day', IF [_Dia da Semana da Resenha] = 7 THEN 2 ELSE 1 END, DATE([Review Last Update Date and Time]))),
    MAKETIME(8,0,0)
    )

// Cenário 2: Resenha recebida na "pausa" de um dia útil (Seg a Sex, entre 03:00 e 07:59)
// A contagem deve iniciar às 08:00 do mesmo dia.
ELSEIF ([_Dia da Semana da Resenha] >= 2 AND [_Dia da Semana da Resenha] <= 6) AND ([_Hora da Resenha] >= 3 AND [_Hora da Resenha] < 8) THEN
    MAKEDATETIME(DATE([Review Last Update Date and Time]), MAKETIME(8,0,0))

// Cenário 3: Resenha recebida durante o horário de trabalho.
// A contagem inicia imediatamente.
ELSE
    [Review Last Update Date and Time]
END
```
7. Calcular `Elegibilidade SLA`:

```
// Verifica se o campo de texto da resenha está vazio ou nulo.
IF ISNULL([Review Text]) OR [Review Text] = "" THEN
    'Não Aplicável'
ELSE
    'Aplicável'
END
```
8. Calcular `Prazo SLA`:

```
// Adiciona 1 dia útil ao Início da Contagem, pulando o fim de semana se necessário.
// (Por exemplo, de sexta para segunda).
DATEADD(
    'day',
    1 + (FLOOR((DATEPART('weekday', [Início da Contagem SLA]) - 1) / 5) * 2),
    [Início da Contagem SLA]
)
```
9. Calcular `Status SLA`:

```
// Passo 1: Primeiro, verifica se o SLA é aplicável.
IF [Elegibilidade SLA] = 'Não Aplicável' THEN
    'Não Aplicável'

// Passo 2: Se for aplicável, aplica a mesma lógica de antes.
// Caso 2.1: Foi respondido DENTRO do prazo.
ELSEIF NOT ISNULL([Developer Reply Date and Time]) AND [Developer Reply Date and Time] <= [Prazo SLA] THEN
    'Dentro do SLA'

// Caso 2.2: O prazo já estourou.
// (Se a resposta veio atrasada OU se não há resposta e o prazo já passou)
ELSEIF ([Developer Reply Date and Time] > [Prazo SLA]) OR (ISNULL([Developer Reply Date and Time]) AND [Prazo SLA] < NOW()) THEN
    'Fora do SLA'

// Caso 2.3: Ainda não foi respondido, mas o prazo ainda não venceu.
ELSE
    'Pendente'
END
```
10. Remapear `Table Names`: "Resenhas Latam" ← "in"; "App Avon" ← "reviews_reviews_com#naturaeco#a"

→ [48] Status Resposta

## [42] Tradução — Container

← [33] Aging e Faixa de Aging

1. Remapear `Estado`: "En Progreso" ← "Em andamento"; "En espera" ← "Em espera"; "Cerrado" ← "Encerrado"; "Nuevo" ← "Novo"; "Resuelto" ← "Resolvido"
2. Renomear `Aberto` → `Abierto`
3. Renomear `Descrição resumida` → `Descripción Resumida`
4. Renomear `Prioridade` → `Prioridad`
5. Renomear `Estado` → `Estatus`
6. Renomear `Grupo de atribuição` → `Grupo de Asignación`
7. Renomear `Atualizado em` → `Actualizado en`
8. Renomear `Atualizado por` → `Actualizado por`
9. Renomear `Criado por` → `Creado por`
10. Renomear `Encerrado` → `Cerrado`
11. Renomear `Resolvido` → `Resuelto`
12. Renomear `Tipo de tarefa` → `Tipo de tarea`
13. Renomear `Serviço` → `Servicio`
14. Renomear `Motivo para estar em espera` → `Razón para estar en Espera`
15. Renomear `Em qual país ocorre o incidente?` → `País`
16. Renomear `Nome do Solicitante` → `Nombre del Solicitante`
17. Renomear `Quem está sendo impactado?` → `Quién fue Impactado`
18. Renomear `Qual a marca impactada?` → `Marca Impactada`
19. Calcular `Semana Abierto`:

```
datepart('week',[Abierto])
```
20. Calcular `Semana Cerrado`:

```
DATEPART('week', [Cerrado])
```

→ [49] Resumen

## [43] AppSheets Resenhas OIS — PublishExtract

← [35] Regra SLA

**Saída:** `4. DATASOURCES/AppSheets Resenhas OIs`

## [44] Resenhas — Container

← [35] Regra SLA

1. Renomear `Responsable de la Respuesta` → `Responsável`
2. Manter só: `ID`, `Pais`, `Responsável`, `Fecha de la Respuesta EXP`
3. Renomear `Fecha de la Respuesta EXP` → `Data`
4. Renomear `ID` → `Protocolo`
5. Calcular `Valor Atendimento`:

```
1
```

→ [111] União de linhas 11

## [45] Limpar 10 — Container

← [36] União de linhas 8

1. Remover colunas: `Table Names`
2. Excluir `Status` em ['"PROTOCOLO"']

→ [50] Status Inelegíveis

## [46] Limpar 18 — Container

← [37] União de colunas 8

1. Remover colunas: `Função do Sistema`
2. Remover colunas: `Função do Sistema - Ticket`
3. Renomear `Função do Sistema - Analitico` → `Função do Sistema`
4. Renomear `Usuário Responsável` → `Responsável`
5. Renomear `ID do Ticket` → `Protocolo`
6. Renomear `Setor do Atendimento` → `Setor Fim`
7. Renomear `Status de Finalização` → `Status de finalização`
8. Duplicar `Data de Criação do Ticket-1`:

```
[Data de Criação do Ticket]
```
9. Renomear `Data de Criação do Ticket-1` → `Data Contato Fuso`
10. Renomear `PEDIDOS FINALIZADOS` → `Pedidos Finalizados`
11. Calcular `Tipo`:

```
IF [Setor Fim] = "APP NATURA" THEN "Email"
ELSEIF [Setor Fim] = "APP Natura Latam" THEN "Email"
ELSEIF [Setor Fim] = "AR" THEN "WhatsApp"
ELSEIF [Setor Fim] = "AR- Email" THEN "Email"
ELSEIF [Setor Fim] = "AR GV" THEN "WhatsApp"
ELSEIF [Setor Fim] = "ATENCIÓN" THEN "WhatsApp"
ELSEIF [Setor Fim] = "ATENDIMIENTO" THEN "WhatsApp"
ELSEIF [Setor Fim] = "CL" THEN "WhatsApp"
ELSEIF [Setor Fim] = "CL GV" THEN "WhatsApp"
ELSEIF [Setor Fim] = "CL - Email" THEN "Email"
ELSEIF [Setor Fim] = "LNN EC" THEN "WhatsApp"
ELSEIF [Setor Fim] = "LNN EC - Email" THEN "Email"
ELSEIF [Setor Fim] = "CO" THEN "WhatsApp"
ELSEIF [Setor Fim] = "CO GV" THEN "WhatsApp"
ELSEIF [Setor Fim] = "CO - Email" THEN "Email"
ELSEIF [Setor Fim] = "CO-CELULAR" THEN "Remover"
ELSEIF [Setor Fim] = "CO-SOPORTE" THEN "Remover"
ELSEIF [Setor Fim] = "EC" THEN "WhatsApp"
ELSEIF [Setor Fim] = "EC GV" THEN "WhatsApp"
ELSEIF [Setor Fim] = "EC - Email" THEN "Email"
ELSEIF [Setor Fim] = "EX" THEN "WhatsApp"
ELSEIF [Setor Fim] = "FV-AYUDA" THEN "Remover"
ELSEIF [Setor Fim] = "GV CL" THEN "WhatsApp"
ELSEIF [Setor Fim] = "GVs CHILE" THEN "WhatsApp"
ELSEIF [Setor Fim] = "MI NEGOCIO" THEN "Email"
ELSEIF [Setor Fim] = "MX" THEN "WhatsApp"
ELSEIF [Setor Fim] = "MX - Email" THEN "Email"
ELSEIF [Setor Fim] = "MX GV" THEN "WhatsApp"
ELSEIF [Setor Fim] = "PE" THEN "WhatsApp"
ELSEIF [Setor Fim] = "PE- Email" THEN "Email"
ELSEIF [Setor Fim] = "PE GV" THEN "WhatsApp"
ELSEIF [Setor Fim] = "PE-CELULAR" THEN "Remover"
ELSEIF [Setor Fim] = "PE-LIDER" THEN "Remover"
ELSEIF [Setor Fim] = "APP AVON" THEN "Email"
ELSE NULL
END

```
12. Calcular `Pais`:

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
ELSEIF [Setor Fim] = "LNN EC" THEN "Ecuador"
ELSEIF [Setor Fim] = "LNN EC - Email" THEN "Ecuador"
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
ELSE NULL
END
```
13. Calcular `Nivel`:

```
IF [Data Contato Fuso] < #2026-03-01# THEN
    // --- REGRA PARA DATAS ANTERIORES A MARÇO 2026 (Base: Nivel) ---
    CASE [Status de finalização]
        // CATEGORIA N2
        WHEN "DIRECCIONADO - PLCOM" THEN "N2"
        WHEN "DIRECCIONADO - TD LOCAL" THEN "N2"
        WHEN "INCIDENTE CRITICO" THEN "N2"
        WHEN "INCIDENTE CRÍTICO" THEN "N2"
        WHEN "INCIDENTE CRÃTICO" THEN "N2"
        WHEN "LLAMADO ABIERTO PARA N2" THEN "N2"
        WHEN "REAPERTURA DE LLAMADO" THEN "N2"

        // CATEGORIA NEUTRO
        WHEN "AJUSTE/ CORRECCION REALIZADO POR PLCOM" THEN "Neutro"
        WHEN "BUEN DIA/AGRADECIMIENTOS" THEN "Neutro"
        WHEN "CERRADO DESPUÉS DE HORAS" THEN "Neutro"
        WHEN "CONSULTA - TD LOCAL" THEN "Neutro"
        WHEN "CONSULTA CON PLCOM" THEN "Neutro"
        WHEN "CONTACTO SIN EXITO" THEN "Neutro"
        WHEN "DIRECCIONADO - ATENCION" THEN "Neutro"
        WHEN "DIRECCIONADO - CRÉDITO" THEN "Neutro"
        WHEN "EXPCN" THEN "Neutro"
        WHEN "FINALIZADO FUERA DE HORÁRIO" THEN "Neutro"
        WHEN "FINALIZADO SIN INTERACCION" THEN "Neutro"
        WHEN "INCIDENTE EN ANDAMIENTO" THEN "Neutro"
        WHEN "INCIDENTE RESUELTO" THEN "Neutro"
        WHEN "REPORTE DIARIO EXP" THEN "Neutro"
        WHEN "Resuelto MKT N3" THEN "Neutro"
        WHEN "Resuelto N2 E-mail" THEN "Neutro"
        WHEN "Resuelto N2 MKT" THEN "Neutro"
        WHEN "Resuelto N3 E-mail" THEN "Neutro"
        WHEN "VALIDACION - TD LOCAL" THEN "Neutro"
        WHEN "VALIDACION DE LLAMADO" THEN "Neutro"
        WHEN "VALIDACION PLCOM" THEN "Neutro"

        ELSE "N1"
    END

ELSEIF [Data Contato Fuso] < #2026-10-01# THEN
    // --- REGRA DE MARÇO DE 2026 ATÉ SETEMBRO DE 2026 (Base: Nivel) ---
    CASE [Status de finalização]
        // CATEGORIA N2
        WHEN "DIRECCIONADO - PLCOM" THEN "N2"
        WHEN "DIRECCIONADO - TD LOCAL" THEN "N2"
        WHEN "INCIDENTE CRITICO" THEN "N2"
        WHEN "INCIDENTE CRÍTICO" THEN "N2"
        WHEN "INCIDENTE CRÃTICO" THEN "N2"
        WHEN "LLAMADO ABIERTO PARA N2" THEN "N2"
        WHEN "REAPERTURA DE LLAMADO" THEN "N2"

        // CATEGORIA NEUTRO
        WHEN "AJUSTE/ CORRECCION REALIZADO POR PLCOM" THEN "Neutro"
        WHEN "BUEN DIA/AGRADECIMIENTOS" THEN "Neutro"
        WHEN "CERRADO DESPUÉS DE HORAS" THEN "Neutro"
        WHEN "CONSULTA - TD LOCAL" THEN "Neutro"
        WHEN "CONSULTA CON PLCOM" THEN "Neutro"
        WHEN "CONTACTO SIN EXITO" THEN "Neutro"
        WHEN "DIRECCIONADO - ATENCION" THEN "Neutro"
        WHEN "DIRECCIONADO - CRÉDITO" THEN "Neutro"
        WHEN "EXPCN" THEN "Neutro"
        WHEN "FINALIZADO FUERA DE HORÁRIO" THEN "Neutro"
        WHEN "FINALIZADO SIN INTERACCION" THEN "Neutro"
        WHEN "INCIDENTE EN ANDAMIENTO" THEN "Neutro"
        WHEN "INCIDENTE RESUELTO" THEN "Neutro"
        WHEN "REPORTE DIARIO EXP" THEN "Neutro"
        WHEN "Resuelto MKT N3" THEN "Neutro"
        WHEN "Resuelto N2 E-mail" THEN "Neutro"
        WHEN "Resuelto N2 MKT" THEN "Neutro"
        WHEN "Resuelto N3 E-mail" THEN "Neutro"
        WHEN "VALIDACION - TD LOCAL" THEN "Neutro"
        WHEN "VALIDACION DE LLAMADO" THEN "Neutro"
        WHEN "VALIDACION PLCOM" THEN "Neutro"

        // CATEGORIA N1 (Específica da nova planilha)
        WHEN "ACTUALIZACION DE LA APP" THEN "N1"
        WHEN "ACTUALIZACIÓN DEL CARRITO" THEN "N1"
        WHEN "ACTUALIZACION DEL NAVEGADOR" THEN "N1"
        WHEN "BIOMETRIA V2 AUTOREGISTRO" THEN "N1"
        WHEN "CADASTRO DUPLICADO" THEN "N1"
        WHEN "CAMBIO DE EMAIL VOL" THEN "N1"
        WHEN "CAMBIO O REINICIO DE CELULAR/PC/NAVEGADOR" THEN "N1"
        WHEN "CREACION DE SU ESPACIO-CND" THEN "N1"
        WHEN "LIMPIEZA DE CACHE/HISTORIAL" THEN "N1"
        WHEN "LINK ENVIADO" THEN "N1"
        WHEN "REGISTRO CESADO/BLOQUEADO O DESACTIVADO" THEN "N1"
        WHEN "REGISTRO RECHAZADO" THEN "N1"
        WHEN "REHABILITAR TIENDA DIGITAL" THEN "N1"
        WHEN "REPORTE DE MOROSIDAD" THEN "N1"
        WHEN "RESET DE CONTRASENA" THEN "N1"
        WHEN "RESILIÊNCIA EN GSP" THEN "N1"
        WHEN "VALIDACION DE DATOS - REGISTRO" THEN "N1"
        WHEN "VALIDACIÓN DE DATOS- INDICADORES" THEN "N1"
        WHEN "VALIDACIÓN DE DATOS-BRM" THEN "N1"
        WHEN "VALIDACIÓN DE DATOS-CND" THEN "N1"
        WHEN "VALIDACION-CAMINO DE CRECIMIENTO" THEN "N1"
        WHEN "VALIDADO SIN INCONVENIENTES" THEN "N1"

        ELSE "Não considerar"
    END

ELSE
    // --- REGRA PARA OUTUBRO DE 2026 EM DIANTE (Base: Nivel Validar) ---
    CASE [Status de finalização]
        // CATEGORIA N2
        WHEN "DIRECCIONADO - PLCOM" THEN "N2"
        WHEN "DIRECCIONADO - TD LOCAL" THEN "N2"
        WHEN "INCIDENTE CRITICO" THEN "N2"
        WHEN "INCIDENTE CRÍTICO" THEN "N2"
        WHEN "INCIDENTE CRÃTICO" THEN "N2"
        WHEN "LLAMADO ABIERTO PARA N2" THEN "N2"
        WHEN "REAPERTURA DE LLAMADO" THEN "N2"

        // CATEGORIA NEUTRO
        WHEN "AJUSTE/ CORRECCION REALIZADO POR PLCOM" THEN "Neutro"
        WHEN "CONSULTA - TD LOCAL" THEN "Neutro"
        WHEN "CONSULTA CON PLCOM" THEN "Neutro"
        WHEN "DIRECCIONADO - ATENCION" THEN "Neutro"
        WHEN "DIRECCIONADO - CRÉDITO" THEN "Neutro"
        WHEN "FINALIZADO SIN INTERACCION" THEN "Neutro"
        WHEN "INCIDENTE EN ANDAMIENTO" THEN "Neutro"
        WHEN "Resuelto E-mail N3" THEN "Neutro"
        WHEN "Resuelto MKT N3" THEN "Neutro"
        WHEN "Resuelto N2 E-mail" THEN "Neutro"
        WHEN "Resuelto N2 MKT" THEN "Neutro"
        WHEN "Resuelto N3 E-mail" THEN "Neutro"
        WHEN "VALIDACION - TD LOCAL" THEN "Neutro"
        WHEN "VALIDACION DE LLAMADO" THEN "Neutro"
        WHEN "VALIDACION PLCOM" THEN "Neutro"
        WHEN "VALIDACION  PLCOM" THEN "Neutro"

        // CATEGORIA N1
        WHEN "ACTUALIZACION DE LA APP" THEN "N1"
        WHEN "ACTUALIZACIÓN DEL CARRITO" THEN "N1"
        WHEN "ACTUALIZACION DEL NAVEGADOR" THEN "N1"
        WHEN "BIOMETRIA V2 AUTOREGISTRO" THEN "N1"
        WHEN "BLANQUEO DEL REGISTRO" THEN "N1"
        WHEN "CADASTRO DUPLICADO" THEN "N1"
        WHEN "CAMBIO DE EMAIL VOL" THEN "N1"
        WHEN "CAMBIO O REINICIO DE CELULAR/PC/NAVEGADOR" THEN "N1"
        WHEN "CREACION DE SU ESPACIO-CND" THEN "N1"
        WHEN "LIMPIEZA DE CACHE/HISTORIAL" THEN "N1"
        WHEN "LINK ENVIADO" THEN "N1"
        WHEN "REGISTRO CESADO/BLOQUEADO O DESACTIVADO" THEN "N1"
        WHEN "REGISTRO RECHAZADO" THEN "N1"
        WHEN "REHABILITAR TIENDA DIGITAL" THEN "N1"
        WHEN "REPORTE DE MOROSIDAD" THEN "N1"
        WHEN "RESET DE CONTRASENA" THEN "N1"
        WHEN "RESILIÊNCIA EN GSP" THEN "N1"
        WHEN "SOLICITUD DE DATOS - APPS" THEN "N1"
        WHEN "VALIDACION DE DATOS - REGISTRO" THEN "N1"
        WHEN "VALIDACIÓN DE DATOS- INDICADORES" THEN "N1"
        WHEN "VALIDACIÓN DE DATOS-BRM" THEN "N1"
        WHEN "VALIDACIÓN DE DATOS-CND" THEN "N1"
        WHEN "VALIDACION-CAMINO DE CRECIMIENTO" THEN "N1"
        WHEN "VALIDADO SIN INCONVENIENTES" THEN "N1"

        // CATEGORIA NÃO CONSIDERAR
        WHEN "BUEN DIA/AGRADECIMIENTOS" THEN "Não considerar"
        WHEN "CERRADO DESPUÉS DE HORAS" THEN "Não considerar"
        WHEN "CONTACTO SIN EXITO" THEN "Não considerar"
        WHEN "EXPCN" THEN "Não considerar"
        WHEN "FINALIZADO FUERA DE HORÁRIO" THEN "Não considerar"
        WHEN "HEALTHCHECK" THEN "Não considerar"
        WHEN "INCIDENTE RESUELTO" THEN "Não considerar"
        WHEN "REPORTE DIARIO EXP" THEN "Não considerar"

        ELSE "Não mapeado"
    END
END
```

→ [51] Whats; [52] Email

## [47] Corrigir Colunas — Container

← [39] União de linhas 4

1. Renomear `Função do Sistema` → `Função do Sistema 2`
2. Calcular `Função do Sistema`:

```
IF ISNULL([Função do Sistema 1]) THEN
	[Função do Sistema 2]
ELSE
	[Função do Sistema 1]
END
```
3. Remover colunas: `Função do Sistema 2`

→ [53] Corrigir Colunas

## [48] Status Resposta — Container

← [41] SLA

1. Duplicar `Review Last Update Date and Time-1`:

```
[Review Last Update Date and Time]
```
2. Renomear `Review Last Update Date and Time-1` → `Data`
3. Calcular `Status Resposta`:

```
// Verifica o status da resenha com base nos comentários e respostas

// 1. Primeiro, verifica se o usuário NÃO escreveu um comentário.
IF ISNULL([Review Text]) OR [Review Text] = "" THEN
    "Evaluación sin Comentarios"

// 2. Se existe um comentário, verifica se a operação AINDA NÃO respondeu.
ELSEIF ISNULL([Developer Reply Text]) OR [Developer Reply Text] = "" THEN
    "Comentario sin respuesta"

// 3. Se nenhuma das anteriores for verdade, significa que há um comentário E uma resposta.
ELSE
    "Comentario Respondido"
END
```

→ [54] Resenhas Hispana

## [49] Resumen — Container

← [42] Tradução

1. Calcular `Resumen`:

```
// Agrupa as descrições em categorias usando a função CONTAINS.
// A ordem é importante: regras mais específicas devem vir antes de regras mais gerais.

IF CONTAINS([Descripción Resumida], "LEGO-GPP(cadastro) - Cad CN CNO") THEN "LEGO-GPP - CAD CN CNO"
ELSEIF CONTAINS([Descripción Resumida], "LEGO-GPP(cadastro) - Backoffice") THEN "LEGO-GPP - BACKOFFICE"
ELSEIF CONTAINS([Descripción Resumida], "LEGO-GSP-Captación - Captación") THEN "LEGO-GSP - CAPTACIÓN"
ELSEIF CONTAINS([Descripción Resumida], "LEGO-GSP-Captación - Dirección") THEN "LEGO-GSP - DIRECCIÓN"
ELSEIF CONTAINS([Descripción Resumida], "LEGO-GSP-Captación - Integración Producto GERA") THEN "LEGO-GSP - INTEGRACIÓN PRODUCTO GERA"
ELSEIF CONTAINS([Descripción Resumida], "LEGO-GSP-Captación - Kit inicio") THEN "LEGO-GSP - KIT INICIO"
ELSEIF CONTAINS([Descripción Resumida], "LEGO-GSP-Captación - Pedido SAC") THEN "LEGO-GSP - PEDIDO SAC"
ELSEIF CONTAINS([Descripción Resumida], "LEGO-GSP-Captación - Reportes") THEN "LEGO-GSP - REPORTES"
ELSEIF CONTAINS([Descripción Resumida], "LEGO-Plataforma Comercial-BRM - Alocação Consultora") THEN "LEGO-BRM - ALOCACIÓN CONSULTORA"
ELSEIF CONTAINS([Descripción Resumida], "LEGO-Plataforma Comercial-BRM - Divergência Estrutura") THEN "LEGO-BRM - DIVERGENCIA ESTRUCTURA"
ELSEIF CONTAINS([Descripción Resumida], "LEGO-Plataforma Comercial-BRM - Gestão de Grupos") THEN "LEGO-BRM - GESTIÓN DE GRUPOS"
ELSEIF CONTAINS([Descripción Resumida], "LEGO-Plataforma Comercial-BRM - Relatórios (Reportes)") THEN "LEGO-BRM - REPORT"
ELSEIF CONTAINS([Descripción Resumida], "LEGO-Plataforma Comercial-BRM - Status Comercial") THEN "LEGO-BRM - STATUS COMERCIAL"
ELSEIF CONTAINS([Descripción Resumida], "LEGO - Plataforma Comercial") THEN "LEGO - PLATAFORMA COMERCIAL"
ELSEIF CONTAINS([Descripción Resumida], "Cadastro - Backoffice") THEN "CADASTRO - BACKOFFICE"
ELSEIF CONTAINS([Descripción Resumida], "Cadastro - Caduni") THEN "CADASTRO - CADUNI"
ELSEIF CONTAINS([Descripción Resumida], "Mi Negócio - Beneficio") THEN "MI NEGOCIO - BENEFICIO"
ELSEIF CONTAINS([Descripción Resumida], "Mi Negócio - Camino de Crecimiento") THEN "MI NEGOCIO - CAMINO DE CRECIMIENTO"
ELSEIF CONTAINS([Descripción Resumida], "Mi Negócio - Cards") THEN "MI NEGOCIO - CARDS"
ELSEIF CONTAINS([Descripción Resumida], "Mi Negócio - Escuela Natura Y Avon") THEN "MI NEGOCIO - ESCUela NATURA Y AVON"
ELSEIF CONTAINS([Descripción Resumida], "Mi Negócio - Ganancia") THEN "MI NEGOCIO - GANANCIA"
ELSEIF CONTAINS([Descripción Resumida], "Mi Negócio - Home") THEN "MI NEGOCIO - HOME"
ELSEIF CONTAINS([Descripción Resumida], "Mi Negócio - Indicador") THEN "MI NEGOCIO - INDICADOR"
ELSEIF CONTAINS([Descripción Resumida], "Mi Negócio - Login") THEN "MI NEGOCIO - LOGIN"
ELSEIF CONTAINS([Descripción Resumida], "Mi Negócio - Menu") THEN "MI NEGOCIO - MENU"
ELSEIF CONTAINS([Descripción Resumida], "Mi Negócio - Meus Pedidos") THEN "MI NEGOCIO - MEUS PEDIDOS"
ELSEIF CONTAINS([Descripción Resumida], "Mi Negócio - Mis Posteos") THEN "MI NEGOCIO - MIS POSTEOS"
ELSEIF CONTAINS([Descripción Resumida], "Mi Negócio - Natura Reconoce") THEN "MI NEGOCIO - NATURA RECONOCE"
ELSEIF CONTAINS([Descripción Resumida], "Mi Negócio - Perfil") THEN "MI NEGOCIO - PERFIL"
ELSEIF CONTAINS([Descripción Resumida], "Mi Negócio - Reporte") THEN "MI NEGOCIO - REPORT"
ELSEIF CONTAINS([Descripción Resumida], "Mi Negócio - Revistas") THEN "MI NEGOCIO - REVISTAS"
ELSEIF CONTAINS([Descripción Resumida], "Mi Negócio - Venta Online") THEN "MI NEGOCIO - VENTA ONLINE"
ELSEIF CONTAINS([Descripción Resumida], "Panel CB-Commerce - Home") THEN "PANEL CB-COMMERCE - HOME"
ELSEIF CONTAINS([Descripción Resumida], "Rede Natura - Cadastro") THEN "REDE NATURA - CADASTRO"
ELSEIF CONTAINS([Descripción Resumida], "Rede Natura - Painel") THEN "REDE NATURA - PAINEL"
ELSEIF CONTAINS([Descripción Resumida], "Rede Natura - REDE NATURA") THEN "REDE NATURA"
ELSEIF CONTAINS([Descripción Resumida], "SalesForce") THEN "SALESFORCE"
ELSEIF CONTAINS([Descripción Resumida], "Site CF") THEN "SITE CF"
ELSEIF CONTAINS([Descripción Resumida], "Telefonia - Ramal") THEN "TELEFONIA - RAMAL"
ELSEIF CONTAINS([Descripción Resumida], "Tiendas") THEN "TIENDAS"
ELSE "NO MAPEADO"
END
```
2. Excluir `País` em [None]
3. Excluir `País` em ['"Argentina, Chile, México, Peru"']
4. Excluir `País` em ['"Argentina, Colômbia, Equador, México"']
5. Excluir `País` em ['"Argentina, México"']
6. Excluir `País` em ['"Brasil"']
7. Excluir `País` em ['"Brasil, Chile"']
8. Excluir `País` em ['"Chile, Colômbia, Equador, México, Peru"']
9. Excluir `País` em ['"Chile, Colômbia, Peru"']
10. Excluir `País` em ['"Colômbia, México"']
11. Excluir `País` em ['"Colômbia, Peru"']
12. Excluir `País` em ['"El Salvador"']

→ [55] Limpar 4

## [50] Status Inelegíveis — Container

_Descrição:_ Remoção de Status inelegíveis conforme Status excluídos da base Analítico

← [45] Limpar 10

1. Calcular `Regra Status`:

```
CASE [Status]
WHEN "BUEN DIA/AGRADECIMIENTOS" THEN "Excluir"
WHEN "BUEN DIA/AGRADECIMIENTOS - CLASSIFICAÇÃO" THEN "Excluir"
WHEN "EXPCN" THEN "Excluir"
WHEN "EXPCN - CLASSIFICAÃ‡ÃƒO" THEN "Excluir"
WHEN "EXPCN - CLASSIFICAÇÃO" THEN "Excluir"
WHEN "test - EXCLUÍDO" THEN "Excluir"
WHEN "AJUSTE/ CORRECCION REALIZADO POR PLCOM" THEN "Excluir"
WHEN "APERTURA DE LLAMADO-N2 - EXCLUÍDO" THEN "Excluir"
WHEN "CAMBIO DE PC/CELULAR/NAVEGADOR - EXCLUÍDO" THEN "Excluir"
WHEN "CELULAR- RED" THEN "Excluir"
WHEN "CELULAR-HARDWARE" THEN "Excluir"
WHEN "CELULAR-REASIGNACION" THEN "Excluir"
WHEN "CENTRAL DE COMANDO - EXCLUÍDO" THEN "Excluir"
WHEN "CIERRE DE PLANTON - EXCLUÍDO" THEN "Excluir"
WHEN "CODIGO RECIBIDO NO FUNCIONA/ EXPIRO - EXCLUÍDO" THEN "Excluir"
WHEN "CONFIGURACION DE CONTACTOS" THEN "Excluir"
WHEN "CONFIGURACIÓN DE E-MAIL" THEN "Excluir"
WHEN "CONFIGURACIÓN DE EQUIPO CELULAR" THEN "Excluir"
WHEN "CONFIGURACION DE MICROSOFT AUTENTICADOR MFA" THEN "Excluir"
WHEN "Contato sin exito - EXCLUÍDO" THEN "Excluir"
WHEN "CORREO-CELULAR" THEN "Excluir"
WHEN "DIRECCIONADO CON EL CAN/SV/GN/GDN/LN - EXCLUÍDO" THEN "Excluir"
WHEN "ENVIO DE BOLETO PARA PAGO - EXCLUÍDO" THEN "Excluir"
WHEN "EQUIPO AVERIADO" THEN "Excluir"
WHEN "FALLA APLICACIONES/S.O" THEN "Excluir"
WHEN "FALTA DE  INFORMACIÓN - EXCLUÍDO" THEN "Excluir"
WHEN "Finaliza - Respuesta Negativa Pro Ativo - EXCLUÍDO" THEN "Excluir"
WHEN "FINALIZA NW" THEN "Excluir"
WHEN "Finalizado New Way" THEN "Excluir"
WHEN "Imagen error - EXCLUÍDO" THEN "Excluir"
WHEN "INCIDENTE CRÃTICO" THEN "Excluir"
WHEN "INCONVENIENTES CON  CORREO OUTLOOK NATURA" THEN "Excluir"
WHEN "INCONVENIENTES CON EQUIPO CELULAR" THEN "Excluir"
WHEN "INCONVENIENTES CON LA OPERADORA TELEFONICA - EXCLUÍDO" THEN "Excluir"
WHEN "INCONVENIENTES CON MICROSOFT TEAMS" THEN "Excluir"
WHEN "LA PLATAFORMA NO RECONOCE EL DOCUMENTO QUE SE INTENTA SUBIR - EXCLUÍDO" THEN "Excluir"
WHEN "MFA CAMPAÑA - EXCLUÍDO" THEN "Excluir"
WHEN "N1-ACCESO A PERSONA NO PERMITIDO - EXCLUÍDO" THEN "Excluir"
WHEN "N1-CADUNI ORIENTACION - EXCLUÍDO" THEN "Excluir"
WHEN "N1-CANTIDAD MAXIMA DE TITULOS PENDIENTES EXCEDIDOS - EXCLUÍDO" THEN "Excluir"
WHEN "N1-CARRITO EN CONVERSION - EXCLUÍDO" THEN "Excluir"
WHEN "N1-CN BLOQUEADA / CESADA O DESACTIVADA - EXCLUÍDO" THEN "Excluir"
WHEN "N1-CN FUERA DE SECTOR - EXCLUÍDO" THEN "Excluir"
WHEN "N1-CORRECCION DE REGISTRO - EXCLUÍDO" THEN "Excluir"
WHEN "N1-DIVERGENCIA DE INDICADORES - EXCLUÍDO" THEN "Excluir"
WHEN "N1-ESTOCK INSUFICIENTE - EXCLUÍDO" THEN "Excluir"
WHEN "N1-GESTION DE NIVEL - EXCLUÍDO" THEN "Excluir"
WHEN "N1-GSP ORIENTACION - EXCLUÍDO" THEN "Excluir"
WHEN "N1-INCONSISTENCIA EN SISTEMA - EXCLUÍDO" THEN "Excluir"
WHEN "N1-INGRESO DENEGADO - EXCLUÍDO" THEN "Excluir"
WHEN "N1-KIT DE INICIO NO CARGA - EXCLUÍDO" THEN "Excluir"
WHEN "N1-LINEA DE CREDITO INSUFICIENTE - EXCLUÍDO" THEN "Excluir"
WHEN "N1-PEDIDO NO APARECE EN GERA - EXCLUÍDO" THEN "Excluir"
WHEN "N1-PRODUCTO NO ENCONTRADO - EXCLUÍDO" THEN "Excluir"
WHEN "N1-PRODUCTO NO TOMA DESCUENTO - EXCLUÍDO" THEN "Excluir"
WHEN "N1-REGISTRO EN PROCESO EN GERA - EXCLUÍDO" THEN "Excluir"
WHEN "N1-REPORTE INDISPONIBLE - EXCLUÍDO" THEN "Excluir"
WHEN "NO LLEGA EL E-MAIL CON EL CODIGO - EXCLUÍDO" THEN "Excluir"
WHEN "NO LLEGA EL SMS CON EL CODIGO - EXCLUÍDO" THEN "Excluir"
WHEN "NO SE APLICA - EXCLUÍDO" THEN "Excluir"
WHEN "NOMBRE DE TIENDA MODIFICADO" THEN "Excluir"
WHEN "NOTEBOOK-HARDWARE" THEN "Excluir"
WHEN "NOTEBOOKS-FALLA APLICACIONES/S.O." THEN "Excluir"
WHEN "ORIENTADA A PAGAR MEDIANTE APP MI NEGOCIO - EXCLUÍDO" THEN "Excluir"
WHEN "ORIENTADA A REALIZAR LA CONSULTA-INFOCREDIT - EXCLUÍDO" THEN "Excluir"
WHEN "ORIENTADA A REALIZAR UN NUEVO REGISTRO DEL PROSPECTO - EXCLUÍDO" THEN "Excluir"
WHEN "ORIENTADA A VINCULAR SU CUENTA-MERCADO PAGO - EXCLUÍDO" THEN "Excluir"
WHEN "ORIENTADA CAPTACION APP MI NEGOCIO-ATENTO - EXCLUÍDO" THEN "Excluir"
WHEN "ORIENTADA EN COMO REALIZAR PEDIDO DE PREVENTA Y/O EVENTO ESPECIAL - EXCLUÍDO" THEN "Excluir"
WHEN "ORIENTADA EN DIVULGAR SU ESPACIO-CND - EXCLUÍDO" THEN "Excluir"
WHEN "ORIENTADA EN EL SITIO DE ENTRENAMIENTO NATURA - EXCLUÍDO" THEN "Excluir"
WHEN "ORIENTADA EN LA CAPTACION WEB MI NEGOCIO-ATENTO - EXCLUÍDO" THEN "Excluir"
WHEN "ORIENTADA EN LA CAPTACION-APP MI NEGOCIO - EXCLUÍDO" THEN "Excluir"
WHEN "ORIENTADA EN LA CAPTACION-CND - EXCLUÍDO" THEN "Excluir"
WHEN "ORIENTADA EN LA CAPTACION-LEGO - EXCLUÍDO" THEN "Excluir"
WHEN "ORIENTADA EN LA CAPTACION-SGI - EXCLUÍDO" THEN "Excluir"
WHEN "ORIENTADA EN LA CAPTACION-WEB MI NEGOCIO - EXCLUÍDO" THEN "Excluir"
WHEN "ORIENTADA EN SGI-FUNCIONES - EXCLUÍDO" THEN "Excluir"
WHEN "ORIENTADA EN SUS INDICADORES- WEB MI NEGOCIO - EXCLUÍDO" THEN "Excluir"
WHEN "ORIENTADA EN SUS INDICADORES-APP MI NEGOCIO - EXCLUÍDO" THEN "Excluir"
WHEN "ORIENTADA PARA CORRECCIÓN DE SU REGISTRO (TELEFONO-EMAIL-FECHA) - EXCLUÍDO" THEN "Excluir"
WHEN "ORIENTADA PARA DESCARGAR SU FACTURA-WEB MI NEGOCIO - EXCLUÍDO" THEN "Excluir"
WHEN "ORIENTADA PARA VERIFICAR SU PEDIDO-APP MI NEGOCIO - EXCLUÍDO" THEN "Excluir"
WHEN "ORIENTADA PARA VERIFICAR SU PEDIDO-WEB MI NEGOCIO - EXCLUÍDO" THEN "Excluir"
WHEN "ORIENTAMOS A REACTIVAR TIENDA DIGITAL - EXCLUÍDO" THEN "Excluir"
WHEN "PEDIDO NO APARECE EN GERA - EXCLUÍDO" THEN "Excluir"
WHEN "PERFIL MAL REGISTRADO - EXCLUÍDO" THEN "Excluir"
WHEN "PLCOM- PRODUCTO NO REGISTRADO - EXCLUÍDO" THEN "Excluir"
WHEN "PLCOM -SIN ALCANCE COMERCIAL - EXCLUÍDO" THEN "Excluir"
WHEN "PROSPECTO ENVIADO PARA APROBAR POR AREA DE ATENCION - EXCLUÍDO" THEN "Excluir"
WHEN "REINICIO DE PC/CELULAR - EXCLUÍDO" THEN "Excluir"
WHEN "REPORTE DIARIO EXP" THEN "Excluir"
WHEN "RESUELTO POR EXPCN N1 - EXCLUÍDO" THEN "Excluir"
WHEN "RETORNO - EXCLUÍDO" THEN "Excluir"
WHEN "SE CONSULTA UN PROSPECTO Y APARECE COMO CONSULTADO - EXCLUÍDO" THEN "Excluir"
WHEN "SMS -ACTUALIZACION DE BD CN'S" THEN "Excluir"
WHEN "SMS -MODIFICACION USUARIOS" THEN "Excluir"
WHEN "SMS-CUPO DE MENSAJES" THEN "Excluir"
WHEN "TEAMS - PROBLEMAS" THEN "Excluir"
WHEN "VALIDACION DE LLAMADO" THEN "Excluir"
WHEN "YA HABIA RESUELTO - EXCLUÍDO" THEN "Excluir"
WHEN "CADASTRO DUPLICADO" THEN "Excluir"
WHEN "CAMBIO DE EMAIL VOL" THEN "Excluir"
WHEN "CERRADO DESPUÃ‰S DE HORAS" THEN "Excluir"
WHEN "CERRADO DESPUÉS DE HORAS" THEN "Excluir"
WHEN "CONSULTA CON PLCOM" THEN "Excluir"
WHEN "VALIDACION PLCOM" THEN "Excluir"
WHEN "INCIDENTE RESUELTO" THEN "Excluir"
WHEN "PLCOM - CLASSIFICAÇÃO" THEN "Excluir"
WHEN "PLCOM-PENDIENTE DE RESPUESTA" THEN "Excluir"
WHEN "INCIDENTE EN ANDAMIENTO" THEN "Excluir"
WHEN "HEALTHCHECK" THEN "Excluir"
ELSE "Manter"
END
```
2. Excluir `Regra Status` em ['"Excluir"']

→ [56] Tipo, Pais, Segundos

## [51] Whats — Container

← [46] Limpar 18

1. Manter só `Tipo` em ['"WhatsApp"']

→ [75] União de linhas 15

## [52] Email — Container

← [46] Limpar 18

1. Manter só `Tipo` em ['"Email"']

→ [57] Limpar 19; [58] Limpar 20

## [53] Corrigir Colunas — Container

← [47] Corrigir Colunas

1. Renomear `Status de Classificação` → `Status de Classificação2`
2. Calcular `Status de Classificação`:

```
IF ISNULL([Status de Classificação 1]) THEN
	[Status de Classificação2]
ELSE
	[Status de Classificação 1]
END
```
3. Remover colunas: `Status de Classificação2`

→ [59] União de linhas 13

## [54] Resenhas Hispana — PublishExtract

← [48] Status Resposta

**Saída:** `4. DATASOURCES/Resenhas OIS`

## [55] Limpar 4 — Container

← [49] Resumen

1. Renomear `Número 1` → `Problema`
2. Renomear `Código de resolução` → `Código de resolución`
3. Renomear `Declaração do problema` → `Declaración del Problema`

→ [60] SN OIS

## [56] Tipo, Pais, Segundos — Container

← [50] Status Inelegíveis

1. Renomear `Setor` → `Setor Fim`
2. Calcular `Tipo`:

```
IF [Setor Fim] = "APP NATURA" THEN "Email"
ELSEIF [Setor Fim] = "APP Natura Latam" THEN "Email"
ELSEIF [Setor Fim] = "AR" THEN "WhatsApp"
ELSEIF [Setor Fim] = "AR- Email" THEN "Email"
ELSEIF [Setor Fim] = "AR GV" THEN "WhatsApp"
ELSEIF [Setor Fim] = "ATENCIÓN" THEN "WhatsApp"
ELSEIF [Setor Fim] = "ATENDIMIENTO" THEN "WhatsApp"
ELSEIF [Setor Fim] = "CL" THEN "WhatsApp"
ELSEIF [Setor Fim] = "CL GV" THEN "WhatsApp"
ELSEIF [Setor Fim] = "CL - Email" THEN "Email"
ELSEIF [Setor Fim] = "CO" THEN "WhatsApp"
ELSEIF [Setor Fim] = "CO GV" THEN "WhatsApp"
ELSEIF [Setor Fim] = "CO - Email" THEN "Email"
ELSEIF [Setor Fim] = "CO-CELULAR" THEN "Remover"
ELSEIF [Setor Fim] = "CO-SOPORTE" THEN "Remover"
ELSEIF [Setor Fim] = "EC" THEN "WhatsApp"
ELSEIF [Setor Fim] = "EC GV" THEN "WhatsApp"
ELSEIF [Setor Fim] = "EC - Email" THEN "Email"
ELSEIF [Setor Fim] = "LNN EC" THEN "WhatsApp"
ELSEIF [Setor Fim] = "LNN EC - Email" THEN "Email"
ELSEIF [Setor Fim] = "EX" THEN "WhatsApp"
ELSEIF [Setor Fim] = "FV-AYUDA" THEN "Remover"
ELSEIF [Setor Fim] = "GV CL" THEN "WhatsApp"
ELSEIF [Setor Fim] = "GVs CHILE" THEN "WhatsApp"
ELSEIF [Setor Fim] = "MI NEGOCIO" THEN "Email"
ELSEIF [Setor Fim] = "MX" THEN "WhatsApp"
ELSEIF [Setor Fim] = "MX - Email" THEN "Email"
ELSEIF [Setor Fim] = "MX GV" THEN "WhatsApp"
ELSEIF [Setor Fim] = "PE" THEN "WhatsApp"
ELSEIF [Setor Fim] = "PE- Email" THEN "Email"
ELSEIF [Setor Fim] = "PE GV" THEN "WhatsApp"
ELSEIF [Setor Fim] = "PE-CELULAR" THEN "Remover"
ELSEIF [Setor Fim] = "PE-LIDER" THEN "Remover"
ELSEIF [Setor Fim] = "APP AVON" THEN "Email"
ELSE NULL
END
```
3. Excluir `Setor Fim` em ['"CL-CELULAR"']
4. Excluir `Tipo` em ['"Remover"']
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
ELSEIF [Setor Fim] = "LNN EC" THEN "Ecuador"
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
ELSE NULL
END
```
6. Renomear `Setor Fim` → `Setor`
7. Calcular `Tempo Segundos`:

```
DATEDIFF('second', [Data criação], [Data conclusão])
```

→ [72] União de colunas 4

## [57] Limpar 19 — Container

← [52] Email

1. Renomear `Protocolo` → `Protocol`
2. Renomear `Setor Fim` → `Setor`
3. Remover colunas: `Data de Criação do Atendimento`
4. Renomear `Data de Criação do Ticket` → `Data criação`
5. Renomear `Data de Finalização` → `Data conclusão`
6. Remover colunas: `Função do Sistema`
7. Remover colunas: `Status de Classificação`
8. Renomear `Cant. de Atendimientos` → `Valor Atendimento`
9. Renomear `Estado` → `Status`
10. Remover colunas: `Data Contato Fuso`
11. Remover colunas: `Protocolo do Atendimento Convertido`
12. Remover colunas: `Data de Conversão do Atendimento`
13. Remover colunas: `Código CN`
14. Remover colunas: `Pedidos Finalizados`
15. Remover colunas: `Llamado`
16. Remover colunas: `Observações`
17. Renomear `Status` → `Situação`

→ [78] União de linhas 21

## [58] Limpar 20 — Container

← [52] Email

1. Renomear `Protocolo` → `Protocolo analitico`
2. Manter só: `Função do Sistema`, `Protocolo analitico`, `Status de Classificação`

→ [61] União de linhas 17

## [59] União de linhas 13 — SuperUnion

← [53] Corrigir Colunas; [28] Substitui por 1

**Union** das entradas acima (colunas com o mesmo nome se juntam; cria `Table Names`).

1. Remover colunas: `Table Names`
2. Remapear `Cant. de Atendimientos`: "1" ← null

→ [62] Remove Status de Classificação

## [60] SN OIS — PublishExtract

← [55] Limpar 4

**Saída:** `4. DATASOURCES/Experiencia Hispana - Chamados Servicenow`

## [61] União de linhas 17 — SuperUnion

← [40] Limpar 13; [58] Limpar 20

**Union** das entradas acima (colunas com o mesmo nome se juntam; cria `Table Names`).

1. Remover colunas: `Table Names`

→ [63] Limpar 14

## [62] Remove Status de Classificação — Container

_Descrição:_ Remove os N2 e N3 do Status de Classificacao

← [59] União de linhas 13

1. Excluir `Status de Classificação 1` em ['"N2 - E-mail - En acompañamiento TD - CLASSIFICAÇÃO"', '"N2 - WhatsApp - EN ACOMPAÑAMIENTO TD - CLASSIFICAÇÃO"', '"N3 – E-mail – Pendientes – JIRA - CLASSIFICAÇÃO"', '"N3 – WhatsApp – Pendientes – JIRA - CLASSIFICAÇÃO"']

→ [64] Registro de Grupos

## [63] Limpar 14 — Container

← [61] União de linhas 17

→ [89] União de colunas 6

## [64] Registro de Grupos — Container

← [62] Remove Status de Classificação

1. Renomear `AlineWEL` → `Origem`
2. Remapear `Origem`: "MKT zAP" ← null

→ [65] Status de Classificação; [66] Limpar 11

## [65] Status de Classificação — Container

← [64] Registro de Grupos

1. RichDiscreteValueFilter: `{"exclude": true, "values": {"Status de Classificação 1": ["\"BUEN DIA/AGRADECIMIENTOS - CLASSIFICAÃ‡ÃƒO\"", "\"BUEN DIA/AGRADECIMIENTOS - CLASSIFICAÇÃO\"", "\"BUEN DIA/AGRADECIMIENTOS - EXCLUÍDO\"", "\"EXPCN - CLASSIFICAÇÃO\"", "\"EXPCN - CLASSIFICAÃ‡ÃƒO\"", "\"MFA - EXCLUÍDO\""]}, "datatype": "string", "fieldId": "70a98400-f261-47ff-9636-21018b31a2c0-Status de Classificação 1", "outOfSampleValues": null}`

→ [67] Status de Finalização

## [66] Limpar 11 — Container

← [64] Registro de Grupos

→ [68] A partir Mar/26

## [67] Status de Finalização — Container

← [65] Status de Classificação

1. RichDiscreteValueFilter: `{"exclude": true, "values": {"Status de finalização": ["\"test - EXCLUÍDO\"", "\"EXPCN\"", "\"BUEN DIA/AGRADECIMIENTOS\""]}, "datatype": "string", "fieldId": "70a98400-f261-47ff-9636-21018b31a2c0-Status de finalização", "outOfSampleValues": null}`

→ [69] Status Finalizacao removidos

## [68] A partir Mar/26 — Container

← [66] Limpar 11

1. Manter só: `Protocolo`, `Cant. de Atendimientos`, `Responsável`, `Status de finalização`

→ [70] Manter Protocolo, SF e Qtd Atendimento

## [69] Status Finalizacao removidos — Container

← [67] Status de Finalização

1. RichDiscreteValueFilter: `{"exclude": true, "values": {"Status de finalização": ["\"APERTURA DE LLAMADO-N2 - EXCLUÍDO\"", "\"CAMBIO DE PC/CELULAR/NAVEGADOR - EXCLUÍDO\"", "\"CELULAR- RED\"", "\"CELULAR-HARDWARE\"", "\"CELULAR-REASIGNACION\"", "\"CENTRAL DE COMANDO - EXCLUÍDO\"", "\"CIERRE DE PLANTON - EXCLUÍDO\"", "\"CODIGO RECIBIDO NO FUNCIONA/ EXPIRO - EXCLUÍDO\"", "\"CONFIGURACION DE CONTACTOS\"", "\"CONFIGURACIÓN DE E-MAIL\"", "\"CONFIGURACIÓN DE EQUIPO CELULAR\"", "\"CONFIGURACION DE MICROSOFT AUTENTICADOR MFA\"", "\"Contato sin exito - EXCLUÍDO\"", "\"CORREO-CELULAR\"", "\"DIRECCIONADO CON EL CAN/SV/GN/GDN/LN - EXCLUÍDO\"", "\"ENVIO DE BOLETO PARA PAGO - EXCLUÍDO\"", "\"EQUIPO AVERIADO\"", "\"FALLA APLICACIONES/S.O\"", "\"FALTA DE  INFORMACIÓN - EXCLUÍDO\"", "\"Finaliza - Respuesta Negativa Pro Ativo - EXCLUÍDO\"", "\"FINALIZA NW\"", "\"Finalizado New Way\"", "\"Imagen error - EXCLUÍDO\"", "\"INCIDENTE CRÃTICO\"", "\"INCONVENIENTES CON  CORREO OUTLOOK NATURA\"", "\"INCONVENIENTES CON EQUIPO CELULAR\"", "\"INCONVENIENTES CON LA OPERADORA TELEFONICA - EXCLUÍDO\"", "\"INCONVENIENTES CON MICROSOFT TEAMS\"", "\"LA PLATAFORMA NO RECONOCE EL DOCUMENTO QUE SE INTENTA SUBIR - EXCLUÍDO\"", "\"MFA CAMPAÑA - EXCLUÍDO\"", "\"N1-ACCESO A PERSONA NO PERMITIDO - EXCLUÍDO\"", "\"N1-CADUNI ORIENTACION - EXCLUÍDO\"", "\"N1-CANTIDAD MAXIMA DE TITULOS PENDIENTES EXCEDIDOS - EXCLUÍDO\"", "\"N1-CARRITO EN CONVERSION - EXCLUÍDO\"", "\"N1-CN BLOQUEADA / CESADA O DESACTIVADA - EXCLUÍDO\"", "\"N1-CN FUERA DE SECTOR - EXCLUÍDO\"", "\"N1-CORRECCION DE REGISTRO - EXCLUÍDO\"", "\"N1-DIVERGENCIA DE INDICADORES - EXCLUÍDO\"", "\"N1-ESTOCK INSUFICIENTE - EXCLUÍDO\"", "\"N1-GESTION DE NIVEL - EXCLUÍDO\"", "\"N1-GSP ORIENTACION - EXCLUÍDO\"", "\"N1-INCONSISTENCIA EN SISTEMA - EXCLUÍDO\"", "\"N1-INGRESO DENEGADO - EXCLUÍDO\"", "\"N1-KIT DE INICIO NO CARGA - EXCLUÍDO\"", "\"N1-LINEA DE CREDITO INSUFICIENTE - EXCLUÍDO\"", "\"N1-PEDIDO NO APARECE EN GERA - EXCLUÍDO\"", "\"N1-PRODUCTO NO ENCONTRADO - EXCLUÍDO\"", "\"N1-PRODUCTO NO TOMA DESCUENTO - EXCLUÍDO\"", "\"N1-REGISTRO EN PROCESO EN GERA - EXCLUÍDO\"", "\"N1-REPORTE INDISPONIBLE - EXCLUÍDO\"", "\"NO LLEGA EL E-MAIL CON EL CODIGO - EXCLUÍDO\"", "\"NO LLEGA EL SMS CON EL CODIGO - EXCLUÍDO\"", "\"NO SE APLICA - EXCLUÍDO\"", "\"NOMBRE DE TIENDA MODIFICADO\"", "\"NOTEBOOK-HARDWARE\"", "\"NOTEBOOKS-FALLA APLICACIONES/S.O.\"", "\"ORIENTADA A PAGAR MEDIANTE APP MI NEGOCIO - EXCLUÍDO\"", "\"ORIENTADA A REALIZAR LA CONSULTA-INFOCREDIT - EXCLUÍDO\"", "\"ORIENTADA A REALIZAR UN NUEVO REGISTRO DEL PROSPECTO - EXCLUÍDO\"", "\"ORIENTADA A VINCULAR SU CUENTA-MERCADO PAGO - EXCLUÍDO\"", "\"ORIENTADA CAPTACION APP MI NEGOCIO-ATENTO - EXCLUÍDO\"", "\"ORIENTADA EN COMO REALIZAR PEDIDO DE PREVENTA Y/O EVENTO ESPECIAL - EXCLUÍDO\"", "\"ORIENTADA EN DIVULGAR SU ESPACIO-CND - EXCLUÍDO\"", "\"ORIENTADA EN EL SITIO DE ENTRENAMIENTO NATURA - EXCLUÍDO\"", "\"ORIENTADA EN LA CAPTACION WEB MI NEGOCIO-ATENTO - EXCLUÍDO\"", "\"ORIENTADA EN LA CAPTACION-APP MI NEGOCIO - EXCLUÍDO\"", "\"ORIENTADA EN LA CAPTACION-CND - EXCLUÍDO\"", "\"ORIENTADA EN LA CAPTACION-LEGO - EXCLUÍDO\"", "\"ORIENTADA EN LA CAPTACION-SGI - EXCLUÍDO\"", "\"ORIENTADA EN LA CAPTACION-WEB MI NEGOCIO - EXCLUÍDO\"", "\"ORIENTADA EN SGI-FUNCIONES - EXCLUÍDO\"", "\"ORIENTADA EN SUS INDICADORES- WEB MI NEGOCIO - EXCLUÍDO\"", "\"ORIENTADA EN SUS INDICADORES-APP MI NEGOCIO - EXCLUÍDO\"", "\"ORIENTADA PARA CORRECCIÓN DE SU REGISTRO (TELEFONO-EMAIL-FECHA) - EXCLUÍDO\"", "\"ORIENTADA PARA DESCARGAR SU FACTURA-WEB MI NEGOCIO - EXCLUÍDO\"", "\"ORIENTADA PARA VERIFICAR SU PEDIDO-APP MI NEGOCIO - EXCLUÍDO\"", "\"ORIENTADA PARA VERIFICAR SU PEDIDO-WEB MI NEGOCIO - EXCLUÍDO\"", "\"ORIENTAMOS A REACTIVAR TIENDA DIGITAL - EXCLUÍDO\"", "\"PEDIDO NO APARECE EN GERA - EXCLUÍDO\"", "\"PERFIL MAL REGISTRADO - EXCLUÍDO\"", "\"PLCOM- PRODUCTO NO REGISTRADO - EXCLUÍDO\"", "\"PLCOM -SIN ALCANCE COMERCIAL - EXCLUÍDO\"", "\"PROSPECTO ENVIADO PARA APROBAR POR AREA DE ATENCION - EXCLUÍDO\"", "\"REINICIO DE PC/CELULAR - EXCLUÍDO\"", "\"REPORTE DIARIO EXP\"", "\"RESUELTO POR EXPCN N1 - EXCLUÍDO\"", "\"RETORNO - EXCLUÍDO\"", "\"SE CONSULTA UN PROSPECTO Y APARECE COMO CONSULTADO - EXCLUÍDO\"", "\"SMS -ACTUALIZACION DE BD CN'S\"", "\"SMS -MODIFICACION USUARIOS\"", "\"SMS-CUPO DE MENSAJES\"", "\"TEAMS - PROBLEMAS\"", "\"YA HABIA RESUELTO - EXCLUÍDO\"", "\"VALIDACION DE LLAMADO\"", "\"AJUSTE/ CORRECCION REALIZADO POR PLCOM\""]}, "datatype": "string", "fieldId": "70a98400-f261-47ff-9636-21018b31a2c0-Status de finalização-c3ab309e-0fb7-4436-a9ee-946e754786a9-Status de finalização", "outOfSampleValues": null}`

→ [71] Segundos, Tipo, SLA e Pais

## [70] Manter Protocolo, SF e Qtd Atendimento — Container

← [68] A partir Mar/26

→ [72] União de colunas 4

## [71] Segundos, Tipo, SLA e Pais — Container

← [69] Status Finalizacao removidos

1. Calcular `Primeiro Tempo de Espera - Segundos`:

```
(INT(SPLIT([Primeiro Tempo de Espera], ":", 1)) * 3600) +
(INT(SPLIT([Primeiro Tempo de Espera], ":", 2)) * 60) +
INT(SPLIT([Primeiro Tempo de Espera], ":", 3))
```
2. Calcular `Tipo`:

```
IF [Setor Fim] = "APP NATURA" THEN "Email"
ELSEIF [Setor Fim] = "APP Natura Latam" THEN "Email"
ELSEIF [Setor Fim] = "AR" THEN "WhatsApp"
ELSEIF [Setor Fim] = "AR- Email" THEN "Email"
ELSEIF [Setor Fim] = "AR GV" THEN "WhatsApp"
ELSEIF [Setor Fim] = "ATENCIÓN" THEN "WhatsApp"
ELSEIF [Setor Fim] = "ATENDIMIENTO" THEN "WhatsApp"
ELSEIF [Setor Fim] = "CL" THEN "WhatsApp"
ELSEIF [Setor Fim] = "CL GV" THEN "WhatsApp"
ELSEIF [Setor Fim] = "CL - Email" THEN "Email"
ELSEIF [Setor Fim] = "LNN EC" THEN "WhatsApp"
ELSEIF [Setor Fim] = "LNN EC - Email" THEN "Email"
ELSEIF [Setor Fim] = "CO" THEN "WhatsApp"
ELSEIF [Setor Fim] = "CO GV" THEN "WhatsApp"
ELSEIF [Setor Fim] = "CO - Email" THEN "Email"
ELSEIF [Setor Fim] = "CO-CELULAR" THEN "Remover"
ELSEIF [Setor Fim] = "CO-SOPORTE" THEN "Remover"
ELSEIF [Setor Fim] = "EC" THEN "WhatsApp"
ELSEIF [Setor Fim] = "EC GV" THEN "WhatsApp"
ELSEIF [Setor Fim] = "EC - Email" THEN "Email"
ELSEIF [Setor Fim] = "EX" THEN "WhatsApp"
ELSEIF [Setor Fim] = "FV-AYUDA" THEN "Remover"
ELSEIF [Setor Fim] = "GV CL" THEN "WhatsApp"
ELSEIF [Setor Fim] = "GVs CHILE" THEN "WhatsApp"
ELSEIF [Setor Fim] = "MI NEGOCIO" THEN "Email"
ELSEIF [Setor Fim] = "MX" THEN "WhatsApp"
ELSEIF [Setor Fim] = "MX - Email" THEN "Email"
ELSEIF [Setor Fim] = "MX GV" THEN "WhatsApp"
ELSEIF [Setor Fim] = "PE" THEN "WhatsApp"
ELSEIF [Setor Fim] = "PE- Email" THEN "Email"
ELSEIF [Setor Fim] = "PE GV" THEN "WhatsApp"
ELSEIF [Setor Fim] = "PE-CELULAR" THEN "Remover"
ELSEIF [Setor Fim] = "PE-LIDER" THEN "Remover"
ELSEIF [Setor Fim] = "APP AVON" THEN "Email"
ELSE NULL
END

```
3. Calcular `SLA`:

```
IF [Tipo] = "Email" AND [Primeiro Tempo de Espera - Segundos] >= 0 AND [Primeiro Tempo de Espera - Segundos] < 3600 THEN
    "Dentro do SLA"
ELSEIF [Tipo] = "Email" AND [Primeiro Tempo de Espera - Segundos] >= 3600 THEN
    "Fora do SLA"
ELSEIF [Tipo] = "WhatsApp" AND [Primeiro Tempo de Espera - Segundos] >= 0 AND [Primeiro Tempo de Espera - Segundos] <= 600 THEN
    "Dentro do SLA"
ELSEIF [Tipo] = "WhatsApp" AND [Primeiro Tempo de Espera - Segundos] > 600 THEN
    "Fora do SLA"
ELSE
    "Dentro do SLA"
END

```
4. Calcular `Tempo de Operação - Segundos`:

```
(INT(SPLIT([Tempo de Operação], ":", 1)) * 3600) +
(INT(SPLIT([Tempo de Operação], ":", 2)) * 60) +
INT(SPLIT([Tempo de Operação], ":", 3))
```
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
ELSEIF [Setor Fim] = "LNN EC" THEN "Ecuador"
ELSEIF [Setor Fim] = "LNN EC - Email" THEN "Ecuador"
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
ELSE NULL
END
```
6. Calcular `Data Contato Fuso`:

```
IF [Pais] = "Chile" THEN DATEADD('hour', -1, [Data Contato])
ELSEIF [Pais] = "Colombia" OR [Pais] = "Peru" OR [Pais] = "Ecuador" THEN DATEADD('hour', -2, [Data Contato])
ELSEIF [Pais] = "Mexico" THEN DATEADD('hour', -3, [Data Contato])
ELSE [Data Contato]
END

```
7. Calcular `Nivel`:

```
IF [Data Contato] < #2026-03-01# THEN
    // --- REGRA PARA DATAS ANTERIORES A MARÇO 2026 (Base: Nivel) ---
    CASE [Status de finalização]
        // CATEGORIA N2
        WHEN "DIRECCIONADO - PLCOM" THEN "N2"
        WHEN "DIRECCIONADO - TD LOCAL" THEN "N2"
        WHEN "INCIDENTE CRITICO" THEN "N2"
        WHEN "INCIDENTE CRÍTICO" THEN "N2"
        WHEN "INCIDENTE CRÃTICO" THEN "N2"
        WHEN "LLAMADO ABIERTO PARA N2" THEN "N2"
        WHEN "REAPERTURA DE LLAMADO" THEN "N2"

        // CATEGORIA NEUTRO
        WHEN "AJUSTE/ CORRECCION REALIZADO POR PLCOM" THEN "Neutro"
        WHEN "BUEN DIA/AGRADECIMIENTOS" THEN "Neutro"
        WHEN "CERRADO DESPUÉS DE HORAS" THEN "Neutro"
        WHEN "CONSULTA - TD LOCAL" THEN "Neutro"
        WHEN "CONSULTA CON PLCOM" THEN "Neutro"
        WHEN "CONTACTO SIN EXITO" THEN "Neutro"
        WHEN "DIRECCIONADO - ATENCION" THEN "Neutro"
        WHEN "DIRECCIONADO - CRÉDITO" THEN "Neutro"
        WHEN "EXPCN" THEN "Neutro"
        WHEN "FINALIZADO FUERA DE HORÁRIO" THEN "Neutro"
        WHEN "FINALIZADO SIN INTERACCION" THEN "Neutro"
        WHEN "INCIDENTE EN ANDAMIENTO" THEN "Neutro"
        WHEN "INCIDENTE RESUELTO" THEN "Neutro"
        WHEN "REPORTE DIARIO EXP" THEN "Neutro"
        WHEN "Resuelto MKT N3" THEN "Neutro"
        WHEN "Resuelto N2 E-mail" THEN "Neutro"
        WHEN "Resuelto N2 MKT" THEN "Neutro"
        WHEN "Resuelto N3 E-mail" THEN "Neutro"
        WHEN "VALIDACION - TD LOCAL" THEN "Neutro"
        WHEN "VALIDACION DE LLAMADO" THEN "Neutro"
        WHEN "VALIDACION PLCOM" THEN "Neutro"

        ELSE "N1"
    END

ELSEIF [Data Contato] < #2026-10-01# THEN
    // --- REGRA DE MARÇO DE 2026 ATÉ SETEMBRO DE 2026 (Base: Nivel) ---
    CASE [Status de finalização]
        // CATEGORIA N2
        WHEN "DIRECCIONADO - PLCOM" THEN "N2"
        WHEN "DIRECCIONADO - TD LOCAL" THEN "N2"
        WHEN "INCIDENTE CRITICO" THEN "N2"
        WHEN "INCIDENTE CRÍTICO" THEN "N2"
        WHEN "INCIDENTE CRÃTICO" THEN "N2"
        WHEN "LLAMADO ABIERTO PARA N2" THEN "N2"
        WHEN "REAPERTURA DE LLAMADO" THEN "N2"

        // CATEGORIA NEUTRO
        WHEN "AJUSTE/ CORRECCION REALIZADO POR PLCOM" THEN "Neutro"
        WHEN "BUEN DIA/AGRADECIMIENTOS" THEN "Neutro"
        WHEN "CERRADO DESPUÉS DE HORAS" THEN "Neutro"
        WHEN "CONSULTA - TD LOCAL" THEN "Neutro"
        WHEN "CONSULTA CON PLCOM" THEN "Neutro"
        WHEN "CONTACTO SIN EXITO" THEN "Neutro"
        WHEN "DIRECCIONADO - ATENCION" THEN "Neutro"
        WHEN "DIRECCIONADO - CRÉDITO" THEN "Neutro"
        WHEN "EXPCN" THEN "Neutro"
        WHEN "FINALIZADO FUERA DE HORÁRIO" THEN "Neutro"
        WHEN "FINALIZADO SIN INTERACCION" THEN "Neutro"
        WHEN "INCIDENTE EN ANDAMIENTO" THEN "Neutro"
        WHEN "INCIDENTE RESUELTO" THEN "Neutro"
        WHEN "REPORTE DIARIO EXP" THEN "Neutro"
        WHEN "Resuelto MKT N3" THEN "Neutro"
        WHEN "Resuelto N2 E-mail" THEN "Neutro"
        WHEN "Resuelto N2 MKT" THEN "Neutro"
        WHEN "Resuelto N3 E-mail" THEN "Neutro"
        WHEN "VALIDACION - TD LOCAL" THEN "Neutro"
        WHEN "VALIDACION DE LLAMADO" THEN "Neutro"
        WHEN "VALIDACION PLCOM" THEN "Neutro"

        // CATEGORIA N1 (Específica da nova planilha)
        WHEN "ACTUALIZACION DE LA APP" THEN "N1"
        WHEN "ACTUALIZACIÓN DEL CARRITO" THEN "N1"
        WHEN "ACTUALIZACION DEL NAVEGADOR" THEN "N1"
        WHEN "BIOMETRIA V2 AUTOREGISTRO" THEN "N1"
        WHEN "CADASTRO DUPLICADO" THEN "N1"
        WHEN "CAMBIO DE EMAIL VOL" THEN "N1"
        WHEN "CAMBIO O REINICIO DE CELULAR/PC/NAVEGADOR" THEN "N1"
        WHEN "CREACION DE SU ESPACIO-CND" THEN "N1"
        WHEN "LIMPIEZA DE CACHE/HISTORIAL" THEN "N1"
        WHEN "LINK ENVIADO" THEN "N1"
        WHEN "REGISTRO CESADO/BLOQUEADO O DESACTIVADO" THEN "N1"
        WHEN "REGISTRO RECHAZADO" THEN "N1"
        WHEN "REHABILITAR TIENDA DIGITAL" THEN "N1"
        WHEN "REPORTE DE MOROSIDAD" THEN "N1"
        WHEN "RESET DE CONTRASENA" THEN "N1"
        WHEN "RESILIÊNCIA EN GSP" THEN "N1"
        WHEN "VALIDACION DE DATOS - REGISTRO" THEN "N1"
        WHEN "VALIDACIÓN DE DATOS- INDICADORES" THEN "N1"
        WHEN "VALIDACIÓN DE DATOS-BRM" THEN "N1"
        WHEN "VALIDACIÓN DE DATOS-CND" THEN "N1"
        WHEN "VALIDACION-CAMINO DE CRECIMIENTO" THEN "N1"
        WHEN "VALIDADO SIN INCONVENIENTES" THEN "N1"

        ELSE "Não considerar"
    END

ELSE
    // --- REGRA PARA OUTUBRO DE 2026 EM DIANTE (Base: Nivel Validar) ---
    CASE [Status de finalização]
        // CATEGORIA N2
        WHEN "DIRECCIONADO - PLCOM" THEN "N2"
        WHEN "DIRECCIONADO - TD LOCAL" THEN "N2"
        WHEN "INCIDENTE CRITICO" THEN "N2"
        WHEN "INCIDENTE CRÍTICO" THEN "N2"
        WHEN "INCIDENTE CRÃTICO" THEN "N2"
        WHEN "LLAMADO ABIERTO PARA N2" THEN "N2"
        WHEN "REAPERTURA DE LLAMADO" THEN "N2"

        // CATEGORIA NEUTRO
        WHEN "AJUSTE/ CORRECCION REALIZADO POR PLCOM" THEN "Neutro"
        WHEN "CONSULTA - TD LOCAL" THEN "Neutro"
        WHEN "CONSULTA CON PLCOM" THEN "Neutro"
        WHEN "DIRECCIONADO - ATENCION" THEN "Neutro"
        WHEN "DIRECCIONADO - CRÉDITO" THEN "Neutro"
        WHEN "FINALIZADO SIN INTERACCION" THEN "Neutro"
        WHEN "INCIDENTE EN ANDAMIENTO" THEN "Neutro"
        
        WHEN "Resuelto E-mail N3" THEN "Neutro"
        WHEN "Resuelto MKT N3" THEN "Neutro"
        WHEN "Resuelto N2 E-mail" THEN "Neutro"
        WHEN "Resuelto N2 MKT" THEN "Neutro"
        WHEN "Resuelto MKT N3" THEN "Neutro"
        WHEN "Resuelto N2 E-mail" THEN "Neutro"
        WHEN "Resuelto N2 MKT" THEN "Neutro"
        WHEN "Resuelto N3 E-mail" THEN "Neutro"
        
        WHEN "VALIDACION - TD LOCAL" THEN "Neutro"
        WHEN "VALIDACION DE LLAMADO" THEN "Neutro"
        WHEN "VALIDACION PLCOM" THEN "Neutro"
        WHEN "VALIDACION  PLCOM" THEN "Neutro"

        // CATEGORIA N1
        WHEN "ACTUALIZACION DE LA APP" THEN "N1"
        WHEN "ACTUALIZACIÓN DEL CARRITO" THEN "N1"
        WHEN "ACTUALIZACION DEL NAVEGADOR" THEN "N1"
        WHEN "BIOMETRIA V2 AUTOREGISTRO" THEN "N1"
        WHEN "BLANQUEO DEL REGISTRO" THEN "N1"
        WHEN "CADASTRO DUPLICADO" THEN "N1"
        WHEN "CAMBIO DE EMAIL VOL" THEN "N1"
        WHEN "CAMBIO O REINICIO DE CELULAR/PC/NAVEGADOR" THEN "N1"
        WHEN "CREACION DE SU ESPACIO-CND" THEN "N1"
        WHEN "LIMPIEZA DE CACHE/HISTORIAL" THEN "N1"
        WHEN "LINK ENVIADO" THEN "N1"
        WHEN "REGISTRO CESADO/BLOQUEADO O DESACTIVADO" THEN "N1"
        WHEN "REGISTRO RECHAZADO" THEN "N1"
        WHEN "REHABILITAR TIENDA DIGITAL" THEN "N1"
        WHEN "REPORTE DE MOROSIDAD" THEN "N1"
        WHEN "RESET DE CONTRASENA" THEN "N1"
        WHEN "RESILIÊNCIA EN GSP" THEN "N1"
        WHEN "SOLICITUD DE DATOS - APPS" THEN "N1"
        WHEN "VALIDACION DE DATOS - REGISTRO" THEN "N1"
        WHEN "VALIDACIÓN DE DATOS- INDICADORES" THEN "N1"
        WHEN "VALIDACIÓN DE DATOS-BRM" THEN "N1"
        WHEN "VALIDACIÓN DE DATOS-CND" THEN "N1"
        WHEN "VALIDACION-CAMINO DE CRECIMIENTO" THEN "N1"
        WHEN "VALIDADO SIN INCONVENIENTES" THEN "N1"

        // CATEGORIA NÃO CONSIDERAR
        WHEN "BUEN DIA/AGRADECIMIENTOS" THEN "Não considerar"
        WHEN "CERRADO DESPUÉS DE HORAS" THEN "Não considerar"
        WHEN "CONTACTO SIN EXITO" THEN "Não considerar"
        WHEN "EXPCN" THEN "Não considerar"
        WHEN "FINALIZADO FUERA DE HORÁRIO" THEN "Não considerar"
        WHEN "HEALTHCHECK" THEN "Não considerar"
        WHEN "INCIDENTE RESUELTO" THEN "Não considerar"
        WHEN "REPORTE DIARIO EXP" THEN "Não considerar"

        ELSE "Não mapeado"
    END
END
```
8. Calcular `Primeiro Contato`:

```
IF [Status de finalização] = "AJUSTE/ CORRECCION REALIZADO POR PLCOM"
    OR [Status de finalização] = "DIRECCIONADO - PLCOM"
    OR [Status de finalização] = "DIRECCIONADO - TD LOCAL"
    OR [Status de finalização] = "INCIDENTE CRÍTICO"
    OR [Status de finalização] = "INCIDENTE CRITICO"
    OR [Status de finalização] = "INCIDENTE CRÃTICO"
    OR [Status de finalização] = "LLAMADO ABIERTO PARA N2"
    OR [Status de finalização] = "PLCOM-PENDIENTE DE RESPUESTA"
    OR [Status de finalização] = "REAPERTURA DE LLAMADO"
THEN "Não Resolvido no 1° Contato"
ELSE "Resolvido no 1° Contato"
END

```
9. Remover colunas: `Data Contato`

→ [73] União de linhas 2

## [72] União de colunas 4 — SuperJoin

← [70] Manter Protocolo, SF e Qtd Atendimento (Left); [56] Tipo, Pais, Segundos (Right)

**Join right**: esquerda = [70] Manter Protocolo, SF e Qtd Atendimento, direita = [56] Tipo, Pais, Segundos

Condição: `esq.[Protocolo] == dir.[Protocol]`

1. Remover colunas: `Protocolo`

→ [74] Nivel

## [73] União de linhas 2 — SuperUnion

← [71] Segundos, Tipo, SLA e Pais; [34] Limpar 8

**Union** das entradas acima (colunas com o mesmo nome se juntam; cria `Table Names`).

1. Remapear `Table Names`: "MKT Zap" ← "Base"

→ [75] União de linhas 15

## [74] Nivel — Container

← [72] União de colunas 4

1. Calcular `Nivel`:

```
IF [Data conclusão] < #2026-10-01# THEN
    // --- LÓGICA ATÉ SETEMBRO DE 2026 (Base: Nivel) ---
    CASE IFNULL([Status], [Status de finalização])
        // --- CATEGORIA N2 ---
        WHEN "DIRECCIONADO - PLCOM" THEN "N2"
        WHEN "DIRECCIONADO - TD LOCAL" THEN "N2"
        WHEN "INCIDENTE CRITICO" THEN "N2"
        WHEN "INCIDENTE CRÍTICO" THEN "N2"
        WHEN "INCIDENTE CRÃTICO" THEN "N2"
        WHEN "LLAMADO ABIERTO PARA N2" THEN "N2"
        WHEN "REAPERTURA DE LLAMADO" THEN "N2"

        // --- CATEGORIA NEUTRO (Desconsiderados / Não considerados) ---
        WHEN "AJUSTE/ CORRECCION REALIZADO POR PLCOM" THEN "Neutro"
        WHEN "BUEN DIA/AGRADECIMIENTOS" THEN "Neutro"
        WHEN "CERRADO DESPUÉS DE HORAS" THEN "Neutro"
        WHEN "CONSULTA - TD LOCAL" THEN "Neutro"
        WHEN "CONSULTA CON PLCOM" THEN "Neutro"
        WHEN "CONTACTO SIN EXITO" THEN "Neutro"
        WHEN "DIRECCIONADO - ATENCION" THEN "Neutro"
        WHEN "DIRECCIONADO - CRÉDITO" THEN "Neutro"
        WHEN "EXPCN" THEN "Neutro"
        WHEN "FINALIZADO FUERA DE HORÁRIO" THEN "Neutro"
        WHEN "FINALIZADO SIN INTERACCION" THEN "Neutro"
        WHEN "HEALTHCHECK" THEN "Neutro"
        WHEN "INCIDENTE EN ANDAMIENTO" THEN "Neutro"
        WHEN "INCIDENTE RESUELTO" THEN "Neutro"
        WHEN "REPORTE DIARIO EXP" THEN "Neutro"
        
        // Status de "Resuelto" mantidos exatamente como chegam na sua base real
        WHEN "Resuelto MKT N3" THEN "Neutro"
        WHEN "Resuelto N2 E-mail" THEN "Neutro"
        WHEN "Resuelto N2 MKT" THEN "Neutro"
        WHEN "Resuelto N3 E-mail" THEN "Neutro"
        
        WHEN "VALIDACION - TD LOCAL" THEN "Neutro"
        WHEN "VALIDACION DE LLAMADO" THEN "Neutro"
        WHEN "VALIDACION PLCOM" THEN "Neutro"

        // --- CATEGORIA N1 ---
        WHEN "ACTUALIZACION DE LA APP" THEN "N1"
        WHEN "ACTUALIZACION DEL NAVEGADOR" THEN "N1"
        WHEN "ACTUALIZACIÓN DEL CARRITO" THEN "N1"
        WHEN "BIOMETRIA V2 AUTOREGISTRO" THEN "N1"
        WHEN "BLANQUEO DEL REGISTRO" THEN "N1"
        WHEN "CADASTRO DUPLICADO" THEN "N1"
        WHEN "CAMBIO DE EMAIL VOL" THEN "N1"
        WHEN "CAMBIO O REINICIO DE CELULAR/PC/NAVEGADOR" THEN "N1"
        WHEN "CREACION DE SU ESPACIO-CND" THEN "N1"
        WHEN "LIMPIEZA DE CACHE/HISTORIAL" THEN "N1"
        WHEN "LINK ENVIADO" THEN "N1"
        WHEN "REGISTRO CESADO/BLOQUEADO O DESACTIVADO" THEN "N1"
        WHEN "REGISTRO RECHAZADO" THEN "N1"
        WHEN "REHABILITAR TIENDA DIGITAL" THEN "N1"
        WHEN "REPORTE DE MOROSIDAD" THEN "N1"
        WHEN "RESET DE CONTRASENA" THEN "N1"
        WHEN "RESILIÊNCIA EN GSP" THEN "N1"
        WHEN "SOLICITUD DE DATOS - APPS" THEN "N1"
        WHEN "VALIDACION DE DATOS - REGISTRO" THEN "N1"
        WHEN "VALIDACION-CAMINO DE CRECIMIENTO" THEN "N1"
        WHEN "VALIDACIÓN DE DATOS- INDICADORES" THEN "N1"
        WHEN "VALIDACIÓN DE DATOS-BRM" THEN "N1"
        WHEN "VALIDACIÓN DE DATOS-CND" THEN "N1"
        WHEN "VALIDADO SIN INCONVENIENTES" THEN "N1"

        // --- EXCLUSÃO / NÃO CONSIDERAR ---
        // Tudo o que estiver na base e não estiver listado acima, será descartado
        ELSE "Não considerar"
    END

ELSE
    // --- LÓGICA A PARTIR DE OUTUBRO DE 2026 (Base: Nivel Validar) ---
    CASE IFNULL([Status], [Status de finalização])
        // --- CATEGORIA N2 ---
        WHEN "DIRECCIONADO - PLCOM" THEN "N2"
        WHEN "DIRECCIONADO - TD LOCAL" THEN "N2"
        WHEN "INCIDENTE CRITICO" THEN "N2"
        WHEN "INCIDENTE CRÍTICO" THEN "N2"
        WHEN "INCIDENTE CRÃTICO" THEN "N2"
        WHEN "LLAMADO ABIERTO PARA N2" THEN "N2"
        WHEN "REAPERTURA DE LLAMADO" THEN "N2"

        // --- CATEGORIA NEUTRO ---
        WHEN "AJUSTE/ CORRECCION REALIZADO POR PLCOM" THEN "Neutro"
        WHEN "CONSULTA - TD LOCAL" THEN "Neutro"
        WHEN "CONSULTA CON PLCOM" THEN "Neutro"
        WHEN "DIRECCIONADO - ATENCION" THEN "Neutro"
        WHEN "DIRECCIONADO - CRÉDITO" THEN "Neutro"
        WHEN "FINALIZADO SIN INTERACCION" THEN "Neutro"
        WHEN "INCIDENTE EN ANDAMIENTO" THEN "Neutro"
        WHEN "Resuelto E-mail N3" THEN "Neutro"
        WHEN "Resuelto MKT N3" THEN "Neutro"
        WHEN "Resuelto N2 E-mail" THEN "Neutro"
        WHEN "Resuelto N2 MKT" THEN "Neutro"
        WHEN "Resuelto N3 E-mail" THEN "Neutro"
        WHEN "VALIDACION - TD LOCAL" THEN "Neutro"
        WHEN "VALIDACION DE LLAMADO" THEN "Neutro"
        WHEN "VALIDACION PLCOM" THEN "Neutro"
        WHEN "VALIDACION  PLCOM" THEN "Neutro"

        // --- CATEGORIA N1 ---
        WHEN "ACTUALIZACION DE LA APP" THEN "N1"
        WHEN "ACTUALIZACIÓN DEL CARRITO" THEN "N1"
        WHEN "ACTUALIZACION DEL NAVEGADOR" THEN "N1"
        WHEN "BIOMETRIA V2 AUTOREGISTRO" THEN "N1"
        WHEN "BLANQUEO DEL REGISTRO" THEN "N1"
        WHEN "CADASTRO DUPLICADO" THEN "N1"
        WHEN "CAMBIO DE EMAIL VOL" THEN "N1"
        WHEN "CAMBIO O REINICIO DE CELULAR/PC/NAVEGADOR" THEN "N1"
        WHEN "CREACION DE SU ESPACIO-CND" THEN "N1"
        WHEN "LIMPIEZA DE CACHE/HISTORIAL" THEN "N1"
        WHEN "LINK ENVIADO" THEN "N1"
        WHEN "REGISTRO CESADO/BLOQUEADO O DESACTIVADO" THEN "N1"
        WHEN "REGISTRO RECHAZADO" THEN "N1"
        WHEN "REHABILITAR TIENDA DIGITAL" THEN "N1"
        WHEN "REPORTE DE MOROSIDAD" THEN "N1"
        WHEN "RESET DE CONTRASENA" THEN "N1"
        WHEN "RESILIÊNCIA EN GSP" THEN "N1"
        WHEN "SOLICITUD DE DATOS - APPS" THEN "N1"
        WHEN "VALIDACION DE DATOS - REGISTRO" THEN "N1"
        WHEN "VALIDACIÓN DE DATOS- INDICADORES" THEN "N1"
        WHEN "VALIDACIÓN DE DATOS-BRM" THEN "N1"
        WHEN "VALIDACIÓN DE DATOS-CND" THEN "N1"
        WHEN "VALIDACION-CAMINO DE CRECIMIENTO" THEN "N1"
        WHEN "VALIDADO SIN INCONVENIENTES" THEN "N1"

        // --- CATEGORIA NÃO CONSIDERAR ---
        WHEN "BUEN DIA/AGRADECIMIENTOS" THEN "Não considerar"
        WHEN "CERRADO DESPUÉS DE HORAS" THEN "Não considerar"
        WHEN "CONTACTO SIN EXITO" THEN "Não considerar"
        WHEN "EXPCN" THEN "Não considerar"
        WHEN "FINALIZADO FUERA DE HORÁRIO" THEN "Não considerar"
        WHEN "HEALTHCHECK" THEN "Não considerar"
        WHEN "INCIDENTE RESUELTO" THEN "Não considerar"
        WHEN "REPORTE DIARIO EXP" THEN "Não considerar"

        // Tudo o que estiver na base e não estiver listado acima:
        ELSE "Não mapeado"
    END
END
```
2. Renomear `Cant. de Atendimientos` → `Valor Atendimento`
3. Remapear `Valor Atendimento`: "1" ← null
4. Mudar tipo: `Valor Atendimento` → integer
5. Remover colunas: `Manter`
6. Calcular `Origem da Linha`:

```
"MKT Completo"
```

→ [76] União de linhas 19

## [75] União de linhas 15 — SuperUnion

← [73] União de linhas 2; [51] Whats

**Union** das entradas acima (colunas com o mesmo nome se juntam; cria `Table Names`).

1. Remover colunas: `Table Names-1`

→ [77] Limpar 12

## [76] União de linhas 19 — SuperUnion

← [74] Nivel

**Union** das entradas acima (colunas com o mesmo nome se juntam; cria `Table Names`).

→ [78] União de linhas 21

## [77] Limpar 12 — Container

← [75] União de linhas 15

→ [79] Remover Status Finalização

## [78] União de linhas 21 — SuperUnion

← [57] Limpar 19; [76] União de linhas 19

**Union** das entradas acima (colunas com o mesmo nome se juntam; cria `Table Names`).

1. Remover colunas: `Table Names-1`
2. Remover colunas: `Table Names`

→ [80] Limpar 21

## [79] Remover Status Finalização — Container

_Descrição:_ Remoção feita em 11/02/26

← [77] Limpar 12

1. Excluir `Status de finalização` em ['"CADASTRO DUPLICADO"']
2. Excluir `Status de finalização` em ['"CAMBIO DE EMAIL VOL"']
3. Excluir `Status de finalização` em ['"CERRADO DESPUÃ‰S DE HORAS"']
4. Excluir `Status de finalização` em ['"CERRADO DESPUÉS DE HORAS"']

→ [81] Limpar 5

## [80] Limpar 21 — Container

← [78] União de linhas 21

1. Remapear `Origem da Linha`: "MKT Completo" ← null

→ [82] MKT Hispana Completo; [83] Limpar 22

## [81] Limpar 5 — Container

← [79] Remover Status Finalização

1. Excluir `Status de finalização` em ['"CONSULTA CON PLCOM"']
2. Excluir `Status de finalização` em ['"AJUSTE/ CORRECCION REALIZADO POR PLCOM"']
3. Excluir `Status de finalização` em ['"VALIDACION PLCOM"']
4. Excluir `Status de finalização` em ['"INCIDENTE RESUELTO"']
5. Excluir `Status de finalização` em ['"PLCOM - CLASSIFICAÇÃO"']
6. Excluir `Status de finalização` em ['"PLCOM-PENDIENTE DE RESPUESTA"']
7. Filtro:

```
NOT ((([Status de finalização] == "INCIDENTE EN ANDAMIENTO") AND NOT (ISNULL([Status de finalização]))))
```

→ [84] Remoção de colunas não usadas

## [82] MKT Hispana Completo — PublishExtract

← [80] Limpar 21

**Saída:** `4. DATASOURCES/MKT Hispana Completo`

## [83] Limpar 22 — Container

← [80] Limpar 21

→ [85] Emails para Retenção

## [84] Remoção de colunas não usadas — Container

← [81] Limpar 5

1. Remover colunas: `Status de Finalização`
2. Remover colunas: `Empresa`, `Nome`, `CPF/CNPJ`, `Número do Contrato`, `Valor do Contrato`
3. Remover colunas: `Origem`
4. Remover colunas: `Status de Classificação 1`
5. Remover colunas: `Função do Sistema 1`
6. Remover colunas: `Detalhe do Sistema`
7. Calcular `Solução Aplicada1`:

```
IF [Solução Aplicada] = 1 THEN 1
ELSEIF [Solução Aplicada] = 2 THEN 2
ELSEIF [Solução Aplicada] = 3 THEN 3
ELSEIF [Solução Aplicada] = 4 THEN 4
ELSEIF [Solução Aplicada] = 5 THEN 5
ELSEIF [Solução Aplicada] = 6 THEN 6
ELSEIF [Solução Aplicada] = 7 THEN 7
ELSEIF [Solução Aplicada] = 8 THEN 8
ELSEIF [Solução Aplicada] = 9 THEN 9
ELSEIF [Solução Aplicada] = 10 THEN 10
ELSEIF [Solução Aplicada] = 11 THEN 11
ELSEIF [Solução Aplicada] = 12 THEN 12
ELSEIF [Solução Aplicada] = 13 THEN 13
ELSEIF [Solução Aplicada] = 14 THEN 14
ELSEIF [Solução Aplicada] = 15 THEN 15
ELSEIF [Solução Aplicada] = 16 THEN 16
ELSEIF [Solução Aplicada] = 17 THEN 17
ELSEIF [Solução Aplicada] = 18 THEN 18
ELSEIF [Solução Aplicada] = 19 THEN 19
ELSEIF [Solução Aplicada] = 20 THEN 20
ELSEIF [Solução Aplicada] = 21 THEN 21
ELSEIF [Solução Aplicada] = 22 THEN 22
ELSEIF [Solução Aplicada] = 23 THEN 23
ELSEIF [Solução Aplicada] = 24 THEN 24
ELSEIF [Solução Aplicada] = 25 THEN 25
ELSE 1
END

```
8. Remover colunas: `Solução Aplicada`
9. Renomear `Solução Aplicada1` → `Solução Aplicada`
10. Remover colunas: `Campos adicionais Web Chat`
11. Cálculo rápido `Função do Sistema`:

```
REPLACE([Função do Sistema], " - CLASSIFICAÇÃO", "")
```
12. Cálculo rápido `Função do Sistema`:

```
REPLACE([Função do Sistema], " - CLASSIFICAÃ‡ÃƒO", "")
```
13. Renomear `Data Contato Fuso` → `Data Contato`
14. Calcular `Hora`:

```
DATEPART('hour', [Data Contato])
```
15. Calcular `Semana`:

```
DATEPART('week', [Data Contato])
```
16. Excluir `Tipo` em ['"Remover"']
17. Calcular `Remover`:

```
[Status de finalização]+[Primeiro Tempo de Espera]
```
18. Excluir `Remover` em ['"VALIDACION DE LLAMADONão atendido"']
19. Excluir `Remover` em ['"VALIDACION DE LLAMADONÃ£o atendido"']
20. Remover colunas: `Remover`
21. Renomear `Table Names` → `Fonte`
22. Remapear `Fonte`: "Tickets" ← null
23. Remapear `Fonte`: "MKT Zap" ← "2020-03-02_mktzap-analitico", "Planilha1,Base", null; "Registro de Grupos" ← "Página1"
24. Duplicar `Fonte-1`:

```
[Fonte]
```
25. Renomear `Fonte-1` → `Fonte dos Dados`
26. Remapear `Fonte`: "MKT Zap" ← "Tickets"
27. Calcular `Tipo2`:

```
IF [Fonte] = "MKT Zap" AND [Tipo] = "Email" THEN
	"Email"
ELSEIF [Fonte]= "MKT Zap" AND [Tipo] =  "WhatsApp" THEN
	"WhatsApp"
ELSEIF [Fonte]= "Registro de Grupos" THEN
	"Requisições"
END
```
28. Remover colunas: `Tipo`
29. Renomear `Tipo2` → `Tipo`
30. Calcular `Tempo Medio - Segundos`:

```
DATEDIFF('second', [Data Contato], [Encerrado em])

```
31. Calcular `Email 1 hora`:

```
IF [Tempo Medio - Segundos] >= 0 AND [Tempo Medio - Segundos] <= 3600 THEN "Dentro de 1 Hora"
ELSEIF [Tempo Medio - Segundos] > 3600 THEN "Acima de 1 Hora"
ELSE "Backlog"
END

```

→ [86] SLA Lojas

## [85] Emails para Retenção — Container

← [83] Limpar 22

1. Calcular `Data Híbrida do Dashboard`:

```
[Data conclusão]
```
2. Excluir `Situação` em ['"Em aberto"']
3. Renomear `Protocol` → `Protocolo`
4. Remover colunas: `Status de finalização`
5. Renomear `Status` → `Status de finalização`
6. Remover colunas: `Tempo Segundos`
7. Remover colunas: `Nome`
8. Remover colunas: `'Atendimentos'(first_message_at)`
9. Remover colunas: `Início Atendimento`
10. Remover colunas: `Atendido`
11. Remover colunas: `Última mensagem`
12. Remover colunas: `Tipo Canal`
13. Remover colunas: `Telefone`
14. Remover colunas: `Regra Status`
15. Remover colunas: `Situação`
16. Remover colunas: `Tempo médio até ser atendidos`
17. Remover colunas: `Tempo médio primeira espera`
18. Remover colunas: `Tempo médio atendimento`
19. Remover colunas: `Tempo médio espera`
20. Remover colunas: `Tempo médio operacional`
21. Renomear `Canal` → `Canal de Entrada`
22. Renomear `Setor` → `Setor Fim`
23. Renomear `Responsável` → `Responsável1`
24. Calcular `Responsável`:

```
IF ISNULL([Operador]) THEN [Responsável1] ELSE [Operador] END
```
25. Remover colunas: `Operador`
26. Remover colunas: `Responsável1`
27. Excluir `Pais` em ['"Latam"']

→ [87] MKT Completo

## [86] SLA Lojas — Container

← [84] Remoção de colunas não usadas

1. Calcular `Data Contato Ajustada`:

```
// Campo: Data Contato Ajustada (Hispana)
// Lógica: Se for Sábado de madrugada (< 03:00), mantém.
// Se for Sábado depois das 03:00 ou Domingo, joga para Segunda.

IF DATEPART('weekday', [Data Contato]) = 1 THEN 
    // Domingo -> Segunda 08:00
    MAKEDATETIME(DATE(DATEADD('day', 1, [Data Contato])), MAKETIME(8,0,0))

ELSEIF DATEPART('weekday', [Data Contato]) = 7 THEN 
    // É Sábado. Precisamos ver a hora.
    IF DATEPART('hour', [Data Contato]) < 3 THEN
        // Madrugada de Sábado (Trabalho) -> Mantém original
        [Data Contato]
    ELSE
        // Sábado dia/noite (Folga) -> Segunda 08:00
        MAKEDATETIME(DATE(DATEADD('day', 2, [Data Contato])), MAKETIME(8,0,0))
    END

ELSEIF DATEPART('hour', [Data Contato]) >= 3 AND DATEPART('hour', [Data Contato]) < 8 THEN 
    // Buraco da Madrugada dias úteis (03:00 - 07:59) -> Hoje 08:00
    MAKEDATETIME(DATE([Data Contato]), MAKETIME(8,0,0))

ELSE 
    [Data Contato]
END
```
2. Calcular `Encerrado em Ajustado`:

```
// Campo: Encerrado em Ajustado (Hispana)

IF DATEPART('weekday', [Encerrado em]) = 1 THEN 
    // Domingo -> Segunda 08:00
    MAKEDATETIME(DATE(DATEADD('day', 1, [Encerrado em])), MAKETIME(8,0,0))

ELSEIF DATEPART('weekday', [Encerrado em]) = 7 THEN 
    // É Sábado.
    IF DATEPART('hour', [Encerrado em]) < 3 THEN
        // Madrugada de Sábado -> Mantém original
        [Encerrado em]
    ELSE
        // Sábado dia/noite -> Segunda 08:00
        MAKEDATETIME(DATE(DATEADD('day', 2, [Encerrado em])), MAKETIME(8,0,0))
    END

ELSEIF DATEPART('hour', [Encerrado em]) >= 3 AND DATEPART('hour', [Encerrado em]) < 8 THEN 
    // Buraco da Madrugada -> Hoje 08:00
    MAKEDATETIME(DATE([Encerrado em]), MAKETIME(8,0,0))

ELSE 
    [Encerrado em]
END
```
3. Calcular `Segundos Úteis`:

```
// Campo: Segundos Úteis (Hispana)
// TRUQUE: Subtraímos 3h para alinhar o fim do turno (03:00) com o fim do dia (00:00)
// Novo Turno Virtual: 05:00 as 24:00 (19h ou 68400s)

// Passo 1: Criar datas virtuais locais
// (No Tableau Prep isso funciona direto. No Desktop pode exigir criar campos calculados separados se der erro, mas tente assim primeiro)

IF DATETRUNC('day', DATEADD('hour', -3, [Data Contato Ajustada])) = DATETRUNC('day', DATEADD('hour', -3, [Encerrado em Ajustado])) THEN
    // Mesmo dia (Virtual): Diferença simples
    DATEDIFF('second', [Data Contato Ajustada], [Encerrado em Ajustado])

ELSE
    // Dias Diferentes
    (
        // 1. Dias Inteiros * 68400
        (
            DATEDIFF('day', 
                DATEADD('day', 1, DATETRUNC('day', DATEADD('hour', -3, [Data Contato Ajustada]))), 
                DATETRUNC('day', DATEADD('hour', -3, [Encerrado em Ajustado]))
            )
            -
            // Desconto de Fim de Semana (Na hora virtual, Sáb e Dom são folgas completas)
            (FLOOR(DATEDIFF('day', 
                DATEADD('day', 1, DATETRUNC('day', DATEADD('hour', -3, [Data Contato Ajustada]))), 
                DATETRUNC('day', DATEADD('hour', -3, [Encerrado em Ajustado]))
            ) / 7) * 2)
        ) * 68400 
    )
    +
    // 2. Saldo do Primeiro Dia
    // Calcula da Hora Real até o teto do dia seguinte (03:00)
    DATEDIFF('second', 
        [Data Contato Ajustada], 
        MAKEDATETIME(DATE(DATEADD('day', 1, DATEADD('hour', -3, [Data Contato Ajustada]))), MAKETIME(3,0,0)) 
    )
    +
    // 3. Saldo do Último Dia
    // Calcula das 08:00 até a Hora Real
    DATEDIFF('second', 
        MAKEDATETIME(DATE(DATEADD('hour', -3, [Encerrado em Ajustado])), MAKETIME(8,0,0)), 
        [Encerrado em Ajustado]
    )
END
```
4. Calcular `Status SLA Email`:

```
// Campo: Status SLA Email (Hispana)

IF NOT ISNULL([Encerrado em]) THEN
    // --- FECHADO ---
    // Usa os segundos (68400s = 19h = 1 dia útil)
    IF [Segundos Úteis] <= 68400 THEN "Dentro do SLA" ELSE "Fora do SLA" END

ELSE
    // --- ABERTO ---
    // Projeção de Calendário
    
    IF NOW() <= 
        (CASE DATEPART('weekday', [Data Contato Ajustada])
            WHEN 6 THEN DATEADD('day', 3, [Data Contato Ajustada]) // Sexta -> Segunda
            WHEN 7 THEN DATEADD('day', 3, [Data Contato Ajustada]) // Sábado -> Terça (CORRIGIDO)
            ELSE DATEADD('day', 1, [Data Contato Ajustada])        // Outros -> Dia Seguinte
        END)
    THEN "Dentro do SLA" 
    ELSE "Fora do SLA" 
    END
END
```

→ [88] Expurgo

## [87] MKT Completo — Container

← [85] Emails para Retenção

1. Excluir `Tipo` em ['"WhatsApp"']
2. Duplicar `Data conclusão-1`:

```
[Data conclusão]
```
3. Renomear `Data conclusão-1` → `Data Contato`

→ [89] União de colunas 6

## [88] Expurgo — SuperJoin

← [31] Limpar 1 (Right); [86] SLA Lojas (Left)

**Join left**: esquerda = [86] SLA Lojas, direita = [31] Limpar 1

Condição: `esq.[Protocolo] == dir.[Protocolo]`

→ [90] Adequação Pais

## [89] União de colunas 6 — SuperJoin

← [63] Limpar 14 (Left); [87] MKT Completo (Right)

**Join right**: esquerda = [63] Limpar 14, direita = [87] MKT Completo

Condição: `esq.[Protocolo analitico] == dir.[Protocolo]`

→ [91] Limpar 23

## [90] Adequação Pais — Container

← [88] Expurgo

1. Remover colunas: `Pais-1`

→ [92] União de colunas 2

## [91] Limpar 23 — Container

← [89] União de colunas 6

1. Renomear `Status de Classificação` → `Status de Classificação1`
2. Calcular `Status de Classificação`:

```
REPLACE([Status de Classificação1], " - CLASSIFICAÇÃO", "")
```
3. Remover colunas: `Status de Classificação1`

→ [96] Analitico + Completo

## [92] União de colunas 2 — SuperJoin

← [90] Adequação Pais (Right); [15] Ticket Medio (Left)

**Join right**: esquerda = [15] Ticket Medio, direita = [90] Adequação Pais

Condição: `esq.[Pais] == dir.[Pais]`

→ [93] SLA com Expurgo

## [93] SLA com Expurgo — Container

← [92] União de colunas 2

1. Remover colunas: `Protocolo-1`, `Pais-1`, `Justificación`, `Autorizado por Natura`
2. Calcular `SLA com Expurgo`:

```
IF[Exento]="Sim" THEN "Dentro do SLA" ELSE [SLA] END
```
3. Calcular `Status de Classificação2`:

```
// Procura pelo texto com erro de codificação ("CLASSIFICAÃ‡ÃƒO")
// e o substitui pela versão correta com "ÇÃO".

REPLACE([Status de Classificação], " - CLASSIFICAÃ‡ÃƒO", " - CLASSIFICAÇÃO")
```
4. Calcular `Status de Classificação3`:

```
// Procura pelo texto com erro de codificação ("CLASSIFICAÃ‡ÃƒO")
// e o substitui pela versão correta com "ÇÃO".

REPLACE([Status de Classificação2], " - CLASSIFICAÇÃO", "")
```
5. Remover colunas: `Status de Classificação`
6. Remover colunas: `Status de Classificação2`
7. Renomear `Status de Classificação3` → `Status de Classificação`
8. Calcular `Data para Vinculo`:

```
DATETRUNC('month', [Data Contato])
```
9. Mudar tipo: `Cant. de Atendimientos` → integer
10. Calcular `Valor Atendimento`:

```
IF [Data Contato] >= #2026-03-01# THEN
    IF [Tipo] = "Requisições" THEN [Solução Aplicada]
    ELSE [Cant. de Atendimientos]
    END
ELSE
    [Solução Aplicada]
END
```

→ [94] Adequar Campos para MKT Completo

## [94] Adequar Campos para MKT Completo — Container

← [93] SLA com Expurgo

1. Calcular `Origem da Linha`:

```
"MKT Analítico"
```
2. Calcular `Data Híbrida do Dashboard`:

```
[Data Contato]
```
3. Calcular `Data criação`:

```
[Data Contato]
```
4. Calcular `Data conclusão`:

```
[Encerrado em]
```

→ [95] MKT Analitico

## [95] MKT Analitico — Container

← [94] Adequar Campos para MKT Completo

1. Remapear `Valor Atendimento`: 1 ← null

→ [96] Analitico + Completo

## [96] Analitico + Completo — SuperUnion

← [91] Limpar 23; [95] MKT Analitico

**Union** das entradas acima (colunas com o mesmo nome se juntam; cria `Table Names`).

→ [97] 

## [97]  — Container

← [96] Analitico + Completo

1. Remapear `Cant. de Atendimientos`: 1 ← null
2. Remapear `Fonte`: "MKT Completo" ← null
3. Remapear `Fonte dos Dados`: "MKT Zap" ← null
4. Remover colunas: `Table Names`

→ [98] Manter Healthcheck; [99] Retirar HealthCheck; [100] Emails Loja

## [98] Manter Healthcheck — Container

← [97] 

1. Manter só `Status de finalização` em ['"HEALTHCHECK"']
2. Excluir `Pais` em ['"Latam"']

→ [101] Limpar 7

## [99] Retirar HealthCheck — Container

← [97] 

1. Excluir `Função do Sistema` em ['"HEALTHCHECK"']
2. Excluir `Status de finalização` em ['"HEALTHCHECK"']
3. Excluir `Pais` em ['"Latam"']
4. Remapear `Responsável`: "Charles Argenis Carrasquel Cerezo" ← "charlescerezo.sonda@natura.net"; "Edilber  Orellana" ← "Edilber Jesus Armeya Orellana"; "ELIANNY MARIELIS RODRIGUEZ BARRIOS" ← "eliannybarrios.sonda@natura.net"; "Ghandy Giovanny Gautier Gomez" ← "ghandygomez.sonda@natura.net"; "Grefanny Mercedes Rodríguez berro" ← "Grefanny Mercedes RodrÃ­guez berro", "grefannyberro.sonda@natura.net"; "Ivan Moralez Díaz" ← "Ivan Moralez DÃ­az", "ivandiaz.sonda@natura.net"; "Jaimeli Orianis Moreno Calvo" ← "jaimelicalvo.sonda@natura.net"; "Jason Jose Bello Fonten" ← "Jason Jose Bello Fonten - INATIVO"; "Katiuska Maineth Labarca Quintero" ← "katiuskaquintero.sonda@natura.net"; "Luis Antolines" ← "luisantolines.sonda@natura.net"; "MAHOLI DEL VALLE LEONET SUBERO" ← "MAHOLI DEL VALLE LEONET SUBERO - INATIVO"; "María Inés Ovalles" ← "MarÃ­a InÃ©s Ovalles", "mariaovalles.sonda@natura.net"; "Reggie Sanchez" ← "Reggie Sanchez - INATIVO"; "Paola Gabriela Gonzalez Gomez" ← "paolagomez.sonda@natura.net"; "Maria Isabel Alvarado Rodriguez" ← "mariarodriguez.sonda@natura.net"; "Vico Casini" ← "Vico Casini - INATIVO", "Casini Vico"; "Vacio" ← "NULL", "", ". - INATIVO", "a - INATIVO", "vacio - INATIVO", null, "ddd - INATIVO", "ex integrante - INATIVO"; "Viannys Del Valle Moreno Moya" ← "viannysmoya.sonda@natura.net"; "Cristian Torres" ← "cristiantorres.sonda@natura.net"; "Cristian Abel Rodriguez" ← "cristianrodriguez.sonda@natura.net"; "Juan Manuel Figueira de Sousa" ← "juansousa.sonda@natura.net"
5. Remapear `Pedidos Finalizados`: "NO" ← "No", "No Aplica", "NO SE APLICA"

→ [102] Valor Atendimiento

## [100] Emails Loja — Container

← [97] 

1. Filtro:

```
([Setor Fim] == "APP NATURA" OR [Setor Fim] == "APP NATURA LATAM" OR [Setor Fim] == "MI NEGOCIO" OR [Setor Fim] == "APP AVON")
```
2. Remapear `Setor Fim`: "APP NATURA" ← "APP NATURA LATAM"
3. Calcular `Função do Sistema1`:

```
IF [Pais] = "Ecuador" AND [Função do Sistema] = "PEDIDO NO APARECE EN SALESFORCE" THEN 
    "PEDIDO NO APARECE EN SAP"
ELSE
    [Função do Sistema]
END
```
4. Remover colunas: `Função do Sistema`
5. Renomear `Função do Sistema1` → `Função do Sistema`

→ [103] Base MKT Lojas OIS; [104] Email Lojas

## [101] Limpar 7 — Container

← [98] Manter Healthcheck

1. Calcular `Valor Atendimento`:

```
IF [Data Contato] >= #2026-03-01# THEN [Cant. de Atendimientos]
ELSE [Solução Aplicada]
END
```
2. Calcular `Função do Sistema1`:

```
IF [Pais] = "Ecuador" AND [Função do Sistema] = "PEDIDO NO APARECE EN SALESFORCE" THEN 
    "PEDIDO NO APARECE EN SAP"
ELSE
    [Função do Sistema]
END
```
3. Remover colunas: `Função do Sistema`
4. Renomear `Função do Sistema1` → `Função do Sistema`

→ [105] Base MKT HC OIS

## [102] Valor Atendimiento — Container

← [99] Retirar HealthCheck

1. Calcular `Função do Sistema1`:

```
IF [Pais] = "Ecuador" AND [Função do Sistema] = "PEDIDO NO APARECE EN SALESFORCE" THEN 
    "PEDIDO NO APARECE EN SAP"
ELSE
    [Função do Sistema]
END
```
2. Remover colunas: `Função do Sistema`
3. Renomear `Função do Sistema1` → `Função do Sistema`

→ [106] Base MKT OIS; [107] MKT Ois

## [103] Base MKT Lojas OIS — PublishExtract

← [100] Emails Loja

**Saída:** `4. DATASOURCES/Base MKT Lojas OIS`

## [104] Email Lojas — Container

← [100] Emails Loja

1. Calcular `Saida`:

```
"Emails de Loja"
```

→ [108] União de linhas 9

## [105] Base MKT HC OIS — PublishExtract

← [101] Limpar 7

**Saída:** `4. DATASOURCES/Base MKT HC OIS`

## [106] Base MKT OIS — PublishExtract

← [102] Valor Atendimiento

**Saída:** `4. DATASOURCES/Base MKT OIS`

## [107] MKT Ois — Container

← [102] Valor Atendimiento

1. Calcular `Saida`:

```
"Base MKT OIS"
```

→ [108] União de linhas 9

## [108] União de linhas 9 — SuperUnion

← [104] Email Lojas; [107] MKT Ois

**Union** das entradas acima (colunas com o mesmo nome se juntam; cria `Table Names`).

→ [109] Remoção de colunas

## [109] Remoção de colunas — Container

← [108] União de linhas 9

1. Manter só: `Fonte`, `Função do Sistema`, `Tipo`, `Nivel`, `Origem da Linha`, `Solução Aplicada`, `Status de Classificação`, `Saida`, `Protocolo`, `Setor Fim`, `Status de finalização`, `Data Contato`, `Responsável`, `Cant. de Atendimientos`, `Valor Atendimento`, `Encerrado em`, `Pais`
2. Remapear `Fonte`: "MKT Completo" ← null
3. Calcular `Filtro Base Duplicada`:

```
IF [Tipo] = "Email" AND [Origem da Linha] = "MKT Analítico" AND [Data Contato] >= #2026-03-01# THEN
    "Remover"
ELSE
    "Manter"
END
```
4. Excluir `Filtro Base Duplicada` em ['"Remover"']
5. Remover colunas: `Filtro Base Duplicada`
6. Excluir `Nivel` em ['"Não considerar"']
7. Remover colunas: `Cant. de Atendimientos`
8. Remover colunas: `Solução Aplicada`
9. Renomear `Data Contato` → `Data`

→ [110] MKT

## [110] MKT — Container

← [109] Remoção de colunas

→ [111] União de linhas 11

## [111] União de linhas 11 — SuperUnion

← [110] MKT; [44] Resenhas

**Union** das entradas acima (colunas com o mesmo nome se juntam; cria `Table Names`).

1. Remover colunas: `Table Names`

→ [112] Limpar 11

## [112] Limpar 11 — Container

← [111] União de linhas 11

1. Remapear `Fonte`: "Resenhas" ← null
2. Remapear `Tipo`: "Resenhas" ← null
3. Remapear `Origem da Linha`: "Resenhas" ← null
4. Remapear `Saida`: "Resenhas" ← null

→ [113] Responsavel

## [113] Responsavel — Container

← [112] Limpar 11

1. Remapear `Responsável`: "Cristian Abel Rodriguez" ← "Cristian Abel Rodriguez - INATIVO"; "Cristian Torres" ← "cristiantorres.sonda@natura.net"; "ELIANNY MARIELIS RODRIGUEZ BARRIOS" ← "eliannybarrios.sonda@natura.net"; "Ghandy Giovanny Gautier Gomez" ← "ghandygomez.sonda@natura.net"; "Grefanny Mercedes Rodríguez berro" ← "Grefanny Mercedes RodrÃ­guez berro", "grefannyberro.sonda@natura.net"; "Ivan Moralez Díaz" ← "Ivan Moralez DÃ­az", "ivandiaz.sonda@natura.net"; "Katiuska Maineth Labarca Quintero" ← "katiuskaquintero.sonda@natura.net"; "Luis Antolines" ← "Luis Antolines - INATIVO", "luisantolines.sonda@natura.net"; "Lupe Sara Otondo Loayza" ← "lupeloayza.sonda@natura.net"; "MARIA JOSE DE LA CRUZ FLOREZ" ← "mariaflorez.sonda@natura.net"; "MARIA BELEN LA GIGLIA LUQUE" ← "marialuque.sonda@natura.net"; "María Inés Ovalles" ← "mariaovalles.sonda@natura.net"; "Maria Isabel Alvarado Rodriguez" ← "mariarodriguez.sonda@natura.net"; "Paola Gabriela Gonzalez Gomez" ← "paolagomez.sonda@natura.net"; "Saulo Jimenez" ← "sauloordaz.sonda@natura.net"; "Viannys Del Valle Moreno Moya" ← "viannysmoya.sonda@natura.net"; "Vico Casini" ← "osvaldocasini.act@natura.net", "Casini Vico"; null ← "", "vacio - INATIVO", "Vacio", "ddd - INATIVO", "a - INATIVO", ". - INATIVO"

→ [114] Experiencia Hispana Produtividade

## [114] Experiencia Hispana Produtividade — PublishExtract

← [113] Responsavel

**Saída:** `4. DATASOURCES/Experiencia Hispana Produtividade`
