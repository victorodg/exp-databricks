from datetime import datetime, time, timedelta
from pathlib import Path

import openpyxl
import pytest

from dexp.leitura import ler_csv_mktzap, ler_excel, normalizar_colunas, valor_texto

BRUTOS_LOCAIS = Path(r"C:\Users\vyoitio\OneDrive - Sonda S.A\Documentos\logic\mktzap\downloads_brutos")


def test_normalizar_colunas():
    nomes = ["Data/Hora de abertura", "Etapa", "Etapa", "", "Responsável", "ResponsÃ¡vel", "1º Contato", "etapa_2"]
    assert normalizar_colunas(nomes) == [
        "data_hora_de_abertura", "etapa", "etapa_2", "coluna_4", "responsavel", "responsavel_2", "c_1o_contato", "etapa_2_2",
    ]


@pytest.mark.parametrize("valor, esperado", [
    (None, None),
    ("", None),
    ("00104893", "00104893"),
    (277.0, "277"),
    (0.25, "0.25"),
    (True, "true"),
    (datetime(2026, 10, 1, 8, 46, 59, 999_800), "2026-10-01 08:47:00"),
    (timedelta(hours=26, minutes=3, seconds=4), "26:03:04"),
    (time(0, 35, 30), "0:35:30"),
])
def test_valor_texto(valor, esperado):
    assert valor_texto(valor) == esperado


def test_csv_mktzap_pula_titulo_e_mantem_texto(tmp_path):
    arquivo = tmp_path / "bruto.csv"
    arquivo.write_text(
        "Relatório;01/10/2026;31/10/2026\n"
        "Protocolo;Nome;Responsável;\n"
        '27-1;"Gest&#227;o ExpCB";Ana;extra\n'
        '27-2;"Linha\nquebrada";;\n',
        encoding="utf-8",
    )
    tabela = ler_csv_mktzap(arquivo)
    assert tabela.colunas_originais == ["Protocolo", "Nome", "Responsável", ""]
    assert tabela.linhas == [["27-1", "Gest&#227;o ExpCB", "Ana", "extra"], ["27-2", "Linha\nquebrada", None, None]]
    assert tabela.numeros_linha == [3, 5]


def test_csv_mktzap_sem_dados_volta_vazio(tmp_path):
    arquivo = tmp_path / "bruto.csv"
    arquivo.write_text("Relatório,01/10/2026,22/10/2026\n", encoding="utf-8")
    assert ler_csv_mktzap(arquivo).colunas_originais == []


def test_excel_detecta_cabecalho_e_ignora_aba_oculta(tmp_path):
    arquivo = tmp_path / "planilha.xlsx"
    wb = openpyxl.Workbook()
    oculta = wb.active
    oculta.title = "hiddenSheet"
    oculta.sheet_state = "hidden"
    ws = wb.create_sheet("Dados")
    ws.append([])
    ws.append([])
    ws.append(["Protocolo", "Etapa", "Etapa", "Data"])
    ws.append(["27-1", "N1", None, datetime(2026, 10, 1, 8, 47)])
    ws.append([])
    ws.append([12.0, None, "N2", None])
    wb.save(arquivo)

    tabela = ler_excel(arquivo)
    assert tabela.colunas_originais == ["Protocolo", "Etapa", "Etapa", "Data"]
    assert tabela.linhas == [["27-1", "N1", None, "2026-10-01 08:47:00"], ["12", None, "N2", None]]
    assert tabela.numeros_linha == [4, 6]


def test_excel_com_erro_do_google_sheets(tmp_path):
    arquivo = tmp_path / "planilha.xlsx"
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.append(["ID", "Valor"])
    ws.append(["a1", 10])
    celula = ws.cell(row=3, column=2, value="#ERROR!")
    celula.data_type = "e"
    ws.cell(row=3, column=1, value="a2")
    wb.save(arquivo)

    tabela = ler_excel(arquivo)
    assert tabela.linhas == [["a1", "10"], ["a2", "#ERROR!"]]


def test_excel_aba_inexistente(tmp_path):
    arquivo = tmp_path / "planilha.xlsx"
    openpyxl.Workbook().save(arquivo)
    with pytest.raises(ValueError, match="não existe"):
        ler_excel(arquivo, aba="Base")


@pytest.mark.skipif(not BRUTOS_LOCAIS.exists(), reason="brutos locais do MKTZap não disponíveis")
def test_bruto_real_do_brasil():
    arquivo = max(BRUTOS_LOCAIS.glob("*/27 - Brasil/bruto_analitico_*.csv"))
    tabela = ler_csv_mktzap(arquivo)
    assert tabela.colunas_originais[0] == "Protocolo"
    assert len(tabela.linhas) > 0
    assert all(len(l) == len(tabela.colunas_originais) for l in tabela.linhas)
