"""Indicadores com meta comparam o mês atual com um mês escolhido no painel (gera uma nova versão; a de entrada não muda).

Os 14 indicadores do redesenho mostram duas barras, antes sempre o mês anterior e o atual (filtro relativo de data).
Agora a segunda barra continua sendo o mês atual e a primeira é o mês do parâmetro "Mês de comparação", escolhido num
seletor ao lado do filtro de mês de cada painel. Se o mês escolhido for o atual (ou um mês futuro), a primeira barra
volta a ser o mês anterior. O valor inicial, "Mês anterior", também é o mês anterior, então quem não mexe vê o mesmo
de antes. Volumes de 6 meses e visões de 3 meses continuam com o filtro relativo.

A lista do parâmetro vai de PRIMEIRO_MES a ULTIMO_MES: para estender, mude ULTIMO_MES e gere a versão de novo.

Uso (a partir da pasta daily-experiencia):
  .venv\\Scripts\\python.exe ferramentas\\mes_de_comparacao_tableau.py <entrada.twbx> <saída.twbx>
"""
import copy
import re
import sys
import zipfile
from datetime import date
from pathlib import Path

from lxml import etree

sys.path.insert(0, str(Path(__file__).resolve().parent))
from unificar_paineis_tableau import (criar_calculo, dependencia_parametro, filtrar_por_calculo, filtros,  # noqa: E402
                                      fonte_parametros)

PRIMEIRO_MES, ULTIMO_MES = date(2025, 1, 1), date(2027, 12, 1)
# Valor inicial do parâmetro, sem apelido: com apelido, o seletor do Tableau Cloud abria em branco
MES_ANTERIOR = '"Mês anterior"'
LEGENDA = "Mês de comparação"
MESES = ["janeiro", "fevereiro", "março", "abril", "maio", "junho", "julho", "agosto", "setembro", "outubro",
         "novembro", "dezembro"]
SUBTITULO_ANTIGO, SUBTITULO_NOVO = "  mês anterior e atual · cor pela meta", "  mês de comparação e atual · cor pela meta"
# filtro do painel ao lado do qual entra o seletor (o primeiro que casar, no layout de desktop e no de celular)
FILTRO_DO_SELETOR = [r"\[mn:[^\]]+:ok\]", r"\[my:[^\]]+:ok\]"]


def meses():
    m = ULTIMO_MES
    while m >= PRIMEIRO_MES:
        yield m
        m = date(m.year - (m.month == 1), 12 if m.month == 1 else m.month - 1, 1)


def criar_parametro_de_mes(raiz):
    ds = fonte_parametros(raiz)
    numero = 1 + max([int(n) for c in ds.findall("column") for n in re.findall(r"\[Parameter (\d+)\]", c.get("name"))]
                     or [0])
    coluna = etree.SubElement(ds, "column", caption=LEGENDA, datatype="string", name=f"[Parameter {numero}]",
                              **{"param-domain-type": "list"}, role="measure", type="nominal", value=MES_ANTERIOR)
    etree.SubElement(coluna, "calculation", {"class": "tableau", "formula": MES_ANTERIOR})
    membros = etree.SubElement(coluna, "members")
    etree.SubElement(membros, "member", value=MES_ANTERIOR)
    for m in meses():
        etree.SubElement(membros, "member", alias=f"{MESES[m.month - 1]} de {m.year}", value=f'"{m.isoformat()}"')
    return coluna


def formula(data, parametro):
    p = f"[Parameters].{parametro.get('name')}"
    atual = "DATE(DATETRUNC('month', TODAY()))"
    anterior = f"DATE(DATEADD('month', -1, {atual}))"
    escolhido = f"(IF {p} = {MES_ANTERIOR} OR DATE({p}) >= {atual} THEN {anterior} ELSE DATE({p}) END)"
    mes = f"DATE(DATETRUNC('month', [{data}]))"
    return f"{mes} = {atual} OR {mes} = {escolhido}"


def indicadores(raiz):
    """Planilhas com o filtro relativo de 2 meses do redesenho: (planilha, filtro, fonte, campo de data)."""
    for ws in raiz.find("worksheets"):
        for f in filtros(ws):
            m = re.fullmatch(r"\[([^\]]+)\]\.\[none:(.+):qk\]", f.get("column") or "")
            if f.get("class") == "relative-date" and f.get("first-period") == "-1" and m:
                yield ws, f, m.group(1), m.group(2)


