"""Compara um extract do Tableau (.tdsx ou .hyper) com uma tabela gold no Databricks.

Para cada coluna em comum mostra, dos dois lados: preenchidos, distintos, mínimo e máximo. Para colunas de categoria
(até 40 valores distintos) compara também a contagem de cada valor. As colunas do extract são casadas com as da gold
pelo nome normalizado (snake_case sem acento) e pelos apelidos em APELIDOS.

Uso (a partir da pasta daily-experiencia):
  .venv\\Scripts\\python.exe ferramentas\\comparar_extract.py validacao\\extracts\\Dynamics_Nivel.tdsx dexp_gold_dynamics_nivel
"""
import glob
import os
import sys
import tempfile
import zipfile
from pathlib import Path

from databricks.sdk import WorkspaceClient
from databricks.sdk.core import Config
from tableauhyperapi import Connection, HyperProcess, Telemetry, TableName

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from dexp.leitura import normalizar_colunas  # noqa: E402

PERFIL = "daily-exp"
WAREHOUSE = "dcb43c45e3a55fe4"
ESQUEMA = "sandbox.sustentacao_bau_experiencias"
MAX_CATEGORIAS = 40

# nome normalizado da coluna no extract -> nome na gold, quando a gold usa um nome mais curto
APELIDOS = {
    "numero_da_ocorrencia_referente_ocorrencia": "numero_da_ocorrencia",
    "primeira_categoria_referente_ocorrencia": "primeira_categoria",
    "segunda_categoria_referente_ocorrencia": "segunda_categoria",
    "motivo_referente_ocorrencia": "motivo",
    "central_de_atendimento_referente_ocorrencia": "central_de_atendimento",
    "codigo_natura_cliente_contato": "codigo_natura",
    "numero_do_documento_cliente_contato": "numero_do_documento",
    "nao_modificar_tarefa": "tarefa_id",
    "nao_modificar_soma_de_verificacao_da_linha": "soma_de_verificacao",
    "nao_modificar_data_de_modificacao": "data_de_modificacao",
    "usuario_que_realizou_alteracao_nome_completo": "usuario_que_realizou_alteracao",
    "modificado_pela_ultima_vez_por_nome_completo": "modificado_pela_ultima_vez_por",
    "sla_5_horas_old": "sla_5_horas_old",
    "sla_experiencia_old": "sla_experiencia_old",
    "dia_da_semana_criacao": "_dia_da_semana_criacao",
    "dia_da_semana_termino": "_dia_da_semana_termino",
    "data_fim_referencia": "_data_fim_referencia",
    "inicio_util": "_inicio_util",
    "termino_util": "_termino_util",
    "dia_da_semana_da_resposta": "_dia_da_semana_da_resposta",
    "hora_da_resposta": "_hora_da_resposta",
    "grupo_de_atribuicao_no_service_now": "grupo_de_atribuicao_tribos",
    "nomenclatura_para_criar_aba_no_service_now": "nomenclatura_aba",
    "nomenclatura_para_criar_aba_no_service_now_1": "nomenclatura_aba_2",
    "de_tempo_de_neg_decorrido": "perc_tempo_de_negocio_decorrido",
    "anotacoes_de_resolucao": "anotacoes_de_resolucao",
    "ultima_reabertura_em": "ultima_reabertura_em",
    "id_rechamada_1": "id_rechamada_1",
    "numero_da_ocorrencia_limpo": "numero_da_ocorrencia",
}


# Quando duas colunas do extract só diferem em maiúsculas ("MERCADO" e "Mercado"), elas viram o mesmo nome em
# snake_case; estas têm nome próprio na gold.
NOMES_EM_COLISAO = {
    "Mercado": "mercado_re",
    "SETOR": "setor_reativos",
    "PEDIDO FINALIZADO": "pedido_finalizado_ticket",
    "Hora Fim do Atendimento": "hora_fim_do_atendimento_ate_julho",
    "Erro Perceptível ao Usuário?": "erro_perceptivel_ao_usuario_ate_julho",
}


