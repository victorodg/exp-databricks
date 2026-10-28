# Databricks notebook source
# MAGIC %md
# MAGIC # Gold – MKT
# MAGIC
# MAGIC Reproduz o fluxo Tableau Prep **"Daily - Experiencia BR - MKT"**. Os números entre colchetes, como `[97]`, são as
# MAGIC etapas de `docs/fluxos/mkt.md`. As colunas usam o nome do Prep em snake_case; quando o Prep cria nomes repetidos
# MAGIC num join ("CHAMADO-1"), aqui eles viram `chamado_1` (ver `dexp.prep.juntar`).
# MAGIC
# MAGIC Lê a saída `dexp_gold_dynamics_nivel` e `dexp_gold_resenhas_appsheets`, por isso roda depois da gold do Dynamics.

# COMMAND ----------

import os
import re
import sys

from pyspark.sql import functions as F

sys.path.append(os.path.abspath(".."))
from dexp import regras_mkt as R
from dexp import tableau as tb
from dexp.prep import juntar, remover, uniao
from dexp.regras_mkt_comuns import (DENTRO, FORA, mes_ano, nivel, para_horario_util, segundos_hms, segundos_uteis,
                                    sla, tempo_formatado)
from dexp.tableau import excluir, filtro_data, igual, manter, remapear

dbutils.widgets.text("catalog", "sandbox")
dbutils.widgets.text("schema", "sustentacao_bau_experiencias")
CATALOGO = dbutils.widgets.get("catalog")
SCHEMA = dbutils.widgets.get("schema")
VOLUME = f"/Volumes/{CATALOGO}/{SCHEMA}/dexp_landing"
tb.preparar_sessao(spark)


def silver(tabela):
    return spark.table(f"{CATALOGO}.{SCHEMA}.dexp_silver_{tabela}").drop("_versao", "_origem")


def gold(tabela):
    return spark.table(f"{CATALOGO}.{SCHEMA}.dexp_gold_{tabela}")


def gravar(df, tabela, descricao):
    nome = f"{CATALOGO}.{SCHEMA}.dexp_gold_mkt_{tabela}"
    df.write.mode("overwrite").option("overwriteSchema", "true").saveAsTable(nome)
    spark.sql(f"COMMENT ON TABLE {nome} IS '{descricao}'")
    print(f"dexp_gold_mkt_{tabela:30} {spark.table(nome).count():>9,} linhas")
    return spark.table(nome)


NULO_TEXTO = F.lit(None).cast("string")
COLUNA = lambda nome: F.col(f"`{nome}`")

# COMMAND ----------

# MAGIC %md ## Saídas independentes: HC, Dynatrace e Requisição Eventual

# COMMAND ----------

# [5] [26] [44] Alguns ciclos estão gravados como data na planilha (exibidos como 06/2025); o Prep lê o texto exibido.
ciclo = F.col("ciclo")
healthcheck = silver("mkt_healthcheck").withColumn(
    "ciclo", F.when(ciclo.rlike(r"^\d{4}-\d{2}-\d{2}"), F.date_format(F.to_date(F.substring(ciclo, 1, 10)), "MM/yyyy"))
              .otherwise(ciclo))
gravar(healthcheck, "hc_exp_brasil", "Gold Daily Experiência BR: Healthcheck (extract HC Exp Brasil)")

# [15] [21] [36] [41] [49] [55]. A planilha até julho tem "Hora Fim do Atendimento" (texto) e "Erro Perceptível ao
# Usuário?" com grafia diferente das colunas da planilha atual; o Prep mantém as duas grafias separadas.
dynatrace = silver("mkt_dynatrace")
dynatrace_ate_julho = (
    remover(silver("mkt_dynatrace_ate_julho"), "mes", "monitoracao", "sistema", "hora_do_alarme",
            "data_e_hora_inicio_do_atendimento")
    .withColumnRenamed("sist_operacional", "sistema_operacional")
    .withColumnRenamed("hora_fim_do_atendimento", "hora_fim_do_atendimento_ate_julho")
    .withColumnRenamed("erro_perceptivel_ao_usuario", "erro_perceptivel_ao_usuario_ate_julho")
    .withColumn("data", F.col("data").cast("timestamp"))
)
gravar(uniao(dynatrace, dynatrace_ate_julho).where(F.col("data").isNotNull() & F.col("conseguiu_contato").isNotNull()),
       "exp_brasil_dynatrace", "Gold Daily Experiência BR: monitoração Dynatrace (extract Exp Brasil Dynatrace)")

# [22] [42] Registros do AppSheets com Nível (usados na Requisição Eventual e no RE do WhatsApp)
chamado_n2 = F.upper(F.col("n_do_chamado_n2"))
appsheets = silver("mkt_appsheets_registros").withColumn(
    "nivel",
    F.when(chamado_n2.contains("INC") | chamado_n2.contains("REQ") | chamado_n2.contains("RITM"), "N2")
     .otherwise(nivel("status_de_finalizacao", "data", R.NIVEL_REGRA_NOVA_COMPLETA)))

# [51] [27] [59]
qtde = F.col("qtde_de_atendimentos")
requisicao = (
    appsheets.where(manter("canal_de_entrada", "Requisição Eventual"))
    .withColumn("data_de_finalizacao", tb.data_hora(F.col("data_de_finalizacao")))
    .withColumn("qtde_de_atendimentos", F.when(qtde.isNull(), F.lit(1)).otherwise(tb.inteiro("qtde_de_atendimentos")))
)
gravar(juntar(silver("mkt_tribos"), requisicao, [("funcao_do_sistema", "assunto_funcao_do_sistema")], "right"),
       "requisicao_eventual", "Gold Daily Experiência BR: requisições eventuais do AppSheets com tribo (extract Requisição Eventual EXP BR)")

