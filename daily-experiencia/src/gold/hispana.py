# Databricks notebook source
# MAGIC %md
# MAGIC # Gold – Hispana
# MAGIC
# MAGIC Reproduz o fluxo Tableau Prep **"Daily Experiencia OIS"**. Os números entre colchetes, como `[71]`, são as etapas
# MAGIC de `docs/fluxos/hispana.md`. As colunas usam o nome do Prep em snake_case.
# MAGIC
# MAGIC | Tabela gold (`dexp_gold_hispana_*`) | Extract atual no Tableau Cloud |
# MAGIC |---|---|
# MAGIC | `base_mkt` | Base MKT OIS |
# MAGIC | `base_mkt_hc` | Base MKT HC OIS |
# MAGIC | `base_mkt_lojas` | Base MKT Lojas OIS |
# MAGIC | `completo` | MKT Hispana Completo |
# MAGIC | `produtividade` | Experiencia Hispana Produtividade |
# MAGIC | `resenhas` | Resenhas OIS |
# MAGIC | `appsheets_resenhas` | AppSheets Resenhas OIs |
# MAGIC | `chamados_servicenow` | Experiencia Hispana - Chamados Servicenow |
# MAGIC | `ticket_medio` | Ticket Medio Hispana |

# COMMAND ----------

import os
import sys

from pyspark.sql import functions as F

sys.path.append(os.path.abspath(".."))
from dexp import regras_hispana as R
from dexp import tableau as tb
from dexp.prep import juntar, remover, uniao
from dexp.regras_mkt_comuns import segundos_hms
from dexp.tableau import excluir, filtro_data, igual, manter, remapear

dbutils.widgets.text("catalog", "sandbox")
dbutils.widgets.text("schema", "sustentacao_bau_experiencias")
CATALOGO = dbutils.widgets.get("catalog")
SCHEMA = dbutils.widgets.get("schema")
tb.preparar_sessao(spark)

DENTRO, FORA = "Dentro do SLA", "Fora do SLA"
MARCO_2026 = F.to_timestamp(F.lit("2026-03-01"))
OUTUBRO_2026 = F.to_timestamp(F.lit("2026-10-01"))
DIAS_16_17 = [F.lit("2026-03-16").cast("date"), F.lit("2026-03-17").cast("date")]


def silver(tabela):
    return spark.table(f"{CATALOGO}.{SCHEMA}.dexp_silver_hispana_{tabela}").drop("_versao", "_origem")


def gravar(df, tabela, descricao):
    nome = f"{CATALOGO}.{SCHEMA}.dexp_gold_hispana_{tabela}"
    df.write.mode("overwrite").option("overwriteSchema", "true").saveAsTable(nome)
    spark.sql(f"COMMENT ON TABLE {nome} IS '{descricao}'")
    print(f"dexp_gold_hispana_{tabela:24} {spark.table(nome).count():>9,} linhas")


def por_setor(coluna, mapa):
    """IF [Setor Fim] = "X" THEN "Y" ... ELSE NULL, sem diferenciar maiúsculas."""
    chaves = F.create_map(*[F.lit(v) for par in {k.lower(): r for k, r in mapa.items()}.items() for v in par])
    return F.try_element_at(chaves, F.lower(F.col(coluna)))


def caso_nivel(status, regra):
    """Um CASE do Nível: cada grupo de status vira o rótulo; o resto, o ELSE da regra."""
    expr = None
    for rotulo, valores in regra["rotulos"].items():
        cond = igual(status, *valores)
        expr = F.when(cond, F.lit(rotulo)) if expr is None else expr.when(cond, F.lit(rotulo))
    return expr.otherwise(F.lit(regra["senao"]))


def nivel(data, status, regras):
    """IF data < mar/26 ... ELSEIF data < out/26 ... ELSE; data nula cai na última regra, como no Tableau."""
    antes_de_marco, ate_setembro, atual = regras
    return (F.when(F.col(data) < MARCO_2026, caso_nivel(status, antes_de_marco))
             .when(F.col(data) < OUTUBRO_2026, caso_nivel(status, ate_setembro))
             .otherwise(caso_nivel(status, atual)))


def semana(c):
    """DATEPART('week'): a semana 1 começa em 1º de janeiro e as seguintes, no domingo."""
    c = F.col(c) if isinstance(c, str) else c
    primeiro_de_janeiro = F.to_date(F.concat(F.year(c).cast("string"), F.lit("-01-01")))
    return ((F.dayofyear(c) + F.dayofweek(primeiro_de_janeiro) - 2) / 7).cast("int") + 1


def somar_horas(c, horas):
    return (F.col(c).cast("long") + horas * 3600).cast("timestamp")


def texto_iso_para_data_hora(coluna):
    """Mudar tipo do Prep sobre '2015-12-20T03:14:33Z'."""
    c = F.col(coluna)
    return F.try_to_timestamp(F.concat(F.substring(c, 1, 10), F.lit(" "), F.substring(c, 12, 8)), F.lit("yyyy-MM-dd HH:mm:ss"))


