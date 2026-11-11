"""Book Executivo Exp Brasil: uma função por aba, para um mês ("aaaa-mm").

Cada regra reproduz a planilha do painel "Daily Experiencia BR" (Tableau Cloud) citada no comentário, lendo as tabelas
gold do Databricks, que são cópias das fontes publicadas no Tableau.
"""
from .databricks import consultar, tabela
from .formatos import dias, inteiro, pct, reais

MANUAL = "manual"  # coluna que não sai do Databricks e continua sendo preenchida à mão


def _mes(coluna, mes):
    return f"date_format({coluna}, 'yyyy-MM') = '{mes}'"


def _um(sql):
    linhas = consultar(sql)
    return {k: (float(v) if v not in (None, "") else None) for k, v in linhas[0].items()} if linhas else {}


# --- Indicadores 2026 -------------------------------------------------------------------------------------------------

def sla_whatsapp(mes):
    """"Tb SLA WhatsApp": % SLA do primeiro contato (fonte MKT BRASIL - WhatsApp)."""
    r = _um(f"""
        SELECT sum(CASE WHEN sla_do_primeiro_contato = 'Dentro do SLA' THEN 1 ELSE 0 END) AS dentro,
               sum(CASE WHEN sla_do_primeiro_contato = 'Fora do SLA' THEN 1 ELSE 0 END) AS fora
        FROM {tabela('dexp_gold_mkt_brasil_whatsapp')}
        WHERE nivel IN ('N1', 'N2', 'NEUTRO')
          AND (desconsiderar_tickets IS NULL OR desconsiderar_tickets = 'Considerar')
          AND {_mes('data_contato', mes)}""")
    return pct(r["dentro"], r["dentro"] + r["fora"])


def sla_email_1h(mes):
    """"Tabela SLA Email 2026": % dentro de 1 hora útil (fonte MKT Email Experiencia CB)."""
    r = _um(f"""
        WITH b AS (
          SELECT qtd_atendimentos,
                 CASE WHEN expurgo = 'Sim' THEN 'Não Considerar'
                      WHEN segundos_uteis >= 0 AND segundos_uteis <= 3600 THEN 'Dentro de 1 Hora'
                      WHEN segundos_uteis > 3600 THEN 'Acima de 1 Hora'
                      ELSE 'Não Considerar' END AS email_1_hora
          FROM {tabela('dexp_gold_mkt_email_experiencia_cb')}
          WHERE nivel IN ('N1', 'N2', 'NEUTRO') AND {_mes('data_contato', mes)})
        SELECT sum(CASE WHEN email_1_hora = 'Dentro de 1 Hora' THEN qtd_atendimentos ELSE 0 END) AS dentro,
               sum(CASE WHEN email_1_hora = 'Acima de 1 Hora' THEN qtd_atendimentos ELSE 0 END) AS acima
        FROM b""")
    return pct(r["dentro"], r["dentro"] + r["acima"])


# Tipos do filtro do painel, mais "Franquias": até setembro/2026 esses protocolos vinham como "Protocolos CB" e entravam
# nos indicadores; depois passaram a ter tipo próprio. Decisão (04/11/2026): continuam entrando, como antes.
TIPOS_RETENCAO = ("APP AVON CF", "APP NATURA", "CBCOM", "Experiência CB", "MINHA CONSULTORIA", "Protocolos CB",
                  "Protocolos CF", "Franquias", "WHATS FRANQUIA", "WHATS GN", "WHATS GV", "WHATS GV ANTECIPADA")


def retencao_n1(mes):
    """"Tab. Ind. N1 2026": atendimentos N1 / (N1 + N2) (fonte Experiencia Brasil Nivel)."""
    tipos = ", ".join(f"'{t}'" for t in TIPOS_RETENCAO)
    r = _um(f"""
        SELECT sum(CASE WHEN nivel = 'N1' THEN qtd_atendimentos ELSE 0 END) AS n1, sum(qtd_atendimentos) AS total
        FROM {tabela('dexp_gold_mkt_experiencia_brasil_nivel')}
        WHERE nivel IN ('N1', 'N2') AND tipo IN ({tipos}) AND {_mes('data', mes)}""")
    return pct(r["n1"], r["total"])


SETORES_CSAT = ("CB Commerce", "TD -  GV Antecipada", "Triagem", "Whats Franquia", "Whats GN", "Whats GV")


def csat(mes):
    """"Tb CSAT": (soma da nota / 5) / protocolos distintos (fonte Enquetes C-SAT, Experiencia Brasil)."""
    setores = ", ".join(f"'{s}'" for s in SETORES_CSAT)
    r = _um(f"""
        SELECT sum(nota_da_csat) / 5 AS pontos, count(DISTINCT protocolo) AS protocolos
        FROM {tabela('dexp_gold_csat_enquetes')}
        WHERE c_sat IN ('DETRATOR', 'NEUTRO', 'PROMOTOR') AND fonte = 'Experiencia Brasil'
          AND (exp_br_setor_fim IS NULL OR exp_br_setor_fim IN ({setores})) AND {_mes('data', mes)}""")
    return pct(r["pontos"], r["protocolos"])


def pedidos_convertidos(mes):
    """"Tab. Ind. Qtd/Valor Pedido Convertido 2026" (fonte Ticket Medio Exp Br)."""
    r = _um(f"""
        SELECT sum(int_pedido_finalizado) AS qtd, sum(ticket_medio * int_pedido_finalizado) AS valor
        FROM {tabela('dexp_gold_mkt_ticket_medio')} WHERE {_mes('data', mes)}""")
    return inteiro(r["qtd"] or 0), reais(r["valor"] or 0)


APPS_RESENHAS = ("Avon", "Consultoria", "Força de Vendas", "Sempre Presente")


def sla_resenhas(mes):
    """"Tb SLA Resenhas Consolidado": % dentro do SLA (fonte Resenhas EXP BR AppSheets)."""
    apps = ", ".join(f"'{a}'" for a in APPS_RESENHAS)
    r = _um(f"""
        SELECT sum(CASE WHEN status_sla = 'Dentro do SLA' THEN 1 ELSE 0 END) AS dentro, count(status_sla) AS total
        FROM {tabela('dexp_gold_resenhas_appsheets')}
        WHERE app_nome IN ({apps}) AND {_mes('data_avaliacao', mes)}""")
    return pct(r["dentro"], r["total"])


