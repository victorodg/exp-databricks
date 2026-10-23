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
| `coleta/google_sheets/exportar_planilhas.gs` | Apps Script que exporta diariamente as 12 Google Sheets para .xlsx no Drive |

## Ambiente Databricks

- Workspace (AWS): `https://dbc-02543f96-daa5.cloud.databricks.com`, perfil da CLI `daily-exp` (login OAuth pelo navegador).
- Schema `sandbox.sustentacao_bau_experiencias`: o grupo `DAHUB_DATABRICKS_CENTRAL_EXPERIENCIAS_CORE` tem ALL PRIVILEGES. No catálogo `sandbox` só há USE_CATALOG, então não é possível criar schemas e tudo fica neste schema.
- O schema é compartilhado com outros projetos, inclusive tabelas de MKT e resenhas criadas por outra pessoa. Os objetos deste projeto usam o prefixo `dexp_` para não colidir.
- SQL Warehouse: `sustentacao_bau_experiencias_sandbox_sql` (serverless, 2X-Small).

## Primeiros passos

```powershell
databricks auth login --host https://dbc-02543f96-daa5.cloud.databricks.com --profile daily-exp
databricks bundle validate -t dev
```
