"""Gera uma especificação em Markdown de um fluxo do Tableau Prep (.tfl/.tflx): etapas em ordem de execução,
com entradas, ações (filtros, renomeações, cálculos completos, remapeamentos), joins, unions, agregações e saídas.

Uso:
  python ferramentas\\especificar_fluxo_prep.py "<fluxo>.tfl" docs\\fluxos\\<nome>.md
"""
import json
import sys
import zipfile
from collections import defaultdict
from datetime import datetime, timezone

IGNORAR = {"nodeType", "name", "id", "baseType", "nextNodes", "serialize", "description", "beforeActionAnnotations",
           "afterActionAnnotations", "actionNode", "loomContainer", "connectionId", "connectionAttributes", "fields",
           "relation", "projectName", "projectLuid", "datasourceName", "datasourceDescription", "serverUrl"}


def tipo(n):
    return n.get("nodeType", "").split(".")[-1]


def data_ms(v):
    try:
        return datetime.fromtimestamp(int(v) / 1000, tz=timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
    except (TypeError, ValueError):
        return v


def acao(a):
    """Uma ação de limpeza em uma linha legível."""
    t = tipo(a)
    if t == "RenameColumn":
        return f"Renomear `{a['columnName']}` → `{a['rename']}`"
    if t == "RemoveColumns":
        return f"Remover colunas: {', '.join(f'`{c}`' for c in a['columnNames'])}"
    if t == "KeepOnlyColumns":
        return f"Manter só: {', '.join(f'`{c}`' for c in a['columnNames'])}"
    if t in ("AddColumn", "QuickCalcColumn", "DuplicateColumn"):
        verbo = {"AddColumn": "Calcular", "QuickCalcColumn": "Cálculo rápido", "DuplicateColumn": "Duplicar"}[t]
        extra = f" ({a['calc']})" if t == "QuickCalcColumn" and a.get("calc") else ""
        return f"{verbo} `{a['columnName']}`{extra}:\n\n```\n{a.get('expression', '')}\n```"
    if t == "ChangeColumnType":
        return "Mudar tipo: " + ", ".join(f"`{c}` → {d['type']}" for c, d in a["fields"].items())
    if t == "Remap":
        pares = "; ".join(f"{novo} ← {', '.join(v for v in velhos if v != novo)}" for novo, velhos in a["values"].items())
        return f"Remapear `{a['columnName']}`: {pares}"
    if t == "ValueFilter":
        modo = "Excluir" if a.get("exclude") else "Manter só"
        return "; ".join(f"{modo} `{c}` em {vals}" for c, vals in a["values"].items())
    if t == "RichRangeFilter":
        # richRangeType: 0 = intervalo (os dois limites), 1 = só máximo ("até"), 2 = só mínimo ("a partir de")
        nulos = "com" if a.get("includeNulls") else "sem"
        de, ate = data_ms(a.get("appliedMin")), data_ms(a.get("appliedMax"))
        regra = {0: f"entre {de} e {ate}", 1: f"até {ate}", 2: f"a partir de {de}"}.get(a.get("richRangeType"),
                                                                                       f"tipo {a.get('richRangeType')}: {de} .. {ate}")
        return f"Filtro de data `{a['columnName']}` ({a.get('dataType')}): **{regra}**, {nulos} nulos"
    if t == "FilterOperation":
        return f"Filtro:\n\n```\n{a['filterExpression'].strip()}\n```"
    if t in ("RichDiscreteValueFilter", "RichRelativeDateFilter"):
        resto = {k: v for k, v in a.items() if k not in IGNORAR}
        return f"{t}: `{json.dumps(resto, ensure_ascii=False)}`"
    resto = {k: v for k, v in a.items() if k not in IGNORAR}
    return f"{t}: `{json.dumps(resto, ensure_ascii=False)[:600]}`"


def coletar_nos(nodes, grupo, saida):
    for no in nodes.values():
        if tipo(no) in ("Group",):
            coletar_nos(no["loomContainer"]["nodes"], no["name"], saida)
        else:
            saida[no["id"]] = (no, grupo)


def acoes_container(no):
    """Etapa de limpeza antiga (Container): as ações são nós encadeados dentro do loomContainer."""
    interno = no["loomContainer"]
    nos = interno["nodes"]
    atual = interno.get("initialNodes", [None])[0]
    ordem = []
    while atual and atual in nos:
        ordem.append(nos[atual])
        proximos = nos[atual].get("nextNodes", [])
        atual = proximos[0]["nextNodeId"] if proximos else None
    return ordem


def main():
    origem, destino = sys.argv[1], sys.argv[2]
    with zipfile.ZipFile(origem) as z:
        fluxo = json.loads(z.read("flow").decode("utf-8"))
    conexoes = {k: v.get("connectionAttributes", {}) for k, v in fluxo["connections"].items()}

    nos = {}
    coletar_nos(fluxo["nodes"], None, nos)
    anteriores = defaultdict(list)
    for nid, (no, _) in nos.items():
        for p in no.get("nextNodes", []):
            anteriores[p["nextNodeId"]].append((nid, p.get("nextNamespace", "Default")))

    # ordem topológica estável (entradas primeiro, na ordem em que aparecem)
    grau = {nid: len(anteriores[nid]) for nid in nos}
    fila = [nid for nid in nos if grau[nid] == 0]
    ordem = []
    while fila:
        nid = fila.pop(0)
        ordem.append(nid)
        for p in nos[nid][0].get("nextNodes", []):
            grau[p["nextNodeId"]] -= 1
            if grau[p["nextNodeId"]] == 0:
                fila.append(p["nextNodeId"])

    numero = {nid: i for i, nid in enumerate(ordem, start=1)}
    ref = lambda nid: f"[{numero[nid]}] {nos[nid][0]['name']}"
    nome_fluxo = origem.replace("\\", "/").split("/")[-1]
    linhas = [f"# Especificação do fluxo `{nome_fluxo}`", "",
              "Gerado por `ferramentas/especificar_fluxo_prep.py`. Etapas em ordem de execução; `←` indica de onde vêm os dados.", ""]

    for nid in ordem:
        no, grupo = nos[nid]
        t = tipo(no)
        cab = f"## [{numero[nid]}] {no['name']} — {t}" + (f" (grupo {grupo})" if grupo else "")
        linhas += [cab, ""]
        if no.get("description"):
            linhas += [f"_Descrição:_ {no['description']}", ""]
        if anteriores[nid]:
            linhas += ["← " + "; ".join(f"{ref(a)}" + (f" ({ns})" if ns not in ("Default",) and not ns.startswith("Union-Namespace") else "")
                                         for a, ns in anteriores[nid]), ""]
        if t in ("LoadSql", "LoadSqlProxy"):
            c = conexoes.get(no.get("connectionId"), {})
            linhas += [f"Arquivo: `{c.get('cloudFileName') or c.get('dbname') or c.get('server')}` · aba `{no.get('relation', {}).get('table')}`", ""]
            campos = ", ".join(f"`{f['name']}`:{f['type']}" for f in no.get("fields", []))
            linhas += [f"Campos: {campos}", ""]
            if no.get("actions"):
                linhas += ["Ações na leitura:", ""] + [f"- {acao(a)}" for a in no["actions"]] + [""]
            if no.get("filters"):
                linhas += [f"Filtros na leitura: `{json.dumps(no['filters'], ensure_ascii=False)}`", ""]
        if t == "PublishExtract":
            linhas += [f"**Saída:** `{no['projectName']}/{no['datasourceName']}`", ""]

        acoes = []
        if t == "Container":
            acoes = acoes_container(no)
        for ann in no.get("beforeActionAnnotations", []):
            lado = ann.get("namespace")
            if lado in ("Left", "Right"):
                acoes.append({**ann["annotationNode"], "_lado": "esquerdo" if lado == "Left" else "direito"})
            else:
                acoes.append(ann["annotationNode"])
        principal = no.get("actionNode")
        if principal:
            pt = tipo(principal)
            if pt == "SimpleJoin":
                conds = " AND ".join(f"esq.{c['leftExpression']} {c['comparator']} dir.{c['rightExpression']}" for c in principal["conditions"])
                lados = {ns: ref(a) for a, ns in anteriores[nid]}
                linhas += [f"**Join {principal['joinType']}**: esquerda = {lados.get('Left')}, direita = {lados.get('Right')}", "",
                           f"Condição: `{conds}`", ""]
            elif pt == "SimpleUnion":
                mapeamentos = [m for m in principal.get("namespaceFieldMappings", []) if m.get("fieldMappings")]
                linhas += ["**Union** das entradas acima (colunas com o mesmo nome se juntam; cria `Table Names`)." , ""]
                for m in mapeamentos:
                    linhas += [f"- Mapeamento {m['namespaceName'][-8:]}: `{json.dumps(m['fieldMappings'], ensure_ascii=False)}`"]
                if mapeamentos:
                    linhas.append("")
            elif pt == "Aggregate":
                gb = ", ".join(f"`{g['columnName']}`" for g in principal.get("groupByFields", []))
                ag = ", ".join(f"{a['function']}(`{a['columnName']}`)" + (f" as `{a['newColumnName']}`" if a.get("newColumnName") else "")
                               for a in principal.get("aggregateFields", []))
                linhas += [f"**Agregar** agrupando por {gb or '(nada)'}: {ag}", ""]
            else:
                linhas += [acao(principal), ""]
        for ann in no.get("afterActionAnnotations", []):
            acoes.append(ann["annotationNode"])
        for i, a in enumerate(acoes, start=1):
            antes = f"(antes do join, lado {a['_lado']}) " if a.get("_lado") else ""
            linhas += [f"{i}. {antes}{acao(a)}"]
        if acoes:
            linhas.append("")
        proximos = [ref(p["nextNodeId"]) for p in no.get("nextNodes", []) if p["nextNodeId"] in numero]
        if proximos:
            linhas += ["→ " + "; ".join(proximos), ""]

    with open(destino, "w", encoding="utf-8") as f:
        f.write("\n".join(linhas))
    print(f"{len(ordem)} etapas -> {destino}")


if __name__ == "__main__":
    main()