def corrigir_funcao_equador(df):
    """PEDIDO NO APARECE EN SALESFORCE é SAP no Equador."""
    return df.withColumn("funcao_do_sistema",
                         F.when(igual("pais", "Ecuador") & igual("funcao_do_sistema", "PEDIDO NO APARECE EN SALESFORCE"),
                                "PEDIDO NO APARECE EN SAP").otherwise(F.col("funcao_do_sistema")))

# COMMAND ----------

# MAGIC %md ## Saídas independentes: Ticket Médio, ServiceNow e Resenhas

# COMMAND ----------

# [10] [27] [38]
gravar(silver("ticket_medio").select("pais", "valor_por_pedido", "data_contato"), "ticket_medio",
       "Gold Daily Hispana: ticket médio por país e mês (extract Ticket Medio Hispana)")

# COMMAND ----------

# [19] [33] [42] [49] [55] [60]
faixa = lambda c: (F.when(c == 0, "EN EL DIA").when(c == 1, "01 DIA").when(c == 2, "02 DIAS").when(c == 3, "03 DIAS")
                   .when(c.between(4, 10), "04 A 10 DIAS").when(c.between(11, 20), "11 A 20 DIAS")
                   .when(c.between(21, 30), "21 A 30 DIAS").otherwise("MAS QUE 30 DIAS"))
servicenow = (
    silver("servicenow")
    .withColumn("aging_encerrado", tb.diff_dias(F.col("aberto"), F.col("encerrado")))
    .withColumn("aging_abertura", tb.diff_dias(F.col("aberto"), tb.hoje()))
    .withColumn("faixa_aging_encerrado", faixa(F.col("aging_encerrado")))
    .withColumn("faixa_aging_aberto", faixa(F.col("aging_abertura")))
    .withColumn("estado", remapear("estado", {"En Progreso": ["Em andamento"], "En espera": ["Em espera"], "Cerrado": ["Encerrado"],
                                              "Nuevo": ["Novo"], "Resuelto": ["Resolvido"]}))
)
for antigo, novo in [("aberto", "abierto"), ("descricao_resumida", "descripcion_resumida"), ("prioridade", "prioridad"),
                     ("estado", "estatus"), ("grupo_de_atribuicao", "grupo_de_asignacion"), ("atualizado_em", "actualizado_en"),
                     ("atualizado_por", "actualizado_por"), ("criado_por", "creado_por"), ("encerrado", "cerrado"),
                     ("resolvido", "resuelto"), ("tipo_de_tarefa", "tipo_de_tarea"), ("servico", "servicio"),
                     ("motivo_para_estar_em_espera", "razon_para_estar_en_espera"), ("em_qual_pais_ocorre_o_incidente", "pais"),
                     ("nome_do_solicitante", "nombre_del_solicitante"), ("quem_esta_sendo_impactado", "quien_fue_impactado"),
                     ("qual_a_marca_impactada", "marca_impactada"), ("numero_2", "problema"),
                     ("codigo_de_resolucao", "codigo_de_resolucion"), ("declaracao_do_problema", "declaracion_del_problema")]:
    servicenow = servicenow.withColumnRenamed(antigo, novo)
resumen = None
for trecho, rotulo in R.RESUMEN_SERVICENOW:
    cond = F.lower(F.col("descripcion_resumida")).contains(trecho.lower())
    resumen = F.when(cond, F.lit(rotulo)) if resumen is None else resumen.when(cond, F.lit(rotulo))
PAISES_FORA = ["Argentina, Chile, México, Peru", "Argentina, Colômbia, Equador, México", "Argentina, México", "Brasil", "Brasil, Chile",
               "Chile, Colômbia, Equador, México, Peru", "Chile, Colômbia, Peru", "Colômbia, México", "Colômbia, Peru", "El Salvador"]
servicenow = (
    servicenow
    .withColumn("semana_abierto", semana("abierto"))
    .withColumn("semana_cerrado", semana("cerrado"))
    .withColumn("resumen", resumen.otherwise("NO MAPEADO"))
    .where(F.col("pais").isNotNull() & excluir("pais", *PAISES_FORA))
)
gravar(servicenow, "chamados_servicenow", "Gold Daily Hispana: incidentes ServiceNow (extract Experiencia Hispana - Chamados Servicenow)")

# COMMAND ----------

# [5] [23] [35] [43] Resenhas tratadas no AppSheets. O prazo conta a partir das 8h do dia útil da resposta.
resenhas_appsheets = (
    silver("resenhas_appsheets").withColumnRenamed("coluna_1", "id")
    .withColumn("aplicacion", remapear("aplicacion", {"App_Avon": ["Avon"], "Resenhas Latam": ["Resenhas LATAM", "Natura LATAM"],
                                                      "App Natura": [" Natura: Perfumes y Cosméticos"]}))
    .withColumnRenamed("fecha_de_la_respuesta", "fecha_de_la_respuesta_original")
    .withColumn("fecha_de_la_respuesta", tb.fazer_data_hora(F.date_add("fecha_de_la_respuesta_original", 1), 2, 59, 59))
)
resposta = F.col("fecha_de_la_respuesta")
dia_resposta = tb.dia_semana(resposta)
resenhas_appsheets = resenhas_appsheets.withColumn(
    "inicio_da_contagem_sla_hispana",
    F.when(dia_resposta == 7, tb.fazer_data_hora(tb.somar_dias(resposta, 2), 8))
     .when(dia_resposta == 1, tb.fazer_data_hora(tb.somar_dias(resposta, 1), 8))
     .otherwise(tb.fazer_data_hora(resposta, 8)))
