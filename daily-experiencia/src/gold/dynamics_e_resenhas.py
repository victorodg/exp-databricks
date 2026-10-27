# Databricks notebook source
# MAGIC %md
# MAGIC # Gold – Dynamics e Resenhas
# MAGIC
# MAGIC Reproduz o fluxo Tableau Prep **"Daily Experiencia BR - Dynamics e Resenhas"**. Os números entre colchetes, como
# MAGIC `[52]`, são as etapas de `docs/fluxos/dynamics_e_resenhas.md`.
# MAGIC
# MAGIC | Tabela gold | Extract atual no Tableau Cloud |
# MAGIC |---|---|
# MAGIC | `dexp_gold_dynamics_tarefas` | Dynamics - Termino Real |
# MAGIC | `dexp_gold_dynamics_nivel` | Dynamics Nivel (entrada do fluxo MKT) |
# MAGIC | `dexp_gold_dynamics_rechamada` | Dynamics - Base para Rechamada |
# MAGIC | `dexp_gold_servicenow_chamados` | EXPBR - Chamados Servicenow |
# MAGIC | `dexp_gold_resenhas_appsheets` | Resenhas EXP BR AppSheets |
# MAGIC | `dexp_gold_resenhas_brasil` | Resenhas Brasil |

# COMMAND ----------

import os
import sys
from functools import reduce

from pyspark.sql import functions as F

sys.path.append(os.path.abspath(".."))
from dexp import tableau as tb
from dexp.tableau import excluir, filtro_data, igual, manter, remapear

dbutils.widgets.text("catalog", "sandbox")
dbutils.widgets.text("schema", "sustentacao_bau_experiencias")
CATALOGO = dbutils.widgets.get("catalog")
SCHEMA = dbutils.widgets.get("schema")
tb.preparar_sessao(spark)


def silver(tabela):
    return spark.table(f"{CATALOGO}.{SCHEMA}.dexp_silver_{tabela}").drop("_versao", "_origem")


def uniao(*dfs):
    """União de linhas do Prep: junta por nome de coluna; o que falta num lado fica nulo."""
    return reduce(lambda a, b: a.unionByName(b, allowMissingColumns=True), dfs)


def deduplicar(df, chave, minimos, maximos=()):
    """Agregação do Prep usada para tirar duplicadas: agrupa pela chave e pega MIN/MAX de cada coluna listada.
    As colunas fora das listas saem do resultado, como no Prep."""
    tipos = dict(df.dtypes)

    def agregar(coluna, funcao):
        if tipos[coluna] == "string":
            return (tb.minimo_texto(coluna) if funcao == "min" else tb.maximo_texto(coluna)).alias(coluna)
        return (F.min(coluna) if funcao == "min" else F.max(coluna)).alias(coluna)

    return df.groupBy(chave).agg(*[agregar(c, "min") for c in minimos], *[agregar(c, "max") for c in maximos])


def gravar(df, tabela, descricao):
    nome = f"{CATALOGO}.{SCHEMA}.{tabela}"
    df.write.mode("overwrite").option("overwriteSchema", "true").saveAsTable(nome)
    spark.sql(f"COMMENT ON TABLE {nome} IS '{descricao}'")
    print(f"{tabela:34} {spark.table(nome).count():>9,} linhas")

# COMMAND ----------

# MAGIC %md ## Regras compartilhadas

# COMMAND ----------

STATUS_SEM_EMOJI = {
    "Finalizado": ["✅ Finalizado"], "Cancelado": ["❌ Cancelado"], "Interface": ["🔀 Interface"],
    "Sistema": ["🤖 Sistema"], "Backoffice": ["🔺Backoffice"], "Cliente": ["👤 Cliente"],
}
ERRO_OPERACIONAL_CRIADO = {"Erro operacional Criado Em": ["Erro operacional"]}
DESVIO = "Solicitação não procedente - Desvio operacional"

ETAPAS_N1 = [
    "Análise Aplicativo Consultoria", "Análise Aplicativo Força de Vendas", "Análise Aplicativo Natura Vendas",
    "Análise de espaço digital", "Analise de liberação do espaço", "Análise de senha", "Análise de Vale-Troca",
    "Análise pedido espaço default", "Análise Plano de crescimento", "Análise Site Consultoria",
    "Análise Site Força de Vendas", "Análise Site Natura", "Cancelamento de Pedido", "Aguardando N3 Experiência",
]
ETAPAS_N2 = ["Acompanhamento tecnologia - espaço digital", "Análise Correção Sistema - SM", "Abertura do chamado"]
SOLUCOES_N2 = ["Abrir chamado", "Card criado no Jira"]
SEGUNDOS_24H, SEGUNDOS_5H = 86400, 18000

