"""Leva para o fluxo do Prep "Daily Experiencia BR - Dynamics e Resenhas" os feriados nacionais no SLA das Resenhas Brasil
(pedido de 16/11/2026). É a mesma regra da gold do Databricks (src/gold/dynamics_e_resenhas.py, FERIADOS_NACIONAIS):

- "Resenhas AppSheets" > "Regras do SLA": o feriado é tratado como o fim de semana. Se a avaliação cai num feriado, a
  contagem começa no próximo dia útil às 08:00; o prazo é o próximo dia útil depois do início (pula sábado, domingo e
  feriado). Sem feriado no caminho, o resultado é o mesmo de antes (segunda às 08:00 no fim de semana; +1 dia, ou +3
  na sexta).
- "Resenhas Google" > "SLA Resenhas": os feriados não contam como dias corridos, nos dois campos "Status SLA" e
  "Status SLA 2".

A lista de feriados é lida da gold, para as duas pontas usarem a mesma. Começa em 20/11/2026, então nenhum mês fechado
muda. As colunas auxiliares (prefixo "_Feriado"/"_Próximo") saem no fim de cada etapa, para o extract não mudar.

Uso: python ferramentas/aplicar_feriados_resenhas_prep.py <Dynamics e Resenhas.tfl>
Grava no mesmo arquivo; faça uma cópia antes. Rodar de novo não duplica nada.
"""
import ast
import json
import re
import sys
import uuid
import zipfile
from pathlib import Path

GOLD = Path(__file__).resolve().parent.parent / "src" / "gold" / "dynamics_e_resenhas.py"
MARCA = "// Feriados nacionais (pedido de 16/11/2026)"


def feriados():
    texto = GOLD.read_text(encoding="utf-8")
    lista = re.search(r"^FERIADOS_NACIONAIS = (\[.*?\])", texto, re.S | re.M).group(1)
    return ast.literal_eval(lista)


FERIADOS = feriados()


def eh_feriado(dia):
    return "(" + " OR ".join(f"{dia} = #{d}#" for d in FERIADOS) + ")"


def dia_util(dia):
    return f"(DATEPART('weekday', {dia}) <> 1 AND DATEPART('weekday', {dia}) <> 7 AND NOT {eh_feriado(dia)})"


def proximo_dia_util(dia):
    """IF/ELSEIF plano (sem IF aninhado, que o Prep Builder recusou em 13/11)."""
    partes = []
    for n in range(1, 5):
        d = f"DATE(DATEADD('day', {n}, {dia}))"
        partes.append(f"{'IF' if n == 1 else 'ELSEIF'} {dia_util(d)} THEN {d}")
    return f"{MARCA}: primeiro dia depois que não é sábado, domingo nem feriado.\n" + "\n".join(partes) + \
        f"\nELSE DATE(DATEADD('day', 5, {dia}))\nEND"


def feriados_entre(depois_de, ate):
    # Data nula dá nulo; esses campos só são usados nos ramos em que as datas existem.
    termos = " +\n".join(f"IIF(#{d}# > {depois_de} AND #{d}# <= {ate}, 1, 0)" for d in FERIADOS)
    return f"{MARCA}: feriados no intervalo (início, fim].\n{termos}"


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


def etapa(fluxo, caminho_nome):
    def walk(nos, prefixo=""):
        for n in nos.values():
            yield prefixo + n.get("name", ""), n
            if "loomContainer" in n:
                yield from walk(n["loomContainer"]["nodes"], prefixo + n.get("name", "") + " > ")
    achadas = [n for p, n in walk(fluxo["nodes"]) if p == caminho_nome]
    assert len(achadas) == 1, f"{caminho_nome}: {len(achadas)} etapas"
    return achadas[0]["beforeActionAnnotations"]


def posicao(anot, coluna):
    pos = [i for i, a in enumerate(anot) if a["annotationNode"].get("columnName") == coluna
           and a["annotationNode"]["nodeType"] == ".v1.AddColumn"]
    assert len(pos) == 1, f"{coluna}: {pos}"
    return pos[0]


def inserir(anot, indice, no):
    """Insere a ação na posição `indice`, refazendo a corrente de nextNodes."""
    no.update({"id": str(uuid.uuid4()), "baseType": "transform", "serialize": False, "description": None})
    anterior = anot[indice - 1]["annotationNode"]
    no["nextNodes"] = anterior["nextNodes"]
    anterior["nextNodes"] = [{"namespace": "Default", "nextNodeId": no["id"], "nextNamespace": "Default"}]
    anot.insert(indice, {"namespace": "Default", "annotationNode": no})


def nova_coluna(coluna, expressao):
    return {"nodeType": ".v1.AddColumn", "columnName": coluna, "expression": expressao, "name": f"Add {coluna}"}


def remover(colunas):
    return {"nodeType": ".v1.RemoveColumns", "name": "Remover colunas auxiliares dos feriados", "columnNames": colunas}


