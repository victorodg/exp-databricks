"""Leva para o fluxo do Prep "Daily Experiencia BR - Dynamics e Resenhas" os feriados nacionais no SLA das Resenhas Brasil
(pedido de 16/11/2026), lendo a base da ANBIMA. É a mesma regra da gold do Databricks (src/gold/dynamics_e_resenhas.py).

A base fica na planilha Expurgo (conexão "Expurgo", a mesma do expurgo de nível e do expurgo de SLA):
- aba "Feriados": a lista da ANBIMA (Data, Dia da Semana, Feriado, Dia Útil);
- aba "Calendário Feriados": uma linha por dia, calculada da lista, só com os feriados a partir de 01/11/2026:
  Data, Feriado (Sim/Não), Próximo Dia Útil, Feriados Acumulados (só feriados em dia útil) e Segundo Dia Útil.

O fluxo lê o calendário dentro dos dois grupos das Resenhas, por joins à esquerda pela data:

- "Resenhas AppSheets": join pelo dia da avaliação, entre "Limpar 3" e "Regras do SLA". O feriado é tratado como o
  fim de semana: a contagem começa no próximo dia útil às 08:00, e o prazo é o dia útil seguinte ao início.
- "Resenhas Google": os campos Status SLA e Status SLA 2 saem de "SLA Resenhas" e vão para a etapa nova
  "SLA Resenhas (feriados)", depois de 4 joins (dia da avaliação, da atualização, da resposta do EXP e de hoje). Os
  feriados em dia útil não contam como dias corridos.

Sem feriado no caminho (e para tudo antes de 01/11/2026), o resultado é o mesmo de antes. As colunas auxiliares (com
"_" na frente) saem no fim, para o extract não mudar.

Uso: python ferramentas/aplicar_feriados_resenhas_prep.py <Dynamics e Resenhas.tfl>
Grava no mesmo arquivo; faça uma cópia antes. Use sobre o fluxo sem a regra (rodar de novo para no aviso).
"""
import json
import re
import sys
import time
import uuid
import zipfile
from pathlib import Path

CONEXAO = "Expurgo"
ABA = "Calendário Feriados"
CAMPOS = [("Data", "date"), ("Feriado", "string"), ("Próximo Dia Útil", "date"), ("Feriados Acumulados", "integer"),
          ("Segundo Dia Útil", "date")]
MARCA = "// Feriados nacionais (ANBIMA, desde 01/11/2026; pedido de 16/11/2026)"


def novo_id():
    return str(uuid.uuid4())


def proximo(no_id, namespace="Default"):
    return {"namespace": "Default", "nextNodeId": no_id, "nextNamespace": namespace}


def acao(tipo, nome, **campos):
    return {"nodeType": tipo, "name": nome, "id": novo_id(), "baseType": "transform", "nextNodes": [],
            "serialize": False, "description": None, **campos}


def coluna(nome, expressao):
    return acao(".v1.AddColumn", f"Add {nome}", columnName=nome, expression=expressao)


def remover(colunas, nome="Remover colunas auxiliares dos feriados"):
    return acao(".v1.RemoveColumns", nome, columnNames=colunas)


def renomear(de, para):
    return acao(".v1.RenameColumn", f"{de} renomeado como {para}", columnName=de, rename=para)


def encadear(acoes):
    """Liga as ações em sequência (nextNodes) e devolve a lista de anotações."""
    for a, b in zip(acoes, acoes[1:]):
        a["nextNodes"] = [proximo(b["id"])]
    acoes[-1]["nextNodes"] = []
    return [{"namespace": "Default", "annotationNode": a} for a in acoes]


def etapa(nome, no_id, seguintes, acoes=()):
    return {"nodeType": ".v2018_2_3.SuperTransform", "name": nome, "id": no_id, "baseType": "superNode",
            "nextNodes": seguintes, "serialize": False, "description": None,
            "beforeActionAnnotations": encadear(list(acoes)) if acoes else [], "afterActionAnnotations": [],
            "actionNode": None}


