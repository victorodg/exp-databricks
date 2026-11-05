# Book Executivo: números do mês a partir do Databricks

Gera, para um mês, a linha de cada aba das planilhas do Book Executivo, lendo as tabelas gold do Databricks
(`sandbox.sustentacao_bau_experiencias.dexp_gold_*`), que são cópias das fontes publicadas no Tableau Cloud. As regras de
cada número reproduzem as planilhas dos painéis do Tableau (citadas no código) e o Manual de Indicadores.

## Uso

A partir desta pasta, com a CLI do Databricks configurada no perfil `daily-exp` (o mesmo do projeto `daily-experiencia`):

```powershell
python executar.py brasil 2026-10              # gera outubro em saida\brasil_2026-10.md
python executar.py brasil 2026-09 --validar    # compara setembro com gabaritos\brasil_2026-09.json
```

Colunas marcadas como `manual` não saem do Databricks e continuam sendo preenchidas à mão.

## Validação

O gabarito de um mês é a linha que já está no Book (`gabaritos/<frente>_<mês>.json`). Uma aba só deve ser usada depois
de bater com o gabarito.

| Aba | Setembro/2026 | Observação |
|---|---|---|
| `Exp_Br_Indicadores_Contratuais` | 5 de 6 iguais (2 manuais) | Retenção N1 dá 70,27%; o Book tem 70,39%. O Tableau de produção hoje também dá 70,27%: os dados mudaram depois do preenchimento (07/10). |
| `Exp_Br_Indicadores_Monitoracao` | 5 de 6 iguais | SLA Prazo Cliente dá 96,61%; o Book tem 96,62%. Mesmo caso: a produção hoje também dá 96,61%. |
| `Exp_Br_Cards01` | 9 de 10 iguais (1 a investigar) | Protocolos CB e CF: 2.176 × 2.178 (dados mudaram). "Resenhas 4 e 5" ainda sem regra. |
| `Exp_Br_Retencao` | 2 de 5 iguais | Diferenças de 1 unidade ou 0,01 p.p. (dados mudaram): Ocorrências 1.890 × 1.891, Retenção N1 70,38% × 70,39%. |
| `Exp_Br_Cards2` | 3 de 6 iguais (1 a investigar) | Retenção Tarefas 76,03% × 76,04% e SLA Tarefas 86,03% × 85,99% (dados mudaram). "TMA E-mail" ainda sem regra. |

| `Exp_Br_Reativos_WA_Mensal`, `Exp_Br_WA_GN/GV/Franq/CBCom_Mensal` | todas iguais | |
| `Exp_Br_Email_Mensal` | todas iguais | O TMA (01:34:47) é a média do tempo de operação com o filtro de status de finalização do painel. |
| `Exp_Br_Email_TMO` | 3 de 4 iguais | "TMO N2 - Origem WhatsApp": o Book tem 203:05:27, mas a monitoração do mesmo mês tem "04 dias" (o programa dá 114:44:46, que bate com a monitoração). O próprio Book está inconsistente nesse número. |
| `Exp_Br_Tarefas_CB_Mensal` | todas iguais | |
| `Exp_Br_Tarefas_Historico_Mensal`, `Exp_Br_Tarefas_CF_Mensal` | diferenças de 1 protocolo | Dados mudaram depois do preenchimento. Em CF, o Book tem N1 = 78% em setembro (os meses anteriores ficam em ~96%, como o programa): parece digitação. |
| `Exp_Br_Tarefas_CB_Fase`, `Exp_Br_Tarefas_CF_Fase` | volumes iguais (±1) | Fase 1 CB: 99,61% × "100%"; CF usa percentuais inteiros no Book. |
| `Exp_Br_ReqEvent_Mensal` | quantidade igual | Volume N1/N2 ainda sem regra. |

| Abas de motivos (`*_Motivos_N1/N2`, `Tarefas_CB/CF_Motivo_N1/N2`) | WA N1 e Tarefas CB N1: 15 de 18 | Regra: as 3 maiores plataformas (Tribo) e, em cada uma, os 3 maiores motivos (Macro), contando linhas e juntando grafias que só mudam em maiúsculas. Diferenças: erros de digitação no Book ("Acesso" 172 × 164; "Manu" por "Menu") e 2 tarefas a mais em AIBV/Cadastro (dados mudaram). Tarefas usam a visão "Encerrado em", só "Normal". |

