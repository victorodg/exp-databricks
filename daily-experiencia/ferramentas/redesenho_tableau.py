"""Redesenho visual do workbook Daily Experiência BR (gera uma nova versão; a de entrada não muda).

1. Indicadores com meta: as barras 100% de um mês só viram uma faixa com os últimos 6 meses, um bloco por mês com o %
   do indicador, pintado pela distância da meta: verde-água dentro da meta, laranja até 10 pontos abaixo, vermelho
   mais abaixo (as cores do "SLA ... por Fase" do Dynamics Consolidado).
2. Volumes que mostravam um mês só passam a mostrar os últimos 6 meses.
3. Laranja deixa de ser cor de série: nas visões que não são indicador com meta, os laranjas viram tons de
   azul-acinzentado (nas Resenhas, roxo e lilás, para os apps continuarem com cores diferentes).
4. "Protocolos Recebidos e SLA Cliente" (Dynamics Consolidado): sai a planilha de % SLA Cliente que ficava por cima
   do gráfico como um ponto solto; o SLA Cliente já tem a própria visão.
5. Filtros de intervalo de datas com data final fixa (ex.: até 30/09/2026, que esvaziava o MKT Email EXPCB em
   outubro) passam a não ter fim; o período vem dos filtros de mês e ano.

Uso (a partir da pasta daily-experiencia):
  .venv\\Scripts\\python.exe ferramentas\\redesenho_tableau.py <entrada.twbx> <saída.twbx>
"""
import copy
import random
import re
import sys
import zipfile
from pathlib import Path

from lxml import etree

DENTRO, ABAIXO, MUITO_ABAIXO = "Dentro da meta", "Abaixo da meta", "Muito abaixo da meta"
CORES_META = {DENTRO: "#76b7b2", ABAIXO: "#f28e2b", MUITO_ABAIXO: "#e15759"}
FAIXA_ABAIXO = 0.10  # até 10 pontos abaixo da meta = laranja
MESES = 6

# planilha -> indicador: campo de status, valores que contam como positivos e negativos, peso e meta.
# Metas que não estão no título das planilhas (e-mail, atendidos até 1 hora, Resenhas) ficaram em 85%.
SLA_DYNAMICS = dict(positivos=["DENTRO DO PRAZO"], negativos=["FORA DO PRAZO"], meta=0.85)
SLA_TEXTO = dict(positivos=["Dentro do SLA"], negativos=["Fora do SLA"])
KPIS = {
    "Dynamics CB+CF SLA EXP": dict(campo="SLA Experiência", legenda="SLA Experiência", **SLA_DYNAMICS),
    "Dynamics CB+CF SLA Cliente": dict(campo="SLA Cliente", legenda="SLA Cliente", **SLA_DYNAMICS),
    "Dynamics CB+CF SLA 5h": dict(campo="SLA 5 Horas", legenda="SLA 5 Horas", **SLA_DYNAMICS),
    "Dynamics CB+CF % N1 Encerrados": dict(campo="Nivel de Atendimento", legenda="Retenção N1 (encerrados)",
                                           positivos=["N1"], negativos=["N2"], meta=0.70),
    "Email APP NATURA": dict(campo="Status SLA Email", legenda="SLA E-mail", meta=0.85, **SLA_TEXTO),
    "Email EXPCB 1 Hora (2)": dict(campo="Calculation_0013859898982401", legenda="Atendidos até 1 hora",
                                   positivos=["Dentro de 1 Hora"], negativos=["Acima de 1 Hora"],
                                   peso="Qtd Atendimentos", meta=0.85),
    "SLA App AVON": dict(campo="Status SLA", legenda="SLA Resenhas", meta=0.85, **SLA_TEXTO),
    "SLA App Consultoria": dict(campo="Status SLA", legenda="SLA Resenhas", meta=0.85, **SLA_TEXTO),
    "SLA App FV": dict(campo="Status SLA", legenda="SLA Resenhas", meta=0.85, **SLA_TEXTO),
    "SLA App Sempre Presente": dict(campo="Status SLA", legenda="SLA Resenhas", meta=0.85, **SLA_TEXTO),
    "Whats GN SLA Primeiro Contato": dict(campo="SLA do Primeiro Contato", legenda="SLA Primeiro Contato",
                                          meta=0.95, **SLA_TEXTO),
    "WhatsApp Consolidado SLA Prim. Cont.": dict(campo="SLA do Primeiro Contato", legenda="SLA Primeiro Contato",
                                                 meta=0.95, **SLA_TEXTO),
    "WhatsApp Consolidado Nivel 2": dict(campo="Nível", legenda="Retenção N1 (atendimentos)", positivos=["N1"],
                                         negativos=["N2"], peso="Qtd Atendimentos", meta=0.70),
}

