# Databricks notebook source
# MAGIC %md
# MAGIC # Gold – CSAT
# MAGIC
# MAGIC Reproduz o fluxo Tableau Prep **"GovEXP - Metricas de Excelencia - CSAT"**, com uma saída: `dexp_gold_csat_enquetes`
# MAGIC (extract **Enquetes C-SAT**). Os números entre colchetes, como `[22]`, são as etapas de `docs/fluxos/csat.md`.
# MAGIC
# MAGIC Cada enquete aparece uma vez por fatia do Modelo Gauge, porque o painel desenha os medidores com esse cruzamento.

# COMMAND ----------

import os
import sys

from pyspark.sql import functions as F

sys.path.append(os.path.abspath(".."))
from dexp import regras_csat as R
from dexp import tableau as tb
from dexp.prep import juntar, remover, uniao
from dexp.tableau import excluir, igual, remapear

dbutils.widgets.text("catalog", "sandbox")
dbutils.widgets.text("schema", "sustentacao_bau_experiencias")
CATALOGO = dbutils.widgets.get("catalog")
SCHEMA = dbutils.widgets.get("schema")
tb.preparar_sessao(spark)


def silver(tabela):
    return spark.table(f"{CATALOGO}.{SCHEMA}.dexp_silver_{tabela}").drop("_versao", "_origem")


def com_prefixo(df, prefixo, chave="protocolo"):
    return df.select(chave, *[F.col(c).alias(f"{prefixo}_{c}") for c in df.columns if c != chave])

# COMMAND ----------

# MAGIC %md ## Enquetes – [1] [3] [5] [7] [12] [18] [20] [22]

# COMMAND ----------

COLUNAS_ENQUETE = ["data_do_contato", "enviado_em", "respondido_em", "protocolo", "nome", "canal", "contato", "responsavel", "nota"]

# [12] [18] A planilha do NCC tem protocolos repetidos: fica uma linha por protocolo, com o menor valor de cada coluna
ncc = silver("csat_enquete_ncc").select(*COLUNAS_ENQUETE).where(excluir("protocolo", "1990-1509513108473"))
ncc = ncc.groupBy("protocolo").agg(
    tb.minimo_texto("canal").alias("canal"), tb.minimo_texto("contato").alias("contato"), F.min("data_do_contato").alias("data_do_contato"),
    F.min("enviado_em").alias("enviado_em"), tb.minimo_texto("nome").alias("nome"), tb.minimo_texto("nota").alias("nota"),
    tb.minimo_texto("respondido_em").alias("respondido_em"), tb.minimo_texto("responsavel").alias("responsavel"))

# [20]
enquetes = uniao(
    silver("csat_enquete_ces").select(*COLUNAS_ENQUETE).withColumn("fonte", F.lit("CES")),
    silver("csat_enquete_brasil").select(*COLUNAS_ENQUETE).withColumn("fonte", F.lit("Experiencia Brasil")),
    ncc.withColumn("fonte", F.lit("NCC")),
    silver("csat_enquete_hispana").select(*COLUNAS_ENQUETE).withColumn("fonte", F.lit("Hispana")),
).withColumn("data", F.col("enviado_em"))

# [22]
primeiro = F.substring(F.trim(F.col("nota")), 1, 1)
enquetes = (
    enquetes
    .withColumn("nota", remapear("nota", R.NOTA_CSAT))
    .withColumn("respondido_em", remapear("respondido_em", {"Não respondido": ["NÃ£o respondido"]}))
    .withColumn("c_sat", F.when(primeiro.isin("5", "4"), "PROMOTOR").when(primeiro == "3", "NEUTRO")
                          .when(primeiro.isin("2", "1"), "DETRATOR").otherwise("Não respondido"))
    .withColumn("enquete_respondida", F.when(F.col("c_sat") == "Não respondido", 0).otherwise(1).cast("bigint"))
    .withColumn("respondido_em", F.when(igual("respondido_em", "Não respondido"), F.lit(None).cast("string")).otherwise(F.col("respondido_em")))
    # O Prep lê essa coluna como texto no formato de exibição do Excel (1/1/2025 18:54)
    .withColumn("respondido_em", F.coalesce(F.date_format(tb.data_hora("respondido_em"), "M/d/yyyy H:mm"), F.col("respondido_em")))
    .withColumn("responsavel", remapear("responsavel", R.RESPONSAVEL_ENQUETE))
)

