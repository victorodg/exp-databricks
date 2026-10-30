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
