"""Publica no Tableau Cloud as fontes de dados do workbook, como extrações das views do Databricks.

Roda todo dia depois do job (última célula do rotina_manual.ipynb ou fim do rotina_diaria.ps1). Para cada fonte em
[tableau.fontes] de fontes.toml, lê a view no SQL Warehouse, grava a extração e a definição da fonte num .tdsx (textos
com a collation do Prep) e publica com o token do Databricks embutido na conexão. As fontes não têm atualização
agendada no Tableau Cloud: ela gravaria os textos com collation "binary" (ver remover_agenda).

Nada de segredo em arquivo: os dois tokens ficam no cofre de credenciais do Windows.
  .venv\\Scripts\\python.exe coleta\\publicar_tableau.py --guardar-tokens

Uso, a partir da pasta daily-experiencia:
  .venv\\Scripts\\python.exe coleta\\publicar_tableau.py --sem-publicar               só gera e confere as linhas
  .venv\\Scripts\\python.exe coleta\\publicar_tableau.py --somente "HC Exp Brasil"    publica só as fontes citadas
  .venv\\Scripts\\python.exe coleta\\publicar_tableau.py                              publica todas
"""
import argparse
import getpass
import io
import re
import sys
import tempfile
import time
import urllib.request
import uuid
import zipfile
from datetime import datetime
from pathlib import Path

import keyring
import pyarrow as pa
import tableauserverclient as TSC
from databricks.sdk.service.sql import Disposition, Format, StatementState
from lxml import etree
from tableauhyperapi import (Connection, CreateMode, HyperProcess, Inserter, Nullability, SqlType, TableDefinition,
                             TableName, Telemetry)

from enviar_arquivos import carregar_config, cliente

SERVICO_COFRE = "dexp-tableau"
COFRE_DATABRICKS = "token-databricks"
# Nome do objeto lógico das fontes de produção. O workbook conta registros e ordena planilhas por
# [__tableau_internal_object_id__].[Migrated Data]; com outro nome, as consultas falham e o Tableau pede para reconectar.
OBJETO = "Migrated Data"

# tipo no Arrow -> (tipo no Hyper, remote-type ao vivo, remote-type na extração, local-type, agregação)
TEXTO = (SqlType.text(), "129", "129", "string", "Count")
INTEIRO = (SqlType.big_int(), "20", "20", "integer", "Sum")
REAL = (SqlType.double(), "5", "5", "real", "Sum")
DATA = (SqlType.date(), "7", "133", "date", "Year")
DATA_HORA = (SqlType.timestamp(), "135", "135", "datetime", "Year")
BOOLEANO = (SqlType.bool(), "11", "11", "boolean", "Count")

# Collation dos textos, a mesma das extrações que o Prep grava: português do Brasil sem diferenciar maiúsculas.
# Com "binary", filtros e grupos do workbook que guardam o nome com outra grafia ("Gabrielle Tenorio" × "Gabrielle
# tenorio") deixam de achar o valor, e a ordem alfabética põe os acentos no fim.
COLLATION_HYPER = "pt_BR_CI"
COLLATION_TABLEAU = "LPT_RBR_S2"


def tipos(tipo):
    if pa.types.is_string(tipo) or pa.types.is_large_string(tipo) or pa.types.is_null(tipo):
        return TEXTO
    if pa.types.is_integer(tipo):
        return INTEIRO
    if pa.types.is_floating(tipo) or pa.types.is_decimal(tipo):
        return REAL
    if pa.types.is_date(tipo):
        return DATA
    if pa.types.is_timestamp(tipo):
        return DATA_HORA
    if pa.types.is_boolean(tipo):
        return BOOLEANO
    raise ValueError(f"tipo sem correspondência no Hyper: {tipo}")


# --- leitura e extração ----------------------------------------------------------------------------------------

def blocos_da_view(w, cfg, view):
    """Lê a view em Arrow; devolve o total de linhas informado pelo Warehouse e os blocos de registros."""
    r = w.statement_execution.execute_statement(
        statement=f"SELECT * FROM {cfg['destino']['schema']}.{view}", warehouse_id=cfg["destino"]["warehouse"],
        format=Format.ARROW_STREAM, disposition=Disposition.EXTERNAL_LINKS, wait_timeout="50s")
    while r.status.state in (StatementState.PENDING, StatementState.RUNNING):
        time.sleep(3)
        r = w.statement_execution.get_statement(r.statement_id)
    if r.status.state != StatementState.SUCCEEDED:
        raise RuntimeError(f"{view}: {r.status.error.message if r.status.error else r.status.state}")

    def blocos():
        for i in range(r.manifest.total_chunk_count or 0):
            pedaco = w.statement_execution.get_statement_result_chunk_n(r.statement_id, i)
            for link in pedaco.external_links or []:
                with urllib.request.urlopen(link.external_link, timeout=300) as c:
                    yield from pa.ipc.open_stream(io.BytesIO(c.read()))

    return r.manifest.total_row_count, blocos()