DEDUP_SALESFORCE = ["aplicativo_com_problemas", "caso_pai_chamado", "chamado", "data_de_criacao", "data_do_sla", "etapa",
                    "etapa_1", "experience", "motivo", "primeira_categoria", "proprietario", "segunda_categoria",
                    "solucao", "status_da_atividade", "termino_real"]


def classificar_nivel(rotulo_1, rotulo_2, olhar_chamado):
    """Nivel de Atendimento (N1/N2) e Fase (Fase 1/Fase 2) usam a mesma regra; a versão 'Encerrado em' também olha o Chamado."""
    regra = (F.when(igual("etapa", *ETAPAS_N1), rotulo_1)
              .when(igual("etapa", *ETAPAS_N2), rotulo_2)
              .when(igual("solucao", *SOLUCOES_N2), rotulo_2))
    if olhar_chamado:
        regra = regra.when(F.col("chamado").isNotNull() & (F.col("chamado") != ""), rotulo_2)
    return regra.otherwise(rotulo_1)


def tipo_protocolo():
    central = "central_de_atendimento"
    return (F.when(igual(central, "MÍDIAS SOCIAIS", "REDE NATURA", "Avon Ecomm", "SNAC"), "Protocolos CF")
             .when(igual(central, "Ato - Atendimento Líder", "CAN", "CIN", "Varejo"), "Protocolos CB")
             .when(igual("fonte", "Salesforce") & igual("tipo_de_registro_do_caso", "Atendimento CF"), "Protocolos CF")
             .when(igual("fonte", "Salesforce") & igual("tipo_de_registro_do_caso", "Atendimento Franquias"), "Franquias")
             .otherwise("Outro"))


def prazo(segundos, limite):
    return (F.when(F.col("termino_real").isNull(), "BACKLOG")
             .when(F.col(segundos) <= limite, "DENTRO DO PRAZO")
             .otherwise("FORA DO PRAZO"))


def faixa_tempo_solucao():
    s = F.col("segundos_corridos_experiencia")
    return F.when(s <= SEGUNDOS_5H, "ATÉ 5 HORAS").when(s <= SEGUNDOS_24H, "ATÉ 24 HORAS").otherwise("ACIMA DE 24 HORAS")


def com_tribos(df):
    """Join à direita com a aba Base Dynamics das Tribos: mantém todas as tarefas e traz a tribo pela Experience."""
    tribos = silver("tribos_dynamics").withColumnRenamed("experience", "experience_tribos")
    return df.join(tribos, tb.chave_join(df["experience"]) == tb.chave_join(tribos["experience_tribos"]), "left")

# COMMAND ----------

# MAGIC %md ## Salesforce legado (Salesforce CF) – usado nas duas visões

# COMMAND ----------

# [8] [23] [34]
salesforce_legado = (
    deduplicar(silver("salesforce_cf_legado"), "numero_da_ocorrencia",
               minimos=["primeira_categoria", "chamado"],
               maximos=["aplicativo_com_problemas", "experience", "data_de_criacao", "data_do_sla", "etapa", "etapa_1",
                        "motivo", "proprietario", "segunda_categoria", "solucao", "status_da_atividade", "termino_real"])
    .withColumn("status_da_atividade", remapear("status_da_atividade", STATUS_SEM_EMOJI))
    .withColumn("tipo_de_registro_do_caso", F.lit("Atendimento CF"))
)

# COMMAND ----------

# MAGIC %md ## Visão "Criado em" – [52] a [67]

# COMMAND ----------

criados_sf = silver("salesforce_cf_criados")

# [9] Dynamics, sem tratamento
criado_dynamics = silver("dynamics_criados_em").withColumn("fonte", F.lit("Dynamics"))

# [7] [22] [33] [44] Salesforce criados de nov a dez/2025
criado_sf_nov_dez25 = (
    criados_sf
    .withColumn("solucao", remapear("solucao", ERRO_OPERACIONAL_CRIADO))
    .withColumn("status_da_atividade", remapear("status_da_atividade", {"Finalizado": ["✅ Finalizado"], "Interface": ["🔀 Interface"]}))
    .where(excluir("status_da_atividade", "🤖 Sistema", "❌ Cancelado", "🔺Backoffice"))
    .transform(lambda df: deduplicar(df, "numero_da_ocorrencia", DEDUP_SALESFORCE, ["tipo_de_registro_do_caso"]))
    .where(filtro_data("data_de_criacao", de="2025-11-01", ate="2025-12-31"))
    .withColumn("fonte", F.lit("Salesforce"))
)

