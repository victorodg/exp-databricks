/**
 * Painel C-SAT (GovEXP) em Apps Script.
 *
 * Projeto vinculado à planilha do painel. Faz duas coisas:
 *  1. importarCsat(): lê os CSV que csat/coleta/exportar_sheets.py grava na pasta do Drive e regrava as abas
 *     dados_<operação>, mensal e _atualizacao, além das abas ocultas _pacote_<operação> (os dados já prontos para a
 *     página). Roda todo dia pelo acionador criado por criarAcionador(); forcarImportacao() importa na hora.
 *  2. doGet(): publica uma página por operação (?pagina=brasil|ncc|hispana|ces) e um índice sem parâmetro.
 *
 * Propriedade do script obrigatória (Configurações do projeto > Propriedades do script):
 *  PASTA_CSAT_ID = ID da pasta "Fontes de Dados\auto\csat" no Drive compartilhado.
 *
 * Regras dos indicadores: csat/README.md.
 */

var PAGINAS = {
  brasil: {
    titulo: 'C-SAT Brasil', fonte: 'Experiencia Brasil', idioma: 'pt', tipo: 'csat',
    filtros: [['mercado', 'Mercado'], ['setor_fim', 'Setor fim'], ['canal', 'Canal'], ['responsavel', 'Responsável']],
    ofensor: ['funcao_do_sistema', 'Função do sistema'],
    detalhe: [['protocolo', 'Protocolo'], ['enviado_em', 'Enviado em'], ['respondido_em', 'Respondido em'], ['time', 'Time'],
      ['mercado', 'Mercado'], ['nome', 'Nome'], ['responsavel', 'Responsável'], ['c_sat', 'C-SAT'], ['nota', 'Nota'],
      ['canal', 'Canal'], ['funcao_do_sistema', 'Função do sistema'], ['status_de_classificacao', 'Status de classificação'],
      ['status_de_finalizacao', 'Status de finalização'], ['primeiro_tempo_de_espera', 'Primeiro tempo de espera'],
      ['setor_fim', 'Setor fim'], ['chamado', 'Chamado'], ['funcao', 'Função']]
  },
  ncc: {
    titulo: 'C-SAT NCC', fonte: 'NCC', idioma: 'pt', tipo: 'csat',
    filtros: [['turno', 'Turno'], ['responsavel', 'Responsável']],
    ofensor: ['status_de_classificacao', 'Status de classificação'],
    detalhe: [['protocolo', 'Protocolo'], ['enviado_em', 'Enviado em'], ['respondido_em', 'Respondido em'], ['turno', 'Turno'],
      ['nome', 'Nome'], ['responsavel', 'Responsável'], ['c_sat', 'C-SAT'], ['nota', 'Nota'], ['canal', 'Canal'],
      ['funcao_do_sistema', 'Function'], ['status_de_classificacao', 'Status de classificação'],
      ['status_de_finalizacao', 'Status de finalização'], ['setor_entrada', 'Setor entrada'],
      ['solucao_aplicada', 'Solution applied'], ['setor_fim', 'Setor fim']]
  },
  hispana: {
    titulo: 'C-SAT Hispana', fonte: 'Hispana', idioma: 'es', tipo: 'csat',
    filtros: [['pais', 'País'], ['canal', 'Canal'], ['setor_fim', 'Sector fin'], ['responsavel', 'Responsable']],
    ofensor: ['funcao_do_sistema', 'Función del sistema'],
    detalhe: [['protocolo', 'Protocolo'], ['enviado_em', 'Enviado'], ['respondido_em', 'Respondido'], ['pais', 'País'],
      ['nome', 'Nombre'], ['responsavel', 'Responsable'], ['c_sat', 'C-SAT'], ['nota', 'Nota'],
      ['canal_de_entrada', 'Canal de entrada'], ['funcao_do_sistema', 'Función del sistema'],
      ['status_de_classificacao', 'Estado de clasificación'], ['status_de_finalizacao', 'Estado de finalización'],
      ['tempo_ate_ser_atendido', 'Tiempo hasta ser atendido'], ['tempo_de_operacao', 'Tiempo de operación'],
      ['tempo_do_atendimento', 'Tiempo de atención'], ['tempo_medio_de_espera', 'Tiempo medio de espera'],
      ['solucao_aplicada', 'Solución aplicada'], ['setor_fim', 'Sector fin']]
  },
  ces: {
    titulo: 'CES – Índice de Esforço do Cliente', fonte: 'CES', idioma: 'pt', tipo: 'ces',
    filtros: [['canal', 'Canal'], ['responsavel', 'Responsável']],
    ofensor: ['funcao_do_sistema', 'Função do sistema'],
    detalhe: [['protocolo', 'Protocolo'], ['enviado_em', 'Enviado em'], ['respondido_em', 'Respondido em'], ['time', 'Time'],
      ['nome', 'Nome'], ['responsavel', 'Responsável'], ['nota', 'Nota'], ['canal', 'Canal'],
      ['funcao_do_sistema', 'Função do sistema'], ['status_de_classificacao', 'Status de classificação'],
      ['status_de_finalizacao', 'Status de finalização']]
  }
};