# [50] [56] [57] [58] Registros "RE" do AppSheets no formato do WhatsApp. O "Mercado" do AppSheets e o "MERCADO" do
# analítico são colunas diferentes no Prep; aqui o do AppSheets fica como mercado_re.
sem_id = F.col("id").isNull()
re_appsheets = (
    appsheets.where(manter("canal_de_entrada", "RE"))
    .select("nivel", F.when(sem_id, "").otherwise("RE").alias("setor_fim"),
            F.when(sem_id, "").otherwise("Protocolo-RE").alias("protocolo"), F.col("data").alias("data_contato"),
            F.col("mercado").alias("mercado_re"))
    .withColumn("sla_do_primeiro_contato", F.when(F.col("protocolo").isNull(), "").otherwise(DENTRO))
    .withColumn("qtd_atendimentos", F.when(F.col("protocolo").isNull(), F.lit(None)).otherwise(1).cast("bigint"))
)
re_ate_set25 = re_appsheets.where(filtro_data("data_contato", ate="2025-09-30"))
re_franquias = (re_appsheets.where(F.col("data_contato").isNull() | (F.col("data_contato") >= F.to_timestamp(F.lit("2025-10-01"))))
                .where(manter("mercado_re", "EMPRESARIAS")))
re_a_partir_out25 = (re_appsheets.where(filtro_data("data_contato", de="2025-10-01"))
                     .where(excluir("mercado_re", "EMPRESARIAS") & F.col("mercado_re").isNotNull()))

# COMMAND ----------

# MAGIC %md ## Base analítica: MKT_Reativos + histórico + AppSheets + Tickets – [18] a [97]

# COMMAND ----------

# [18] [38] [1] [48] [54]
dias_16_17 = [F.lit("2026-03-16").cast("date"), F.lit("2026-03-17").cast("date")]
reativos = silver("mkt_reativos")
mkt = (uniao(reativos.where(~F.coalesce(F.to_date("data_contato").isin(*dias_16_17), F.lit(False))),
             silver("mkt_reativos_historico_ate_out25"))
       .withColumn("origem", F.lit("MKT")).withColumn("protocolo_relacionado", F.lit("")))

# [23] [43] Registros de Acionamentos no formato do analítico
canal = F.col("canal_de_entrada")
acionamentos = (
    silver("mkt_registros_de_acionamentos")
    .withColumnRenamed("protocolo", "protocolo_relacionado").withColumnRenamed("id", "protocolo")
    .withColumn("data_contato", F.col("data_do_contato").cast("timestamp")).drop("data_do_contato")
    .withColumnRenamed("analista", "responsavel").withColumnRenamed("codigo_do_impactado", "codigo")
    .withColumnRenamed("qtde_de_atendimentos", "qtd_atendimentos")
    .withColumnRenamed("status_de_organizacao", "status_de_classificacao")
    .withColumn("origem", F.lit("AppSheets"))
    .withColumn("setor_fim", F.when(igual(canal, "E-mail - EXPCB (Gerentes)"), "E-mail - Experiência CB")
                              .when(igual(canal, "TD -  GV Antecipada", "TD - GV Antecipada"), "TD -  GV Antecipada")
                              .when(igual(canal, "Whats Franquia"), "Whats Franquias")
                              .when(igual(canal, "Whats GN"), "Whats GN")
                              .when(igual(canal, "Whats GV"), "Whats GV")
                              .otherwise(canal))
    .withColumn("setor_entrada", canal)
    .withColumn("canal_de_entrada", remapear(canal, {
        "E-mail - Experiência CB": ["E-mail - EXPCB (Gerentes)"],
        "Whatsapp Enterprise - Natura CN": ["TD -  GV Antecipada", "Whats Franquia", "TD - GV Antecipada", "Whats GV", "Whats GN"]}))
)
analitico = uniao(acionamentos, mkt)  # [61]

# [2] [11] [32] [45] [53] [60] Tickets Brasil com a função do sistema do analítico
tickets = juntar(silver("mkt_auxiliar_brasil"), silver("mkt_tickets_brasil"),
                 [("funcao_do_sistema_tickets", "funcao_do_sistema")], "right")
qtd = F.col("qtd_atendimentos")
setor_atendimento = F.col("setor_do_atendimento")
tickets = (
    remover(tickets, "funcao_do_sistema", "funcao_do_sistema_tickets")
    .withColumnRenamed("funcao_do_sistema_analitico", "funcao_do_sistema")
    .withColumn("qtd_atendimentos", F.when(qtd.isNull() | (qtd == 33923426), 1).otherwise(qtd))
    .withColumn("tipo", F.when(igual(setor_atendimento, "EXPERIÊNCIA CB"), "Email")
                         .when(igual(setor_atendimento, "TD - GV Antecipada", "Whats GN", "Whats Franquia", "Whats GV"), "WhatsApp"))
    .withColumn("data_contato", F.col("data_de_criacao_do_ticket"))
)

# [64] Tickets no formato do analítico do WhatsApp (vale para todos os tickets, inclusive os de e-mail)
tickets_analitico = (
    tickets.withColumnRenamed("setor_do_atendimento", "setor_fim").drop("tipo")
    .withColumnRenamed("id_do_ticket", "protocolo").drop("data_de_criacao_do_atendimento", "estado")
    .withColumnRenamed("data_de_finalizacao", "encerrado_em").withColumnRenamed("usuario_responsavel", "responsavel")
    .withColumn("pedido_finalizado", remapear("pedido_finalizado", {"SIM": ["sim"], "NÃO SE APLICA": ["nao_se_aplica"], "NÃO": ["nao"]}))
    .withColumn("qtd_atendimentos", F.when(qtd.between(1, 100), qtd).otherwise(1))
    .withColumn("esta_em_fechamento", remapear("esta_em_fechamento", {"NÃO": ["nao"], "SIM": ["sim"]}))
    .withColumn("canal_de_entrada", F.lit("Whatsapp Enterprise - Natura CN"))
)

