# Book Executivo: números do mês a partir do Databricks

Gera, para um mês, a linha de cada aba das planilhas do Book Executivo, lendo as tabelas gold do Databricks
(`sandbox.sustentacao_bau_experiencias.dexp_gold_*`), que são cópias das fontes publicadas no Tableau Cloud. As regras de
cada número reproduzem as planilhas dos painéis do Tableau (citadas no código) e o Manual de Indicadores.

## Uso

A partir desta pasta, com a CLI do Databricks configurada no perfil `daily-exp` (o mesmo do projeto `daily-experiencia`):

```powershell
python executar.py brasil 2026-10              # gera outubro em saida\brasil_2026-10.md
python executar.py brasil 2026-09 --validar    # compara setembro com gabaritos\brasil_2026-09.json
```

Colunas marcadas como `manual` não saem do Databricks e continuam sendo preenchidas à mão.

## Validação

O gabarito de um mês é a linha que já está no Book (`gabaritos/<frente>_<mês>.json`). Uma aba só deve ser usada depois
de bater com o gabarito.

| Aba | Setembro/2026 | Observação |
|---|---|---|
| `Exp_Br_Indicadores_Contratuais` | 5 de 6 iguais (2 manuais) | Retenção N1 dá 70,27%; o Book tem 70,39%. O Tableau de produção hoje também dá 70,27%: os dados mudaram depois do preenchimento (07/10). |
| `Exp_Br_Indicadores_Monitoracao` | 5 de 6 iguais | SLA Prazo Cliente dá 96,61%; o Book tem 96,62%. Mesmo caso: a produção hoje também dá 96,61%. |
| `Exp_Br_Cards01` | 9 de 10 iguais (1 a investigar) | Protocolos CB e CF: 2.176 × 2.178 (dados mudaram). "Resenhas 4 e 5" ainda sem regra. |
| `Exp_Br_Retencao` | 2 de 5 iguais | Diferenças de 1 unidade ou 0,01 p.p. (dados mudaram): Ocorrências 1.890 × 1.891, Retenção N1 70,38% × 70,39%. |
| `Exp_Br_Cards2` | 3 de 6 iguais (1 a investigar) | Retenção Tarefas 76,03% × 76,04% e SLA Tarefas 86,03% × 85,99% (dados mudaram). "TMA E-mail" ainda sem regra. |

| `Exp_Br_Reativos_WA_Mensal`, `Exp_Br_WA_GN/GV/Franq/CBCom_Mensal` | todas iguais | |
| `Exp_Br_Email_Mensal` | todas iguais | O TMA (01:34:47) é a média do tempo de operação com o filtro de status de finalização do painel. |
| `Exp_Br_Email_TMO` | 3 de 4 iguais | "TMO N2 - Origem WhatsApp": o Book tem 203:05:27, mas a monitoração do mesmo mês tem "04 dias" (o programa dá 114:44:46, que bate com a monitoração). O próprio Book está inconsistente nesse número. |
| `Exp_Br_Tarefas_CB_Mensal` | todas iguais | |
| `Exp_Br_Tarefas_Historico_Mensal`, `Exp_Br_Tarefas_CF_Mensal` | diferenças de 1 protocolo | Dados mudaram depois do preenchimento. Em CF, o Book tem N1 = 78% em setembro (os meses anteriores ficam em ~96%, como o programa): parece digitação. |
| `Exp_Br_Tarefas_CB_Fase`, `Exp_Br_Tarefas_CF_Fase` | volumes iguais (±1) | Fase 1 CB: 99,61% × "100%"; CF usa percentuais inteiros no Book. |
| `Exp_Br_ReqEvent_Mensal` | quantidade igual | Volume N1/N2 ainda sem regra. |

| Abas de motivos (`*_Motivos_N1/N2`, `Tarefas_CB/CF_Motivo_N1/N2`) | WA N1 e Tarefas CB N1: 15 de 18 | Regra: as 3 maiores plataformas (Tribo) e, em cada uma, os 3 maiores motivos (Macro), contando linhas e juntando grafias que só mudam em maiúsculas. Diferenças: erros de digitação no Book ("Acesso" 172 × 164; "Manu" por "Menu") e 2 tarefas a mais em AIBV/Cadastro (dados mudaram). Tarefas usam a visão "Encerrado em", só "Normal". |