def sla_cliente_crm(mes):
    """"Tb SLA Cliente CRM": % dentro do prazo do cliente (fonte Dynamics - Termino Real)."""
    r = _um(f"""
        SELECT sum(CASE WHEN sla_cliente = 'DENTRO DO PRAZO' THEN 1 ELSE 0 END) AS dentro,
               sum(CASE WHEN sla_cliente = 'FORA DO PRAZO' THEN 1 ELSE 0 END) AS fora
        FROM {tabela('dexp_gold_dynamics_tarefas')}
        WHERE base = 'Encerrado em' AND retrabalho = 'Normal' AND {_mes('termino_real', mes)}""")
    return pct(r["dentro"], r["dentro"] + r["fora"])


def tmo(mes, status):
    """"Tb TMO WhatsApp/Email N2/N3": média de "Tempo Medio em Segundos" (fonte MKT Brasil Completo).

    No e-mail o painel usa o campo Status2, que junta EXPCN e a grafia "Resolvido N2 e-mali" a "Resolvido N2 e-mail".
    """
    status2 = ("CASE WHEN status = 'EXPCN' OR status = 'Resolvido N2 e-mali' THEN 'Resolvido N2 e-mail' "
               "ELSE status END")
    r = _um(f"""
        SELECT avg(tempo_medio_em_segundos) AS segundos
        FROM {tabela('dexp_gold_mkt_brasil_completo')}
        WHERE canal = 'Experiência CB' AND ({status2}) = '{status}' AND {_mes('data_conclusao', mes)}""")
    return dias(r.get("segundos"))


def indicadores_contratuais(mes):
    qtd, valor = pedidos_convertidos(mes)
    return {
        "TPR - Tempo de Primeira Resposta - Atendimento Gerentes": sla_whatsapp(mes),
        "TMR - SLA de Resolução -E-mail (N1)": sla_email_1h(mes),
        "Notificação de Incidente": MANUAL,
        "Retenção em N1": retencao_n1(mes),
        "CSAT": csat(mes),
        "Quality Assurance": MANUAL,
        "Pedidos convertidos": qtd,
        "Valor de pedido convertido": valor,
    }


def indicadores_monitoracao(mes):
    return {
        "TPA - Tempo de Primeiro Atendimento - Atendimento Resenhas": sla_resenhas(mes),
        "TMR - SLA de Resolução - Prazo Cliente (Protocolo Atendimento)": sla_cliente_crm(mes),
        "TMR - SLA de Resolução -E-mail (origem whatsapp) N2": tmo(mes, "Resolvido N2 MKT"),
        "TMR - SLA de Resolução -E-mail (origem whatsapp) N3": tmo(mes, "Resolvido MKT N3"),
        "TMR - SLA de Resolução -E-mail (origem e-mail) N2": tmo(mes, "Resolvido N2 e-mail"),
        "TMR - SLA de Resolução -E-mail (origem e-mail) N3": tmo(mes, "Resolvido E-mail N3"),
    }


A_INVESTIGAR = "a investigar"  # regra ainda não reproduzida: preencher pelo painel

# --- Retenção Dia / Solicitações (fonte Experiencia Brasil Nivel) ------------------------------------------------------

# Campo "Tipo2" do painel: agrupa o Tipo em ferramentas
TIPO2 = """CASE WHEN upper(tipo) IN ('APP AVON CF', 'APP NATURA', 'NATURA EXPCB', 'MINHA CONSULTORIA') THEN 'EMAIL LOJA'
                WHEN upper(tipo) IN ('PROTOCOLOS CB', 'PROTOCOLOS CF', 'FRANQUIAS') THEN 'SERVICE CLOUD / DYNAMICS'
                WHEN upper(tipo) IN ('CBCOM', 'WHATS FRANQUIA', 'WHATS GN', 'WHATS GV', 'WHATS GV ANTECIPADA') THEN 'WHATS MKT'
                WHEN upper(tipo) = 'EXPERIÊNCIA CB' THEN 'EMAIL MKT' ELSE upper(tipo) END"""


def por_ferramenta(mes):
    """"Total por Tipo" e "Retenção por Ferramenta": volume (todos os níveis) e retenção N1 / (N1 + N2) por Tipo2."""
    tipos = ", ".join(f"'{t}'" for t in TIPOS_RETENCAO)
    linhas = consultar(f"""
        SELECT {TIPO2} AS ferramenta, sum(qtd_atendimentos) AS volume,
               sum(CASE WHEN nivel = 'N1' THEN qtd_atendimentos ELSE 0 END) AS n1,
               sum(CASE WHEN nivel IN ('N1', 'N2') THEN qtd_atendimentos ELSE 0 END) AS n1n2
        FROM {tabela('dexp_gold_mkt_experiencia_brasil_nivel')}
        WHERE tipo IN ({tipos}) AND {_mes('data', mes)}
        GROUP BY 1""")
    return {l["ferramenta"]: {k: float(l[k] or 0) for k in ("volume", "n1", "n1n2")} for l in linhas}


def retencao(mes):
    f = por_ferramenta(mes)
    wa, em, dy = (f.get(k, {"volume": 0}) for k in ("WHATS MKT", "EMAIL MKT", "SERVICE CLOUD / DYNAMICS"))
    return {
        "Volumetria Total": inteiro(wa["volume"] + em["volume"] + dy["volume"]),
        "WhatsApp": inteiro(wa["volume"]),
        "E-mail": inteiro(em["volume"]),
        "Ocorrências": inteiro(dy["volume"]),
        "Retenção N1": retencao_n1(mes),
    }


# --- Proativos, Resenhas, Requisições Eventuais, Dynamics ---------------------------------------------------------------

def health_check(mes):
    """"HC Recebidos e Agendados": soma de Qtde Agendamento (fonte HC Exp Brasil)."""
    r = _um(f"SELECT sum(qtde_agendamento) AS ag FROM {tabela('dexp_gold_mkt_hc_exp_brasil')} WHERE {_mes('data', mes)}")
    return inteiro(r["ag"] or 0)


def dynatrace(mes):
    """"Dynatrace Mes": quantidade de registros (fonte Exp Brasil Dynatrace)."""
    r = _um(f"SELECT count(*) AS n FROM {tabela('dexp_gold_mkt_exp_brasil_dynatrace')} WHERE {_mes('data', mes)}")
    return inteiro(r["n"])