# [66] [68] Função do sistema agrupada (Função do Sistema-1) e Qtd 0 -> 1
analitico = (
    uniao(tickets_analitico, analitico)
    .withColumn("funcao_do_sistema_1", remapear("funcao_do_sistema", R.FUNCAO_MACRO))
    .withColumn("qtd_atendimentos", F.when(qtd == 0, 1).otherwise(qtd))
)
analitico_68 = analitico

# [70] [75] [76] [81] [82] [86] [90] Tribos: até set/2026 por join à esquerda com a aba Base_MKT; a partir de out/2026
# por join à direita com a mesma aba agrupada. Nos dois casos a coluna da tribo que repete o nome vira funcao_do_sistema_2.
analitico = analitico.where(excluir("protocolo", *R.PROTOCOLOS_REMOVIDOS_16_01_26))
corte = F.to_timestamp(F.lit("2026-10-01"))
tribos = silver("mkt_tribos")
tribos_agrupadas = tribos.select("funcao_do_sistema", "macro", "plataforma", "tribo").distinct()
analitico = uniao(
    juntar(analitico.where((F.col("data_contato") < corte) | F.col("data_contato").isNull()), tribos,
           [("funcao_do_sistema", "funcao_do_sistema")], "left"),
    juntar(tribos_agrupadas, analitico.where(F.col("data_contato") >= corte),
           [("funcao_do_sistema", "funcao_do_sistema")], "right"),
)
analitico = remover(analitico, "funcao_do_sistema").withColumnRenamed("funcao_do_sistema_1", "funcao_do_sistema")

# [20] [40] [94] Expurgo autorizado pela gestão
expurgo = (silver("mkt_expurgo").withColumnRenamed("chamado_protocolo", "protocolo")
           .withColumnRenamed("autorizado_gestao_natura", "expurgo"))
analitico = remover(juntar(expurgo, analitico, [("protocolo", "protocolo")], "right"), "protocolo", "referencia", "data")
analitico = analitico.withColumnRenamed("protocolo_1", "protocolo")

# [97] Alterações comuns: filtros, SLAs em horas úteis e tickets a desconsiderar
qtd_para_1 = [v for v in R.QTD_ATENDIMENTOS_PARA_1 if v is not None]
analitico = (
    analitico
    .where(excluir("status_de_classificacao", "HEALTH CHECK - CLASSIFICAÇÃO"))
    .where(excluir("status_de_finalizacao", *R.STATUS_FINALIZACAO_EXCLUIDOS))
    .withColumn("qtd_atendimentos", F.when(qtd.isNull() | qtd.isin(*qtd_para_1), 1).otherwise(qtd))
    .withColumn("status_de_classificacao", F.regexp_replace("status_de_classificacao", re.escape(" - CLASSIFICAÇÃO"), ""))
    .withColumn("tempo_medio_segundos", tb.diff_segundos(F.col("data_contato"), F.col("encerrado_em")))
    .withColumn("data_contato_ajustada", para_horario_util("data_contato"))
    .withColumn("encerrado_em_ajustado", para_horario_util("encerrado_em"))
    .withColumn("segundos_uteis", segundos_uteis("data_contato_ajustada", "encerrado_em_ajustado"))
    .withColumn("sla_5_horas", sla("segundos_uteis", 18000))
    .withColumn("sla_10_horas", sla("segundos_uteis", 36000))
    .withColumn("sla_15_horas", sla("segundos_uteis", 54000))
    .withColumn("sla_24_horas", sla("tempo_medio_segundos", 86400))
    .withColumn("sla_4_dias_uteis", F.when(F.col("segundos_uteis").isNull(), "Em Andamento")
                                     .when(F.col("segundos_uteis") <= 230400, DENTRO).otherwise(FORA))
    .withColumn("desconsiderar_tickets", F.when(F.col("protocolo").startswith("T-"), "Desconsiderar").otherwise("Considerar"))
)
analitico_97 = analitico

# COMMAND ----------

# MAGIC %md ## WhatsApp – [100] a [125], [133] a [151]

# COMMAND ----------

def primeiro_contato_e_nivel(df):
    """[105] [108] SLA do primeiro contato (até 5min59s) e Nível com a regra do WhatsApp."""
    return (df.withColumn("primeiro_tempo_de_espera_segundos", segundos_hms("primeiro_tempo_de_espera"))
              .withColumn("sla_do_primeiro_contato",
                          F.when(igual("expurgo", "Sim"), DENTRO).when(igual("origem", "AppSheets"), NULO_TEXTO)
                           .when(F.col("primeiro_tempo_de_espera_segundos") <= 359, DENTRO).otherwise(FORA))
              .withColumn("nivel", nivel("status_de_finalizacao", "data_contato", R.NIVEL_REGRA_NOVA_WHATSAPP)))


def tempo_whatsapp(df, real=False):
    tempo = tb.diff_segundos(F.col("data_contato"), F.col("encerrado_em"))
    return (df.withColumn("tempo_atendimento_whatsapp", tempo.cast("double") if real else tempo)
              .withColumn("tempo_formatado_whatsapp", tempo_formatado("tempo_atendimento_whatsapp")))


whatsapp = primeiro_contato_e_nivel(
    analitico_97.where(manter("canal_de_entrada", "Whatsapp Enterprise - Natura CN")).where(excluir("setor_fim", "ATIVOS", "Triagem")))

# [111] [120]
whats_gn = remover(tempo_whatsapp(whatsapp, real=True).where(manter("setor_fim", "Whats GN")), "testelis")
gravar(whats_gn, "whats_gn", "Gold Daily Experiência BR: WhatsApp GN (extract MKT Whats GN)")

