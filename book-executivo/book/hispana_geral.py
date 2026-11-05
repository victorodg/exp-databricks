"""Planilha "Book Executivo" (a geral, lida pelo Apps Script como EXECUTIVO_SS_ID): Hispana consolidada (abas "OIs"),
Mercado Andino (Colômbia, Equador e Peru), CSAT e indicadores da Hispana.

Reaproveita as regras de book/hispana.py (as mesmas dos painéis Daily da Hispana). Nesta planilha os países aparecem
em português ("Colômbia", "Equador", "México") e a comparação com o mês anterior leva "%" ("+1,15% p.p.").
"""
from .databricks import consultar, tabela
from .formatos import _br, inteiro, pct, reais
from . import hispana as h
from .hispana import A_INVESTIGAR, MANUAL, MERCADOS

NOME = {"Argentina": "Argentina", "Chile": "Chile", "Colombia": "Colômbia", "Ecuador": "Equador", "Mexico": "México",
        "Peru": "Peru"}
BANDEIRA = {"Colombia": "Colômbia 🇨🇴", "Ecuador": "Equador 🇪🇨", "Peru": "Peru 🇵🇪"}
TIPOS = h.TIPOS


def _desempenho(mes, paises):
    atual, anterior = h._por_pais(mes, paises), h._por_pais(h._mes_anterior(mes), paises)
    linhas = []
    for p in paises:
        a = h._soma(atual, (p,), ("WhatsApp",), "dentro"), h._soma(atual, (p,), ("WhatsApp",), "fora")
        b = h._soma(anterior, (p,), ("WhatsApp",), "dentro"), h._soma(anterior, (p,), ("WhatsApp",), "fora")
        if not sum(a) or not sum(b):
            comp = "-"
        else:
            dif = round(100 * a[0] / sum(a), 2) - round(100 * b[0] / sum(b), 2)
            comp = ("+" if dif >= 0 else "-") + _br(abs(dif), 2) + "% p.p. em relação ao mês anterior"
        linhas.append({"País": NOME[p], "SLA": pct(a[0], sum(a)), "Comparativo / Observação": comp})
    return linhas


def _pais(mes, ordem):
    """Aba por país (coluna A = país, B = mês). Volumetria = WhatsApp + e-mail, como a fórmula da planilha."""
    d = h._por_pais(mes, ordem)
    return [{"País": NOME[p], "Volumetria Total": inteiro(h._soma(d, (p,), ("WhatsApp", "Email"), "vol")),
             "WhatsApp (Vol)": inteiro(h._soma(d, (p,), ("WhatsApp",), "vol")),
             "E-mail (Vol)*": inteiro(h._soma(d, (p,), ("Email",), "vol")),
             "SLA WhatsApp": h._sla(d, (p,)), "N1 Dentro do Prazo": h._retencao(d, (p,))} for p in ordem]


def _tma(mes, ordem):
    return [{"País": NOME[p], "TMA E-mail": h._tma(mes, (p,))} for p in ordem]


def _causa_raiz(mercado, mes, nivel, por_pais):
    saida = []
    for p, t, pp, m, v in h._motivos(mercado, mes, (nivel,)):
        r = {"Plataforma": h._limpo(p), "Volume Total": inteiro(t)}
        if por_pais:
            r.update({f"Vol {NOME[x]}": inteiro(pp[x]) for x in MERCADOS[mercado]})
        r.update({f"Motivo Causa Raiz ({nivel})": h._frase(m), "Volume Motivo": inteiro(v), "Percentual (%)": pct(v, t)})
        saida.append(r)
    return saida


# --- Mercado Andino (abas Exp_Hisp_Pag_4/5/6_Mercado_Andino_*) ---------------------------------------------------------

AND = MERCADOS["andino"]


def andino_vol_retencao(mes):
    d = h._por_pais(mes, AND)
    r = {"Volumetria Total": inteiro(h._soma(d, AND, TIPOS, "vol"))}
    r.update({f"{NOME[p]} (Vol)": inteiro(h._soma(d, (p,), TIPOS, "vol")) for p in AND})
    r["Retenção N1"] = h._retencao(d, AND)
    return r


