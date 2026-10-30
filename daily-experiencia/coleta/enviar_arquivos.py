"""Envia os arquivos de entrada do Daily Experiência BR para o volume dexp_landing no Databricks.

Fontes (configuradas em fontes.toml):
  - mktzap:        brutos baixados pelo Selenium (logic-local\\mktzap\\downloads_brutos\\<AAAAMM>\\<operação>\\)
  - drive:         planilhas .xlsx do Drive compartilhado
  - google_sheets: cópias .xlsx das Google Sheets geradas pelo Apps Script (google_sheets/exportar_planilhas.gs)

Destino no volume:
  mktzap/<operação>/<AAAAMM>/<arquivo>
  drive/<fonte>/<AAAA-MM-DD>/<arquivo>            (AAAA-MM-DD = dia em que esta versão foi capturada)
  google_sheets/<fonte>/<AAAA-MM-DD>/<arquivo>
A data é a da captura, e não a de alteração do arquivo, porque o Google Drive para desktop
reescreve a data de alteração toda vez que baixa o arquivo para leitura.

Arquivos iguais aos do último envio são pulados (comparação por SHA-256, guardada em .estado/manifesto.json).
Nada é apagado, nem no volume nem na origem. No fim, se nenhum envio deu erro, dispara o job do Databricks
(destino.job em fontes.toml), que processa o volume da bronze até a gold.

Uso (a partir da pasta daily-experiencia):
  .venv\\Scripts\\python.exe coleta\\enviar_arquivos.py                       # envia tudo e dispara o job
  .venv\\Scripts\\python.exe coleta\\enviar_arquivos.py --aguardar            # idem, esperando o job terminar
  .venv\\Scripts\\python.exe coleta\\enviar_arquivos.py --sem-job             # só envia
  .venv\\Scripts\\python.exe coleta\\enviar_arquivos.py --simular             # só mostra o que seria enviado
  .venv\\Scripts\\python.exe coleta\\enviar_arquivos.py --somente mktzap drive
"""
import argparse
import glob
import hashlib
import json
import os
import shutil
import sys
import time
import tomllib
from dataclasses import dataclass
from datetime import date, datetime, timedelta
from pathlib import Path

from databricks.sdk import WorkspaceClient
from databricks.sdk.core import Config

PASTA = Path(__file__).resolve().parent
ARQUIVO_MANIFESTO = PASTA / ".estado" / "manifesto.json"
GRUPOS = ("mktzap", "drive", "google_sheets")


@dataclass
class Envio:
    chave: str           # identifica a fonte no manifesto
    origem: Path
    destino: str | None  # caminho relativo dentro do volume (None se a origem não existe)


def caminho_cli():
    """Caminho da CLI do Databricks, que o SDK usa para o login OAuth do perfil."""
    achado = shutil.which("databricks")
    if achado:
        return achado
    candidatos = glob.glob(os.path.expandvars(
        r"%LOCALAPPDATA%\Microsoft\WinGet\Packages\Databricks.DatabricksCLI_*\databricks.exe"))
    if not candidatos:
        sys.exit("CLI do Databricks não encontrada. Instale com: winget install --id Databricks.DatabricksCLI -e --source winget")
    return candidatos[0]


def sha256(caminho):
    h = hashlib.sha256()
    with open(caminho, "rb") as f:
        for bloco in iter(lambda: f.read(1024 * 1024), b""):
            h.update(bloco)
    return h.hexdigest()


def envio_versionado(grupo, fonte, arquivo):
    """Planilhas que são sobrescritas na origem: cada versão nova vai para uma pasta com a data da captura."""
    destino = None
    if arquivo.exists():
        destino = f"{grupo}/{fonte}/{date.today():%Y-%m-%d}/{arquivo.name}"
    return Envio(f"{grupo}/{fonte}", arquivo, destino)


def envios_mktzap(cfg):
    """Cada execução do Selenium gera um arquivo novo (bruto_<relatório>_<de>_a_<até>.csv), então sobe com o mesmo nome."""
    raiz = Path(cfg["origens"]["mktzap"])
    envios = []
    for pasta_operacao, operacao in cfg["mktzap"]["operacoes"].items():
        for arquivo in sorted(raiz.glob(f"*/{pasta_operacao}/bruto_*.csv")):
            mes = arquivo.parent.parent.name
            destino = f"mktzap/{operacao}/{mes}/{arquivo.name}"
            envios.append(Envio(destino, arquivo, destino))
    return envios


def envios_drive(cfg):
    raiz = Path(cfg["origens"]["drive"])
    return [envio_versionado("drive", fonte, raiz / relativo) for fonte, relativo in cfg["drive"].items()]


def envios_google_sheets(cfg):
    raiz = Path(cfg["origens"]["google_sheets"])
    return [envio_versionado("google_sheets", fonte, raiz / f"{fonte}.xlsx")
            for fonte in cfg["google_sheets"]["arquivos"]]