| `Exp_Br_Proativos_Mensal`, `_Contatos_Pedidos`, `_HC_Mensal` | todas iguais (1 a investigar) | "Alcance %" do Health Check ainda sem regra. |
| `Exp_Br_Email_Natura_Expcb/AppNatura/AppAvon_Mensal` e `_SLA` | todas iguais | Volumetria e SLA contam só e-mails encerrados; sem e-mails no mês, "0" e "Sem dados" (como o Book). |
| `Exp_Br_CSAT_3Meses`, `_Classificacao`, `_Nota` | todas iguais | Contagem por protocolo distinto (a fonte tem uma linha por pergunta da enquete). O C-SAT daqui (promotores ÷ respondidas) é diferente do CSAT dos indicadores contratuais (média das notas). **Só os setores do C-SAT** (`SETORES_CSAT`, sem o ATIVOS): é a base do C-SAT oficial (out/2026: 87,90%) e da análise de qualidade dos detratores (`Exp_Br_CSAT_Analise_Quald`; out: 30 detratores = 23 corretos + 7 de melhoria). Junho/2026 bate exatamente com essa regra; setembro/2026 foi gravado com todos os setores (88,22% em vez de 88,97%) e não foi alterado. Outubro foi regravado com a regra em 09/11/2026 (antes: 87,09%, 1.627 enviadas, 906 respondidas e 41 detratores, contando os 11 do ATIVOS). |
| `Exp_Br_CSAT_Mercado` | 3 de 5 | Araucária e Atlântica diferem alguns décimos; a regra de mercado pode juntar outros códigos. |
| `Exp_Br_CSAT_Ofensores_Detr` | 2 de 3 | Empate no 3º lugar (vários com 2 casos): o programa escolhe pela ordem alfabética. |

| `Exp_Br_Resenhas_<app>_01` a `_06` (Minha Consultoria, FV, App Natura, App Avon) | iguais, fora 1 avaliação a mais em Minha Consultoria (dados mudaram) | 01: média de estrelas do mês e de todas as avaliações até o fim do mês; 02 e 03: avaliações das lojas (Resenhas Brasil); 04 a 06: respostas do time (AppSheets): SLA, tipo (categoria) e motivo (categoria 2). App Natura = "App Sempre Presente". |
| `Exp_Br_Resenhas_<app>_07` | parcial | Linha 2 (1 a 3 estrelas) sai das respostas do AppSheets; a contagem de 4 e 5 estrelas respondidas ainda não bate (Minha Consultoria: Book 30, testes 24–27). |

Manuais (texto): `Exp_Br_Highlights`, `Exp_Br_Lowlights`, `Exp_Br_Proativos_HC_Comentarios`, `Exp_Br_CSAT_Comentarios`,
`Exp_Br_CSAT_Analise_Quald`, abas `Exp_Br_QA_*`.

Regras conferidas com setembro/2026 e usadas para gravar outubro em 06/11/2026 (calculadas por consulta, ainda fora do `executar.py`):

| Aba | Regra |
|---|---|
| `Exp_Br_Desempenho_Ferramenta` | SLA do primeiro contato de cada WhatsApp (GN, GV, Franquia, CBCom, GV Antecipada) e SLA Tarefas do Cards2; texto = diferença em p.p. contra o mês anterior gravado. Setembro bate. |
| `Exp_Br_Top3_Plataformas` | WhatsApp reativos (5 setores), níveis N1, N2 e NEUTRO: 3 maiores tribos × 3 maiores motivos (macro). Setembro bate (AIBV 524, FV 435, Cognito 343). |
| `Exp_Br_Solicitacoes_Dia` | Soma de Qtd Atendimentos por dia e nível (N1, N2) da Experiencia Brasil Nivel. Setembro bate dia a dia. |
| `Exp_Br_Tarefas_Top3_N1` | Apesar do nome, todos os níveis: tarefas "Encerrado em", retrabalho Normal, 3 tribos × 3 motivos. Setembro: Exp. Compras 374 = 240 N1 + 134 N2. |
| `Exp_Br_Tarefas_Top3_N2` | Mesma regra, só N2. Setembro: Exp. Compras 134 bate; AIBV 169 × 168 e FV 51 × 57. |
| `Exp_Br_Email_*_Assunto` | E-mails de loja encerrados do setor, campo Função do Sistema 2, 3 maiores sem "Não especificado". Sem e-mails no mês: linha "Sem dados". |
| `Exp_Br_ReqEvent_Motivos_N1/N2` | Mês sem requisições: uma linha "Sem requisições eventuais no mês" com volume 0 (pedido da Juliana, para não parecer erro). |
| `Exp_Br_Email_TMO` | Valores são durações (dias); desde 06/11/2026 a coluna usa o formato `0.0 "dias"`. O Book lê o valor, não o texto. |

