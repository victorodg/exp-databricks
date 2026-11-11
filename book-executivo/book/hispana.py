"""Book Executivo Hispana (planilhas "Book Executivo Hispana Mexico" e "Book Executivo Hispana Sur"): uma função por aba.

As regras reproduzem as planilhas dos painéis "Daily Mexico OIS" e "Experiência Hispana Sur - Daily" (Tableau Cloud),
lendo as tabelas gold do Databricks (dexp_gold_hispana_*, dexp_gold_csat_enquetes), que são cópias das fontes publicadas.

Nível consolidado (cálculo "Nivel Consolidado" do painel): a partir de março/2026 o e-mail conta pelas linhas do
MKT Completo; WhatsApp, Requisições (grupos) e e-mails anteriores contam pelas linhas do MKT Analítico. Só entram os
níveis N1, N2 e Neutro, e o mês é o da data de contato.
"""
from .databricks import consultar, tabela
from .formatos import _br, inteiro, pct, reais

MANUAL = "manual"
A_INVESTIGAR = "a investigar"

MERCADOS = {"mexico": ("Mexico",), "sur": ("Argentina", "Chile"), "andino": ("Colombia", "Ecuador", "Peru"),
            "hispana": ("Argentina", "Chile", "Colombia", "Ecuador", "Mexico", "Peru")}
# A planilha do Sur lista os países nesta ordem em Desempenho_Pais
ORDEM_DESEMPENHO = {"mexico": ("Mexico",), "sur": ("Chile", "Argentina")}
# Algumas abas escrevem o México com acento
ACENTO = {"Mexico": "México"}

# Planilha "Estatus de Classificacion - General2": exclui as filas de acompanhamento
ACOMPANHAMENTO = ("N2 - E-mail - En acompañamiento TD", "N2 - WhatsApp - EN ACOMPAÑAMIENTO TD",
                  "N3 – E-mail – Pendientes – JIRA")


def _lista(valores):
    return ", ".join("'" + v.replace("'", "''") + "'" for v in valores)


def _mes(coluna, mes):
    return f"date_format({coluna}, 'yyyy-MM') = '{mes}'"


def _base(mes, paises):
    """Atendimentos do mês que entram no nível consolidado."""
    return f"""{tabela('dexp_gold_hispana_base_mkt')}
        WHERE pais IN ({_lista(paises)}) AND {_mes('data_contato', mes)} AND nivel IN ('N1', 'N2', 'Neutro')
          AND CASE WHEN tipo = 'Email' AND data_hibrida_do_dashboard >= '2026-03-01' THEN origem_da_linha = 'MKT Completo'
                   ELSE origem_da_linha = 'MKT Analítico' END"""


def _mes_anterior(mes):
    a, m = map(int, mes.split("-"))
    return f"{a - 1}-12" if m == 1 else f"{a}-{m - 1:02d}"


def _hms(segundos):
    if segundos is None:
        return "-"
    s = int(segundos)
    return f"{s // 3600:02d}:{s % 3600 // 60:02d}:{s % 60:02d}"


def _f(v):
    return float(v) if v not in (None, "") else 0.0


def _limpo(texto):
    """Troca hífens e sublinhados por espaço ("PEDIDO-GERA-ERROR_INVALID" -> "PEDIDO GERA ERROR INVALID")."""
    return " ".join(texto.replace("_", " ").replace(" - ", " ").replace("-", " ").split()) if texto else texto


def _frase(texto):
    """Nome de motivo como frase ("REGISTRO - APROBADO" -> "Registro aprobado")."""
    texto = _limpo(texto)
    return texto[:1].upper() + texto[1:].lower() if texto else texto


# --- Volumes, níveis e SLA por país -----------------------------------------------------------------------------------