var META_CSAT = 0.7;          // campo [Meta] do workbook
var MESES_INICIAIS = 24;      // a página carrega os últimos 24 meses; o resto só quando pedido
var LINHAS_POR_ESCRITA = 5000;

// ---------------------------------------------------------------- Importação

function planilha_() {
  var id = PropertiesService.getScriptProperties().getProperty('PLANILHA_ID');
  return id ? SpreadsheetApp.openById(id) : SpreadsheetApp.getActiveSpreadsheet();
}

function pastaCsat_() {
  var id = PropertiesService.getScriptProperties().getProperty('PASTA_CSAT_ID');
  if (!id) throw new Error('Defina a propriedade do script PASTA_CSAT_ID com o ID da pasta Fontes de Dados\\auto\\csat.');
  return DriveApp.getFolderById(id);
}

function arquivo_(pasta, nome) {
  var it = pasta.getFilesByName(nome);
  if (!it.hasNext()) throw new Error('Arquivo não encontrado na pasta do CSAT: ' + nome);
  return it.next();
}

/** Regrava uma aba inteira com as linhas do CSV, tudo como texto (as datas ficam como AAAA-MM-DD). */
function gravarAba_(ss, nome, linhas) {
  var aba = ss.getSheetByName(nome) || ss.insertSheet(nome);
  aba.clear();
  var colunas = linhas[0].length;
  if (aba.getMaxRows() < linhas.length) aba.insertRowsAfter(aba.getMaxRows(), linhas.length - aba.getMaxRows());
  if (aba.getMaxColumns() < colunas) aba.insertColumnsAfter(aba.getMaxColumns(), colunas - aba.getMaxColumns());
  aba.getRange(1, 1, linhas.length, colunas).setNumberFormat('@');
  for (var i = 0; i < linhas.length; i += LINHAS_POR_ESCRITA) {
    var parte = linhas.slice(i, i + LINHAS_POR_ESCRITA);
    aba.getRange(i + 1, 1, parte.length, colunas).setValues(parte);
  }
  // Tira as linhas e colunas que sobraram de uma importação maior
  if (aba.getMaxRows() > linhas.length + 1) aba.deleteRows(linhas.length + 2, aba.getMaxRows() - linhas.length - 1);
  if (aba.getMaxColumns() > colunas) aba.deleteColumns(colunas + 1, aba.getMaxColumns() - colunas);
  aba.setFrozenRows(1);
}

/**
 * Importa a exportação mais recente. Sem mudança desde a última importação, não faz nada
 * (passe true para forçar). O acionador diário chama sem parâmetro.
 */
function importarCsat(forcar) {
  forcar = forcar === true;
  var trava = LockService.getScriptLock();
  trava.waitLock(30000);
  try {
    var pasta = pastaCsat_();
    var resumo = JSON.parse(arquivo_(pasta, '_ultima_exportacao.json').getBlob().getDataAsString('UTF-8'));
    var props = PropertiesService.getScriptProperties();
    if (!forcar && props.getProperty('ULTIMA_EXPORTACAO') === resumo.exportado_em) {
      console.log('Nada novo: a exportação de ' + resumo.exportado_em + ' já foi importada.');
      return;
    }
    var ss = planilha_();
    var linhasPorAba = [];
    Object.keys(PAGINAS).forEach(function (chave) {
      var csv = Utilities.parseCsv(arquivo_(pasta, 'csat_' + chave + '.csv').getBlob().getDataAsString('UTF-8'));
      gravarAba_(ss, 'dados_' + chave, csv);
      linhasPorAba.push(['dados_' + chave, csv.length - 1]);
      gravarPacotes_(ss, chave, csv);
    });
    var mensal = Utilities.parseCsv(arquivo_(pasta, 'csat_mensal.csv').getBlob().getDataAsString('UTF-8'));
    gravarAba_(ss, 'mensal', mensal);
    linhasPorAba.push(['mensal', mensal.length - 1]);

    var agora = Utilities.formatDate(new Date(), 'America/Sao_Paulo', "yyyy-MM-dd'T'HH:mm:ssXXX");
    gravarAba_(ss, '_atualizacao', [['item', 'valor'], ['exportado_em', resumo.exportado_em], ['importado_em', agora]]
      .concat(linhasPorAba.map(function (l) { return ['linhas ' + l[0], String(l[1])]; })));
    props.setProperty('ULTIMA_EXPORTACAO', resumo.exportado_em);
    console.log('Importado: ' + JSON.stringify(linhasPorAba));
  } finally {
    trava.releaseLock();
  }
}