def linhas_do_bloco(bloco):
    colunas = []
    for coluna in bloco.columns:
        valores = coluna.to_pylist()
        if pa.types.is_timestamp(coluna.type):  # o Hyper não guarda fuso; a gold é gravada em UTC
            valores = [None if v is None else v.replace(tzinfo=None) for v in valores]
        colunas.append(valores)
    return zip(*colunas)


def gerar_hyper(w, cfg, hyper, view, caminho):
    """Grava a extração com os nomes da view, os mesmos que a atualização no Tableau Cloud vai gravar depois."""
    total, blocos = blocos_da_view(w, cfg, view)
    inseridas, esquema, tabela = 0, None, None
    with Connection(hyper.endpoint, str(caminho), CreateMode.CREATE_AND_REPLACE) as con:
        con.catalog.create_schema("Extract")
        for bloco in blocos:
            if tabela is None:
                esquema = bloco.schema
                tabela = TableDefinition(TableName("Extract", "Extract"), [
                    TableDefinition.Column(c.name, tipos(c.type)[0], Nullability.NULLABLE,
                                           COLLATION_HYPER if tipos(c.type) is TEXTO else None) for c in esquema])
                con.catalog.create_table(tabela)
            with Inserter(con, tabela) as ins:
                ins.add_rows(linhas_do_bloco(bloco))
                ins.execute()
            inseridas += bloco.num_rows
    if tabela is None or inseridas != total:
        raise RuntimeError(f"{view}: {inseridas} linhas gravadas de {total}")
    return inseridas, esquema


# --- definição da fonte (.tds) -----------------------------------------------------------------------------------

def registro(pai, coluna, ordinal, objeto, extracao, view=None):
    _, ao_vivo, na_extracao, local, agregacao = tipos(coluna.type)
    r = etree.Element("metadata-record", {"class": "column"})
    campos = [("remote-name", coluna.name), ("remote-type", na_extracao if extracao else ao_vivo),
              ("local-name", f"[{coluna.name}]"), ("parent-name", f"[{pai}]"), ("remote-alias", coluna.name),
              ("ordinal", str(ordinal))]
    if extracao:
        campos.append(("family", view))
    campos += [("local-type", local), ("aggregation", agregacao), ("contains-null", "true")]
    for tag, valor in campos:
        etree.SubElement(r, tag).text = valor
    if local == "string":
        etree.SubElement(r, "collation", flag="1", name=COLLATION_TABLEAU)
    etree.SubElement(r, "object-id").text = f"[{objeto}]"
    return r


def definicao_da_fonte(cfg, nome, view, esquema, arquivo_hyper):
    """O mesmo formato de uma fonte publicada pelo Tableau Desktop: conexão por token e extração em Extract.Extract."""
    d = cfg["tableau"]["databricks"]
    catalogo, schema = cfg["destino"]["schema"].split(".")
    ligacao = "databricks." + uuid.uuid4().hex[:28]
    objeto = OBJETO
    relacao = dict(connection=ligacao, name=view, table=f"[{catalogo}].[{schema}].[{view}]", type="table")

    fonte = etree.Element("datasource", {"formatted-name": nome, "inline": "true", "source-platform": "win",
                                         "version": "18.1"})
    manifesto = etree.SubElement(fonte, "document-format-change-manifest")
    for item in ("DatabricksCatalog", "ObjectModelEncapsulateLegacy", "ObjectModelExtractV2", "ObjectModelTableType",
                 "SchemaViewerObjectModel"):
        etree.SubElement(manifesto, item)
    con = etree.SubElement(fonte, "connection", {"class": "federated"})
    nomeadas = etree.SubElement(con, "named-connections")
    nomeada = etree.SubElement(nomeadas, "named-connection", caption=d["servidor"], name=ligacao)
    etree.SubElement(nomeada, "connection", {
        "authentication": "auth-pass", "authentication-type": "", "class": "databricks", "dbname": catalogo,
        "odbc-connect-string-extras": "", "one-time-sql": "", "schema": schema, "server": d["servidor"],
        "server-oauth": "", "username": "token", "usesPrivateConnect": "", "v-auth-scope": "",
        "v-http-path": d["caminho_http"], "v-oidc-discovery-endpoint": "", "v-query-tags": "",
        "workgroup-auth-mode": "prompt"})
    etree.SubElement(con, "relation", relacao)
    registros = etree.SubElement(con, "metadata-records")
    for i, coluna in enumerate(esquema):
        registros.append(registro(view, coluna, i + 1, objeto, False))
    etree.SubElement(fonte, "aliases", enabled="yes")
    etree.SubElement(fonte, "column", {"caption": objeto, "datatype": "table", "role": "measure", "type": "quantitative",
                                       "name": f"[__tableau_internal_object_id__].[{objeto}]"})
    extracao = etree.SubElement(fonte, "extract", {"count": "-1", "enabled": "true", "object-id": "",
                                                   "units": "records", "user-specific": "false"})
    con_extracao = etree.SubElement(extracao, "connection", {
        "authentication": "auth-none", "author-locale": "en_US", "class": "hyper", "dbname": arquivo_hyper,
        "schema": "Extract", "tablename": "Extract",
        "update-time": datetime.now().strftime("%m/%d/%Y %I:%M:%S %p")})
    etree.SubElement(con_extracao, "relation", name="Extract", table="[Extract].[Extract]", type="table")
    registros = etree.SubElement(con_extracao, "metadata-records")
    for i, coluna in enumerate(esquema):
        registros.append(registro("Extract", coluna, i, objeto, True, view))
    etree.SubElement(fonte, "layout", {"dim-ordering": "alphabetic", "measure-ordering": "alphabetic",
                                       "show-structure": "true"})
    grafo = etree.SubElement(etree.SubElement(fonte, "object-graph"), "objects")
    obj = etree.SubElement(grafo, "object", caption=objeto, id=objeto)
    etree.SubElement(etree.SubElement(obj, "properties", context=""), "relation", relacao)
    etree.SubElement(etree.SubElement(obj, "properties", context="extract"), "relation", name="Extract",
                     table="[Extract].[Extract]", type="table")
    return etree.tostring(fonte, xml_declaration=True, encoding="utf-8", pretty_print=True)