def resenhas_1a3(mes):
    """"Classificacao Resenhas 1, 2 e 3": respostas a avaliações de 1 a 3 estrelas (fonte Resenhas EXP BR AppSheets)."""
    r = _um(f"""SELECT count(categoria_da_resposta) AS n FROM {tabela('dexp_gold_resenhas_appsheets')}
                WHERE classificacao_de_estrelas IN ('1', '2', '3') AND {_mes('data_da_resposta', mes)}""")
    return inteiro(r["n"])


def requisicoes_eventuais(mes):
    """"RE Total": quantidade de requisições eventuais (fonte Requisição Eventual EXP BR)."""
    r = _um(f"SELECT count(*) AS n FROM {tabela('dexp_gold_mkt_requisicao_eventual')} WHERE {_mes('data', mes)}")
    return inteiro(r["n"])


def protocolos_cb_cf(mes):
    """Protocolos encerrados no mês (fonte Dynamics - Termino Real, visão "Encerrado em", CB + CF + Franquias)."""
    r = _um(f"""SELECT count(*) AS n FROM {tabela('dexp_gold_dynamics_tarefas')}
                WHERE base = 'Encerrado em' AND {_mes('termino_real', mes)}""")
    return inteiro(r["n"])


SOLUCOES_SLA = ("Abrir chamado", "Analisar Erro - Evidencia Anexada", "Analisar Erro - Sem evidência",
                "Análise remuneração solicitada", "Cancelamento realizado", "Card criado no Jira", "Caso resolvido",
                "Cliente não Postou o Produto", "Correção realizada", "Correção solicitada", "Correção solicitada TD",
                "Documento inválido", "Documento não anexado", "Erro operacional Criado Em", "Estorno solicitado",
                "Fluxo de exceção", "Pedido Cancelado", "Pedido entregue", "Reativação realizada",
                "Rechamada SLA fora do prazo", "Reset de senha realizado", "Resolvido", "Sem Retorno do cliente",
                "Solicitação de análise de pagamento", "Solicitação não procedente",
                "Solicitação não procedente - Desvio operacional Criados Em", "Solicitação procedente",
                "Verificar requisitos para gerar vale troca")


def sla_tarefas(mes):
    """"Dynamics CB+CF SLA EXP": % dentro do prazo do SLA Experiência, com o filtro de Solução do painel."""
    solucoes = ", ".join("'" + s.replace("'", "''") + "'" for s in SOLUCOES_SLA)
    r = _um(f"""
        SELECT sum(CASE WHEN sla_experiencia = 'DENTRO DO PRAZO' THEN 1 ELSE 0 END) AS dentro,
               sum(CASE WHEN sla_experiencia = 'FORA DO PRAZO' THEN 1 ELSE 0 END) AS fora
        FROM {tabela('dexp_gold_dynamics_tarefas')}
        WHERE base = 'Encerrado em' AND (solucao IS NULL OR solucao IN ({solucoes})) AND {_mes('termino_real', mes)}""")
    return pct(r["dentro"], r["dentro"] + r["fora"])


def cards01(mes):
    f = por_ferramenta(mes)
    qtd, valor = pedidos_convertidos(mes)
    return {
        "Valor de pedido convertido": valor,
        "Pedidos convertidos": qtd,
        "Volume de Casos Recebidos WhatsApp": inteiro(f.get("WHATS MKT", {}).get("volume", 0)),
        "Volume de E-mails Recebidos": inteiro(f.get("EMAIL MKT", {}).get("volume", 0)),
        "Health Check Agendados": health_check(mes),
        "Monitoração Dynatrace": dynatrace(mes),
        "Resenhas 1 a 3": resenhas_1a3(mes),
        "Resenhas 4 e 5": A_INVESTIGAR,
        "Protocolos Central CB e CF": protocolos_cb_cf(mes),
        "E-mails Loja": inteiro(f.get("EMAIL LOJA", {}).get("volume", 0)),
        "Requisições Eventuais": requisicoes_eventuais(mes),
    }


def cards2(mes):
    f = por_ferramenta(mes)
    ret = lambda k: pct(f.get(k, {}).get("n1", 0), f.get(k, {}).get("n1n2", 0))
    vol = sum(f.get(k, {}).get("volume", 0) for k in ("WHATS MKT", "EMAIL MKT", "SERVICE CLOUD / DYNAMICS"))
    return {
        "SLA WhatsApp": sla_whatsapp(mes),
        "TMA E-mail": email_atendimentos(mes)[1],
        "SLA Tarefas": sla_tarefas(mes),
        "Retenção WhatsApp": ret("WHATS MKT"),
        "Retenção E-mail": ret("EMAIL MKT"),
        "Retenção Tarefas": ret("SERVICE CLOUD / DYNAMICS"),
        "Volumetria Total": inteiro(vol),
    }


# --- Abas mensais de WhatsApp (fonte MKT BRASIL - WhatsApp + Experiencia Brasil Nivel) ---------------------------------

SETORES_WA = {"GN": ("WHATS GN",), "GV": ("WHATS GV",), "Franq": ("WHATS FRANQUIA",), "CBCom": ("CBCOM",),
              "Reativos": ("WHATS GN", "WHATS GV", "WHATS GV ANTECIPADA", "WHATS FRANQUIA", "CBCOM")}


def _wa_mensal(mes, setores):
    """Acionamentos e SLA do primeiro contato do(s) setor(es); N1 e N2 da retenção (tipo de mesmo nome)."""
    lista = ", ".join(f"'{s}'" for s in setores)
    r = _um(f"""
        SELECT count(*) AS qtd,
               sum(CASE WHEN sla_do_primeiro_contato = 'Dentro do SLA' THEN 1 ELSE 0 END) AS dentro,
               sum(CASE WHEN sla_do_primeiro_contato = 'Fora do SLA' THEN 1 ELSE 0 END) AS fora
        FROM {tabela('dexp_gold_mkt_brasil_whatsapp')}
        WHERE setor IN ({lista}) AND nivel IN ('N1', 'N2', 'NEUTRO')
          AND (desconsiderar_tickets IS NULL OR desconsiderar_tickets = 'Considerar') AND {_mes('data_contato', mes)}""")
    n = _um(f"""
        SELECT sum(CASE WHEN nivel = 'N1' THEN qtd_atendimentos ELSE 0 END) AS n1,
               sum(CASE WHEN nivel = 'N2' THEN qtd_atendimentos ELSE 0 END) AS n2
        FROM {tabela('dexp_gold_mkt_experiencia_brasil_nivel')}
        WHERE upper(tipo) IN ({lista}) AND {_mes('data', mes)}""")
    n1, n2 = n.get("n1") or 0, n.get("n2") or 0
    return {
        "Quantidade de Acionamentos": inteiro(r["qtd"] or 0),
        "SLA (≥ 95%)": pct(r["dentro"] or 0, (r["dentro"] or 0) + (r["fora"] or 0)),
        "Volume N1": inteiro(n1),
        "Volume N2": inteiro(n2),
        "N1 (% dentro do prazo ≥ 70%)": pct(n1, n1 + n2),
    }


