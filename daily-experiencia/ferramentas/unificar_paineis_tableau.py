"""Junta os painéis repetidos do workbook Daily Experiência BR (gera uma nova versão; a de entrada não muda).

- Dynamics: os painéis "Dynamics CB" e "Dynamics CF" saem. O "Dynamics Consolidado" já tem o filtro de Tipo Protocolo
  (CB, CF, Franquias) e as mesmas visões.
- E-mail: "Email APP AVON - Detalhes", "Email APP Natura - Detalhes" e "Email Natura EXPCN - Detalhes" eram o mesmo
  painel filtrado por setor. Fica um só, "Email Lojas - Detalhes", com o parâmetro "Setor do e-mail": filtra o Setor
  nas planilhas da fonte MKT Emails de Lojas e o Canal nas de TMO e retenção (NATURA EXPCB = canal MINHA CONSULTORIA).
- WhatsApp: os cinco "Whats ... - Detalhes" (GN, GV, GV Antecipada, Franquia, CBCOM) liam cinco fontes com os mesmos
  campos e cálculos. Fica um só, "Whats - Detalhes", lendo a view dexp_vw_mkt_whats_detalhes (as cinco juntas, com a
  coluna Painel) e com o parâmetro "Painel do WhatsApp". A planilha de SLA do primeiro contato do GV filtrava
  Setor Fim = "Whats GV"; o filtro continua valendo só quando o painel escolhido é o GV.

Planilhas, janelas, miniaturas, ações e fontes que só os painéis removidos usavam também saem.

Uso (a partir da pasta daily-experiencia):
  .venv\\Scripts\\python.exe ferramentas\\unificar_paineis_tableau.py <entrada.twbx> <saída.twbx>
"""
import copy
import random
import re
import string
import sys
import zipfile
from pathlib import Path

from lxml import etree

USER = "http://www.tableausoftware.com/xml/user"

REMOVER_DYNAMICS = ["Dynamics CB", "Dynamics CF"]

EMAIL_BASE, EMAIL_NOVO = "Email APP Natura - Detalhes", "Email Lojas - Detalhes"
EMAIL_REMOVER = ["Email APP AVON - Detalhes", "Email Natura EXPCN - Detalhes"]
EMAIL_VALORES = [("APP AVON CF", "APP AVON"), ("APP NATURA", None), ("NATURA EXPCB", "NATURA EXPCN")]
EMAIL_PADRAO = "APP NATURA"
# fonte -> (campo filtrado pelo setor, fórmula do filtro com {p} no lugar do parâmetro)
EMAIL_FILTROS = {
    "MKT Emails de Lojas": ("Setor", "[Setor] = {p}"),
    "MKT Brasil Completo": ("Canal", '[Canal] = (IF {p} = "NATURA EXPCB" THEN "MINHA CONSULTORIA" ELSE {p} END)'),
    "MKT Brasil Completo Nivel": ("Canal", '[Canal] = (IF {p} = "NATURA EXPCB" THEN "MINHA CONSULTORIA" ELSE {p} END)'),
}

WHATS_BASE, WHATS_NOVO = "Whats GN - Detalhes", "Whats - Detalhes"
WHATS_REMOVER = ["Whats GV - Detalhes", "Whats GV Antecipada - Detalhes", "Whats FRANQUIA - Detalhes",
                 "Whats CBCOM - Detalhes"]
WHATS_FONTE, WHATS_FONTE_NOVA = "MKT Whats GN", "MKT Whats Detalhes"
WHATS_VIEW_ANTIGA, WHATS_VIEW = "dexp_vw_mkt_whats_gn", "dexp_vw_mkt_whats_detalhes"
WHATS_VALORES = [("GN", None), ("GV", None), ("GV Antecipada", None), ("Franquia", None), ("CBCOM", None)]
WHATS_PADRAO = "GN"
WHATS_PLANILHA_GV = "Whats GN SLA Primeiro Contato"  # a do GV tinha também Setor Fim = "Whats GV"


