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