# [112] [122]
whats_gv_antecipada = (
    whatsapp.where(manter("setor_fim", "Atend. -  GV Antecipada", "TD -  GV Antecipada"))
    .withColumn("tipo_setor", F.when(igual("setor_fim", "Atend. -  GV Antecipada"), "Atendimento")
                               .when(igual("setor_fim", "TD -  GV Antecipada"), "TD"))
    .where(manter("setor_fim", "TD -  GV Antecipada"))
)
gravar(whats_gv_antecipada, "whats_gv_antecipada", "Gold Daily Experiência BR: WhatsApp GV Antecipada (extract MKT Whats GV Antecipada)")

# [114] [125] [134]
whats_franquia = uniao(tempo_whatsapp(whatsapp.where(manter("setor_fim", "Whats Franquia"))), re_franquias)
gravar(whats_franquia, "whats_franquia", "Gold Daily Experiência BR: WhatsApp Franquia (extract MKT Whats Franquia)")

# [113] [124] [132]
whats_gv = tempo_whatsapp(uniao(re_a_partir_out25, re_ate_set25, whatsapp)
                          .where(F.coalesce(igual("setor_fim", "Whats GV", "RE"), F.lit(False))))
gravar(whats_gv, "whats_gv", "Gold Daily Experiência BR: WhatsApp GV com registros RE (extract MKT Whats GV)")

# COMMAND ----------

# MAGIC %md ## E-mail – [101] [106] [107] [115] a [117] [126] a [128] [136] [139]

# COMMAND ----------

email = analitico_97
for classificacao in ["N2 - CB COM - Em acomp TD", "N2 - E.mail - EM ACOMPANHAMENTO - TD", "N2 - WhatsApp - EM ACOMPANHAMENTO - TD",
                      "N3 - CB COM - Pendentes - JIRA", "N3 - WhatsAPP - Pendentes - JIRA"]:
    email = email.where(excluir("status_de_classificacao", classificacao))
tempo_operacao = F.col("tempo_operacao_em_segundos")
email = (
    email.withColumn("tempo_operacao_em_segundos", segundos_hms("tempo_de_operacao"))
    .withColumn("sla_tempo_medio_operacional", F.when(tempo_operacao.isNull(), "Sem informação")
                                                .when(tempo_operacao < 3600, DENTRO).otherwise(FORA))
    .withColumn("nivel", nivel("status_de_finalizacao", "data_contato", R.NIVEL_REGRA_NOVA_COMPLETA))
    .where(excluir("status_de_classificacao", "N3 - E.mail - Pendentes - JIRA"))
)

# [106] [116] [126]
email_cb = email.where(manter("canal_de_entrada", "E-mail - Experiência CB"))
gravar(email_cb.withColumn("nivel_considerar", F.when(igual("nivel", "NEUTRO"), "Desconsiderar").otherwise("Considerar")),
       "email_experiencia_cb", "Gold Daily Experiência BR: e-mail Experiência CB (extract MKT Email Experiencia CB)")

# [107] [117] [127]
# O Prep cria "Setor" (calculado) ao lado do "SETOR" do MKT_Reativos; são colunas diferentes nas saídas, então o
# original fica como setor_reativos.
setor_fim = F.col("setor_fim")
data_ajustada = F.col("data_contato_ajustada")
prazo_aberto = (F.when(tb.dia_semana(data_ajustada) == 6, tb.somar_dias(data_ajustada, 3))
                 .when(tb.dia_semana(data_ajustada) == 7, tb.somar_dias(data_ajustada, 2))
                 .otherwise(tb.somar_dias(data_ajustada, 1)))
emails_lojas = (
    email.where(manter("setor_fim", "APP AVON CF", "APP NATURA", "NATURA EXPCB", "NATURA EXPCN"))
    .withColumn("sla_tempo_medio_operacional", F.when(tempo_operacao.isNull(), "Sem informação")
                                                .when(tempo_operacao <= 86400, DENTRO).otherwise(FORA))
    .withColumnRenamed("setor", "setor_reativos")
    .withColumn("setor", F.when(igual(setor_fim, "APP AVON CF"), "APP AVON CF").when(igual(setor_fim, "APP NATURA"), "APP NATURA")
                          .when(igual(setor_fim, "NATURA EXPCN", "NATURA EXPCB"), "NATURA EXPCB"))
    .where(excluir("status_de_finalizacao", "Card Em Branco"))
    .withColumn("status_sla_email",
                F.when(F.col("encerrado_em").isNotNull(), sla("segundos_uteis", 57600))
                 .otherwise(F.when(tb.agora() <= prazo_aberto, DENTRO).otherwise(FORA)))
)
gravar(emails_lojas, "emails_de_lojas", "Gold Daily Experiência BR: e-mails de lojas (extract MKT Emails de Lojas)")

# [115] [128] [136] [139]
COLUNAS_PESSOAIS = ["empresa", "nome", "cpf_cnpj", "numero_do_contrato", "valor_do_contrato", "codigo", "gv", "funcao"]
COLUNAS_ATENDIMENTO = ["responsavel", "tempo_ate_ser_atendido", "tempo_do_atendimento", "primeiro_tempo_de_espera",
                       "tempo_medio_de_espera", "fone_cliente", "setor_entrada", "qtde_mensagens", "observacoes",
                       "campos_adicionais_web_chat", "sla_24_horas"]
email_cb_reduzido = (
    remover(email_cb, "tempo_medio_segundos", "tempo_operacao_em_segundos", *COLUNAS_PESSOAIS, "testelis",
            "ciclo_health_check", "recebidos_health_check", "e_mail", *COLUNAS_ATENDIMENTO)
    .withColumnRenamed("setor", "setor_reativos")
    .withColumn("setor", F.when(F.col("protocolo").isNull(), NULO_TEXTO).otherwise("Experiência CB"))
    .drop("chamado", "fornecedor")
)
emails_lojas_reduzido = remover(emails_lojas, "tempo_medio_segundos", "tempo_operacao_em_segundos", *COLUNAS_PESSOAIS,
                                "fornecedor", "testelis", "ciclo_health_check", "recebidos_health_check", "e_mail",
                                *COLUNAS_ATENDIMENTO, "chamado")
