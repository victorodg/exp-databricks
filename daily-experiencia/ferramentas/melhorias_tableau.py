"""Aplica melhorias de visualização no workbook do Daily Experiência BR (gera uma nova versão; o original não muda).

Melhorias implementadas:
  dynamics_por_fase: nos painéis Dynamics CB e Dynamics CF, troca os 6 gráficos "Fase 1/Fase 2 × SLA Cliente/EXP/5h"
    (uma barra por mês com o % em cima, que vira um quadrado quando o filtro deixa só um mês) pelas 3 planilhas
    "SLA ... por Fase" já usadas no Dynamics Consolidado, uma barra horizontal por fase. As planilhas novas são cópias
    das do Consolidado, ligadas aos filtros e ações do painel de destino e filtradas pelo tipo de protocolo.
  filtro_sla_expurgado: as planilhas que mostram a fatia de cada valor de SLA Experiência / SLA 5 Horas sobre o total
    de registros passam a considerar só "DENTRO DO PRAZO" e "FORA DO PRAZO", como as de SLA Cliente já faziam. Assim as
    tarefas expurgadas (SLA = "EXPURGADO", aba "Expurgo SLA") não aparecem nem entram no percentual.

Uso (a partir da pasta daily-experiencia):
  .venv\\Scripts\\python.exe ferramentas\\melhorias_tableau.py <entrada.twbx> <saída.twbx>
"""
import copy
import re
import sys
import zipfile
from pathlib import Path

from lxml import etree

# planilha do Consolidado -> (prefixo das antigas Fase 1 e Fase 2 a substituir, sem "Dynamics CB "/"Dynamics CF ")
POR_FASE = {
    "Dynamics CB+CF - SLA Cliente por Fase": ("Fase 1 - 3 Meses", "Fase 2 - 3 Meses"),
    "Dynamics CB+CF - SLA EXP por Fase": ("Fase 1 SLA EXP - 3 Meses", "Fase 2 SLA EXP - 3 Meses"),
    "Dynamics CB+CF - SLA 5h por Fase": ("Fase 1 SLA 5h - 3 Meses", "Fase 2 SLA 5h - 3 Meses"),
}
PAINEIS = {"Dynamics CB": "Protocolos CB", "Dynamics CF": "Protocolos CF"}
# filtros que são da própria visão "por Fase" e ficam como estão na cópia
FILTROS_DA_VISAO = ("[none:Fase:nk]", "[none:Base:nk]", "[none:Solução:nk]")


def chave(nome):
    """Nome sem espaços, para achar "Fase 2 SLA EXP- 3 Meses" e "Fase 2 SLA EXP - 3 Meses" igual."""
    return re.sub(r"\s+", "", nome)


def coluna_do_filtro(f):
    return re.sub(r"^\[[^\]]+\]\.", "", f.get("column") or "")


def filtros(ws):
    return ws.find("table/view").findall("filter")


def copiar_planilha(modelo, nome, referencia):
    """Cópia de `modelo` chamada `nome`, com os filtros de painel (grupos, ações, tipo de protocolo) de `referencia`."""
    nova = copy.deepcopy(modelo)
    nova.set("name", nome)
    view = nova.find("table/view")
    da_ref = {coluna_do_filtro(f): f for f in filtros(referencia)}
    for f in filtros(nova):
        col = coluna_do_filtro(f)
        if col in FILTROS_DA_VISAO:
            continue
        if col in da_ref:
            substituto = copy.deepcopy(da_ref.pop(col))
            substituto.tail = f.tail
            view.replace(f, substituto)
        else:
            view.remove(f)  # filtro que só existe no Consolidado (ex.: Fonte)
    # filtros do painel de destino que a cópia ainda não tem (ex.: ações com dois campos)
    ultimo = filtros(nova)[-1]
    for col, f in da_ref.items():
        if col not in FILTROS_DA_VISAO:
            ultimo.addnext(copy.deepcopy(f))
            ultimo = ultimo.getnext()
    # <slices> lista os campos filtrados, na mesma ordem dos filtros
    slices = view.find("slices")
    if slices is not None:
        for c in list(slices):
            slices.remove(c)
        for f in filtros(nova):
            etree.SubElement(slices, "column").text = f.get("column")
    return nova


def trocar_no_painel(painel, antigas_por_nova):
    """Em cada layout do painel, a zona da Fase 1 passa a mostrar a planilha nova, ocupando também o espaço da Fase 2."""
    removidas = {a for par in antigas_por_nova.values() for a in par}
    for zona in list(painel.iter("zone")):
        nome = zona.get("name")
        if nome not in removidas or zona.getparent() is None:
            continue
        if zona.get("type-v2"):  # legenda da planilha antiga
            zona.getparent().remove(zona)
            continue
        nova = next(n for n, par in antigas_por_nova.items() if nome in par)
        fase1, fase2 = antigas_por_nova[nova]
        pai = zona.getparent()
        if nome == fase1:
            zona.set("name", nova)
            irmas = [z for z in pai if z.get("name") == fase2]
            if irmas and pai.get("param") == "horz":
                fim = int(irmas[0].get("x")) + int(irmas[0].get("w"))
                largura_antiga, largura = int(zona.get("w")), fim - int(zona.get("x"))
                zona.set("w", str(largura))
                if zona.get("fixed-size"):  # largura fixa em pixels, numa sequência horizontal
                    zona.set("fixed-size", str(round(int(zona.get("fixed-size")) * largura / largura_antiga)))
                # o espaço vazio entre as duas
                for z in list(pai):
                    if z is not zona and z.get("type-v2") == "empty" and int(zona.get("x")) < int(z.get("x")) < fim:
                        pai.remove(z)
        else:
            pai.remove(zona)


