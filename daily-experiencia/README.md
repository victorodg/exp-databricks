# Daily Experiência BR no Databricks

Migração dos fluxos Tableau Prep **"Daily - Experiencia BR - MKT"** e **"Daily Experiencia BR - Dynamics e Resenhas"** para o Databricks. Os dashboards continuam no Tableau Cloud, passando a ler as tabelas do Databricks.

## Arquitetura

```
 Máquina local (diária)                       Databricks (AWS) – sandbox.sustentacao_bau_experiencias
 ───────────────────────                      ─────────────────────────────────────────────────────────
 Selenium MKTZap ──┐                          Volume de entrada (arquivos como chegaram)
 .xlsx do Drive  ──┼── upload (CLI/SDK) ───►       │
 Google Sheets*  ──┘                               ▼
                                              bronze   arquivo bruto lido como texto + metadados de carga
                                                   ▼
                                              silver   limpeza, tipos, nomes corrigidos, regras de negócio
                                                   ▼
                                              gold     uma tabela por saída usada no Tableau
                                                   ▼
                                              SQL Warehouse (serverless) ──► Tableau Cloud
```

\* As Google Sheets nativas precisam ser exportadas para .xlsx antes do upload (não há API do Google Drive disponível).

Orquestração: um Job do Databricks em que o ramo **Dynamics** roda antes do **MKT**, porque a saída "Dynamics Nivel" é entrada do fluxo MKT.

## Decisões

- Escopo: só os dois fluxos acima. OIS, CSAT, Hispana e NCC ficam para depois.
- A coleta continua na máquina local, rodada diariamente. A API do MKTZap ainda não é confiável, então o Selenium continua.
- As regras fixas do Prep (datas de corte, exclusões pontuais, feriados) são mantidas como estão e viram tabelas de parâmetros.
- Nomes de colunas podem ser corrigidos (ex.: `ResponsÃ¡vel`), mas os **números têm que bater** com os extracts atuais.
- Validação: o pipeline novo roda em paralelo ao fluxo de produção, que não é alterado.
- Carga inicial do histórico a partir das planilhas consolidadas oficiais (ex.: `EXP BR\MKT\MKT_Reativos.xlsx`). Depois disso, entram só os brutos diários.
- LGPD/mascaramento: fora do escopo por enquanto.

## Estrutura

| Caminho | Conteúdo |
|---|---|
| `databricks.yml` | Definição do bundle (ambientes, catálogo e schema) |
| `docs/inventario.md` | Fontes, saídas, dependências e regras fixas dos fluxos atuais |
| `docs/fluxos/` | Especificação de cada fluxo do Prep (etapas em ordem, fórmulas completas), gerada do `.tfl` |
| `docs/validacao_*.md` | Resultado da comparação com os extracts do Tableau e decisões tomadas |
| `resources/daily_experiencia.job.yml` | Job `dexp_daily_experiencia`: bronze → silver → gold Dynamics e Resenhas → gold MKT |
| `src/bronze/carregar_bronze.py` | Notebook da camada bronze |
| `src/silver/carregar_silver.py` | Notebook da camada silver (definições em `src/dexp/silver.py`) |
| `src/gold/dynamics_e_resenhas.py`, `src/gold/mkt.py` | Notebooks da gold, um por fluxo do Prep; cada bloco cita a etapa da especificação |
| `src/dexp/fontes.py` | De onde vem cada tabela bronze (pasta no volume e aba) |
| `src/dexp/leitura.py` | Leitura dos CSV do MKTZap e dos .xlsx como texto |
| `src/dexp/tableau.py`, `src/dexp/prep.py`, `src/dexp/nomes.py` | Equivalentes das funções do Tableau e das operações do Prep (join com os mesmos sufixos -1/-2) |
| `src/dexp/regras_mkt.py` | Listas grandes do fluxo MKT, extraídas do `.tfl` por `ferramentas/extrair_regras_mkt.py` |
| `ferramentas/` | Gerador de especificação, comparação com extracts, carga do histórico do Backlog |
| `tests/` | Testes locais (ver abaixo) |
| `coleta/fontes.toml` | Origem de cada arquivo enviado ao volume de entrada |
| `coleta/enviar_arquivos.py` | Envia brutos do MKTZap, .xlsx do Drive e cópias das Google Sheets para o volume |
| `coleta/google_sheets/exportar_planilhas.gs` | Apps Script que exporta diariamente as 12 Google Sheets para .xlsx em `G:\Meu Drive\dexp_google_sheets` |

## Rotina diária

O pipeline não depende de nada do Tableau Prep: lê só os arquivos do volume e as próprias tabelas gold.

1. 9h (com até ~15 min de folga): o Apps Script exporta as 12 Google Sheets para `G:\Meu Drive\dexp_google_sheets`
   e grava `_ultima_exportacao.json` com o horário e o resultado.
2. Rodar o notebook do Selenium (`logic\mktzap\new_pipeline_mktzap.ipynb`) como hoje.
3. Abrir `coleta\rotina_manual.ipynb` no VS Code (abrindo a pasta `logic-local`, o Python do `.venv` já vem escolhido)
   e rodar as células em ordem: confere a exportação das Google Sheets, envia os arquivos, dispara o job
   `dexp_daily_experiencia` (bronze → silver → gold, uns 15 minutos), acompanha e mostra as tabelas atualizadas.