# [45] Salesforce legado criado até 31/10/2025
criado_sf_legado = (
    salesforce_legado
    .withColumn("solucao", remapear("solucao", ERRO_OPERACIONAL_CRIADO))
    .where(filtro_data("data_de_criacao", ate="2025-10-31"))
    .withColumn("fonte", F.lit("Salesforce"))
)

# [1] [17] [28] [40] Salesforce criados a partir de 2026
criado_sf_2026 = (
    criados_sf
    .where(filtro_data("data_de_criacao", de="2026-01-01"))
    .transform(lambda df: deduplicar(df, "numero_da_ocorrencia", DEDUP_SALESFORCE + ["id_caso_completo"],
                                     ["tipo_de_registro_do_caso"]))
    .withColumn("status_da_atividade", remapear("status_da_atividade",
                                                {k: v for k, v in STATUS_SEM_EMOJI.items() if k != "Cliente"}))
    .withColumn("solucao", remapear("solucao", ERRO_OPERACIONAL_CRIADO))
    .withColumn("fonte", F.lit("Salesforce"))
)

# [52] [57] [60] [63] [67]
visao_criado = (
    uniao(criado_sf_nov_dez25, criado_sf_legado, criado_dynamics, criado_sf_2026)
    .withColumn("dias_corridos_cliente", tb.diff_dias(F.col("termino_real"), F.col("data_do_sla")))
    .withColumn("segundos_corridos_experiencia", tb.diff_segundos(F.col("data_de_criacao"), F.col("termino_real")))
    .withColumn("sla_cliente", F.when(F.col("termino_real").isNull(), "BACKLOG")
                                .when(F.col("dias_corridos_cliente") >= 0, "DENTRO DO PRAZO")
                                .otherwise("FORA DO PRAZO"))
    .withColumn("sla_experiencia_24_horas", prazo("segundos_corridos_experiencia", SEGUNDOS_24H))
    .withColumn("nivel_de_atendimento", classificar_nivel("N1", "N2", olhar_chamado=False))
    .withColumn("faixa_tempo_solucao_sla_experiencia", faixa_tempo_solucao())
    .withColumn("sla_5_horas", prazo("segundos_corridos_experiencia", SEGUNDOS_5H))
    .withColumn("solucao", remapear("solucao", {f"{DESVIO} Criados Em": [DESVIO]}))
    .transform(com_tribos)
    .withColumn("fase", classificar_nivel("Fase 1", "Fase 2", olhar_chamado=False))
    .withColumn("tipo_protocolo", tipo_protocolo())
    .drop("problema_de_sistema", "opcao_menu", "problema_de_sistema_fv", "problema_site_natura")
    .withColumn("base", F.when(F.col("numero_da_ocorrencia").isNull(), "").otherwise("Criado em"))
    .withColumn("data", F.col("data_de_criacao"))
)

# COMMAND ----------

# MAGIC %md ## Visão "Encerrado em" – [61] a [72]

# COMMAND ----------

encerrados_sf = silver("salesforce_cf_encerrados")

# [12] Dynamics, sem tratamento
encerrado_dynamics = silver("dynamics_termino_real").withColumn("fonte", F.lit("Dynamics"))

# [46] Salesforce legado encerrado até 31/10/2025
encerrado_sf_legado = (
    salesforce_legado
    .where(excluir("status_da_atividade", "Interface"))
    .where(filtro_data("termino_real", ate="2025-10-31"))
)

# [11] [25] [36] [37] [48] [54] [58] Salesforce encerrados em nov a dez/2025
encerrados_nov25 = (
    encerrados_sf
    .where(filtro_data("termino_real", de="2025-11-01"))
    .where(excluir("status_da_atividade", "❌ Cancelado"))
    .withColumn("status_da_atividade", remapear("status_da_atividade", {"Finalizado": ["✅ Finalizado"]}))
)
encerrado_sf_nov_dez25 = (
    uniao(
        deduplicar(encerrados_nov25.where(excluir("solucao", "Erro operacional")), "numero_da_ocorrencia",
                   DEDUP_SALESFORCE, ["tipo_de_registro_do_caso"]),
        encerrados_nov25.where(manter("solucao", "Erro operacional")),
    )
    .where(filtro_data("termino_real", de="2025-10-27", ate="2025-12-31"))
)

