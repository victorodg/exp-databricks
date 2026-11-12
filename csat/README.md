# C-SAT (GovEXP) no Databricks e em Apps Script

Migração do C-SAT do workbook **"GovEXP - Métricas da Excelência"** e do fluxo Tableau Prep **"GovEXP - Metricas de
Excelencia - CSAT"** (cópias em `tableau/`):

- **Dados:** o fluxo roda no Databricks, dentro do pipeline do Daily Experiência (`../daily-experiencia`), nas camadas
  bronze, silver e gold, no job `dexp_daily_experiencia` (tarefa `gold_csat`).
- **Painel:** o painel passa para Google Sheets + Apps Script, com um desenho novo e uma página por operação: Brasil, NCC,
  Hispana e CES.

Os outros painéis do workbook (QA, Produtividade, Retenção) não leem a fonte do C-SAT. Eles entram na próxima etapa,
no fim deste arquivo.

## Arquitetura

```
 Databricks (sandbox.sustentacao_bau_experiencias)        Máquina local                 Google
 ─────────────────────────────────────────────────        ─────────────                 ──────
 bronze → silver → dexp_gold_csat_enquetes  ─┐
                    dexp_gold_csat_detalhe  ─┼─► coleta/exportar_sheets.py ─► Drive: Fontes de Dados\auto\csat
                    dexp_gold_csat_mensal   ─┘   (perfil daily-exp da CLI)          │ csat_<operação>.csv
                                                                                     ▼ csat_mensal.csv
                                                         Planilha "Painel C-SAT" ◄── importarCsat() (todo dia, 10h)
                                                         abas dados_<operação>        │
                                                                                     ▼
                                                         App da Web: ?pagina=brasil | ncc | hispana | ces
```

O caminho Databricks → Drive local → Apps Script segue o padrão do Daily Experiência: não guarda token do Databricks
no Google e não depende da API do Drive.

## Estrutura

| Caminho | Conteúdo |
|---|---|
| `tableau/` | Fluxo (.tflx) e workbook (.twbx) baixados do Tableau Cloud, usados como referência |
| `coleta/config.toml` | Pasta do Drive de destino e colunas exportadas por operação |
| `coleta/exportar_sheets.py` | Lê as saídas da gold e grava os CSV na pasta do Drive. Só regrava o que mudou |
| `apps_script/Codigo.gs` | Importação dos CSV para a planilha, acionador diário, `doGet` e a função `dados()` das páginas |
| `apps_script/Pagina.html`, `Script.html`, `Estilo.html` | Página de cada operação (HTML, JS e CSS) |
| `apps_script/Indice.html` | Página sem parâmetro, com os links das quatro páginas |
| `apps_script/appsscript.json` | Manifesto: fuso de São Paulo, escopos e app da Web restrito ao domínio |

No `../daily-experiencia`:

| Caminho | Conteúdo |
|---|---|
| `docs/fluxos/csat.md` | Especificação do fluxo, etapa por etapa. O `.tflx` desta pasta gera a mesma especificação |
| `src/gold/csat.py` | Gold do fluxo (`dexp_gold_csat_enquetes`) e as duas saídas do painel |
| `src/dexp/csat_saidas.py` | SQL de `dexp_gold_csat_detalhe` e `dexp_gold_csat_mensal`. O job, a exportação e a validação usam o mesmo SQL |
| `ferramentas/validar_csat_mensal.py` | Validação mês a mês contra o extract do Tableau |
| `docs/validacao_csat.md` | Resultados das validações |

## Rotina

1. **9h–9h30:** o job `dexp_daily_experiencia` atualiza a gold (rotina do Daily Experiência).
2. **Depois do job:** a exportação grava os CSV na pasta do Drive, e o Google Drive para desktop sincroniza a pasta.
   Ela já faz parte da rotina do Daily Experiência:
   - no `rotina_manual.ipynb`, é a célula 5;
   - no `rotina_diaria.ps1`, roda sozinha quando o job termina.

   Só os arquivos que mudaram são regravados. Se nada mudou, o `_ultima_exportacao.json` fica igual, e o Apps Script não
   reimporta. Para rodar à mão, a partir da pasta `csat`:
   ```powershell
   ..\daily-experiencia\.venv\Scripts\python.exe coleta\exportar_sheets.py --aguardar-job
   ```
   Opções:
   - `--aguardar-job`: espera a execução do job em andamento terminar;
   - `--simular`: consulta tudo e não grava nada;
   - `--pasta <outra>`: testa fora do Drive.
