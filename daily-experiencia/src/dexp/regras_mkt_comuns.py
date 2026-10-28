"""Regras reaproveitadas em várias etapas do fluxo MKT (Nível, SLAs em horas úteis, conversões de tempo)."""
from pyspark.sql import functions as F

from dexp import tableau as tb
from dexp.tableau import igual

DENTRO, FORA = "Dentro do SLA", "Fora do SLA"


def nivel(coluna_status, coluna_data, regra_nova):
    """Nível N1/N2/NEUTRO: regra nova (lista de status) a partir de 2026 pela data; antes disso, a regra antiga."""
    status = F.col(coluna_status)
    nova = F.when(status.isNull(), "Não mapeado")
    for rotulo, valores in regra_nova.items():
        nova = nova.when(igual(F.trim(status), *valores), rotulo)
    nova = nova.otherwise("Não mapeado")
    antiga = (F.when(igual(status, "CHAMADO", "INCIDENTE CRÍTICO"), "N2")
               .when(igual(status, "INCIDENTE EM ANDAMENTO", "INCIDENTE RESOLVIDO"), "NEUTRO")
               .otherwise("N1"))
    return F.when(F.year(coluna_data) >= 2026, nova).otherwise(antiga)


def segundos_hms(coluna):
    """INT(SPLIT(x, ":", 1)) * 3600 + INT(SPLIT(x, ":", 2)) * 60 + INT(SPLIT(x, ":", 3))."""
    parte = lambda i: f"try_cast(try_cast(try_element_at(split(`{coluna}`, ':'), {i}) AS DOUBLE) AS BIGINT)"
    return F.expr(f"{parte(1)} * 3600 + {parte(2)} * 60 + {parte(3)}")


def tempo_formatado(coluna):
    """RIGHT('0' + STR(INT(t / 3600)), 2) + ':' + ... — acima de 99 horas o Tableau corta a hora em 2 dígitos."""
    t = f"`{coluna}`"
    dois = lambda e: f"right(concat('0', cast(cast({e} AS BIGINT) AS STRING)), 2)"
    return F.expr(f"concat({dois(f'{t} / 3600')}, ':', {dois(f'({t} % 3600) / 60')}, ':', {dois(f'{t} % 60')})")


def mes_ano(coluna):
    """RIGHT("0" + STR(MONTH(d)), 2) + "/" + STR(YEAR(d)) -> '03/2026'."""
    d = F.col(coluna)
    return F.when(d.isNotNull(), F.format_string("%02d/%d", F.month(d), F.year(d)))


def para_horario_util(coluna):
    """Domingo -> segunda 08:00; sábado -> segunda 08:00; antes das 08:00 -> 08:00 do mesmo dia."""
    c = F.col(coluna)
    dia = tb.dia_semana(c)
    return (F.when(dia == 1, tb.fazer_data_hora(tb.somar_dias(c, 1), 8))
             .when(dia == 7, tb.fazer_data_hora(tb.somar_dias(c, 2), 8))
             .when(F.hour(c) < 8, tb.fazer_data_hora(c, 8))
             .otherwise(c))


def segundos_uteis(inicio, fim):
    """Mesmo dia: diferença simples. Dias diferentes: dias inteiros do meio (menos fins de semana aproximados) x 16 h,
    mais o resto do primeiro dia até 24:00 e o último dia a partir das 08:00."""
    ini, fi = F.col(inicio), F.col(fim)
    dia_ini, dia_fim = F.date_trunc("day", ini), F.date_trunc("day", fi)
    meio = tb.diff_dias(tb.somar_dias(dia_ini, 1), dia_fim)
    return (F.when(dia_ini == dia_fim, tb.diff_segundos(ini, fi))
             .otherwise((meio - F.floor(meio / 7) * 2) * 57600
                        + tb.diff_segundos(ini, tb.fazer_data_hora(tb.somar_dias(ini, 1), 0))
                        + tb.diff_segundos(tb.fazer_data_hora(fi, 8), fi)))


def sla(coluna, limite):
    return F.when(F.col(coluna) <= limite, DENTRO).otherwise(FORA)
