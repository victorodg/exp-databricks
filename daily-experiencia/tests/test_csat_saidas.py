from dexp.csat_saidas import SQL_DETALHE, SQL_MENSAL


def test_consultas_usam_so_a_fatia_1_e_a_tabela_passada():
    for consulta in (SQL_DETALHE, SQL_MENSAL):
        texto = consulta.format(enquetes="x.y.dexp_gold_csat_enquetes")
        assert "FROM x.y.dexp_gold_csat_enquetes" in texto
        assert "slice_numero = 1" in texto


def test_ofensor_do_ncc_e_o_status_de_classificacao():
    # Decisão de 09/11/2026: no Tableau o NCC agrupava pelo status de finalização
    linha = next(l for l in SQL_DETALHE.splitlines() if l.strip().endswith("AS ofensor,"))
    assert "WHEN 'NCC' THEN ncc_status_de_classificacao" in linha
    assert "WHEN 'Hispana' THEN ois_funcao_do_sistema" in linha
    assert "ELSE exp_br_funcao_do_sistema" in linha


def test_mensal_conta_protocolos_distintos():
    assert "count(DISTINCT protocolo) AS enviadas" in SQL_MENSAL
    assert "count(DISTINCT CASE WHEN c_sat = 'PROMOTOR' THEN protocolo END) AS promotores" in SQL_MENSAL
    assert "try_divide(promotores, respondidas) AS csat" in SQL_MENSAL
