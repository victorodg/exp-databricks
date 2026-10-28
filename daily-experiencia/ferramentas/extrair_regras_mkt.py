"""Extrai do fluxo MKT do Tableau Prep as listas e mapeamentos grandes usados na gold e grava src/dexp/regras_mkt.py.

Copiar essas listas à mão seria fácil de errar; aqui elas saem exatamente como estão no fluxo.
Uso: python ferramentas\\extrair_regras_mkt.py "<Daily - Experiencia BR - MKT.tfl>"
"""
import json
import pprint
import re
import sys
import zipfile
from pathlib import Path

DESTINO = Path(__file__).resolve().parents[1] / "src" / "dexp" / "regras_mkt.py"


def nos_por_nome(fluxo):
    nos = {}
    for no in fluxo["nodes"].values():
        nos.setdefault(no["name"], []).append(no)
    return nos


def acoes(no):
    if "loomContainer" in no:
        return list(no["loomContainer"]["nodes"].values())
    return [a["annotationNode"] for a in no.get("beforeActionAnnotations", []) + no.get("afterActionAnnotations", [])]


def acao(nos, etapa, tipo, coluna=None, indice=0):
    candidatas = [a for no in nos[etapa] for a in acoes(no)
                  if a["nodeType"].endswith(tipo) and (coluna is None or a.get("columnName") == coluna)]
    return candidatas[indice]


def valor(texto):
    v = json.loads(texto) if texto != "null" else None
    return v


def remap(a):
    return {valor(novo): [valor(v) for v in antigos if valor(v) != valor(novo)] for novo, antigos in a["values"].items()}


def protocolos(expressao):
    return re.findall(r"\[Protocolo?\] = '([^']+)'", expressao)


def niveis(expressao):
    """Lê 'UPPER(TRIM([x])) == "VALOR" THEN "N1"' da regra nova de Nível."""
    pares = re.findall(r'==\s*"([^"]+)"\s*THEN\s*"([^"]+)"', expressao.split("ELSE\n    // --- INÍCIO DA REGRA ANTIGA")[0])
    saida = {}
    for status, nivel in pares:
        saida.setdefault(nivel, []).append(status)
    return saida


def main():
    fluxo = json.loads(zipfile.ZipFile(sys.argv[1]).read("flow"))
    nos = nos_por_nome(fluxo)
    regras = {
        "FUNCAO_MACRO": remap(acao(nos, "Limpar 18", "Remap", "Função do Sistema-1")),
        "PROTOCOLOS_REMOVIDOS_16_01_26": protocolos(acao(nos, "Remover protocolos de 16/01/26", "AddColumn", "Remover")["expression"]),
        "PROTOCOLOS_RESOLVIDO_N3_MKT": protocolos(acao(nos, "Expurgo Solicitado", "AddColumn", "Status")["expression"]),
        "STATUS_FINALIZACAO_EXCLUIDOS": [valor(v) for a in acoes(nos["Alterações Comuns MKT"][0])
                                         if a["nodeType"].endswith("RichDiscreteValueFilter")
                                         for v in a["values"].get("Status de finalização", [])],
        "QTD_ATENDIMENTOS_PARA_1": [valor(v) for v in acao(nos, "Alterações Comuns MKT", "Remap", "Qtd Atendimentos")["values"]["1"]],
        "NIVEL_REGRA_NOVA_COMPLETA": niveis(acao(nos, "Nivel", "AddColumn", "Nivel")["expression"]),
        "NIVEL_REGRA_NOVA_WHATSAPP": niveis(acao(nos, "SLA Primeiro Contato e Nivel", "AddColumn", "Nível")["expression"]),
        "NOME_RESPONSAVEL": dict(re.findall(r'WHEN\s*"([^"]+)"\s*THEN\s*"([^"]+)"',
                                            acao(nos, "Responsavel", "AddColumn", "Nome Responsavel")["expression"])),
        "RESPONSAVEL_ACIONAMENTO": remap(next(a for no in nos["Responsavel"] for a in acoes(no)
                                              if a["nodeType"].endswith("Remap") and "adrianaoliveira.sonda@natura.net" in str(a["values"])
                                              and '"Adriana Conceicao De Oliveira"' in a["values"])),
        "RESPONSAVEL_ANALISTAS": remap(next(a for no in nos["Responsavel"] for a in acoes(no)
                                            if a["nodeType"].endswith("Remap") and '"Adriana Conceição"' in a["values"])),
        "RESPONSAVEL_FINAL": remap(acao(nos, "Limpar 27", "Remap", "Responsavel")),
    }
    # garantias: a regra da página do Completo e a do WhatsApp diferem só nos 4 status "ENCERRADO PELO EXPCB"
    assert set(regras["NIVEL_REGRA_NOVA_COMPLETA"]) == {"N1", "N2", "NEUTRO", "NÃO CONSIDERAR"}
    linhas = ['"""Listas e mapeamentos do fluxo Tableau Prep "Daily - Experiencia BR - MKT".',
              "", "Gerado por ferramentas/extrair_regras_mkt.py a partir do .tfl; não editar à mão.", '"""', ""]
    for nome, conteudo in regras.items():
        linhas.append(f"{nome} = {pprint.pformat(conteudo, width=120, sort_dicts=False)}")
        linhas.append("")
    DESTINO.write_text("\n".join(linhas), encoding="utf-8")
    for nome, conteudo in regras.items():
        print(f"{nome}: {len(conteudo)} itens")


if __name__ == "__main__":
    main()