inicio = F.col("inicio_da_contagem_sla_hispana")
resenhas_appsheets = resenhas_appsheets.withColumn(
    "prazo_sla_hispana", F.when(tb.dia_semana(inicio) == 6, tb.somar_dias(inicio, 3)).otherwise(tb.somar_dias(inicio, 1)))
resposta_exp, prazo_h = F.col("fecha_de_la_respuesta_exp"), F.col("prazo_sla_hispana")
resenhas_appsheets = resenhas_appsheets.withColumn(
    "status_sla_hispana",
    F.when(resposta_exp.isNotNull(), F.when(resposta_exp <= prazo_h, DENTRO).otherwise(FORA))
     .otherwise(F.when(tb.agora() <= prazo_h, DENTRO).otherwise(FORA)))
gravar(resenhas_appsheets, "appsheets_resenhas", "Gold Daily Hispana: resenhas tratadas no AppSheets com SLA (extract AppSheets Resenhas OIs)")
resenhas_appsheets = spark.table(f"{CATALOGO}.{SCHEMA}.dexp_gold_hispana_appsheets_resenhas")

# COMMAND ----------

# [6] [13] [17] [18] [32] [41] [48] [54] Avaliações das lojas. Só a planilha Latam não é filtrada por idioma.
lojas = spark.table(f"{CATALOGO}.{SCHEMA}.dexp_silver_hispana_resenhas_lojas")
ORIGEM_APP = F.col("_origem")
resenhas = (
    lojas.where((ORIGEM_APP == "dexp_bronze_resenhas_latam") | igual("reviewer_language", "es"))
    .withColumn("table_names", F.when(ORIGEM_APP == "dexp_bronze_app_natura", "App Natura")
                                .when(ORIGEM_APP == "dexp_bronze_app_avon", "App Avon")
                                .when(ORIGEM_APP == "dexp_bronze_mi_negocio", "Mi Negocio")
                                .otherwise("Resenhas Latam"))
    .drop("_versao", "_origem")
    .withColumn("developer_reply_date_and_time", texto_iso_para_data_hora("developer_reply_date_and_time"))
    .withColumn("review_last_update_date_and_time", texto_iso_para_data_hora("review_last_update_date_and_time"))
    .withColumn("review_submit_date_and_time", texto_iso_para_data_hora("review_submit_date_and_time"))
)
atualizada = F.col("review_last_update_date_and_time")
resenhas = (
    resenhas
    .withColumn("dia_da_semana_da_resenha", tb.dia_semana(atualizada).cast("bigint"))
    .withColumn("hora_da_resenha", F.hour(atualizada).cast("bigint"))
)
dia_r, hora_r = F.col("dia_da_semana_da_resenha"), F.col("hora_da_resenha")
resenhas = resenhas.withColumn(
    "inicio_da_contagem_sla",
    F.when(((dia_r == 7) & (hora_r >= 3)) | (dia_r == 1),
           tb.fazer_data_hora(tb.somar_dias(atualizada, F.when(dia_r == 7, 2).otherwise(1)), 8))
     .when(dia_r.between(2, 6) & (hora_r >= 3) & (hora_r < 8), tb.fazer_data_hora(atualizada, 8))
     .otherwise(atualizada))
inicio_r = F.col("inicio_da_contagem_sla")
sem_texto = F.col("review_text").isNull() | (F.col("review_text") == "")
resenhas = (
    resenhas
    .withColumn("elegibilidade_sla", F.when(sem_texto, "Não Aplicável").otherwise("Aplicável"))
    .withColumn("prazo_sla", tb.somar_dias(inicio_r, F.floor((tb.dia_semana(inicio_r) - 1) / 5) * 2 + 1))
)
resposta_loja, prazo_loja = F.col("developer_reply_date_and_time"), F.col("prazo_sla")
resenhas = (
    resenhas
    .withColumn("status_sla",
                F.when(F.col("elegibilidade_sla") == "Não Aplicável", "Não Aplicável")
                 .when(resposta_loja.isNotNull() & (resposta_loja <= prazo_loja), DENTRO)
                 .when((resposta_loja > prazo_loja) | (resposta_loja.isNull() & (prazo_loja < tb.agora())), FORA)
                 .otherwise("Pendente"))
    .withColumn("data", atualizada)
    .withColumn("status_resposta",
                F.when(sem_texto, "Evaluación sin Comentarios")
                 .when(F.col("developer_reply_text").isNull() | (F.col("developer_reply_text") == ""), "Comentario sin respuesta")
                 .otherwise("Comentario Respondido"))
)
gravar(resenhas, "resenhas", "Gold Daily Hispana: avaliações das lojas de apps com SLA (extract Resenhas OIS)")