# [2] [18] [29] [30] [31] [41] [42] [50] [56] Salesforce encerrados a partir de 2026: N1, N2 e Retrabalho
encerrados_2026 = (
    encerrados_sf
    .where(filtro_data("termino_real", de="2026-01-01"))
    .withColumn("status_da_atividade", remapear("status_da_atividade",
                                                {"Finalizado": ["✅ Finalizado"], "Cancelado": ["❌ Cancelado"]}))
)
DEDUP_SITUACAO = DEDUP_SALESFORCE + ["id_caso_completo", "situacao"]
encerrado_sf_2026 = uniao(
    deduplicar(encerrados_2026.where(manter("solucao", "Erro operacional") & manter("status_da_atividade", "Finalizado"))
               .withColumn("situacao", F.lit("Retrabalho")), "numero_da_ocorrencia", DEDUP_SITUACAO, ["tipo_de_registro_do_caso"]),
    encerrados_2026.where(manter("solucao", "Abrir chamado")).withColumn("situacao", F.lit("N2")),
    deduplicar(encerrados_2026.where(manter("chamado", None) & manter("solucao", "Caso resolvido", "Resolvido"))
               .withColumn("situacao", F.lit("N1")), "numero_da_ocorrencia", DEDUP_SITUACAO, ["tipo_de_registro_do_caso"]),
)

# [61] União e fonte
visao_encerrado = uniao(encerrado_sf_2026, encerrado_sf_nov_dez25, encerrado_sf_legado, encerrado_dynamics)
visao_encerrado = visao_encerrado.withColumn("fonte", F.coalesce(F.col("fonte"), F.lit("Salesforce")))

# [64] Tribos
visao_encerrado = com_tribos(visao_encerrado)

# [66] Feriados de dez/2025: criação em 24 ou 25/12 vai para 26/12 e em 31/12 vai para 02/01/2026, mantendo o horário
criacao = F.col("data_de_criacao")
dia = F.to_date(criacao)
visao_encerrado = visao_encerrado.withColumn(
    "data_de_criacao",
    F.when(dia.isin(F.lit("2025-12-24").cast("date"), F.lit("2025-12-25").cast("date")),
           tb.somar_dias(criacao, F.datediff(F.lit("2025-12-26").cast("date"), dia)))
     .when(dia == F.lit("2025-12-31").cast("date"), tb.somar_dias(criacao, F.datediff(F.lit("2026-01-02").cast("date"), dia)))
     .otherwise(criacao))

# [68] Prazos
visao_encerrado = (
    visao_encerrado
    .withColumn("dias_corridos_cliente", tb.diff_dias(F.col("termino_real"), F.col("data_do_sla")))
    .withColumn("segundos_corridos_experiencia", tb.diff_segundos(F.col("data_de_criacao"), F.col("termino_real")))
    .withColumn("sla_cliente", F.when(F.col("termino_real").isNull(), "BACKLOG")
                                .when(F.col("termino_real") > F.col("data_do_sla"), "FORA DO PRAZO")
                                .otherwise("DENTRO DO PRAZO"))
    .withColumn("sla_experiencia", prazo("segundos_corridos_experiencia", SEGUNDOS_24H))
    .withColumn("nivel_de_atendimento", classificar_nivel("N1", "N2", olhar_chamado=True))
    .withColumn("faixa_tempo_solucao_sla_experiencia", faixa_tempo_solucao())
    .withColumn("sla_5_horas", prazo("segundos_corridos_experiencia", SEGUNDOS_5H))
)

# [69] Horas úteis: das 8h às 22h, de segunda a sexta (14 horas por dia útil)
criacao, termino = F.col("data_de_criacao"), F.col("termino_real")
dia_criacao, dia_termino = tb.dia_semana(criacao), tb.dia_semana(termino)
inicio_util = (
    F.when(dia_criacao.isin(1, 7), tb.fazer_data_hora(tb.somar_dias(criacao, F.when(dia_criacao == 1, 1).otherwise(2)), 8))
     .when(F.hour(criacao) < 8, tb.fazer_data_hora(criacao, 8))
     .when(F.hour(criacao) >= 22, tb.fazer_data_hora(tb.somar_dias(criacao, F.when(dia_criacao == 6, 3).otherwise(1)), 8))
     .otherwise(criacao))