/** Importa de novo mesmo sem exportação nova (por exemplo, depois de atualizar este código). Rode pelo editor. */
function forcarImportacao() {
  importarCsat(true);
}

/** Cria (uma vez) o acionador diário da importação. A exportação local roda antes, na rotina da manhã. */
function criarAcionador() {
  ScriptApp.getProjectTriggers().forEach(function (t) {
    if (t.getHandlerFunction() === 'importarCsat') ScriptApp.deleteTrigger(t);
  });
  ScriptApp.newTrigger('importarCsat').timeBased().everyDays(1).atHour(10).nearMinute(0).create();
  console.log('Acionador diário criado: importarCsat por volta das 10h (America/Sao_Paulo).');
}

// ---------------------------------------------------------------- Páginas

function doGet(e) {
  var chave = e && e.parameter && e.parameter.pagina;
  var url = ScriptApp.getService().getUrl();
  var modelo;
  if (chave && PAGINAS[chave]) {
    modelo = HtmlService.createTemplateFromFile('Pagina');
    var cfg = JSON.parse(JSON.stringify(PAGINAS[chave]));
    cfg.chave = chave;
    cfg.meta = META_CSAT;
    cfg.paginas = Object.keys(PAGINAS).map(function (c) { return { chave: c, titulo: PAGINAS[c].titulo, url: url + '?pagina=' + c }; });
    modelo.configJson = JSON.stringify(cfg).replace(/</g, '\\u003c');
    modelo.titulo = PAGINAS[chave].titulo;
  } else {
    modelo = HtmlService.createTemplateFromFile('Indice');
    modelo.paginas = Object.keys(PAGINAS).map(function (c) { return { titulo: PAGINAS[c].titulo, url: url + '?pagina=' + c }; });
    modelo.titulo = 'Painel C-SAT';
  }
  return modelo.evaluate()
    .setTitle(modelo.titulo)
    .addMetaTag('viewport', 'width=device-width, initial-scale=1');
}

function incluir(nome) {
  return HtmlService.createHtmlOutputFromFile(nome).getContent();
}

function subtrairMeses_(mes, n) {
  var a = Number(mes.slice(0, 4)), m = Number(mes.slice(5, 7)) - n;
  while (m < 1) { m += 12; a -= 1; }
  return a + '-' + (m < 10 ? '0' : '') + m;
}

/**
 * Dados de uma operação para a página, com as colunas repetitivas codificadas em dicionário
 * (cada valor vira o índice numa lista), para a resposta ficar pequena.
 * desde = 'AAAA-MM' para cortar o histórico; vazio = os últimos MESES_INICIAIS meses; 'tudo' = tudo.
 */
function dados(chave, desde) {
  if (!PAGINAS[chave]) throw new Error('Página desconhecida: ' + chave);
  var aba = planilha_().getSheetByName('dados_' + chave);
  if (!aba || aba.getLastRow() < 2) return { colunas: [], dicionarios: {}, linhas: [], atualizacao: atualizacao_() };
  var saida = montarDados_(aba.getRange(1, 1, aba.getLastRow(), aba.getLastColumn()).getDisplayValues(), desde);
  saida.atualizacao = atualizacao_();
  return saida;
}

/**
 * Monta a resposta de dados() a partir das linhas da aba (com o cabeçalho). Não altera `tabela`.
 */