Ainda sem regra: `Exp_Br_Top3_Plataformas`, `Exp_Br_Tarefas_Top3_N1/N2`, `Exp_Br_ReqEvent_Motivos_*`, volume N1/N2 de
Requisições Eventuais e "Resenhas 4 e 5".

**Franquias (decidido em 04/11/2026):** até setembro os protocolos de Franquias vinham como "Protocolos CB" e entravam
na retenção e nas Ocorrências; depois passaram a ter tipo próprio, que o filtro do painel não inclui. O programa
continua incluindo esses protocolos (agrupados em "SERVICE CLOUD / DYNAMICS"), para manter a série comparável.

## Hispana (México e Sur)

```powershell
python executar.py mexico 2026-10              # Book Executivo Hispana Mexico
python executar.py sur 2026-10                 # Book Executivo Hispana Sur (Argentina + Chile)
python executar.py mexico 2026-09 --validar    # compara com gabaritos\mexico_2026-09.json
```

Regras (painéis "Daily Mexico OIS" e "Experiência Hispana Sur - Daily", tabelas `dexp_gold_hispana_*`):

- **Volumes e níveis:** nível consolidado do painel. E-mail a partir de março/2026 conta pelas linhas do MKT Completo;
  WhatsApp e Requisições (grupos) pelo MKT Analítico. Só N1, N2 e Neutro; mês da data de contato. Retenção = N1 / (N1 + N2).
- **SLA WhatsApp:** linhas de WhatsApp do MKT Analítico, dentro / (dentro + fora) do SLA com expurgo.
- **Pedidos convertidos:** quantidade de LINHAS do MKT Analítico com Pedidos Finalizados = "SI", sem diferenciar maiúsculas (a base tem "SI" e "Si"), × ticket médio do país no mês. Corrigido em 05/11/2026: antes o programa somava "Cant. de Atendimientos" e só de "SI". Com a regra nova, setembro bate país a país com o Book e outubro dá 4.892 / R$ 3.185.569,25, o número da Juliana.
- **Motivos e causa raiz:** 3 maiores plataformas (status de classificação, sem as filas de acompanhamento) e, em cada
  uma, as 3 maiores funções do sistema.
- **CSAT:** enquetes `fonte = 'Hispana'` do país, por protocolo distinto. **A partir de out/2026** (decisão de 09/11/2026), sem as enquetes do canal PRO ACTIVO (WhatsApp proativo), como o ATIVOS no Brasil: a análise de qualidade dos detratores não as considera. Em out/2026 isso tirou 19 enviadas e 7 respondidas, entre elas o único detrator do canal (México, protocolo 1531-2628401036571). Com isso, os detratores da Hispana fecham com a análise: 24 + 59 = 83 = 62 corretos + 21 inconformes. Até set/2026 o canal estava incluído; os meses fechados não foram alterados. Regra em `filtro_canal_csat` (`book/hispana.py`).

| Setembro/2026 | México | Sur | Observação |
|---|---|---|---|
| Conferência | 83 de 96 | 94 de 116 | |
| Volumes de WhatsApp, grupos, retenção total, SLA, solicitações por dia, motivos, causa raiz, CSAT | iguais | iguais | Empates no 3º ofensor detrator: o programa escolhe pela ordem alfabética. |
| E-mails | 262 × 33 | 932 × 644 | Os tickets de e-mail de setembro concluídos depois do preenchimento entraram na base (agosto bate: 330). Por isso o total e a retenção de e-mail também diferem. |
| TMA E-mail | não confere | 03:36 × 03:41 | Regra provável: média do tempo de operação dos e-mails N1 e N2 do MKT Analítico. |
| Pedidos convertidos | iguais (1.290) | iguais (1.691) | Depois da correção de 05/11/2026 (contar linhas "SI"/"Si"). |

Sem regra (ficam em branco): **Health Check** (vem da planilha "Healthcheck Paises Consolidado", fora do Databricks).
Manuais: Comentarios dos Cards1, `*_CSAT_Analise_Quald`, `*_CSAT_Comentarios` e o texto de `*_CSAT_Paises_Ofensor`.
Nas abas `*_Pais` e `*_CSAT_Paises_3_Meses` a coluna A é o país e a B é o mês.

## Planilha geral "Book Executivo" (Hispana consolidada, Mercado Andino, CSAT e resenhas da Hispana)

```powershell
python executar.py geral 2026-10
python executar.py geral 2026-09 --validar     # compara com gabaritos\geral_2026-09.json
```