# --- E-mail Experiência CB (fonte MKT Email Experiencia CB) --------------------------------------------------------------

# Filtro de "Status de finalização" da planilha "Email EXPCB Atendimento e Tempo Medio" (inclui os vazios)
STATUS_EMAIL = ("AÇÕES EM MASSA", "AGUARD. RETORNO FV", "ATUALIZAÇÃO APP", "ATUALIZAÇÃO DO APP", "ATUALIZAÇÃO DO NAVEGADOR",
                "Card Em Branco", "CHAMADO", "Contato sem interação", "CONTATO SEM SUCESSO",
                "DIRECIONADO PARA O ATENDIMENTO", "DIRECIONADO PARA O SERVICE DESK", "DIRECIONADO PARA O TRANSPORTE",
                "DIRECIONADO PARA TERCEIROS", "EXCLUSÃO DE PEDIDO EM RASCUNHO", "EXPCN - CLASSIFICAÇÃO",
                "FINALIZA EM MASSA - API", "Finalizado no primeiro contato", "Finalizado pelo cliente", "FOLLOWUP",
                "INCIDENTE CRÍTICO", "JÁ ESTAVA RESOLVIDO",
                "LIMPEZA DE CACHE/ NAVEGAÇÃO EM GUIA ANÔNIMA/ TROCA DE NAVEGADOR", "ORIENTADA PROCESSO|REGRA",
                "PROTOCOLO", "REABERTURA DE CHAMADO", "REENVIO DOS TERMOS", "REESTÍMULO NO AGREEMENTS",
                "REESTÍMULO NO SALESFORCE", "REPROCESSAMENTO DE CADASTRO", "RESET DE SENHA", "RESET SENHA",
                "RESOLVIDO SEM ATUAÇÃO DO EXP", "VALIDAÇÃO DE CHAMADO")


def _hms(segundos):
    if segundos is None:
        return "-"
    s = int(segundos)
    return f"{s // 3600:02d}:{s % 3600 // 60:02d}:{s % 60:02d}"


def email_atendimentos(mes):
    """"Email EXPCB Atendimento e Tempo Medio": soma de atendimentos e média do tempo de operação."""
    lista = ", ".join("'" + s.replace("'", "''") + "'" for s in STATUS_EMAIL)
    r = _um(f"""
        SELECT sum(qtd_atendimentos) AS qtd, avg(tempo_operacao_em_segundos) AS tma
        FROM {tabela('dexp_gold_mkt_email_experiencia_cb')}
        WHERE nivel IN ('N1', 'N2', 'NEUTRO') AND (status_de_finalizacao IS NULL OR status_de_finalizacao IN ({lista}))
          AND {_mes('data_contato', mes)}""")
    return inteiro(r["qtd"] or 0), _hms(r["tma"])


def email_mensal(mes):
    qtd, tma = email_atendimentos(mes)
    f = por_ferramenta(mes).get("EMAIL MKT", {})
    n = _um(f"""SELECT sum(CASE WHEN nivel = 'N2' THEN qtd_atendimentos ELSE 0 END) AS n2
                FROM {tabela('dexp_gold_mkt_experiencia_brasil_nivel')}
                WHERE tipo = 'Experiência CB' AND {_mes('data', mes)}""")
    n1, n2 = f.get("n1", 0), n.get("n2") or 0
    return {"Quantidade de Acionamentos": qtd, "Tempo Médio Operacional N1": tma, "Volume N1": inteiro(n1),
            "Volume N2": inteiro(n2), "N1 (% dentro do prazo ≥ 70%)": pct(n1, n1 + n2)}


def _tmo_segundos(mes, status):
    status2 = ("CASE WHEN status = 'EXPCN' OR status = 'Resolvido N2 e-mali' THEN 'Resolvido N2 e-mail' "
               "ELSE status END")
    r = _um(f"""SELECT avg(tempo_medio_em_segundos) AS s FROM {tabela('dexp_gold_mkt_brasil_completo')}
                WHERE canal = 'Experiência CB' AND ({status2}) = '{status}' AND {_mes('data_conclusao', mes)}""")
    return r.get("s")


def email_tmo(mes):
    """Mesmos TMOs da monitoração, em horas ("hhh:mm:ss")."""
    hms = lambda s: "-" if s is None else f"{int(s) // 3600}:{int(s) % 3600 // 60:02d}:{int(s) % 60:02d}"
    return {"TMO N2 - Origem WhatsApp": hms(_tmo_segundos(mes, "Resolvido N2 MKT")),
            "TMO N2 - Origem E-mail": hms(_tmo_segundos(mes, "Resolvido N2 e-mail")),
            "TMO N3 - Origem WhatsApp": hms(_tmo_segundos(mes, "Resolvido MKT N3")),
            "TMO N3 - Origem E-mail": hms(_tmo_segundos(mes, "Resolvido E-mail N3"))}


# --- Tarefas CB e CF (fonte Dynamics - Termino Real) ---------------------------------------------------------------------

GRUPO_TAREFA = {"CB": ("Protocolos CB", "Franquias"), "CF": ("Protocolos CF",), "Total": ("Protocolos CB", "Franquias", "Protocolos CF")}


def _tarefas(mes, grupo):
    tipos = ", ".join(f"'{t}'" for t in GRUPO_TAREFA[grupo])
    T = tabela("dexp_gold_dynamics_tarefas")
    sla = lambda c: f"sum(CASE WHEN {c} = 'DENTRO DO PRAZO' THEN 1 ELSE 0 END) AS {c}_d, sum(CASE WHEN {c} = 'FORA DO PRAZO' THEN 1 ELSE 0 END) AS {c}_f"
    a = _um(f"SELECT count(numero_da_ocorrencia) AS abertos FROM {T} WHERE base = 'Criado em' AND tipo_protocolo IN ({tipos}) AND {_mes('data', mes)}")
    e = _um(f"""SELECT sum(CASE WHEN retrabalho = 'Normal' THEN 1 ELSE 0 END) AS fechados,
                       sum(CASE WHEN retrabalho = 'Retrabalho' THEN 1 ELSE 0 END) AS retrabalho
                FROM {T} WHERE base = 'Encerrado em' AND tipo_protocolo IN ({tipos}) AND {_mes('termino_real', mes)}""")
    s = _um(f"""SELECT {sla('sla_cliente')}, {sla('sla_experiencia')}, {sla('sla_5_horas')}
                FROM {T} WHERE base = 'Encerrado em' AND retrabalho = 'Normal' AND tipo_protocolo IN ({tipos})
                  AND {_mes('termino_real', mes)}""")
    p = lambda c: pct(s[f"{c}_d"] or 0, (s[f"{c}_d"] or 0) + (s[f"{c}_f"] or 0))
    return a, e, p


