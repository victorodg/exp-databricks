"""Liga um workbook às fontes publicadas no Tableau Cloud por coleta/publicar_tableau.py, no lugar do Databricks.

Quem abre o workbook passa a precisar só de acesso ao Tableau Cloud. Cada fonte continua inteira (cálculos, apelidos,
formatos, cores, pastas); só a conexão muda, para o formato que o Tableau grava em fonte publicada (sqlproxy). As colunas
que na view ganharam " (2)" continuam mapeadas para o nome de campo original, então nenhum cálculo ou planilha muda.
Fontes fora de [tableau.fontes] (as que já estão no Cloud e os arquivos do Drive) ficam como estão.

Uso (a partir da pasta daily-experiencia):
  .venv\\Scripts\\python.exe ferramentas\\ligar_fontes_publicadas_tableau.py <original.twbx> <saída.twbx>
"""
import sys
import zipfile
from pathlib import Path

import tableauserverclient as TSC
from lxml import etree

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "coleta"))
from publicar_tableau import carregar_config, conectar_tableau, id_do_projeto  # noqa: E402

# Na extração, data é 133; ao vivo no Databricks é 7
REMOTE_TYPE_EXTRACAO = {"7": "133"}

# Toda fonte publicada leva um registro de capacidades na conexão: sem ele o Tableau Desktop fecha ao abrir o workbook
# (0xC0000005). Valores do que o Tableau grava para fontes em extração, sem o "datasource" e o "update-time", que ele
# refaz ao conectar.
CAPACIDADES_LIGADAS = [
    "CAP_CREATE_TEMP_TABLES", "CAP_QUERY_BLENDING_PREFER_LOCAL_MAPPING_TABLES", "CAP_QUERY_BLENDING_REMOTE_MAPPING_TABLES",
    "CAP_QUERY_CASE_INSENSITIVE_CONTAINS", "CAP_QUERY_IGNORE_HINT_CHECK_NOT_NULL", "CAP_QUERY_SORT_BY", "CAP_QUERY_SUBQUERIES",
    "CAP_QUERY_SUBQUERY_QUERY_CONTEXT", "CAP_QUERY_SUPPORTS_LODJOINS", "CAP_QUERY_SUPPORT_ANALYTIC_FUNCTIONS", "CAP_QUERY_TOP_N",
    "CAP_QUERY_USE_QUERY_FUSION", "CAP_SUPPORTS_SPLIT_FROM_LEFT", "CAP_SUPPORTS_SPLIT_FROM_RIGHT"]
DIALETO = """"<dialect-definition>
  <primary-dialect class='hyper' version='0.0.0'>
  </primary-dialect>
  <overlay-dialect-set>
    <overlay-dialect class='vizengine' version='0.1.0'>
    </overlay-dialect>
  </overlay-dialect-set>
</dialect-definition>
\""""


def registro_de_capacidades():
    reg = etree.Element("metadata-record", {"class": "capability"})
    etree.SubElement(reg, "remote-name")
    etree.SubElement(reg, "remote-type").text = "0"
    etree.SubElement(reg, "parent-name").text = "[sqlproxy]"
    etree.SubElement(reg, "remote-alias")
    etree.SubElement(reg, "aggregation").text = "Count"
    etree.SubElement(reg, "contains-null").text = "true"
    atributos = etree.SubElement(reg, "attributes")

    def atributo(tipo, nome, valor):
        etree.SubElement(atributos, "attribute", datatype=tipo, name=nome).text = valor

    for nome in CAPACIDADES_LIGADAS:
        atributo("boolean", nome, "true")
    atributo("boolean", "CAP_QUERY_BLENDING_ALWAYS_USE_LOCAL_MAPPING_TABLES", "false")
    atributo("integer", "charset", "0")
    atributo("string", "collation", '"binary"')
    atributo("string", "dialect-definition", DIALETO)
    atributo("boolean", "extract-active", "false")
    atributo("boolean", "fast-get-server-time", "true")
    return reg


def endereco_das_fontes(cfg):
    """Nome da fonte no workbook -> contentUrl da fonte publicada; todas precisam existir no projeto."""
    tb = cfg["tableau"]
    servidor = conectar_tableau(cfg)
    try:
        projeto = id_do_projeto(servidor, cfg)
        publicadas = {f.name: f.content_url for f in TSC.Pager(servidor.datasources) if f.project_id == projeto}
    finally:
        servidor.auth.sign_out()
    urls = {nome: publicadas.get(tb["prefixo"] + nome) for nome in tb["fontes"]}
    faltando = [nome for nome, url in urls.items() if not url]
    if faltando:
        raise SystemExit(f"Fontes ainda não publicadas: {faltando}")
    return urls