def _por_pais(mes, paises):
    linhas = consultar(f"""
        SELECT pais, tipo,
               sum(valor_atendimento) AS vol,
               sum(CASE WHEN nivel = 'N1' THEN valor_atendimento ELSE 0 END) AS n1,
               sum(CASE WHEN nivel = 'N2' THEN valor_atendimento ELSE 0 END) AS n2
        FROM {_base(mes, paises)}
        GROUP BY pais, tipo""")
    d = {}
    for l in linhas:
        d[(l["pais"], l["tipo"])] = {k: _f(l[k]) for k in ("vol", "n1", "n2")}
    # SLA (planilha "Tabela WhatsApp" do painel Consolidado): linhas de WhatsApp do MKT Analítico, sem filtro de nível;
    # conta linhas dentro e fora do SLA com expurgo (as linhas sem SLA ficam de fora)
    for l in consultar(f"""
        SELECT pais, sum(CASE WHEN sla_com_expurgo = 'Dentro do SLA' THEN 1 ELSE 0 END) AS dentro,
               sum(CASE WHEN sla_com_expurgo = 'Fora do SLA' THEN 1 ELSE 0 END) AS fora
        FROM {tabela('dexp_gold_hispana_base_mkt')}
        WHERE pais IN ({_lista(paises)}) AND {_mes('data_contato', mes)} AND tipo = 'WhatsApp'
          AND origem_da_linha = 'MKT Analítico'
        GROUP BY pais"""):
        d.setdefault((l["pais"], "WhatsApp"), {"vol": 0, "n1": 0, "n2": 0}).update(dentro=_f(l["dentro"]), fora=_f(l["fora"]))
    return d


def _soma(d, paises, tipos, campo):
    return sum(d.get((p, t), {}).get(campo, 0) for p in paises for t in tipos)


TIPOS = ("WhatsApp", "Email", "Requisições")


def _retencao(d, paises, tipos=TIPOS):
    n1, n2 = _soma(d, paises, tipos, "n1"), _soma(d, paises, tipos, "n2")
    return pct(n1, n1 + n2)


def _sla(d, paises):
    dentro, fora = _soma(d, paises, ("WhatsApp",), "dentro"), _soma(d, paises, ("WhatsApp",), "fora")
    return pct(dentro, dentro + fora)


def _tma(mes, paises):
    """TMA de e-mail: média do tempo de operação dos e-mails N1 e N2 do MKT Analítico.
    Regra provável: em setembro Chile bate por 1 minuto e Argentina por 18; o México não confere porque os e-mails de
    setembro mudaram depois do preenchimento."""
    r = consultar(f"""SELECT avg(tempo_de_operacao_segundos) AS s FROM {tabela('dexp_gold_hispana_base_mkt')}
                      WHERE pais IN ({_lista(paises)}) AND {_mes('data_contato', mes)} AND tipo = 'Email'
                        AND origem_da_linha = 'MKT Analítico' AND nivel IN ('N1', 'N2')""")
    return _hms(_f(r[0]["s"]) if r and r[0]["s"] else None)


def _pedidos(mes, paises):
    """Pedidos convertidos: LINHAS com pedido finalizado no MKT Analítico; valor = quantidade x ticket médio do país no
    mês (fonte Ticket Medio Hispana).

    Regra do painel (planilha "Tabela Pedidos Convertidos", fonte Base MKT OIS):
    [Pedidos Convertidos (Qtd)] = IF [Pedidos Finalizados] = "SI" THEN 1 END, somado por país e mês. Conta linhas (não
    soma "Cant. de Atendimientos") e a comparação do Tableau não diferencia maiúsculas: a base tem "SI" e "Si".
    Corrigido em 05/11/2026: set/2026 passou a bater país a país com o Book (4.744 / R$ 2.797.575,83) e out/2026 dá
    4.892 / R$ 3.185.569,25, o número da planilha da Juliana. Antes o programa somava valor_atendimento só de "SI".
    """
    linhas = consultar(f"""
        SELECT b.pais, sum(CASE WHEN upper(trim(b.pedidos_finalizados)) = 'SI' THEN 1 ELSE 0 END) AS qtd,
               max(t.valor_por_pedido) AS ticket
        FROM {tabela('dexp_gold_hispana_base_mkt')} b
        LEFT JOIN {tabela('dexp_gold_hispana_ticket_medio')} t ON t.pais = b.pais AND {_mes('t.data_contato', mes)}
        WHERE b.pais IN ({_lista(paises)}) AND {_mes('b.data_contato', mes)} AND b.origem_da_linha = 'MKT Analítico'
        GROUP BY b.pais""")
    return {l["pais"]: (_f(l["qtd"]), _f(l["qtd"]) * _f(l["ticket"])) for l in linhas}