brasil_email = gravar(uniao(email_cb_reduzido, emails_lojas_reduzido), "brasil_email",
                      "Gold Daily Experiência BR: e-mails Experiência CB e lojas (extract MKT BRASIL - Email)")

# COMMAND ----------

# MAGIC %md ## CBCOM e consolidado do WhatsApp – [102] [108] [118] [121] [123] [129] [130] [133] [135] [138] a [151]

# COMMAND ----------

cbcom = primeiro_contato_e_nivel(analitico_97.where(manter("setor_fim", "CB Commerce")))
cbcom = cbcom.withColumn("tempo_medio_segundos", tb.diff_segundos(F.col("data_contato"), F.col("encerrado_em")))
gravar(cbcom, "cbcom", "Gold Daily Experiência BR: CB Commerce (extract MKT - CBCOM)")

REMOVER_WHATSAPP = ["tempo_medio_segundos", "primeiro_tempo_de_espera_segundos", "tempo_atendimento_whatsapp",
                    "tempo_formatado_whatsapp", *COLUNAS_PESSOAIS, "chamado", "fornecedor", "testelis",
                    "ciclo_health_check", "recebidos_health_check", "e_mail", *COLUNAS_ATENDIMENTO]


def reduzido(df, setor):
    return (remover(df, *REMOVER_WHATSAPP).withColumnRenamed("setor", "setor_reativos")
            .withColumn("setor", F.when(F.col("protocolo").isNull(), NULO_TEXTO).otherwise(setor)))


whats_gv_reduzido = reduzido(whats_gv, "WHATS GV")
for coluna in ["sla_5_horas", "sla_10_horas", "sla_15_horas"]:
    whats_gv_reduzido = whats_gv_reduzido.withColumn(coluna, F.coalesce(coluna, F.lit(DENTRO)))
whatsapp_consolidado = uniao(
    reduzido(cbcom, "CBCOM"), reduzido(whats_franquia, "WHATS FRANQUIA"), reduzido(whats_gn, "WHATS GN"),
    whats_gv_reduzido, remover(reduzido(whats_gv_antecipada, "WHATS GV ANTECIPADA"), "tipo_setor"),
)
gravar(whatsapp_consolidado.withColumn("origem", F.coalesce("origem", F.lit("AppSheets"))), "brasil_whatsapp",
       "Gold Daily Experiência BR: WhatsApp e CBCOM consolidados (extract MKT BRASIL - WhatsApp)")

# COMMAND ----------

# MAGIC %md ## MKT Brasil Completo – [19] [39] [65] [67] [69] a [74] [78] [83] [87] [91] [95] [98] [103] [109] [119] [131] [137]

# COMMAND ----------

completo = silver("mkt_brasil_completo").withColumn(
    "status", F.when(F.col("protocol").isin(*R.PROTOCOLOS_RESOLVIDO_N3_MKT), "Resolvido N3 MKT").otherwise(F.col("status")))

# [65] Tickets no formato do MKT Brasil Completo
tickets_completo = (
    tickets.withColumn("canal", remapear(setor_atendimento, {"Experiência CB": ["EXPERIÊNCIA CB"]}))
    .withColumn("situacao", remapear("estado", {"Concluído": ["Finalizado"]}))
    .withColumnRenamed("id_do_ticket", "protocol").withColumnRenamed("data_de_criacao_do_ticket", "data_criacao")
    .withColumnRenamed("data_de_finalizacao", "data_conclusao").withColumnRenamed("tipo", "tipo_canal")
    .withColumn("setor", setor_atendimento).withColumnRenamed("usuario_responsavel", "operador")
    .withColumnRenamed("status_de_finalizacao", "status").withColumnRenamed("status_de_classificacao", "status_de_classificacao1")
    .withColumnRenamed("qtd_atendimentos", "qtd_atendimentos_tickets")
)
completo = uniao(completo, tickets_completo)  # [67]

# [73] [79]
status = F.col("status")
concluidos = (
    completo.where(manter("situacao", "Concluído"))
    .withColumn("tempo_medio_em_segundos", tb.diff_segundos(F.col("data_criacao"), F.col("data_conclusao")))
    .withColumn("status_2", F.when(igual(status, "EXPCN"),
                                   F.when(F.col("data_conclusao") < F.to_timestamp(F.lit("2025-11-01")), "EXPCN")
                                    .otherwise("EXPCN Desconsiderar"))
                             .otherwise(status))
    .where(manter("status", "EXPCN", "Resolvido N2 MKT", "Resolvido N2 e-mail", "Resolvido MKT N3", "Resolvido E-mail N3"))
    .drop("status").withColumnRenamed("status_2", "status")
)
gravar(concluidos, "brasil_completo", "Gold Daily Experiência BR: atendimentos concluídos (extract MKT Brasil Completo)")

# [72] [35] [78] Concluídos dos canais de e-mail e app com os dados da Base MKT
base_mkt = remover(
    silver("mkt_base_mkt"), "ticket", *COLUNAS_PESSOAIS, "pedido_finalizado", "contato_de_solucao", "chamado", "fornecedor",
    "testelis", "ciclo_health_check", "recebidos_health_check", "categoria_1_wr_transp", "categoria_2_wr_transp",
    "origem_health_check", "esta_em_fechamento", "codigo_do_impactado", "ciclo_vigente", "setor", "mercado",
    "resposta_pedido_duplicado", "dados_bancarios", "e_mail", "data_contato", "responsavel", "tempo_ate_ser_atendido",
    "tempo_do_atendimento", "primeiro_tempo_de_espera", "tempo_medio_de_espera", "tempo_de_operacao", "fone_cliente",
    "canal_de_entrada", "setor_entrada", "setor_fim", "qtde_mensagens", "encerrado_em", "observacoes",
    "campos_adicionais_web_chat", "quantidade_de_tickets",
).withColumnRenamed("protocolo", "protocolo2")
canais = (completo.where(manter("situacao", "Concluído") & manter("canal", "Experiência CB", "APP AVON CF", "APP NATURA", "MINHA CONSULTORIA"))
          .withColumnRenamed("protocol", "protocolo"))