def dynamics_por_fase(raiz):
    planilhas = raiz.find("worksheets")
    por_nome = {w.get("name"): w for w in planilhas}
    por_chave = {chave(n): n for n in por_nome}
    janelas = raiz.find("windows")
    janela_de = {j.get("name"): j for j in janelas if j.get("class") == "worksheet"}
    paineis = {d.get("name"): d for d in raiz.find("dashboards")}
    removidas = set()

    for nome_painel, tipo in PAINEIS.items():
        sigla = nome_painel.split()[-1]
        antigas_por_nova = {}
        for modelo_nome, (f1, f2) in POR_FASE.items():
            fase1 = por_chave[chave(f"Dynamics {sigla} {f1}")]
            fase2 = por_chave[chave(f"Dynamics {sigla} {f2}")]
            nova_nome = modelo_nome.replace("CB+CF", sigla)
            nova = copiar_planilha(por_nome[modelo_nome], nova_nome, por_nome[fase1])
            membros = [g.get("member") for f in filtros(nova) if coluna_do_filtro(f) == "[none:Tipo Protocolo:nk]"
                       for g in f.iter("groupfilter")]
            assert f'"{tipo}"' in membros, (nova_nome, membros)
            por_nome[fase2].addnext(nova)
            janela = copy.deepcopy(janela_de[modelo_nome])
            janela.set("name", nova_nome)
            janela_de[fase2].addnext(janela)
            antigas_por_nova[nova_nome] = (fase1, fase2)
            removidas |= {fase1, fase2}
            print(f"+ {nome_painel}: '{nova_nome}' no lugar de '{fase1}' e '{fase2}'")
        trocar_no_painel(paineis[nome_painel], antigas_por_nova)

    # as planilhas antigas saem do workbook, com janelas, miniaturas e ações que partiam delas
    for n in removidas:
        planilhas.remove(por_nome[n])
        janelas.remove(janela_de[n])
    # estado de zoom e seleção que as janelas dos painéis guardam para cada planilha
    for vp in list(janelas.iter("viewpoint")):
        if vp.get("name") in removidas:
            vp.getparent().remove(vp)
    miniaturas = raiz.find("thumbnails")
    if miniaturas is not None:
        for m in list(miniaturas):
            if m.get("name") in removidas:
                miniaturas.remove(m)
    acoes = raiz.find("actions")
    for a in list(acoes):
        origem = a.find("source")
        if origem is not None and origem.get("worksheet") in removidas:
            acoes.remove(a)
    return removidas


# planilha -> campo de SLA que ela mostra como fatias do total
PLANILHAS_SLA = {
    "Dynamics CB SLA EXP": "SLA Experiência", "Dynamics CF SLA EXP": "SLA Experiência",
    "Dynamics CB+CF SLA EXP": "SLA Experiência", "Dynamics CB+CF SLA 5h": "SLA 5 Horas",
}
MODELO_FILTRO_SLA = "Dynamics CB+CF SLA Cliente"  # já filtra SLA Cliente em DENTRO DO PRAZO / FORA DO PRAZO


def filtro_sla_expurgado(raiz):
    por_nome = {w.get("name"): w for w in raiz.find("worksheets")}
    modelo = next(f for f in filtros(por_nome[MODELO_FILTRO_SLA])
                  if coluna_do_filtro(f) == "[none:SLA Cliente:nk]")
    for nome, campo in PLANILHAS_SLA.items():
        ws = por_nome.get(nome)
        if ws is None:
            continue
        instancia = f"[none:{campo}:nk]"
        if any(coluna_do_filtro(f) == instancia for f in filtros(ws)):
            continue
        novo = etree.fromstring(etree.tostring(modelo).replace(b"[none:SLA Cliente:nk]", instancia.encode("utf-8")))
        ultimo = filtros(ws)[-1]
        fonte = ultimo.get("column").split("].[")[0] + "]"
        novo.set("column", f"{fonte}.{instancia}")
        novo.tail = ultimo.tail
        ultimo.addnext(novo)
        slices = ws.find("table/view/slices")
        if slices is not None:
            etree.SubElement(slices, "column").text = novo.get("column")
        print(f"+ {nome}: só DENTRO DO PRAZO e FORA DO PRAZO em {campo}")


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    entrada, saida = Path(sys.argv[1]), Path(sys.argv[2])
    with zipfile.ZipFile(entrada) as z:
        twb = next(n for n in z.namelist() if n.lower().endswith(".twb") and "/" not in n)
        raiz = etree.fromstring(z.read(twb), etree.XMLParser(huge_tree=True))

        removidas = dynamics_por_fase(raiz)
        filtro_sla_expurgado(raiz)

        texto = etree.tostring(raiz, encoding="utf-8", xml_declaration=True)
        # nenhuma referência às planilhas removidas pode sobrar
        for n in removidas:
            escapado = n.replace("&", "&amp;").replace("'", "&apos;").replace('"', "&quot;")
            sobra = [m.start() for m in re.finditer(re.escape(f'"{escapado}"'), texto.decode("utf-8"))]
            assert not sobra, (n, len(sobra))

        with zipfile.ZipFile(saida, "w", zipfile.ZIP_DEFLATED) as novo:
            novo.writestr(saida.with_suffix(".twb").name, texto)
            for item in z.infolist():
                if item.filename != twb:
                    novo.writestr(item, z.read(item.filename))
    print(f"Gravado em {saida}")


if __name__ == "__main__":
    main()
