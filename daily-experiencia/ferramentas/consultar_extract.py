"""Roda uma consulta SQL no extract do Tableau (Hyper) e outra na gold (Databricks) e mostra lado a lado.

Uso: python ferramentas\\consultar_extract.py <arquivo.tdsx> "<SQL no extract>" "<SQL na gold>"
No SQL do extract, a tabela é {t} e as colunas vão entre aspas duplas ("Tipo Protocolo").
No SQL da gold, use {g} para o esquema (ex.: {g}.dexp_gold_dynamics_tarefas).
"""
import sys
import tempfile
from pathlib import Path

from tableauhyperapi import Connection, HyperProcess, Telemetry

sys.path.insert(0, str(Path(__file__).resolve().parent))
from comparar_extract import ESQUEMA, arquivo_hyper, cliente, sql_databricks, texto  # noqa: E402


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    origem, sql_ext, sql_gold = Path(sys.argv[1]), sys.argv[2], sys.argv[3]
    with tempfile.TemporaryDirectory() as pasta, HyperProcess(Telemetry.DO_NOT_SEND_USAGE_DATA_TO_TABLEAU) as hyper:
        with Connection(hyper.endpoint, str(arquivo_hyper(origem, pasta))) as con:
            ext = con.execute_list_query(sql_ext.format(t='"Extract"."Extract"'))
    gold = sql_databricks(cliente(), sql_gold.format(g=ESQUEMA))
    chave = lambda linha: tuple((texto(v) or "").lower() for v in linha[:-1])
    a = {chave(l): int(l[-1]) for l in ext}
    b = {chave(l): int(l[-1]) for l in gold}
    print("| chave | extract | gold | diferença |\n|---|---|---|---|")
    for k in sorted(set(a) | set(b)):
        marca = "" if a.get(k, 0) == b.get(k, 0) else " ⚠️"
        print(f"| {' · '.join(k)}{marca} | {a.get(k, 0):,} | {b.get(k, 0):,} | {b.get(k, 0) - a.get(k, 0):+,} |")


if __name__ == "__main__":
    main()
