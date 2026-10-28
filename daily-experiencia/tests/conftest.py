import os
import sys

import pytest


@pytest.fixture(scope="session")
def spark():
    """Spark local para testar as funções da silver/gold. Precisa do ambiente .venv-spark (Python 3.12 + PySpark 3.5);
    no .venv principal (Python 3.14) os testes que usam esta fixture são pulados."""
    pytest.importorskip("pyspark")
    if sys.version_info >= (3, 13):
        pytest.skip("PySpark 3.5 não roda em Python 3.13+: use .venv-spark")
    os.environ.setdefault("PYSPARK_PYTHON", sys.executable)
    os.environ.setdefault("PYSPARK_DRIVER_PYTHON", sys.executable)
    from pyspark.sql import SparkSession

    sessao = (SparkSession.builder.master("local[1]").config("spark.ui.enabled", "false")
              .config("spark.sql.shuffle.partitions", "1").getOrCreate())
    from dexp import tableau as tb
    tb.preparar_sessao(sessao)
    yield sessao
    sessao.stop()