completo_nivel = juntar(base_mkt, canais, [("protocolo2", "protocolo")], "right")

# [83] Nos dias 16 e 17/03/2026 o Status vazio é completado com o Status de finalização da Base MKT
dias = (F.to_date("data_criacao").isin(*dias_16_17) | F.to_date("data_conclusao").isin(*dias_16_17))
sem_status_fin = F.col("status_de_finalizacao").isNull() | (F.col("status_de_finalizacao") == "")
completo_nivel = completo_nivel.withColumn(
    "status", F.when(dias, F.when(sem_status_fin, status).otherwise(F.col("status_de_finalizacao"))).otherwise(status))

# [87] [77] [91] [95] [98]
completo_nivel = completo_nivel.withColumn("nivel", nivel("status", "data_conclusao", R.NIVEL_REGRA_NOVA_COMPLETA))
completo_nivel = juntar(completo_nivel, analitico_68.select("protocolo", "qtd_atendimentos", "responsavel"),
                        [("protocolo2", "protocolo")], "left")
completo_nivel = remover(completo_nivel, "protocolo_1").withColumn("validacao_tickets", F.col("protocolo").startswith("T-"))

# [103] [109] [119]
completo_nivel = completo_nivel.withColumn(
    "status", F.when(dias, F.when(status.isNull() | (status == ""), F.col("status_de_finalizacao")).otherwise(status))
                .otherwise(status))
completo_nivel = remover(completo_nivel, "status_de_finalizacao").where(
    excluir("status", "AÇÕES EM MASSA", "AGRADECIMENTOS", "EXPCN", "HEALTH CHECK", "N2 - E.mail - EM ACOMPANHAMENTO - TD", "TESTE")
    & excluir("status", "FINALIZADO FORA DO HORÁRIO") & excluir("status", "PROTOCOLO"))

# [131] [137] Responsável e nome padronizado; só o ano corrente pela data de conclusão
completo_nivel = completo_nivel.withColumn("responsavel", F.coalesce("responsavel", "operador"))
chave_nome = F.expr("replace(replace(upper(trim(responsavel)), ' - INATIVO', ''), '  ', ' ')")
mapa_nomes = F.create_map(*[F.lit(v) for par in R.NOME_RESPONSAVEL.items() for v in par])
completo_nivel = (
    completo_nivel
    .withColumn("nome_responsavel", F.coalesce(F.try_element_at(mapa_nomes, chave_nome), F.expr("replace(responsavel, ' - INATIVO', '')")))
    .withColumn("qtd_atendimentos_1", F.coalesce("qtd_atendimentos_1", F.lit(1)))
    .drop("qtd_atendimentos", "qtd_atendimentos_tickets").withColumnRenamed("qtd_atendimentos_1", "qtd_atendimentos")
    .where(F.year("data_conclusao") == F.year(tb.hoje()))
    .where(excluir("status", "Card Em Branco") & excluir("status", "EXPCB"))
)
completo_nivel = gravar(completo_nivel, "brasil_completo_nivel",
                        "Gold Daily Experiência BR: concluídos de e-mail e app com nível, ano corrente (extract MKT Brasil Completo Nivel)")

# COMMAND ----------

# MAGIC %md ## Backlog – [74] [80] [84] [85] [88] [89] [92] [96] [99] [104]

# COMMAND ----------

idade = F.col("tempo_medio_em_segundos") / 86400
em_aberto = (
    completo.where(manter("situacao", "Em aberto"))
    .withColumn("tempo_medio_em_segundos", tb.diff_segundos(F.col("data_criacao"), tb.agora()))
    .withColumn("faixa_de_aging", F.when(idade <= 1, "1 - Até 24 horas").when(idade <= 3, "2 - 01 a 03 dias")
                                   .when(idade <= 7, "3 - 04 a 07 dias").when(idade <= 15, "4 - 08 a 15 dias")
                                   .when(idade <= 30, "5 - 16 a 30 dias").otherwise("6 - Mais de 30 dias"))
    .withColumn("aging", tb.diff_dias(F.col("data_criacao"), tb.hoje()))
)
analitico_71 = remover(
    analitico_68, "origem", "empresa", "source_id_ctwa", "nome", "cpf_cnpj", "numero_do_contrato", "valor_do_contrato", "gv",
    "funcao", "contato_de_solucao", "fornecedor", "testelis", "ciclo_health_check", "recebidos_health_check",
    "categoria_1_wr_transp", "categoria_2_wr_transp", "solucao_aplicada", "origem_health_check", "esta_em_fechamento",
    "codigo_do_impactado", "ciclo_vigente", "setor", "mercado", "e_mail", "tempo_ate_ser_atendido", "tempo_do_atendimento",
    "primeiro_tempo_de_espera", "tempo_medio_de_espera", "tempo_de_operacao", "fone_cliente", "qtde_mensagens",
    "encerrado_em", "observacoes",
)
backlog = remover(juntar(em_aberto, analitico_71, [("protocol", "protocolo")], "left"),
                  "protocolo", "codigo", "pedido_finalizado", "data_contato", "responsavel", "campos_adicionais_web_chat",
                  "resposta_pedido_duplicado", "dados_bancarios", "protocolo_relacionado")