def trocar_subtitulo(ws):
    trocados = 0
    for run in ws.iter("run"):
        if run.text == SUBTITULO_ANTIGO:
            run.text = SUBTITULO_NOVO
            trocados += 1
    return trocados


def seletor_no_painel(painel, parametro):
    """Põe o seletor ao lado do filtro de mês do painel, uma vez por layout (desktop e celular), como
    controle_de_parametro de unificar_paineis_tableau.py faz ao lado do filtro de Nível."""
    for padrao in FILTRO_DO_SELETOR:
        zonas = [z for z in painel.iter("zone") if z.get("type-v2") == "filter" and re.search(padrao, z.get("param") or "")]
        if zonas:
            break
    else:
        return 0
    por_layout = {}
    for z in zonas:
        layout = next((a for a in z.iterancestors() if a.tag in ("devicelayout", "dashboard")), None)
        por_layout.setdefault(id(layout), z)
    proximo_id = 1 + max(int(z.get("id")) for z in painel.iter("zone") if z.get("id"))
    for zona in por_layout.values():
        pai = zona.getparent()
        controle = copy.deepcopy(zona)
        for a in ("name", "values"):
            controle.attrib.pop(a, None)
        controle.set("id", str(proximo_id))
        proximo_id += 1
        controle.set("type-v2", "paramctrl")
        controle.set("param", f"[Parameters].{parametro.get('name')}")
        controle.set("mode", "compact")
        if pai.get("param") == "horz":
            # divide a largura da linha de filtros entre os controles, agora um a mais
            irmas = [z for z in pai if z.get("type-v2") in ("filter", "paramctrl")] + [controle]
            inicio, largura = int(pai.get("x")), int(pai.get("w"))
            cada = largura // len(irmas)
            for i, z in enumerate(irmas):
                z.set("x", str(inicio + i * cada))
                z.set("w", str(cada if i < len(irmas) - 1 else largura - cada * (len(irmas) - 1)))
        zona.addnext(controle)
    dependencia_parametro(painel, parametro)
    return len(por_layout)


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    entrada, saida = Path(sys.argv[1]), Path(sys.argv[2])
    with zipfile.ZipFile(entrada) as z:
        twb = next(n for n in z.namelist() if n.lower().endswith(".twb") and "/" not in n)
        raiz = etree.fromstring(z.read(twb), etree.XMLParser(huge_tree=True))
        outros = {i.filename: (i, z.read(i.filename)) for i in z.infolist() if i.filename != twb}

    fontes = {d.get("name"): d for d in raiz.find("datasources")}
    parametro = criar_parametro_de_mes(raiz)
    calculos, alteradas = {}, set()
    for ws, filtro, ds_nome, data in list(indicadores(raiz)):
        if (ds_nome, data) not in calculos:
            calculos[ds_nome, data] = criar_calculo(fontes[ds_nome], f"{LEGENDA} ({data})", formula(data, parametro))
        filtrar_por_calculo(ws, ds_nome, calculos[ds_nome, data], [], remover=(f"[none:{data}:qk]",))
        dependencia_parametro(ws.find("table/view"), parametro)
        alteradas.add(ws.get("name"))
        print(f"+ {ws.get('name')}: mês atual e mês de comparação por {data} (subtítulos: {trocar_subtitulo(ws)})")

    for painel in raiz.find("dashboards"):
        if {z.get("name") for z in painel.iter("zone")} & alteradas:
            print(f"  seletor em {painel.get('name')}: {seletor_no_painel(painel, parametro)} layouts")

    texto = etree.tostring(raiz, encoding="utf-8", xml_declaration=True)
    etree.fromstring(texto, etree.XMLParser(huge_tree=True))
    with zipfile.ZipFile(saida, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr(saida.with_suffix(".twb").name, texto)
        for item, conteudo in outros.values():
            z.writestr(item, conteudo)
    print(f"\n{len(alteradas)} indicadores alterados. Gravado em {saida}")


if __name__ == "__main__":
    main()
