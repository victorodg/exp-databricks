"""Extrai do fluxo CSAT do Tableau Prep os mapeamentos usados na gold e grava src/dexp/regras_csat.py.

Os nomes têm erros de codificação no original ("JoÃ£o"); copiá-los à mão seria fácil de errar.
Uso: python ferramentas\\extrair_regras_csat.py "<GovEXP - Metricas de Excelencia - CSAT.tflx>"
"""
import json
import pprint
import sys
import zipfile
from pathlib import Path

from extrair_regras_hispana import mapa_setor
from extrair_regras_mkt import acao, nos_por_nome, remap

DESTINO = Path(__file__).resolve().parents[1] / "src" / "dexp" / "regras_csat.py"


def main():
    fluxo = json.loads(zipfile.ZipFile(sys.argv[1]).read("flow"))
    nos = nos_por_nome(fluxo)
    regras = {
        "PAIS_POR_SETOR": mapa_setor(acao(nos, "Manter Apenas Colunas para Join (1)", "AddColumn", "Pais")["expression"]),
        "NOTA_CSAT": remap(acao(nos, "Limpar 1 (1)", "Remap", "Nota")),
        "RESPONSAVEL_ENQUETE": remap(acao(nos, "Limpar 1 (1)", "Remap", "Responsavel")),
        "RESPONSAVEL_CONSOLIDADO": remap(acao(nos, "remover teste NCC", "Remap", "Responsavel", 0)),
        "RESPONSAVEL_FINAL": remap(acao(nos, "remover teste NCC", "Remap", "Responsavel", 1)),
        "NOTA_CES": remap(acao(nos, "Limpar 7 (1)", "Remap", "Nota")),
    }
    linhas = ['"""Mapeamentos do fluxo Tableau Prep "GovEXP - Metricas de Excelencia - CSAT".',
              "", "Gerado por ferramentas/extrair_regras_csat.py a partir do .tflx; não editar à mão.", '"""', ""]
    for nome, conteudo in regras.items():
        linhas.append(f"{nome} = {pprint.pformat(conteudo, width=120, sort_dicts=False)}")
        linhas.append("")
    DESTINO.write_text("\n".join(linhas), encoding="utf-8")
    for nome, conteudo in regras.items():
        print(f"{nome}: {len(conteudo)} itens")


if __name__ == "__main__":
    main()