def vol_retencao(mercado, mes):
    paises = MERCADOS[mercado]
    d = _por_pais(mes, paises)
    r = {"Volumetria Total": inteiro(_soma(d, paises, TIPOS, "vol"))}
    if len(paises) > 1:
        for p in paises:
            r[f"{p} (Vol)"] = inteiro(_soma(d, (p,), TIPOS, "vol"))
    r["Retenção N1"] = _retencao(d, paises)
    return r


def cards1(mercado, mes):
    paises = MERCADOS[mercado]
    d = _por_pais(mes, paises)
    ped = _pedidos(mes, paises)
    r = {"Valor de pedido convertido (Geral)": reais(sum(v for _, v in ped.values())),
         "Quantidade de pedidos convertidos": inteiro(sum(q for q, _ in ped.values())),
         "Volume de Casos Recebidos WhatsApp": inteiro(_soma(d, paises, ("WhatsApp",), "vol")),
         "Volume de E-mails Recebidos": inteiro(_soma(d, paises, ("Email",), "vol")),
         "Health Check": A_INVESTIGAR,  # vem da planilha "Healthcheck Paises Consolidado", que não está no Databricks
         "Acionamentos Recebidos nos Grupos": inteiro(_soma(d, paises, ("Requisições",), "vol"))}
    if len(paises) > 1:
        bandeira = {"Argentina": "Argentina 🇦🇷", "Chile": "Chile 🇨🇱"}
        for p in paises:
            r[f"Pedidos Convertidos - {bandeira.get(p, p)}"] = reais(ped.get(p, (0, 0))[1])
    r["SLA WhatsApp Global"] = _sla(d, paises)
    r["Comentarios"] = MANUAL
    return r


def cards2(mercado, mes):
    paises = MERCADOS[mercado]
    d = _por_pais(mes, paises)
    return {"SLA WhatsApp": _sla(d, paises), "TMA E-mail": _tma(mes, paises),
            "Retenção WhatsApp": _retencao(d, paises, ("WhatsApp",)),
            "Retenção E-mail": _retencao(d, paises, ("Email",)),
            "Volumetria Total": inteiro(_soma(d, paises, TIPOS, "vol"))}


def desempenho_pais(mercado, mes):
    paises = ORDEM_DESEMPENHO[mercado]
    atual, anterior = _por_pais(mes, paises), _por_pais(_mes_anterior(mes), paises)
    linhas = []
    for p in paises:
        a = _soma(atual, (p,), ("WhatsApp",), "dentro"), _soma(atual, (p,), ("WhatsApp",), "fora")
        b = _soma(anterior, (p,), ("WhatsApp",), "dentro"), _soma(anterior, (p,), ("WhatsApp",), "fora")
        sla_a, sla_b = 100 * a[0] / sum(a) if sum(a) else None, 100 * b[0] / sum(b) if sum(b) else None
        if sla_a is None or sla_b is None:
            comp = "-"
        else:
            dif = round(sla_a, 2) - round(sla_b, 2)
            comp = ("+" if dif >= 0 else "-") + _br(abs(dif), 2) + " p.p. em relação ao mês anterior"
        linhas.append({"País": p, "SLA": pct(a[0], sum(a)), "Comparativo / Observação": comp})
    return linhas


