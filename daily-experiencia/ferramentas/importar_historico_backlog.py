"""Carga única: copia o histórico do extract "Histórico Backlog Diário" do Tableau para o volume dexp_landing.

No Tableau esse extract é acumulado (cada execução do fluxo acrescenta uma linha), então o histórico só existe lá.
A gold do MKT lê o CSV gerado aqui na primeira vez que cria a tabela dexp_gold_mkt_historico_backlog_diario.
Uso: .venv\\Scripts\\python.exe ferramentas\\importar_historico_backlog.py "validacao\\extracts\\Histórico Backlog Diário.tdsx"
"""
import csv
import io
import sys
import tempfile
from pathlib import Path

from tableauhyperapi import Connection, HyperProcess, Telemetry

sys.path.insert(0, str(Path(__file__).resolve().parent))
from comparar_extract import arquivo_hyper, cliente  # noqa: E402

DESTINO = "/Volumes/sandbox/sustentacao_bau_experiencias/dexp_landing/historico/historico_backlog_diario_tableau.csv"


def main():
    with tempfile.TemporaryDirectory() as pasta, HyperProcess(Telemetry.DO_NOT_SEND_USAGE_DATA_TO_TABLEAU) as hyper:
        with Connection(hyper.endpoint, str(arquivo_hyper(Path(sys.argv[1]), pasta))) as con:
            linhas = con.execute_list_query(
                'SELECT "Data Hoje", "Protocol", "Carimbo Tempo" FROM "Extract"."Extract" ORDER BY "Carimbo Tempo"')
    saida = io.StringIO()
    escritor = csv.writer(saida)
    escritor.writerow(["data_hoje", "protocol", "carimbo_tempo"])
    for data, protocolos, carimbo in linhas:
        escritor.writerow([str(data), protocolos, str(carimbo)])
    cliente().files.upload(DESTINO, io.BytesIO(saida.getvalue().encode("utf-8")), overwrite=True)
    print(f"{len(linhas)} linhas enviadas para {DESTINO}")


if __name__ == "__main__":
    main()