def u(nome):
    return f"{{{USER}}}{nome}"


def aspas(valor):
    return f'"{valor}"'


def novo_calculo():
    return f"[Calculation_{random.randint(10 ** 18, 9 * 10 ** 18)}]"


def coluna_do_filtro(f):
    return re.sub(r"^\[[^\]]+\]\.", "", f.get("column") or "")


def filtros(ws):
    return ws.find("table/view").findall("filter")


def planilhas_do_painel(painel, por_nome):
    return list(dict.fromkeys(z.get("name") for z in painel.iter("zone")
                              if z.get("name") in por_nome and not z.get("type-v2")))


# --- parâmetros ------------------------------------------------------------------------------------------------

def fonte_parametros(raiz):
    fontes = raiz.find("datasources")
    for ds in fontes:
        if ds.get("name") == "Parameters":
            return ds
    ds = etree.Element("datasource", hasconnection="false", inline="true", name="Parameters", version="18.1")
    etree.SubElement(ds, "aliases", enabled="yes")
    fontes.insert(0, ds)
    return ds


def criar_parametro(raiz, legenda, valores, padrao):
    ds = fonte_parametros(raiz)
    numero = 1 + max([int(m) for c in ds.findall("column") for m in re.findall(r"\[Parameter (\d+)\]", c.get("name"))]
                     or [0])
    coluna = etree.SubElement(ds, "column", caption=legenda, datatype="string", name=f"[Parameter {numero}]",
                              **{"param-domain-type": "list"}, role="measure", type="nominal", value=aspas(padrao))
    etree.SubElement(coluna, "calculation", {"class": "tableau", "formula": aspas(padrao)})
    membros = etree.SubElement(coluna, "members")
    for valor, apelido in valores:
        m = etree.SubElement(membros, "member", value=aspas(valor))
        if apelido:
            m.set("alias", apelido)
    return coluna


def dependencia_parametro(alvo, parametro):
    """Declara o parâmetro nas fontes usadas por uma planilha (table/view) ou por um painel."""
    lista = alvo.find("datasources")
    if lista is not None and not any(d.get("name") == "Parameters" for d in lista):
        etree.SubElement(lista, "datasource", name="Parameters")
    deps = [d for d in alvo.findall("datasource-dependencies") if d.get("datasource") == "Parameters"]
    if deps:
        dep = deps[0]
    else:
        dep = etree.Element("datasource-dependencies", datasource="Parameters")
        ultimas = alvo.findall("datasource-dependencies")
        if ultimas:
            ultimas[-1].addnext(dep)
        else:
            lista.addnext(dep)
    if not any(c.get("name") == parametro.get("name") for c in dep):
        dep.append(copy.deepcopy(parametro))


# --- filtros por cálculo ---------------------------------------------------------------------------------------

def criar_calculo(ds, legenda, formula):
    nome = novo_calculo()
    coluna = etree.Element("column", caption=legenda, datatype="boolean", name=nome, role="dimension", type="nominal")
    etree.SubElement(coluna, "calculation", {"class": "tableau", "formula": formula})
    colunas = ds.findall("column")
    (colunas[-1] if colunas else ds.find("connection")).addnext(coluna)
    return coluna