def gerar_tdsx(w, cfg, hyper, nome, view, pasta):
    base = re.sub(r"\W+", "_", view)
    caminho_hyper = Path(pasta) / f"{base}.hyper"
    linhas, esquema = gerar_hyper(w, cfg, hyper, view, caminho_hyper)
    interno = f"Data/Extracts/{base}.hyper"
    caminho = Path(pasta) / f"{base}.tdsx"
    with zipfile.ZipFile(caminho, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr(f"{base}.tds", definicao_da_fonte(cfg, nome, view, esquema, interno))
        z.write(caminho_hyper, interno)
    caminho_hyper.unlink()
    return caminho, linhas


# --- Tableau Cloud ---------------------------------------------------------------------------------------------

def conectar_tableau(cfg):
    tb = cfg["tableau"]
    segredo = keyring.get_password(SERVICO_COFRE, tb["token_nome"])
    if not segredo:
        raise RuntimeError("Token do Tableau não encontrado. Rode: python coleta\\publicar_tableau.py --guardar-tokens")
    servidor = TSC.Server(tb["servidor"], use_server_version=True)
    servidor.auth.sign_in(TSC.PersonalAccessTokenAuth(tb["token_nome"], segredo, site_id=tb["site"]))
    return servidor


def id_do_projeto(servidor, cfg):
    """O projeto é o da fonte de referência: há vários projetos com o mesmo nome em pastas diferentes."""
    filtro = TSC.RequestOptions()
    filtro.filter.add(TSC.Filter(TSC.RequestOptions.Field.Name, TSC.RequestOptions.Operator.Equals,
                                 cfg["tableau"]["fonte_referencia"]))
    achadas = list(TSC.Pager(servidor.datasources, filtro))
    if len(achadas) != 1:
        raise RuntimeError(f"Fonte de referência {cfg['tableau']['fonte_referencia']!r}: {len(achadas)} encontradas.")
    if achadas[0].project_name != cfg["tableau"]["projeto"]:
        raise RuntimeError(f"A fonte de referência está em {achadas[0].project_name!r}, não em {cfg['tableau']['projeto']!r}.")
    return achadas[0].project_id


def remover_agenda(servidor, fonte_id):
    """Apaga a atualização agendada da fonte, se houver. A fonte passa a ser atualizada só pela publicação diária
    (última célula do rotina_manual.ipynb ou fim do rotina_diaria.ps1).

    Motivo: a atualização do Tableau Cloud relê o Databricks e grava os textos com collation "binary", desfazendo a
    collation do Prep gravada aqui (testado em 12/11/2026). Além disso, o job só roda quando a rotina roda, então a
    atualização agendada não trazia dado novo."""
    removidas = 0
    for tarefa in TSC.Pager(servidor.tasks):
        if tarefa.target is not None and tarefa.target.id == fonte_id:
            servidor.tasks.delete(tarefa.id)
            removidas += 1
    return "atualização agendada removida" if removidas else "sem atualização agendada"


def sessao_caiu(erro):
    """O Tableau Cloud derruba a sessão quando o mesmo token pessoal entra de novo em outro lugar (outro script, a
    renovação do token, uma consulta feita à parte): a partir daí toda chamada volta 401002."""
    return type(erro).__name__ in ("FailedSignInError", "NotSignedInError") or "401002" in str(erro)


def publicar(cfg, w=None, somente=None, sem_publicar=False):
    """Uma falha numa fonte não para as demais. Devolve uma lista de (fonte, linhas, segundos, situação, erro)."""
    w = w or cliente(cfg)
    fontes = {n: v for n, v in cfg["tableau"]["fontes"].items() if not somente or n in somente}
    if somente and len(fontes) != len(somente):
        raise SystemExit(f"Fontes desconhecidas: {sorted(set(somente) - set(fontes))}")
    servidor = projeto = credencial = None
    if not sem_publicar:
        token = keyring.get_password(SERVICO_COFRE, COFRE_DATABRICKS)
        if not token:
            raise RuntimeError("Token do Databricks não encontrado. Rode: python coleta\\publicar_tableau.py --guardar-tokens")
        credencial = TSC.ConnectionCredentials("token", token, embed=True)
        servidor = conectar_tableau(cfg)
        projeto = id_do_projeto(servidor, cfg)
    resultados = []
    try:
        with tempfile.TemporaryDirectory() as pasta, HyperProcess(
                Telemetry.DO_NOT_SEND_USAGE_DATA_TO_TABLEAU, parameters={"log_dir": pasta}) as hyper:
            for nome, view in fontes.items():
                inicio = time.time()
                linhas, situacao, erro = None, "gerada", None
                try:
                    caminho, linhas = gerar_tdsx(w, cfg, hyper, nome, view, pasta)
                    if not sem_publicar:
                        for tentativa in (1, 2):
                            try:
                                item = TSC.DatasourceItem(projeto, name=cfg["tableau"]["prefixo"] + nome)
                                item = servidor.datasources.publish(item, str(caminho), TSC.Server.PublishMode.Overwrite,
                                                                    connection_credentials=credencial)
                                situacao = f"publicada, {remover_agenda(servidor, item.id)}"
                                break
                            except Exception as e:
                                if tentativa == 2 or not sessao_caiu(e):
                                    raise
                                print(f"{nome}: a sessão do Tableau caiu (o token foi usado em outro lugar); "
                                      "entrando de novo...", flush=True)
                                servidor = conectar_tableau(cfg)
                    caminho.unlink()
                except Exception as e:
                    erro = f"{type(e).__name__}: {e}"
                resultados.append((nome, linhas, round(time.time() - inicio), situacao, erro))
                texto = f"❌ {erro}" if erro else f"✅ {situacao}"
                print(f"{nome}: {linhas if linhas is None else f'{linhas:,}'} linhas, {resultados[-1][2]}s {texto}", flush=True)
    finally:
        if servidor:
            try:
                servidor.auth.sign_out()
            except Exception:  # noqa: BLE001 - a sessão pode já ter caído
                pass
    return resultados


def guardar_tokens(cfg):
    tb = cfg["tableau"]
    for rotulo, chave in [(f"token do Tableau Cloud ({tb['token_nome']})", tb["token_nome"]),
                          ("token do Databricks", COFRE_DATABRICKS)]:
        segredo = getpass.getpass(f"Cole o {rotulo} (não aparece na tela) e tecle Enter: ").strip()
        if not segredo:
            raise SystemExit("Nada foi guardado.")
        keyring.set_password(SERVICO_COFRE, chave, segredo)
    servidor = conectar_tableau(cfg)
    try:
        print(f"✅ Tokens guardados. O Tableau Cloud aceitou o token (site {tb['site']}).")
        print(f"✅ Projeto {tb['projeto']!r} encontrado: {id_do_projeto(servidor, cfg)}")
    finally:
        servidor.auth.sign_out()


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    p = argparse.ArgumentParser(description="Cria as fontes do workbook no Tableau Cloud")
    p.add_argument("--guardar-tokens", action="store_true", help="guarda os dois tokens no cofre do Windows")
    p.add_argument("--somente", nargs="+", help="nomes das fontes a publicar")
    p.add_argument("--sem-publicar", action="store_true", help="só gera as extrações e confere as linhas")
    a = p.parse_args()
    cfg = carregar_config()
    if a.guardar_tokens:
        guardar_tokens(cfg)
        return
    resultados = publicar(cfg, somente=a.somente, sem_publicar=a.sem_publicar)
    erros = [r for r in resultados if r[4]]
    print(f"\n{len(resultados) - len(erros)} de {len(resultados)} fontes {'geradas' if a.sem_publicar else 'publicadas'}.")
    if erros:
        sys.exit(1)


if __name__ == "__main__":
    main()
