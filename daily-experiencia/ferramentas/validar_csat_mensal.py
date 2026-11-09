"""Valida os indicadores do CSAT mês a mês: extract "Enquetes C-SAT" (Tableau) × gold (Databricks).

Calcula, por operação e mês, os indicadores com as fórmulas do workbook "GovEXP - Métricas da Excelência", no extract e
na view dexp_vw_csat_enquetes (mesmos nomes de campo), e mostra onde diferem. Depois compara o que o painel do Tableau
mostra com a regra nova da gold (dexp_gold_csat_mensal: tudo por protocolo distinto), para registrar o efeito da mudança.

Uso (a partir da pasta daily-experiencia):
  .venv\\Scripts\\python.exe ferramentas\\validar_csat_mensal.py [extract.tdsx] [--ate AAAA-MM] [--saida relatorio.md]

Sem --ate, compara até o mês anterior ao da última data do extract (o último mês do extract está incompleto).
"""
import argparse
import sys
import tempfile
from pathlib import Path

from tableauhyperapi import Connection, HyperProcess, Telemetry

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from comparar_extract import ESQUEMA, arquivo_hyper, cliente, sql_databricks  # noqa: E402
from dexp.csat_saidas import SQL_MENSAL  # noqa: E402

PASTA = Path(__file__).resolve().parents[1]
EXTRACT_PADRAO = PASTA / "validacao" / "extracts_csat" / "Enquetes C-SAT.tdsx"
RESPONDIDA = "('PROMOTOR', 'NEUTRO', 'DETRATOR')"
NOTAS_CES = "('1 - Muito Difícil', '2 - Difícil', '3 - Neutro | Razoável', '4 - Fácil', '5 - Muito Fácil')"

# Indicador -> (expressão com as fórmulas do workbook, casas para comparar). {c} é a coluna C-SAT e assim por diante.
INDICADORES = {
    # Medidores: (SUM(Nota da CSAT)/5) / COUNTD(Protocolo), com C-SAT em promotor, neutro ou detrator
    "csat": ("(SUM(CASE WHEN {c} IN " + RESPONDIDA + " THEN {nota_csat} END) / 5.0)"
             " / NULLIF(COUNT(DISTINCT CASE WHEN {c} IN " + RESPONDIDA + " THEN {p} END), 0)", 6),
    "csat_simple": ("(SUM(CASE WHEN {c} IN " + RESPONDIDA + " THEN {nota_simple} END) / 5.0)"
                    " / NULLIF(COUNT(DISTINCT CASE WHEN {c} IN " + RESPONDIDA + " THEN {p} END), 0)", 6),
    # Status e Response Rate
    "enviadas": ("COUNT(DISTINCT {p})", 0),
    "respondidas": ("COUNT(DISTINCT CASE WHEN {c} <> 'Não respondido' THEN {p} END)", 0),
    # Cartões e gráficos de Brasil e Hispana: linhas da fatia 1
    "promotores_linhas": ("SUM(CASE WHEN {s} = 1 AND {c} = 'PROMOTOR' THEN 1 ELSE 0 END)", 0),
    "neutros_linhas": ("SUM(CASE WHEN {s} = 1 AND {c} = 'NEUTRO' THEN 1 ELSE 0 END)", 0),
    "detratores_linhas": ("SUM(CASE WHEN {s} = 1 AND {c} = 'DETRATOR' THEN 1 ELSE 0 END)", 0),
    "respondidas_linhas": ("SUM(CASE WHEN {s} = 1 THEN {resp} ELSE 0 END)", 0),
    # Cartões e gráficos do NCC: protocolos distintos
    "promotores": ("COUNT(DISTINCT CASE WHEN {c} = 'PROMOTOR' THEN {p} END)", 0),
    "neutros": ("COUNT(DISTINCT CASE WHEN {c} = 'NEUTRO' THEN {p} END)", 0),
    "detratores": ("COUNT(DISTINCT CASE WHEN {c} = 'DETRATOR' THEN {p} END)", 0),
    # CES - Total Respostas e Média: o gráfico não filtra a fatia, então o total sai 5x
    "ces_total_painel": ("SUM(CASE WHEN {n} IN " + NOTAS_CES + " THEN 1 ELSE 0 END)", 0),
    "ces_media": ("SUM(CASE WHEN {n} IN " + NOTAS_CES + " THEN {nota_ces} END) * 1.0"
                  " / NULLIF(SUM(CASE WHEN {n} IN " + NOTAS_CES + " THEN 1 ELSE 0 END), 0)", 6),
}
CAMPOS = {"c": "C-SAT", "p": "Protocolo", "s": "Slice #", "n": "Nota", "nota_csat": "Nota da CSAT",
          "nota_simple": "Nota da CSAT Simple", "nota_ces": "Nota CES", "resp": "Enquete Respondida",
          "fonte": "Fonte", "data": "Data"}


def consulta(citar, tabela):
    c = {k: citar(v) for k, v in CAMPOS.items()}
    mes = f"CAST(EXTRACT(YEAR FROM {c['data']}) * 100 + EXTRACT(MONTH FROM {c['data']}) AS INT)"
    colunas = ",\n  ".join(f"{expr.format(**c)} AS {nome}" for nome, (expr, _) in INDICADORES.items())
    return f"SELECT {c['fonte']}, {mes},\n  {colunas}\nFROM {tabela}\nGROUP BY 1, 2"


def numero(v):
    return None if v is None else float(v)


def chaves(linhas):
    return {(str(l[0]), f"{int(l[1]) // 100}-{int(l[1]) % 100:02d}"): [numero(v) for v in l[2:]] for l in linhas}


