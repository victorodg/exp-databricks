"""Gera as linhas de um mês para as abas do Book e, opcionalmente, compara com um gabarito.

Uso (a partir da pasta book-executivo):
  python executar.py brasil 2026-10                 # gera outubro
  python executar.py brasil 2026-09 --validar       # gera setembro e compara com gabaritos/brasil_2026-09.json
Saída: saida/<frente>_<mês>.md
"""
import argparse
import re
import unicodedata
import json
import sys
from pathlib import Path

from book import brasil, hispana, hispana_geral
from book.brasil import MANUAL

FRENTES = {"brasil": brasil.ABAS, "mexico": hispana.ABAS_MEXICO, "sur": hispana.ABAS_SUR,
           "geral": hispana_geral.ABAS}
RAIZ = Path(__file__).resolve().parent


def normalizar(texto):
    """Compara nomes de plataforma e motivo sem diferença de maiúsculas e com as abreviações do Book."""
    t = str(texto).upper().strip()
    t = {"EXP. COMPRAS": "EXP. DE COMPRAS"}.get(t, t)
    # ignora acentos, hífens e espaços ("REGISTRO - APROBADO" = "Registro Aprobado")
    t = unicodedata.normalize("NFKD", t).encode("ascii", "ignore").decode()
    return re.sub(r"[^A-Z0-9%]", "", t)


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    p = argparse.ArgumentParser()
    p.add_argument("frente", choices=FRENTES)
    p.add_argument("mes", help="aaaa-mm")
    p.add_argument("--validar", action="store_true")
    p.add_argument("--abas", nargs="*", help="só estas abas")
    a = p.parse_args()

    gabarito = {}
    if a.validar:
        gabarito = json.loads((RAIZ / "gabaritos" / f"{a.frente}_{a.mes}.json").read_text(encoding="utf-8"))

    linhas = [f"# Book {a.frente}: {a.mes}", ""]
    total = iguais = 0
    dados = {}
    for aba, funcao in FRENTES[a.frente].items():
        if a.abas and aba not in a.abas:
            continue
        valores = funcao(a.mes)
        dados[aba] = valores
        if isinstance(valores, list):
            # aba de lista (várias linhas por mês): imprime a tabela; na validação confere o volume de cada motivo
            linhas += [f"## {aba}", ""]
            if valores:
                cols = list(valores[0])
                linhas += ["| " + " | ".join(cols) + " |" + (" Confere |" if a.validar else ""),
                           "|" + "---|" * (len(cols) + bool(a.validar))]
            # chave: as colunas de texto (plataforma, motivo, mercado...); valor comparado: a coluna de volume/percentual
            chave = lambda r: (tuple(normalizar(v) for k, v in r.items()
                                     if not any(c.isdigit() for c in str(v)) and v not in (MANUAL, brasil.A_INVESTIGAR))
                               or (normalizar(list(r.values())[0]),))
            valor = lambda r: next((str(v).replace(".", "") for k, v in r.items() if k.startswith("Volume") and "Plataforma" not in k),
                                   str(list(r.values())[-1]).replace(".", ""))
            book = {chave(r): valor(r) for r in gabarito.get(aba, [])} if a.validar else {}
            for r in valores:
                ok = ""
                if book:
                    esperado = book.get(chave(r))
                    total += 1
                    ok = "✅" if esperado == valor(r) else f"❌ ({esperado})"
                    iguais += ok == "✅"
                linhas.append("| " + " | ".join(r.values()) + " |" + (f" {ok} |" if a.validar else ""))
            linhas.append("")
            continue
        linhas += [f"## {aba}", "", "| Coluna | Valor |" + (" Book | Confere |" if a.validar else ""),
                   "|---|---|" + ("---|---|" if a.validar else "")]
        for coluna, valor in valores.items():
            if a.validar:
                esperado = gabarito.get(aba, {}).get(coluna, "")
                if valor in (MANUAL, brasil.A_INVESTIGAR):
                    ok = valor
                else:
                    total += 1
                    ok = "✅" if valor.replace(".", "") == esperado.replace(".", "") else "❌"
                    iguais += ok == "✅"
                linhas.append(f"| {coluna} | {valor} | {esperado} | {ok} |")
            else:
                linhas.append(f"| {coluna} | {valor} |")
        linhas.append("")
    if a.validar:
        linhas.insert(2, f"**Conferência: {iguais} de {total} colunas iguais ao Book.**\n")

    saida = RAIZ / "saida" / f"{a.frente}_{a.mes}.md"
    saida.parent.mkdir(exist_ok=True)
    saida.write_text("\n".join(linhas), encoding="utf-8")
    saida.with_suffix(".json").write_text(json.dumps(dados, ensure_ascii=False, indent=1), encoding="utf-8")
    print("\n".join(linhas))


if __name__ == "__main__":
    main()
