"""Leva para os fluxos do Prep a regra de nível do CRM da planilha "Definições N1 N2" (aba Brasil), a partir de 01/11/2026.

É a mesma regra da gold do Databricks (src/gold/dynamics_e_resenhas.py, REGRA_DEFINICOES_DESDE, e src/gold/mkt.py):

- "Daily Experiencia BR - Dynamics e Resenhas", etapa "SLA CLIENTE, SLA EXPERIENCIA" da visão Encerrado em:
  o cálculo "Nivel de Atendimento" ganha a regra nova na frente da antiga. No Dynamics o nível sai da Solução; no
  Salesforce, "Erro operacional" vira NEUTRO; o que a planilha não lista continua na regra antiga. O expurgo de nível
  ("Limpar 10") continua prevalecendo.
- Mesmo fluxo, etapa "Deixar colunas para MKT": os dois filtros que tiravam o retrabalho ("Erro operacional" e
  "Solicitação não procedente - Desvio operacional") viram um filtro só, que tira o retrabalho até 31/10/2026 e o
  mantém (como NEUTRO) a partir de 01/11/2026. Assim ele conta na produtividade e fica fora da Retenção.
- "Daily - Experiencia BR - MKT", etapa "Remoção do Dynamics": o retrabalho do CRM sai antes do Ticket Médio, como antes.

Uso: python ferramentas/aplicar_regra_definicoes_prep.py <Dynamics e Resenhas.tfl> <MKT.tfl>
Grava nos mesmos arquivos; faça uma cópia antes. Rodar de novo não duplica nada.
"""
import json
import sys
import uuid
import zipfile
from pathlib import Path

DESDE = "#2026-11-01#"
DESVIO = "Solicitação não procedente - Desvio operacional"
MARCA = "// Regra da planilha Definições N1 N2"

N1 = ["Cancelamento realizado", "Correção realizada", "Reativação realizada", "Reset de senha realizado",
      "Solicitação não procedente", "Solicitação procedente"]
N2 = ["Correção solicitada", "Correção solicitada - TD", "Correção solicitada TD"]
NEUTRO = ["Documento invalido", "Documento inválido", "Documento não anexado", "Documento não anexado:", DESVIO,
          "Solicitação não procedente –desvio operacional:", "Solicitação não procedente – Desvio operacional"]


INICIO_ANTIGA = '\nIF [Etapa] = "Análise Aplicativo Consultoria"'


def alguma(valores):
    """TRIM([Solução]) = "a" OR TRIM([Solução]) = "b" ... (sem IN, que o Prep não aceitou)."""
    return "(" + "\n  OR ".join(f'TRIM([Solução]) = "{v}"' for v in valores) + ")"


def expressao_nivel(antiga):
    """Uma cadeia IF/ELSEIF só: as condições novas na frente e a regra antiga, sem o IF inicial, em seguida."""
    assert antiga.count(INICIO_ANTIGA) == 1, "o começo da regra antiga mudou; conferir o cálculo no fluxo"
    resto = antiga.replace(INICIO_ANTIGA, '\nELSEIF [Etapa] = "Análise Aplicativo Consultoria"', 1)
    nova = f"""{MARCA} (aba Brasil), para tarefas encerradas a partir de 01/11/2026.
// Dynamics: o nível sai da Solução. Salesforce: Erro operacional é NEUTRO (retrabalho: fora da Retenção,
// mas conta na produtividade). O que a planilha não lista segue a regra antiga, logo abaixo.
IF [Término Real] >= {DESDE} AND [Fonte] = "Dynamics" AND {alguma(N1)} THEN "N1"
ELSEIF [Término Real] >= {DESDE} AND [Fonte] = "Dynamics" AND {alguma(N2)} THEN "N2"
ELSEIF [Término Real] >= {DESDE} AND [Fonte] = "Dynamics" AND {alguma(NEUTRO)} THEN "NEUTRO"
ELSEIF [Término Real] >= {DESDE} AND IFNULL([Fonte], "") <> "Dynamics" AND TRIM([Solução]) = "Erro operacional" THEN "NEUTRO"
"""
    return nova + resto.lstrip("\n")


FILTRO_RETRABALHO = f"""// Retrabalho (Erro operacional e Desvio operacional): até 31/10/2026 sai da base; a partir de 01/11/2026 fica,
// como NEUTRO, e conta na produtividade (regra da planilha Definições N1 N2).
NOT (IFNULL([Status de finalização], "") = "Erro operacional"
  OR IFNULL([Status de finalização], "") = "{DESVIO}")
OR IFNULL([Data], #1900-01-01#) >= {DESDE}"""