termino_util = (
    F.when(dia_termino.isin(1, 7), tb.fazer_data_hora(tb.somar_dias(termino, F.when(dia_termino == 1, -2).otherwise(-1)), 22))
     .when(F.hour(termino) < 8, tb.fazer_data_hora(tb.somar_dias(termino, F.when(dia_termino == 2, -3).otherwise(-1)), 22))
     .when(F.hour(termino) >= 22, tb.fazer_data_hora(termino, 22))
     .otherwise(termino))
visao_encerrado = (
    visao_encerrado
    .withColumn("_dia_da_semana_criacao", dia_criacao)
    .withColumn("_dia_da_semana_termino", dia_termino)
    .withColumn("_data_fim_referencia", F.coalesce(termino, tb.agora()))
    .withColumn("_inicio_util", inicio_util)
    .withColumn("_termino_util", termino_util)
)
iu, tu = F.col("_inicio_util"), F.col("_termino_util")
dias_uteis_inteiros = (
    (tb.diff_dias(iu, tu) - 1)
    - tb.diff_semanas(iu, tu) * 2
    - F.when(tb.dia_semana(iu) == 1, 1).otherwise(0)
    + F.when(tb.dia_semana(tu) == 1, 1).otherwise(0)
)
visao_encerrado = (
    visao_encerrado
    .withColumn("segundos_uteis_decorridos",
                F.when(F.to_date(iu) == F.to_date(tu), tb.diff_segundos(iu, tu))
                 .otherwise(tb.diff_segundos(iu, tb.fazer_data_hora(iu, 22))
                            + tb.diff_segundos(tb.fazer_data_hora(tu, 8), tu)
                            + dias_uteis_inteiros * (14 * 3600)))
    .withColumnRenamed("sla_5_horas", "sla_5_horas_old")
    .withColumnRenamed("sla_experiencia", "sla_experiencia_old")
    .withColumn("sla_experiencia", prazo("segundos_uteis_decorridos", SEGUNDOS_24H))
    .withColumn("sla_5_horas", prazo("segundos_uteis_decorridos", SEGUNDOS_5H))
)

# [70] [71] Expurgo: quando a tarefa está na planilha de expurgo, o nível de lá prevalece
expurgo = silver("expurgo_dynamics").select(F.col("numero_da_ocorrencia").alias("numero"),
                                            F.col("nivel_de_atendimento").alias("nivel_expurgo"))
visao_encerrado = (
    visao_encerrado
    .join(expurgo, tb.chave_join(visao_encerrado["numero_da_ocorrencia"]) == tb.chave_join(expurgo["numero"]), "left")
    .withColumn("nivel_de_atendimento", F.coalesce("nivel_expurgo", "nivel_de_atendimento"))
    .drop("nivel_expurgo")
)

# [72]
visao_encerrado = (
    visao_encerrado
    .withColumn("fase", classificar_nivel("Fase 1", "Fase 2", olhar_chamado=True))
    .withColumn("tipo_protocolo", tipo_protocolo())
    .withColumn("base", F.when(F.col("numero_da_ocorrencia").isNull(), "").otherwise("Encerrado em"))
    .withColumn("data", F.col("termino_real"))
)

# COMMAND ----------

# MAGIC %md ## Saídas Dynamics – [73] a [86]

# COMMAND ----------

# [73] [74] Base unificada (extract "Dynamics - Termino Real")
tarefas = (
    uniao(visao_encerrado, visao_criado)
    .drop("sla_experiencia_24_horas")
    .withColumn("status_da_atividade", remapear("status_da_atividade", {"Finalizado": ["✅ Finalizado"]}))
    .withColumn("retrabalho", F.when(igual("solucao", "Erro Operacional", DESVIO), "Retrabalho").otherwise("Normal"))
)
gravar(tarefas, "dexp_gold_dynamics_tarefas",
       "Gold Daily Experiência BR: tarefas Dynamics e Salesforce nas visões Criado em e Encerrado em (extract Dynamics - Termino Real)")
tarefas = spark.table(f"{CATALOGO}.{SCHEMA}.dexp_gold_dynamics_tarefas")