function montarDados_(tabela, desde) {
  var colunas = tabela[0];
  var valores = tabela.slice(1);
  var iMes = colunas.indexOf('mes');
  var ultimo = valores.reduce(function (m, l) { return l[iMes] > m ? l[iMes] : m; }, '');
  var corte = desde === 'tudo' ? '' : (desde || subtrairMeses_(ultimo, MESES_INICIAIS - 1));
  valores = valores.filter(function (l) { return !corte || l[iMes] >= corte; })
    .map(function (l) { return l.slice(); });  // cópia: a codificação abaixo troca os valores pelos índices

  var dicionarios = {};
  colunas.forEach(function (c, i) {
    var vistos = {}, lista = [];
    for (var k = 0; k < valores.length && lista.length <= valores.length / 4; k++) {
      var v = valores[k][i];
      if (!(v in vistos)) { vistos[v] = lista.length; lista.push(v); }
    }
    if (lista.length > valores.length / 4) return; // coluna quase única (protocolo, nome, datas): vai como texto
    for (k = 0; k < valores.length; k++) valores[k][i] = vistos[valores[k][i]];
    dicionarios[c] = lista;
  });
  return { colunas: colunas, dicionarios: dicionarios, linhas: valores, corte: corte, ultimoMes: ultimo };
}

// ---------------------------------------------------------------- Pacotes prontos
//
// Ler a aba inteira a cada acesso deixava a página lenta (a Hispana tem ~52 mil linhas). Por isso, a importação já grava
// a resposta de dados() pronta: em JSON, compactada (gzip) e em base64, em pedaços de até 45 mil caracteres na aba
// oculta _pacote_<operação>. A coluna A tem os últimos MESES_INICIAIS meses e a coluna B, o histórico inteiro.
// A página descompacta no navegador. Sem pacote (ou num navegador sem DecompressionStream), ela usa dados().

var PEDACO_PACOTE = 45000;  // o limite de uma célula é 50 mil caracteres

function compactar_(objeto) {
  var blob = Utilities.newBlob(JSON.stringify(objeto), 'application/json');
  return Utilities.base64Encode(Utilities.gzip(blob).getBytes());
}

function gravarPacotes_(ss, chave, tabela) {
  var colunas = ['', 'tudo'].map(function (desde) {
    var texto = compactar_(montarDados_(tabela, desde)), pedacos = [];
    // o "p" na frente impede que a planilha leia um pedaço como número ou fórmula
    for (var i = 0; i < texto.length; i += PEDACO_PACOTE) pedacos.push('p' + texto.slice(i, i + PEDACO_PACOTE));
    return pedacos;
  });
  var linhas = Math.max(colunas[0].length, colunas[1].length);
  var valores = [];
  for (var i = 0; i < linhas; i++) valores.push([colunas[0][i] || '', colunas[1][i] || '']);
  var nome = '_pacote_' + chave;
  var aba = ss.getSheetByName(nome) || ss.insertSheet(nome);
  aba.clear();
  if (aba.getMaxRows() < linhas) aba.insertRowsAfter(aba.getMaxRows(), linhas - aba.getMaxRows());
  aba.getRange(1, 1, linhas, 2).setNumberFormat('@').setValues(valores);
  if (aba.getMaxRows() > linhas + 1) aba.deleteRows(linhas + 2, aba.getMaxRows() - linhas - 1);
  aba.hideSheet();
  return colunas[0].join('').length + colunas[1].join('').length;
}

/**
 * Resposta de dados() já pronta e compactada: { base64, atualizacao }. Devolve null quando não há pacote para o
 * corte pedido (só existem o padrão e 'tudo'); aí a página chama dados().
 */
function pacote(chave, desde) {
  if (!PAGINAS[chave]) throw new Error('Página desconhecida: ' + chave);
  if (desde && desde !== 'tudo') return null;
  var aba = planilha_().getSheetByName('_pacote_' + chave);
  if (!aba || aba.getLastRow() < 1) return null;
  var coluna = desde === 'tudo' ? 2 : 1;
  var pedacos = aba.getRange(1, coluna, aba.getLastRow(), 1).getValues()
    .map(function (l) { return String(l[0]).slice(1); })
    .filter(function (p) { return p; });
  if (!pedacos.length) return null;
  return { base64: pedacos.join(''), atualizacao: atualizacao_() };
}

function atualizacao_() {
  var aba = planilha_().getSheetByName('_atualizacao');
  if (!aba) return {};
  var saida = {};
  aba.getDataRange().getDisplayValues().slice(1).forEach(function (l) { saida[l[0]] = l[1]; });
  return saida;
}
