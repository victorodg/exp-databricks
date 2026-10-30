# Automação MKTZap – Como funciona

## Para que serve

Todo mês, os times precisam de três relatórios do MKTZap (a plataforma de atendimento por WhatsApp da Natura) para alimentar os dashboards do Tableau:

- **Analítico** – lista dos atendimentos realizados.
- **Enquetes** – respostas da pesquisa de satisfação (C-SAT) enviada aos clientes.
- **Tickets** – histórico dos tickets abertos e finalizados.

Fazer isso à mão significa entrar no sistema, trocar de empresa, gerar e baixar cada relatório, ajustar as planilhas e colar os dados nas bases. A automação faz tudo isso sozinha, para as três operações (empresas): **27 - Brasil**, **1531 - Hispana** e **1990 - NCC**.

---

## Parte 1 – Coleta dos relatórios (o "robô" no navegador)

O robô abre o Google Chrome e navega pelo MKTZap como uma pessoa faria.

1. **Define o período.** Sempre do dia 1º do mês atual até hoje. Se o mês anterior ainda não foi fechado, ele também é baixado de novo, inteiro (veja [Virada do mês](#virada-do-mês)). Nesse caso, todos os passos abaixo são feitos para os dois períodos.
2. **Entra no site** https://natura.mktzap.com.br. O Chrome usado pela automação guarda o login. Na primeira vez, alguém precisa entrar manualmente com usuário e senha; depois disso, a sessão se mantém.
3. **Repete os passos abaixo para cada operação** (27 - Brasil, depois 1531 - Hispana, depois 1990 - NCC):
   1. Troca para a empresa correspondente, pelo menu do usuário ("Alterar empresa"):
      - 27 - Brasil → "27 - Natura - CN"
      - 1531 - Hispana → "1531 - Natura - Experiencia CN OIs"
      - 1990 - NCC → "1990 - Natura - NCC"
   2. **Relatório Analítico:** abre a tela de relatórios analíticos, escolhe o atalho de período "Este mês" (ou "Mês passado", quando está baixando o mês anterior inteiro), seleciona o formato CSV e clica em "Gerar Relatório". O MKTZap processa em segundo plano, então o robô abre a fila de "Relatórios em Background", espera aparecer o status **Finalizado** e clica em baixar.
   3. **Relatório de Enquetes:** abre a tela de enquetes, preenche as datas e escolhe a enquete de satisfação certa para cada operação:
      - Brasil: "C-SAT (Experiência CNF)"
      - Hispana: "C-SAT - Satisfaccion"
      - NCC: "C-SAT - NCC (New)"

      Depois clica em "Baixar detalhes da enquete" e baixa o arquivo da fila de background, do mesmo jeito do Analítico.
   4. **Relatório de Tickets:** abre o histórico de tickets, preenche as datas, clica em gerar e o arquivo é baixado direto.
4. **Guarda cada arquivo baixado** na pasta `downloads_brutos\<AAAAMM>\<operação>\`, onde `<AAAAMM>` é o mês do período, com nome como `bruto_analitico_20261001_a_20261022.csv`. Esses arquivos são a cópia exata do que o MKTZap entregou e **nunca são alterados**.
5. **Fecha o navegador e confere o resultado.** Mostra uma lista com os 9 arquivos esperados por período (3 relatórios × 3 operações; 18 quando o mês anterior também é baixado), indicando se cada um foi baixado, o tamanho e se parece mesmo um relatório. Falhas ficam listadas na tela. Por fim, apaga as pastas temporárias de download.

Cuidados que o robô já tem: espera o download terminar por completo antes de mover o arquivo, aguarda até 3 minutos por download e até 5 minutos pelo processamento em segundo plano. Se não conseguir trocar para a empresa certa, pula aquela operação, para nunca gravar dados de uma empresa na pasta de outra.

---

## Parte 2 – Tratamento das bases

Para cada operação e cada relatório, o processo é o mesmo: pegar o arquivo bruto, deixá-lo no padrão da base consolidada e gerar um arquivo "pronto" (chamado de **Gold**).

### Tratamentos aplicados em todos os relatórios

- **Limpeza dos textos.** O MKTZap entrega alguns textos com caracteres quebrados, como `N&#195;O` no lugar de "NÃO". O robô corrige para o texto certo (acentos, símbolos e emojis) e troca quebras de linha dentro de uma célula por espaço, além de remover espaços sobrando nas pontas.
- **Mesmas colunas da base consolidada.** O robô olha o cabeçalho da planilha consolidada e organiza o arquivo novo com as mesmas colunas, na mesma ordem. Colunas que existem só no bruto são descartadas. Colunas que existem só na base ficam vazias.

### Tratamentos específicos

| Base | Tratamento adicional |
|---|---|
| **Analítico Brasil** | Aplica a regra da coluna "Qtd Atendimentos": se estiver vazia, não for número, for zero/negativa ou for 100 ou mais, o valor passa a ser **1**. Nos demais casos, mantém o número. |
| **Analítico Hispana** | A coluna "PEDIDOS FINALIZADOS" é renomeada para "Pedidos Finalizados", como está na base. |
| **Analítico NCC** | Organiza as colunas conforme a base "BASE MALASIA". A coluna "telefone" é descartada e as duas colunas chamadas "Nome" ficam cada uma na sua posição. |
| **Enquetes (as 3 operações)** | A coluna "Responsável" é renomeada para "ResponsÃ¡vel" (grafia que já existe nas bases, mantida para não alterar o histórico). |
| **Tickets (Brasil e Hispana)** | Apenas a limpeza de texto e o alinhamento de colunas. |

### Arquivos Gold

O arquivo tratado é salvo como CSV com nome no formato:

`AAAA-MM-DD-<operação>-<relatório>-periodo-<data início>-a-<data fim>.csv`

A primeira data é sempre o dia em que a automação rodou. Exemplos:

- `2026-10-22-brasil-analitico-periodo-2026-10-01-a-2026-10-22.csv` (mês atual)
- `2026-11-03-brasil-analitico-periodo-2026-10-01-a-2026-10-31.csv` (outubro inteiro, baixado em 03/11 no fechamento)

O Gold é gerado a partir do arquivo bruto **daquele período e daquela execução**. Se o download falhou, a automação para com erro em vez de usar um arquivo bruto antigo.

Se já existir um arquivo com o mesmo nome (por exemplo, uma segunda execução no mesmo dia), a versão antiga não é apagada: ela é guardada ao lado com o sufixo `.anterior_<hora>`.

---

## Parte 3 – Atualização das bases consolidadas (planilhas Excel)

Depois de gerar o Gold, a automação atualiza a planilha histórica de cada base. A lógica é sempre a mesma, em três passos:

1. **Abre a planilha** e localiza as linhas do **mês atual** (e também do mês anterior, quando ele foi baixado de novo nesta execução).
2. **Remove essas linhas.** Elas são substituídas porque o relatório do mês é baixado completo a cada execução, e assim os dados não duplicam.
3. **Cola todas as linhas dos arquivos Gold** e salva por cima da mesma planilha (mesmo nome e mesmo arquivo no Drive).

**Os demais meses não são alterados.** Datas, números e horários são gravados como valores reais do Excel (e não como texto), e a formatação original das colunas é mantida.

O mês é identificado por uma coluna diferente em cada base:

| Base | Coluna usada para identificar o mês |
|---|---|
| Analítico | Data Contato |
| Enquetes | Enviado em (data de envio da pesquisa) |
| Tickets | Data de Criação do Ticket |

---

## Virada do mês

A última execução de um mês quase nunca pega o mês inteiro: o dia 1º pode cair num fim de semana ou feriado prolongado, e mesmo uma execução no dia 31 não pega as últimas horas. Por isso, a automação confere sozinha se o mês anterior já foi **fechado**.

**Como ela decide.** Um mês está fechado quando as 8 bases tratadas (3 do Brasil, 3 da Hispana e 2 do NCC) têm um arquivo Gold do mês inteiro gerado **depois** do último dia do mês. A data da execução está no começo do nome do Gold, então não é preciso nenhum controle extra, nem um calendário de feriados.

- **Mês anterior fechado:** baixa e atualiza só o mês atual, como sempre.
- **Mês anterior não fechado:** baixa de novo o mês anterior **inteiro** e o mês atual, gera os Golds dos dois e atualiza as planilhas substituindo as linhas dos dois meses de uma só vez.

Exemplo: o dia 1º/11 cai num domingo e a última execução de outubro foi na sexta, 30/10. Na segunda, 02/11, a automação vê que outubro não está fechado e baixa outubro inteiro e mais o dia 02/11. Na terça, outubro já consta como fechado e só novembro é baixado.

Essa conferência só é feita **até o dia 10** do mês, para não refazer sem querer um mês antigo. Depois disso, se o mês anterior não estiver fechado, a automação só mostra um aviso.

**Escolha manual.** Na Célula 1, a opção `MES_REF` aceita:

| Valor | O que baixa |
|---|---|
| `None` (padrão) | Automático, como descrito acima |
| `"mes_atual"` | Só o mês atual |
| `"mes_anterior"` | Só o mês anterior inteiro |
| `"ambos"` | Mês anterior inteiro + mês atual, sem conferir nada |

O limite de 10 dias fica em `JANELA_FECHAMENTO_DIAS`, também na Célula 1.

---

## Onde os arquivos ficam salvos

**Pasta raiz no Drive compartilhado:**
`G:\Drives compartilhados\REPÓSITORIOS - DOCUMENTAÇÕES\Dashboards - Tableau\Central de EXP e Serviços\Fontes de Dados\auto\mktzap`

| O quê | Onde |
|---|---|
| Arquivos brutos (como vieram do MKTZap) | `downloads_brutos\<AAAAMM>\<operação>\` na pasta onde o notebook roda (máquina local) |
| Arquivos Gold (tratados) | `<pasta raiz>\pre-processing\<AAAAMM>\<operação>\` (`<AAAAMM>` = mês do período) |
| Planilhas consolidadas (o resultado final, que alimenta o Tableau) | Pastas oficiais de `Fontes de Dados`, na tabela abaixo |

**Planilhas consolidadas atualizadas** (desde 30/10/2026, gravadas direto nas pastas oficiais, sem passar por `auto\mktzap\<operação>\`):

| Operação | Analítico | Enquetes | Tickets |
|---|---|---|---|
| 27 - Brasil | `EXP BR\MKT\MKT_Reativos.xlsx` | `Enquetes\Enquete MKT REATIVOS.xlsx` | `EXP BR\MKT\Tickets Brasil.xlsx` |
| 1531 - Hispana | `EXP OIS\MKT\MKT Analitico Hispana.xlsx` | `Enquetes\Enquete BASE MTK.xlsx` | `EXP OIS\MKT\Tickets Hispana.xlsx` |
| 1990 - NCC | `Enquetes\BASE MALASIA.xlsx` | `Enquetes\Enquete Malasia.xlsx` | *(ver observação abaixo)* |

---

## Pontos de atenção

- **Tickets do NCC:** o robô baixa o relatório de Tickets do NCC, mas ele ainda **não é tratado nem consolidado** em nenhuma planilha. Fica apenas como arquivo bruto.
- **Primeiro acesso:** é preciso fazer o login manual no MKTZap uma vez. Não entre com a conta Google nesse Chrome.
- **Reexecução:** pode ser feita a qualquer momento no mesmo mês. As linhas do mês são sempre substituídas, sem duplicar.
- **Fechamento do mês:** é automático (veja [Virada do mês](#virada-do-mês)). Basta rodar normalmente no primeiro dia útil do mês. Se essa execução falhar, a próxima tenta de novo, até o dia 10.
- **Atalho "Mês passado" do Analítico:** no fechamento, o robô clica no atalho "Mês passado" da tela de relatórios analíticos. Esse atalho preenche do dia 1º ao último dia do mês anterior (conferido na tela em 26/10/2026). Se o MKTZap mudar o nome do botão, o Analítico do mês anterior falha e aparece na lista de falhas da conferência. Enquetes e Tickets não usam atalho: as datas são digitadas nos campos.
- **Conferência:** ao final da coleta, a automação mostra quais arquivos foram baixados e quais falharam. Vale olhar essa lista antes de usar os dados.
