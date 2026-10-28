from dexp.nomes import renomes_direita


def test_coluna_da_direita_vai_para_o_proximo_sufixo_livre_da_esquerda():
    # [81]: esquerda {X, X-1} e direita {X} -> X-2
    assert renomes_direita(["x", "x_1"], ["x", "y"]) == {"x": "x_2"}


def test_familia_da_direita_e_renumerada():
    # [82]: esquerda {X} e direita {X, X-1} -> X-1 e X-2
    assert renomes_direita(["x", "macro"], ["x", "x_1"]) == {"x": "x_1", "x_1": "x_2"}


def test_coluna_de_join_anterior_e_preservada():
    # [92]: chamado_1 veio do join [80]; o chamado da direita vai para chamado_2
    assert renomes_direita(["chamado"], ["chamado", "chamado_1"], preservar=["chamado_1"]) == {"chamado": "chamado_2"}


def test_sem_colisao_nao_renomeia():
    assert renomes_direita(["a"], ["b", "b_1"]) == {}