def pais(mercado, mes):
    """Aba por país. Atenção: nesta aba a coluna A é o país e a B é o mês."""
    paises = MERCADOS[mercado]
    d = _por_pais(mes, paises)
    return [{"Pais": ACENTO.get(p, p), "Volumetria Total": inteiro(_soma(d, (p,), TIPOS, "vol")),
             "WhatsApp (Vol)": inteiro(_soma(d, (p,), ("WhatsApp",), "vol")),
             "E-mail (Vol)*": inteiro(_soma(d, (p,), ("Email",), "vol")),
             "SLA WhatsApp": _sla(d, (p,)), "N1 Dentro do Prazo": _retencao(d, (p,))} for p in paises]


def tma(mercado, mes):
    return [{"Pais": p, "TMA E-mail": _tma(mes, (p,))} for p in sorted(MERCADOS[mercado])]


def solicitacoes_dia(mercado, mes):
    linhas = consultar(f"""
        SELECT date_format(data_contato, 'dd/MM') AS dia,
               sum(CASE WHEN nivel = 'N1' THEN valor_atendimento ELSE 0 END) AS n1,
               sum(CASE WHEN nivel = 'N2' THEN valor_atendimento ELSE 0 END) AS n2
        FROM {_base(mes, MERCADOS[mercado])} AND nivel IN ('N1', 'N2')
        GROUP BY 1 ORDER BY 1""")
    return [{"Data": l["dia"], "N1": inteiro(_f(l["n1"])), "N2": inteiro(_f(l["n2"])),
             "Total Diário": inteiro(_f(l["n1"]) + _f(l["n2"]))} for l in linhas]


# --- Motivos: 3 maiores plataformas e, em cada uma, os 3 maiores motivos (função do sistema) ---------------------------

def _motivos(mercado, mes, niveis):
    paises = MERCADOS[mercado]
    linhas = consultar(f"""
        SELECT status_de_classificacao AS plat, funcao_do_sistema AS mot, pais, sum(valor_atendimento) AS v
        FROM {_base(mes, paises)} AND nivel IN ({_lista(niveis)})
          AND status_de_classificacao IS NOT NULL AND status_de_classificacao NOT IN ({_lista(ACOMPANHAMENTO)})
        GROUP BY 1, 2, 3""")
    plat, mot, plat_pais = {}, {}, {}
    for l in linhas:
        v = _f(l["v"])
        plat[l["plat"]] = plat.get(l["plat"], 0) + v
        plat_pais[(l["plat"], l["pais"])] = plat_pais.get((l["plat"], l["pais"]), 0) + v
        if l["mot"]:
            mot[(l["plat"], l["mot"])] = mot.get((l["plat"], l["mot"]), 0) + v
    saida = []
    for p in sorted(plat, key=lambda k: (-plat[k], k))[:3]:
        tops = sorted(((m, v) for (pp, m), v in mot.items() if pp == p), key=lambda x: (-x[1], x[0]))[:3]
        for m, v in tops:
            saida.append((p, plat[p], {pa: plat_pais.get((p, pa), 0) for pa in paises}, m, v))
    return saida


def top3_motivo_contato(mercado, mes):
    return [{"Plataforma": _limpo(p), "Volume Total Plataforma": inteiro(t), "Motivo do Contato": _frase(m),
             "Volume do Motivo": inteiro(v), "Percentual (%)": pct(v, t)}
            for p, t, _, m, v in _motivos(mercado, mes, ("N1", "N2", "Neutro"))]


def _causa_raiz(mercado, mes, nivel):
    saida = []
    for p, t, por_pais, m, v in _motivos(mercado, mes, (nivel,)):
        r = {"Plataforma": _limpo(p), "Volume Total": inteiro(t)}
        if len(MERCADOS[mercado]) > 1:
            r.update({"Vol Argentina": inteiro(por_pais["Argentina"]), "Vol Chile": inteiro(por_pais["Chile"])})
        r.update({f"Motivo Causa Raiz ({nivel})": _frase(m), "Volume Motivo": inteiro(v), "Percentual (%)": pct(v, t)})
        saida.append(r)
    return saida