def ligar_fonte(ds, url, tb):
    host = tb["servidor"].removeprefix("https://")
    antiga = ds.find("connection")
    nova = etree.Element("connection", {
        "channel": "http", "class": "sqlproxy", "dbname": url, "directory": "/dataserver", "port": "80", "server": host,
        "server-oauth": "", "username": "", "workgroup-auth-mode": "prompt"})
    relacao = etree.SubElement(nova, "relation", name="sqlproxy", table="[sqlproxy]", type="table")

    mapas = []
    registros = etree.Element("metadata-records")
    for reg in antiga.find("metadata-records"):
        if reg.get("class") not in ("column", "measure"):
            continue
        remoto, local = reg.findtext("remote-name"), reg.findtext("local-name")
        if f"[{remoto}]" != local:
            mapas.append((local, remoto))
        reg.find("parent-name").text = "[sqlproxy]"
        tipo = reg.find("remote-type")
        tipo.text = REMOTE_TYPE_EXTRACAO.get(tipo.text, tipo.text)
        registros.append(reg)
    registros.append(registro_de_capacidades())
    if mapas:
        cols = etree.SubElement(nova, "cols")
        for local, remoto in mapas:
            etree.SubElement(cols, "map", key=local, value=f"[sqlproxy].[{remoto}]")
    nova.append(registros)
    nova.tail = antiga.tail
    ds.replace(antiga, nova)

    site = tb["site"]
    local_repo = etree.Element("repository-location", {
        "derived-from": f"{tb['servidor']}/t/{site}/datasources/{url}?rev=1.0", "id": url,
        "path": f"/t/{site}/datasources", "revision": "1.0", "site": site})
    local_repo.tail = ds.text
    ds.insert(0, local_repo)

    for props in ds.iterfind("object-graph/objects/object/properties"):
        r = props.find("relation")
        if r is not None:
            novo_r = etree.Element("relation", relacao.attrib)
            novo_r.tail = r.tail
            props.replace(r, novo_r)
    return [m[1] for m in mapas]


def ligar(raiz, urls, tb):
    """Troca as conexões na árvore e devolve (texto do workbook, nomes trocados)."""
    trocas = {}
    for ds in raiz.find("datasources"):
        url = urls.get(ds.get("caption"))
        if url is None:
            print(f"- mantida: {ds.get('caption')}")
            continue
        mapeadas = ligar_fonte(ds, url, tb)
        antigo = ds.get("name")
        if not antigo.startswith("sqlproxy."):  # fonte que já era publicada (de produção) mantém o nome interno
            trocas[antigo] = "sqlproxy." + antigo.removeprefix("federated.")
        print(f"+ {ds.get('caption')} -> {url}" + (f" | campos com outro nome na fonte: {mapeadas}" if mapeadas else ""))

    texto = etree.tostring(raiz, encoding="utf-8", xml_declaration=True).decode("utf-8")
    for antigo, novo in trocas.items():
        texto = texto.replace(antigo, novo)
    restantes = [a for a in trocas if a in texto]
    assert not restantes, restantes
    assert tb["databricks"]["servidor"] not in texto, "sobrou conexão com o Databricks"
    etree.fromstring(texto.encode("utf-8"), etree.XMLParser(huge_tree=True))  # continua sendo XML válido
    return texto, trocas


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    original, saida = (Path(a) for a in sys.argv[1:3])
    cfg = carregar_config()
    urls = endereco_das_fontes(cfg)
    with zipfile.ZipFile(original) as z:
        nome = next(n for n in z.namelist() if n.lower().endswith(".twb") and "/" not in n)
        raiz = etree.fromstring(z.read(nome), etree.XMLParser(huge_tree=True))
        texto, trocas = ligar(raiz, urls, cfg["tableau"])
        with zipfile.ZipFile(saida, "w", zipfile.ZIP_DEFLATED) as novo:
            novo.writestr(saida.with_suffix(".twb").name, texto.encode("utf-8"))
            for item in z.infolist():
                if item.filename != nome:
                    novo.writestr(item, z.read(item.filename))
    print(f"\n{len(trocas)} fontes ligadas ao Tableau Cloud. Gravado em {saida}")


if __name__ == "__main__":
    main()