def filtrar_por_calculo(ws, ds_nome, calculo, campos_base, remover=()):
    """Troca os filtros das colunas `remover` por um filtro [calculo] = verdadeiro."""
    view = ws.find("table/view")
    dep = next(d for d in view.findall("datasource-dependencies") if d.get("datasource") == ds_nome)
    existentes = {c.get("name") for c in dep}
    for campo in campos_base:
        if f"[{campo}]" not in existentes:
            dep.insert(0, etree.Element("column", datatype="string", name=f"[{campo}]", role="dimension",
                                        type="nominal"))
    dep.insert(0, copy.deepcopy(calculo))
    instancia = f"[none:{calculo.get('name').strip('[]')}:nk]"
    etree.SubElement(dep, "column-instance", column=calculo.get("name"), derivation="None", name=instancia,
                     pivot="key", type="nominal")

    lista = filtros(ws)
    ancora = lista[-1] if lista else dep
    for f in lista:
        if coluna_do_filtro(f) in remover:
            if f is ancora:
                ancora = f.getprevious()
            view.remove(f)
    novo = etree.Element("filter", {"class": "categorical", "column": f"[{ds_nome}].{instancia}"})
    etree.SubElement(novo, "groupfilter", {"function": "member", "level": instancia, "member": "true",
                                           u("ui-domain"): "database", u("ui-enumeration"): "inclusive",
                                           u("ui-marker"): "enumerate"})
    ancora.addnext(novo)

    slices = view.find("slices")
    if slices is None:
        slices = etree.Element("slices")
        novo.addnext(slices)
    for c in list(slices):
        if coluna_do_filtro(etree.Element("x", column=c.text or "")) in remover:
            slices.remove(c)
    etree.SubElement(slices, "column").text = novo.get("column")


# --- painéis ---------------------------------------------------------------------------------------------------

def renomear_painel(raiz, antigo, novo):
    for e in raiz.iter():
        for atributo in ("name", "dashboard", "value"):
            if e.get(atributo) == antigo:
                e.set(atributo, novo)


def controle_de_parametro(painel, parametro):
    """Põe o controle do parâmetro ao lado do filtro de Nível, nos layouts de desktop e de celular."""
    proximo_id = 1 + max(int(z.get("id")) for z in painel.iter("zone") if z.get("id"))
    referencia = f"[Parameters].{parametro.get('name')}"
    for zona in [z for z in painel.iter("zone") if z.get("type-v2") == "filter" and "Nível:nk" in (z.get("param") or "")]:
        pai = zona.getparent()
        controle = copy.deepcopy(zona)
        for a in ("name", "values"):
            controle.attrib.pop(a, None)
        controle.set("id", str(proximo_id))
        controle.set("type-v2", "paramctrl")
        controle.set("param", referencia)
        controle.set("mode", "compact")
        if pai.get("param") == "horz":
            # divide a largura da linha de filtros entre os controles, agora um a mais
            irmas = [z for z in pai if z.get("type-v2") == "filter"] + [controle]
            inicio, largura = int(pai.get("x")), int(pai.get("w"))
            cada = largura // len(irmas)
            for i, z in enumerate(irmas):
                z.set("x", str(inicio + i * cada))
                z.set("w", str(cada if i < len(irmas) - 1 else largura - cada * (len(irmas) - 1)))
        zona.addnext(controle)
    dependencia_parametro(painel, parametro)


def titulo_com_parametro(painel, texto_antigo, prefixo, parametro):
    for run in painel.iter("run"):
        if (run.text or "").strip() == texto_antigo:
            run.text = prefixo
            novo = copy.deepcopy(run)
            novo.text = f"<[Parameters].{parametro.get('name')}>"
            novo.tail, run.tail = run.tail, None
            run.addnext(novo)


# --- WhatsApp: fonte nova --------------------------------------------------------------------------------------

