"""Copia um painel que lê fontes publicadas (Hispana, GovEXP) apontando para as fontes dexp - ... em vez das de produção.

O workbook já lê fontes publicadas, então a conexão continua a mesma e só muda o endereço de cada fonte que tem versão
dexp; as demais ficam na produção. O vínculo com o workbook publicado sai, para a cópia não sobrescrever o de produção.
O registro de capacidades guarda uma cópia da definição da fonte de produção; ela sai, porque o Tableau a refaz ao conectar.

Uso (a partir da pasta daily-experiencia):
  .venv\\Scripts\\python.exe ferramentas\\ligar_hispana_tableau.py <original.twbx> <saída.twbx> [fonte ...]

Com nomes de fonte, liga só essas.
"""
import sys
import zipfile
from pathlib import Path

from lxml import etree

sys.path.insert(0, str(Path(__file__).resolve().parent))
from ligar_fontes_publicadas_tableau import carregar_config, endereco_das_fontes  # noqa: E402


# Campos que na fonte dexp têm " (2)", porque a view não aceita nomes que só diferem em maiúsculas
CAMPOS_COM_SUFIXO = {"Experiencia Brasil Nivel": ["Pedido Finalizado"]}


def mapear_sufixos(ds, con):
    mapas = []
    for reg in con.find("metadata-records"):
        remoto = reg.find("remote-name")
        if reg.get("class") in ("column", "measure") and remoto.text in CAMPOS_COM_SUFIXO.get(ds.get("caption"), []):
            remoto.text += " (2)"
            reg.find("remote-alias").text = remoto.text
            mapas.append((reg.findtext("local-name"), remoto.text))
    if mapas:
        cols = etree.Element("cols")
        for local, remoto in mapas:
            etree.SubElement(cols, "map", key=local, value=f"[sqlproxy].[{remoto}]")
        con.find("metadata-records").addprevious(cols)


def apontar(ds, url, tb):
    con = ds.find("connection")
    con.set("dbname", url)
    mapear_sufixos(ds, con)
    con.attrib.pop("saved-credentials-viewerid", None)
    rl = ds.find("repository-location")
    rl.set("id", url)
    rl.set("derived-from", f"{tb['servidor']}/t/{tb['site']}/datasources/{url}?rev=1.0")
    rl.set("revision", "1.0")
    for pds in ds.iter("pds"):
        if pds.get("datasource-url"):
            pds.set("datasource-url", url)
    for atributo in con.iterfind("metadata-records/metadata-record[@class='capability']/attributes/attribute"):
        if atributo.get("name") in ("datasource", "update-time"):
            atributo.getparent().remove(atributo)


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    original, saida = (Path(a) for a in sys.argv[1:3])
    cfg = carregar_config()
    tb = cfg["tableau"]
    urls = endereco_das_fontes(cfg)
    if sys.argv[3:]:
        urls = {nome: url for nome, url in urls.items() if nome in sys.argv[3:]}
    with zipfile.ZipFile(original) as z:
        nome = next(n for n in z.namelist() if n.lower().endswith(".twb") and "/" not in n)
        raiz = etree.fromstring(z.read(nome), etree.XMLParser(huge_tree=True))
        for rl in raiz.findall("repository-location"):
            raiz.remove(rl)
        ligadas = 0
        for ds in raiz.find("datasources"):
            con = ds.find("connection")
            url = urls.get(ds.get("caption"))
            if con is None or con.get("class") != "sqlproxy" or url is None:
                print(f"- mantida: {ds.get('caption')}")
                continue
            apontar(ds, url, tb)
            ligadas += 1
            print(f"+ {ds.get('caption')} -> {url}")
        texto = etree.tostring(raiz, encoding="utf-8", xml_declaration=True)
        etree.fromstring(texto, etree.XMLParser(huge_tree=True))
        with zipfile.ZipFile(saida, "w", zipfile.ZIP_DEFLATED) as novo:
            novo.writestr(saida.with_suffix(".twb").name, texto)
            for item in z.infolist():
                if item.filename != nome:
                    novo.writestr(item, z.read(item.filename))
    print(f"\n{ligadas} fontes ligadas. Gravado em {saida}")


if __name__ == "__main__":
    main()