# COMMAND ----------

# MAGIC %md ## Bases de origem – [1] [3] [4] [7] [8] [9] [11] [12] [14] [16] [20] a [29]

# COMMAND ----------

# Em BASE MTK há "Status de Finalização" (do sistema) e "Status de finalização" (do atendimento): no Prep são colunas
# diferentes. A leitura da bronze dá _2 à segunda; o nome sem sufixo fica com a do atendimento, como nas demais planilhas.
# A função e a classificação aparecem duas vezes com o mesmo título; a segunda é a "1" do Prep.
def base_mtk(tabela):
    return (silver(tabela)
            .withColumnRenamed("status_de_finalizacao", "status_de_finalizacao_sistema")
            .withColumnRenamed("status_de_finalizacao_2", "status_de_finalizacao")
            .withColumnRenamed("funcao_do_sistema_2", "funcao_do_sistema_1")
            .withColumnRenamed("status_de_classificacao_2", "status_de_classificacao_1"))


fora_16_17 = lambda coluna: ~F.coalesce(F.to_date(coluna).isin(*DIAS_16_17), F.lit(False))
mtk = base_mtk("base_mtk")
mtk_historico = base_mtk("base_mtk_historico")
novo_analitico = silver("analitico")

# [24] [25] [29] [39] [47] [53] [28] [59]
mtk_sem_16_17 = mtk.where(fora_16_17("data_contato") & excluir("status_de_finalizacao", "PROTOCOLO"))
historico_analitico = (
    uniao(mtk_sem_16_17, mtk_historico)
    .withColumn("funcao_do_sistema", F.coalesce("funcao_do_sistema_1", "funcao_do_sistema"))
    .withColumn("status_de_classificacao", F.coalesce("status_de_classificacao_1", "status_de_classificacao"))
)
analitico = uniao(historico_analitico, novo_analitico).withColumn("cant_de_atendimientos", F.coalesce("cant_de_atendimientos", F.lit(1)))

# [62] [64] [65] [67] [69]
analitico = analitico.where(excluir("status_de_classificacao_1", *R.CLASSIFICACAO_N2_N3))
analitico_inteiro = analitico  # [66] sem os filtros seguintes: usado no join com o Completo
analitico = (
    analitico.where(excluir("status_de_classificacao_1", *R.CLASSIFICACAO_EXCLUIDA))
    .where(excluir("status_de_finalizacao", *R.FINALIZACAO_EXCLUIDA))
)

# [71]
espera = F.col("primeiro_tempo_de_espera_segundos")
tipo = F.col("tipo")
analitico = (
    analitico
    .withColumn("primeiro_tempo_de_espera_segundos", segundos_hms("primeiro_tempo_de_espera"))
    .withColumn("tipo", por_setor("setor_fim", R.TIPO_ANALITICO))
    .withColumn("sla", F.when(igual(tipo, "Email") & (espera >= 0) & (espera < 3600), DENTRO)
                        .when(igual(tipo, "Email") & (espera >= 3600), FORA)
                        .when(igual(tipo, "WhatsApp") & (espera >= 0) & (espera <= 600), DENTRO)
                        .when(igual(tipo, "WhatsApp") & (espera > 600), FORA)
                        .otherwise(DENTRO))
    .withColumn("tempo_de_operacao_segundos", segundos_hms("tempo_de_operacao"))
    .withColumn("pais", por_setor("setor_fim", R.PAIS_ANALITICO))
)
pais = F.col("pais")
analitico = (
    analitico
    .withColumn("data_contato_fuso", F.when(igual(pais, "Chile"), somar_horas("data_contato", -1))
                                      .when(igual(pais, "Colombia", "Peru", "Ecuador"), somar_horas("data_contato", -2))
                                      .when(igual(pais, "Mexico"), somar_horas("data_contato", -3))
                                      .otherwise(F.col("data_contato")))
    .withColumn("nivel", nivel("data_contato", "status_de_finalizacao", R.NIVEL_ANALITICO))
    .withColumn("primeiro_contato",
                F.when(igual("status_de_finalizacao", "AJUSTE/ CORRECCION REALIZADO POR PLCOM", "DIRECCIONADO - PLCOM",
                             "DIRECCIONADO - TD LOCAL", "INCIDENTE CRÍTICO", "INCIDENTE CRITICO", "INCIDENTE CRÃTICO",
                             "LLAMADO ABIERTO PARA N2", "PLCOM-PENDIENTE DE RESPUESTA", "REAPERTURA DE LLAMADO"),
                       "Não Resolvido no 1° Contato").otherwise("Resolvido no 1° Contato"))
    .drop("data_contato")
    .withColumn("fonte", F.lit("MKT Zap"))
)