3. **10h:** o acionador roda `importarCsat()`, que regrava as abas da planilha. Se a exportação não mudou, ele não faz
   nada.

## Instalação do Apps Script (uma vez)

1. Crie a planilha **Painel C-SAT** no Drive compartilhado e abra **Extensões > Apps Script**.
2. Copie os arquivos de `apps_script/` com os mesmos nomes. Em **Configurações do projeto**, marque "Mostrar o arquivo de
   manifesto" para colar o `appsscript.json`.
3. Em **Configurações do projeto > Propriedades do script**, crie `PASTA_CSAT_ID` com o ID da pasta
   `Fontes de Dados\auto\csat`. O ID é o trecho do link da pasta depois de `/folders/`.
4. Rode `importarCsat` uma vez pelo editor e autorize. Para importar de novo sem exportação nova (por exemplo, depois de
   atualizar o código), rode `forcarImportacao`.
5. Rode `criarAcionador` uma vez.
6. **Implantar > Nova implantação > App da Web**, executando como você e com acesso restrito à organização. O link sem
   parâmetro abre o índice. Cada página é `<link>?pagina=brasil`, `ncc`, `hispana` ou `ces`.

A primeira carga de cada página traz os últimos 24 meses. No seletor de mês, "Carregar meses anteriores…" traz o resto
do histórico. A página abre no último mês que tem alguma resposta.

Para a página abrir rápido, a importação também grava os dados de cada página já prontos, compactados (gzip, em base64),
nas abas ocultas `_pacote_<operação>`: a coluna A com os últimos 24 meses e a B com tudo. A página descompacta no
navegador. Se o pacote não existir, ou o navegador não tiver `DecompressionStream`, ela lê a aba `dados_<operação>`, que é
o caminho lento.

### Atualizar o código publicado

1. Cole no editor os arquivos que mudaram.
2. Se mudou a importação, rode `forcarImportacao`.
3. Em **Implantar > Gerenciar implantações**, clique no lápis da implantação, escolha **Versão: Nova versão** e clique
   em **Implantar**. O link continua o mesmo.

## Fontes e regras do fluxo

O fluxo tem 34 etapas, especificadas em `../daily-experiencia/docs/fluxos/csat.md`.

| Fonte | Arquivo | Papel |
|---|---|---|
| Enquete MKT REATIVOS | `Enquete MKT REATIVOS.xlsx` | Enquetes do Brasil (`fonte = Experiencia Brasil`) |
| Enquete Malasia | `Enquete Malasia.xlsx` | Enquetes do NCC. Fica uma linha por protocolo, com o menor valor de cada coluna, e sai o protocolo de teste `1990-1509513108473` |
| Enquete BASE MTK | `Enquete BASE MTK.xlsx` | Enquetes da Hispana |
| Enquete CES | `Enquete CES.xlsx` | Enquetes do CES |
| MKT_Reativos | `EXP BR\MKT\MKT_Reativos.xlsx` | Atributos do Brasil e do CES: mercado, função do sistema, setor fim e status |
| BASE MTK, BASE MTK Histórico, MKT Analítico Hispana | `EXP OIS\MKT\...` | Atributos da Hispana. O país sai do setor fim |
| BASE MALASIA | `BASE MALASIA.xlsx` | Atributos do NCC: function, status, setores e solution applied |
| Analistas Enquetes | `Analistas Enquetes.xlsx` | Só entram enquetes de analistas da lista, que também traz o Time. **Exceção: NCC a partir de out/2026** (abaixo) |
| Modelo Gauge | Excel | 5 fatias. Cada enquete aparece 5 vezes na `dexp_gold_csat_enquetes`, porque o Tableau desenha os medidores assim |