def juntar(nome, no_id, seguinte, chave_esquerda, chave_direita):
    return {"nodeType": ".v2018_2_3.SuperJoin", "name": nome, "id": no_id, "baseType": "superNode",
            "nextNodes": [seguinte], "serialize": False, "description": None, "beforeActionAnnotations": [],
            "afterActionAnnotations": [], "actionNode": acao(".v1.SimpleJoin", nome, joinType="left", conditions=[
                {"leftExpression": f"[{chave_esquerda}]", "rightExpression": f"[{chave_direita}]", "comparator": "=="}])}


def entrada(no_id, conexao_id, seguintes):
    return {"nodeType": ".v1.LoadSql", "name": ABA, "id": no_id, "baseType": "input", "nextNodes": seguintes,
            "serialize": False, "description": None, "connectionId": conexao_id, "connectionAttributes": {},
            "fields": [{"name": n, "type": t, "collation": "LPT_RBR_S2" if t == "string" else None, "caption": "",
                        "ordinal": i, "isGenerated": False, "prettifiedName": n} for i, (n, t) in enumerate(CAMPOS)],
            "actions": [], "debugModeRowLimit": 393216, "originalDataTypes": {}, "randomSampling": None,
            "updateTimestamp": int(time.time() * 1000), "restrictedFields": {}, "userRenamedFields": {},
            "selectedFields": None, "samplingType": None, "groupByFields": None, "filters": [],
            "relation": {"type": "table", "table": f"[{ABA}$]"}}


def limpar_calendario(nome, no_id, seguinte, renomeacoes):
    """Só as colunas do calendário que o join usa, com nomes próprios (cada join tem a sua cópia)."""
    sobram = [n for n, _ in CAMPOS if n not in renomeacoes]
    acoes = ([remover(sobram, "Remover colunas que o join não usa")] if sobram else []) + \
        [renomear(de, para) for de, para in renomeacoes.items()]
    return etapa(nome, no_id, [seguinte], acoes)


def anexar(no, acoes):
    """Acrescenta ações no fim de uma etapa existente."""
    anot = no["beforeActionAnnotations"]
    novas = encadear(list(acoes))
    if anot:
        anot[-1]["annotationNode"]["nextNodes"] = [proximo(novas[0]["annotationNode"]["id"])]
    anot.extend(novas)


def coluna_existente(no, nome):
    achadas = [a["annotationNode"] for a in no["beforeActionAnnotations"]
               if a["annotationNode"].get("columnName") == nome and a["annotationNode"]["nodeType"] == ".v1.AddColumn"]
    assert len(achadas) == 1, f"{no['name']}: {nome} aparece {len(achadas)} vezes"
    return achadas[0]


def posicionar(exibicao, ids, x0, y, cor):
    posicoes = exibicao["flowDisplaySettings"]["flowNodeDisplaySettings"]
    for i, no_id in enumerate(ids):
        posicoes[no_id] = {"color": cor, "position": {"x": x0 + i, "y": y}, "size": {"width": 1, "height": 1}}


def linha_livre(exibicao):
    return max(p["position"]["y"] for p in exibicao["flowDisplaySettings"]["flowNodeDisplaySettings"].values()) + 1


# ---------------------------------------------------------------- Resenhas AppSheets

INICIO_APPSHEETS = f"""// Cenário 1: Fim de semana (Domingo=1 ou Sábado=7) ou feriado nacional
{MARCA}: o feriado é tratado como o fim de semana.
// Avaliações a partir de 01/11/2026: vai para o próximo dia útil às 08:00 (sem feriado, é a segunda-feira).
IF [Data da Resposta] >= #2026-11-01# AND ([_Dia da Semana da Resposta] = 1 OR [_Dia da Semana da Resposta] = 7 OR [_Feriado da Resposta] = "Sim") THEN
    MAKEDATETIME([_Próximo Dia Útil da Resposta], MAKETIME(8,0,0))

// Avaliações anteriores (regra antiga): fim de semana vai para a próxima segunda às 08:00
ELSEIF [_Dia da Semana da Resposta] = 1 OR [_Dia da Semana da Resposta] = 7 THEN
    MAKEDATETIME(
        DATE(DATEADD('day', IF [_Dia da Semana da Resposta] = 1 THEN 1 ELSE 2 END, [Data da Resposta])),
        MAKETIME(8,0,0)
    )

// Cenário 2: Dia útil, mas antes das 08:00 (Madrugada)
// Vai para as 08:00 do mesmo dia
ELSEIF [_Hora da Resposta] < 8 THEN
    MAKEDATETIME(DATE([Data da Resposta]), MAKETIME(8,0,0))

// Cenário 3: Dia útil, dentro do horário (08:00 em diante)
// Mantém a data original
ELSE
    DATETIME([Data da Resposta])
END"""

