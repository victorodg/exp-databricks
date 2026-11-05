"""De onde vem cada tabela bronze (dexp_bronze_<tabela>) dentro do volume dexp_landing.

As abas são as que os fluxos Tableau Prep leem (ver docs/inventario.md).
"""
from dataclasses import dataclass


@dataclass(frozen=True)
class FonteExcel:
    tabela: str
    grupo: str                          # drive | google_sheets
    fonte: str                          # pasta no volume: <grupo>/<fonte>/<AAAA-MM-DD>/<arquivo>
    aba: str | None = None              # None = primeira aba visível
    linha_cabecalho: int | None = None  # None = detectar
    opcional: bool = False              # aba que pode ainda não existir: sem ela, a tabela não é criada


@dataclass(frozen=True)
class FonteMktzap:
    tabela: str
    operacao: str                       # pasta no volume: mktzap/<operacao>/<AAAAMM>/
    relatorio: str                      # bruto_<relatorio>_<de>_a_<ate>.csv


FONTES_EXCEL = [
    # Drive compartilhado
    FonteExcel("mkt_reativos", "drive", "mkt_reativos", "Sheet1"),
    FonteExcel("mkt_reativos_historico_ate_out25", "drive", "mkt_reativos_historico_ate_out25", "Sheet1"),
    FonteExcel("mkt_brasil_completo", "drive", "mkt_brasil_completo", "Sheet1"),
    FonteExcel("tickets_brasil", "drive", "tickets_brasil", "Planilha1"),
    FonteExcel("servicenow_incidentes", "drive", "servicenow_incidentes", "incident (1)"),
    FonteExcel("salesforce_cf", "drive", "salesforce_cf", "Base"),
    FonteExcel("salesforce_cf_criados", "drive", "salesforce_cf_criados", "Base"),
    FonteExcel("salesforce_cf_encerrados", "drive", "salesforce_cf_encerrados", "Base"),
    FonteExcel("salesforce_cf_encerrados_analistas", "drive", "salesforce_cf_encerrados_analistas", "Base"),
    FonteExcel("dynamics_criados_em", "drive", "dynamics_criados_em"),
    FonteExcel("dynamics_termino_real", "drive", "dynamics_termino_real"),
    FonteExcel("app_natura", "drive", "app_natura"),
    FonteExcel("app_avon", "drive", "app_avon"),
    FonteExcel("consultoria_natura", "drive", "consultoria_natura"),
    FonteExcel("forca_de_vendas", "drive", "forca_de_vendas"),
    # Google Sheets exportadas pelo Apps Script
    FonteExcel("base_expurgo_mkt", "google_sheets", "base_expurgo_mkt", "MKT"),
    FonteExcel("expurgo_dynamics", "google_sheets", "expurgo_dynamics", "Página1"),
    # Expurgo de SLA por tarefa (aba criada em 29/10/2026, primeiro caso: INC1203571)
    FonteExcel("expurgo_dynamics_sla", "google_sheets", "expurgo_dynamics", "Expurgo SLA", opcional=True),
    FonteExcel("auxiliar_brasil", "google_sheets", "auxiliar_brasil", "Página1"),
    FonteExcel("base_mkt", "google_sheets", "base_mkt", "MKT Brasil"),
    FonteExcel("tribos_base_mkt", "google_sheets", "mapeamento_tribos", "Base_MKT_1309"),
    FonteExcel("tribos_base_dynamics", "google_sheets", "mapeamento_tribos", "Base Dynamics_1309"),
    FonteExcel("tribos_grupos_servicenow", "google_sheets", "mapeamento_tribos", "Base_GruposServiceNow_2209"),
    FonteExcel("monitoracao_dynatrace", "google_sheets", "monitoracao_dynatrace", "Página1"),
    FonteExcel("registros_ate_julho_dynatrace", "google_sheets", "registros_ate_julho_dynatrace", "Página1"),
    FonteExcel("appsheets_registros_experiencia_cb", "google_sheets", "appsheets_registros_experiencia_cb", "Registro"),
    FonteExcel("registros_de_acionamentos", "google_sheets", "registros_de_acionamentos", "Página1"),
    FonteExcel("ticket_medio", "google_sheets", "ticket_medio", "Página1"),
    FonteExcel("healthcheck_2025", "google_sheets", "healthcheck_2025", "Página1"),
    FonteExcel("resenhas_appsheets", "google_sheets", "resenhas_appsheets", "BaseDados"),
    # Daily Hispana (App Natura e App_Avon vêm das mesmas planilhas do Brasil)
    FonteExcel("mkt_analitico_hispana", "drive", "mkt_analitico_hispana", "Planilha1"),
    FonteExcel("mkt_hispana_completo", "drive", "mkt_hispana_completo", "Sheet1"),
    FonteExcel("tickets_hispana", "drive", "tickets_hispana", "Planilha1"),
    FonteExcel("base_mtk", "drive", "base_mtk", "Base"),
    FonteExcel("base_mtk_historico", "drive", "base_mtk_historico", "Base"),
    FonteExcel("base_sn_ois", "drive", "base_sn_ois", "Page 1"),
    FonteExcel("resenhas_latam", "drive", "resenhas_latam", "in"),
    FonteExcel("mi_negocio", "drive", "mi_negocio", "reviews_reviews_net.natura.mine"),
    FonteExcel("auxiliar_hispana", "google_sheets", "auxiliar_hispana", "Funcao do Sistema"),
    FonteExcel("registro_de_grupos_hispana", "google_sheets", "registro_de_grupos_hispana", "Página1"),
    FonteExcel("resenhas_ois", "google_sheets", "resenhas_ois", "BaseDados"),
    FonteExcel("ticket_medio_hispana", "google_sheets", "ticket_medio_hispana", "Ticket Medio"),
    FonteExcel("ticket_medio_por_pais", "google_sheets", "ticket_medio_por_pais", "Ticket Medio"),
    FonteExcel("base_exento", "google_sheets", "base_exento", "Página1"),
    # CSAT (MKT_Reativos, BASE MTK e MKT Analitico Hispana vêm das fontes acima)
    FonteExcel("enquete_mkt_reativos", "drive", "enquete_mkt_reativos", "Base"),
    FonteExcel("enquete_base_mtk", "drive", "enquete_base_mtk", "Base"),
    FonteExcel("enquete_malasia", "drive", "enquete_malasia", "Base"),
    FonteExcel("enquete_ces", "drive", "enquete_ces", "CES"),
    FonteExcel("analistas_enquetes", "drive", "analistas_enquetes", "Planilha1"),
    FonteExcel("base_malasia", "drive", "base_malasia", "BASE MALASIA"),
    FonteExcel("modelo_gauge", "drive", "modelo_gauge", "Página1"),
]

# Só o Brasil está no escopo; os brutos de Hispana e NCC já ficam guardados no volume para quando entrarem.
FONTES_MKTZAP = [
    FonteMktzap("mktzap_brasil_analitico", "brasil", "analitico"),
    FonteMktzap("mktzap_brasil_tickets", "brasil", "tickets"),
]