def fonte_whats_unificada(raiz):
    fontes = raiz.find("datasources")
    antiga = next(d for d in fontes if d.get("caption") == WHATS_FONTE)
    conexao_antiga = antiga.find("connection/named-connections/named-connection").get("name")
    nome = "federated." + "".join(random.choices(string.ascii_lowercase + string.digits, k=28))
    texto = etree.tostring(antiga).decode("utf-8")
    texto = (texto.replace(antiga.get("name"), nome).replace(WHATS_VIEW_ANTIGA, WHATS_VIEW)
             .replace(conexao_antiga, "databricks." + "".join(random.choices(string.ascii_lowercase + string.digits, k=28))))
    nova = etree.fromstring(texto.encode("utf-8"))
    nova.set("caption", WHATS_FONTE_NOVA)
    registros = nova.find("connection/metadata-records")
    modelo = next(m for m in registros if m.findtext("remote-name") == "Setor Fim")
    painel_col = copy.deepcopy(modelo)
    for tag, valor in [("remote-name", "Painel"), ("local-name", "[Painel]"), ("remote-alias", "Painel"),
                       ("ordinal", str(1 + max(int(m.findtext("ordinal")) for m in registros)))]:
        painel_col.find(tag).text = valor
    registros.append(painel_col)
    nova.tail = antiga.tail
    antiga.addnext(nova)
    return antiga.get("name"), nova


def trocar_fonte(elemento, antiga, nova, legenda_nova):
    for e in elemento.iter():
        for a, v in list(e.attrib.items()):
            if antiga in v:
                e.set(a, v.replace(antiga, nova))
        if e.text and antiga in e.text:
            e.text = e.text.replace(antiga, nova)
        if e.tag == "datasource" and e.get("name") == nova and e.get("caption"):
            e.set("caption", legenda_nova)


# --- limpeza ---------------------------------------------------------------------------------------------------

