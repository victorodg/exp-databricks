"""Troca, num workbook do Tableau, as fontes publicadas no Tableau Cloud pelas views dexp_vw_* do Databricks.

Cada fonte publicada (sqlproxy) que tem view correspondente continua inteira (cálculos, apelidos, formatos, cores,
pastas); só a conexão é trocada pela do Databricks, no formato que o próprio Tableau grava. As colunas que na view
ganharam " (2)" (nomes que só diferem em maiúsculas) são mapeadas de volta para o nome de campo original, então
nenhum cálculo ou planilha muda. O vínculo do workbook com o original publicado também é removido, para a cópia não
sobrescrever o workbook de produção se for publicada.

O modelo da conexão vem de um workbook em que uma fonte já foi ligada ao Databricks pelo Tableau Desktop (login,
servidor, caminho HTTP e as customizações do driver).

Uso (a partir da pasta daily-experiencia):
  .venv\\Scripts\\python.exe ferramentas\\trocar_fontes_tableau.py <original.twbx ou .twb> <modelo.twbx> <saída.twbx>

Se o original for um .twb, as imagens do pacote vêm do modelo.
"""
import copy
import random
import string
import sys
import zipfile
from pathlib import Path

from lxml import etree

sys.path.insert(0, str(Path(__file__).resolve().parent))
from comparar_extract import ESQUEMA, cliente, sql_databricks  # noqa: E402
from gerar_views_tableau import SAIDAS  # noqa: E402

CATALOGO, SCHEMA = ESQUEMA.split(".")

# fonte no workbook (caption) -> view; os nomes são os dos extracts, menos o "(1)" do arquivo baixado duas vezes
VIEWS = {extract.removesuffix("(1)"): gold.replace("dexp_gold_", "dexp_vw_") for extract, gold in SAIDAS.items()}

# tipo no Databricks -> (remote-type do Tableau, local-type)
TIPOS = {"string": (129, "string"), "bigint": (20, "integer"), "int": (3, "integer"), "double": (5, "real"),
         "date": (7, "date"), "timestamp": (135, "datetime"), "boolean": (11, "boolean")}


def ler_twb(caminho):
    caminho = Path(caminho)
    if caminho.suffix.lower() == ".twbx":
        with zipfile.ZipFile(caminho) as z:
            nome = next(n for n in z.namelist() if n.lower().endswith(".twb") and "/" not in n)
            return etree.fromstring(z.read(nome), etree.XMLParser(huge_tree=True, remove_blank_text=False))
    return etree.parse(str(caminho), etree.XMLParser(huge_tree=True)).getroot()


def id_aleatorio():
    return "".join(random.choices(string.ascii_lowercase + string.digits, k=28))


def conexao_modelo(raiz):
    """O <connection class='databricks'> que o Tableau Desktop gravou no workbook modelo."""
    for nc in raiz.iter("named-connection"):
        con = nc.find("connection")
        if con is not None and con.get("class") == "databricks":
            return nc.get("caption"), con
    raise SystemExit("O modelo não tem nenhuma conexão com o Databricks.")


def colunas_view(w, view):
    return [(r[0], r[1].lower()) for r in sql_databricks(w, f"DESCRIBE TABLE {ESQUEMA}.{view}")
            if r[0] and not r[0].startswith("#")]


def nome_na_view(remoto, colunas):
    """Nome da coluna na view: o mesmo do extract ou, se só diferia em maiúsculas de outra, com " (2)"."""
    nomes = [n for n, _ in colunas]
    if remoto in nomes:
        return remoto
    if f"{remoto} (2)" in nomes:
        return f"{remoto} (2)"
    return None