| `Exp_Br_Proativos_Mensal`, `_Contatos_Pedidos`, `_HC_Mensal` | todas iguais (1 a investigar) | "Alcance %" do Health Check ainda sem regra. |
| `Exp_Br_Email_Natura_Expcb/AppNatura/AppAvon_Mensal` e `_SLA` | todas iguais | Volumetria e SLA contam só e-mails encerrados; sem e-mails no mês, "0" e "Sem dados" (como o Book). |
| `Exp_Br_CSAT_3Meses`, `_Classificacao`, `_Nota` | todas iguais | Contagem por protocolo distinto (a fonte tem uma linha por pergunta da enquete). O C-SAT daqui (promotores ÷ respondidas) é diferente do CSAT dos indicadores contratuais (média das notas). |
| `Exp_Br_CSAT_Mercado` | 3 de 5 | Araucária e Atlântica diferem alguns décimos; a regra de mercado pode juntar outros códigos. |
| `Exp_Br_CSAT_Ofensores_Detr` | 2 de 3 | Empate no 3º lugar (vários com 2 casos): o programa escolhe pela ordem alfabética. |

| `Exp_Br_Resenhas_<app>_01` a `_06` (Minha Consultoria, FV, App Natura, App Avon) | iguais, fora 1 avaliação a mais em Minha Consultoria (dados mudaram) | 01: média de estrelas do mês e de todas as avaliações até o fim do mês; 02 e 03: avaliações das lojas (Resenhas Brasil); 04 a 06: respostas do time (AppSheets): SLA, tipo (categoria) e motivo (categoria 2). App Natura = "App Sempre Presente". |
| `Exp_Br_Resenhas_<app>_07` | parcial | Linha 2 (1 a 3 estrelas) sai das respostas do AppSheets; a contagem de 4 e 5 estrelas respondidas ainda não bate (Minha Consultoria: Book 30, testes 24–27). |

Manuais (texto): `Exp_Br_Highlights`, `Exp_Br_Lowlights`, `Exp_Br_Proativos_HC_Comentarios`, `Exp_Br_CSAT_Comentarios`,
`Exp_Br_CSAT_Analise_Quald`, abas `Exp_Br_QA_*`.

Ainda sem regra: `Exp_Br_Top3_Plataformas`, `Exp_Br_Tarefas_Top3_N1/N2`, `Exp_Br_ReqEvent_Motivos_*`, volume N1/N2 de
Requisições Eventuais e "Resenhas 4 e 5".

**Franquias (decidido em 04/11/2026):** até setembro os protocolos de Franquias vinham como "Protocolos CB" e entravam
na retenção e nas Ocorrências; depois passaram a ter tipo próprio, que o filtro do painel não inclui. O programa
continua incluindo esses protocolos (agrupados em "SERVICE CLOUD / DYNAMICS"), para manter a série comparável.

## Hispana (México e Sur)

```powershell
python executar.py mexico 2026-10              # Book Executivo Hispana Mexico
python executar.py sur 2026-10                 # Book Executivo Hispana Sur (Argentina + Chile)
python executar.py mexico 2026-09 --validar    # compara com gabaritos\mexico_2026-09.json
```

Regras (painéis "Daily Mexico OIS" e "Experiência Hispana Sur - Daily", tabelas `dexp_gold_hispana_*`):

- **Volumes e níveis:** nível consolidado do painel. E-mail a partir de março/2026 conta pelas linhas do MKT Completo;
  WhatsApp e Requisições (grupos) pelo MKT Analítico. Só N1, N2 e Neutro; mês da data de contato. Retenção = N1 / (N1 + N2).
- **SLA WhatsApp:** linhas de WhatsApp do MKT Analítico, dentro / (dentro + fora) do SLA com expurgo.
- **Pedidos convertidos:** soma de atendimentos com pedido finalizado "SI" × ticket médio do país no mês.
- **Motivos e causa raiz:** 3 maiores plataformas (status de classificação, sem as filas de acompanhamento) e, em cada
  uma, as 3 maiores funções do sistema.