VOLUMES = ["Dynamics CB+CF N2", "Resenhas App Avon Contagem", "Resenhas App CN Contagem", "Resenhas App FV Contagem",
           "Resenhas App Sempre Presente Contagem", "Email AppNatura Atendimento e Tempo Medio",
           "Email EXPCB Atendimento e Tempo Medio"]

PONTO_SOLTO = ("Dynamics Consolidado", "Dynamics CB+CF % SLA Cliente", "Dynamics CB+CF Recebidos 3 Meses",
               "Protocolos Recebidos e SLA Cliente", "Protocolos Recebidos")

LARANJA_PARA_AZUL = {"#eb6619": "#557084", "#fe772c": "#557084", "#f28e2b": "#557084", "#c46348": "#46627a",
                     "#f1945f": "#8a9faf", "#ffbe7d": "#bac6d0", "#e8b09f": "#cbd4db"}
LARANJA_PARA_ROXO = {"#eb6619": "#6e597f", "#fe772c": "#6e597f", "#f28e2b": "#6e597f", "#c46348": "#5a4868",
                     "#f1945f": "#a0a7d8", "#ffbe7d": "#c5c9ea", "#e8b09f": "#d5d7ef"}
PAINEIS_RESENHAS = ["Resenhas", "Resenhas Visão Executiva"]
GRADIENTE_AZUL = ["#f1f1f1", "#dde2e6", "#cbd4db", "#bac6d0", "#a9b9c5", "#99acba", "#8a9faf", "#7b93a4", "#6d8799",
                  "#617b8e", "#557084"]
DERIVACOES_DE_DATA = ("dy", "mn", "yr", "my", "qr", "wk", "tdy", "tmn", "tyr", "mdy", "wd", "hr")


# --- utilidades ------------------------------------------------------------------------------------------------

def novo_calculo():
    return f"Calculation_{random.randint(10 ** 18, 9 * 10 ** 18)}"


def coluna_do_filtro(f):
    return re.sub(r"^\[[^\]]+\]\.", "", f.get("column") or "")


def filtros(ws):
    return ws.find("table/view").findall("filter")


def dependencia(ws, ds_nome):
    return next(d for d in ws.find("table/view").findall("datasource-dependencies") if d.get("datasource") == ds_nome)


def garantir_coluna(dep, xml):
    novo = etree.fromstring(xml)
    if not any(c.get("name") == novo.get("name") for c in dep if c.tag == novo.tag):
        if novo.tag == "column":
            dep.insert(0, novo)
        else:
            dep.append(novo)


def refazer_slices(ws):
    view = ws.find("table/view")
    slices = view.find("slices")
    if slices is None:
        slices = etree.Element("slices")
        (filtros(ws)[-1] if filtros(ws) else view.findall("datasource-dependencies")[-1]).addnext(slices)
    for c in list(slices):
        slices.remove(c)
    for f in filtros(ws):
        etree.SubElement(slices, "column").text = f.get("column")


def campo_de_data(ws, ds_nome):
    """Campo de data que a planilha usa para o período (nas prateleiras ou nos filtros de mês/ano)."""
    texto = " ".join(filter(None, [ws.find("table/rows").text, ws.find("table/cols").text]
                            + [f.get("column") for f in filtros(ws)]))
    achados = re.findall(re.escape(f"[{ds_nome}].") + r"\[(?:mn|my|yr|tmn):([^:\]]+):ok\]", texto)
    return max(set(achados), key=achados.count) if achados else None