# --- CSAT (fonte Enquetes C-SAT, Hispana): uma linha por pergunta da enquete, contamos protocolos distintos ----------

# A partir de outubro/2026 (decisão de 09/11/2026), as enquetes do canal PRO ACTIVO (WhatsApp proativo) ficam fora do
# C-SAT, como o ATIVOS no Brasil: a análise de qualidade dos detratores não as considera. Meses fechados não mudam.
SEM_PROATIVO_DESDE = "2026-10"


def filtro_canal_csat(mes):
    return "AND coalesce(canal, '') NOT LIKE 'PRO ACTIVO%'" if mes >= SEM_PROATIVO_DESDE else ""


def _csat_base(mes, paises):
    return f"""{tabela('dexp_gold_csat_enquetes')}
        WHERE fonte = 'Hispana' AND pais IN ({_lista(paises)}) AND {_mes('data', mes)} {filtro_canal_csat(mes)}"""


def _csat_contagem(mes, paises):
    linhas = consultar(f"""
        SELECT pais, count(DISTINCT protocolo) AS enviadas,
               count(DISTINCT CASE WHEN enquete_respondida = 1 THEN protocolo END) AS respondidas,
               count(DISTINCT CASE WHEN c_sat = 'PROMOTOR' THEN protocolo END) AS promotor,
               count(DISTINCT CASE WHEN c_sat = 'NEUTRO' THEN protocolo END) AS neutro,
               count(DISTINCT CASE WHEN c_sat = 'DETRATOR' THEN protocolo END) AS detrator
        FROM {_csat_base(mes, paises)} GROUP BY ROLLUP(pais)""")
    return {l["pais"] or "total": {k: _f(v) for k, v in l.items() if k != "pais"} for l in linhas}


def csat_3_meses(mercado, mes):
    r = _csat_contagem(mes, MERCADOS[mercado]).get("total", {})
    return {"C-SAT (%)": pct(r.get("promotor", 0), r.get("respondidas")),
            "Enquetes Enviadas": inteiro(r.get("enviadas", 0)), "Enquetes Respondidas": inteiro(r.get("respondidas", 0)),
            "Response Rate (%)": pct(r.get("respondidas", 0), r.get("enviadas"))}


def _classificacao(r):
    total = r.get("promotor", 0) + r.get("neutro", 0) + r.get("detrator", 0)
    return [(nome, pct(r.get(chave, 0), total)) for nome, chave in
            (("Promotor", "promotor"), ("Neutro", "neutro"), ("Detrator", "detrator"))]


def csat_classificacao(mercado, mes):
    r = _csat_contagem(mes, MERCADOS[mercado]).get("total", {})
    return [{"Classificação C-SAT": n, "Percentual (%)": v} for n, v in _classificacao(r)]


ROTULOS_NOTA = {"5": "Totalmente Satisfeito", "4": "Satisfeito", "3": "Neutro", "2": "Insatisfeito",
                "1": "Totalmente Insatisfeito"}


def _notas(mes, paises):
    linhas = consultar(f"""SELECT pais, left(nota, 1) AS n, count(DISTINCT protocolo) AS vol FROM {_csat_base(mes, paises)}
                           AND enquete_respondida = 1 AND slice_numero = 1 GROUP BY ROLLUP(pais, left(nota, 1))""")
    return {(l["pais"] or "total", l["n"]): _f(l["vol"]) for l in linhas if l["n"] is not None or l["pais"] is None}


def csat_nota(mercado, mes):
    v = _notas(mes, MERCADOS[mercado])
    tot = {}
    for (p, n), x in v.items():
        if p != "total" and n:
            tot[n] = tot.get(n, 0) + x
    return [{"Nota Avaliada": rot, "Volume de Respostas": inteiro(tot.get(k, 0))} for k, rot in ROTULOS_NOTA.items()]


