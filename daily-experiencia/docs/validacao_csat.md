# Validação – CSAT

Comparação de `dexp_gold_csat_enquetes` com o extract `Enquetes C-SAT` (atualizado em 30/10/2026 por volta de 09:30 de
Brasília). Ferramenta: `ferramentas/comparar_extract.py`. Gabarito em `validacao\extracts_csat\`.

## Resultado

Linhas: 509.165 nos dois lados, com as mesmas colunas. São 101.833 enquetes, cada uma repetida nas 5 fatias do Modelo Gauge.

## Diferenças que sobraram

- **`OIS Solução Aplicada`:** um protocolo tem 434 na gold e 435 no extract (5 linhas, uma por fatia). Causa não investigada.
- **Grafia do "INCIDENTE CRÍTICO" quebrado em `NCC Setor Entrada` e `NCC Setor Fim`:** o Prep grava o caractere de controle como
  `_x008D_`, e a gold o mantém. O valor já vem quebrado da planilha.
- **Textos** (`Nome`, `Contato`, tempos, observações): o Prep lê o formato de exibição do Excel e guarda uma grafia só
  para textos iguais sem diferenciar maiúsculas.

## Comportamentos do Prep reproduzidos

- **`Respondido em`:** texto no formato de exibição do Excel (`1/1/2025 18:54`), sem os segundos.
- **Enquete Malasia:** uma linha por protocolo, com o menor valor de cada coluna, e sem o protocolo de teste `1990-1509513108473`.
- **Join com Analistas Enquetes:** interno, então enquete de analista fora da lista sai da base.
- **`Slice #` e `Slice`:** números e textos do Modelo Gauge; na gold, `slice_numero` e `slice`.

## Indicadores mês a mês (09/11/2026)

`ferramentas/validar_csat_mensal.py` calcula os indicadores com as fórmulas do workbook GovEXP. A comparação é por
operação e mês, entre o extract de 30/10 e a view `dexp_vw_csat_enquetes`. Os indicadores comparados são:
- C-SAT e C-SAT Simple dos medidores;
- enviadas e respondidas;
- promotores, neutros e detratores, contados por linha e por protocolo;
- total e média do CES.

| Operação | Meses comparados (até set/2026) | Meses iguais em todos os indicadores |
|---|---|---|
| Experiencia Brasil | 40 | 40 |
| Hispana | 25 | 25 |
| NCC | 23 | 23 |
| CES | 8 | 8 |

O relatório também mostra o efeito das regras do painel novo em Apps Script (`dexp_gold_csat_mensal`), que conta tudo
por protocolo distinto. Só o Brasil muda, em dez/2024, abr/2025 e set/2025, por protocolos com mais de uma enquete. Em
abr/2025, o C-SAT vai de 90,37% para 86,31%. Detalhes e decisões em `../csat/README.md`.

## NCC com a regra do Daily NCC (09/11/2026)

A partir de out/2026, a gold deixa de seguir o Prep no NCC. A regra passa a ser a do painel Daily NCC: entra toda
enquete cujo protocolo está na BASE MALASIA e cujo Status de finalização não contém "Teste", esteja o analista na
lista Analistas Enquetes ou não. Até set/2026 nada muda, e por isso a comparação com o extract continua valendo para os
meses fechados.

Em out/2026, o NCC passou de 86 enviadas, 26 respondidas e 96,15% para 131, 39 e 94,87%. A diferença são 45 enquetes de
4 analistas do NCC fora da lista. Decisão e detalhes em `../csat/README.md`.
