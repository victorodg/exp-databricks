"""Consultas ao SQL Warehouse do Databricks pela CLI (perfil e warehouse do projeto daily-experiencia)."""
import glob
import json
import os
import subprocess

PERFIL = "daily-exp"
WAREHOUSE = "dcb43c45e3a55fe4"
SCHEMA = "sandbox.sustentacao_bau_experiencias"


def _cli():
    achados = glob.glob(os.path.expandvars(r"%LOCALAPPDATA%\Microsoft\WinGet\Packages\Databricks*\databricks.exe"))
    if not achados:
        raise RuntimeError("CLI do Databricks não encontrada (instalada pelo WinGet).")
    return achados[0]


def consultar(sql):
    """Roda um SELECT e devolve uma lista de dicionários (coluna -> valor em texto)."""
    corpo = json.dumps({"warehouse_id": WAREHOUSE, "statement": sql, "wait_timeout": "50s",
                        "format": "JSON_ARRAY", "disposition": "INLINE"})
    saida = subprocess.run([_cli(), "api", "post", "/api/2.0/sql/statements", "--json", corpo, "-p", PERFIL],
                           capture_output=True, text=True, encoding="utf-8")
    if saida.returncode:
        raise RuntimeError(saida.stderr)
    r = json.loads(saida.stdout)
    if r["status"]["state"] != "SUCCEEDED":
        raise RuntimeError(f"{r['status']['state']}: {r['status'].get('error', {}).get('message', '')}\n{sql}")
    colunas = [c["name"] for c in r["manifest"]["schema"]["columns"]]
    return [dict(zip(colunas, linha)) for linha in r.get("result", {}).get("data_array", [])]


def tabela(nome):
    return f"{SCHEMA}.{nome}"