Quando a rotina for ficar automática, a tarefa agendada roda `coleta\rotina_diaria.ps1` (mesmo envio + job, com log
em `coleta\.estado\logs\`). Pela linha de comando, a partir da pasta `daily-experiencia`:

```powershell
powershell -ExecutionPolicy Bypass -File coleta\rotina_diaria.ps1            # envia e dispara o job
powershell -ExecutionPolicy Bypass -File coleta\rotina_diaria.ps1 --aguardar # idem, esperando o job terminar
```

O envio só manda arquivos novos ou alterados (compara o SHA-256 com o último envio, guardado em
`coleta\.estado\manifesto.json`) e nunca apaga nada. Com erro em algum envio, o job não é disparado.
Outras opções de `coleta\enviar_arquivos.py`: `--sem-job`, `--simular`, `--somente mktzap drive google_sheets`.

Agendar (ou mudar o horário): `powershell -ExecutionPolicy Bypass -File coleta\agendar_rotina.ps1 -Horario 09:40`.

## Volume de entrada

`/Volumes/sandbox/sustentacao_bau_experiencias/dexp_landing`

| Caminho | Conteúdo |
|---|---|
| `mktzap/<operação>/<AAAAMM>/bruto_<relatório>_<de>_a_<até>.csv` | Brutos do Selenium, um por execução (brasil, hispana, ncc) |
| `drive/<fonte>/<AAAA-MM-DD>/<arquivo>.xlsx` | Uma pasta por versão nova de cada planilha do Drive, com a data da captura |
| `google_sheets/<fonte>/<AAAA-MM-DD>/<fonte>.xlsx` | Idem, para as cópias das Google Sheets |

A data das pastas é a da captura porque o Google Drive para desktop reescreve a data de alteração dos arquivos quando os baixa.

## Camada bronze

Uma tabela `dexp_bronze_<tabela>` por fonte listada em `src/dexp/fontes.py`:

- **Planilhas:** a versão mais recente no volume substitui a tabela inteira, como o Tableau Prep faz ao ler a planilha.
- **MKTZap:** o bruto mais recente de cada mês (cada bruto traz o mês inteiro até o dia da coleta).
- Todas as colunas como texto, com nomes em snake_case sem acento. O nome original de cada coluna fica em `dexp_bronze_colunas`.
- Colunas de controle: `_linha` (linha no arquivo de origem), `_arquivo`, `_versao` e `_carregado_em`.
- A tabela só é regravada quando o arquivo de origem muda. O parâmetro `forcar = sim` regrava tudo.

```powershell
databricks bundle deploy -t dev -p daily-exp
databricks bundle run dexp_daily_experiencia -t dev -p daily-exp
```

## Ambiente Databricks

- Workspace (AWS): `https://dbc-02543f96-daa5.cloud.databricks.com`, perfil da CLI `daily-exp` (login OAuth pelo navegador).
- Schema `sandbox.sustentacao_bau_experiencias`: o grupo `DAHUB_DATABRICKS_CENTRAL_EXPERIENCIAS_CORE` tem ALL PRIVILEGES. No catálogo `sandbox` só há USE_CATALOG, então não é possível criar schemas e tudo fica neste schema.
- O schema é compartilhado com outros projetos, inclusive tabelas de MKT e resenhas criadas por outra pessoa. Os objetos deste projeto usam o prefixo `dexp_` para não colidir.
- SQL Warehouse: `sustentacao_bau_experiencias_sandbox_sql` (serverless, 2X-Small, desliga após 2 min parado).
- Jobs: o usuário não tem permissão para computação serverless em jobs. Os jobs rodam no cluster all-purpose do time, `sustentacao_bau_experiencias_sandbox_python` (DBR 16.4, 1 worker, desliga após 20 min parado).

## Preparar a máquina (uma vez)

```powershell
winget install --id Git.Git -e --scope user --source winget
winget install --id Databricks.DatabricksCLI -e --source winget
databricks auth login --host https://dbc-02543f96-daa5.cloud.databricks.com --profile daily-exp
python -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
databricks bundle validate -t dev
```

## Testes locais

- `.venv\Scripts\python.exe -m pytest`: leitura dos arquivos e regra de nomes do Prep (sem Spark).
- `.venv-spark\Scripts\python.exe -m pytest`: tudo, inclusive as funções que emulam o Tableau, com Spark local.
  O `.venv-spark` usa Python 3.12 e PySpark 3.5 (a versão do DBR 16.4), porque o PySpark 3.5 não roda no Python 3.14,
  e precisa de Java (o Java 8 já instalado serve). Para recriar:

```powershell
.venv\Scripts\python.exe -m pip install uv
.venv\Scripts\uv.exe python install 3.12
& "$env:APPDATA\uv\python\cpython-3.12.16-windows-x86_64-none\python.exe" -m venv .venv-spark
.venv-spark\Scripts\python.exe -m pip install -r requirements.txt "pyspark==3.5.*"
```

## Validação contra o Tableau

Baixe os extracts (.tdsx) do Tableau Cloud para `validacao\extracts\` (fora do Git) e rode, no Git Bash:

```bash
sh ferramentas/comparar_mkt.sh
```

Para as saídas do Dynamics, `ferramentas/comparar_extract.py <extract> <tabela gold>`. Os resultados ficam em `validacao\relatorios\`.
