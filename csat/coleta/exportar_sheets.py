"""Exporta o CSAT do Databricks para a pasta do Drive de onde o Apps Script do painel importa.

Gera, na pasta `[exportacao] pasta` de config.toml:
- csat_<operação>.csv: uma linha por enquete (dexp_gold_csat_detalhe), com as colunas da operação;
- csat_mensal.csv: indicadores por operação e mês (dexp_gold_csat_mensal);
- _ultima_exportacao.json: horário, linhas por arquivo e última data de cada operação.

Só regrava um arquivo quando o conteúdo muda, para o Drive não sincronizar à toa. Usa o perfil `daily-exp` da CLI e
refaz o login pelo navegador quando o token vence (mesma função do daily-experiencia).

Uso (a partir da pasta csat):
  ..\\daily-experiencia\\.venv\\Scripts\\python.exe coleta\\exportar_sheets.py [--aguardar-job] [--pasta <outra pasta>] [--simular]

Na rotina diária do Daily Experiência (rotina_diaria.ps1 e rotina_manual.ipynb), roda depois do job: com --aguardar-job,
espera a execução em andamento terminar antes de ler a gold.
"""
import argparse
import csv
import hashlib
import io
import json
import sys
import time
import tomllib
from datetime import datetime
from pathlib import Path

PASTA = Path(__file__).resolve().parent
DAILY = PASTA.parents[1] / "daily-experiencia"
sys.path.insert(0, str(DAILY / "coleta"))
sys.path.insert(0, str(DAILY / "src"))
from enviar_arquivos import acompanhar_job, carregar_config, cliente  # noqa: E402
from dexp.csat_saidas import SQL_DETALHE, SQL_MENSAL  # noqa: E402

COLUNAS_MENSAL = ["fonte", "mes", "enviadas", "respondidas", "sem_resposta", "promotores", "neutros", "detratores",
                  "csat", "csat_simple", "response_rate", "ces_respostas", "ces_media"]


def sql(w, cfg, consulta):
    """Linhas de uma consulta no SQL Warehouse (liga sozinho se estiver parado)."""
    r = w.statement_execution.execute_statement(statement=consulta, warehouse_id=cfg["destino"]["warehouse"],
                                                wait_timeout="50s")
    while r.status.state.value in ("PENDING", "RUNNING"):
        time.sleep(2)
        r = w.statement_execution.get_statement(r.statement_id)
    if r.status.state.value != "SUCCEEDED":
        raise RuntimeError(r.status.error.message)
    linhas = list(r.result.data_array or [])
    proximo = r.result.next_chunk_index
    while proximo:
        parte = w.statement_execution.get_statement_result_chunk_n(r.statement_id, proximo)
        linhas += parte.data_array or []
        proximo = parte.next_chunk_index
    return linhas


def origens(w, cfg):
    """Tabelas de onde ler. Antes de o job gravar as saídas novas, usa as consultas sobre dexp_gold_csat_enquetes."""
    schema = cfg["destino"]["schema"]
    catalogo, nome_schema = schema.split(".")
    existentes = {t.name for t in w.tables.list(catalogo, nome_schema) if t.name.startswith("dexp_gold_csat_")}
    enquetes = f"{schema}.dexp_gold_csat_enquetes"
    detalhe = f"{schema}.dexp_gold_csat_detalhe" if "dexp_gold_csat_detalhe" in existentes else f"({SQL_DETALHE.format(enquetes=enquetes)})"
    mensal = f"{schema}.dexp_gold_csat_mensal" if "dexp_gold_csat_mensal" in existentes else f"({SQL_MENSAL.format(enquetes=enquetes)})"
    if "dexp_gold_csat_detalhe" not in existentes or "dexp_gold_csat_mensal" not in existentes:
        print("Aviso: o job ainda não gravou dexp_gold_csat_detalhe/mensal; lendo direto de dexp_gold_csat_enquetes.")
    return detalhe, mensal


def csv_texto(colunas, linhas):
    saida = io.StringIO()
    escritor = csv.writer(saida, lineterminator="\n")
    escritor.writerow(colunas)
    escritor.writerows([["" if v is None else v for v in linha] for linha in linhas])
    return saida.getvalue()


def gravar(pasta, nome, texto, simular):
    """Grava só se mudou. Devolve 'novo', 'alterado' ou 'igual'."""
    destino = pasta / nome
    if destino.exists() and hashlib.sha256(destino.read_bytes()).digest() == hashlib.sha256(texto.encode("utf-8")).digest():
        return "igual"
    estado = "alterado" if destino.exists() else "novo"
    if not simular:
        temporario = destino.with_suffix(".tmp")
        temporario.write_text(texto, encoding="utf-8", newline="")
        temporario.replace(destino)
    return estado