# COMMAND ----------

# MAGIC %md ## Dados do atendimento por operação – [11] [17] [23] [24] [2] [4] [8] [14] [19] [21] [25] [9] [15] [26]

# COMMAND ----------

# [17] [23] [24] Brasil
exp_br = (
    silver("mkt_reativos")
    .select("protocolo", "gv", "funcao", "chamado", "qtd_atendimentos", "funcao_do_sistema", "mercado", "primeiro_tempo_de_espera",
            "setor_fim", "status_de_classificacao", "status_de_finalizacao")
    .withColumn("mercado", remapear("mercado", {"ARAUCÁRIA": ["ARAUCARIA"]}))
)
base = remover(juntar(enquetes, com_prefixo(exp_br, "exp_br"), [("protocolo", "protocolo")], "left"), "protocolo_1")


# [14] [19] [21] [25] Hispana. A função e a classificação aparecem duas vezes na BASE MTK; a segunda é a "1" do Prep.
def base_mtk(tabela):
    return (silver(tabela)
            .withColumnRenamed("status_de_finalizacao", "status_de_finalizacao_sistema")
            .withColumnRenamed("status_de_finalizacao_2", "status_de_finalizacao")
            .withColumnRenamed("funcao_do_sistema_2", "funcao_do_sistema_1")
            .withColumnRenamed("status_de_classificacao_2", "status_de_classificacao_1"))


pais_por_setor = F.create_map(*[F.lit(v) for par in {k.lower(): r for k, r in R.PAIS_POR_SETOR.items()}.items() for v in par])
ois = (
    uniao(base_mtk("hispana_base_mtk_historico"), base_mtk("hispana_base_mtk"), silver("hispana_analitico"))
    .withColumn("funcao_do_sistema", F.coalesce("funcao_do_sistema", "funcao_do_sistema_1"))
    .select("protocolo", "sistema", "funcao_do_sistema", "detalhe_do_sistema", "solucao_aplicada", "tempo_ate_ser_atendido",
            "tempo_do_atendimento", "primeiro_tempo_de_espera", "tempo_medio_de_espera", "tempo_de_operacao", "canal_de_entrada",
            "setor_entrada", "setor_fim", F.col("status_de_classificacao_1").alias("status_de_classificacao"), "status_de_finalizacao",
            "observacoes")
    .withColumn("pais", F.try_element_at(pais_por_setor, F.lower(F.col("setor_fim"))))
)
ois = com_prefixo(ois, "ois").withColumnRenamed("ois_pais", "pais")
base = remover(juntar(base, ois, [("protocolo", "protocolo")], "left"), "protocolo_1")

# [15] [26] NCC
ncc_atendimento = silver("csat_base_malasia").select(
    "protocolo", F.col("function").alias("ncc_function"), F.col("solution_applied").alias("ncc_solution_applied"),
    F.col("canal_de_entrada").alias("ncc_canal_de_entrada"), F.col("setor_entrada").alias("ncc_setor_entrada"),
    F.col("setor_fim").alias("ncc_setor_fim"), F.col("status_de_classificacao").alias("ncc_status_de_classificacao"),
    F.col("status_de_finalizacao").alias("ncc_status_de_finalizacao"))
base = remover(juntar(base, ncc_atendimento, [("protocolo", "protocolo")], "left"), "protocolo_1")

# COMMAND ----------

# MAGIC %md ## Analistas, notas e medidores – [27] a [33]

# COMMAND ----------

# [27] [13] [28] Só entram as enquetes dos analistas da lista
base = (
    base
    .withColumn("responsavel", remapear("responsavel", R.RESPONSAVEL_CONSOLIDADO))
    .where(excluir("ncc_status_de_finalizacao", "Teste NCC"))
    .withColumn("responsavel", remapear("responsavel", R.RESPONSAVEL_FINAL))
)
base = juntar(base, silver("csat_analistas").drop("coluna_1"), [("responsavel", "analista_para_considerar_nas_enquetes")], "inner")