# [4] [22] [34] Registro de Grupos no formato do analítico
registro = (
    silver("registro_de_grupos")
    .withColumnRenamed("fecha_del_contacto", "data_contato_fuso").withColumnRenamed("id", "protocolo")
    .withColumnRenamed("analista", "responsavel").withColumnRenamed("grupo_de_whatsapp", "origem")
    .withColumnRenamed("pais_afectado", "pais")
    .withColumn("pais", remapear("pais", {"Chile": ["CHILE"], "Colombia": ["COLOMBIA"], "Mexico": ["MEXICO"], "Peru": ["PERU"]}))
    .withColumnRenamed("usuario_afectado", "codigo_cn").withColumnRenamed("solucion_aplicada", "solucao_aplicada")
    .withColumnRenamed("pedido_finalizado", "pedidos_finalizados").withColumnRenamed("status_de_finalizacion", "status_de_finalizacao")
    .withColumnRenamed("plataforma", "status_de_classificacao").withColumnRenamed("funcion_del_sistema", "funcao_do_sistema")
    .withColumn("nivel", nivel("data_contato_fuso", "status_de_finalizacao", R.NIVEL_REGISTRO_GRUPOS))
    .where(excluir("status_de_finalizacao", "VALIDACION DE LLAMADO"))
    .withColumn("fonte", F.lit("Registro de Grupos"))
)

# [9] [2] [26] [37] [46] Tickets com a função do sistema do analítico
tickets = (
    silver("tickets")
    .withColumn("pedidos_finalizados", remapear("pedidos_finalizados", {"SI": ["si"], "NO": ["no"], "": ["no_se_aplica"]}))
)
tickets = juntar(tickets, silver("auxiliar").drop("coluna_1"), [("funcao_do_sistema", "funcao_do_sistema_ticket")], "left")
tickets = (
    remover(tickets, "funcao_do_sistema", "funcao_do_sistema_ticket")
    .withColumnRenamed("funcao_do_sistema_analitico", "funcao_do_sistema")
    .withColumnRenamed("usuario_responsavel", "responsavel").withColumnRenamed("id_do_ticket", "protocolo")
    .withColumnRenamed("setor_do_atendimento", "setor_fim")
    .withColumn("data_contato_fuso", F.col("data_de_criacao_do_ticket"))
    .withColumn("tipo", por_setor("setor_fim", R.TIPO_TICKETS))
    .withColumn("pais", por_setor("setor_fim", R.PAIS_TICKETS))
    .withColumn("nivel", nivel("data_contato_fuso", "status_de_finalizacao", R.NIVEL_TICKETS))
)
tickets_whats = tickets.where(manter("tipo", "WhatsApp"))
tickets_email = tickets.where(manter("tipo", "Email"))

# COMMAND ----------

# MAGIC %md ## MKT Hispana Completo – [20] [24] [36] [45] [50] [56] [57] [70] [72] [74] [78] [80] [82]

# COMMAND ----------

# Nos dias 16 e 17/03/2026 os atendimentos vêm da BASE MTK Historico, no formato do Completo
historico_completo = (
    mtk_historico.where(filtro_data("data_contato", de="2026-03-01"))
    .select(F.col("protocolo").alias("protocol"), F.col("setor_fim").alias("setor"), F.col("canal_de_entrada").alias("canal"),
            F.col("data_contato").alias("data_criacao"), F.col("encerrado_em").alias("data_conclusao"),
            F.col("responsavel").alias("operador"), F.col("status_de_finalizacao").alias("status"))
)
completo = (
    uniao(silver("completo").where(fora_16_17("data_criacao")), historico_completo)
    .where(excluir("status", "PROTOCOLO"))
    .withColumn("regra_status", F.when(igual("status", *R.STATUS_INELEGIVEIS), "Excluir").otherwise("Manter"))
    .where(F.col("regra_status") != "Excluir")
    .withColumnRenamed("setor", "setor_fim")
    .withColumn("tipo", por_setor("setor_fim", R.TIPO_COMPLETO))
    .where(excluir("setor_fim", "CL-CELULAR") & excluir("tipo", "Remover"))
    .withColumn("pais", por_setor("setor_fim", R.PAIS_COMPLETO))
    .withColumnRenamed("setor_fim", "setor")
    .withColumn("tempo_segundos", tb.diff_segundos(F.col("data_criacao"), F.col("data_conclusao")))
)
# [68] [70] [72] Quantidade, responsável e status vêm do analítico pelo protocolo
do_analitico = analitico_inteiro.select("protocolo", "cant_de_atendimientos", "responsavel", "status_de_finalizacao")
completo = remover(juntar(do_analitico, completo, [("protocolo", "protocol")], "right"), "protocolo")
# [74]
status_ou_final = F.coalesce("status", "status_de_finalizacao")
ate_setembro, atual = R.NIVEL_COMPLETO
completo = (
    completo
    .withColumn("nivel", F.when(F.col("data_conclusao") < OUTUBRO_2026, caso_nivel(status_ou_final, ate_setembro))
                          .otherwise(caso_nivel(status_ou_final, atual)))
    .withColumn("valor_atendimento", F.coalesce("cant_de_atendimientos", F.lit(1)).cast("bigint"))
    .drop("cant_de_atendimientos")
    .withColumn("origem_da_linha", F.lit("MKT Completo"))
)
# [57] Tickets de e-mail no formato do Completo
tickets_email_completo = (
    remover(tickets_email, "data_de_criacao_do_atendimento", "funcao_do_sistema", "status_de_classificacao", "data_contato_fuso",
            "protocolo_do_atendimento_convertido", "data_de_conversao_do_atendimento", "codigo_cn", "pedidos_finalizados",
            "llamado", "observacoes")
    .withColumnRenamed("protocolo", "protocol").withColumnRenamed("setor_fim", "setor")
    .withColumnRenamed("data_de_criacao_do_ticket", "data_criacao").withColumnRenamed("data_de_finalizacao", "data_conclusao")
    .withColumnRenamed("cant_de_atendimientos", "valor_atendimento").withColumnRenamed("estado", "situacao")
)
# [78] [80]
completo_final = uniao(tickets_email_completo, completo).withColumn("origem_da_linha", F.coalesce("origem_da_linha", F.lit("MKT Completo")))
gravar(completo_final, "completo", "Gold Daily Hispana: atendimentos concluídos e tickets de e-mail (extract MKT Hispana Completo)")
completo_final = spark.table(f"{CATALOGO}.{SCHEMA}.dexp_gold_hispana_completo")