def andino_cards(mes):
    d, ped = h._por_pais(mes, AND), h._pedidos(mes, AND)
    r = {"Valor de pedido convertido (Geral)": reais(sum(v for _, v in ped.values())),
         "Quantidade de pedidos convertidos": inteiro(sum(q for q, _ in ped.values())),
         "Volume de Casos Recebidos WhatsApp": inteiro(h._soma(d, AND, ("WhatsApp",), "vol")),
         "Volume de E-mails Recebidos": inteiro(h._soma(d, AND, ("Email",), "vol")),
         "Health Check": A_INVESTIGAR,
         "Acionamentos Recebidos nos Grupos": inteiro(h._soma(d, AND, ("Requisições",), "vol"))}
    r.update({f"Pedidos Convertidos - {BANDEIRA[p]}": reais(ped.get(p, (0, 0))[1]) for p in AND})
    r.update({"SLA Geral do Mercado Andino (Texto)": A_INVESTIGAR, "Soporte Experiencia": A_INVESTIGAR,
              "Atendimentos Líderes Equador": A_INVESTIGAR, "Comentarios": MANUAL})
    return r


def _csat_classificacao_qtd(mes, paises):
    """No Andino a aba de classificação traz quantidades (protocolos), não percentuais."""
    r = h._csat_contagem(mes, paises).get("total", {})
    return [{"Classificação C-SAT": n, "Percentual (%)": inteiro(r.get(k, 0))}
            for n, k in (("Promotor", "promotor"), ("Neutro", "neutro"), ("Detrator", "detrator"))]


ABAS_ANDINO = {
    "Exp_Hisp_Pag_4_Mercado_Andino_Vol_Retencao": andino_vol_retencao,
    "Exp_Hisp_Pag_4_Mercado_Andino_Cards": andino_cards,
    "Exp_Hisp_Pag_5_Mercado_Andino_Cards": lambda m: h.cards2("andino", m),
    "Exp_Hisp_Pag_5_Mercado_Andino_Desempenho_Pais": lambda m: _desempenho(m, AND),
    "Exp_Hisp_Pag_5_Mercado_Andino_Top3_Motivo_Contato": lambda m: h.top3_motivo_contato("andino", m),
    "Exp_Hisp_Pag_5_Mercado_Andino_Solicitacoes_Dia": lambda m: h.solicitacoes_dia("andino", m),
    "Exp_Hisp_Pag_6_Mercado_Andino_Pais": lambda m: _pais(m, ("Ecuador", "Colombia", "Peru")),
    "Exp_Hisp_Pag_6_Mercado_Andino_TMA": lambda m: _tma(m, ("Ecuador", "Colombia", "Peru")),
    "Exp_Hisp_Pag_6_Mercado_Andino_Causa_Raiz_N1": lambda m: _causa_raiz("andino", m, "N1", True),
    "Exp_Hisp_Pag_6_Mercado_Andino_Causa_Raiz_N2": lambda m: _causa_raiz("andino", m, "N2", True),
    "Exp_Hisp_Pag_6_Mercado_Andino_CSAT_3_Meses": lambda m: h.csat_3_meses("andino", m),
    "Exp_Hisp_Pag_6_Mercado_Andino_CSAT_Classificacao": lambda m: _csat_classificacao_qtd(m, AND),
    "Exp_Hisp_Pag_6_Mercado_Andino_CSAT_Nota": lambda m: h.csat_nota("andino", m),
    "Exp_Hisp_Pag_6_Mercado_Andino_CSAT_Ofensores_Detr": lambda m: h.csat_ofensores_detr("andino", m),
    "Exp_Hisp_Pag_6_Mercado_Andino_CSAT_Paises_3_Meses": lambda m: [
        dict(r, Pais=NOME[p]) for p, r in zip(AND, h.csat_paises_3_meses("andino", m))],
    "Exp_Hisp_Pag_6_Mercado_Andino_CSAT_Paises_Classifi": lambda m: [
        dict(r, Pais=NOME.get(r["Pais"], r["Pais"])) for r in h.csat_paises_classifi("andino", m)],
    "Exp_Hisp_Pag_6_Mercado_Andino_CSAT_Paises_Notas": lambda m: [
        dict(r, Pais=NOME.get(r["Pais"], r["Pais"])) for r in h.csat_paises_notas("andino", m)],
    "Exp_Hisp_Pag_6_Mercado_Andino_CSAT_Paises_Ofensor": lambda m: [
        dict(r, Pais=NOME.get(r["Pais"], r["Pais"])) for r in h.csat_paises_ofensor("andino", m)],
}


# --- Hispana consolidada (abas Exp_Hisp_OIs_*, CSAT e indicadores) ---------------------------------------------------

HIS = MERCADOS["hispana"]


