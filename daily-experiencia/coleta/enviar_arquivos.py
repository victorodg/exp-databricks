"""Envia os arquivos de entrada do Daily Experiência BR para o volume dexp_landing no Databricks.

Fontes (configuradas em fontes.toml):
  - mktzap:        brutos baixados pelo Selenium (logic\\mktzap\\downloads_brutos\\<AAAAMM>\\<operação>\\)
  - drive:         planilhas .xlsx do Drive compartilhado
  - google_sheets: cópias .xlsx das Google Sheets geradas pelo Apps Script (google_sheets/exportar_planilhas.gs)

Destino no volume:
  mktzap/<operação>/<AAAAMM>/<arquivo>
  drive/<fonte>/<AAAA-MM-DD>/<arquivo>            (AAAA-MM-DD = dia em que esta versão foi capturada)
  google_sheets/<fonte>/<AAAA-MM-DD>/<arquivo>
A data é a da captura, e não a de alteração do arquivo, porque o Google Drive para desktop
reescreve a data de alteração toda vez que baixa o arquivo para leitura.

Arquivos iguais aos do último envio são pulados (comparação por SHA-256, guardada em .estado/manifesto.json).
Nada é apagado, nem no volume nem na origem.

Uso (a partir da pasta daily-experiencia):
  .venv\\Scripts\\python.exe coleta\\enviar_arquivos.py                       # envia tudo
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
import tomllib
from dataclasses import dataclass
from datetime import date, datetime
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


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description="Envia os arquivos de entrada para o volume dexp_landing.")
    parser.add_argument("--simular", action="store_true", help="não envia nada; só lista o que seria enviado")
    parser.add_argument("--forcar", action="store_true", help="reenvia mesmo os arquivos sem mudança")
    parser.add_argument("--somente", nargs="+", choices=GRUPOS, default=list(GRUPOS), help="grupos de fontes a enviar")
    parser.add_argument("--config", default=PASTA / "fontes.toml", type=Path)
    args = parser.parse_args()

    with open(args.config, "rb") as f:
        cfg = tomllib.load(f)
    volume = cfg["destino"]["volume"].rstrip("/")
    manifesto = json.loads(ARQUIVO_MANIFESTO.read_text("utf-8")) if ARQUIVO_MANIFESTO.exists() else {}
    w = None
    if not args.simular:
        w = WorkspaceClient(config=Config(profile=cfg["destino"]["perfil"], databricks_cli_path=caminho_cli()))

    resultados = []  # (chave, situação, detalhe)
    for grupo in args.somente:
        for envio in GERADORES[grupo](cfg):
            if envio.destino is None:
                resultados.append((envio.chave, "ausente", str(envio.origem)))
                continue
            try:
                hash_atual = sha256(envio.origem)
                anterior = manifesto.get(envio.chave)
                if anterior and anterior["sha256"] == hash_atual and not args.forcar:
                    resultados.append((envio.chave, "sem mudança", anterior["destino"]))
                    continue
                remoto = f"{volume}/{envio.destino}"
                if args.simular:
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

    icones = {"enviado": "✅", "a enviar": "📤", "sem mudança": "➖", "ausente": "⚠️", "erro": "❌"}
    print(f"Volume: {volume}\n")
    for chave, situacao, detalhe in resultados:
        if situacao != "sem mudança":
            print(f"{icones[situacao]} {situacao:11} {detalhe}" if detalhe.startswith(chave)
                  else f"{icones[situacao]} {situacao:11} {chave}: {detalhe}")
    contagem = {s: sum(1 for r in resultados if r[1] == s) for s in icones}
    print("\nResumo: " + " | ".join(f"{s}: {n}" for s, n in contagem.items() if n))
    if contagem["ausente"]:
        print("⚠️ Arquivos ausentes não foram enviados: confira o caminho em fontes.toml ou se a exportação rodou.")
    sys.exit(1 if contagem["erro"] else 0)


if __name__ == "__main__":
    main()
