"""Gera as views dexp_vw_* com os nomes e tipos de campo dos extracts do Tableau, para o workbook trocar a fonte
publicada pelo Databricks sem quebrar os campos.

Cada view tem as colunas do extract, na mesma ordem, lidas da tabela gold correspondente (casadas como em
comparar_extract.py). Colunas que o extract tem e a gold não (ex.: "Table Names" do Prep) entram como NULL, para o
workbook não ficar com campo faltando. Quando o tipo da gold difere do extract (fora int/bigint, que para o Tableau
são o mesmo), a coluna é convertida para o tipo do extract. O Databricks não aceita duas colunas que só diferem em maiúsculas ("SETOR" e "Setor"); a segunda recebe " (2)"
no nome, e o workbook precisa apontar para ela.

Grava o SQL em src/views/views_tableau.sql. Com --aplicar, cria as views no SQL Warehouse.

Uso (a partir da pasta daily-experiencia):
  .venv\\Scripts\\python.exe ferramentas\\gerar_views_tableau.py [--aplicar]
"""
import sys
import tempfile
from pathlib import Path

from tableauhyperapi import Connection, HyperProcess, Telemetry

sys.path.insert(0, str(Path(__file__).resolve().parent))
from comparar_extract import ESQUEMA, arquivo_hyper, casar_colunas, cliente, sql_databricks  # noqa: E402

RAIZ = Path(__file__).resolve().parents[1]
EXTRACTS = RAIZ / "validacao" / "extracts"
SAIDA = RAIZ / "src" / "views" / "views_tableau.sql"

# extract (.tdsx em validacao/extracts) -> tabela gold; a view se chama dexp_vw_<tabela sem o prefixo dexp_gold_>
SAIDAS = {
    "Dynamics - Termino Real": "dexp_gold_dynamics_tarefas",
    "Dynamics Nivel": "dexp_gold_dynamics_nivel",
    "Dynamics - Base para Rechamada": "dexp_gold_dynamics_rechamada",
    "EXPBR - Chamados Servicenow": "dexp_gold_servicenow_chamados",
    "Resenhas EXP BR AppSheets": "dexp_gold_resenhas_appsheets",
    "Resenhas Brasil": "dexp_gold_resenhas_brasil",
    "Experiencia Brasil Nivel": "dexp_gold_mkt_experiencia_brasil_nivel",
    "Ticket Medio Exp Br": "dexp_gold_mkt_ticket_medio",
    "MKT BRASIL - WhatsApp": "dexp_gold_mkt_brasil_whatsapp",
    "MKT Whats GN": "dexp_gold_mkt_whats_gn",
    "MKT Brasil Completo": "dexp_gold_mkt_brasil_completo",
    "MKT BRASIL - Email": "dexp_gold_mkt_brasil_email",
    "Exp Brasil Dynatrace": "dexp_gold_mkt_exp_brasil_dynatrace",
    "MKT Emails de Lojas": "dexp_gold_mkt_emails_de_lojas",
    "MKT Email Experiencia CB": "dexp_gold_mkt_email_experiencia_cb",
    "MKT Brasil Completo Nivel": "dexp_gold_mkt_brasil_completo_nivel",
    "MKT - CBCOM": "dexp_gold_mkt_cbcom",
    "MKT Whats GV": "dexp_gold_mkt_whats_gv",
    "Requisição Eventual EXP BR": "dexp_gold_mkt_requisicao_eventual",
    "MKT Whats GV Antecipada(1)": "dexp_gold_mkt_whats_gv_antecipada",
    "MKT Whats Franquia": "dexp_gold_mkt_whats_franquia",
    "Histórico Backlog Diário": "dexp_gold_mkt_historico_backlog_diario",
    "MKT Brasil Backlog": "dexp_gold_mkt_brasil_backlog",
    "HC Exp Brasil": "dexp_gold_mkt_hc_exp_brasil",
}

