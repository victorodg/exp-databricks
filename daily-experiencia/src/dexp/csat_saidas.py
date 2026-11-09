"""Saídas do CSAT para o painel em Apps Script (`logic-local/csat`).

As duas consultas leem `dexp_gold_csat_enquetes` (passado em `{enquetes}`) e são usadas em dois lugares:
- `src/gold/csat.py` grava `dexp_gold_csat_detalhe` e `dexp_gold_csat_mensal` com elas;
- `ferramentas/validar_csat_mensal.py` roda `SQL_MENSAL` no SQL Warehouse para comparar com o extract do Tableau.

Regras (decididas em 09/11/2026, ver `csat/README.md`):
- Uma linha por enquete: só a fatia 1 do Modelo Gauge, que no Tableau só serve para desenhar os medidores.
- Todas as contagens são por protocolo distinto, inclusive as que no Tableau contavam linhas (Brasil e Hispana).
- C-SAT = promotores ÷ respondidas; C-SAT Simple = (promotores + neutros) ÷ respondidas;
  Response Rate = respondidas ÷ enviadas. Os medidores do Tableau usam o mesmo numerador e denominador.
- CES: respostas = protocolos com nota de 1 a 5; média = média das notas. No Tableau o total do gráfico mensal saía 5×
  maior porque o gráfico não filtrava a fatia.
- Ofensores: Brasil e CES pela função do sistema do MKT Reativos, Hispana pela função do sistema da BASE MTK e NCC pelo
  status de classificação da BASE MALASIA. No Tableau o NCC usava o status de finalização.
"""

MERCADOS = ("CAATINGA", "AMAZÔNIA", "ARAUCÁRIA", "ATLÂNTICA", "CERRADO")


def _por_fonte(brasil, hispana, ncc):
    """Coluna que muda conforme a operação (None = não existe nela). CES usa as colunas do Brasil, como o painel CES."""
    return f"CASE fonte WHEN 'Hispana' THEN {hispana or 'NULL'} WHEN 'NCC' THEN {ncc or 'NULL'} ELSE {brasil or 'NULL'} END"


SQL_DETALHE = f"""
SELECT
  fonte,
  protocolo,
  date_format(data, 'yyyy-MM') AS mes,
  date_format(data, 'yyyy-MM-dd') AS dia,
  date_format(enviado_em, 'yyyy-MM-dd HH:mm') AS enviado_em,
  respondido_em,
  c_sat,
  nota,
  nota_ces,
  responsavel,
  time,
  turno,
  canal,
  CASE WHEN exp_br_mercado IN ({", ".join(f"'{m}'" for m in MERCADOS)}) THEN exp_br_mercado END AS mercado,
  pais,
  {_por_fonte("exp_br_setor_fim", "ois_setor_fim", "ncc_setor_fim")} AS setor_fim,
  {_por_fonte(None, "ois_canal_de_entrada", "ncc_canal_de_entrada")} AS canal_de_entrada,
  {_por_fonte("exp_br_funcao_do_sistema", "ois_funcao_do_sistema", "ncc_function")} AS funcao_do_sistema,
  {_por_fonte("exp_br_status_de_classificacao", "ois_status_de_classificacao", "ncc_status_de_classificacao")}
    AS status_de_classificacao,
  {_por_fonte("exp_br_status_de_finalizacao", "ois_status_de_finalizacao", "ncc_status_de_finalizacao")}
    AS status_de_finalizacao,
  {_por_fonte("exp_br_funcao_do_sistema", "ois_funcao_do_sistema", "ncc_status_de_classificacao")} AS ofensor,
  {_por_fonte("exp_br_primeiro_tempo_de_espera", "ois_primeiro_tempo_de_espera", None)} AS primeiro_tempo_de_espera,
  ois_tempo_ate_ser_atendido AS tempo_ate_ser_atendido,
  ois_tempo_do_atendimento AS tempo_do_atendimento,
  ois_tempo_medio_de_espera AS tempo_medio_de_espera,
  ois_tempo_de_operacao AS tempo_de_operacao,
  {_por_fonte(None, "CAST(ois_solucao_aplicada AS STRING)", "ncc_solution_applied")} AS solucao_aplicada,
  ncc_setor_entrada AS setor_entrada,
  exp_br_chamado AS chamado,
  exp_br_funcao AS funcao,
  nome
FROM {{enquetes}}
WHERE slice_numero = 1
"""


def _distintos(condicao):
    return f"count(DISTINCT CASE WHEN {condicao} THEN protocolo END)"


SQL_MENSAL = f"""
WITH base AS (
  SELECT
    fonte,
    date_format(data, 'yyyy-MM') AS mes,
    count(DISTINCT protocolo) AS enviadas,
    {_distintos("c_sat <> 'Não respondido'")} AS respondidas,
    {_distintos("c_sat = 'Não respondido'")} AS sem_resposta,
    {_distintos("c_sat = 'PROMOTOR'")} AS promotores,
    {_distintos("c_sat = 'NEUTRO'")} AS neutros,
    {_distintos("c_sat = 'DETRATOR'")} AS detratores,
    {_distintos("c_sat IN ('PROMOTOR', 'NEUTRO')")} AS promotores_e_neutros,
    {_distintos("nota_ces IS NOT NULL")} AS ces_respostas,
    avg(nota_ces) AS ces_media
  FROM {{enquetes}}
  WHERE slice_numero = 1
  GROUP BY fonte, date_format(data, 'yyyy-MM')
)
SELECT
  fonte, mes, enviadas, respondidas, sem_resposta, promotores, neutros, detratores,
  try_divide(promotores, respondidas) AS csat,
  try_divide(promotores_e_neutros, respondidas) AS csat_simple,
  try_divide(respondidas, enviadas) AS response_rate,
  ces_respostas,
  ces_media
FROM base
"""