PRAZO_APPSHEETS = f"""{MARCA}: o prazo é o dia útil seguinte ao início, no mesmo horário.
// Sem feriado no caminho é o mesmo de antes: +1 dia, ou +3 se o início for sexta-feira.
// Avaliações anteriores a 01/11/2026 seguem a regra antiga, mesmo que o prazo caia depois.
// Se o início já foi levado para o próximo dia útil, o prazo é o segundo dia útil depois da avaliação.
IF [Data da Resposta] < #2026-11-01# AND DATEPART('weekday', [Início da Contagem SLA (Brasil)]) = 6 THEN
    DATEADD('day', 3, [Início da Contagem SLA (Brasil)])
ELSEIF [Data da Resposta] < #2026-11-01# THEN
    DATEADD('day', 1, [Início da Contagem SLA (Brasil)])
ELSEIF DATE([Início da Contagem SLA (Brasil)]) = [_Próximo Dia Útil da Resposta] THEN
    DATEADD('day', DATEDIFF('day', [_Próximo Dia Útil da Resposta], [_Segundo Dia Útil da Resposta]), [Início da Contagem SLA (Brasil)])
ELSE
    DATEADD('day', DATEDIFF('day', DATE([Início da Contagem SLA (Brasil)]), [_Próximo Dia Útil da Resposta]), [Início da Contagem SLA (Brasil)])
END"""


def appsheets(grupo, conexao_id, exibicao):
    nos = grupo["loomContainer"]["nodes"]
    por_nome = {n["name"]: n for n in nos.values()}
    assert ABA not in por_nome, "Resenhas AppSheets: o calendário já está no fluxo"
    limpar3, regras = por_nome["Limpar 3"], por_nome["Regras do SLA"]
    assert limpar3["nextNodes"] == [proximo(regras["id"])], limpar3["nextNodes"]

    ids = {k: novo_id() for k in ("entrada", "limpar", "join")}
    anexar(limpar3, [coluna("_Dia da Resposta", f"{MARCA}: chave do join com o calendário.\nDATE([Data da Resposta])")])
    nos[ids["entrada"]] = entrada(ids["entrada"], conexao_id, [proximo(ids["limpar"])])
    nos[ids["limpar"]] = limpar_calendario("Calendário (dia da avaliação)", ids["limpar"], proximo(ids["join"], "Right"), {
        "Data": "_Calendário Dia da Resposta", "Feriado": "_Feriado da Resposta",
        "Próximo Dia Útil": "_Próximo Dia Útil da Resposta", "Segundo Dia Útil": "_Segundo Dia Útil da Resposta"})
    nos[ids["join"]] = juntar("Feriados da avaliação", ids["join"], proximo(regras["id"]),
                              "_Dia da Resposta", "_Calendário Dia da Resposta")
    limpar3["nextNodes"] = [proximo(ids["join"], "Left")]
    grupo["loomContainer"]["initialNodes"].append(ids["entrada"])

    inicio = coluna_existente(regras, "Início da Contagem SLA (Brasil)")
    assert "IF [_Dia da Semana da Resposta] = 1 OR [_Dia da Semana da Resposta] = 7 THEN" in inicio["expression"]
    inicio["expression"] = INICIO_APPSHEETS
    coluna_existente(regras, "Prazo SLA (Brasil)")["expression"] = PRAZO_APPSHEETS
    status = coluna_existente(regras, "Status SLA")
    anot = regras["beforeActionAnnotations"]
    i = next(k for k, a in enumerate(anot) if a["annotationNode"] is status)
    novo = remover(["_Dia da Resposta", "_Calendário Dia da Resposta", "_Feriado da Resposta",
                    "_Próximo Dia Útil da Resposta", "_Segundo Dia Útil da Resposta"])
    novo["nextNodes"] = status["nextNodes"]
    status["nextNodes"] = [proximo(novo["id"])]
    anot.insert(i + 1, {"namespace": "Default", "annotationNode": novo})

    y = linha_livre(exibicao)
    cor = exibicao["flowDisplaySettings"]["flowNodeDisplaySettings"][regras["id"]]["color"]
    posicionar(exibicao, [ids["entrada"], ids["limpar"], ids["join"]], 3, y, cor)
    print("Resenhas AppSheets: calendário de feriados ligado; início e prazo do SLA com feriados")