def ois_cards1(mes):
    d, ped = h._por_pais(mes, HIS), h._pedidos(mes, HIS)
    return {"Valor de pedido convertido": reais(sum(v for _, v in ped.values())),
            "Pedidos convertidos": inteiro(sum(q for q, _ in ped.values())),
            "Volume de Casos Recebidos WhatsApp": inteiro(h._soma(d, HIS, ("WhatsApp",), "vol")),
            "Volume de E-mails Recebidos": inteiro(h._soma(d, HIS, ("Email",), "vol")),
            "Health Check": A_INVESTIGAR,
            "Acionamentos Recebidos nos Grupos": inteiro(h._soma(d, HIS, ("Requisições",), "vol")),
            "Resenhas 1 a 3": A_INVESTIGAR, "Resenhas 4 e 5": A_INVESTIGAR, "E-mails Loja": A_INVESTIGAR,
            "Soporte Experiencia": A_INVESTIGAR, "Atendimentos Líderes Equador": A_INVESTIGAR, "Comentários": MANUAL}


def ois_vol(mes):
    d = h._por_pais(mes, HIS)
    return {"Volumetria Total": inteiro(h._soma(d, HIS, TIPOS, "vol")),
            "WhatsApp": inteiro(h._soma(d, HIS, ("WhatsApp",), "vol")),
            "E-mail": inteiro(h._soma(d, HIS, ("Email",), "vol")),
            "Requisicoes": inteiro(h._soma(d, HIS, ("Requisições",), "vol")),
            "Retenção N1": h._retencao(d, HIS)}


def _csat_hispana_base(mes):
    """CSAT consolidado: todas as enquetes da fonte Hispana (inclui o país "Latam")."""
    return f"{tabela('dexp_gold_csat_enquetes')} WHERE fonte = 'Hispana' AND {h._mes('data', mes)}"


def csat_hispana(mes):
    r = consultar(f"""SELECT count(DISTINCT protocolo) AS enviadas,
                             count(DISTINCT CASE WHEN enquete_respondida = 1 THEN protocolo END) AS respondidas,
                             count(DISTINCT CASE WHEN c_sat = 'PROMOTOR' THEN protocolo END) AS promotor,
                             count(DISTINCT CASE WHEN c_sat = 'NEUTRO' THEN protocolo END) AS neutro,
                             count(DISTINCT CASE WHEN c_sat = 'DETRATOR' THEN protocolo END) AS detrator
                      FROM {_csat_hispana_base(mes)}""")[0]
    return {k: h._f(v) for k, v in r.items()}


def csat_3meses(mes):
    r = csat_hispana(mes)
    return {"C-SAT (%)": pct(r["promotor"], r["respondidas"]), "Enquetes Enviadas": inteiro(r["enviadas"]),
            "Enquetes Respondidas": inteiro(r["respondidas"]), "Response Rate (%)": pct(r["respondidas"], r["enviadas"])}


def csat_classificacao(mes):
    return [{"Classificação C-SAT": n, "Percentual (%)": v} for n, v in h._classificacao(csat_hispana(mes))]


def csat_nota(mes):
    linhas = consultar(f"""SELECT left(nota, 1) AS n, count(DISTINCT protocolo) AS vol FROM {_csat_hispana_base(mes)}
                           AND enquete_respondida = 1 AND slice_numero = 1 GROUP BY 1""")
    v = {l["n"]: h._f(l["vol"]) for l in linhas}
    return [{"Nota Avaliada": rot, "Volume de Respostas": inteiro(v.get(k, 0))} for k, rot in h.ROTULOS_NOTA.items()]


def csat_ofensores(mes):
    linhas = consultar(f"""
        SELECT ois_funcao_do_sistema AS f, count(DISTINCT protocolo) AS n FROM {_csat_hispana_base(mes)}
          AND c_sat = 'DETRATOR' AND ois_funcao_do_sistema IS NOT NULL
        GROUP BY 1 ORDER BY 2 DESC, 1 LIMIT 3""")
    return [{"Ofensor Detrator": h._frase(l["f"]), "Volume de Casos": inteiro(h._f(l["n"]))} for l in linhas]


