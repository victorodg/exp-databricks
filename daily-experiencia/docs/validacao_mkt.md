# Validação – MKT

Comparação das 18 tabelas gold com os extracts publicados no Tableau Cloud (atualizados em 27/10/2026 por volta de
09:30 de Brasília), usando as planilhas capturadas no mesmo dia. Ferramentas: `ferramentas/comparar_mkt.sh`
(roda `comparar_extract.py` para as 18 saídas) e `ferramentas/consultar_extract.py`.

## Resultado

As 18 saídas têm exatamente o mesmo número de linhas do Tableau, e os campos calculados (Nível, SLAs em horas úteis,
SLA do primeiro contato, tempos, função do sistema, tribo, expurgo, responsável, ticket médio) batem.

| Gold (`dexp_gold_mkt_*`) | Extract | Linhas |
|---|---|---|
| `experiencia_brasil_nivel` | Experiencia Brasil Nivel | 137.738 |
| `ticket_medio` | Ticket Medio Exp Br | 68.734 |
| `brasil_whatsapp` | MKT BRASIL - WhatsApp | 63.340 |
| `whats_gn` | MKT Whats GN | 59.587 |
| `brasil_completo` | MKT Brasil Completo | 32.762 |
| `brasil_email` | MKT BRASIL - Email | 28.788 |
| `exp_brasil_dynatrace` | Exp Brasil Dynatrace | 23.571 |
| `emails_de_lojas` | MKT Emails de Lojas | 17.511 |
| `email_experiencia_cb` | MKT Email Experiencia CB | 11.277 |
| `brasil_completo_nivel` | MKT Brasil Completo Nivel | 10.109 |
| `cbcom` | MKT - CBCOM | 1.441 |
| `whats_gv` | MKT Whats GV | 1.360 |
| `requisicao_eventual` | Requisição Eventual EXP BR | 618 |
| `whats_gv_antecipada` | MKT Whats GV Antecipada | 510 |
| `whats_franquia` | MKT Whats Franquia | 442 |
| `historico_backlog_diario` | Histórico Backlog Diário | 308 + 1 por dia |
| `brasil_backlog` | MKT Brasil Backlog | 146 |
| `hc_exp_brasil` | HC Exp Brasil | 63 |

## Diferenças que sobraram

- **Dependem da hora de execução** (`NOW()`/`TODAY()`): Faixa de Aging e Aging do Backlog e o Status SLA Email dos
  e-mails ainda abertos. Mudam a cada dia; não são diferença de regra.
- **Durações de 24 horas ou mais** (ex.: "Tempo de Operação" 44:44:06): o Prep converte a célula do Excel em texto pelo
  formato de exibição e interpreta "[h]:mm:ss" errado — perde a hora e põe o mês no lugar dos minutos (44:44:06 vira
  ":12:06"). Com isso o Prep dá "Sem informação" no SLA Tempo Médio Operacional, e a gold, que lê o valor certo, dá
  "Fora do SLA" (10 linhas no MKT BRASIL - Email, 8 no Email Experiencia CB, 2 nos Emails de Lojas).
  **Decisão (28/10/2026): manter o valor correto na gold**, diferente do Prep.
- **CPF/CNPJ**: num registro o Prep arredondou o número (10424500000); a gold tem o valor certo (10424494817).
- **Grafias que só mudam maiúsculas** ("SIM"/"Sim", "ARAUCÁRIA"/"Araucária"): o extract guarda uma grafia só para textos
  iguais sem diferenciar maiúsculas. Vai acontecer igual quando o Tableau ler do Databricks.
- **"Table Names"**, **F31 a F34** (ServiceNow): colunas técnicas do Prep e colunas sem cabeçalho, não levadas para a gold.

## Comportamentos do Prep reproduzidos

- **Nomes repetidos em join** (`dexp/nomes.py`): a família da coluna no lado direito (X, X-1...) é renumerada a partir
  do maior sufixo do lado esquerdo; colunas X-1 que vieram de um join anterior são mantidas. Várias regras dependem
  disso ("CHAMADO-1", "Função do Sistema-2"), e a regra foi confirmada nos extracts do Backlog e do WhatsApp.
- **Colunas que só diferem em maiúsculas** são colunas diferentes no Prep e viram nomes próprios na gold:
  "Mercado" (registros RE do AppSheets) = `mercado_re`; "PEDIDO FINALIZADO" do ticket na Experiencia Brasil Nivel =
  `pedido_finalizado_ticket`; na planilha do Dynatrace até julho, `hora_fim_do_atendimento_ate_julho` e
  `erro_perceptivel_ao_usuario_ate_julho`.
- **Ciclo do Healthcheck** gravado como data na planilha sai como MM/AAAA, igual ao texto exibido que o Prep lê.
- **Histórico Backlog Diário**: no Tableau o extract é acumulado (uma linha por execução do fluxo, 308 linhas desde
  25/02/2026). O histórico foi importado do extract (`ferramentas/importar_historico_backlog.py`) e a gold acrescenta
  uma linha por dia (`origem_registro = 'databricks'`).
- As listas grandes do fluxo (remapeamento de função do sistema, nomes de responsáveis, protocolos expurgados, regras de
  Nível) são extraídas do `.tfl` por `ferramentas/extrair_regras_mkt.py` para `src/dexp/regras_mkt.py`.