É a planilha que o Apps Script lê como `EXECUTIVO_SS_ID` (`1QABgQDBqWPCHunLU84uxy6P__zJKPAPqnnRCmzp9rJ8`). Usa as mesmas
regras de `book/hispana.py`: Andino = Colômbia, Equador e Peru; Hispana consolidada ("OIs") = os seis países.
Os países aparecem em português e as abas `*_Pais` e `*_CSAT_Paises_3_Meses` têm o país na coluna A.

Setembro/2026: 184 de 265 colunas iguais. Além dos e-mails que entraram depois (como no México e no Sur):

| Assunto | Situação |
|---|---|
| Pedidos convertidos do Andino | Iguais país a país depois da correção de 05/11/2026 (Colômbia 512, Equador 492, Peru 759). |
| Resenhas 01 a 03 (média, volume, estrelas) | Regra certa; o Book tem 3 a 4% menos avaliações (as lojas acrescentam avaliações depois). |
| Resenhas 07 | Só a linha 2 (respostas a 1 a 3 estrelas). |
| Resenhas 04, 05, 06, 08, 09, 10 (regras de 06/11/2026, conferidas de junho a agosto; setembro foi lançado com uma foto anterior da base) | **04 e 09**: respostas do AppSheets do app com 1 a 3 estrelas, pelo mês de `fecha_de_la_respuesta_exp`, % com `status_sla_hispana` = "Dentro do SLA"; na 09, >D+2 = 100% − D+1. **05**: contagem por `categoria_de_la_respuesta` (mesmo recorte). Desde 18/09/2026 o time preenche "-" nesse campo (como no Brasil); outubro inteiro veio "-" e foi lançado como "Sem categoria no AppSheets". **06**: 5 maiores `categoria_de_la_respuesta_2` (o Book traduz alguns nomes: Acceso → Acesso, Funcionalidad → Funcionalidade no Mi Negocio). **08**: e-mails da `dexp_gold_hispana_base_mkt_lojas` por `setor_fim` (MI NEGOCIO, APP NATURA, APP AVON) e data de contato; TMO = média de `tempo_de_operacao_segundos`, truncada em hh:mm:ss. **10**: 3 maiores `funcao_do_sistema` desses e-mails. Out/2026: Mi Negocio 93,65% / 33 e-mails / 02:07:37; Natura Latam 82,35% / 9 / 03:28:45; App Avon 80% / 1 / 06:21:31. |
| Monitoração | TMO N2/N3 de origem WhatsApp e N2 de origem e-mail batem. **N3 de origem e-mail**: status "Resuelto E-mail N3" (a Matriz de Indicadores; o programa usava "N3 – E-mail – Pendientes – JIRA"), média truncada em 1 casa; jun a set batem; out = 26,8 dias. **TPA de resenhas**: mesma regra da Resenhas 04 com os três apps juntos; jun a set batem (set 66/145 = 45,51%, truncado); out = 119/136 = 87,50%, igual à planilha da Juliana. |
| Cards (`Exp_Hisp_OIs_Pag_1_Cards`), regras de 05/11/2026 | **Resenhas 1 a 3**: respostas do AppSheets dos três apps no mês (= soma da linha 2 das `_07`); jun 116 e set 114 batem, jul 85 × 84 e ago 131 × 113 (respostas registradas depois). **E-mails Loja**: todas as linhas da `dexp_gold_hispana_base_mkt_lojas` pela data de contato, sem filtro de nível; jun a ago batem, set 60 × 38. **Líderes Equador**: Setor Fim "LNN EC" e "LNN EC - Email", só MKT Analítico, todos os níveis; ago e set batem, jul 78 × 79 (com os e-mails do MKT Completo, outubro iria de 42 para 45). O mesmo número vai no card do Andino (`Exp_Hisp_Pag_4_Mercado_Andino_Cards`), onde julho tem 110 no Book. |
| Cards, fora do Databricks | **Soporte Experiencia**: exportação do ServiceNow `sc_req_item.xlsx` (item "Soporte Experiencia CB OIs"), contando todos os RITMs pela data de criação, em qualquer fase, sem a coluna País = BRA (testes, segundo a Juliana em 05/11/2026); jul 55, ago 79 e set 159 batem; nenhum BRA em outubro. Card da Hispana: total sem Brasil, out = 272. Card do Andino, a partir de outubro/2026 (decisão de 05/11/2026): só Colômbia, Equador e Peru, pela segunda coluna de país (a do afetado), out = 215 (90 + 44 + 81). Até setembro o Andino usava o total, porque quase todos os casos eram da Colômbia e do Peru. **Health Check** e **Resenhas 4 e 5**: vêm da planilha da Juliana "<mês> - Dados para o Book" (aba OIs; texto em vermelho = ainda não confirmado). Health Check OIs = soma dos mercados (out: Andino 402 + Sur 912 + México 282 = 1.596). **SLA Geral do Andino** = SLA WhatsApp do Andino (`Exp_Hisp_Pag_5_Mercado_Andino_Cards`): jun a ago iguais, set 96,39% × 97,25%; out = 96,71%. |
| Indicadores contratuais | **TMR e-mail N1** = % de e-mails respondidos em até 1 hora: planilha "EMAIL % 1 Hora" do painel "Llamados MKT" (Experiência Hispana - Daily). Base MKT OIS, `tipo` = Email, `origem_da_linha` = MKT Analítico, `email_1_hora` em ("Dentro de 1 Hora", "Acima de 1 Hora"), sem os status de classificação "EN ACOMPAÑAMIENTO TD" e "Pendientes – JIRA", todos os níveis (apesar do "N1" no nome), pela data de contato. % = "Dentro de 1 Hora" ÷ total. Set/2026 bate exatamente (27/719 = 3,76%); jun a ago batem com a mesma regra sem a exclusão de status (5,08%, 3,61%, 1,49%), que deve ter entrado no painel depois. Out/2026 = 84/791 = 10,62% (gravado em 06/11/2026). Notificação de Incidente e QA manuais. |
| Pedidos convertidos nos meses fechados (conferência de 06/11/2026, regra corrigida) | Out/2026 certo nas quatro planilhas (México 1.442, Sur 2.129, Andino 1.321, OIs 4.892). Jul e set batem país a país, salvo um erro de digitação no Chile de julho no Book do Sur (R$ 528.826,53; a base dá R$ 527.826,53). Ago: o Book usou um ticket único de R$ 572,38 para todos os países, em vez do ticket de cada país; a quantidade bate, o valor por país não (o total da OIs fica perto: R$ 2.659.262,65 × R$ 2.661.326,41). Jun: o Book do Sur tem 1.465 pedidos, a base dá 1.430 (a OIs, 4.467, bate). Nada foi alterado nos meses fechados. |

