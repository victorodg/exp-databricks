"""Formatos de texto usados nas planilhas do Book (padrão brasileiro)."""
from decimal import ROUND_HALF_UP, Decimal


def _br(numero, casas):
    # arredonda como a planilha (meio para cima): 90,625 -> 90,63
    numero = Decimal(str(numero)).quantize(Decimal(1).scaleb(-casas), rounding=ROUND_HALF_UP)
    texto = f"{numero:,.{casas}f}"
    return texto.replace(",", "X").replace(".", ",").replace("X", ".")


def pct(parte, total, casas=2):
    """Percentual com 2 casas ("98,85%"); "-" quando não há denominador."""
    if not total:
        return "-"
    return _br(100 * parte / total, casas) + "%"


def inteiro(n):
    return _br(n, 0)


def reais(n):
    return "R$ " + _br(n, 2)


def dias(segundos):
    """Tempo médio em dias inteiros, com dois dígitos ("04 dias"); "-" quando não há casos."""
    if segundos is None:
        return "-"
    return f"{int(segundos // 86400):02d} dias"