# [85] [89] [93] Histórico Backlog Diário: no Tableau o extract é acumulado (uma linha por execução). Aqui fica uma
# linha por dia; as linhas importadas do extract antigo são mantidas (origem_registro = 'tableau').
historico_tabela = f"{CATALOGO}.{SCHEMA}.dexp_gold_mkt_historico_backlog_diario"
hoje_backlog = backlog.groupBy(tb.hoje().alias("data_hoje")).agg(
    F.count("protocol").alias("protocol"), F.max(tb.agora()).alias("carimbo_tempo")).withColumn("origem_registro", F.lit("databricks"))
if not spark.catalog.tableExists(historico_tabela):
    importado = f"{VOLUME}/historico/historico_backlog_diario_tableau.csv"
    if os.path.exists(importado):
        (spark.read.option("header", True).csv(importado)
         .select(F.to_date("data_hoje").alias("data_hoje"), F.col("protocol").cast("bigint").alias("protocol"),
                 F.to_timestamp("carimbo_tempo").alias("carimbo_tempo"), F.lit("tableau").alias("origem_registro"))
         .write.saveAsTable(historico_tabela))
    else:
        hoje_backlog.limit(0).write.saveAsTable(historico_tabela)
spark.sql(f"DELETE FROM {historico_tabela} WHERE origem_registro = 'databricks' AND data_hoje = current_date()")
hoje_backlog.write.mode("append").saveAsTable(historico_tabela)
print(f"dexp_gold_mkt_historico_backlog_diario {spark.table(historico_tabela).count():>9,} linhas")

# [84] [31] [92] [96]
backlog = backlog.withColumn("chamado", F.trim(F.regexp_replace("chamado", r"\s+", " ")))
analitico_chamado = (reativos.withColumnRenamed("protocolo", "protocolo_analitico")
                     .select("protocolo_analitico", "chamado", "funcao_do_sistema", "observacoes")
                     .withColumnRenamed("funcao_do_sistema", "funcao_do_sistema_analitico"))
# chamado_1 veio do join [80] e mantém o nome; o chamado do ticket vai para chamado_2
backlog = juntar(analitico_chamado, backlog, [("protocolo_analitico", "protocol")], "right", preservar=["chamado_1"])
backlog = (
    backlog.withColumnRenamed("chamado", "chamado1")
    .withColumn("chamado", F.coalesce("chamado_1", "chamado1"))
    .transform(lambda df: remover(df, "chamado_2", "chamado_1", "chamado1", "observacoes_1", "funcao_do_sistema"))
    .withColumn("funcao_do_sistema", F.coalesce("funcao_do_sistema_analitico", "funcao_do_sistema_1", "funcao_do_sistema_2"))
    .transform(lambda df: remover(df, "funcao_do_sistema_2", "funcao_do_sistema_1", "funcao_do_sistema_analitico"))
)

# [7] [28] [99] [104] Incidente do ServiceNow ligado pelo número do chamado
incidentes = silver("servicenow_incidentes").select(
    F.col("numero").alias("number"), F.col("status").alias("estado_incidente"),
    F.col("motivo_para_estar_em_espera").alias("motivo_em_espera_incidente"), F.col("jira").alias("jira_incidente"),
    F.col("ticket_externo").alias("ticket_externo_incidente"))
backlog = remover(juntar(incidentes, backlog, [("number", "chamado")], "right"), "number")
gravar(backlog, "brasil_backlog", "Gold Daily Experiência BR: atendimentos em aberto com incidente (extract MKT Brasil Backlog)")

# COMMAND ----------

# MAGIC %md ## Experiência Brasil Nivel e Ticket Médio – [46] [140] [142] [144] [148] [150] a [172]

# COMMAND ----------

COLUNAS_NIVEL = ["status_de_classificacao", "nivel", "setor", "protocolo", "pedido_finalizado", "contato_de_solucao",
                 "qtd_atendimentos", "funcao_do_sistema", "data_contato", "status_de_finalizacao"]


def no_formato_nivel(df):
    return (df.select(*COLUNAS_NIVEL).withColumnRenamed("setor", "tipo").withColumnRenamed("protocolo", "ticket")
              .withColumnRenamed("data_contato", "data"))


# [140]
nivel_email = (no_formato_nivel(brasil_email)
               .withColumn("pedido_finalizado", remapear("pedido_finalizado", {"NÃO": ["nao", "N&#195;O"],
                                                                                "NÃO SE APLICA": ["nao_se_aplica", "N&#195;O SE APLICA"]}))
               .withColumn("origem", F.lit("MKT Analitico")))
# [148]
nivel_whatsapp = no_formato_nivel(whatsapp_consolidado)
# [142] O MKT Brasil Completo tem "PEDIDO FINALIZADO" (dos tickets) e o Prep cria "Pedido Finalizado" nulo; para não
# colidirem em snake_case, o dos tickets fica como pedido_finalizado_ticket.
nivel_completo = remover(
    completo_nivel.withColumnRenamed("status", "status_de_finalizacao").withColumn("origem", F.lit("MKT Completo"))
    .withColumnRenamed("canal", "tipo").withColumn("contato_de_solucao", NULO_TEXTO)
    .withColumnRenamed("pedido_finalizado", "pedido_finalizado_ticket").withColumn("pedido_finalizado", NULO_TEXTO)
    .drop("qtde_mensagens").withColumnRenamed("protocolo", "ticket").withColumnRenamed("data_conclusao", "data"),
    "solucao_aplicada", "protocolo2", "responsavel", "tempo_medio_operacional", "tempo_medio_espera", "tempo_medio_atendimento",
    "tempo_medio_primeira_espera", "tempo_medio_ate_ser_atendidos", "situacao", "telefone", "operador", "setor", "tipo_canal",
    "ultima_mensagem", "atendido", "inicio_atendimento", "data_criacao", "atendimentos_first_message_at", "nome",
    "nome_responsavel",
)
# [46] Dynatrace no formato do nível
nivel_dynatrace = dynatrace.select(
    F.lit("Dynatrace").alias("tipo"), NULO_TEXTO.alias("nivel"), NULO_TEXTO.alias("contato_de_solucao"),
    F.col("id").alias("ticket"), "data", "pedido_finalizado").withColumn("qtd_atendimentos", F.lit(1).cast("bigint"))