Fora do programa: `Interacoes_Mes` (soma de NCC + Brasil + Hispana), `Hisp_HC_3Meses`, QA, Highlights e Lowlights.

Regras da `Interacoes_Mes` (conferidas em agosto e setembro/2026; outubro preenchido em 05/11/2026):

| Coluna | Regra |
|---|---|
| Torre Técnica | Volumetria total do 80x20 (N1 + N2) + Changes + Requisições (`NCC_8020` + `NCC_Changes` + `NCC_TT_REQ`). Até junho/2026 só entrava o N1 (Juliana, 05/11/2026). Julho tem só o 80x20 total; Changes e Requisições entram a partir de agosto. Out = 9.456 + 131 + 75 = 9.662. |
| Gestão de Alerta | Gestão + Impacto Evitado (`NCC_GA`). |
| SEV 3 / Incidentes Críticos | `NCC_SEV3` e `NCC_IC` (volumetria total). |
| Interações NCC | Torre Técnica + SEV 3 + Gestão de Alerta + Incidentes Críticos. |
| Experiência Hispana | Soma das colunas de volume de `Exp_Hisp_OIs_Pag_1_Cards` (WhatsApp, e-mails, Health Check, grupos, resenhas 1 a 3 e 4 e 5, E-mails Loja, Soporte, Líderes Equador). |
| Experiência BR | Soma das colunas de volume de `Exp_Br_Cards01` (WhatsApp, e-mails, Health Check, Dynatrace, resenhas, protocolos CB/CF, E-mails Loja, Requisições Eventuais). |
| Atendimentos Experiência / Total Geral | Fórmulas `=I+J` e `=C+H`. |
| Pedidos e valor | Cards da Hispana e Indicadores Contratuais do Brasil. Out/2026 = 4.892 / R$ 3.185.569,25 depois da correção da regra (igual à planilha da Juliana). |

## Estrutura

| Caminho | Conteúdo |
|---|---|
| `executar.py` | Linha de comando: gera o mês e, com `--validar`, compara com o gabarito |
| `book/databricks.py` | Consulta ao SQL Warehouse pela CLI do Databricks |
| `book/formatos.py` | Formatos do Book ("98,85%", "R$ 1.234,56", "04 dias") |
| `book/brasil.py` | Uma função por aba do Book Exp Brasil |
| `gabaritos/` | Valores já lançados no Book, usados na validação |
| `saida/` | Resultado de cada execução |