GERADORES = {"mktzap": envios_mktzap, "drive": envios_drive, "google_sheets": envios_google_sheets}


def salvar_manifesto(manifesto):
    ARQUIVO_MANIFESTO.parent.mkdir(parents=True, exist_ok=True)
    temporario = ARQUIVO_MANIFESTO.with_suffix(".tmp")
    temporario.write_text(json.dumps(manifesto, ensure_ascii=False, indent=2), encoding="utf-8")
    temporario.replace(ARQUIVO_MANIFESTO)


def carregar_config(caminho=PASTA / "fontes.toml"):
    with open(caminho, "rb") as f:
        return tomllib.load(f)


def cliente(cfg):
    return WorkspaceClient(config=Config(profile=cfg["destino"]["perfil"], databricks_cli_path=caminho_cli()))


def verificar_google_sheets(cfg):
    """Diz se a exportação de hoje das Google Sheets já terminou, pelo _ultima_exportacao.json que o Apps Script grava.
    Devolve (pronta, mensagem)."""
    pasta = Path(cfg["origens"]["google_sheets"])
    status_arquivo = pasta / "_ultima_exportacao.json"
    faltando = [f for f in cfg["google_sheets"]["arquivos"] if not (pasta / f"{f}.xlsx").exists()]
    if not status_arquivo.exists():
        return False, f"⏳ Ainda não há {status_arquivo.name} em {pasta} (o Apps Script grava esse arquivo a cada exportação)."
    status = json.loads(status_arquivo.read_text(encoding="utf-8"))
    quando = status.get("exportado_em", "")
    if not quando.startswith(f"{date.today():%Y-%m-%d}"):
        return False, f"⏳ A última exportação foi em {quando}; a de hoje ainda não chegou ao Drive."
    if status.get("falhas"):
        return False, f"❌ A exportação de hoje ({quando}) teve falhas: {status['falhas']}"
    if faltando:
        return False, f"⏳ Exportação de hoje feita às {quando[11:16]}, mas o Drive ainda não sincronizou: {faltando}"
    return True, f"✅ Google Sheets exportadas hoje às {quando[11:16]} ({len(status.get('exportadas', []))} planilhas)."


def enviar(cfg, w=None, grupos=GRUPOS, simular=False, forcar=False):
    """Envia ao volume os arquivos novos ou alterados. Devolve a lista de (chave, situação, detalhe)."""
    volume = cfg["destino"]["volume"].rstrip("/")
    manifesto = json.loads(ARQUIVO_MANIFESTO.read_text("utf-8")) if ARQUIVO_MANIFESTO.exists() else {}
    resultados = []
    for grupo in grupos:
        for envio in GERADORES[grupo](cfg):
            if envio.destino is None:
                resultados.append((envio.chave, "ausente", str(envio.origem)))
                continue
            try:
                hash_atual = sha256(envio.origem)
                anterior = manifesto.get(envio.chave)
                if anterior and anterior["sha256"] == hash_atual and not forcar:
                    resultados.append((envio.chave, "sem mudança", anterior["destino"]))
                    continue
                remoto = f"{volume}/{envio.destino}"
                if simular:
                    resultados.append((envio.chave, "a enviar", f"{envio.destino} ({envio.origem.stat().st_size / 1024:,.0f} KB)"))
                    continue
                with open(envio.origem, "rb") as f:
                    w.files.upload(remoto, f, overwrite=True)
                tamanho_remoto = int(w.files.get_metadata(remoto).content_length)
                if tamanho_remoto != envio.origem.stat().st_size:
                    raise RuntimeError(f"tamanho no volume ({tamanho_remoto}) diferente do local ({envio.origem.stat().st_size})")
                manifesto[envio.chave] = {"sha256": hash_atual, "destino": envio.destino,
                                          "enviado_em": datetime.now().isoformat(timespec="seconds")}
                salvar_manifesto(manifesto)  # a cada arquivo: uma falha no meio não perde o que já subiu
                resultados.append((envio.chave, "enviado", f"{envio.destino} ({tamanho_remoto / 1024:,.0f} KB)"))
            except Exception as e:
                resultados.append((envio.chave, "erro", f"{type(e).__name__}: {e}"))
    return resultados


ICONES = {"enviado": "✅", "a enviar": "📤", "sem mudança": "➖", "ausente": "⚠️", "erro": "❌"}