# Monitoração: TMO dos tickets de e-mail concluídos no mês (painel TMO, fonte MKT Hispana Completo), em dias
TMO_STATUS = {"TMR - SLA de Resolução N2 -E-mail (origem whatsapp)": ("Resuelto N2 MKT",),
              "TMR - SLA de Resolução N3 -E-mail (origem whatsapp)": ("Resuelto MKT N3",),
              "TMR - SLA de Resolução N2 -E-mail (origem e-mail)": ("Resuelto N2 E-mail",),
              "TMR - SLA de Resolução N3 -E-mail (origem e-mail)": ("N3 – E-mail – Pendientes – JIRA",)}


def indicadores_monitoracao(mes):
    r = {"TPA - Tempo de Primeiro Atendimento - Atendimento Resenhas": A_INVESTIGAR}
    for col, status in TMO_STATUS.items():
        x = consultar(f"""SELECT avg(tempo_segundos) AS s FROM {tabela('dexp_gold_hispana_completo')}
                          WHERE situacao = 'Concluído' AND status IN ({h._lista(status)})
                            AND {h._mes('data_conclusao', mes)}""")[0]["s"]
        r[col] = A_INVESTIGAR if not x else _br(h._f(x) / 86400, 1) + " dias"
    return r


def indicadores_contratuais(mes):
    d, ped, c = h._por_pais(mes, HIS), h._pedidos(mes, HIS), csat_hispana(mes)
    return {"TPR - Tempo de Primeira Resposta - Atendimento Gerentes": h._sla(d, HIS),
            "TMR - SLA de Resolução -E-mail (N1)": A_INVESTIGAR, "Notificação de Incidente": MANUAL,
            "Retenção em N1": h._retencao(d, HIS), "CSAT": pct(c["promotor"], c["respondidas"]),
            "Quality Assurance": MANUAL, "Pedidos convertidos": inteiro(sum(q for q, _ in ped.values())),
            "Valor de pedido convertido": reais(sum(v for _, v in ped.values()))}


ORDEM_DESEMPENHO = ("Colombia", "Mexico", "Ecuador", "Peru", "Argentina", "Chile")
ORDEM_PAIS = ("Argentina", "Ecuador", "Chile", "Mexico", "Colombia", "Peru")

ABAS_HISPANA = {
    "Exp_Hisp_Indicadores_Contratuais": indicadores_contratuais,
    "Exp_Hisp_Indicadores_Monitoracao": indicadores_monitoracao,
    "Exp_Hisp_OIs_Pag_1_Cards": ois_cards1,
    "Exp_Hisp_OIs_Pag_1_Vol_WA_Email_Retencao": ois_vol,
    "Exp_Hisp_OIs_Pag_2_Cards": lambda m: h.cards2("hispana", m),
    "Exp_Hisp_OIs_Pag_2_Desempenho_Pais": lambda m: _desempenho(m, ORDEM_DESEMPENHO),
    "Exp_Hisp_OIs_Pag_2_Tabela_Solicitacoes_Dia": lambda m: h.solicitacoes_dia("hispana", m),
    "Exp_Hisp_OIs_Pag_2_Top3_Motivos_Contato": lambda m: [
        {"Plataforma": r["Plataforma"], "Volume Total Plataforma": r["Volume Total Plataforma"],
         "Motivo do Contato": r["Motivo do Contato"], "Volume Motivo": r["Volume do Motivo"],
         "Percentual (%)": r["Percentual (%)"]} for r in h.top3_motivo_contato("hispana", m)],
    "Exp_Hisp_OIs_Pag_3_Total_Pais": lambda m: _pais(m, ORDEM_PAIS),
    "Exp_Hisp_OIs_Pag_3_TMA": lambda m: _tma(m, ORDEM_PAIS),
    "Exp_Hisp_OIs_Pag_3_Causa_Raiz": lambda m: [
        {"Plataforma": r["Plataforma"], "Volume Total Plataforma": r["Volume Total"],
         "Motivo Causa Raiz (N2)": r["Motivo Causa Raiz (N2)"], "Volume do Motivo": r["Volume Motivo"],
         "Percentual (%)": r["Percentual (%)"]} for r in _causa_raiz("hispana", m, "N2", False)],
    "Exp_Hisp_CSAT_3Meses": csat_3meses,
    "Exp_Hisp_CSAT_Classificacao": csat_classificacao,
    "Exp_Hisp_CSAT_Nota": csat_nota,
    "Exp_Hisp_CSAT_Ofensores_Detr": csat_ofensores,
}

# --- Resenhas (fontes Resenhas OIS, das lojas, e AppSheets Resenhas OIs, das respostas do time) ----------------------
# A planilha chama de "Mi Negocio", "Natura Latam" e "App Avon"; na base: table_names / aplicacion

