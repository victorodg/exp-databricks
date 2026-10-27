"""Equivalentes em PySpark das funções e comportamentos do Tableau Prep usados nos fluxos.

Premissas (confirmar na validação contra os extracts atuais):
- A sessão Spark roda em UTC (ver `preparar_sessao`): os horários das planilhas são "de parede", sem fuso, como no Prep.
- Comparações de texto ignoram maiúsculas/minúsculas, mas não acentos: o Prep usa a collation LPT_RBR_S2
  (português do Brasil, força 2). Vale para "=", filtros por valor, remapeamentos e joins.
- DATEPART('weekday'): domingo = 1 ... sábado = 7; DATEDIFF('week') conta semanas que começam no domingo.
- NOW()/TODAY() usam o relógio de FUSO_AGORA.
"""
from pyspark.sql import Column
from pyspark.sql import functions as F

FUSO_AGORA = "America/Sao_Paulo"
SEGUNDOS_DIA = 86400
_COM_ACENTO = "áàâãäéèêëíìîïóòôõöúùûüçñ"
_SEM_ACENTO = "aaaaaeeeeiiiiooooouuuucn"


def preparar_sessao(spark):
    spark.conf.set("spark.sql.session.timeZone", "UTC")


# --- leitura dos textos da bronze -------------------------------------------------------------------------

def data_hora(c) -> Column:
    """Texto 'AAAA-MM-DD HH:MM:SS' (ou só a data) da bronze -> timestamp."""
    c = F.col(c) if isinstance(c, str) else c
    return F.coalesce(F.try_to_timestamp(c, F.lit("yyyy-MM-dd HH:mm:ss")), F.try_to_timestamp(c, F.lit("yyyy-MM-dd")))


def data(c) -> Column:
    return F.to_date(data_hora(c))


def inteiro(nome) -> Column:
    return F.expr(f"try_cast(try_cast(`{nome}` AS DOUBLE) AS BIGINT)")


# --- texto ------------------------------------------------------------------------------------------------

def _valores(valores):
    return [v.lower() for v in valores if v is not None]


def igual(c, *valores) -> Column:
    """[c] = "a" OR [c] = "b", ignorando maiúsculas. Nulo continua nulo (vira falso num IF)."""
    c = F.col(c) if isinstance(c, str) else c
    return F.lower(c).isin(_valores(valores))


def manter(c, *valores) -> Column:
    """Filtro 'Manter só' do Prep. None na lista mantém os nulos."""
    c = F.col(c) if isinstance(c, str) else c
    cond = F.coalesce(igual(c, *valores), F.lit(False))
    return cond | c.isNull() if None in valores else cond


def excluir(c, *valores) -> Column:
    """Filtro 'Excluir' do Prep: tira só os valores listados; nulos ficam."""
    return ~F.coalesce(igual(c, *valores), F.lit(False))


def remapear(c, mapa) -> Column:
    """Remapear do Prep: {novo: [antigos]}; valores fora do mapa ficam como estão."""
    c = F.col(c) if isinstance(c, str) else c
    expr = None
    for novo, antigos in mapa.items():
        cond = igual(c, *antigos)
        expr = F.when(cond, F.lit(novo)) if expr is None else expr.when(cond, F.lit(novo))
    return expr.otherwise(c)


def chave_ordem_texto(c) -> Column:
    """Ordem aproximada da collation do Prep: sem acento e minúsculo primeiro, depois com acento."""
    minusculo = F.lower(c)
    return F.concat(F.translate(minusculo, _COM_ACENTO, _SEM_ACENTO), F.lit("\u0000"), minusculo)


def minimo_texto(c) -> Column:
    c = F.col(c) if isinstance(c, str) else c
    return F.min_by(c, chave_ordem_texto(c))


def maximo_texto(c) -> Column:
    c = F.col(c) if isinstance(c, str) else c
    return F.max_by(c, chave_ordem_texto(c))


def chave_join(c) -> Column:
    return F.lower(F.col(c) if isinstance(c, str) else c)


# --- datas ------------------------------------------------------------------------------------------------

def agora() -> Column:
    return F.from_utc_timestamp(F.current_timestamp(), FUSO_AGORA)


def hoje() -> Column:
    return F.to_date(agora())


def dia_semana(c) -> Column:
    """DATEPART('weekday'): domingo = 1 ... sábado = 7."""
    return F.dayofweek(c)


def fazer_data_hora(dia, h, m=0, s=0) -> Column:
    """MAKEDATETIME(DATE(dia), MAKETIME(h, m, s))."""
    return F.to_timestamp(F.concat(F.date_format(dia, "yyyy-MM-dd"), F.lit(f" {h:02d}:{m:02d}:{s:02d}")))


def somar_dias(c, dias) -> Column:
    """DATEADD('day', dias, c) mantendo o horário (dias pode ser coluna). A conta é em 64 bits: com inteiro de
    32 bits, somas grandes como os 86.399 dias da fórmula de Resenhas Brasil estouram e viram datas no passado."""
    dias = dias if isinstance(dias, Column) else F.lit(dias)
    return (c.cast("long") + dias.cast("long") * SEGUNDOS_DIA).cast("timestamp")


def diff_dias(inicio, fim) -> Column:
    """DATEDIFF('day', inicio, fim): viradas de dia, não blocos de 24 h."""
    return F.datediff(F.to_date(fim), F.to_date(inicio))


def diff_segundos(inicio, fim) -> Column:
    return fim.cast("long") - inicio.cast("long")


def _inicio_semana(c) -> Column:
    return F.date_sub(F.to_date(c), F.dayofweek(c) - 1)


def diff_semanas(inicio, fim) -> Column:
    """DATEDIFF('week', inicio, fim) com semanas começando no domingo."""
    return (F.datediff(_inicio_semana(fim), _inicio_semana(inicio)) / 7).cast("int")


def filtro_data(c, de=None, ate=None) -> Column:
    """Filtro de data do Prep (sem nulos). Os limites são os valores gravados no fluxo (AAAA-MM-DD 00:00:00):
    'a partir de' usa só `de`, 'até' usa só `ate`, 'intervalo' usa os dois, todos inclusivos."""
    c = F.col(c) if isinstance(c, str) else c
    cond = c.isNotNull()
    if de:
        cond = cond & (c >= F.to_timestamp(F.lit(de)))
    if ate:
        cond = cond & (c <= F.to_timestamp(F.lit(ate)))
    return cond