# [29] [30]
c_sat = F.col("c_sat")
solucao = F.col("ois_solucao_aplicada")
nota = F.col("nota")
base = (
    base
    .withColumn("exp_br_qtd_atendimentos", F.coalesce("exp_br_qtd_atendimentos", F.lit(1)))
    .withColumn("ois_solucao_aplicada", F.when(solucao.isNull() | (solucao == 6256), 1).otherwise(solucao))
    .withColumn("nota_csat", F.when(c_sat == "PROMOTOR", 1).otherwise(0).cast("bigint"))
    .withColumn("nota_csat_simple", F.when(c_sat.isin("NEUTRO", "PROMOTOR"), 1).otherwise(0).cast("bigint"))
    .withColumn("nota", remapear("nota", R.NOTA_CES))
)
nota = F.col("nota")
base = (
    base
    .withColumn("nota_ces", F.when(igual(nota, "1 - Muito Difícil"), 1).when(igual(nota, "2 - Difícil"), 2)
                             .when(igual(nota, "3 - Neutro | Razoável"), 3).when(igual(nota, "4 - Fácil"), 4)
                             .when(igual(nota, "5 - Muito Fácil"), 5).cast("bigint"))
    .withColumn("chave_join", F.lit(1).cast("bigint"))
    .withColumn("nota_da_csat", F.col("nota_csat"))
    .withColumn("nota_da_csat_simple", F.col("nota_csat_simple"))
)

# [10] [16] [31] Uma linha por fatia do medidor
gauge = (silver("csat_modelo_gauge").withColumnRenamed("slice", "slice_numero").withColumnRenamed("slice_2", "slice")
         .withColumn("slice_numero", tb.inteiro("slice_numero")).withColumn("chave_join", F.lit(1).cast("bigint")))
base = juntar(gauge, base, [("chave_join", "chave_join")], "inner")

# [32] [33]
hora = F.col("time")
mercado = F.col("exp_br_mercado")
mercado_maiusculo = F.upper(mercado)
base = (
    base
    .withColumn("turno", F.when(igual(hora, "NCC - Turno A Dia", "NCC - Turno A Noite", "NCC - Turno B Dia", "NCC - Turno B Noite"), hora))
    .withColumn("time", remapear("time", {"IM": ["NCC - Turno B Noite", "NCC - Turno A Dia", "NCC - Turno A Noite", "NCC - Turno B Dia"]}))
    .withColumn("exp_br_mercado",
                F.when(F.upper(F.trim(mercado)) == "AT", "ATLÂNTICA").when(F.upper(F.trim(mercado)) == "AM", "AMAZÔNIA")
                 .when(mercado_maiusculo.contains("AMA"), "AMAZÔNIA").when(mercado_maiusculo.contains("ARA"), "ARAUCÁRIA")
                 .when(mercado_maiusculo.contains("ATL"), "ATLÂNTICA").when(mercado_maiusculo.contains("CAA"), "CAATINGA")
                 .when(mercado_maiusculo.contains("CER"), "CERRADO").otherwise(mercado))
)

nome = f"{CATALOGO}.{SCHEMA}.dexp_gold_csat_enquetes"
base.write.mode("overwrite").option("overwriteSchema", "true").saveAsTable(nome)
spark.sql(f"COMMENT ON TABLE {nome} IS 'Gold GovEXP: enquetes de satisfação por analista, com uma linha por fatia do medidor (extract Enquetes C-SAT)'")
print(f"dexp_gold_csat_enquetes {spark.table(nome).count():>9,} linhas")

# COMMAND ----------

# MAGIC %md ## Saídas do painel em Apps Script (`logic-local/csat`)
# MAGIC
# MAGIC Uma linha por enquete e os indicadores por operação e mês, contando protocolos distintos. As regras estão em
# MAGIC `src/dexp/csat_saidas.py` e em `csat/README.md`.

# COMMAND ----------

from dexp.csat_saidas import SQL_DETALHE, SQL_MENSAL

SAIDAS = {
    "dexp_gold_csat_detalhe": (SQL_DETALHE, "Gold CSAT: uma linha por enquete (sem as fatias do medidor), para o painel em Apps Script"),
    "dexp_gold_csat_mensal": (SQL_MENSAL, "Gold CSAT: indicadores por operação e mês, por protocolo distinto"),
}
for tabela, (consulta, comentario) in SAIDAS.items():
    destino = f"{CATALOGO}.{SCHEMA}.{tabela}"
    spark.sql(consulta.format(enquetes=nome)).write.mode("overwrite").option("overwriteSchema", "true").saveAsTable(destino)
    spark.sql(f"COMMENT ON TABLE {destino} IS '{comentario}'")
    print(f"{tabela} {spark.table(destino).count():>9,} linhas")