APPS = {"Mi_Negocio": ("Mi Negocio", "Mi Negocio"), "Natura_Latam": ("Resenhas Latam", "Resenhas Latam"),
        "App_Avon": ("App Avon", "App_Avon")}


def _estrela(x):
    return "-" if x is None else _br(x, 2)


def _loja(app, mes):
    return f"""{tabela('dexp_gold_hispana_resenhas')} WHERE table_names = '{APPS[app][0]}'
               AND {h._mes('review_submit_date_and_time', mes)}"""


def _resp(app, mes):
    return f"""{tabela('dexp_gold_hispana_appsheets_resenhas')} WHERE aplicacion = '{APPS[app][1]}'
               AND {h._mes('fecha_de_la_respuesta_original', mes)}"""


def resenhas_01(app, mes):
    r = consultar(f"""SELECT avg(CASE WHEN {h._mes('review_submit_date_and_time', mes)} THEN star_rating END) AS mes,
                             avg(CASE WHEN date_format(review_submit_date_and_time, 'yyyy-MM') <= '{mes}' THEN star_rating END) AS geral
                      FROM {tabela('dexp_gold_hispana_resenhas')} WHERE table_names = '{APPS[app][0]}'""")[0]
    return {"Classificação Mensal": _estrela(h._f(r["mes"]) if r["mes"] else None),
            "Consolidado Geral (★)": _estrela(h._f(r["geral"]) if r["geral"] else None)}


def resenhas_02(app, mes):
    return {"Volumetria de Avaliação": inteiro(h._f(consultar(f"SELECT count(*) AS n FROM {_loja(app, mes)}")[0]["n"]))}


def resenhas_03(app, mes):
    n = {str(l["e"]): h._f(l["n"]) for l in consultar(f"SELECT star_rating AS e, count(*) AS n FROM {_loja(app, mes)} GROUP BY 1")}
    return [{"Nota (Estrelas)": str(e), "Volume de Resenhas": inteiro(n.get(str(e), 0))} for e in range(1, 6)]


def resenhas_05(app, mes):
    linhas = consultar(f"""SELECT categoria_de_la_respuesta AS c, count(*) AS n FROM {_resp(app, mes)}
                           AND categoria_de_la_respuesta IS NOT NULL AND categoria_de_la_respuesta <> '-'
                           GROUP BY 1 ORDER BY 2 DESC, 1""")
    return [{"Tipo de Comentário": l["c"], "Volume": inteiro(h._f(l["n"]))} for l in linhas]


def resenhas_06(app, mes):
    linhas = consultar(f"""SELECT categoria_de_la_respuesta_2 AS c, count(*) AS n FROM {_resp(app, mes)}
                           AND categoria_de_la_respuesta_2 IS NOT NULL GROUP BY 1 ORDER BY 2 DESC, 1""")
    return [{"Motivo da Reclamação": l["c"], "Volume": inteiro(h._f(l["n"]))} for l in linhas]


def resenhas_07(app, mes):
    n = h._f(consultar(f"SELECT count(*) AS n FROM {_resp(app, mes)}")[0]["n"])
    return [{"Linha": "1", "Texto Integral do Comentário": A_INVESTIGAR},
            {"Linha": "2", "Texto Integral do Comentário":
                f"Das {int(n):02d} avaliações de 1 a 3 estrelas com comentários, 100% foram respondidas."},
            {"Linha": "3", "Texto Integral do Comentário": A_INVESTIGAR}]


ABAS_RESENHAS = {}
for _app in APPS:
    # 04, 05, 06, 08, 09 e 10 ainda sem regra que bata com setembro (ver README)
    for _n, _f in (("01", resenhas_01), ("02", resenhas_02), ("03", resenhas_03), ("07", resenhas_07)):
        ABAS_RESENHAS[f"Exp_Hisp_Resenhas_{_app}_{_n}"] = (lambda f, a: lambda m: f(a, m))(_f, _app)

ABAS = {**ABAS_HISPANA, **ABAS_ANDINO, **ABAS_RESENHAS}
# Nas abas abaixo a coluna A é o país e a B é o mês
PAIS_PRIMEIRO = ("Exp_Hisp_OIs_Pag_3_Total_Pais", "Exp_Hisp_Pag_6_Mercado_Andino_Pais",
                 "Exp_Hisp_Pag_6_Mercado_Andino_CSAT_Paises_3_Meses")