def fmt(v, casas):
    if v is None:
        return "–"
    return f"{v:.{casas}f}" if casas else f"{v:,.0f}".replace(",", ".")


def painel_tableau(fonte, ind):
    """O que cada painel do Tableau mostra: Brasil e Hispana contam linhas, NCC e CES contam protocolos."""
    linhas = fonte in ("Experiencia Brasil", "Hispana")
    return {
        "csat": ind["csat"], "csat_simple": ind["csat_simple"],
        "response_rate": ind["respondidas"] / ind["enviadas"] if ind["enviadas"] else None,
        "promotores": ind["promotores_linhas"] if linhas else ind["promotores"],
        "neutros": ind["neutros_linhas"] if linhas else ind["neutros"],
        "detratores": ind["detratores_linhas"] if linhas else ind["detratores"],
        "respondidas": ind["respondidas_linhas"] if linhas else ind["respondidas"],
        "ces_respostas": ind["ces_total_painel"], "ces_media": ind["ces_media"],
    }


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser()
    ap.add_argument("extract", nargs="?", default=str(EXTRACT_PADRAO))
    ap.add_argument("--ate", help="último mês comparado (AAAA-MM)")
    ap.add_argument("--saida", help="grava o relatório em Markdown neste arquivo")
    args = ap.parse_args()

    with tempfile.TemporaryDirectory() as pasta, HyperProcess(Telemetry.DO_NOT_SEND_USAGE_DATA_TO_TABLEAU) as hyper:
        with Connection(hyper.endpoint, str(arquivo_hyper(Path(args.extract), pasta))) as con:
            ext = chaves(con.execute_list_query(consulta(lambda n: f'"{n}"', '"Extract"."Extract"')))
            ultima = con.execute_scalar_query('SELECT MAX("Data") FROM "Extract"."Extract"')
    w = cliente()
    gold = chaves(sql_databricks(w, consulta(lambda n: f"`{n}`", f"{ESQUEMA}.dexp_vw_csat_enquetes")))
    nova = {(l[0], l[1]): l for l in sql_databricks(w, f"SELECT * FROM ({SQL_MENSAL.format(enquetes=f'{ESQUEMA}.dexp_gold_csat_enquetes')})")}

    ate = args.ate
    if not ate:
        a, m = ultima.year, ultima.month
        ate = f"{a - 1}-12" if m == 1 else f"{a}-{m - 1:02d}"
    nomes = list(INDICADORES)
    meses = sorted(k for k in set(ext) | set(gold) if k[1] <= ate)

    saida = [f"# Validação mensal do CSAT – extract × gold\n",
             f"Extract: `{Path(args.extract).name}` (última data {ultima}). Meses comparados: até {ate}.\n",
             "## 1. Fórmulas do Tableau nos dois lados\n"]
    diferencas = []
    for k in meses:
        a, b = ext.get(k), gold.get(k)
        if a is None or b is None:
            diferencas.append((k, "mês só de um lado", fmt(None, 0), fmt(None, 0)))
            continue
        for i, nome in enumerate(nomes):
            casas = INDICADORES[nome][1]
            if fmt(a[i], casas) != fmt(b[i], casas):
                diferencas.append((k, nome, fmt(a[i], casas), fmt(b[i], casas)))
    por_fonte = {}
    for f, _ in meses:
        por_fonte[f] = por_fonte.get(f, 0) + 1
    meses_com_dif = {k for k, *_ in diferencas}
    saida.append("| Operação | Meses | Meses iguais em todos os indicadores |\n|---|---|---|")
    for f, n in sorted(por_fonte.items()):
        iguais = sum(1 for k in meses if k[0] == f and k not in meses_com_dif)
        saida.append(f"| {f} | {n} | {iguais} |")
    if diferencas:
        saida.append("\n| Operação | Mês | Indicador | Extract | Gold |\n|---|---|---|---|---|")
        saida += [f"| {k[0]} | {k[1]} | {nome} | {x} | {y} |" for k, nome, x, y in diferencas]

    saida.append("\n## 2. Painel do Tableau × regra nova (protocolos distintos)\n")
    saida.append("Valores da gold. C-SAT e Response Rate em %, com 2 casas.\n")
    saida.append("| Operação | Mês | C-SAT painel | C-SAT novo | Simple painel | Simple novo | Promotores painel | novo |"
                 " Respondidas painel | novo | CES respostas painel | novo |\n|---|---|---|---|---|---|---|---|---|---|---|---|")
    pct = lambda v: "–" if v is None else f"{100 * float(v):.2f}"
    for k in sorted(gold):
        if k not in nova:
            continue
        p = painel_tableau(k[0], dict(zip(nomes, gold[k])))
        n = nova[k]  # fonte, mes, enviadas, respondidas, sem_resposta, promotores, neutros, detratores, csat, simple, rr, ces_resp, ces_media
        linha = [pct(p["csat"]), pct(n[8]), pct(p["csat_simple"]), pct(n[9]), fmt(p["promotores"], 0), fmt(numero(n[5]), 0),
                 fmt(p["respondidas"], 0), fmt(numero(n[3]), 0)]
        linha += [fmt(p["ces_respostas"], 0), fmt(numero(n[11]), 0)] if k[0] == "CES" else ["", ""]
        diferente = linha[0] != linha[1] or linha[2] != linha[3] or linha[4] != linha[5] or linha[6] != linha[7] or linha[8] != linha[9]
        if diferente:
            saida.append(f"| {k[0]} | {k[1]} | " + " | ".join(linha) + " |")
    saida.append("\nSó aparecem os meses em que algum valor muda.")

    texto = "\n".join(saida)
    print(texto)
    if args.saida:
        Path(args.saida).write_text(texto + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