# [76] Dynamics Nivel: tarefas encerradas no formato que o fluxo MKT junta à base dele
nivel = (
    tarefas.where(manter("base", "Encerrado em"))
    .select(F.col("nivel_de_atendimento").alias("nivel"), F.col("tipo_protocolo").alias("tipo"),
            F.col("numero_da_ocorrencia").alias("ticket"), F.col("motivo").alias("status_de_classificacao"),
            F.col("experience").alias("funcao_do_sistema"), F.col("termino_real").alias("data"),
            F.col("solucao").alias("status_de_finalizacao"), F.col("modificado_por").alias("responsavel_dynamics"))
    .withColumn("qtd_atendimentos", F.lit(1))
    .where(excluir("status_de_finalizacao", "Erro operacional"))
    .where(excluir("status_de_finalizacao", DESVIO))
)
gravar(nivel, "dexp_gold_dynamics_nivel", "Gold Daily Experiência BR: tarefas encerradas com nível, para o fluxo MKT (extract Dynamics Nivel)")

# [75] [78] [81] [83] [84] [85] Rechamada: mesma consultora e mesma tribo com tarefa no mês anterior
por_ocorrencia = (
    tarefas
    .where(excluir("base", "Criado em") & excluir("fonte", "Salesforce") & excluir("solucao", DESVIO)
           & excluir("fase", "Fase 1") & excluir("experience_tribos", "Incluir / Excluir membro"))
    .withColumn("numero_da_ocorrencia_limpo", F.trim(F.upper("numero_da_ocorrencia")))
    .groupBy("numero_da_ocorrencia_limpo")
    .agg(tb.minimo_texto("experience_tribos").alias("experience_tribos"),
         tb.maximo_texto("codigo_natura").alias("codigo_natura"),
         tb.minimo_texto("fase").alias("fase"),
         tb.minimo_texto("solucao").alias("solucao"),
         tb.maximo_texto("tipo_protocolo").alias("tipo_protocolo"),
         F.max("termino_real").alias("termino_real"))
    .withColumn("mes_ano", F.date_trunc("month", "termino_real"))
    .withColumn("mes", F.month("termino_real"))
    .withColumn("id_rechamada", F.concat("codigo_natura", F.lit("-"), "experience_tribos"))
    .withColumn("mes_seguinte", F.add_months("mes_ano", 1).cast("timestamp"))
)
# No join [84] o Prep põe o sufixo "-1" nas colunas do lado DIREITO (todas as ocorrências), não no do mês anterior:
# "ID Rechamada" é o do mês anterior (só preenchido quando casa) e "ID Rechamada-1" é o da própria ocorrência.
# Como a flag testa "ID Rechamada-1", hoje toda ocorrência com código e tribo vira "Rechamada" (12 mil de 16 mil).
# Mantido igual à produção; a rechamada de fato (casou com o mês anterior) é id_rechamada não nulo.
mes_anterior = (
    por_ocorrencia.groupBy("id_rechamada", "mes_ano").agg(F.max("mes_seguinte").alias("mes_seguinte"))
    .withColumnRenamed("mes_ano", "mes_ano_a")
)
atual = por_ocorrencia.select(
    "numero_da_ocorrencia_limpo", "experience_tribos", "codigo_natura", "fase", "solucao", "tipo_protocolo",
    "termino_real", "mes_ano", "mes", F.col("id_rechamada").alias("id_rechamada_1"),
    F.col("mes_seguinte").alias("mes_seguinte_1"))
rechamada = (
    atual
    .join(mes_anterior, (tb.chave_join(mes_anterior["id_rechamada"]) == tb.chave_join(atual["id_rechamada_1"]))
          & (mes_anterior["mes_seguinte"] == atual["mes_ano"]), "left")
    .withColumn("flag_de_rechamada", F.when(F.col("id_rechamada_1").isNotNull(), 1).otherwise(0))
    .withColumn("tarefa_status", F.when(F.col("id_rechamada_1").isNotNull(), "Rechamada").otherwise("Comum"))
    .drop("mes_seguinte_1", "mes_ano_a")
    .withColumnRenamed("numero_da_ocorrencia_limpo", "numero_da_ocorrencia")
)
gravar(rechamada, "dexp_gold_dynamics_rechamada", "Gold Daily Experiência BR: ocorrências com flag de rechamada (extract Dynamics - Base para Rechamada)")

# COMMAND ----------

# MAGIC %md ## Chamados ServiceNow – [10] [24] [35] [47]

# COMMAND ----------