def tarefas_mensal(mes, grupo):
    a, e, p = _tarefas(mes, grupo)
    f = por_ferramenta(mes).get("SERVICE CLOUD / DYNAMICS", {}) if grupo == "Total" else None
    if f is None:
        tipos = ", ".join(f"'{t}'" for t in GRUPO_TAREFA[grupo])
        n = _um(f"""SELECT sum(CASE WHEN nivel = 'N1' THEN qtd_atendimentos ELSE 0 END) AS n1,
                           sum(CASE WHEN nivel IN ('N1', 'N2') THEN qtd_atendimentos ELSE 0 END) AS n1n2
                    FROM {tabela('dexp_gold_mkt_experiencia_brasil_nivel')} WHERE tipo IN ({tipos}) AND {_mes('data', mes)}""")
        f = {"n1": n.get("n1") or 0, "n1n2": n.get("n1n2") or 0}
    return {
        "Protocolos Abertos": inteiro(a["abertos"] or 0),
        "Protocolos Fechados": inteiro(e["fechados"] or 0),
        "Retrabalho": inteiro(e["retrabalho"] or 0),
        "N1 (% dentro do prazo): geral 70%": pct(f["n1"], f["n1n2"]),
        "SLA Cliente": p("sla_cliente"),
        "Até 24h": p("sla_experiencia"),
        "Até 5h": p("sla_5_horas"),
    }


def tarefas_fase(mes, grupo):
    tipos = ", ".join(f"'{t}'" for t in GRUPO_TAREFA[grupo])
    linhas = consultar(f"""
        SELECT fase, count(*) AS vol,
               sum(CASE WHEN sla_experiencia = 'DENTRO DO PRAZO' THEN 1 ELSE 0 END) AS d,
               sum(CASE WHEN sla_experiencia = 'FORA DO PRAZO' THEN 1 ELSE 0 END) AS f
        FROM {tabela('dexp_gold_dynamics_tarefas')}
        WHERE base = 'Encerrado em' AND retrabalho = 'Normal' AND tipo_protocolo IN ({tipos}) AND {_mes('termino_real', mes)}
        GROUP BY fase""")
    x = {l["fase"]: {k: float(l[k] or 0) for k in ("vol", "d", "f")} for l in linhas}
    out = {}
    for fase in ("Fase 1", "Fase 2"):
        v = x.get(fase, {"vol": 0, "d": 0, "f": 0})
        out[f"{fase} - Volume"] = inteiro(v["vol"])
        out[f"{fase} - % SLA 24h (≥ 85%)"] = pct(v["d"], v["d"] + v["f"])
    return out


def reqevent_mensal(mes):
    return {"Quantidade de Acionamentos": requisicoes_eventuais(mes), "Volume N1": A_INVESTIGAR, "Volume N2": A_INVESTIGAR}


# --- Abas de motivos: 3 maiores plataformas (Tribo) x 3 maiores motivos (Macro) ------------------------------------------

NOME_PLATAFORMA = {"Experiencia de Compras": "Exp. de Compras", "Experiencia de Compra": "Exp. de Compras"}


def _motivos(fonte, filtro):
    """Linhas do mês: plataforma, volume da plataforma, motivo, volume do motivo e percentual sobre a plataforma.

    Conta linhas (atendimentos/tarefas). Motivos que só mudam em maiúsculas são somados ("MINHA LOJA" e "Minha Loja"),
    e o nome exibido é a grafia mais frequente.
    """
    linhas = consultar(f"""
        WITH b AS (SELECT tribo, macro FROM {tabela(fonte)} WHERE {filtro} AND tribo IS NOT NULL),
        p AS (SELECT tribo, count(*) AS vol FROM b GROUP BY tribo ORDER BY vol DESC LIMIT 3),
        m AS (SELECT b.tribo, upper(b.macro) AS chave, count(*) AS vol
              FROM b JOIN p ON b.tribo = p.tribo WHERE b.macro IS NOT NULL GROUP BY b.tribo, upper(b.macro)),
        g AS (SELECT b.tribo, upper(b.macro) AS chave, b.macro, count(*) AS n FROM b WHERE b.macro IS NOT NULL
              GROUP BY 1, 2, 3),
        -- nome exibido: a grafia mais frequente, preferindo a que não está toda em maiúsculas
        nome AS (SELECT tribo, chave, max_by(macro, (CASE WHEN macro <> upper(macro) THEN 1000000 ELSE 0 END) + n) AS macro
                 FROM g GROUP BY 1, 2),
        -- empate no volume: vence o motivo que não está todo em maiúsculas (como no Book)
        r AS (SELECT m.tribo, p.vol AS vol_plat, nome.macro, m.vol,
                     row_number() OVER (PARTITION BY m.tribo ORDER BY m.vol DESC,
                                        CASE WHEN nome.macro <> upper(nome.macro) THEN 0 ELSE 1 END, nome.macro) AS pos
              FROM m JOIN p ON m.tribo = p.tribo JOIN nome ON m.tribo = nome.tribo AND m.chave = nome.chave)
        SELECT tribo, vol_plat, macro, vol FROM r WHERE pos <= 3 ORDER BY vol_plat DESC, vol DESC""")
    return [{"Plataforma": NOME_PLATAFORMA.get(l["tribo"], l["tribo"]), "Volume Total Plataforma": inteiro(float(l["vol_plat"])),
             "Motivo do Contato": l["macro"], "Volume Motivo": inteiro(float(l["vol"])),
             "Percentual (%)": pct(float(l["vol"]), float(l["vol_plat"]))} for l in linhas]


