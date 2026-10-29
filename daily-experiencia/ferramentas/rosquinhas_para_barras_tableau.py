"""Troca as rosquinhas de SLA do workbook pela barra 100% horizontal usada no SLA Experiência do Dynamics.

As rosquinhas (duas pizzas em eixo duplo: os status do SLA e um círculo com o % no meio) passam a ter o mesmo desenho
da planilha "Dynamics CB+CF SLA EXP": uma barra por mês, dividida pelos valores do status, com o % de cada parte.
Cada planilha continua com a própria fonte, filtros, título e cores do status; muda só a visualização.

Uso (a partir da pasta daily-experiencia):
  .venv\\Scripts\\python.exe ferramentas\\rosquinhas_para_barras_tableau.py <entrada.twbx> <saída.twbx>
"""
import copy
import re
import sys
import zipfile
from pathlib import Path

from lxml import etree

MODELO = "Dynamics CB+CF SLA EXP"
ROSQUINHAS = ["Whats GN SLA Primeiro Contato", "SLA App AVON", "SLA App Consultoria", "SLA App FV",
              "SLA App Sempre Presente"]


def fonte_de(ws):
    return ws.find("table/view/datasources/datasource").get("name")


def campos_do_modelo(modelo):
    pane = modelo.find("table/panes/pane")
    enc = pane.find("encodings")
    return {"cor": enc.find("color").get("column"), "texto": enc.find("text").get("column"),
            "contagem": re.search(r"\* (\[[^*]+\])\)$", modelo.find("table/cols").text).group(1)}


def campos_da_rosquinha(ws):
    for pane in ws.find("table/panes"):
        enc = pane.find("encodings")
        if enc is not None and enc.find("color") is not None and enc.find("wedge-size") is not None:
            return {"cor": enc.find("color").get("column"), "texto": enc.find("wedge-size").get("column"),
                    "contagem": enc.find("text").get("column")}
    return None


def converter(ws, modelo):
    origem = campos_do_modelo(modelo)
    destino = campos_da_rosquinha(ws)
    if destino is None:
        return False
    tabela = ws.find("table")
    trocas = [(origem[k], destino[k]) for k in ("texto", "contagem", "cor")] + [(fonte_de(modelo), fonte_de(ws))]

    def adaptar(elemento):
        texto = etree.tostring(elemento, encoding="unicode")
        for de, para in trocas:
            texto = texto.replace(de, para)
        return etree.fromstring(texto.encode("utf-8"))

    # o estilo vem do modelo, menos os títulos dos filtros rápidos, que continuam sendo os da própria planilha
    estilo_novo = adaptar(modelo.find("table/style"))
    for f in list(estilo_novo.iter("format")):
        if f.get("attr") == "title":
            f.getparent().remove(f)
    regras = {r.get("element"): r for r in estilo_novo.findall("style-rule")}
    for regra in tabela.find("style").findall("style-rule"):
        titulos = [f for f in regra.findall("format") if f.get("attr") == "title"]
        if titulos:
            destino_regra = regras.get(regra.get("element"))
            if destino_regra is None:
                destino_regra = etree.SubElement(estilo_novo, "style-rule", element=regra.get("element"))
                regras[regra.get("element")] = destino_regra
            destino_regra.extend(copy.deepcopy(t) for t in titulos)
    pane_novo = adaptar(modelo.find("table/panes/pane"))
    pane_novo.find("mark").set("class", "Bar")
    panes = etree.Element("panes")
    panes.append(pane_novo)

    for antigo, novo in [(tabela.find("style"), estilo_novo), (tabela.find("panes"), panes)]:
        novo.tail = antigo.tail
        tabela.replace(antigo, novo)
    colunas_antigas = (tabela.find("cols").text or "").strip()
    tabela.find("rows").text = None
    tabela.find("cols").text = (f"({colunas_antigas} * {destino['contagem']})" if colunas_antigas
                                else destino["contagem"])
    return True


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    entrada, saida = Path(sys.argv[1]), Path(sys.argv[2])
    with zipfile.ZipFile(entrada) as z:
        twb = next(n for n in z.namelist() if n.lower().endswith(".twb") and "/" not in n)
        raiz = etree.fromstring(z.read(twb), etree.XMLParser(huge_tree=True))
        outros = [(i, z.read(i.filename)) for i in z.infolist() if i.filename != twb]

    por_nome = {w.get("name"): w for w in raiz.find("worksheets")}
    for nome in ROSQUINHAS:
        if nome in por_nome and converter(por_nome[nome], por_nome[MODELO]):
            print(f"+ {nome}: barra 100% no lugar da rosquinha")
        else:
            print(f"- {nome}: não encontrada ou não é uma rosquinha")

    texto = etree.tostring(raiz, encoding="utf-8", xml_declaration=True)
    etree.fromstring(texto, etree.XMLParser(huge_tree=True))
    with zipfile.ZipFile(saida, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr(saida.with_suffix(".twb").name, texto)
        for item, conteudo in outros:
            z.writestr(item, conteudo)
    print(f"Gravado em {saida}")


if __name__ == "__main__":
    main()