incidentes = silver("servicenow_incidentes")
abertura = F.col("aberto_em")
incidentes = incidentes.withColumn(
    "dias_corridos",
    F.when(igual("status", "Cancelado"), tb.diff_dias(abertura, F.col("encerrado")))
     .when(igual("status", "Resolvido", "Encerrado"), tb.diff_dias(abertura, F.col("resolvido")))
     .otherwise(tb.diff_dias(abertura, tb.hoje())))
dias = F.col("dias_corridos")
incidentes = incidentes.withColumn(
    "faixa_dias",
    F.when(dias.isNull(), F.lit(None))
     .when(dias < 1, "NO MESMO DIA").when(dias < 2, "01 DIA").when(dias < 3, "02 DIAS").when(dias < 4, "03 DIAS")
     .when(dias < 11, "04 A 10 DIAS").when(dias < 21, "11 A 20 DIAS").when(dias < 31, "21 A 30 DIAS")
     .otherwise("MAIS DE 30 DIAS"))
grupos = silver("tribos_grupos_servicenow").withColumnRenamed("grupo_de_atribuicao", "grupo_de_atribuicao_tribos")
chamados = incidentes.join(grupos, tb.chave_join(incidentes["grupo_de_atribuicao"])
                           == tb.chave_join(grupos["grupo_de_atribuicao_tribos"]), "left")
gravar(chamados, "dexp_gold_servicenow_chamados", "Gold Daily Experiência BR: incidentes ServiceNow com tribo (extract EXPBR - Chamados Servicenow)")

# COMMAND ----------

# MAGIC %md ## Resenhas AppSheets – [5] [20] [32] [43]

# COMMAND ----------

APLICATIVO_SEMPRE_PRESENTE = {"Sempre Presente": ["Natura CF"]}
LOJAS = ["Google Play", "Applestore"]

resenhas = (
    silver("resenhas_appsheets")
    .withColumn("aplicativo", remapear("aplicativo", APLICATIVO_SEMPRE_PRESENTE))
    .withColumn("data_da_resposta", tb.fazer_data_hora(F.col("data_da_resposta"), 23, 59, 59))
)
resposta = F.col("data_da_resposta")
dia_resposta = tb.dia_semana(resposta)
inicio_sla = (
    F.when(dia_resposta.isin(1, 7), tb.fazer_data_hora(tb.somar_dias(resposta, F.when(dia_resposta == 1, 1).otherwise(2)), 8))
     .when(F.hour(resposta) < 8, tb.fazer_data_hora(resposta, 8))
     .otherwise(resposta))
resenhas = (
    resenhas
    .withColumn("_dia_da_semana_da_resposta", dia_resposta)
    .withColumn("_hora_da_resposta", F.hour(resposta))
    .withColumn("inicio_da_contagem_sla_brasil", inicio_sla)
)
inicio = F.col("inicio_da_contagem_sla_brasil")
resenhas = resenhas.withColumn(
    "prazo_sla_brasil", F.when(tb.dia_semana(inicio) == 6, tb.somar_dias(inicio, 3)).otherwise(tb.somar_dias(inicio, 1)))
resposta_exp, prazo_br = F.col("data_da_resposta_exp"), F.col("prazo_sla_brasil")
aplicativo, loja = F.col("aplicativo"), F.col("loja")
resenhas = (
    resenhas
    .withColumn("status_sla",
                F.when(resposta_exp.isNotNull(), F.when(resposta_exp <= prazo_br, "Dentro do SLA").otherwise("Fora do SLA"))
                 .otherwise(F.when(tb.agora() > prazo_br, "Fora do SLA").otherwise("Dentro do SLA")))
    .withColumn("data_avaliacao", resposta)
    .withColumn("nome_aplicativo", aplicativo)
    .withColumn("star_rating", tb.inteiro("classificacao_de_estrelas"))
    .withColumn("app_nome",
                F.when(igual(aplicativo, *LOJAS) & igual(loja, *LOJAS), "Não Identificado")
                 .when(igual(aplicativo, *LOJAS),
                       F.when(loja.isNull() | (loja == "") | igual(loja, *LOJAS), "Não Identificado").otherwise(loja))
                 .when(igual(loja, *LOJAS),
                       F.when(aplicativo.isNull() | (aplicativo == "") | igual(aplicativo, *LOJAS), "Não Identificado")
                        .otherwise(aplicativo))
                 .otherwise("Não Identificado"))
    .withColumn("app_nome", remapear("app_nome", APLICATIVO_SEMPRE_PRESENTE))
)
gravar(resenhas, "dexp_gold_resenhas_appsheets", "Gold Daily Experiência BR: resenhas tratadas no AppSheets com SLA (extract Resenhas EXP BR AppSheets)")