def filtro_ultimos_meses(ws, ds_nome, data):
    """Tira os filtros de dia/mês/ano/intervalo e as seleções salvas de ações sobre a data; filtra os últimos meses."""
    view = ws.find("table/view")
    padrao = re.compile(r"\[(?:%s):%s:(?:ok|qk)\]" % ("|".join(DERIVACOES_DE_DATA + ("none",)), re.escape(data)))
    for f in filtros(ws):
        col = coluna_do_filtro(f)
        if padrao.fullmatch(col) or (col.startswith("[Action (") and data in col):
            view.remove(f)
    dep = dependencia(ws, ds_nome)
    garantir_coluna(dep, f'<column-instance column="[{data}]" derivation="None" name="[none:{data}:qk]" pivot="key" '
                         f'type="quantitative"/>')
    garantir_coluna(dep, f'<column-instance column="[{data}]" derivation="MY" name="[my:{data}:ok]" pivot="key" '
                         f'type="ordinal"/>')
    novo = etree.Element("filter", {"class": "relative-date", "column": f"[{ds_nome}].[none:{data}:qk]",
                                    "first-period": str(1 - MESES), "include-future": "true",
                                    "include-null": "false", "last-period": "0", "period-type-v2": "month"})
    lista = filtros(ws)
    (lista[-1] if lista else view.findall("datasource-dependencies")[-1]).addnext(novo)
    refazer_slices(ws)


def acrescentar_ao_titulo(ws, texto):
    titulo = ws.find("layout-options/title/formatted-text")
    if titulo is None:
        return
    run = etree.SubElement(titulo, "run", fontsize="8")
    run.text = f"  {texto}"


# --- 1. indicadores com meta -----------------------------------------------------------------------------------

def estilo_da_fonte(ds):
    estilo = ds.find("style")
    if estilo is None:
        estilo = etree.Element("style")
        ancora = ds.find("layout") if ds.find("layout") is not None else ds.findall("column")[-1]
        ancora.addnext(estilo)
    regra = next((r for r in estilo.findall("style-rule") if r.get("element") == "mark"), None)
    if regra is None:
        regra = etree.SubElement(estilo, "style-rule", element="mark")
    return regra


def calculos_do_indicador(ds, cfg, ja_criados):
    chave = (ds.get("name"), cfg["campo"], tuple(cfg["positivos"]), tuple(cfg["negativos"]), cfg.get("peso"),
             cfg["meta"])
    if chave in ja_criados:
        return ja_criados[chave]
    campo = f"[{cfg['campo']}]"
    peso = f"[{cfg['peso']}]" if cfg.get("peso") else "1"
    cond = lambda valores: " OR ".join(f'{campo} = "{v}"' for v in valores)
    pct, status = novo_calculo(), novo_calculo()
    formula_pct = (f"SUM(IF {cond(cfg['positivos'])} THEN {peso} ELSE 0 END) / "
                   f"SUM(IF {cond(cfg['positivos'] + cfg['negativos'])} THEN {peso} ELSE 0 END)")
    meta, piso = cfg["meta"], round(cfg["meta"] - FAIXA_ABAIXO, 4)
    formula_status = (f'IF [{pct}] >= {meta} THEN "{DENTRO}" ELSEIF [{pct}] >= {piso} THEN "{ABAIXO}" '
                      f'ELSE "{MUITO_ABAIXO}" END')
    col_pct = etree.fromstring(f'<column caption="% {cfg["legenda"]} (meta {round(meta * 100)}%)" datatype="real" '
                               f'default-format="p0.0%" name="[{pct}]" role="measure" type="quantitative"/>')
    etree.SubElement(col_pct, "calculation", {"class": "tableau", "formula": formula_pct})
    col_status = etree.fromstring(f'<column caption="Status Meta {cfg["legenda"]} ({round(meta * 100)}%)" '
                                  f'datatype="string" name="[{status}]" role="measure" type="nominal"/>')
    etree.SubElement(col_status, "calculation", {"class": "tableau", "formula": formula_status})
    ds.findall("column")[-1].addnext(col_pct)
    col_pct.addnext(col_status)
    cor = etree.SubElement(estilo_da_fonte(ds), "encoding", attr="color", field=f"[{ds.get('name')}].[usr:{status}:nk]",
                           type="palette")
    for valor, hexa in CORES_META.items():
        etree.SubElement(etree.SubElement(cor, "map", to=hexa), "bucket").text = f'"{valor}"'
    ja_criados[chave] = (col_pct, col_status)
    return ja_criados[chave]