# COMMAND ----------

# MAGIC %md ## Base MKT – [75] [79] [81] [84] [86] [88] [90] [92] [93] a [97]

# COMMAND ----------

# [73] [75] [79] [81]
base = (
    uniao(analitico, registro, tickets_whats)
    .withColumn("fonte_dos_dados", F.coalesce("fonte", F.lit("Tickets")))
    .withColumn("fonte", F.coalesce("fonte", F.lit("MKT Zap")))
    .where(excluir("status_de_finalizacao", "CADASTRO DUPLICADO", "CAMBIO DE EMAIL VOL", "CERRADO DESPUÃ‰S DE HORAS",
                   "CERRADO DESPUÉS DE HORAS", "CONSULTA CON PLCOM", "AJUSTE/ CORRECCION REALIZADO POR PLCOM", "VALIDACION PLCOM",
                   "INCIDENTE RESUELTO", "PLCOM - CLASSIFICAÇÃO", "PLCOM-PENDIENTE DE RESPUESTA", "INCIDENTE EN ANDAMIENTO"))
)
# [84]
solucao = F.col("solucao_aplicada")
base = (
    remover(base, "status_de_finalizacao_sistema", "empresa", "nome", "cpf_cnpj", "numero_do_contrato", "valor_do_contrato", "origem", "alinewel",
            "status_de_classificacao_1", "funcao_do_sistema_1", "detalhe_do_sistema", "campos_adicionais_web_chat")
    .withColumn("solucao_aplicada", F.when(solucao.between(1, 25), solucao).otherwise(1).cast("bigint"))
    .withColumn("funcao_do_sistema", F.regexp_replace(F.regexp_replace("funcao_do_sistema", " - CLASSIFICAÇÃO", ""), " - CLASSIFICAÃ‡ÃƒO", ""))
    .withColumnRenamed("data_contato_fuso", "data_contato")
    .withColumn("hora", F.hour("data_contato").cast("bigint"))
    .withColumn("semana", semana("data_contato").cast("bigint"))
    .where(excluir("tipo", "Remover"))
    .where(excluir(F.concat("status_de_finalizacao", "primeiro_tempo_de_espera"),
                   "VALIDACION DE LLAMADONão atendido", "VALIDACION DE LLAMADONÃ£o atendido"))
    .withColumn("tipo", F.when(igual("fonte", "MKT Zap") & igual("tipo", "Email"), "Email")
                         .when(igual("fonte", "MKT Zap") & igual("tipo", "WhatsApp"), "WhatsApp")
                         .when(igual("fonte", "Registro de Grupos"), "Requisições"))
    .withColumn("tempo_medio_segundos", tb.diff_segundos(F.col("data_contato"), F.col("encerrado_em")))
)
tempo_medio = F.col("tempo_medio_segundos")
base = base.withColumn("email_1_hora", F.when(tempo_medio.between(0, 3600), "Dentro de 1 Hora")
                                        .when(tempo_medio > 3600, "Acima de 1 Hora").otherwise("Backlog"))


# [86] Horário útil do Hispana: fim de semana e madrugada (3h às 7h59) vão para as 8h seguintes
def ajustada(coluna):
    c = F.col(coluna)
    dia = tb.dia_semana(c)
    return (F.when(dia == 1, tb.fazer_data_hora(tb.somar_dias(c, 1), 8))
             .when(dia == 7, F.when(F.hour(c) < 3, c).otherwise(tb.fazer_data_hora(tb.somar_dias(c, 2), 8)))
             .when((F.hour(c) >= 3) & (F.hour(c) < 8), tb.fazer_data_hora(c, 8))
             .otherwise(c))