def appsheets(fluxo):
    anot = etapa(fluxo, "Resenhas AppSheets > Regras do SLA")
    if any(MARCA in (a["annotationNode"].get("expression") or "") for a in anot):
        print("Resenhas AppSheets: feriados já estavam no fluxo")
        return
    i = posicao(anot, "Início da Contagem SLA (Brasil)")
    inicio = anot[i]["annotationNode"]
    assert "IF [_Dia da Semana da Resposta] = 1 OR [_Dia da Semana da Resposta] = 7 THEN" in inicio["expression"]
    assert "ELSEIF [_Hora da Resposta] < 8 THEN" in inicio["expression"]
    inserir(anot, i, nova_coluna("_Feriado da Resposta", f"{MARCA}\n{eh_feriado('DATE([Data da Resposta])')}"))
    inserir(anot, i + 1, nova_coluna("_Próximo Dia Útil da Resposta", proximo_dia_util("DATE([Data da Resposta])")))
    inicio["expression"] = f"""// Cenário 1: Fim de semana (Domingo=1 ou Sábado=7) ou feriado nacional
{MARCA}: o feriado é tratado como o fim de semana.
// Vai para o próximo dia útil às 08:00 (sem feriado, é a segunda-feira).
IF [_Dia da Semana da Resposta] = 1 OR [_Dia da Semana da Resposta] = 7 OR [_Feriado da Resposta] THEN
    MAKEDATETIME([_Próximo Dia Útil da Resposta], MAKETIME(8,0,0))

// Cenário 2: Dia útil, mas antes das 08:00 (Madrugada)
// Vai para as 08:00 do mesmo dia
ELSEIF [_Hora da Resposta] < 8 THEN
    MAKEDATETIME(DATE([Data da Resposta]), MAKETIME(8,0,0))

// Cenário 3: Dia útil, dentro do horário (08:00 em diante)
// Mantém a data original
ELSE
    DATETIME([Data da Resposta])
END"""
    j = posicao(anot, "Prazo SLA (Brasil)")
    inserir(anot, j, nova_coluna("_Próximo Dia Útil do Início", proximo_dia_util("DATE([Início da Contagem SLA (Brasil)])")))
    prazo = anot[j + 1]["annotationNode"]
    prazo["expression"] = f"""{MARCA}: o prazo é o próximo dia útil depois do início, no mesmo horário.
// Sem feriado no caminho é o mesmo de antes: +1 dia, ou +3 se o início for sexta-feira.
DATEADD('day', DATEDIFF('day', DATE([Início da Contagem SLA (Brasil)]), [_Próximo Dia Útil do Início]), [Início da Contagem SLA (Brasil)])"""
    k = posicao(anot, "Status SLA")
    inserir(anot, k + 1, remover(["_Feriado da Resposta", "_Próximo Dia Útil da Resposta", "_Próximo Dia Útil do Início"]))
    print("Resenhas AppSheets: feriados incluídos no início e no prazo do SLA")


TROCAS_GOOGLE = [
    ("DATEDIFF('day', DATE([Data Avaliação]), TODAY())",
     "(DATEDIFF('day', DATE([Data Avaliação]), TODAY()) - [_Feriados desde a Avaliação])", 2),
    ("DATEDIFF('day', DATE([Data Atualização da Avaliação]), TODAY())",
     "(DATEDIFF('day', DATE([Data Atualização da Avaliação]), TODAY()) - [_Feriados desde a Atualização])", 2),
    ("DATEADD('day', 5, DATE([Data Avaliação]))",
     "DATEADD('day', 5 + [_Feriados até a Resposta EXP], DATE([Data Avaliação]))", 1),
]
FIM_CASE_BAIXA = re.compile(r"END, *\n( *)\[Data Avaliação\]\)")


def google(fluxo):
    anot = etapa(fluxo, "Resenhas Google > SLA Resenhas")
    if any(MARCA in (a["annotationNode"].get("expression") or "") for a in anot):
        print("Resenhas Google: feriados já estavam no fluxo")
        return
    for coluna in ("Status SLA", "Status SLA 2"):
        no = anot[posicao(anot, coluna)]["annotationNode"]
        e = no["expression"]
        for velho, novo, vezes in TROCAS_GOOGLE:
            assert e.count(velho) == vezes, f"{coluna}: '{velho}' aparece {e.count(velho)} vezes"
            e = e.replace(velho, novo)
        assert len(FIM_CASE_BAIXA.findall(e)) == 1, f"{coluna}: prazo das 1 a 3 estrelas fora do esperado"
        e = FIM_CASE_BAIXA.sub(lambda m: f"END + [_Feriados até a Resposta EXP],\n{m.group(1)}[Data Avaliação])", e)
        no["expression"] = f"{MARCA}: os feriados não contam como dias corridos.\n" + e
    i = posicao(anot, "Status SLA")
    inserir(anot, i, nova_coluna("_Feriados desde a Avaliação", feriados_entre("DATE([Data Avaliação])", "TODAY()")))
    inserir(anot, i + 1, nova_coluna("_Feriados desde a Atualização",
                                     feriados_entre("DATE([Data Atualização da Avaliação])", "TODAY()")))
    inserir(anot, i + 2, nova_coluna("_Feriados até a Resposta EXP",
                                     feriados_entre("DATE([Data Avaliação])", "DATE([Data da Resposta EXP])")))
    k = posicao(anot, "Status SLA 2")
    inserir(anot, k + 1, remover(["_Feriados desde a Avaliação", "_Feriados desde a Atualização",
                                  "_Feriados até a Resposta EXP"]))
    print("Resenhas Google: feriados descontados dos dias corridos em Status SLA e Status SLA 2")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    caminho = Path(sys.argv[1])
    partes, fluxo = ler(caminho)
    appsheets(fluxo)
    google(fluxo)
    gravar(caminho, partes, fluxo)
