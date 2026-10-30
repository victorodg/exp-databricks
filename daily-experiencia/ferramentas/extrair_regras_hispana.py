"""Extrai do fluxo Hispana do Tableau Prep as listas e mapeamentos grandes usados na gold e grava src/dexp/regras_hispana.py.

Copiar essas listas à mão seria fácil de errar; aqui elas saem exatamente como estão no fluxo.
Uso: python ferramentas\\extrair_regras_hispana.py "<Daily Experiencia OIS.tfl>"
"""
import json
import pprint
import re
import sys
import zipfile
from pathlib import Path

from extrair_regras_mkt import acao, acoes, nos_por_nome, remap, valor

DESTINO = Path(__file__).resolve().parents[1] / "src" / "dexp" / "regras_hispana.py"


def mapa_setor(expressao):
    """IF [Setor Fim] = "X" THEN "Y" ... -> {"X": "Y"}."""
    return dict(re.findall(r'\[Setor Fim\]\s*=\s*"([^"]+)"\s*THEN\s*"([^"]+)"', expressao))


def regra_nivel(trecho):
    """Um CASE do Nível -> {"rotulos": {nível: [status]}, "senao": nível}."""
    rotulos = {}
    for status, nivel in re.findall(r'WHEN\s*"([^"]+)"\s*THEN\s*"([^"]+)"', trecho):
        rotulos.setdefault(nivel, []).append(status)
    return {"rotulos": rotulos, "senao": re.findall(r'ELSE\s*"([^"]+)"', trecho)[-1]}


def regras_nivel(expressao):
    """Os CASE da fórmula, na ordem; os limites de data ficam no código da gold."""
    return [regra_nivel(t) for t in re.split(r"\bCASE\b", expressao)[1:]]


def valores_filtro(no, coluna):
    return [valor(v) for a in acoes(no) if a["nodeType"].endswith(("RichDiscreteValueFilter", ".ValueFilter"))
            for v in a["values"].get(coluna, [])]


def main():
    fluxo = json.loads(zipfile.ZipFile(sys.argv[1]).read("flow"))
    nos = nos_por_nome(fluxo)
    resumen = acao(nos, "Resumen", "AddColumn", "Resumen")["expression"]
    regras = {
        "TIPO_TICKETS": mapa_setor(acao(nos, "Limpar 18", "AddColumn", "Tipo")["expression"]),
        "PAIS_TICKETS": mapa_setor(acao(nos, "Limpar 18", "AddColumn", "Pais")["expression"]),
        "TIPO_COMPLETO": mapa_setor(acao(nos, "Tipo, Pais, Segundos", "AddColumn", "Tipo")["expression"]),
        "PAIS_COMPLETO": mapa_setor(acao(nos, "Tipo, Pais, Segundos", "AddColumn", "Pais")["expression"]),
        "TIPO_ANALITICO": mapa_setor(acao(nos, "Segundos, Tipo, SLA e Pais", "AddColumn", "Tipo")["expression"]),
        "PAIS_ANALITICO": mapa_setor(acao(nos, "Segundos, Tipo, SLA e Pais", "AddColumn", "Pais")["expression"]),
        "NIVEL_REGISTRO_GRUPOS": regras_nivel(acao(nos, "Renomear colunas", "AddColumn", "Nivel")["expression"]),
        "NIVEL_TICKETS": regras_nivel(acao(nos, "Limpar 18", "AddColumn", "Nivel")["expression"]),
        "NIVEL_ANALITICO": regras_nivel(acao(nos, "Segundos, Tipo, SLA e Pais", "AddColumn", "Nivel")["expression"]),
        "NIVEL_COMPLETO": regras_nivel(acao(nos, "Nivel", "AddColumn", "Nivel")["expression"]),
        "RESUMEN_SERVICENOW": re.findall(r'CONTAINS\(\[Descripción Resumida\],\s*"([^"]+)"\)\s*THEN\s*"([^"]+)"', resumen),
        "STATUS_INELEGIVEIS": re.findall(r'WHEN\s*"([^"]+)"\s*THEN\s*"Excluir"',
                                         acao(nos, "Status Inelegíveis", "AddColumn", "Regra Status")["expression"]),
        "CLASSIFICACAO_N2_N3": valores_filtro(nos["Remove Status de Classificação"][0], "Status de Classificação 1"),
        "CLASSIFICACAO_EXCLUIDA": valores_filtro(nos["Status de Classificação"][0], "Status de Classificação 1"),
        "FINALIZACAO_EXCLUIDA": valores_filtro(nos["Status de Finalização"][0], "Status de finalização")
                                + valores_filtro(nos["Status Finalizacao removidos"][0], "Status de finalização"),
        "RESPONSAVEL_BASE": remap(acao(nos, "Retirar HealthCheck", "Remap", "Responsável")),
        "RESPONSAVEL_PRODUTIVIDADE": remap(acao(nos, "Responsavel", "Remap", "Responsável")),
    }
    # a lista de responsáveis ou de status vazia quer dizer que o nome da etapa ou da coluna mudou no fluxo
    vazias = [nome for nome, conteudo in regras.items() if not conteudo]
    assert not vazias, vazias
    assert [len(regras[n]) for n in ("NIVEL_REGISTRO_GRUPOS", "NIVEL_TICKETS", "NIVEL_ANALITICO", "NIVEL_COMPLETO")] == [3, 3, 3, 2]
    linhas = ['"""Listas e mapeamentos do fluxo Tableau Prep "Daily Experiencia OIS".',
              "", "Gerado por ferramentas/extrair_regras_hispana.py a partir do .tfl; não editar à mão.", '"""', ""]
    for nome, conteudo in regras.items():
        linhas.append(f"{nome} = {pprint.pformat(conteudo, width=120, sort_dicts=False)}")
        linhas.append("")
    DESTINO.write_text("\n".join(linhas), encoding="utf-8")
    for nome, conteudo in regras.items():
        print(f"{nome}: {len(conteudo)} itens")


if __name__ == "__main__":
    main()