def _ofensores(mes, paises):
    linhas = consultar(f"""
        SELECT ois_funcao_do_sistema AS f, count(DISTINCT protocolo) AS n FROM {_csat_base(mes, paises)}
          AND c_sat = 'DETRATOR' AND ois_funcao_do_sistema IS NOT NULL
        GROUP BY 1 ORDER BY 2 DESC, 1 LIMIT 3""")
    return [(_frase(l["f"]), inteiro(_f(l["n"]))) for l in linhas]


def csat_ofensores_detr(mercado, mes):
    return [{"Ofensor Detrator": f, "Volume de Casos": n} for f, n in _ofensores(mes, MERCADOS[mercado])]


def csat_paises_3_meses(mercado, mes):
    """Atenção: nesta aba a coluna A é o país e a B é o mês."""
    c = _csat_contagem(mes, MERCADOS[mercado])
    return [{"Pais": ACENTO.get(p, p), "C-SAT (%)": pct(c.get(p, {}).get("promotor", 0), c.get(p, {}).get("respondidas")),
             "Response Rate (%)": pct(c.get(p, {}).get("respondidas", 0), c.get(p, {}).get("enviadas"))}
            for p in MERCADOS[mercado]]


def csat_paises_classifi(mercado, mes):
    c = _csat_contagem(mes, MERCADOS[mercado])
    return [{"Pais": ACENTO.get(p, p), "Classificação C-SAT": n, "Percentual (%)": v}
            for p in MERCADOS[mercado] for n, v in _classificacao(c.get(p, {}))]


def csat_paises_notas(mercado, mes):
    v = _notas(mes, MERCADOS[mercado])
    return [{"Pais": p, "Nota Avaliada": rot, "Volume de Respostas": inteiro(v.get((p, k), 0))}
            for p in MERCADOS[mercado] for k, rot in ROTULOS_NOTA.items()]


def csat_paises_ofensor(mercado, mes):
    return [{"Pais": ACENTO.get(p, p), "Ofensor Detrator": f, "Volume de Casos": n, "Texto do Comentário": MANUAL}
            for p in MERCADOS[mercado] for f, n in _ofensores(mes, (p,))]


def _abas(mercado, prefixo):
    funcoes = {
        "Vol_Retencao": vol_retencao, "Cards1": cards1, "Cards2": cards2, "Desempenho_Pais": desempenho_pais,
        "Top3_Motivo_Contato": top3_motivo_contato, "Solicitacoes_Dia": solicitacoes_dia, "Pais": pais, "TMA": tma,
        "Causa_Raiz_N1": lambda m, x: _causa_raiz(m, x, "N1"), "Causa_Raiz_N2": lambda m, x: _causa_raiz(m, x, "N2"),
        "CSAT_3_Meses": csat_3_meses, "CSAT_Classificacao": csat_classificacao, "CSAT_Nota": csat_nota,
        "CSAT_Ofensores_Detr": csat_ofensores_detr, "CSAT_Paises_3_Meses": csat_paises_3_meses,
        "CSAT_Paises_Classifi": csat_paises_classifi, "CSAT_Paises_Notas": csat_paises_notas,
        "CSAT_Paises_Ofensor": csat_paises_ofensor,
    }
    return {f"{prefixo}_{aba}": (lambda f: lambda mes: f(mercado, mes))(f) for aba, f in funcoes.items()}


# Abas manuais (texto): Mercado_*_CSAT_Analise_Quald e Mercado_*_CSAT_Comentarios
ABAS_MEXICO = _abas("mexico", "Mercado_Mexico")
ABAS_SUR = _abas("sur", "Mercado_Sur")
# Nas abas abaixo a coluna A é o país e a B é o mês (as demais começam pelo mês)
PAIS_PRIMEIRO = ("Mercado_Mexico_Pais", "Mercado_Mexico_CSAT_Paises_3_Meses", "Mercado_Sur_Pais", "Mercado_Sur_CSAT_Paises_3_Meses")
