"""Leitura dos arquivos brutos (CSV do MKTZap e .xlsx) como tabelas de texto, sem interpretar valores.

Usado pela camada bronze: cada célula vira texto como estava no arquivo, e os nomes de coluna viram
snake_case sem acento (o nome original fica registrado à parte, na tabela dexp_bronze_colunas).
"""
import codecs
import csv
import io
import re
import unicodedata
from dataclasses import dataclass, field
from datetime import date, datetime, time, timedelta

import openpyxl
from python_calamine import CalamineError, CalamineWorkbook, SheetVisibleEnum

LINHAS_PROCURA_CABECALHO = 20
# A linha de cabeçalho é a primeira com pelo menos esta fração das células preenchidas da linha mais cheia
FRACAO_CABECALHO = 0.8
# Linha de cabeçalho dos relatórios do MKTZap (o export traz uma linha de título antes)
MARCAS_CABECALHO_MKTZAP = ("protocolo", "protocol", "data contato")


@dataclass
class TabelaTexto:
    colunas_originais: list[str]
    linhas: list[list[str | None]] = field(default_factory=list)  # None = célula vazia
    numeros_linha: list[int] = field(default_factory=list)        # linha de cada registro no arquivo (1 = primeira)


def normalizar_colunas(nomes):
    """'Data/Hora de abertura' -> 'data_hora_de_abertura'. Vazios viram coluna_<n>; repetidos ganham _2, _3..."""
    resultado, usados = [], set()
    for posicao, nome in enumerate(nomes, start=1):
        base = unicodedata.normalize("NFKD", str(nome or "")).encode("ascii", "ignore").decode()
        base = re.sub(r"[^0-9a-zA-Z]+", "_", base).strip("_").lower() or f"coluna_{posicao}"
        if base[0].isdigit():
            base = f"c_{base}"
        candidato, n = base, 1
        while candidato in usados:
            n += 1
            candidato = f"{base}_{n}"
        usados.add(candidato)
        resultado.append(candidato)
    return resultado


def valor_texto(valor):
    """Valor de célula do Excel como texto. Datas em ISO (2026-10-01 08:47:00), inteiros sem '.0'."""
    if valor is None or valor == "":
        return None
    if isinstance(valor, bool):
        return "true" if valor else "false"
    if isinstance(valor, float) and valor.is_integer():
        return str(int(valor))
    if isinstance(valor, datetime):
        # o Excel guarda datas como frações de dia; arredonda o resíduo de ponto flutuante para o segundo
        return (valor + timedelta(microseconds=500_000)).replace(microsecond=0).isoformat(sep=" ")
    if isinstance(valor, (date, time)):
        return valor.isoformat()
    if isinstance(valor, timedelta):
        segundos = round(valor.total_seconds())
        sinal = "-" if segundos < 0 else ""
        h, resto = divmod(abs(segundos), 3600)
        return f"{sinal}{h}:{resto // 60:02d}:{resto % 60:02d}"
    return str(valor)


def _linha_cabecalho(linhas):
    preenchidas = [sum(v is not None for v in linha) for linha in linhas[:LINHAS_PROCURA_CABECALHO]]
    maximo = max(preenchidas, default=0)
    if maximo == 0:
        return None
    return next(i for i, n in enumerate(preenchidas) if n >= FRACAO_CABECALHO * maximo)


def _montar(linhas, numeros, indice_cabecalho):
    """Cabeçalho + registros não vazios, todos com a mesma largura (a da linha mais larga)."""
    largura = max((max((i for i, v in enumerate(l) if v is not None), default=-1) + 1 for l in linhas), default=0)
    cabecalho = (linhas[indice_cabecalho] + [None] * largura)[:largura]
    tabela = TabelaTexto([c if c is not None else "" for c in cabecalho])
    for linha, numero in zip(linhas[indice_cabecalho + 1:], numeros[indice_cabecalho + 1:]):
        if any(v is not None for v in linha):
            tabela.linhas.append((linha + [None] * largura)[:largura])
            tabela.numeros_linha.append(numero)
    return tabela


def ler_excel(caminho, aba=None, linha_cabecalho=None):
    """Lê uma aba do .xlsx. aba=None usa a primeira aba visível; linha_cabecalho (1 = primeira) ou detecção."""
    with CalamineWorkbook.from_path(caminho) as wb:
        if aba is None:
            visiveis = [m.name for m in wb.sheets_metadata if m.visible == SheetVisibleEnum.Visible]
            if not visiveis:
                raise ValueError(f"{caminho}: nenhuma aba visível")
            aba = visiveis[0]
        elif aba not in wb.sheet_names:
            raise ValueError(f"{caminho}: aba {aba!r} não existe (abas: {wb.sheet_names})")
        try:
            brutas = wb.get_sheet_by_name(aba).to_python(skip_empty_area=False)
        except CalamineError:
            brutas = None
    if brutas is None:
        # O calamine (rápido) recusa erros fora do padrão do Excel, como o #ERROR! do Google Sheets;
        # o openpyxl lê a célula como o texto do erro.
        brutas = _linhas_openpyxl(caminho, aba)

    linhas = [[valor_texto(v) for v in linha] for linha in brutas]
    numeros = list(range(1, len(linhas) + 1))
    indice = linha_cabecalho - 1 if linha_cabecalho else _linha_cabecalho(linhas)
    if indice is None:
        return TabelaTexto([])
    return _montar(linhas, numeros, indice)


def _linhas_openpyxl(caminho, aba):
    wb = openpyxl.load_workbook(caminho, read_only=True, data_only=True)
    try:
        return [list(linha) for linha in wb[aba].iter_rows(values_only=True)]
    finally:
        wb.close()


def _decodificar(conteudo):
    if conteudo.startswith((codecs.BOM_UTF16_LE, codecs.BOM_UTF16_BE)):
        return conteudo.decode("utf-16")
    try:
        return conteudo.decode("utf-8-sig")
    except UnicodeDecodeError:
        return conteudo.decode("latin-1")


def ler_csv_mktzap(caminho):
    """Lê um relatório CSV do MKTZap: pula as linhas de título, detecta o separador e mantém o texto como veio
    (entidades HTML como N&#195;O ficam para a silver). Relatório sem cabeçalho (sem dados) volta vazio."""
    with open(caminho, "rb") as f:
        texto = _decodificar(f.read())
    fisicas = texto.splitlines()
    indice = next((i for i, l in enumerate(fisicas) if any(m in l.lower() for m in MARCAS_CABECALHO_MKTZAP)), None)
    if indice is None:
        if sum(bool(l.strip()) for l in fisicas) <= 1:
            return TabelaTexto([])
        raise ValueError(f"{caminho}: não achei a linha de cabeçalho (nenhuma linha com {MARCAS_CABECALHO_MKTZAP})")

    separador = max((";", ",", "\t"), key=lambda s: len(next(csv.reader([fisicas[indice]], delimiter=s))))
    leitor = csv.reader(io.StringIO("\n".join(fisicas[indice:])), delimiter=separador)
    linhas, numeros = [], []
    for registro in leitor:
        linhas.append([v if v != "" else None for v in registro])
        numeros.append(indice + leitor.line_num)
    return _montar(linhas, numeros, 0)
