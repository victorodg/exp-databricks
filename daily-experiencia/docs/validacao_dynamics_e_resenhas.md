# Validação – Dynamics e Resenhas

Comparação das 6 tabelas gold com os extracts publicados no Tableau Cloud (atualizados em 27/10/2026 às 09:15 de
Brasília), usando as planilhas capturadas no mesmo dia. Ferramentas: `ferramentas/comparar_extract.py` (perfil
coluna a coluna) e `ferramentas/consultar_extract.py` (mesma consulta nos dois lados).

## Resultado

| Gold | Extract | Linhas (extract = gold) | Campos calculados |
|---|---|---|---|
| `dexp_gold_dynamics_tarefas` | Dynamics - Termino Real | 131.309 | iguais, exceto Tipo Protocolo em 165 linhas (abaixo) |
| `dexp_gold_dynamics_nivel` | Dynamics Nivel | 55.060 | iguais |
| `dexp_gold_dynamics_rechamada` | Dynamics - Base para Rechamada | 16.431 | iguais |
| `dexp_gold_servicenow_chamados` | EXPBR - Chamados Servicenow | 31.044 | iguais |
| `dexp_gold_resenhas_appsheets` | Resenhas EXP BR AppSheets | 9.229 | iguais |
| `dexp_gold_resenhas_brasil` | Resenhas Brasil | 569.995 | iguais |

## Diferenças que sobraram

- **Tipo Protocolo (165 tarefas):** Salesforce, tipo "Atendimento Franquias", visão "Criado em", set–out/2026. O extract
  traz "Protocolos CB"; a fórmula do `.tfl` local dá "Franquias" (e é o que o próprio extract traz na visão "Encerrado em").
  A fórmula é idêntica nas etapas [63] e [72] do arquivo local, então o fluxo publicado no Tableau Cloud deve ser
  outra versão. **Decisão (27/10/2026): o correto é "Franquias"**, como na gold; a produção está errada nessas linhas.
- **Grafias que só mudam maiúsculas** ("Pós-compra" × "Pós-Compra"): o extract do Tableau guarda uma grafia só para
  textos iguais sem diferenciar maiúsculas. Vai acontecer igual quando o Tableau ler do Databricks.
- **Textos livres** (descrições, comentários, anotações): pequenas diferenças na contagem de distintos e no mínimo/máximo,
  por causa da ordenação da collation do Tableau. Não afetam nenhuma métrica.
- **Colunas sem cabeçalho** (F7, F31 a F34 do ServiceNow): não foram levadas para a gold.

## Comportamentos do Prep reproduzidos

- Texto comparado sem diferenciar maiúsculas (collation LPT_RBR_S2), e espaços do fim dos textos removidos na leitura.
- Filtros de data "a partir de" / "até" / "intervalo" com os limites exatos gravados no fluxo.
## Correções em relação à produção

- **Flag de Rechamada e Tarefa Status (28/10/2026):** no join [84] do Prep o sufixo "-1" vai para o lado da própria
  ocorrência, e a flag testava essa coluna: toda ocorrência com código e tribo saía como "Rechamada" (12.391 de 16.431).
  Agora a flag testa `id_rechamada`, que só é preenchido quando a ocorrência casa com o mês anterior (107).
  O painel "% Rechamada 6 meses" não muda: o numerador do workbook já é
  `{ FIXED [Mes/Ano] : COUNTD(IF [Flag de Rechamada] = 1 THEN [ID Rechamada] END) }` (mai–out/2026: 1,44%, 0,85%,
  0,42%, 0,83%, 0,90%, 0,26%). Muda só a coluna Flag da planilha "Tabela de Tarefas Rechamada", que passa a mostrar 1
  apenas nas rechamadas de fato.
- **Status SLA de Resenhas Brasil (27/10/2026):** o "+ 86399" da fórmula soma 86.399 dias no Tableau, e o ramo
  "última interação do EXP, 1 a 3 estrelas" sempre dava "Dentro do SLA". Corrigido para 86.399 segundos (prazo até
  23:59:59 do dia limite). Efeito com os dados de 27/10: 17.775 das 39.851 avaliações desse ramo passam a "Fora do SLA";
  no Status SLA 2 (só avaliações com texto), "Dentro do SLA" cai de 83,6% para 68,8% em 2026 e de 91,0% para 79,9% em 2025.
- **Tipo Protocolo das Franquias:** ver acima; a gold traz "Franquias", que é o correto.

## Expurgo de SLA por tarefa (29/10/2026)

Antes só existia o expurgo de nível (aba "Página1" da planilha Expurgo: o nível da ocorrência passa a ser o da planilha).
Para tirar tarefas dos indicadores de SLA foi criada a aba **"Expurgo SLA"** na mesma planilha, uma linha por tarefa:
Número da Ocorrência, Tarefa (o "(Não Modificar) Tarefa" do relatório do Dynamics), Etapa, Término Real, Indicador
("Todos os SLAs"), Data Expurgo, Mês de Expurgo, Incidente, Motivo e Aprovado por. A chave é a tarefa e não a
ocorrência, porque uma ocorrência tem tarefas de Fase 1 e de Fase 2 e só algumas são expurgadas.

As tarefas da aba saem de **todos os SLAs**: SLA Experiência, SLA Cliente e SLA 5 Horas passam a ser **"EXPURGADO"**.
Continuam contando nos volumes (encerrados, tops), mas não como dentro nem como fora do prazo. A regra está na gold
(`src/gold/dynamics_e_resenhas.py`) e nas etapas "Expurgo SLA" do fluxo no Prep (`ferramentas/adicionar_expurgo_sla_prep.py`).

No workbook, os percentuais dentro ÷ (dentro + fora) já ignoram o EXPURGADO, e as planilhas de SLA Cliente já filtravam
só DENTRO DO PRAZO / FORA DO PRAZO. As planilhas que mostram a fatia de cada valor sobre o total de registros (SLA EXP do
CB, do CF e do Consolidado, e SLA 5h do Consolidado) ganharam esse mesmo filtro; sem ele o EXPURGADO aparece como uma
fatia e reduz o percentual dentro do prazo (`ferramentas/melhorias_tableau.py`, filtro_sla_expurgado).

Primeiro caso: 94 tarefas do SEV 1 [INC1203571] Captação de Pedidos, pedido da Suelen com aprovação da Valéria em
27/10/2026. Com o cálculo do painel (horas úteis), 76 delas estavam fora do prazo de 24h e 18 dentro; a lista aprovada
foi aplicada inteira.