def casar_colunas(colunas_ext, colunas_gold):
    """Para cada coluna do extract, a coluna da gold correspondente (ou None se não houver)."""
    # nome normalizado sem o sufixo de desempate (_2) que normalizar_colunas põe nas repetidas
    normalizadas = [normalizar_colunas([c])[0] for c in colunas_ext]
    repetidas = {n for n in normalizadas if normalizadas.count(n) > 1}
    alvos = [NOMES_EM_COLISAO.get(o, APELIDOS.get(n, n)) if n in repetidas else APELIDOS.get(n, n)
             for o, n in zip(colunas_ext, normalizadas)]
    return [a if a in colunas_gold else None for a in alvos]


def cliente():
    cli = glob.glob(os.path.expandvars(r"%LOCALAPPDATA%\Microsoft\WinGet\Packages\Databricks.DatabricksCLI_*\databricks.exe"))
    return WorkspaceClient(config=Config(profile=PERFIL, databricks_cli_path=cli[0] if cli else None))


def sql_databricks(w, consulta):
    r = w.statement_execution.execute_statement(statement=consulta, warehouse_id=WAREHOUSE, wait_timeout="50s")
    while r.status.state.value in ("PENDING", "RUNNING"):
        r = w.statement_execution.get_statement(r.statement_id)
    if r.status.state.value != "SUCCEEDED":
        raise RuntimeError(r.status.error.message)
    linhas = r.result.data_array or []
    while r.result.next_chunk_index:
        r.result = w.statement_execution.get_statement_result_chunk_n(r.statement_id, r.result.next_chunk_index)
        linhas += r.result.data_array or []
    return linhas


def arquivo_hyper(caminho, pasta_temp):
    if caminho.suffix.lower() == ".hyper":
        return caminho
    with zipfile.ZipFile(caminho) as z:
        nome = next(n for n in z.namelist() if n.lower().endswith(".hyper"))
        return Path(z.extract(nome, pasta_temp))


def texto(v):
    """Valor como texto comparável entre os dois lados (1.0 == 1, datas sem fração)."""
    if v is None:
        return None
    s = str(v)
    try:
        f = float(s)
        return str(int(f)) if f.is_integer() else f"{f:.6f}".rstrip("0")
    except ValueError:
        return s[:19] if len(s) >= 19 and s[4] == "-" and s[10] in " Tt" else s


def perfil_sql(colunas, tabela, citar, textos=()):
    """No extract, textos são comparados sem diferenciar maiúsculas (collation do Tableau); na gold, usa lower()."""
    hyper = citar is citar_hyper
    partes = ["count(*)"]
    for c in colunas:
        q = citar(c)
        if c in textos and not hyper:
            v = f"lower({q})"
        else:
            v = f"CAST({q} AS {'TEXT' if hyper else 'STRING'})"
        partes += [f"count({q})", f"count(DISTINCT {v})", f"min({v})", f"max({v})"]
    return f"SELECT {', '.join(partes)} FROM {tabela}"


def citar_hyper(c):
    return '"' + c.replace('"', '""') + '"'


