"""Acrescenta ao fluxo Prep "Daily Experiencia BR - Dynamics e Resenhas" o expurgo de SLA por tarefa.

Lê a aba "Expurgo SLA" da mesma planilha do Google Drive do expurgo de nível (conexão "Expurgo") e, depois da etapa
"Limpar 10", marca como "EXPURGADO" o SLA Experiência, o SLA Cliente e o SLA 5 Horas das tarefas listadas. Assim
elas não contam como dentro nem como fora do prazo em nenhum SLA do workbook. É a mesma regra da gold do Databricks
(src/gold/dynamics_e_resenhas.py).

Etapas novas: entrada "Expurgo SLA" -> "Limpar Expurgo SLA" (só a coluna Tarefa) ->
"Tarefas expurgadas" (uma linha por tarefa, para o join não duplicar linhas) -> join à esquerda "Expurgo SLA" com
"Limpar 10" por [(Não Modificar) Tarefa] -> "Aplicar Expurgo SLA" -> "FASE, Tipo Protocolo" (como antes).

Se o fluxo já tem essas etapas, só refaz o tratamento de "Limpar Expurgo SLA" e "Aplicar Expurgo SLA".

Uso: python ferramentas/adicionar_expurgo_sla_prep.py <fluxo.tfl>   (grava no mesmo arquivo; faça uma cópia antes)
"""
import json
import sys
import time
import uuid
import zipfile
from pathlib import Path

CONEXAO_EXPURGO = "Expurgo"
ABA = "Expurgo SLA"
CAMPOS = [("Número da Ocorrência (Referente) (Ocorrência)", "string"), ("Tarefa", "string"), ("Etapa", "string"),
          ("Término Real", "string"), ("Indicador", "string"), ("Data Expurgo", "date"),
          ("Mês de Expurgo", "string"), ("Incidente", "string"), ("Motivo", "string"), ("Aprovado por", "string")]
SLAS = ["SLA Experiência", "SLA Cliente", "SLA 5 Horas"]


def novo_id():
    return str(uuid.uuid4())


def proximo(no_id, namespace="Default"):
    return {"namespace": "Default", "nextNodeId": no_id, "nextNamespace": namespace}


def anotacao(no):
    return {"namespace": "Default", "annotationNode": no}


def transformacao(tipo, nome, **campos):
    return {"nodeType": tipo, "name": nome, "id": novo_id(), "baseType": "transform", "nextNodes": [],
            "serialize": False, "description": None, **campos}


def renomear(de, para):
    return transformacao(".v1.RenameColumn", f"{de} renomeado como {para}", columnName=de, rename=para)


def super_no(tipo, nome, no_id, seguinte, antes=(), acao=None):
    return {"nodeType": tipo, "name": nome, "id": no_id, "baseType": "superNode", "nextNodes": [seguinte],
            "serialize": False, "description": None, "beforeActionAnnotations": [anotacao(a) for a in antes],
            "afterActionAnnotations": [], "actionNode": acao}


def tratamento_limpar():
    return [
        transformacao(".v1.RemoveColumns", "Remover colunas que não são a Tarefa",
                      columnNames=[n for n, _ in CAMPOS if n != "Tarefa"]),
        renomear("Tarefa", "Tarefa Expurgo SLA"),
    ]


def tratamento_aplicar():
    passos = []
    for sla in SLAS:
        passos += [
            transformacao(".v1.AddColumn", f"Add {sla} expurgo", columnName=f"{sla} expurgo",
                          expression=f'IF ISNULL([Tarefa Expurgo SLA]) THEN\n\t[{sla}]\nELSE\n\t"EXPURGADO"\nEND'),
            renomear(sla, f"{sla} antes do expurgo"),
            renomear(f"{sla} expurgo", sla),
        ]
    passos.append(transformacao(".v1.RemoveColumns", "Remover colunas do expurgo de SLA",
                                columnNames=[f"{s} antes do expurgo" for s in SLAS] + ["Tarefa Expurgo SLA"]))
    return passos


def gravar(caminho, partes, fluxo, exibicao):
    partes["flow"] = json.dumps(fluxo, ensure_ascii=False, indent=2).encode("utf-8")
    partes["displaySettings"] = json.dumps(exibicao, ensure_ascii=False, indent=2).encode("utf-8")
    temporario = caminho.with_suffix(".tmp")
    with zipfile.ZipFile(temporario, "w", zipfile.ZIP_DEFLATED) as z:
        for nome, conteudo in partes.items():
            z.writestr(nome, conteudo)
    temporario.replace(caminho)