def kpi_em_faixa(ws, ds, cfg, ja_criados):
    ds_nome = ds.get("name")
    data = campo_de_data(ws, ds_nome)
    if data is None:
        return f"sem campo de data, ficou como estava"
    col_pct, col_status = calculos_do_indicador(ds, cfg, ja_criados)
    pct, status = col_pct.get("name").strip("[]"), col_status.get("name").strip("[]")
    dep = dependencia(ws, ds_nome)
    for base, tipo, papel in [(cfg["campo"], "string", "dimension"), (cfg.get("peso"), "real", "measure"),
                              (data, "datetime", "dimension")]:
        if base and not base.startswith("Calculation_"):
            garantir_coluna(dep, f'<column datatype="{tipo}" name="[{base}]" role="{papel}" '
                                 f'type="{"quantitative" if tipo == "real" else "nominal"}"/>')
    for col in (col_status, col_pct):
        garantir_coluna(dep, etree.tostring(col).decode("utf-8"))
    garantir_coluna(dep, f'<column-instance column="[{pct}]" derivation="User" name="[usr:{pct}:qk]" pivot="key" '
                         f'type="quantitative"/>')
    garantir_coluna(dep, f'<column-instance column="[{status}]" derivation="User" name="[usr:{status}:nk]" '
                         f'pivot="key" type="nominal"/>')
    filtro_ultimos_meses(ws, ds_nome, data)

    tabela = ws.find("table")
    ref = lambda n: f"[{ds_nome}].[{n}]"
    estilo = etree.fromstring(f"""<style>
      <style-rule element="cell"><format attr="text-format" field="{ref(f'usr:{pct}:qk')}" value="p0.0%"/>
        <format attr="text-align" value="center"/><format attr="vertical-align" value="center"/></style-rule>
      <style-rule element="header"><format attr="font-size" value="8"/></style-rule>
      <style-rule element="datalabel"><format attr="color-mode" value="auto"/><format attr="font-weight" value="bold"/>
        <format attr="font-size" value="11"/></style-rule>
      <style-rule element="table"><format attr="background-color" value="#00000000"/></style-rule>
      <style-rule element="worksheet"><format attr="display-field-labels" scope="cols" value="false"/></style-rule>
    </style>""")
    panes = etree.fromstring(f"""<panes><pane selection-relaxation-option="selection-relaxation-allow">
      <view><breakdown value="auto"/></view><mark class="Square"/>
      <encodings><color column="{ref(f'usr:{status}:nk')}"/><text column="{ref(f'usr:{pct}:qk')}"/></encodings>
      <style><style-rule element="mark"><format attr="mark-labels-show" value="true"/>
        <format attr="mark-labels-cull" value="false"/></style-rule></style>
    </pane></panes>""")
    for antigo, novo in [(tabela.find("style"), estilo), (tabela.find("panes"), panes)]:
        if antigo is None:
            tabela.find("view").addnext(novo)
        else:
            novo.tail = antigo.tail
            tabela.replace(antigo, novo)
    tabela.find("rows").text = None
    tabela.find("cols").text = ref(f"my:{data}:ok")
    acrescentar_ao_titulo(ws, f"últimos {MESES} meses · cor pela meta")
    return f"faixa de {MESES} meses de {cfg['campo']} por {data}, meta {round(cfg['meta'] * 100)}%"