- **CSAT:** enquetes `fonte = 'Hispana'` do país, por protocolo distinto.

| Setembro/2026 | México | Sur | Observação |
|---|---|---|---|
| Conferência | 83 de 96 | 94 de 116 | |
| Volumes de WhatsApp, grupos, retenção total, SLA, solicitações por dia, motivos, causa raiz, CSAT | iguais | iguais | Empates no 3º ofensor detrator: o programa escolhe pela ordem alfabética. |
| E-mails | 262 × 33 | 932 × 644 | Os tickets de e-mail de setembro concluídos depois do preenchimento entraram na base (agosto bate: 330). Por isso o total e a retenção de e-mail também diferem. |
| TMA E-mail | não confere | 03:36 × 03:41 | Regra provável: média do tempo de operação dos e-mails N1 e N2 do MKT Analítico. |
| Pedidos convertidos | 1.285 × 1.290 | 1.706 × 1.691 | Mesma regra, dados mudaram. |

Sem regra (ficam em branco): **Health Check** (vem da planilha "Healthcheck Paises Consolidado", fora do Databricks).
Manuais: Comentarios dos Cards1, `*_CSAT_Analise_Quald`, `*_CSAT_Comentarios` e o texto de `*_CSAT_Paises_Ofensor`.
Nas abas `*_Pais` e `*_CSAT_Paises_3_Meses` a coluna A é o país e a B é o mês.

## Planilha geral "Book Executivo" (Hispana consolidada, Mercado Andino, CSAT e resenhas da Hispana)

```powershell
python executar.py geral 2026-10
python executar.py geral 2026-09 --validar     # compara com gabaritos\geral_2026-09.json
```

É a planilha que o Apps Script lê como `EXECUTIVO_SS_ID` (`1QABgQDBqWPCHunLU84uxy6P__zJKPAPqnnRCmzp9rJ8`). Usa as mesmas
regras de `book/hispana.py`: Andino = Colômbia, Equador e Peru; Hispana consolidada ("OIs") = os seis países.
Os países aparecem em português e as abas `*_Pais` e `*_CSAT_Paises_3_Meses` têm o país na coluna A.

Setembro/2026: 184 de 265 colunas iguais. Além dos e-mails que entraram depois (como no México e no Sur):

| Assunto | Situação |
|---|---|
| Pedidos convertidos do Andino | Colômbia bate (515 × 512), mas Equador (406 × 492) e Peru (606 × 759) ficam abaixo do Book. Regra a confirmar. |
| Resenhas 01 a 03 (média, volume, estrelas) | Regra certa; o Book tem 3 a 4% menos avaliações (as lojas acrescentam avaliações depois). |
| Resenhas 07 | Só a linha 2 (respostas a 1 a 3 estrelas). |
| Resenhas 04, 05, 06, 08, 09, 10 | Sem regra que bata (SLA, categorias, TMO e assunto). Ficam fora do programa. |
| Monitoração | TMO N2/N3 de origem WhatsApp e N2 de origem e-mail batem; N3 de origem e-mail e TPA de resenhas, a investigar. |
| Cards | Health Check, Resenhas 1 a 3/4 e 5, E-mails Loja, Soporte Experiencia, Líderes Equador e SLA Geral do Andino, a investigar. |
| Indicadores contratuais | TMR e-mail N1 a investigar; Notificação de Incidente e QA manuais. |

Fora do programa: `Interacoes_Mes` (soma de NCC + Brasil + Hispana), `Hisp_HC_3Meses`, QA, Highlights e Lowlights.

## Estrutura

| Caminho | Conteúdo |
|---|---|
| `executar.py` | Linha de comando: gera o mês e, com `--validar`, compara com o gabarito |
| `book/databricks.py` | Consulta ao SQL Warehouse pela CLI do Databricks |
| `book/formatos.py` | Formatos do Book ("98,85%", "R$ 1.234,56", "04 dias") |
| `book/brasil.py` | Uma função por aba do Book Exp Brasil |
| `gabaritos/` | Valores já lançados no Book, usados na validação |
| `saida/` | Resultado de cada execução |
