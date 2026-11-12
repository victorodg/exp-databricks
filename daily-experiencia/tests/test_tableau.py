"""Testes das funções que emulam o Tableau (rodar com .venv-spark\\Scripts\\python.exe -m pytest)."""
from datetime import datetime

import pytest

pytest.importorskip("pyspark")
from pyspark.sql import functions as F  # noqa: E402

from dexp import tableau as tb  # noqa: E402
from dexp.prep import juntar  # noqa: E402


def valor(spark, expr, **colunas):
    """Datas vão como texto e são convertidas como na silver (datetime do Python seria lido no fuso do Windows)."""
    linha = spark.createDataFrame([tuple(str(v) for v in colunas.values())], list(colunas))
    for nome, v in colunas.items():
        if isinstance(v, datetime):
            linha = linha.withColumn(nome, tb.data_hora(F.col(nome)))
    return linha.select(expr.alias("r")).first()["r"]


def test_somar_86399_dias_nao_estoura(spark):
    # data + 86399 no Tableau soma dias; com inteiro de 32 bits isso virava uma data no passado
    r = valor(spark, tb.somar_dias(F.col("d"), 86399), d=datetime(2026, 1, 1))
    assert r.year > 2200


def test_diff_dias_conta_viradas_de_dia(spark):
    assert valor(spark, tb.diff_dias(F.col("a"), F.col("b")), a=datetime(2026, 1, 1, 23, 59), b=datetime(2026, 1, 2, 0, 1)) == 1


def test_diff_semanas_com_semana_comecando_no_domingo(spark):
    # sábado 03/01/2026 -> domingo 04/01/2026: uma virada de semana
    assert valor(spark, tb.diff_semanas(F.col("a"), F.col("b")), a=datetime(2026, 1, 3), b=datetime(2026, 1, 4)) == 1


def test_dia_semana_domingo_e_1(spark):
    assert valor(spark, tb.dia_semana(F.col("d")), d=datetime(2026, 1, 4)) == 1


def test_igual_ignora_maiusculas(spark):
    assert valor(spark, tb.igual(F.col("s"), "Erro Operacional"), s="erro operacional") is True


def test_excluir_mantem_nulos_e_manter_none_pega_nulos(spark):
    df = spark.createDataFrame([("a",), ("b",), (None,)], "s string")
    assert sorted(r.s or "-" for r in df.where(tb.excluir("s", "a")).collect()) == ["-", "b"]
    assert [r.s for r in df.where(tb.manter("s", None)).collect()] == [None]


def test_remapear_ignora_maiusculas_e_mantem_o_resto(spark):
    df = spark.createDataFrame([("✅ Finalizado",), ("aberta",)], "s string")
    r = [x.r for x in df.select(tb.remapear("s", {"Finalizado": ["✅ FINALIZADO"]}).alias("r")).collect()]
    assert r == ["Finalizado", "aberta"]


def test_remapear_poe_a_grafia_do_grupo_no_proprio_nome(spark):
    df = spark.createDataFrame([("Gabrielle Tenorio",), ("gabrielletenorio.sonda@natura.net",), ("Gabrielle tenorio",), (None,)], "s string")
    mapa = {"Gabrielle tenorio": ["gabrielletenorio.sonda@natura.net"], None: [""]}
    r = [x.r for x in df.select(tb.remapear("s", mapa).alias("r")).collect()]
    assert r == ["Gabrielle tenorio"] * 3 + [None]

def test_filtro_data_ate_usa_o_limite_gravado(spark):
    df = spark.createDataFrame([("2025-10-31 00:00:00",), ("2025-10-31 09:00:00",), (None,)], "d string")
    assert df.withColumn("d", tb.data_hora(F.col("d"))).where(tb.filtro_data("d", ate="2025-10-31")).count() == 1


def test_juntar_reproduz_sufixos_do_prep(spark):
    esquerda = spark.createDataFrame([("27-1", "x")], "protocolo string, chamado string")
    direita = spark.createDataFrame([("27-1", "y", "z")], "protocol string, chamado string, chamado_1 string")
    r = juntar(esquerda, direita, [("protocolo", "protocol")], "right", preservar=["chamado_1"])
    assert sorted(r.columns) == ["chamado", "chamado_1", "chamado_2", "protocol", "protocolo"]
    assert r.first()["chamado_2"] == "y"
