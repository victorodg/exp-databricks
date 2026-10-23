# Databricks notebook source
# MAGIC %md
# MAGIC # Bronze – Daily Experiência BR
# MAGIC
# MAGIC Lê os arquivos mais recentes do volume `dexp_landing` e grava uma tabela Delta por fonte (`dexp_bronze_<tabela>`):
# MAGIC
# MAGIC - **Planilhas (drive / google_sheets):** a versão mais recente (última pasta `AAAA-MM-DD`) substitui a tabela inteira,
# MAGIC   como o Tableau Prep faz ao ler a planilha. As versões antigas continuam no volume.
# MAGIC - **MKTZap:** cada bruto traz o mês inteiro até a data da coleta, então a tabela junta o bruto mais recente de cada mês.
# MAGIC
# MAGIC Todas as colunas ficam como texto, do jeito que estavam no arquivo. Os nomes de coluna viram snake_case sem acento,
# MAGIC e o nome original fica em `dexp_bronze_colunas`. Colunas de controle: `_linha` (linha no arquivo), `_arquivo`,
# MAGIC `_versao` e `_carregado_em`. Uma tabela só é regravada quando o arquivo de origem muda (ou com `forcar = sim`).

# COMMAND ----------

# MAGIC %pip install python-calamine==0.9.0 --quiet

# COMMAND ----------

import os
import re
import sys
import traceback

import pandas as pd
from pyspark.sql import functions as F
from pyspark.sql.types import LongType, StringType, StructField, StructType

sys.path.append(os.path.abspath(".."))  # pasta src/ do bundle
from dexp.fontes import FONTES_EXCEL, FONTES_MKTZAP
from dexp.leitura import ler_csv_mktzap, ler_excel, normalizar_colunas

dbutils.widgets.text("catalog", "sandbox")
dbutils.widgets.text("schema", "sustentacao_bau_experiencias")
dbutils.widgets.dropdown("forcar", "nao", ["nao", "sim"])
CATALOGO = dbutils.widgets.get("catalog")
SCHEMA = dbutils.widgets.get("schema")
FORCAR = dbutils.widgets.get("forcar") == "sim"
VOLUME = f"/Volumes/{CATALOGO}/{SCHEMA}/dexp_landing"
TABELA_COLUNAS = f"{CATALOGO}.{SCHEMA}.dexp_bronze_colunas"


def nome_tabela(tabela):
    return f"{CATALOGO}.{SCHEMA}.dexp_bronze_{tabela}"

# COMMAND ----------

# MAGIC %md ## Arquivo a carregar por fonte

# COMMAND ----------

def versao_mais_recente(grupo, fonte):
    """(caminho, versão) do arquivo na última pasta AAAA-MM-DD da fonte, ou None se a fonte ainda não chegou."""
    pasta = f"{VOLUME}/{grupo}/{fonte}"
    if not os.path.isdir(pasta):
        return None
    versoes = sorted(d for d in os.listdir(pasta) if re.fullmatch(r"\d{4}-\d{2}-\d{2}", d))
    if not versoes:
        return None
    arquivos = sorted(os.listdir(f"{pasta}/{versoes[-1]}"))
    if len(arquivos) != 1:
        raise ValueError(f"{pasta}/{versoes[-1]}: esperava 1 arquivo, há {len(arquivos)}: {arquivos}")
    return f"{pasta}/{versoes[-1]}/{arquivos[0]}", versoes[-1]


def brutos_por_mes(operacao, relatorio):
    """[(caminho, versão)] com o bruto de maior data final de cada mês (bruto_<relatório>_<de>_a_<até>.csv)."""
    pasta = f"{VOLUME}/mktzap/{operacao}"
    if not os.path.isdir(pasta):
        return []
    padrao = re.compile(rf"bruto_{relatorio}_(\d{{8}})_a_(\d{{8}})\.csv")
    escolhidos = []
    for mes in sorted(os.listdir(pasta)):
        candidatos = [(m.group(2), nome) for nome in os.listdir(f"{pasta}/{mes}") if (m := padrao.fullmatch(nome))]
        if candidatos:
            ate, nome = max(candidatos)
            escolhidos.append((f"{pasta}/{mes}/{nome}", f"{ate[:4]}-{ate[4:6]}-{ate[6:]}"))
    return escolhidos


def arquivos_carregados(tabela):
    if not spark.catalog.tableExists(nome_tabela(tabela)):
        return set()
    return {r["_arquivo"] for r in spark.table(nome_tabela(tabela)).select("_arquivo").distinct().collect()}

# COMMAND ----------

# MAGIC %md ## Gravação

# COMMAND ----------

