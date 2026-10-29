# Databricks notebook source
# MAGIC %md
# MAGIC # Silver – Daily Experiência BR
# MAGIC
# MAGIC Cada tabela `dexp_silver_<tabela>` é uma ou mais tabelas bronze com colunas renomeadas e tipadas
# MAGIC (definições em `src/dexp/silver.py`). Datas e horários são gravados sem fuso, como estão nas planilhas.
# MAGIC Nenhuma regra de negócio é aplicada aqui: as regras do Tableau Prep ficam na gold.

# COMMAND ----------

import os
import sys

from pyspark.sql import functions as F

sys.path.append(os.path.abspath(".."))
from dexp import tableau as tb
from dexp.silver import OPCIONAIS, TABELAS, MesmasColunas, tipar

dbutils.widgets.text("catalog", "sandbox")
dbutils.widgets.text("schema", "sustentacao_bau_experiencias")
CATALOGO = dbutils.widgets.get("catalog")
SCHEMA = dbutils.widgets.get("schema")
tb.preparar_sessao(spark)

# COMMAND ----------

resumo = []
for tabela, (bronzes, definicao) in TABELAS.items():
    destino = f"{CATALOGO}.{SCHEMA}.dexp_silver_{tabela}"
    if tabela in OPCIONAIS and not all(spark.catalog.tableExists(f"{CATALOGO}.{SCHEMA}.dexp_bronze_{b}") for b in bronzes):
        spark.sql(f"DROP TABLE IF EXISTS {destino}")
        print(f"dexp_silver_{tabela:32}  ausente (bronze opcional não existe)")
        continue
    partes = []
    for bronze in bronzes:
        df = spark.table(f"{CATALOGO}.{SCHEMA}.dexp_bronze_{bronze}")
        colunas = definicao.colunas(df.columns) if isinstance(definicao, MesmasColunas) else definicao
        faltando = [b for _, b, _ in colunas if b not in df.columns]
        if faltando:
            raise ValueError(f"dexp_bronze_{bronze}: colunas esperadas não encontradas: {faltando}")
        partes.append(tipar(df, colunas).withColumn("_origem", F.lit(f"dexp_bronze_{bronze}")))
    df = partes[0]
    for p in partes[1:]:
        df = df.unionByName(p)
    df.write.mode("overwrite").option("overwriteSchema", "true").saveAsTable(destino)
    resumo.append((f"dexp_silver_{tabela}", spark.table(destino).count()))
    print(f"dexp_silver_{tabela:32} {resumo[-1][1]:>9,} linhas")