Regras principais:

- **Classificação pela nota:** 4–5 = PROMOTOR, 3 = NEUTRO, 1–2 = DETRATOR. Sem nota = "Não respondido".
- **CES:** a nota vira um número de 1 a 5 (`nota_ces`). As classes valem para o CES como fácil, neutro e difícil.
- **Turno:** sai do Time do NCC.
- **Mercado:** é normalizado (AT → ATLÂNTICA, AM → AMAZÔNIA etc.). No filtro, só os 5 mercados válidos aparecem; os
  outros ficam vazios.
- **Data da enquete:** é a data de `Enviado em`. O mês de cada indicador é o mês dessa data.
- **Quais enquetes do NCC entram (a partir de out/2026):** vale a mesma regra do painel Daily NCC. Entra toda enquete
  cujo protocolo está na BASE MALASIA e cujo Status de finalização não contém "Teste", esteja o analista na lista
  Analistas Enquetes ou não. Analistas fora da lista ficam sem Time e sem Turno.
  - Até set/2026, o NCC continua com a regra da lista, para não mudar meses fechados. Antes de jul/2026 a regra do
    Daily nem daria certo, porque a BASE MALASIA só tem atendimentos a partir de jul/2026.
  - A regra está em `daily-experiencia/src/gold/csat.py` (`NCC_REGRA_DAILY_DESDE`). Por isso, a gold se afasta do
    fluxo do Prep a partir de out/2026.

## Indicadores

| Indicador | Painel novo (gold `dexp_gold_csat_mensal` e páginas) | Tableau (como era) |
|---|---|---|
| C-SAT | promotores ÷ respondidas | medidor: `(SUM(Nota da CSAT)/5) / COUNTD(Protocolo)` das respondidas |
| C-SAT Simple | (promotores + neutros) ÷ respondidas | igual, com `Nota da CSAT Simple` |
| Response Rate | respondidas ÷ enviadas | `COUNTD(respondidas) / COUNTD(Protocolo)` |
| Enviadas, Respondidas, Sem resposta | protocolos distintos | protocolos distintos (gráfico de Status) |
| Promotores, Neutros, Detratores e gráficos de contagem | protocolos distintos | Brasil e Hispana: linhas da fatia 1; NCC: protocolos distintos |
| CES médio | média das notas de 1 a 5 | `SUM(Nota CES) / Total CES` |
| CES respostas | protocolos com nota | `Total CES`, que no gráfico mensal saía 5× maior |
| Meta do C-SAT | 70%, com indicação "na meta" ou "abaixo da meta" | o campo `Meta` = 0,7 existia, mas não aparecia |

Todas as porcentagens aparecem com 1 casa decimal. O medidor do NCC usava 2.

Filtros de cada página, todos de seleção múltipla, mais o mês:

| Página | Filtros |
|---|---|
| Brasil | Mercado, Setor fim, Canal, Responsável |
| NCC | Turno, Responsável |
| Hispana | País, Canal, Sector fin, Responsable. A página fica em espanhol, como no Tableau |
| CES | Canal, Responsável |

Clicar numa linha de Ofensores ou de Analistas filtra a página inteira, como as ações de filtro do Tableau. Os filtros
ativos aparecem como etiquetas que podem ser removidas.

## Desenho do painel novo

Uma página por operação, todas com a mesma estrutura:

1. **Indicadores do mês:**
   - C-SAT em destaque, com a meta e a variação em pontos percentuais contra o mês anterior;
   - C-SAT Simple;
   - Response Rate (respondidas de enviadas);
   - Respondidas, divididas em promotores, neutros e detratores.
2. **Evolução em 12 meses:** linhas de C-SAT e C-SAT Simple com a meta, no lugar dos medidores. Os valores também
   aparecem numa tabela que se abre.