def imprimir_resultados(cfg, resultados):
    """Mostra o que mudou e devolve a contagem por situação."""
    print(f"Volume: {cfg['destino']['volume']}" + chr(10))
    for chave, situacao, detalhe in resultados:
        if situacao != "sem mudança":
            print(f"{ICONES[situacao]} {situacao:11} {detalhe}" if detalhe.startswith(chave)
                  else f"{ICONES[situacao]} {situacao:11} {chave}: {detalhe}")
    contagem = {s: sum(1 for r in resultados if r[1] == s) for s in ICONES}
    print(chr(10) + "Resumo: " + " | ".join(f"{s}: {n}" for s, n in contagem.items() if n))
    if contagem["ausente"]:
        print("⚠️ Arquivos ausentes não foram enviados: confira o caminho em fontes.toml ou se a exportação rodou.")
    return contagem


def disparar_job(w, nome_job):
    """Dispara o job que processa o volume (bronze -> silver -> gold) e devolve o id da execução."""
    jobs = list(w.jobs.list(name=nome_job))
    if len(jobs) != 1:
        raise RuntimeError(f"Esperava 1 job chamado {nome_job!r} e achei {len(jobs)}: confira destino.job em fontes.toml.")
    execucao = w.jobs.run_now(jobs[0].job_id)
    print(f"🚀 Job disparado: {w.jobs.get_run(execucao.run_id).run_page_url}")
    return execucao.run_id


def acompanhar_job(w, run_id, intervalo=30):
    """Mostra o andamento de cada tarefa do job até ele terminar. Devolve True se terminou com sucesso."""
    ultimo = None
    while True:
        execucao = w.jobs.get_run(run_id)
        tarefas = " | ".join(f"{t.task_key}: {(t.state.result_state or t.state.life_cycle_state).value}" for t in execucao.tasks or [])
        if tarefas != ultimo:
            print(f"{datetime.now():%H:%M:%S}  {tarefas}")
            ultimo = tarefas
        if execucao.state.life_cycle_state.value in ("TERMINATED", "SKIPPED", "INTERNAL_ERROR"):
            resultado = execucao.state.result_state.value if execucao.state.result_state else execucao.state.life_cycle_state.value
            print(f"{'✅' if resultado == 'SUCCESS' else '❌'} Job terminou: {resultado}  {execucao.run_page_url}")
            return resultado == "SUCCESS"
        time.sleep(intervalo)


def conferir_gold(w, cfg):
    """[(tabela, linhas, última gravação)] das tabelas dexp_gold_*, pelo SQL Warehouse (liga sozinho se estiver parado)."""
    catalogo, schema = cfg["destino"]["schema"].split(".")

    def sql(consulta):
        r = w.statement_execution.execute_statement(statement=consulta, warehouse_id=cfg["destino"]["warehouse"],
                                                    wait_timeout="50s")
        while r.status.state.value in ("PENDING", "RUNNING"):
            time.sleep(2)
            r = w.statement_execution.get_statement(r.statement_id)
        if r.status.state.value != "SUCCEEDED":
            raise RuntimeError(r.status.error.message)
        return r.result.data_array or []

    tabelas = sorted(t.name for t in w.tables.list(catalogo, schema) if t.name.startswith("dexp_gold_"))
    linhas = dict(sql(" UNION ALL ".join(f"SELECT '{t}', count(*) FROM {catalogo}.{schema}.{t}" for t in tabelas)))
    saida = []
    for t in tabelas:
        historico = sql(f"DESCRIBE HISTORY {catalogo}.{schema}.{t} LIMIT 1")
        gravada = datetime.fromisoformat(historico[0][1].replace("Z", "+00:00")).astimezone() if historico else None
        saida.append((t, int(linhas[t]), gravada.strftime("%d/%m %H:%M") if gravada else "?"))
    return saida


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description="Envia os arquivos de entrada para o volume dexp_landing.")
    parser.add_argument("--simular", action="store_true", help="não envia nada; só lista o que seria enviado")
    parser.add_argument("--forcar", action="store_true", help="reenvia mesmo os arquivos sem mudança")
    parser.add_argument("--somente", nargs="+", choices=GRUPOS, default=list(GRUPOS), help="grupos de fontes a enviar")
    parser.add_argument("--sem-job", action="store_true", help="só envia os arquivos, sem disparar o job do Databricks")
    parser.add_argument("--aguardar", action="store_true", help="espera o job terminar e mostra o resultado")
    parser.add_argument("--config", default=PASTA / "fontes.toml", type=Path)
    args = parser.parse_args()

    cfg = carregar_config(args.config)
    print(verificar_google_sheets(cfg)[1])
    w = None if args.simular else cliente(cfg)
    contagem = imprimir_resultados(cfg, enviar(cfg, w, args.somente, args.simular, args.forcar))
    if contagem["erro"]:
        print("❌ Houve erro no envio: o job do Databricks não foi disparado.")
        sys.exit(1)
    if args.simular or args.sem_job:
        return
    run_id = disparar_job(w, cfg["destino"]["job"])
    if args.aguardar and not acompanhar_job(w, run_id):
        sys.exit(1)


if __name__ == "__main__":
    main()