base = base.withColumn("data_contato_ajustada", ajustada("data_contato")).withColumn("encerrado_em_ajustado", ajustada("encerrado_em"))
ini, fim = F.col("data_contato_ajustada"), F.col("encerrado_em_ajustado")
ini_v, fim_v = (ini.cast("long") - 10800).cast("timestamp"), (fim.cast("long") - 10800).cast("timestamp")
dia_ini_v, dia_fim_v = F.date_trunc("day", ini_v), F.date_trunc("day", fim_v)
meio = tb.diff_dias(tb.somar_dias(dia_ini_v, 1), dia_fim_v)
base = base.withColumn(
    "segundos_uteis",
    F.when(dia_ini_v == dia_fim_v, tb.diff_segundos(ini, fim))
     .otherwise((meio - F.floor(meio / 7) * 2) * 68400
                + tb.diff_segundos(ini, tb.fazer_data_hora(tb.somar_dias(ini_v, 1), 3))
                + tb.diff_segundos(tb.fazer_data_hora(fim_v, 8), fim)))
prazo_aberto = (F.when(tb.dia_semana(ini).isin(6, 7), tb.somar_dias(ini, 3)).otherwise(tb.somar_dias(ini, 1)))
base = base.withColumn(
    "status_sla_email",
    F.when(F.col("encerrado_em").isNotNull(), F.when(F.col("segundos_uteis") <= 68400, DENTRO).otherwise(FORA))
     .otherwise(F.when(tb.agora() <= prazo_aberto, DENTRO).otherwise(FORA)))

# [88] [90] [92] O "Pais" que fica depois do join [92] é o da planilha de ticket médio, como no Prep
base = remover(juntar(base, silver("exento"), [("protocolo", "protocolo")], "left"), "pais_1")
ticket_pais = silver("ticket_medio_pais").select("pais", "valor_por_pedido")
base = remover(juntar(ticket_pais, base, [("pais", "pais")], "right"), "pais_1", "protocolo_1", "justificacion", "autorizado_por_natura")

# [93] [94] [95]
tipo = F.col("tipo")
data_contato = F.col("data_contato")
base = (
    base
    .withColumn("sla_com_expurgo", F.when(igual("exento", "Sim"), DENTRO).otherwise(F.col("sla")))
    .withColumn("status_de_classificacao", F.regexp_replace(F.regexp_replace("status_de_classificacao", " - CLASSIFICAÃ‡ÃƒO", " - CLASSIFICAÇÃO"), " - CLASSIFICAÇÃO", ""))
    .withColumn("data_para_vinculo", F.date_trunc("month", data_contato))
    .withColumn("cant_de_atendimientos", F.col("cant_de_atendimientos").cast("bigint"))
    .withColumn("valor_atendimento",
                F.when(data_contato >= MARCO_2026, F.when(igual(tipo, "Requisições"), F.col("solucao_aplicada")).otherwise(F.col("cant_de_atendimientos")))
                 .otherwise(F.col("solucao_aplicada")))
    .withColumn("origem_da_linha", F.lit("MKT Analítico"))
    .withColumn("data_hibrida_do_dashboard", data_contato)
    .withColumn("data_criacao", data_contato)
    .withColumn("data_conclusao", F.col("encerrado_em"))
    .withColumn("valor_atendimento", F.coalesce("valor_atendimento", F.lit(1)))
)

# COMMAND ----------

# [40] [58] [61] [63] [85] [87] [89] [91] Concluídos do Completo com a função e a classificação do analítico
consolidado_historico = (
    uniao(novo_analitico, mtk)
    .withColumn("status_de_classificacao", F.coalesce("status_de_classificacao_1", "status_de_classificacao"))
    .withColumn("funcao_do_sistema", F.coalesce("funcao_do_sistema_1", "funcao_do_sistema"))
    .select(F.col("protocolo").alias("protocolo_analitico"), "status_de_classificacao", "funcao_do_sistema")
)
classificacao = uniao(consolidado_historico, tickets_email.select(F.col("protocolo").alias("protocolo_analitico"), "funcao_do_sistema", "status_de_classificacao"))
concluidos = (
    remover(completo_final.withColumn("data_hibrida_do_dashboard", F.col("data_conclusao")).where(excluir("situacao", "Em aberto")),
            "status_de_finalizacao", "tempo_segundos", "nome", "atendimentos_first_message_at", "inicio_atendimento", "atendido",
            "ultima_mensagem", "tipo_canal", "telefone", "regra_status", "situacao", "tempo_medio_ate_ser_atendidos",
            "tempo_medio_primeira_espera", "tempo_medio_atendimento", "tempo_medio_espera", "tempo_medio_operacional")
    .withColumnRenamed("protocol", "protocolo").withColumnRenamed("status", "status_de_finalizacao")
    .withColumnRenamed("canal", "canal_de_entrada").withColumnRenamed("setor", "setor_fim")
    .withColumn("responsavel", F.coalesce("operador", "responsavel")).drop("operador")
    .where(excluir("pais", "Latam"))
    .where(excluir("tipo", "WhatsApp"))
    .withColumn("data_contato", F.col("data_conclusao"))
)
concluidos = juntar(classificacao, concluidos, [("protocolo_analitico", "protocolo")], "right")
concluidos = concluidos.withColumn("status_de_classificacao", F.regexp_replace("status_de_classificacao", " - CLASSIFICAÇÃO", ""))