3. **Do envio à promoção:** funil enviadas → respondidas → promotores.
4. **Respostas por mês:** colunas empilhadas por classificação.
5. **Distribuição das notas:** barra 100% por classificação e contagem por nota.
6. **Ofensores:** volume, detratores, % de detratores e C-SAT por categoria, ordenados por detratores.
7. **Analistas:** a mesma visão por responsável, com ordenação por qualquer coluna.
8. **Enquetes do mês:** detalhe com busca, filtro de classificação e páginas de 25 linhas. Tem as mesmas colunas da
   tabela do Tableau.

No CES, o destaque é o CES médio, e as classes aparecem como Fácil (4–5), Neutro (3) e Difícil (1–2).

## Validação

`ferramentas/validar_csat_mensal.py`, no `daily-experiencia`, calcula os indicadores com as fórmulas do workbook no
extract "Enquetes C-SAT" (30/10/2026) e na gold, por operação e mês.

**Resultado em 09/11/2026: todos os meses fechados batem, até set/2026.**

| Operação | Meses comparados | Meses iguais em todos os indicadores |
|---|---|---|
| Experiencia Brasil | 40 | 40 |
| Hispana | 25 | 25 |
| NCC | 23 | 23 |
| CES | 8 | 8 |

Out/2026 ficou de fora porque o extract foi tirado no dia 30. Os números do painel novo (C-SAT, Simple, Response Rate e
os volumes) foram conferidos nas quatro páginas, numa cópia local com os CSV exportados, contra a
`dexp_gold_csat_mensal`. Os meses conferidos foram Brasil e Hispana em nov/2026, NCC em out/2026 e CES em set/2026. Um
filtro (Mercado = CERRADO) foi conferido contra o cálculo direto no CSV.

Efeito da regra nova, que conta protocolos distintos em tudo:
- **Hispana, NCC e CES:** não muda nenhum mês.
- **Brasil:** muda em 3 meses, por protocolos com mais de uma enquete.

| Brasil | C-SAT Tableau | C-SAT novo | Promotores Tableau → novo | Respondidas Tableau → novo |
|---|---|---|---|---|
| dez/2024 | 80,78% | 80,59% | 412 → 411 | 514 → 510 |
| abr/2025 | 90,37% | 86,31% | 845 → 807 | 975 → 935 |
| set/2025 | 84,98% | 84,85% | 690 → 689 | 813 → 812 |

O CES respostas passa a ser 1/5 do que o gráfico mensal do Tableau mostrava (correção 2 abaixo).