def legendas_do_indicador(raiz, ws, ds_nome, status):
    for zona in raiz.iter("zone"):
        if zona.get("name") == ws.get("name") and zona.get("type-v2") == "color":
            zona.set("param", f"[{ds_nome}].[usr:{status}:nk]")
            zona.attrib.pop("pane-specification-id", None)


# --- 2. volumes ------------------------------------------------------------------------------------------------

def volume_em_meses(ws):
    ds_nome = ws.find("table/view/datasources/datasource").get("name")
    data = campo_de_data(ws, ds_nome)
    if data is None:
        return "sem campo de data, ficou como estava"
    filtro_ultimos_meses(ws, ds_nome, data)
    acrescentar_ao_titulo(ws, f"últimos {MESES} meses")
    return f"últimos {MESES} meses por {data}"


# --- 3. cores --------------------------------------------------------------------------------------------------

def trocar_cores(elemento, mapa, pular=()):
    for e in elemento.iter():
        if e.tag == "encoding" and any(p in (e.get("field") or "") for p in pular):
            continue
        for a in ("value", "to", "fontcolor"):
            v = (e.get(a) or "").lower()
            if v in mapa and not any(p in (e.getparent().get("field") or "") for p in pular if e.getparent() is not None):
                e.set(a, mapa[v])
        if e.tag == "color-palette":
            cores = [c.text.lower() for c in e.findall("color")]
            if cores and cores[-1] in mapa and len(cores) == len(GRADIENTE_AZUL):
                for c, novo in zip(e.findall("color"), GRADIENTE_AZUL):
                    c.text = novo


def cores(raiz):
    # cálculos de status de meta (os novos e os do "por Fase") mantêm verde-água, laranja e vermelho
    pular = [f"usr:{c.get('name').strip('[]')}:nk" for d in raiz.find("datasources") for c in d.findall("column")
             if (c.get("caption") or "").startswith("Status Meta")]
    paineis = {d.get("name"): d for d in raiz.find("dashboards")}
    resenhas = {z.get("name") for p in PAINEIS_RESENHAS if p in paineis for z in paineis[p].iter("zone") if z.get("name")}
    fontes_resenhas = {d.get("name") for d in raiz.find("datasources") if "Resenhas" in (d.get("caption") or "")}
    for ws in raiz.find("worksheets"):
        if ws.get("name") in KPIS:
            continue
        trocar_cores(ws, LARANJA_PARA_ROXO if ws.get("name") in resenhas else LARANJA_PARA_AZUL, pular)
    for ds in raiz.find("datasources"):
        trocar_cores(ds, LARANJA_PARA_ROXO if ds.get("name") in fontes_resenhas else LARANJA_PARA_AZUL, pular)
    for nome, painel in paineis.items():
        trocar_cores(painel, LARANJA_PARA_ROXO if nome in PAINEIS_RESENHAS else LARANJA_PARA_AZUL, pular)


# --- 4. ponto solto --------------------------------------------------------------------------------------------

def tirar_ponto_solto(raiz):
    painel_nome, sobreposta, grafico, titulo_antigo, titulo_novo = PONTO_SOLTO
    painel = next(d for d in raiz.find("dashboards") if d.get("name") == painel_nome)
    for zona in list(painel.iter("zone")):
        if zona.get("name") == sobreposta and zona.getparent() is not None:
            zona.getparent().remove(zona)
    usada = any(z.get("name") == sobreposta for d in raiz.find("dashboards") for z in d.iter("zone"))
    if not usada:
        for grupo in ("worksheets", "windows", "thumbnails"):
            g = raiz.find(grupo)
            for e in list(g) if g is not None else []:
                if e.get("name") == sobreposta:
                    g.remove(e)
        for vp in list(raiz.iter("viewpoint")):
            if vp.get("name") == sobreposta:
                vp.getparent().remove(vp)
        acoes = raiz.find("actions")
        for a in list(acoes):
            if a.find("source") is not None and a.find("source").get("worksheet") == sobreposta:
                acoes.remove(a)
    ws = next(w for w in raiz.find("worksheets") if w.get("name") == grafico)
    runs = list(ws.iter("run"))
    for run in runs:
        if (run.text or "").strip() == titulo_antigo:
            run.text = titulo_novo
        elif "Meta" in (run.text or ""):
            run.getparent().remove(run)