# COMMAND ----------

# MAGIC %md ## Resenhas Brasil (Google Play) – [13] a [16] [27] [39] [49] [55] [59]

# COMMAND ----------

def texto_iso_para_data_hora(coluna):
    """DATETIME(MID(x, 1, 10) + " " + MID(x, 12, 8)) sobre '2015-12-20T03:14:33Z'."""
    c = F.col(coluna)
    return F.try_to_timestamp(F.concat(F.substring(c, 1, 10), F.lit(" "), F.substring(c, 12, 8)), F.lit("yyyy-MM-dd HH:mm:ss"))


avaliacoes = (
    silver("resenhas_google_play")
    .withColumn("elegibilidade_sla", F.when(F.col("review_text").isNull() | (F.col("review_text") == ""), "Não Aplicável")
                                      .otherwise("Aplicável"))
    .withColumn("data_avaliacao", texto_iso_para_data_hora("review_submit_date_and_time"))
    .withColumn("data_da_resposta_exp", texto_iso_para_data_hora("developer_reply_date_and_time"))
    .withColumn("data_atualizacao_da_avaliacao", texto_iso_para_data_hora("review_last_update_date_and_time"))
)
estrelas = F.col("star_rating")
baixa, alta = estrelas.between(1, 3), estrelas.between(4, 5)
avaliacao, resposta_exp, atualizacao = F.col("data_avaliacao"), F.col("data_da_resposta_exp"), F.col("data_atualizacao_da_avaliacao")
dias_desde_avaliacao = tb.diff_dias(avaliacao, tb.hoje())
dias_desde_atualizacao = tb.diff_dias(atualizacao, tb.hoje())
tolerancia_baixa = F.when(tb.dia_semana(avaliacao) == 6, 2).when(tb.dia_semana(avaliacao) == 7, 1).otherwise(1)


def dentro_ou_fora(fora):
    return F.when(fora, "Fora do SLA").otherwise("Dentro do SLA")


sem_resposta = (F.when(baixa, dentro_ou_fora(dias_desde_avaliacao > tolerancia_baixa))
                 .when(alta, dentro_ou_fora(dias_desde_avaliacao > 5))
                 .otherwise("Dentro do SLA"))
usuario_replicou = (F.when(baixa, dentro_ou_fora(dias_desde_atualizacao > 1))
                     .when(alta, dentro_ou_fora(dias_desde_atualizacao > 5))
                     .otherwise("Dentro do SLA"))
# No Tableau, data + número soma DIAS: o "+ 86399" da fórmula original soma 86.399 dias (e não segundos),
# então esta comparação nunca dá "Fora do SLA". Mantido igual para os números baterem com o extract atual.
limite_resposta_baixa = tb.somar_dias(F.date_trunc("day", tb.somar_dias(avaliacao, tolerancia_baixa)), 86399)
ultima_foi_exp = (F.when(baixa, dentro_ou_fora(resposta_exp > limite_resposta_baixa))
                   .when(alta, dentro_ou_fora(F.to_date(resposta_exp) > F.date_add(F.to_date(avaliacao), 5)))
                   .otherwise("Dentro do SLA"))
status_sla = (F.when(resposta_exp.isNull(), sem_resposta)
               .otherwise(F.when(atualizacao.isNotNull() & (atualizacao > resposta_exp), usuario_replicou)
                           .otherwise(ultima_foi_exp)))
avaliacoes = (
    avaliacoes
    .withColumn("prazo_sla", F.when(baixa, 1).when(alta, 5).otherwise(0))
    .withColumn("status_sla", status_sla)
    .withColumn("status_sla_2", F.when(F.col("elegibilidade_sla") == "Não Aplicável", "Não Aplicável").otherwise(status_sla))
    .withColumn("package_name", remapear("package_name", {
        "App Avon": ["com.naturaeco.app.avon"],
        "App Consultoria Natura": ["Consultoria Natura", "net.natura.cn"],
        "App Força de Vendas": ["Força de Vendas", "net.natura.fv"],
        "App Sempre Presente": ["Sempre Presente", "net.natura.semprepresente"],
    }))
    .withColumnRenamed("package_name", "nome_aplicativo")
)
gravar(avaliacoes, "dexp_gold_resenhas_brasil", "Gold Daily Experiência BR: avaliações das lojas de apps com SLA (extract Resenhas Brasil)")