# [153] [154]
nivel_geral = (
    uniao(nivel_dynatrace, gold("dynamics_nivel"), nivel_whatsapp, nivel_completo, nivel_email)
    .withColumn("int_pedido_finalizado", F.when(igual("pedido_finalizado", "Sim"), 1).otherwise(0))
    .withColumn("mes", mes_ano("data"))
)

# [155] [157] [12] [33] [159] [163] Ticket médio do mês ao lado de cada atendimento (sem Dynamics e sem MKT Completo)
pedidos_mes = (remover(nivel_geral, "status_de_classificacao", "status_de_finalizacao")
               .where(excluir("origem", "MKT Completo")).where(excluir("tipo", "Protocolos CB", "Protocolos CF"))
               .select("int_pedido_finalizado", "mes"))
ticket_medio = silver("mkt_ticket_medio").withColumnRenamed("mes", "data").withColumn("mes", mes_ano("data"))
gravar(remover(juntar(ticket_medio, pedidos_mes, [("mes", "mes")], "inner"), "mes_1"), "ticket_medio",
       "Gold Daily Experiência BR: pedidos finalizados com o ticket médio do mês (extract Ticket Medio Exp Br)")

# [156] [158] [160] Responsável: primeiro o do Dynamics, depois o do MKT_Reativos
experiencia = nivel_geral.where(excluir("origem", "MKT Analitico")).drop("origem").where(excluir("tipo", "Dynatrace"))
experiencia = remover(juntar(reativos.select("protocolo", "responsavel"), experiencia, [("protocolo", "ticket")], "right"), "protocolo")
experiencia = experiencia.withColumn("responsavel", F.coalesce("responsavel_dynamics", "responsavel")).drop("responsavel_dynamics")

# [16] [162] [164] [165] Depois o analista dos Registros de Acionamentos
experiencia = juntar(silver("mkt_registros_de_acionamentos").select("id", "analista"), experiencia, [("id", "ticket")], "right")
experiencia = (experiencia.withColumn("responsavel", F.coalesce("responsavel", "analista")).drop("analista")
               .withColumn("responsavel", remapear("responsavel", R.RESPONSAVEL_ACIONAMENTO))
               .withColumnRenamed("responsavel", "responsavel1"))

# [17] [37] [47] [166] [167] Por fim o analista do Service Cloud
analistas_sc = (silver("mkt_salesforce_analistas")
                .select(F.col("numero_do_caso").alias("id_sc"), F.col("nome_do_usuario_que_realizou_alteracao").alias("analista_sc"))
                .groupBy("id_sc").agg(tb.maximo_texto("analista_sc").alias("analista_sc")))
experiencia = juntar(analistas_sc, experiencia, [("id_sc", "ticket")], "right")
experiencia = experiencia.withColumn("responsavel", F.coalesce("responsavel1", "analista_sc")).drop("responsavel1", "id_sc", "analista_sc")

# [13] [34] [168] [169] Resenhas tratadas pelo time
resenhas = gold("resenhas_appsheets").select(
    F.coalesce("id", F.lit("Resenha ID")).alias("ticket"), F.col("resp_pela_resposta").alias("responsavel"),
    F.col("data_da_resposta_exp").alias("data"), "observacao", F.lit(1).cast("bigint").alias("qtd_atendimentos"),
    mes_ano("data_avaliacao").alias("mes"), F.lit("Resenhas").alias("tipo"))
experiencia = uniao(experiencia, resenhas).withColumn("responsavel", remapear("responsavel", R.RESPONSAVEL_ANALISTAS))

# [9] [30] [170] [171] [172] Função do sistema e classificação: tickets, depois o próprio registro, depois o MKT_Reativos
reativos_30 = reativos.select("protocolo", "funcao_do_sistema", F.col("status_de_classificacao").alias("status_de_classificacao3"))
# funcao_do_sistema_1 (a do ticket) veio do join [78] e mantém o nome; a do próprio registro vai para _2
experiencia = remover(juntar(reativos_30, experiencia, [("protocolo", "ticket")], "right",
                             preservar=["funcao_do_sistema_1"]), "protocolo")
experiencia = (
    experiencia.withColumnRenamed("funcao_do_sistema", "funcao_do_sistema_3")
    .withColumn("funcao_do_sistema", F.coalesce(*[c for c in ["funcao_do_sistema_1", "funcao_do_sistema_2", "funcao_do_sistema_3"]
                                                  if c in experiencia.columns or c == "funcao_do_sistema_3"]))
    .transform(lambda df: remover(df, "funcao_do_sistema_3", "funcao_do_sistema_1", "funcao_do_sistema_2"))
    .withColumnRenamed("status_de_classificacao", "status_de_classificacao2")
    .withColumn("status_de_classificacao", F.coalesce("status_de_classificacao1", "status_de_classificacao2", "status_de_classificacao3"))
    .transform(lambda df: remover(df, "status_de_classificacao3", "status_de_classificacao2", "status_de_classificacao1"))
    .withColumn("responsavel", remapear("responsavel", R.RESPONSAVEL_FINAL))
)
gravar(experiencia, "experiencia_brasil_nivel",
       "Gold Daily Experiência BR: atendimentos MKT, Dynamics e Resenhas com nível e responsável (extract Experiencia Brasil Nivel)")