def motivos_wa(mes, setores, nivel):
    lista = ", ".join(f"'{s}'" for s in setores)
    return _motivos("dexp_gold_mkt_brasil_whatsapp", f"setor IN ({lista}) AND nivel = '{nivel}' AND {_mes('data_contato', mes)}")


def motivos_email(mes, nivel):
    return _motivos("dexp_gold_mkt_email_experiencia_cb", f"nivel = '{nivel}' AND {_mes('data_contato', mes)}")


def motivos_tarefas(mes, grupo, nivel):
    tipos = ", ".join(f"'{t}'" for t in GRUPO_TAREFA[grupo])
    return _motivos("dexp_gold_dynamics_tarefas",
                    f"base = 'Encerrado em' AND retrabalho = 'Normal' AND tipo_protocolo IN ({tipos}) "
                    f"AND nivel_de_atendimento = '{nivel}' AND {_mes('termino_real', mes)}")


# --- Proativos (fontes Exp Brasil Dynatrace e HC Exp Brasil) --------------------------------------------------------------

def _dynatrace(mes):
    return _um(f"""
        SELECT count(*) AS total,
               sum(CASE WHEN upper(conseguiu_contato) = 'SIM' THEN 1 ELSE 0 END) AS sucesso,
               sum(CASE WHEN upper(conseguiu_contato) = 'SIM' AND upper(pedido_finalizado) = 'SIM' THEN 1 ELSE 0 END) AS pedidos
        FROM {tabela('dexp_gold_mkt_exp_brasil_dynatrace')} WHERE {_mes('data', mes)}""")


def proativos_mensal(mes):
    """"Dynatrace Mes" e "Dynatrace Status": monitorações, contatos com e sem sucesso e pedidos finalizados."""
    d = _dynatrace(mes)
    total, sucesso, pedidos = (d[k] or 0 for k in ("total", "sucesso", "pedidos"))
    return {"Total de Monitorações": inteiro(total), "Contatos Bem-Sucedidos (Com Sucesso)": inteiro(sucesso),
            "Sem Sucesso": inteiro(total - sucesso), "Pedidos Finalizados com Contato": inteiro(pedidos),
            "Taxa de Sucesso dos Contatos": pct(pedidos, sucesso)}


def proativos_contatos_pedidos(mes):
    d = _dynatrace(mes)
    return {"Contatos Realizados": inteiro(d["sucesso"] or 0), "Pedidos Finalizados": inteiro(d["pedidos"] or 0)}


def proativos_hc_mensal(mes):
    """"HC Recebidos e Agendados" e "HC% Enviados" (fonte HC Exp Brasil)."""
    r = _um(f"""SELECT sum(qtde_agendamento) AS ag, sum(qtde_recebidos) AS rec
                FROM {tabela('dexp_gold_mkt_hc_exp_brasil')} WHERE {_mes('data', mes)}""")
    return {"Qtd Agendamento": inteiro(r["ag"] or 0), "Qtd Recebidos": inteiro(r["rec"] or 0),
            "Conversão (Atendimento com o Expcb)": pct(r["rec"] or 0, r["ag"] or 0), "Alcance %": A_INVESTIGAR}


# --- E-mails de loja (fonte MKT Emails de Lojas) ---------------------------------------------------------------------------

SETOR_LOJA = {"Natura_Expcb": "NATURA EXPCB", "AppNatura": "APP NATURA", "AppAvon": "APP AVON CF"}


def _loja(mes, setor):
    """Volumetria e SLA contam só e-mails encerrados; o TMO é a média do tempo de operação."""
    return _um(f"""
        SELECT sum(CASE WHEN encerrado_em IS NOT NULL THEN 1 ELSE 0 END) AS vol,
               sum(CASE WHEN encerrado_em IS NOT NULL AND status_sla_email = 'Dentro do SLA' THEN 1 ELSE 0 END) AS d1,
               avg(tempo_operacao_em_segundos) AS tmo
        FROM {tabela('dexp_gold_mkt_emails_de_lojas')} WHERE setor = '{setor}' AND {_mes('data_contato', mes)}""")


def loja_mensal(mes, chave):
    r = _loja(mes, SETOR_LOJA[chave])
    vol = r.get("vol") or 0
    return {"Volumetria": inteiro(vol), "Tempo Médio Operacional (TMO)": _hms(r["tmo"]) if vol else "Sem dados"}


def loja_sla(mes, chave):
    r = _loja(mes, SETOR_LOJA[chave])
    vol, d1 = r.get("vol") or 0, r.get("d1") or 0
    if not vol:
        return {"SLA D+1": "Sem dados", "SLA >D+2": "Sem dados"}
    return {"SLA D+1": pct(d1, vol), "SLA >D+2": pct(vol - d1, vol)}


# --- CSAT (fonte Enquetes C-SAT, Experiencia Brasil) -----------------------------------------------------------------------
# A tabela tem uma linha por pergunta (slice) da enquete: contamos protocolos distintos.
# Só os setores do C-SAT (SETORES_CSAT; fica de fora o ATIVOS), como o C-SAT dos Indicadores Contratuais e a análise de
# qualidade dos detratores. Setembro/2026 foi gravado com todos os setores (88,22% × 88,97% nos Contratuais); corrigido a
# partir de outubro/2026 (decisão de 09/11/2026), sem alterar os meses fechados.

def _csat_base(mes):
    setores = ", ".join(f"'{s}'" for s in SETORES_CSAT)
    return (f"fonte = 'Experiencia Brasil' AND (exp_br_setor_fim IS NULL OR exp_br_setor_fim IN ({setores})) "
            f"AND {_mes('data', mes)}")


def csat_3meses(mes):
    r = _um(f"""
        SELECT count(DISTINCT protocolo) AS enviadas,
               count(DISTINCT CASE WHEN enquete_respondida = '1' THEN protocolo END) AS respondidas,
               count(DISTINCT CASE WHEN c_sat = 'PROMOTOR' THEN protocolo END) AS promotores
        FROM {tabela('dexp_gold_csat_enquetes')} WHERE {_csat_base(mes)}""")
    return {"C-SAT (%)": pct(r["promotores"], r["respondidas"]), "Enquetes Enviadas": inteiro(r["enviadas"]),
            "Enquetes Respondidas": inteiro(r["respondidas"]), "Response Rate (%)": pct(r["respondidas"], r["enviadas"])}