# tipo do Hyper -> tipo do Databricks
TIPOS = {"TEXT": "STRING", "BIG_INT": "BIGINT", "INT": "INT", "SMALL_INT": "INT", "DOUBLE": "DOUBLE",
         "DATE": "DATE", "TIMESTAMP": "TIMESTAMP", "BOOL": "BOOLEAN"}


def tipo_databricks(tipo_hyper):
    t = str(tipo_hyper).upper()
    if t.startswith("NUMERIC"):
        return t.replace("NUMERIC", "DECIMAL")
    return TIPOS[t]


def colunas_extract(hyper, caminho, pasta):
    with Connection(hyper.endpoint, str(arquivo_hyper(caminho, pasta))) as con:
        tabelas = [t for s in con.catalog.get_schema_names() for t in con.catalog.get_table_names(s)]
        tabela = max(tabelas, key=lambda t: con.execute_scalar_query(f"SELECT count(*) FROM {t}"))
        return [(str(c.name.unescaped), tipo_databricks(c.type)) for c in con.catalog.get_table_definition(tabela).columns]


def definicao_view(extract, gold, colunas, tipos_gold):
    view = "dexp_vw_" + gold.removeprefix("dexp_gold_")
    alvos = casar_colunas([n for n, _ in colunas], list(tipos_gold))
    usados, linhas, avisos = set(), [], []
    for (nome, tipo), alvo in zip(colunas, alvos):
        apelido = nome if nome.lower() not in usados else f"{nome} (2)"
        usados.add(apelido.lower())
        if apelido != nome:
            avisos.append(f"`{nome}` virou `{apelido}` (já existe com outra grafia)")
        if alvo is None:
            expressao = f"CAST(NULL AS {tipo})"
            avisos.append(f"`{nome}` não existe na gold: fica NULL")
        elif tipos_gold[alvo] != tipo.lower() and {tipos_gold[alvo], tipo.lower()} != {"int", "bigint"}:
            expressao = f"CAST(`{alvo}` AS {tipo})"
            avisos.append(f"`{nome}`: {tipos_gold[alvo]} na gold, convertido para {tipo.lower()}")
        else:
            expressao = f"`{alvo}`"
        linhas.append(f"  {expressao} AS `{apelido.replace('`', '``')}`")
    sql = (f"-- {extract}\nCREATE OR REPLACE VIEW {ESQUEMA}.{view}\n"
           f"COMMENT 'Daily Experiência BR: {gold} com os nomes de campo do extract \"{extract}\" (para o Tableau)'\nAS SELECT\n"
           + ",\n".join(linhas) + f"\nFROM {ESQUEMA}.{gold}")
    return view, sql, avisos


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    aplicar = "--aplicar" in sys.argv
    w = cliente()
    blocos = []
    with tempfile.TemporaryDirectory() as pasta, HyperProcess(Telemetry.DO_NOT_SEND_USAGE_DATA_TO_TABLEAU) as hyper:
        for extract, gold in SAIDAS.items():
            colunas = colunas_extract(hyper, EXTRACTS / f"{extract}.tdsx", pasta)
            tipos_gold = {r[0]: r[1].lower() for r in sql_databricks(w, f"DESCRIBE TABLE {ESQUEMA}.{gold}")
                          if r[0] and not r[0].startswith("#")}
            view, sql, avisos = definicao_view(extract, gold, colunas, tipos_gold)
            blocos.append(sql)
            print(f"{view}: {len(colunas)} colunas")
            for a in avisos:
                print(f"  - {a}")
            if aplicar:
                sql_databricks(w, sql)

    SAIDA.parent.mkdir(exist_ok=True)
    SAIDA.write_text("-- Gerado por ferramentas/gerar_views_tableau.py; não editar à mão.\n\n"
                     + ";\n\n".join(blocos) + ";\n", encoding="utf-8")
    print(f"\nSQL em {SAIDA.relative_to(RAIZ)}" + ("; views criadas." if aplicar else " (sem --aplicar, nada foi criado)."))


if __name__ == "__main__":
    main()