# [96] [97]
tudo = (
    uniao(concluidos, base)
    .withColumn("cant_de_atendimientos", F.coalesce("cant_de_atendimientos", F.lit(1)))
    .withColumn("fonte", F.coalesce("fonte", F.lit("MKT Completo")))
    .withColumn("fonte_dos_dados", F.coalesce("fonte_dos_dados", F.lit("MKT Zap")))
)
tudo.write.mode("overwrite").option("overwriteSchema", "true").saveAsTable(f"{CATALOGO}.{SCHEMA}.dexp_gold_hispana_tmp_base")
tudo = spark.table(f"{CATALOGO}.{SCHEMA}.dexp_gold_hispana_tmp_base")

# [98] [101] Healthcheck
hc = (
    tudo.where(manter("status_de_finalizacao", "HEALTHCHECK")).where(excluir("pais", "Latam"))
    .withColumn("valor_atendimento", F.when(F.col("data_contato") >= MARCO_2026, F.col("cant_de_atendimientos")).otherwise(F.col("solucao_aplicada")))
    .transform(corrigir_funcao_equador)
)
gravar(hc, "base_mkt_hc", "Gold Daily Hispana: atendimentos de Healthcheck (extract Base MKT HC OIS)")

# [99] [102] [106]
base_mkt = (
    tudo.where(excluir("funcao_do_sistema", "HEALTHCHECK") & excluir("status_de_finalizacao", "HEALTHCHECK") & excluir("pais", "Latam"))
    # o remapeamento do Prep também põe os vazios em "Vacio"
    .withColumn("responsavel", F.coalesce(remapear("responsavel", R.RESPONSAVEL_BASE), F.lit("Vacio")))
    .withColumn("pedidos_finalizados", remapear("pedidos_finalizados", {"NO": ["No", "No Aplica", "NO SE APLICA"]}))
    .transform(corrigir_funcao_equador)
)
gravar(base_mkt, "base_mkt", "Gold Daily Hispana: atendimentos sem Healthcheck (extract Base MKT OIS)")
base_mkt = spark.table(f"{CATALOGO}.{SCHEMA}.dexp_gold_hispana_base_mkt")

# [100] [103]
lojas_mkt = (
    tudo.where(igual("setor_fim", "APP NATURA", "APP NATURA LATAM", "MI NEGOCIO", "APP AVON"))
    .withColumn("setor_fim", remapear("setor_fim", {"APP NATURA": ["APP NATURA LATAM"]}))
    .transform(corrigir_funcao_equador)
)
gravar(lojas_mkt, "base_mkt_lojas", "Gold Daily Hispana: e-mails de lojas (extract Base MKT Lojas OIS)")
lojas_mkt = spark.table(f"{CATALOGO}.{SCHEMA}.dexp_gold_hispana_base_mkt_lojas")

# COMMAND ----------

# MAGIC %md ## Produtividade – [44] [104] [107] a [114]

# COMMAND ----------

COLUNAS_PRODUTIVIDADE = ["fonte", "funcao_do_sistema", "tipo", "nivel", "origem_da_linha", "status_de_classificacao", "saida", "protocolo",
                         "setor_fim", "status_de_finalizacao", "data_contato", "responsavel", "valor_atendimento", "encerrado_em", "pais"]
mkt = (
    uniao(lojas_mkt.withColumn("saida", F.lit("Emails de Loja")), base_mkt.withColumn("saida", F.lit("Base MKT OIS")))
    .select(*COLUNAS_PRODUTIVIDADE)
    .withColumn("fonte", F.coalesce("fonte", F.lit("MKT Completo")))
    .where(~F.coalesce(igual("tipo", "Email") & igual("origem_da_linha", "MKT Analítico") & (F.col("data_contato") >= MARCO_2026), F.lit(False)))
    .where(excluir("nivel", "Não considerar"))
    .withColumnRenamed("data_contato", "data")
)
resenhas_equipe = resenhas_appsheets.select(
    F.col("id").alias("protocolo"), "pais", F.col("responsable_de_la_respuesta").alias("responsavel"),
    F.col("fecha_de_la_respuesta_exp").alias("data"), F.lit(1).cast("bigint").alias("valor_atendimento"))
produtividade = uniao(mkt, resenhas_equipe)
for coluna in ["fonte", "tipo", "origem_da_linha", "saida"]:
    produtividade = produtividade.withColumn(coluna, F.coalesce(coluna, F.lit("Resenhas")))
produtividade = produtividade.withColumn("responsavel", remapear("responsavel", R.RESPONSAVEL_PRODUTIVIDADE))
gravar(produtividade, "produtividade", "Gold Daily Hispana: atendimentos e resenhas por responsável (extract Experiencia Hispana Produtividade)")
spark.sql(f"DROP TABLE IF EXISTS {CATALOGO}.{SCHEMA}.dexp_gold_hispana_tmp_base")