def citar_spark(c):
    return f"`{c}`"


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    origem, tabela_gold = Path(sys.argv[1]), sys.argv[2]
    w = cliente()
    colunas_gold = [r[0] for r in sql_databricks(w, f"SHOW COLUMNS IN {ESQUEMA}.{tabela_gold}")]

    with tempfile.TemporaryDirectory() as pasta, HyperProcess(Telemetry.DO_NOT_SEND_USAGE_DATA_TO_TABLEAU) as hyper:
        with Connection(hyper.endpoint, str(arquivo_hyper(origem, pasta))) as con:
            tabelas = [t for s in con.catalog.get_schema_names() for t in con.catalog.get_table_names(s)]
            tabela_ext = max(tabelas, key=lambda t: con.execute_scalar_query(f"SELECT count(*) FROM {t}"))
            colunas_ext = [str(c.name.unescaped) for c in con.catalog.get_table_definition(tabela_ext).columns]

            alvos = casar_colunas(colunas_ext, colunas_gold)
            pares = [(o, a) for o, a in zip(colunas_ext, alvos) if a]
            so_extract = [o for o, a in zip(colunas_ext, alvos) if not a]
            so_gold = [g for g in colunas_gold if g not in {a for _, a in pares}]

            definicao = {str(c.name.unescaped): str(c.type).lower() for c in con.catalog.get_table_definition(tabela_ext).columns}
            textos_gold = {a for o, a in pares if definicao[o] == "text"}
            ext = con.execute_list_query(perfil_sql([o for o, _ in pares], tabela_ext, citar_hyper))[0]
            gold = sql_databricks(w, perfil_sql([a for _, a in pares], f"{ESQUEMA}.{tabela_gold}", citar_spark, textos_gold))[0]

            print(f"# {origem.name}  x  {tabela_gold}\n")
            print(f"Linhas: extract {int(ext[0]):,} | gold {int(gold[0]):,} | diferença {int(gold[0]) - int(ext[0]):+,}\n")
            print("| coluna (extract) | preenchidos ext/gold | distintos ext/gold | mínimo ext / gold | máximo ext / gold |")
            print("|---|---|---|---|---|")
            categorias = []
            for i, (original, alvo) in enumerate(pares):
                e = ext[1 + 4 * i: 5 + 4 * i]
                g = gold[1 + 4 * i: 5 + 4 * i]
                eh_texto = alvo in textos_gold
                comparar = (lambda v: (texto(v) or "").lower()) if eh_texto else texto
                iguais = [str(int(e[0])) == str(g[0]), str(int(e[1])) == str(g[1]),
                          comparar(e[2]) == comparar(g[2]), comparar(e[3]) == comparar(g[3])]
                marca = "" if all(iguais) else " ⚠️"
                curto = lambda v: (texto(v) or "")[:60].replace("\n", " ").replace("|", "/")
                print(f"| {original}{marca} | {int(e[0]):,} / {int(g[0]):,} | {int(e[1]):,} / {int(g[1]):,} | "
                      f"{curto(e[2])} / {curto(g[2])} | {curto(e[3])} / {curto(g[3])} |")
                if 0 < int(e[1]) <= MAX_CATEGORIAS:
                    categorias.append((original, alvo))
            print(f"\nSó no extract: {so_extract}\nSó na gold: {so_gold}\n")

            for original, alvo in categorias:
                # o extract guarda uma grafia só para textos iguais sem diferenciar maiúsculas; compara em minúsculas
                q = citar_hyper(original)
                chave = (lambda v: None if v is None else texto(v).lower()) if alvo in textos_gold else texto
                cont_ext, cont_gold = {}, {}
                for v, n in con.execute_list_query(f"SELECT CAST({q} AS TEXT), count(*) FROM {tabela_ext} GROUP BY 1"):
                    cont_ext[chave(v)] = cont_ext.get(chave(v), 0) + int(n)
                for v, n in sql_databricks(w, f"SELECT CAST(`{alvo}` AS STRING), count(*) FROM {ESQUEMA}.{tabela_gold} GROUP BY 1"):
                    cont_gold[chave(v)] = cont_gold.get(chave(v), 0) + int(n)
                difs = {k: (cont_ext.get(k, 0), cont_gold.get(k, 0)) for k in set(cont_ext) | set(cont_gold)
                        if cont_ext.get(k, 0) != cont_gold.get(k, 0)}
                if difs:
                    print(f"## {original}: valores com contagem diferente (extract, gold)")
                    for k, (a, b) in sorted(difs.items(), key=lambda kv: -abs(kv[1][0] - kv[1][1]))[:15]:
                        print(f"- {k!r}: {a:,} vs {b:,} ({b - a:+,})")
                    print()


if __name__ == "__main__":
    main()