# --- 6. filtros rápidos -----------------------------------------------------------------------------------------

def religar_filtros_rapidos(raiz):
    """Filtro rápido cuja planilha deixou de ter aquele filtro passa a ficar preso a outra planilha do painel que tem."""
    por_nome = {w.get("name"): w for w in raiz.find("worksheets")}
    religados = []
    for painel in raiz.find("dashboards"):
        planilhas = [z.get("name") for z in painel.iter("zone") if z.get("name") in por_nome and not z.get("type-v2")]
        for zona in painel.iter("zone"):
            if zona.get("type-v2") != "filter" or zona.get("name") not in por_nome:
                continue
            campo = zona.get("param")
            tem = lambda n: any(f.get("column") == campo and f.get("class") != "relative-date" for f in filtros(por_nome[n]))
            if tem(zona.get("name")):
                continue
            outra = next((n for n in planilhas if tem(n)), None)
            if outra:
                religados.append(f"{painel.get('name')}: {re.sub(r'^.*\]\.', '', campo)} -> {outra}")
                zona.set("name", outra)
            else:
                religados.append(f"{painel.get('name')}: {campo} SEM PLANILHA")
    return religados


# --- 5. intervalos de datas ------------------------------------------------------------------------------------

def soltar_fim_dos_intervalos(raiz):
    soltos = 0
    for ws in raiz.find("worksheets"):
        for f in filtros(ws):
            fim = f.find("max")
            if f.get("class") == "quantitative" and fim is not None and (fim.text or "").startswith("#"):
                f.remove(fim)
                soltos += 1
    return soltos


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    entrada, saida = Path(sys.argv[1]), Path(sys.argv[2])
    with zipfile.ZipFile(entrada) as z:
        twb = next(n for n in z.namelist() if n.lower().endswith(".twb") and "/" not in n)
        raiz = etree.fromstring(z.read(twb), etree.XMLParser(huge_tree=True))
        outros = [(i, z.read(i.filename)) for i in z.infolist() if i.filename != twb]

    print(f"5. intervalos de datas sem fim fixo: {soltar_fim_dos_intervalos(raiz)} filtros")
    fontes = {d.get("name"): d for d in raiz.find("datasources")}
    por_nome = {w.get("name"): w for w in raiz.find("worksheets")}
    ja_criados, status_criados = {}, []
    for nome, cfg in KPIS.items():
        ws = por_nome.get(nome)
        if ws is None:
            print(f"1. {nome}: não existe")
            continue
        cor = next(e.get("column") for e in ws.iter("color") if e.get("column"))
        ds = fontes[re.match(r"\[([^\]]+)\]", cor).group(1)]
        print(f"1. {nome}: {kpi_em_faixa(ws, ds, cfg, ja_criados)}")
        _, col_status = calculos_do_indicador(ds, cfg, ja_criados)
        status_criados.append(col_status.get("name").strip("[]"))
        legendas_do_indicador(raiz, ws, ds.get("name"), status_criados[-1])
    for nome in VOLUMES:
        print(f"2. {nome}: {volume_em_meses(por_nome[nome]) if nome in por_nome else 'não existe'}")
    cores(raiz)
    print(f"6. filtros rápidos religados: {religar_filtros_rapidos(raiz)}")
    print("3. laranjas trocados fora dos indicadores com meta")
    tirar_ponto_solto(raiz)
    print("4. ponto solto do SLA Cliente retirado do Protocolos Recebidos")

    texto = etree.tostring(raiz, encoding="utf-8", xml_declaration=True)
    etree.fromstring(texto, etree.XMLParser(huge_tree=True))
    with zipfile.ZipFile(saida, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr(saida.with_suffix(".twb").name, texto)
        for item, conteudo in outros:
            z.writestr(item, conteudo)
    print(f"Gravado em {saida}")


if __name__ == "__main__":
    main()