def csat_classificacao(mes):
    linhas = consultar(f"""SELECT c_sat, count(DISTINCT protocolo) AS n FROM {tabela('dexp_gold_csat_enquetes')}
                           WHERE {_csat_base(mes)} AND enquete_respondida = '1' GROUP BY c_sat""")
    n = {l["c_sat"]: float(l["n"]) for l in linhas}
    total = sum(n.values())
    return [{"Classificação C-SAT": nome.capitalize(), "Percentual (%)": pct(n.get(nome, 0), total)}
            for nome in ("PROMOTOR", "NEUTRO", "DETRATOR")]


ROTULOS_NOTA = {"5": "Totalmente Satisfeito", "4": "Satisfeito", "3": "Neutro", "2": "Insatisfeito", "1": "Totalmente Insatisfeito"}


def csat_nota(mes):
    linhas = consultar(f"""SELECT left(nota, 1) AS n, count(DISTINCT protocolo) AS vol FROM {tabela('dexp_gold_csat_enquetes')}
                           WHERE {_csat_base(mes)} AND enquete_respondida = '1' AND slice_numero = '1' GROUP BY 1""")
    vol = {l["n"]: float(l["vol"]) for l in linhas}
    return [{"Nota Avaliada": rotulo, "Volume de Respostas": inteiro(vol.get(k, 0))} for k, rotulo in ROTULOS_NOTA.items()]


MERCADOS_CSAT = ("AMAZÔNIA", "ARAUCÁRIA", "ATLÂNTICA", "CAATINGA", "CERRADO")


def csat_mercado(mes):
    linhas = consultar(f"""
        SELECT exp_br_mercado AS m, count(DISTINCT protocolo) AS resp,
               count(DISTINCT CASE WHEN c_sat = 'PROMOTOR' THEN protocolo END) AS prom
        FROM {tabela('dexp_gold_csat_enquetes')} WHERE {_csat_base(mes)} AND enquete_respondida = '1' GROUP BY 1""")
    x = {l["m"]: l for l in linhas}
    return [{"Mercado": m.capitalize(), "Nota": pct(float(x[m]["prom"]), float(x[m]["resp"])) if m in x else "-"}
            for m in MERCADOS_CSAT]


def csat_ofensores(mes):
    linhas = consultar(f"""
        SELECT exp_br_funcao_do_sistema AS f, count(DISTINCT protocolo) AS n FROM {tabela('dexp_gold_csat_enquetes')}
        WHERE {_csat_base(mes)} AND c_sat = 'DETRATOR' AND exp_br_funcao_do_sistema IS NOT NULL
        GROUP BY 1 ORDER BY 2 DESC, 1 LIMIT 3""")
    return [{"Ofensor Detrator": l["f"].capitalize(), "Volume de Casos": inteiro(float(l["n"]))} for l in linhas]


# --- Resenhas (fontes Resenhas Brasil, das lojas de aplicativo, e Resenhas EXP BR AppSheets, das respostas do time) -----

APPS_RESENHA = {"Minha_Consultoria": ("App Consultoria Natura", "Consultoria"), "FV": ("App Força de Vendas", "Força de Vendas"),
                "AppNatura": ("App Sempre Presente", "Sempre Presente"), "AppAvon": ("App Avon", "Avon")}


def _estrela(media):
    return "-" if media is None else f"{media:.1f}".replace(".", ",")


def resenhas_01(mes, app):
    """Média de estrelas do mês e média geral (todas as avaliações até o fim do mês)."""
    loja, _ = APPS_RESENHA[app]
    r = _um(f"""SELECT avg(CASE WHEN {_mes('data_avaliacao', mes)} THEN star_rating END) AS mes,
                       avg(CASE WHEN date_format(data_avaliacao, 'yyyy-MM') <= '{mes}' THEN star_rating END) AS geral
                FROM {tabela('dexp_gold_resenhas_brasil')} WHERE nome_aplicativo = '{loja}'""")
    return {"Classificação Mensal": _estrela(r["mes"]), "Consolidado Geral (★)": _estrela(r["geral"])}


def resenhas_02(mes, app):
    loja, _ = APPS_RESENHA[app]
    r = _um(f"""SELECT count(*) AS n FROM {tabela('dexp_gold_resenhas_brasil')}
                WHERE nome_aplicativo = '{loja}' AND {_mes('data_avaliacao', mes)}""")
    return {"Volumetria de Avaliação": inteiro(r["n"])}


def resenhas_03(mes, app):
    loja, _ = APPS_RESENHA[app]
    linhas = consultar(f"""SELECT star_rating AS e, count(*) AS n FROM {tabela('dexp_gold_resenhas_brasil')}
                           WHERE nome_aplicativo = '{loja}' AND {_mes('data_avaliacao', mes)} GROUP BY 1""")
    n = {str(int(float(l["e"]))): float(l["n"]) for l in linhas}
    return [{"Nota (Estrelas)": str(e), "Volume de Resenhas": inteiro(n.get(str(e), 0))} for e in range(1, 6)]


def _respostas(mes, app):
    _, nome = APPS_RESENHA[app]
    return f"app_nome = '{nome}' AND {_mes('data_avaliacao', mes)}"


def resenhas_04(mes, app):
    """SLA das respostas (AppSheets): D+1 = dentro do SLA."""
    r = _um(f"""SELECT count(*) AS n, sum(CASE WHEN status_sla = 'Dentro do SLA' THEN 1 ELSE 0 END) AS d
                FROM {tabela('dexp_gold_resenhas_appsheets')} WHERE {_respostas(mes, app)}""")
    n, d = r["n"] or 0, r["d"] or 0
    return {"SLA D+1": pct(d, n), "SLA >D+2": pct(n - d, n)}


def resenhas_05(mes, app):
    linhas = consultar(f"""SELECT categoria_da_resposta AS c, count(*) AS n FROM {tabela('dexp_gold_resenhas_appsheets')}
                           WHERE {_respostas(mes, app)} GROUP BY 1 ORDER BY 2 DESC""")
    return [{"Tipo de Comentário": l["c"] or "-", "Volume": inteiro(float(l["n"]))} for l in linhas]


def resenhas_06(mes, app):
    linhas = consultar(f"""SELECT categoria_da_resposta_2 AS c, count(*) AS n FROM {tabela('dexp_gold_resenhas_appsheets')}
                           WHERE {_respostas(mes, app)} AND categoria_da_resposta_2 IS NOT NULL GROUP BY 1 ORDER BY 2 DESC, 1""")
    return [{"Motivo da Reclamação": l["c"], "Volume": inteiro(float(l["n"]))} for l in linhas]