def para_pandas(tabela_texto, arquivo, versao):
    colunas = normalizar_colunas(tabela_texto.colunas_originais)
    pdf = pd.DataFrame(tabela_texto.linhas, columns=colunas, dtype="object")
    pdf["_linha"] = tabela_texto.numeros_linha
    pdf["_arquivo"] = arquivo
    pdf["_versao"] = versao
    mapa = pd.DataFrame({"coluna": colunas, "coluna_original": tabela_texto.colunas_originais})
    return pdf, mapa


def gravar(tabela, partes, descricao):
    """partes: [(pandas, mapa de colunas)] de um ou mais arquivos; colunas que faltam em algum arquivo ficam nulas."""
    pdf = pd.concat([p for p, _ in partes], ignore_index=True)
    pdf = pdf.astype(object).where(pdf.notna(), None)
    colunas_dados = [c for c in pdf.columns if not c.startswith("_")]
    pdf = pdf[colunas_dados + ["_linha", "_arquivo", "_versao"]]
    esquema = StructType([StructField(c, StringType()) for c in colunas_dados]
                         + [StructField("_linha", LongType()), StructField("_arquivo", StringType()),
                            StructField("_versao", StringType())])
    df = spark.createDataFrame(pdf, esquema).withColumn("_carregado_em", F.current_timestamp())
    df.write.mode("overwrite").option("overwriteSchema", "true").saveAsTable(nome_tabela(tabela))
    spark.sql(f"COMMENT ON TABLE {nome_tabela(tabela)} IS '{descricao}. Colunas como texto; nomes originais em dexp_bronze_colunas.'")

    mapa = pd.concat([m for _, m in partes]).drop_duplicates("coluna")
    mapa = mapa.assign(tabela=f"dexp_bronze_{tabela}", posicao=range(1, len(mapa) + 1))
    df_mapa = spark.createDataFrame(mapa[["tabela", "posicao", "coluna", "coluna_original"]].astype({"posicao": "int64"}))
    if spark.catalog.tableExists(TABELA_COLUNAS):
        df_mapa.write.mode("overwrite").option("replaceWhere", f"tabela = 'dexp_bronze_{tabela}'").saveAsTable(TABELA_COLUNAS)
    else:
        df_mapa.write.saveAsTable(TABELA_COLUNAS)
    return len(pdf)

# COMMAND ----------

# MAGIC %md ## Carga

# COMMAND ----------

resultados = []


def registrar(tabela, situacao, detalhe="", linhas=None):
    resultados.append({"tabela": f"dexp_bronze_{tabela}", "situacao": situacao, "linhas": linhas, "detalhe": detalhe})
    print(f"{situacao:12} dexp_bronze_{tabela:38} {'' if linhas is None else f'{linhas:,} linhas  '}{detalhe}")


for f in FONTES_EXCEL:
    try:
        achado = versao_mais_recente(f.grupo, f.fonte)
        if achado is None:
            registrar(f.tabela, "ausente", f"nada em {f.grupo}/{f.fonte}")
            continue
        arquivo, versao = achado
        if not FORCAR and arquivos_carregados(f.tabela) == {arquivo}:
            registrar(f.tabela, "sem mudança", versao)
            continue
        tabela_texto = ler_excel(arquivo, f.aba, f.linha_cabecalho)
        descricao = f"Bronze Daily Experiência BR: {f.grupo}/{f.fonte}, aba {f.aba or '(primeira visível)'}"
        linhas = gravar(f.tabela, [para_pandas(tabela_texto, arquivo, versao)], descricao)
        registrar(f.tabela, "carregada", versao, linhas)
    except Exception as e:
        registrar(f.tabela, "erro", f"{type(e).__name__}: {e}")
        traceback.print_exc()

for f in FONTES_MKTZAP:
    try:
        escolhidos = brutos_por_mes(f.operacao, f.relatorio)
        if not escolhidos:
            registrar(f.tabela, "ausente", f"nada em mktzap/{f.operacao}")
            continue
        if not FORCAR and arquivos_carregados(f.tabela) == {a for a, _ in escolhidos}:
            registrar(f.tabela, "sem mudança", escolhidos[-1][1])
            continue
        partes = [para_pandas(ler_csv_mktzap(a), a, v) for a, v in escolhidos]
        descricao = f"Bronze Daily Experiência BR: MKTZap {f.operacao} {f.relatorio}, bruto mais recente de cada mês"
        linhas = gravar(f.tabela, partes, descricao)
        registrar(f.tabela, "carregada", f"{len(escolhidos)} mês(es), até {escolhidos[-1][1]}", linhas)
    except Exception as e:
        registrar(f.tabela, "erro", f"{type(e).__name__}: {e}")
        traceback.print_exc()

# COMMAND ----------

resumo = pd.DataFrame(resultados)
display(resumo)
erros = resumo[resumo["situacao"] == "erro"]
if len(erros):
    raise RuntimeError(f"{len(erros)} tabela(s) com erro: {', '.join(erros['tabela'])}")