# ---------------------------------------------------------------- Resenhas Google

TROCAS_GOOGLE = [
    ("DATEDIFF('day', DATE([Data Avaliação]), TODAY())",
     "(DATEDIFF('day', DATE([Data Avaliação]), TODAY()) - [_Feriados desde a Avaliação])", 2),
    ("DATEDIFF('day', DATE([Data Atualização da Avaliação]), TODAY())",
     "(DATEDIFF('day', DATE([Data Atualização da Avaliação]), TODAY()) - [_Feriados desde a Atualização])", 2),
    ("DATEADD('day', 5, DATE([Data Avaliação]))",
     "DATEADD('day', 5 + [_Feriados até a Resposta EXP], DATE([Data Avaliação]))", 1),
]
FIM_CASE_BAIXA = re.compile(r"END, *\n( *)\[Data Avaliação\]\)")
JOINS_GOOGLE = [  # (chave no fluxo, expressão da chave, coluna de acumulados)
    ("_Dia da Avaliação", "DATE([Data Avaliação])", "_Acumulados na Avaliação"),
    ("_Dia da Atualização", "DATE([Data Atualização da Avaliação])", "_Acumulados na Atualização"),
    ("_Dia da Resposta EXP", "DATE([Data da Resposta EXP])", "_Acumulados na Resposta EXP"),
    ("_Hoje", "TODAY()", "_Acumulados Hoje"),
]


def status_com_feriados(expressao, nome):
    e = expressao
    for velho, novo, vezes in TROCAS_GOOGLE:
        assert e.count(velho) == vezes, f"{nome}: '{velho}' aparece {e.count(velho)} vezes"
        e = e.replace(velho, novo)
    assert len(FIM_CASE_BAIXA.findall(e)) == 1, f"{nome}: prazo das 1 a 3 estrelas fora do esperado"
    e = FIM_CASE_BAIXA.sub(lambda m: f"END + [_Feriados até a Resposta EXP],\n{m.group(1)}[Data Avaliação])", e)
    return f"{MARCA}: os feriados em dia útil não contam como dias corridos.\n" + e