def main():
    caminho = Path(sys.argv[1])
    with zipfile.ZipFile(caminho) as z:
        partes = {n: z.read(n) for n in z.namelist()}
    fluxo = json.loads(partes["flow"])
    exibicao = json.loads(partes["displaySettings"])
    nos = fluxo["nodes"]
    por_nome = {n["name"]: n for n in nos.values()}

    if ABA in por_nome:
        por_nome["Limpar Expurgo SLA"]["beforeActionAnnotations"] = [anotacao(a) for a in tratamento_limpar()]
        por_nome["Aplicar Expurgo SLA"]["beforeActionAnnotations"] = [anotacao(a) for a in tratamento_aplicar()]
        gravar(caminho, partes, fluxo, exibicao)
        print(f"Tratamento do expurgo de SLA atualizado em {caminho.name}")
        return

    conexao = next(c for c in fluxo["connections"].values() if c["name"] == CONEXAO_EXPURGO)
    limpar10, fase = por_nome["Limpar 10"], por_nome["FASE, Tipo Protocolo"]
    assert limpar10["nextNodes"] == [proximo(fase["id"])], limpar10["nextNodes"]

    ids = {k: novo_id() for k in ("entrada", "limpar", "agregar", "join", "aplicar")}
    entrada = {
        "nodeType": ".v1.LoadSql", "name": ABA, "id": ids["entrada"], "baseType": "input",
        "nextNodes": [proximo(ids["limpar"])], "serialize": False, "description": None,
        "connectionId": conexao["id"], "connectionAttributes": {},
        "fields": [{"name": n, "type": t, "collation": "LPT_RBR_S2" if t == "string" else None, "caption": "",
                    "ordinal": i, "isGenerated": False, "prettifiedName": n} for i, (n, t) in enumerate(CAMPOS)],
        "actions": [], "debugModeRowLimit": 393216, "originalDataTypes": {}, "randomSampling": None,
        "updateTimestamp": int(time.time() * 1000), "restrictedFields": {}, "userRenamedFields": {},
        "selectedFields": None, "samplingType": None, "groupByFields": None, "filters": [],
        "relation": {"type": "table", "table": f"[{ABA}$]"},
    }
    limpar = super_no(".v2018_2_3.SuperTransform", "Limpar Expurgo SLA", ids["limpar"], proximo(ids["agregar"]),
                      antes=tratamento_limpar())
    agregar = super_no(".v2018_2_3.SuperAggregate", "Tarefas expurgadas", ids["agregar"], proximo(ids["join"], "Right"),
                       acao=transformacao(".v1.Aggregate", "Agregar Expurgo SLA", aggregateFields=[], groupByFields=[
                           {"columnName": "Tarefa Expurgo SLA", "function": "GroupBy", "newColumnName": None,
                            "specialFieldType": None}]))
    juntar = super_no(".v2018_2_3.SuperJoin", "Expurgo SLA (tarefas)", ids["join"], proximo(ids["aplicar"]),
                      acao=transformacao(".v1.SimpleJoin", "Expurgo SLA (tarefas)", joinType="left", conditions=[
                          {"leftExpression": "[(Não Modificar) Tarefa]", "rightExpression": "[Tarefa Expurgo SLA]",
                           "comparator": "=="}]))
    aplicar = super_no(".v2018_2_3.SuperTransform", "Aplicar Expurgo SLA", ids["aplicar"], proximo(fase["id"]),
                       antes=tratamento_aplicar())

    limpar10["nextNodes"] = [proximo(ids["join"], "Left")]
    for no in (entrada, limpar, agregar, juntar, aplicar):
        nos[no["id"]] = no
    fluxo["initialNodes"].append(ids["entrada"])

    # posições no desenho: a entrada e o tratamento numa linha livre, o join e a aplicação antes de FASE
    posicoes = exibicao["flowDisplaySettings"]["flowNodeDisplaySettings"]
    ref = posicoes[fase["id"]]["position"]
    cor = posicoes[por_nome["Expurgo"]["id"]]["color"]
    livre_y = max(p["position"]["y"] for p in posicoes.values()) + 1
    for (chave, x, y) in [("entrada", ref["x"] - 4, livre_y), ("limpar", ref["x"] - 3, livre_y),
                          ("agregar", ref["x"] - 2, livre_y), ("join", ref["x"] - 1, livre_y),
                          ("aplicar", ref["x"] - 1, livre_y + 1)]:
        posicoes[ids[chave]] = {"color": cor, "position": {"x": x, "y": y}, "size": {"width": 1, "height": 1}}

    gravar(caminho, partes, fluxo, exibicao)
    print(f"Etapas de expurgo de SLA acrescentadas em {caminho.name}")


if __name__ == "__main__":
    main()
