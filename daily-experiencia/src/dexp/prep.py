"""Operações de linha do Tableau Prep (join e união) com a mesma nomenclatura de colunas.

A regra de nomes repetidos num join está em `dexp.nomes` (e testada em tests/test_nomes.py).
"""
from functools import reduce

from pyspark.sql import functions as F

from dexp import tableau as tb
from dexp.nomes import renomes_direita


def juntar(esquerda, direita, chaves, como, preservar=()):
    """Join do Prep. chaves: [(coluna da esquerda, coluna da direita)] com os nomes de antes do join;
    como: 'left', 'right', 'inner' ou 'full'. Textos são comparados sem diferenciar maiúsculas.
    preservar: colunas X_n da direita que vieram de um join anterior e mantêm o nome."""
    renomes = renomes_direita(esquerda.columns, direita.columns, preservar)
    direita = direita.select([F.col(f"`{c}`").alias(renomes.get(c, c)) for c in direita.columns])
    tipos = dict(esquerda.dtypes)
    condicoes = []
    for coluna_esq, coluna_dir in chaves:
        e, d = esquerda[f"`{coluna_esq}`"], direita[f"`{renomes.get(coluna_dir, coluna_dir)}`"]
        if tipos[coluna_esq] == "string":
            e, d = tb.chave_join(e), tb.chave_join(d)
        condicoes.append(e == d)
    return esquerda.join(direita, reduce(lambda a, b: a & b, condicoes), como)


def uniao(*dfs):
    """União de linhas do Prep: junta por nome de coluna; o que falta num lado fica nulo.
    A coluna "Table Names" que o Prep cria não é reproduzida."""
    return reduce(lambda a, b: a.unionByName(b, allowMissingColumns=True), dfs)


def remover(df, *colunas):
    """Remover colunas do Prep; ignora as que não existem (o Prep as descarta sem erro na mesma situação)."""
    return df.drop(*[c for c in colunas if c in df.columns])