def google(grupo, conexao_id, exibicao):
    nos = grupo["loomContainer"]["nodes"]
    por_nome = {n["name"]: n for n in nos.values()}
    assert ABA not in por_nome, "Resenhas Google: o calendário já está no fluxo"
    sla, nome_apps = por_nome["SLA Resenhas"], por_nome["Nome Apps"]
    assert sla["nextNodes"] == [proximo(nome_apps["id"])], sla["nextNodes"]

    # Status SLA e Status SLA 2 saem de "SLA Resenhas" (são as duas últimas ações) e vão para depois dos joins
    anot = sla["beforeActionAnnotations"]
    assert [a["annotationNode"].get("columnName") for a in anot[-2:]] == ["Status SLA", "Status SLA 2"]
    status = [a["annotationNode"] for a in anot[-2:]]
    del anot[-2:]
    anot[-1]["annotationNode"]["nextNodes"] = []
    anexar(sla, [coluna(chave, f"{MARCA}: chave do join com o calendário.\n{expr}") for chave, expr, _ in JOINS_GOOGLE])

    ids = {"entrada": novo_id(), "final": novo_id()}
    limpezas, joins = [novo_id() for _ in JOINS_GOOGLE], [novo_id() for _ in JOINS_GOOGLE]
    nos[ids["entrada"]] = entrada(ids["entrada"], conexao_id, [proximo(i) for i in limpezas])
    anterior = sla
    for k, (chave, _, acumulados) in enumerate(JOINS_GOOGLE):
        cal = f"_Calendário{chave}"
        nos[limpezas[k]] = limpar_calendario(f"Calendário ({chave[1:]})", limpezas[k], proximo(joins[k], "Right"),
                                             {"Data": cal, "Feriados Acumulados": acumulados})
        seguinte = joins[k + 1] if k + 1 < len(joins) else ids["final"]
        nos[joins[k]] = juntar(f"Feriados ({chave[1:]})", joins[k], proximo(seguinte, "Left" if k + 1 < len(joins) else "Default"),
                               chave, cal)
        anterior["nextNodes"] = [proximo(joins[k], "Left")]
        anterior = nos[joins[k]]

    def zn(c):
        return f"IFNULL([{c}], 0)"

    def so_desde(expr):
        """Só para avaliações feitas a partir de 01/11/2026 (as anteriores seguem a regra antiga)."""
        return f"IIF(DATE([Data Avaliação]) >= #2026-11-01#, {expr}, 0)"
    auxiliares = [chave for chave, _, _ in JOINS_GOOGLE] + [f"_Calendário{chave}" for chave, _, _ in JOINS_GOOGLE] + \
        [a for _, _, a in JOINS_GOOGLE] + ["_Feriados desde a Avaliação", "_Feriados desde a Atualização",
                                           "_Feriados até a Resposta EXP"]
    for s in status:
        s["expression"] = status_com_feriados(s["expression"], s["columnName"])
        s["id"] = novo_id()
    nos[ids["final"]] = etapa("SLA Resenhas (feriados)", ids["final"], [proximo(nome_apps["id"])], [
        coluna("_Feriados desde a Avaliação",
               f"{MARCA}: feriados em dia útil depois da avaliação, até hoje.\n"
               + so_desde(f"{zn('_Acumulados Hoje')} - {zn('_Acumulados na Avaliação')}")),
        coluna("_Feriados desde a Atualização",
               f"{MARCA}\n" + so_desde(f"{zn('_Acumulados Hoje')} - {zn('_Acumulados na Atualização')}")),
        coluna("_Feriados até a Resposta EXP",
               f"{MARCA}\n" + so_desde(f"{zn('_Acumulados na Resposta EXP')} - {zn('_Acumulados na Avaliação')}")),
        *status,
        remover(auxiliares),
    ])
    grupo["loomContainer"]["initialNodes"].append(ids["entrada"])

    y = linha_livre(exibicao)
    cor = exibicao["flowDisplaySettings"]["flowNodeDisplaySettings"][sla["id"]]["color"]
    posicionar(exibicao, [ids["entrada"]], 2, y, cor)
    for k in range(len(JOINS_GOOGLE)):
        posicionar(exibicao, [limpezas[k]], 3 + k, y, cor)
        posicionar(exibicao, [joins[k]], 3 + k, y + 1, cor)
    posicionar(exibicao, [ids["final"]], 3 + len(JOINS_GOOGLE), y + 1, cor)
    print("Resenhas Google: calendário de feriados ligado; Status SLA e Status SLA 2 descontam os feriados")


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    caminho = Path(sys.argv[1])
    with zipfile.ZipFile(caminho) as z:
        partes = {n: z.read(n) for n in z.namelist()}
    fluxo, exibicao = json.loads(partes["flow"]), json.loads(partes["displaySettings"])
    if MARCA in partes["flow"].decode("utf-8"):
        print("O fluxo já tem a regra de feriados; nada foi alterado.")
        return
    conexao = next(c for c in fluxo["connections"].values() if c["name"] == CONEXAO)
    grupos = {n["name"]: n for n in fluxo["nodes"].values() if n["nodeType"].endswith(".Group")}
    appsheets(grupos["Resenhas AppSheets"], conexao["id"], exibicao)
    google(grupos["Resenhas Google"], conexao["id"], exibicao)
    partes["flow"] = json.dumps(fluxo, ensure_ascii=False, indent=2).encode("utf-8")
    partes["displaySettings"] = json.dumps(exibicao, ensure_ascii=False, indent=2).encode("utf-8")
    temporario = caminho.with_suffix(".tmp")
    with zipfile.ZipFile(temporario, "w", zipfile.ZIP_DEFLATED) as z:
        for nome, conteudo in partes.items():
            z.writestr(nome, conteudo)
    temporario.replace(caminho)


if __name__ == "__main__":
    main()