Para validar de novo, baixe um extract novo de "Enquetes C-SAT" para `daily-experiencia\validacao\extracts_csat\` e,
a partir da pasta `daily-experiencia`, rode:
```powershell
.venv\Scripts\python.exe ferramentas\validar_csat_mensal.py --saida validacao\relatorios\csat_mensal.md
```

## Decisões (09/11/2026) e pontos a avaliar

| # | Tableau | Decisão | Situação |
|---|---|---|---|
| 1 | Brasil e Hispana contavam linhas; NCC contava protocolos | Tudo por protocolo distinto | **A avaliar no futuro.** Efeito na tabela acima |
| 2 | "CES – Total Respostas e Média" não filtrava a fatia, e o total saía 5× maior | Corrigido: respostas = protocolos com nota | Fechado |
| 3 | O painel NCC foi salvo com o intervalo de 01/01 a 31/03/2026 junto com o mês 11/2026, e abria vazio | Corrigido: só um seletor de mês, igual em todas as páginas | Fechado |
| 4 | Os ofensores do NCC agrupavam pelo status de finalização, e o título dizia "classificação" | Agrupa pelo status de classificação | **A avaliar no futuro** |
| 5 | O NCC só contava analistas da lista Analistas Enquetes. Em out/2026, isso deixava de fora 45 das 131 enquetes, de 4 analistas do NCC que não estavam na lista. Por isso, o Daily NCC e o Tableau davam números diferentes | A partir de out/2026, vale a regra do Daily NCC (protocolo na BASE MALASIA, sem "Teste"). Os meses até set/2026 não mudam | Decidido pelo Victor em 09/11/2026 |

Outros pontos encontrados:

- **Hispana sem enquetes de jul/2025 a jun/2026:** o extract do Tableau tem a mesma lacuna, então ela vem das planilhas
  de origem (`Enquete BASE MTK.xlsx` ou a lista de analistas).
- **CES com meses salteados:** só 8 meses entre jun/2025 e set/2026, e nada depois de set/2026. Conferir se a planilha
  `Enquete CES.xlsx` continua sendo atualizada.
- **Nome do cliente na planilha:** o Tableau já mostrava esse campo. Como a planilha fica no Drive, o acesso a ela
  precisa ficar restrito, por causa da LGPD.
- **Mês corrente parcial:** o mês atual aparece por padrão, como no Tableau. Volumes e variações comparam um mês
  incompleto com um mês fechado.
- **Diferenças da validação linha a linha de 30/10**, em `docs/validacao_csat.md`: um protocolo com
  `OIS Solução Aplicada` 434 × 435 e a grafia `_x008D_` no setor do NCC. Nenhum dos dois afeta os indicadores.

## O que falta (depende de OK)

- [x] `databricks bundle deploy` e o job só com a tarefa `gold_csat` (09/11/2026). As duas tabelas novas foram gravadas,
      com as mesmas contagens da `dexp_gold_csat_enquetes`.
- [x] Primeira exportação para a pasta do Drive (09/11/2026): 103 mil enquetes em 4 CSV mais o mensal.
- [x] Exportação incluída na rotina diária, depois do job: `rotina_manual.ipynb` (célula 5) e `rotina_diaria.ps1` do
      daily-experiencia (09/11/2026).
- [x] Planilha **Painel C-SAT** criada, Apps Script colado, `PASTA_CSAT_ID` configurado, primeira importação feita e app da
      Web publicado (09/11/2026):
      <https://script.google.com/a/macros/natura.net/s/AKfycbyHsn22MGj041T0fbGpOfGh2oxUGVd5uvtm3jnz4A6T6MU3PQCehw3j0oU6h2x11Nw/exec>.
      As 4 páginas conferem com o Databricks (Brasil nov/2026: 88,1% / 94,7% / 58,5% / 226; Hispana nov/2026:
      84,9% / 91,8% / 42,2%; CES set/2026: 4,26).
- [x] Na primeira versão, a Hispana levava uns 35 s para abrir e o Brasil uns 15 s, porque a página lia a aba inteira a
      cada acesso. Também o NCC abria em nov/2026, com 2 enquetes enviadas e nenhuma respondida. A versão 2 (09/11/2026)
      grava os pacotes prontos e abre no último mês com respostas. No painel publicado, a Hispana abre em menos de 5 s
      e o NCC abre em out/2026 (96,2% / 30,2% / 26).
- [ ] Conferir no painel o "Carregar meses anteriores…", que usa o pacote do histórico inteiro (coluna B). No teste local,
      esse pacote volta igual ao dados() antigo.
- [x] NCC com a regra do Daily NCC a partir de out/2026: gold e CSV atualizados em 09/11/2026. Out/2026 ficou em 131
      enviadas, 39 respondidas e 94,87%; antes eram 86, 26 e 96,15%.
- [ ] Tableau: o workbook GovEXP lê a fonte "Enquetes C-SAT", que sai do fluxo do Prep e não tem a regra nova. Para o
      Tableau mostrar a regra do Daily NCC, troque a fonte do workbook por "dexp - Enquetes C-SAT" (3. SANDBOX), que
      sai do Databricks e se atualiza às 09:30. **Versão local pronta em 12/11/2026** (etapa 1 abaixo).

## Próxima etapa: o Métricas da Excelência inteiro (reunião de 12/11/2026)

A reunião "Alinhamento: Evolução do Painel de Métricas de Excelência" (Juliana, Valéria, Suelen, Sabrina, Vico, Victor e
outros) definiu:

- **Tableau é o lugar do histórico e dos resultados fechados**, por ser a ferramenta oficial da Natura. **Apps Script é
  para o acompanhamento do dia a dia.** Para o C-SAT, isso dá dois usos da mesma gold: o Métricas no Tableau para a
  linha histórica e o Painel C-SAT em Apps Script para o mês corrente.
- **O Métricas vai ser reorganizado por bloco** (eficiência, produtividade, qualidade, monitoramento e contratuais). A
  Juliana vai recuperar a planilha de categorização feita pela Valéria em 2025. Qualidade (CES e C-SAT) fica num painel;
  produtividade e retenção, em outro.
- **NCC:** o Daily NCC (Apps Script do Diego) recebe a qualidade: nota geral de C-SAT, que já existe, e abas de
  incidente crítico, monitoring, torre, ECAB e monitoria WR, sem detalhe por analista. O detalhe por analista vai para
  um painel à parte, da operação e supervisão. Por isso as abas de QA saíram do Métricas em 12/11/2026.
- **Fórum semanal** com a Experiência a partir da semana de 16/11, para revisar o documento de páginas e necessidades
  da Valéria e priorizar. Tudo que for feito para o Brasil vale também para a Espanha.

### Fontes do Métricas (levantadas no .twbx de 12/11/2026)

| Painel | Fonte de produção | No Databricks |
|---|---|---|
| C-SAT Brasil, C-SAT NCC, C-SAT OIS, CES | Enquetes C-SAT | `dexp - Enquetes C-SAT` (`dexp_vw_csat_enquetes`) |
| PRODUTIVIDADE EXP. BRASIL, RETENCAO EXP. BRASIL | Experiencia Brasil Nivel | `dexp - Experiencia Brasil Nivel` (`dexp_vw_mkt_experiencia_brasil_nivel`) |
| PRODUTIVIDADE EXP. HISPANA | Experiencia Hispana Produtividade | `dexp - Experiencia Hispana Produtividade` (`dexp_vw_hispana_produtividade`) |
| QA Brasil (removido) | GovEXP_QA_BR_V2, GovEXP_QA_BR_V2_MediaFinal | Não |
| QA Hispana (removido) | GovEXP_QA_OIS_V2, GovEXP_QA_OIS_V2_MediaFinal | Não |
| QA NCC IC, QA NCC IC por Analista (removidos) | QA_IC_SEV3_Base_Consolidada, _Apontamentos, _Analistas | Não |
| QA Monitoring (removido) | QA Gestao de Alertas | Não |
| QA Incidentes N1 (removido) | QA Incidentes N1 | Não |
| QA Mudancas (removido) | QA Mudancas TT | Não |
| QA Monitoria WR (removido) | QA Monitoria WR | Não |

Os 8 painéis que ficaram no Métricas já têm todas as fontes no Databricks. Só as fontes de QA estão fora.

### Etapas

1. **Métricas no Databricks.** `metricas-excelencia/GovEXP - Métricas da Excelência - Databricks.twbx` é o Métricas sem
   QA com as três fontes trocadas pelas `dexp -`, gerado por `ferramentas/ligar_fontes_publicadas_tableau.py`. Todas as
   colunas que o workbook declara existem nas views, menos `Pedido Finalizado` (Experiencia Brasil Nivel), que nenhuma
   planilha usa. Diferença esperada: NCC a partir de out/2026 com a regra do Daily NCC.
   - [x] Publicado em 3. SANDBOX como **"GovEXP - Métricas da Excelência - Databricks"** (12/11/2026) e comparado
         com o de produção. Imagens dos 8 painéis e contagem por analista nas fontes de novembro:
         - Ficha de Relatório, CES e C-SAT Brasil: imagens idênticas.
         - C-SAT NCC: muda só o mês de out/2026, pela regra do Daily NCC (esperado).
         - Produtividade Brasil, Retenção Brasil, Produtividade Hispana e C-SAT OIS: os totais batem (Brasil 1.723,
           Hispana 1.790 em nov/2026). Muda só a grafia de 4 analistas: "Gabrielle Tenorio" × "Gabrielle tenorio",
           "Haryssa Nayanne da Silva Santana" × "Da Silva", "Maria Belen La Giglia Luque" × "MARIA BELEN…" e
           "…Rodríguez berro" × "Berro". O painel filtra ou agrupa pelo nome, então a pessoa perde linhas ou aparece
           duas vezes.
         - Causa: no Remapear do Prep, o valor igual ao nome do grupo (sem diferenciar maiúsculas) também entra no
           grupo e sai com a grafia do grupo. O `remapear` de `src/dexp/tableau.py` não fazia isso. Corrigido em
           12/11/2026, com teste. Deploy, job e as 3 fontes `dexp -` republicados no mesmo dia.
         - Segunda comparação (12/11/2026): Ficha, CES, C-SAT Brasil, C-SAT OIS e Retenção Brasil idênticos; NCC
           com a diferença esperada. Produtividade Hispana: mesmos números, só a ordem de "MARÍA INÉS" e "MARIA
           ISABEL" troca. Produtividade Brasil: some a linha de "Gabrielle tenorio" (34 atendimentos em nov/2026).
         - Causa do que sobrou: os filtros do workbook guardam o nome com uma grafia fixa ("Gabrielle Tenorio" em
           umas planilhas, "Gabrielle tenorio" em outras). A fonte de produção usa a collation `LPT_RBR_S2`
           (português, sem diferenciar maiúsculas), então as duas grafias batem. As fontes `dexp -` são gravadas por
           `coleta/publicar_tableau.py` com collation `binary`, que diferencia maiúsculas e ordena os acentos no fim.
         - Decisão (Victor, 12/11/2026): gravar as fontes `dexp -` com a collation do Prep. `publicar_tableau.py`
           passou a gravar os textos com `pt_BR_CI` no Hyper e `LPT_RBR_S2` na definição da fonte, como as
           extrações do Prep. Vale para todas as fontes `dexp -` a partir da próxima publicação.
         - Terceira comparação (12/11/2026), com as 3 fontes republicadas: os 7 painéis ficam idênticos à produção.
           A única diferença é a esperada, no C-SAT NCC de out/2026.
         - **Limite:** a atualização agendada do Tableau Cloud (todo dia às 09:30) relê o Databricks e volta a
           collation para `binary`, tanto no Hyper quanto na definição. Foi testado em 12/11/2026 na "dexp - Ticket
           Medio Hispana", com a agenda adiantada para as 14:45 e depois devolvida para 09:30. A collation do Prep só
           fica valendo até a próxima atualização agendada. O site também não permite disparar uma atualização à mão
           (erro 409082).
         - Decisão (Victor, 12/11/2026): sem atualização agendada; as fontes `dexp -` são publicadas todo dia pelo
           script. As 28 atualizações agendadas foram apagadas em 12/11/2026. `publicar_tableau.py` passou a apagar a
           agenda que encontrar, no lugar de criar uma. A publicação é a última célula do `rotina_manual.ipynb` e
           também o fim do `rotina_diaria.ps1`. O job só roda quando a rotina roda, então a agenda não trazia dado
           novo. As outras 25 fontes `dexp -` ganham a collation do Prep na próxima publicação diária.
   - [ ] Depois do OK, publicar por cima do Métricas de produção. Com isso, o fluxo Prep "GovEXP - Metricas de
         Excelencia - CSAT" pode ser desligado.
2. **Divisão por bloco.** Separar qualidade (CES, C-SAT) de produtividade e retenção, com os nomes da planilha de
   categorização. Esperar a planilha da Juliana para não refazer os nomes.
3. **QA no Databricks.** Levar as fontes de QA para o pipeline, como foi feito com o C-SAT: levantar de onde vem cada
   uma (fluxo do Prep ou planilha), especificar, gerar a gold e validar. É o que alimenta as abas de qualidade do Daily
   NCC e, para Brasil e Hispana, a linha histórica de qualidade que a Valéria quer no Tableau.
4. **Fórum.** Levar ao primeiro fórum um mapa de cada painel atual: para onde vai (Tableau histórico, Apps Script dia
   a dia ou painel por analista) e se já está no Databricks. Cruzar com o documento da Valéria quando a Juliana
   compartilhar. O documento dela ("Revisão dos Dash no Tableau", CDES-2708) já foi cruzado com a versão Databricks
   do Daily em `../daily-experiencia/docs/revisao_dash_valeria.md`.