def resenhas_07(mes, app):
    """Texto: a linha das avaliações de 1 a 3 estrelas sai das respostas do AppSheets; as de 4 e 5 ainda não."""
    r = _um(f"SELECT count(*) AS n FROM {tabela('dexp_gold_resenhas_appsheets')} WHERE {_respostas(mes, app)}")
    return [{"Linha": "1", "Texto Integral do Comentário": f"Volume de resenhas respondidas: {A_INVESTIGAR} (linha 2 + linha 3)"},
            {"Linha": "2", "Texto Integral do Comentário":
                f"Das {inteiro(r['n'] or 0)} avaliações de 1 a 3 estrelas com comentários, 100% foram respondidas."},
            {"Linha": "3", "Texto Integral do Comentário": f"Das {A_INVESTIGAR} avaliações de 4 e 5 estrelas com comentários, 100% foram respondidas."}]


def _abas_resenhas():
    abas = {}
    for app in APPS_RESENHA:
        for n, f in (("01", resenhas_01), ("02", resenhas_02), ("03", resenhas_03), ("04", resenhas_04),
                     ("05", resenhas_05), ("06", resenhas_06), ("07", resenhas_07)):
            abas[f"Exp_Br_Resenhas_{app}_{n}"] = (lambda f, app: lambda m: f(m, app))(f, app)
    return abas


ABAS = {
    "Exp_Br_Indicadores_Contratuais": indicadores_contratuais,
    "Exp_Br_Indicadores_Monitoracao": indicadores_monitoracao,
    "Exp_Br_Cards01": cards01,
    "Exp_Br_Retencao": retencao,
    "Exp_Br_Cards2": cards2,
    "Exp_Br_Reativos_WA_Mensal": lambda m: _wa_mensal(m, SETORES_WA["Reativos"]),
    "Exp_Br_WA_GN_Mensal": lambda m: _wa_mensal(m, SETORES_WA["GN"]),
    "Exp_Br_WA_GV_Mensal": lambda m: _wa_mensal(m, SETORES_WA["GV"]),
    "Exp_Br_WA_Franq_Mensal": lambda m: _wa_mensal(m, SETORES_WA["Franq"]),
    "Exp_Br_WA_CBCom_Mensal": lambda m: _wa_mensal(m, SETORES_WA["CBCom"]),
    "Exp_Br_Email_Mensal": email_mensal,
    "Exp_Br_Email_TMO": email_tmo,
    "Exp_Br_Tarefas_Historico_Mensal": lambda m: tarefas_mensal(m, "Total"),
    "Exp_Br_Tarefas_CB_Mensal": lambda m: tarefas_mensal(m, "CB"),
    "Exp_Br_Tarefas_CF_Mensal": lambda m: tarefas_mensal(m, "CF"),
    "Exp_Br_Tarefas_CB_Fase": lambda m: tarefas_fase(m, "CB"),
    "Exp_Br_Tarefas_CF_Fase": lambda m: tarefas_fase(m, "CF"),
    "Exp_Br_ReqEvent_Mensal": reqevent_mensal,
    "Exp_Br_Reativos_WA_Motivos_N1": lambda m: motivos_wa(m, SETORES_WA["Reativos"], "N1"),
    "Exp_Br_Reativos_WA_Motivos_N2": lambda m: motivos_wa(m, SETORES_WA["Reativos"], "N2"),
    "Exp_Br_WA_GN_Motivos_N1": lambda m: motivos_wa(m, SETORES_WA["GN"], "N1"),
    "Exp_Br_WA_GN_Motivos_N2": lambda m: motivos_wa(m, SETORES_WA["GN"], "N2"),
    "Exp_Br_WA_GV_Motivos_N1": lambda m: motivos_wa(m, SETORES_WA["GV"], "N1"),
    "Exp_Br_WA_GV_Motivos_N2": lambda m: motivos_wa(m, SETORES_WA["GV"], "N2"),
    "Exp_Br_WA_Franq_Motivos_N1": lambda m: motivos_wa(m, SETORES_WA["Franq"], "N1"),
    "Exp_Br_WA_Franq_Motivos_N2": lambda m: motivos_wa(m, SETORES_WA["Franq"], "N2"),
    "Exp_Br_WA_CBCom_Motivos_N1": lambda m: motivos_wa(m, SETORES_WA["CBCom"], "N1"),
    "Exp_Br_WA_CBCom_Motivos_N2": lambda m: motivos_wa(m, SETORES_WA["CBCom"], "N2"),
    "Exp_Br_Email_Motivos_N1": lambda m: motivos_email(m, "N1"),
    "Exp_Br_Email_Motivos_N2": lambda m: motivos_email(m, "N2"),
    "Exp_Br_Tarefas_CB_Motivo_N1": lambda m: motivos_tarefas(m, "CB", "N1"),
    "Exp_Br_Tarefas_CB_Motivo_N2": lambda m: motivos_tarefas(m, "CB", "N2"),
    "Exp_Br_Tarefas_CF_Motivo_N1": lambda m: motivos_tarefas(m, "CF", "N1"),
    "Exp_Br_Tarefas_CF_Motivo_N2": lambda m: motivos_tarefas(m, "CF", "N2"),
    "Exp_Br_Proativos_Mensal": proativos_mensal,
    "Exp_Br_Proativos_Contatos_Pedidos": proativos_contatos_pedidos,
    "Exp_Br_Proativos_HC_Mensal": proativos_hc_mensal,
    "Exp_Br_Email_Natura_Expcb_Mensal": lambda m: loja_mensal(m, "Natura_Expcb"),
    "Exp_Br_Email_Natura_Expcb_SLA": lambda m: loja_sla(m, "Natura_Expcb"),
    "Exp_Br_Email_AppNatura_Mensal": lambda m: loja_mensal(m, "AppNatura"),
    "Exp_Br_Email_AppNatura_SLA": lambda m: loja_sla(m, "AppNatura"),
    "Exp_Br_Email_AppAvon_Mensal": lambda m: loja_mensal(m, "AppAvon"),
    "Exp_Br_Email_AppAvon_SLA": lambda m: loja_sla(m, "AppAvon"),
    "Exp_Br_CSAT_3Meses": csat_3meses,
    "Exp_Br_CSAT_Classificacao": csat_classificacao,
    "Exp_Br_CSAT_Nota": csat_nota,
    "Exp_Br_CSAT_Mercado": csat_mercado,
    "Exp_Br_CSAT_Ofensores_Detr": csat_ofensores,
    **_abas_resenhas(),
}
