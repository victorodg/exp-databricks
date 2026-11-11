# Validação – Hispana

Comparação das 9 tabelas gold com os extracts publicados no Tableau Cloud (atualizados em 30/10/2026 por volta de 09:20
de Brasília). As Google Sheets da gold foram exportadas no mesmo dia, às 14:45. Ferramentas: `ferramentas/comparar_hispana.sh`
(roda `comparar_extract.py` para as 9 saídas). Gabarito em `validacao\extracts_hispana\`.

## Resultado

| Gold (`dexp_gold_hispana_*`) | Extract | Linhas extract | Linhas gold |
|---|---|---|---|
| `resenhas` | Resenhas OIS | 443.362 | 443.362 |
| `base_mkt` | Base MKT OIS | 254.072 | 254.072 |
| `produtividade` | Experiencia Hispana Produtividade | 245.702 | 245.705 |
| `completo` | MKT Hispana Completo | 42.441 | 42.441 |
| `chamados_servicenow` | Experiencia Hispana - Chamados Servicenow | 31.222 | 31.222 |
| `base_mkt_hc` | Base MKT HC OIS | 5.513 | 5.513 |
| `appsheets_resenhas` | AppSheets Resenhas OIs | 2.611 | 2.614 |
| `base_mkt_lojas` | Base MKT Lojas OIS | 935 | 935 |
| `ticket_medio` | Ticket Medio Hispana | 147 | 147 |

## Diferenças que sobraram

- **3 linhas a mais em AppSheets e Produtividade:** a planilha `Resenhas OIs` foi exportada às 14:45, depois do extract
  (a resposta mais recente na gold é de 30/10 às 12:35). Produtividade herda essas 3 linhas.
- **`Encerrado em` em 7 linhas:** na `BASE MTK Historico` essas células são números de série do Excel (45980,93), sem
  formato de data. O Prep lê só o dia e perde o horário, e o SLA dessas linhas pode sair errado; a gold mantém o horário.
  **Decisão (30/10/2026): manter o valor correto na gold**, diferente do Prep.
- **`Tempo de Operação - Segundos`:** 39 linhas preenchidas só na gold, em que o Prep não converteu o texto. A causa
  esperada é a mesma das durações de 24 horas ou mais do fluxo MKT, mas não foi conferida linha a linha.
- **`Status SLA Email`:** depende de `NOW()` nos e-mails abertos, então muda com a hora da execução. Na Base MKT, a gold
  tem 7 "Fora do SLA" a mais, e nas Lojas e no HC a diferença é de 1 linha.
- **Textos** (`Código CN`, `Código da Gerente`, `GV`, tempos em texto, descrições): o Prep lê o formato de exibição do
  Excel e guarda uma grafia só para textos iguais sem diferenciar maiúsculas. Não entram em indicador.
- **F12 e F13** do Registro de Grupos: colunas sem cabeçalho, não levadas para a gold. Nas views entram como NULL.

## Painel

Conferido pelo usuário em 30/10/2026 na cópia ligada às fontes `dexp - …`, sem avisos. No painel Llamados MKT, as visões de
Healthcheck ficam vazias com o filtro em outubro de 2026: não há atendimento de Healthcheck nesse mês, nem no extract de
produção nem na gold. Os dois têm os mesmos totais por mês (setembro/2026: 19 linhas).

## Comportamentos do Prep reproduzidos

- **`Pais` depois do join [92]:** é o da planilha Ticket Medio por Pais, não o da linha. País sem correspondência fica nulo.
- **Fonte:** o Prep deriva de `Table Names`; a gold usa um valor fixo por ramo (MKT Zap, Registro de Grupos, Tickets).
- **Responsável vazio:** vira "Vacio" na Base MKT OIS.
- **Colunas repetidas na BASE MTK:** "Função do Sistema" e "Status de Classificação" aparecem duas vezes com o mesmo
  título; a segunda é a "1" do Prep. "Status de Finalização" (sistema) e "Status de finalização" (atendimento) são colunas diferentes.
- **Horário útil:** 8h às 3h do dia seguinte (19 horas), diferente do Brasil. Os limites ficam nas fórmulas da gold.

## Correção do status dos tickets de e-mail (04/11/2026)

Na etapa [85] "Emails para Retenção" o Prep removia `Status de finalização` e renomeava `Status` (o do relatório
Completo) para esse nome. Os tickets de e-mail (T-…) não têm `Status`, então ficavam com status nulo no painel, mesmo
com o status preenchido no relatório de Tickets. A correção foi feita igual nos dois lados:

- **Prep** (`Daily Experiencia OIS`, publicado no projeto EXPERIÊNCIA HISPANA / ANDINO / 4. DATASOURCES):
  `Status de finalização novo = IFNULL([Status], [Status de finalização])`, depois remove `Status de finalização` e
  `Status` e renomeia o novo campo.
- **Gold** (`src/gold/hispana.py`, bloco [85]): `status = coalesce(status, status_de_finalizacao)` antes da remoção.

Efeito medido em `dexp_gold_hispana_completo` (concluídos, sem Latam e sem WhatsApp, as mesmas 60 linhas nulas da
Base MKT OIS publicada em 04/11):

| Mês | Linhas | Status que passam a ter |
|---|---|---|
| 03/2026 | 21 atendimentos | o do analítico (ex.: EXPCN, DIRECCIONADO - ATENCION, LLAMADO ABIERTO PARA N2) |
| 04/2026 | 3 atendimentos | o do analítico (EXPCN) |
| 06 a 10/2026 | 36 tickets de e-mail (19, 3, 6, 2, 6) | o do próprio ticket |

Os atendimentos com `Status` preenchido no Completo não mudam.

## Casos de acompanhamento sem Função do Sistema (decidido em 04/11/2026)

Os "Resuelto N2/N3" (classificações "EN ACOMPAÑAMIENTO TD" e "Pendientes – JIRA", nível Neutro) vêm do Completo sem
Função do Sistema e são usados no TMO (outubro/2026: 172 linhas). No painel consolidado (Experiência Hispana - Daily) o
gráfico "Funcion del Sistema - General" já os exclui por filtro de `Status de Classificação`; nos painéis Andino, Sur e
México não há esse filtro e eles aparecem como Função nula.

Decisão: os três painéis regionais recebem o mesmo filtro do consolidado. O filtro tira do gráfico todas as linhas com
essas classificações, não só as sem função (outubro/2026: 916 linhas, 172 sem função e 744 com função). A gold não muda,
porque o TMO precisa dessas linhas. As cópias ligadas às fontes `dexp - …` são geradas a partir do workbook publicado
(`ferramentas/ligar_hispana_tableau.py`), então herdam o filtro quando forem geradas de novo.

## Colunas novas do MKT Hispana Completo (05/11/2026)

O MKT Hispana Completo ganhou `Qtde Msg Automático`, `Qtde Msg Operador` e `Qtde Msg Recebidas`, e o Prep as repassa para
Base MKT OIS, Base MKT HC OIS, Base MKT Lojas OIS e MKT Hispana Completo. As golds já as tinham (a silver do Completo
leva todas as colunas da planilha); faltavam nas views, geradas dos extracts de 30/10. Os extracts dessas quatro saídas
em `validacao\extracts_hispana\` foram trocados pelos de produção de 05/11 (os anteriores estão em
`anteriores_20261030\`) e as views foram regeneradas com `gerar_views_tableau.py --aplicar`. Os painéis México, Andino e
Sur usam esses campos.