def ler(caminho):
    with zipfile.ZipFile(caminho) as z:
        partes = {n: z.read(n) for n in z.namelist()}
    return partes, json.loads(partes["flow"])


def gravar(caminho, partes, fluxo):
    partes["flow"] = json.dumps(fluxo, ensure_ascii=False, indent=2).encode("utf-8")
    temporario = caminho.with_suffix(".tmp")
    with zipfile.ZipFile(temporario, "w", zipfile.ZIP_DEFLATED) as z:
        for nome, conteudo in partes.items():
            z.writestr(nome, conteudo)
    temporario.replace(caminho)


def acoes(no):
    return [a["annotationNode"] for a in no.get("beforeActionAnnotations", [])]


def dynamics(caminho):
    partes, fluxo = ler(caminho)
    nos = fluxo["nodes"].values()

    # Visão Encerrado em: a etapa que calcula "SLA Experiência" (a da visão Criado em calcula "SLA Experiência 24 Horas")
    etapa = [n for n in nos if n["name"] == "SLA CLIENTE, SLA EXPERIENCIA"
             and any(a.get("columnName") == "SLA Experiência" for a in acoes(n))]
    assert len(etapa) == 1, f"etapas de Encerrado em encontradas: {len(etapa)}"
    calculo = next(a for a in acoes(etapa[0]) if a.get("columnName") == "Nivel de Atendimento")
    if MARCA in calculo["expression"]:
        print("Nivel de Atendimento: regra nova já estava no fluxo")
    else:
        calculo["expression"] = expressao_nivel(calculo["expression"])
        print("Nivel de Atendimento: regra nova incluída")

    mkt = next(n for n in nos if n["name"] == "Deixar colunas para MKT")
    anot = mkt["beforeActionAnnotations"]
    if any(a["annotationNode"].get("filterExpression") == FILTRO_RETRABALHO for a in anot):
        print("Deixar colunas para MKT: filtro do retrabalho já estava no fluxo")
    else:
        pos = [i for i, a in enumerate(anot) if a["annotationNode"]["nodeType"] == ".v1.ValueFilter"
               and list(a["annotationNode"].get("values", {})) == ["Status de finalização"]]
        assert len(pos) == 2 and pos[1] == pos[0] + 1 == len(anot) - 1, f"filtros do retrabalho fora do esperado: {pos}"
        primeiro = anot[pos[0]]["annotationNode"]
        anot[pos[0]]["annotationNode"] = {
            "nodeType": ".v1.FilterOperation", "name": "Retrabalho só a partir de nov/2026", "id": primeiro["id"],
            "baseType": "transform", "nextNodes": [], "serialize": False,
            "description": "Regra da planilha Definições N1 N2: retrabalho conta na produtividade como NEUTRO desde 01/11/2026",
            "filterExpression": FILTRO_RETRABALHO}
        del anot[pos[1]]
        print("Deixar colunas para MKT: dois filtros do retrabalho trocados por um filtro com data")
    gravar(caminho, partes, fluxo)


def mkt(caminho):
    partes, fluxo = ler(caminho)
    etapa = next(n for n in fluxo["nodes"].values() if n["name"] == "Remoção do Dynamics")
    conteiner = etapa["loomContainer"]
    filtro_nome = "Excluir Status de finalização: retrabalho do CRM"
    if any(n["name"] == filtro_nome for n in conteiner["nodes"].values()):
        print("Remoção do Dynamics: filtro do retrabalho já estava no fluxo")
    else:
        assert len(conteiner["initialNodes"]) == 1
        primeiro = conteiner["initialNodes"][0]
        assert conteiner["nodes"][primeiro]["name"].startswith("Remover Status de Classificação"), conteiner["nodes"][primeiro]["name"]
        novo = str(uuid.uuid4())
        conteiner["nodes"][novo] = {
            "nodeType": ".v1.ValueFilter", "name": filtro_nome, "id": novo, "baseType": "transform",
            "nextNodes": [{"namespace": "Default", "nextNodeId": primeiro, "nextNamespace": "Default"}],
            "serialize": False,
            "description": "Regra da planilha Definições N1 N2: o retrabalho do CRM entra no Nivel desde nov/2026, mas fica fora do Ticket Médio",
            "exclude": True, "values": {"Status de finalização": ['"Erro operacional"', f'"{DESVIO}"']}}
        conteiner["initialNodes"] = [novo]
        print("Remoção do Dynamics: filtro do retrabalho incluído antes de remover o Status de finalização")
    gravar(caminho, partes, fluxo)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    dynamics(Path(sys.argv[1]))
    mkt(Path(sys.argv[2]))