def limpar(raiz, paineis_removidos):
    paineis = raiz.find("dashboards")
    for d in list(paineis):
        if d.get("name") in paineis_removidos:
            paineis.remove(d)
    usadas = {z.get("name") for d in paineis for z in d.iter("zone") if z.get("name")}
    planilhas = raiz.find("worksheets")
    removidas = {w.get("name") for w in planilhas if w.get("name") not in usadas}
    for w in list(planilhas):
        if w.get("name") in removidas:
            planilhas.remove(w)
    fora = removidas | set(paineis_removidos)
    for grupo in ("windows", "thumbnails"):
        g = raiz.find(grupo)
        for e in list(g) if g is not None else []:
            if e.get("name") in fora:
                g.remove(e)
    for vp in list(raiz.iter("viewpoint")):
        if vp.get("name") in removidas:
            vp.getparent().remove(vp)
    acoes = raiz.find("actions")
    for a in list(acoes):
        origem = a.find("source")
        alvos = {p.get("value") for p in a.iter("param") if p.get("name") == "target"}
        if (origem is not None and (origem.get("dashboard") in paineis_removidos or origem.get("worksheet") in removidas)) \
                or alvos & set(paineis_removidos):
            acoes.remove(a)
    # fontes que nenhuma planilha, painel ou janela usa mais
    usos = "".join(etree.tostring(raiz.find(g)).decode("utf-8") for g in ("worksheets", "dashboards", "windows", "actions"))
    fontes = raiz.find("datasources")
    sem_uso = [d for d in fontes if d.get("name") != "Parameters" and d.get("name") not in usos]
    for d in sem_uso:
        fontes.remove(d)
    return removidas, [d.get("caption") for d in sem_uso]


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    entrada, saida = Path(sys.argv[1]), Path(sys.argv[2])
    with zipfile.ZipFile(entrada) as z:
        twb = next(n for n in z.namelist() if n.lower().endswith(".twb") and "/" not in n)
        raiz = etree.fromstring(z.read(twb), etree.XMLParser(huge_tree=True))
        outros = {i.filename: (i, z.read(i.filename)) for i in z.infolist() if i.filename != twb}

    fontes = {d.get("caption"): d for d in raiz.find("datasources")}
    por_nome = {w.get("name"): w for w in raiz.find("worksheets")}
    paineis = {d.get("name"): d for d in raiz.find("dashboards")}

    # E-mail
    p_email = criar_parametro(raiz, "Setor do e-mail", EMAIL_VALORES, EMAIL_PADRAO)
    calculos = {}
    for fonte, (campo, formula) in EMAIL_FILTROS.items():
        calculos[fontes[fonte].get("name")] = (campo, criar_calculo(
            fontes[fonte], "Filtro do setor do e-mail", formula.format(p=f"[Parameters].{p_email.get('name')}")))
    for n in planilhas_do_painel(paineis[EMAIL_BASE], por_nome):
        ws = por_nome[n]
        for ds_nome, (campo, calculo) in calculos.items():
            if any(f.get("column", "").startswith(f"[{ds_nome}].[none:{campo}:nk]") for f in filtros(ws)):
                filtrar_por_calculo(ws, ds_nome, calculo, [campo], remover=(f"[none:{campo}:nk]",))
                dependencia_parametro(ws.find("table/view"), p_email)
                print(f"+ e-mail: {n} filtra {campo} pelo parâmetro")
    controle_de_parametro(paineis[EMAIL_BASE], p_email)
    titulo_com_parametro(paineis[EMAIL_BASE], "EMAIL APP NATURA", "EMAIL ", p_email)

    # WhatsApp
    antiga, nova = fonte_whats_unificada(raiz)
    p_whats = criar_parametro(raiz, "Painel do WhatsApp", WHATS_VALORES, WHATS_PADRAO)
    ref = f"[Parameters].{p_whats.get('name')}"
    calc_painel = criar_calculo(nova, "Filtro do painel do WhatsApp", f"[Painel] = {ref}")
    calc_gv = criar_calculo(nova, "Filtro Setor Fim do GV", '[Painel] <> "GV" OR [Setor Fim] = "Whats GV"')
    painel_whats = paineis[WHATS_BASE]
    trocar_fonte(painel_whats, antiga, nova.get("name"), WHATS_FONTE_NOVA)
    janelas = {j.get("name"): j for j in raiz.find("windows")}
    trocar_fonte(janelas[WHATS_BASE], antiga, nova.get("name"), WHATS_FONTE_NOVA)
    for n in planilhas_do_painel(painel_whats, por_nome):
        ws = por_nome[n]
        trocar_fonte(ws, antiga, nova.get("name"), WHATS_FONTE_NOVA)
        if n in janelas:  # cartões e legendas guardados na janela da planilha
            trocar_fonte(janelas[n], antiga, nova.get("name"), WHATS_FONTE_NOVA)
        if not any(d.get("datasource") == nova.get("name") for d in ws.iter("datasource-dependencies")):
            continue
        filtrar_por_calculo(ws, nova.get("name"), calc_painel, ["Painel"])
        if n == WHATS_PLANILHA_GV:
            filtrar_por_calculo(ws, nova.get("name"), calc_gv, ["Painel", "Setor Fim"])
        dependencia_parametro(ws.find("table/view"), p_whats)
        print(f"+ whats: {n} lê {WHATS_FONTE_NOVA} filtrada pelo parâmetro")
    controle_de_parametro(painel_whats, p_whats)
    titulo_com_parametro(painel_whats, "WHATSAPP GN", "WHATSAPP ", p_whats)

    removidos = REMOVER_DYNAMICS + EMAIL_REMOVER + WHATS_REMOVER
    removidas, fontes_sem_uso = limpar(raiz, removidos)
    renomear_painel(raiz, EMAIL_BASE, EMAIL_NOVO)
    renomear_painel(raiz, WHATS_BASE, WHATS_NOVO)
    print(f"\nPainéis removidos: {removidos}\nPlanilhas removidas: {len(removidas)}\nFontes sem uso removidas: {fontes_sem_uso}")

    texto = etree.tostring(raiz, encoding="utf-8", xml_declaration=True)
    etree.fromstring(texto, etree.XMLParser(huge_tree=True))
    with zipfile.ZipFile(saida, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr(saida.with_suffix(".twb").name, texto)
        for item, conteudo in outros.values():
            z.writestr(item, conteudo)
    print(f"Gravado em {saida}")


if __name__ == "__main__":
    main()
