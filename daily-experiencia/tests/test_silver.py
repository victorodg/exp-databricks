"""Testes da preparação da silver (rodar com .venv-spark\\Scripts\\python.exe -m pytest)."""
import pytest

pytest.importorskip("pyspark")

from dexp.silver import sem_linhas_vazias  # noqa: E402


def test_tira_linha_com_valor_so_em_coluna_sem_cabecalho(spark):
    df = spark.createDataFrame(
        [("INC1", None, None, "1"), (None, None, "PRB0044013", "2"), (None, "x", None, "3"), (None, None, None, "4")],
        "number string, state string, coluna_31 string, _linha string")
    assert [r["_linha"] for r in sem_linhas_vazias(df).collect()] == ["1", "3"]