def trocar_fonte(ds, view, colunas, servidor, modelo):
    tipos = dict(colunas)
    nome_con = f"databricks.{id_aleatorio()}"
    relacao = etree.Element("relation", connection=nome_con, name=view,
                            table=f"[{CATALOGO}].[{SCHEMA}].[{view}]", type="table")

    antiga = ds.find("connection")
    nova = etree.Element("connection", {"class": "federated"})
    ncs = etree.SubElement(nova, "named-connections")
    nc = etree.SubElement(ncs, "named-connection", caption=servidor, name=nome_con)
    nc.append(copy.deepcopy(modelo))
    nova.append(copy.deepcopy(relacao))

    usados, mapas, registros, faltando = set(), [], [], []
    for reg in antiga.find("metadata-records"):
        if reg.get("class") not in ("column", "measure"):
            continue
        remoto = reg.findtext("remote-name")
        na_view = nome_na_view(remoto, colunas)
        if na_view is None:
            faltando.append(remoto)
            continue
        usados.add(na_view)
        local = reg.findtext("local-name")
        mapas.append((local, na_view))
        remote_type, local_type = TIPOS.get(tipos[na_view], (129, reg.findtext("local-type")))
        novo = etree.Element("metadata-record", {"class": reg.get("class")})
        for tag, valor in [("remote-name", na_view), ("remote-type", str(remote_type)), ("local-name", local),
                           ("parent-name", f"[{view}]"), ("remote-alias", na_view),
                           ("ordinal", reg.findtext("ordinal")), ("local-type", reg.findtext("local-type") or local_type),
                           ("aggregation", reg.findtext("aggregation")), ("contains-null", "true")]:
            if valor is not None:
                etree.SubElement(novo, tag).text = valor
        if (reg.findtext("local-type") or local_type) == "string":
            etree.SubElement(novo, "collation", flag="0", name="binary")
        etree.SubElement(novo, "object-id").text = reg.findtext("object-id") or "[Migrated Data]"
        registros.append(novo)

    cols = etree.SubElement(nova, "cols")
    for local, na_view in mapas:
        etree.SubElement(cols, "map", key=local, value=f"[{view}].[{na_view}]")
    mr = etree.SubElement(nova, "metadata-records")
    mr.extend(registros)
    nova.tail = antiga.tail
    ds.replace(antiga, nova)

    # o resto que só faz sentido para fonte publicada
    for filho in list(ds):
        if filho.tag in ("repository-location",) or "data-source-tree" in str(filho.tag):
            ds.remove(filho)
    for obj in ds.iter("object"):
        for atributo in [a for a in obj.attrib if "origin-pds" in a]:
            del obj.attrib[atributo]
        props = obj.find("properties")
        if props is not None and props.find("relation") is not None:
            r = props.find("relation")
            novo_r = copy.deepcopy(relacao)
            novo_r.tail = r.tail
            props.replace(r, novo_r)

    sobrando = [n for n, _ in colunas if n not in usados]
    return faltando, sobrando


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    original, modelo_arq, saida = (Path(a) for a in sys.argv[1:4])
    raiz = ler_twb(original)
    servidor, modelo = conexao_modelo(ler_twb(modelo_arq))
    w = cliente()

    trocas = {}
    for ds in raiz.find("datasources"):
        con = ds.find("connection")
        if con is None or con.get("class") != "sqlproxy":
            continue
        view = VIEWS.get(ds.get("caption"))
        if view is None:
            print(f"- mantida no Tableau Cloud: {ds.get('caption')}")
            continue
        faltando, sobrando = trocar_fonte(ds, view, colunas_view(w, view), servidor, modelo)
        antigo = ds.get("name")
        trocas[antigo] = "federated." + antigo.removeprefix("sqlproxy.")
        print(f"+ {ds.get('caption')} -> {view}"
              + (f" | campos da fonte que a view não tem: {faltando}" if faltando else "")
              + (f" | colunas da view não usadas: {sobrando}" if sobrando else ""))

    # sem o vínculo com o workbook publicado
    for rl in raiz.findall("repository-location"):
        raiz.remove(rl)

    texto = etree.tostring(raiz, encoding="utf-8", xml_declaration=True).decode("utf-8")
    for antigo, novo in trocas.items():
        texto = texto.replace(antigo, novo)
    restantes = [a for a in trocas if a in texto]
    assert not restantes, restantes
    etree.fromstring(texto.encode("utf-8"), etree.XMLParser(huge_tree=True))  # continua sendo XML válido

    # imagens e demais arquivos do pacote: do original se for .twbx, senão do modelo
    pacote = original if original.suffix.lower() == ".twbx" else modelo_arq
    with zipfile.ZipFile(pacote) as z, zipfile.ZipFile(saida, "w", zipfile.ZIP_DEFLATED) as novo:
        novo.writestr(saida.with_suffix(".twb").name, texto.encode("utf-8"))
        for item in z.infolist():
            if not (item.filename.lower().endswith(".twb") and "/" not in item.filename):
                novo.writestr(item, z.read(item.filename))
    print(f"\n{len(trocas)} fontes trocadas. Gravado em {saida}")


if __name__ == "__main__":
    main()