def configuracao():
    with open(PASTA / "config.toml", "rb") as f:
        return tomllib.load(f)["exportacao"]


def aguardar_job(w, cfg):
    """Se o job do Daily Experiência estiver rodando, espera ele terminar. Devolve False se a última execução falhou."""
    jobs = list(w.jobs.list(name=cfg["destino"]["job"]))
    if len(jobs) != 1:
        raise RuntimeError(f"Esperava 1 job chamado {cfg['destino']['job']!r} e achei {len(jobs)}.")
    ativos = list(w.jobs.list_runs(job_id=jobs[0].job_id, active_only=True))
    if ativos:
        print("Esperando o job terminar para exportar a gold atualizada...")
        return acompanhar_job(w, ativos[0].run_id)
    ultima = next(iter(w.jobs.list_runs(job_id=jobs[0].job_id, completed_only=True, limit=1)), None)
    return ultima is None or (ultima.state.result_state is not None and ultima.state.result_state.value == "SUCCESS")


def exportar(cfg, w, pasta=None, simular=False):
    """Grava os CSV do painel. Devolve o resumo; quando nada mudou, não regrava o _ultima_exportacao.json, e o Apps Script
    não reimporta."""
    exp = configuracao()
    pasta = Path(pasta or exp["pasta"])
    if not simular:
        pasta.mkdir(parents=True, exist_ok=True)
    detalhe, mensal = origens(w, cfg)

    resumo = {"exportado_em": datetime.now().astimezone().isoformat(timespec="seconds"), "arquivos": {}}
    estados = []
    for chave, op in exp["operacoes"].items():
        colunas = exp["colunas"]["comuns"] + op["colunas"]
        anos = [l[0] for l in sql(w, cfg, f"SELECT DISTINCT left(mes, 4) FROM {detalhe} WHERE fonte = '{op['fonte']}' ORDER BY 1")]
        linhas = []
        for ano in anos:  # por ano, para cada resposta ficar abaixo do limite de 25 MB do resultado em linha
            linhas += sql(w, cfg, f"SELECT {', '.join(colunas)} FROM {detalhe} "
                                  f"WHERE fonte = '{op['fonte']}' AND left(mes, 4) = '{ano}' ORDER BY dia, protocolo")
        nome = f"csat_{chave}.csv"
        estados.append(gravar(pasta, nome, csv_texto(colunas, linhas), simular))
        ultimo_dia = max((l[colunas.index("dia")] for l in linhas if l[colunas.index("dia")]), default=None)
        resumo["arquivos"][nome] = {"fonte": op["fonte"], "linhas": len(linhas), "ultimo_dia": ultimo_dia}
        print(f"{nome:<20} {len(linhas):>7,} linhas  até {ultimo_dia}  ({estados[-1]})")

    linhas = sql(w, cfg, f"SELECT {', '.join(COLUNAS_MENSAL)} FROM {mensal} ORDER BY fonte, mes")
    estados.append(gravar(pasta, "csat_mensal.csv", csv_texto(COLUNAS_MENSAL, linhas), simular))
    resumo["arquivos"]["csat_mensal.csv"] = {"linhas": len(linhas)}
    print(f"{'csat_mensal.csv':<20} {len(linhas):>7,} linhas  ({estados[-1]})")

    if simular:
        print("Simulação: nada gravado.")
    elif all(e == "igual" for e in estados) and (pasta / "_ultima_exportacao.json").exists():
        print(f"Nada mudou desde a última exportação ({pasta}).")
    else:
        (pasta / "_ultima_exportacao.json").write_text(json.dumps(resumo, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"Gravado em {pasta}")
    return resumo


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser(description="Exporta o CSAT do Databricks para a pasta do Drive do painel.")
    ap.add_argument("--pasta", help="grava em outra pasta (para testar sem mexer no Drive)")
    ap.add_argument("--simular", action="store_true", help="consulta tudo, mas não grava nada")
    ap.add_argument("--aguardar-job", action="store_true",
                    help="se o job do Daily Experiência estiver rodando, espera ele terminar antes de exportar")
    args = ap.parse_args()

    cfg = carregar_config(DAILY / "coleta" / "fontes.toml")
    w = cliente(cfg)
    if args.aguardar_job and not aguardar_job(w, cfg):
        print("⚠️ A última execução do job não terminou com sucesso: a gold pode estar desatualizada. Exportando assim mesmo.")
    exportar(cfg, w, args.pasta, args.simular)


if __name__ == "__main__":
    main()
