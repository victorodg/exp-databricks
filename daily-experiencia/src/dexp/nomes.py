"""Regra do Tableau Prep para nomes de coluna repetidos num join (sem dependência do Spark, para testar localmente).

Quando os dois lados têm uma coluna com o mesmo nome, a "família" dessa coluna no lado DIREITO (X, X-1, X-2...) é
renumerada a partir do maior sufixo que a família já tem no lado esquerdo. Exemplos vistos nos extracts:
esquerda {X, X-1} e direita {X} -> a da direita vira X-2; esquerda {X} e direita {X, X-1} -> as da direita viram
X-1 e X-2. A exceção são as colunas X-1 que já nasceram de um join anterior: essas o Prep mantém, e a X que colide
vai para o próximo sufixo livre (são as de `preservar`). Em snake_case o sufixo -1 vira _1.
"""
import re


def _sufixo(coluna, base):
    if coluna == base:
        return 0
    m = re.fullmatch(re.escape(base) + r"_(\d+)", coluna)
    return int(m.group(1)) if m else None


def renomes_direita(colunas_esquerda, colunas_direita, preservar=()):
    """{coluna da direita: novo nome} para as colunas que precisam mudar de nome."""
    renomes = {}
    for base in [c for c in colunas_direita if c in colunas_esquerda]:
        sufixos_esquerda = {s for s in (_sufixo(c, base) for c in colunas_esquerda) if s is not None}
        familia = sorted((s, c) for c in colunas_direita if (s := _sufixo(c, base)) is not None and c not in renomes)
        ocupados = sufixos_esquerda | {s for s, c in familia if c in preservar}
        proximo = max(sufixos_esquerda) + 1
        for _, coluna in [(s, c) for s, c in familia if c not in preservar]:
            while proximo in ocupados:
                proximo += 1
            renomes[coluna] = f"{base}_{proximo}"
            ocupados.add(proximo)
    return renomes
