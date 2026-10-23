/**
 * Exporta as Google Sheets usadas pelo Daily Experiência BR como .xlsx numa pasta do "Meu Drive".
 * O Google Drive para desktop sincroniza essa pasta no G:\ e o script local envia os arquivos ao Databricks.
 *
 * Instalação (uma vez), em https://script.google.com com a conta da Natura:
 *   1. Novo projeto -> cole este arquivo -> em Configurações do projeto, fuso horário "America/Sao_Paulo".
 *   2. Preencha PASTA_DESTINO_ID com o ID de uma pasta sua no Meu Drive (o trecho final da URL da pasta).
 *   3. Execute exportarPlanilhas() uma vez e autorize o acesso pedido.
 *   4. Execute criarGatilhoDiario() para agendar a exportação todo dia.
 * Se alguma planilha falhar, a execução termina com erro e o Google envia um e-mail de aviso ao dono do script.
 */
const PASTA_DESTINO_ID = 'COLE_AQUI_O_ID_DA_PASTA';
// Horário do gatilho diário. O Google roda gatilhos de horário com até ~15 min de folga em torno do minuto pedido.
const HORA_EXECUCAO = 9;
const MINUTO_EXECUCAO = 10;

// nome do arquivo exportado -> ID da Google Sheet (ver docs/inventario.md)
const PLANILHAS = {
  base_expurgo_mkt: '1Xxq8GLBU4qDf5yw1_w3F6LKDg-SPSBZUUa6Hgol0nA8',
  expurgo_dynamics: '15TkEO9bS5D6W1_DYJ2VeoDiYVVUQN729P6H5YgdlzJo',
  auxiliar_brasil: '1bboKHWs4Nni5XLxSKQXIt7dFhRPG9SQVVWzADq9NeYA',
  base_mkt: '1Huh-FLUWQ9yH21EhyvhX9GbT3F5D1N3jcHtGo2PKfe0',
  mapeamento_tribos: '1y4uGJ1ik89sDJ4qYKJgtgduGfHbn6jnbvukCzGYNjWE',
  monitoracao_dynatrace: '1TUhzUExoiv-3b835EJ3BehDPzBeNTrKER4vvMmnjdvA',
  registros_ate_julho_dynatrace: '1nECQI_RirnwWPaNOw1NMGBMLl-H9mFvBRkw8P1Yv6TA',
  appsheets_registros_experiencia_cb: '1KoUKxm5LF5x5pgUXouQFfftr4ftnQBA_PuB95N4LPJA',
  registros_de_acionamentos: '1QId6xiTda8zlnVdBwKsczLqowpxifk2jiAWfxJ9OeO0',
  ticket_medio: '1A_VHAujNp0oYAnAnNA_xuWBjT6GsWKJ-jhIC6d4a06s',
  healthcheck_2025: '1j_CTBASV-2p_WWwZTnMY_MlizYPanlu4mMBm20zhD7g',
  resenhas_appsheets: '1RAFYqizyyX6H7FCzWZdog2vTS3Hbh3TOfkwt2pdHTUA',
};

function exportarPlanilhas() {
  const pasta = DriveApp.getFolderById(PASTA_DESTINO_ID);
  const token = ScriptApp.getOAuthToken();
  const falhas = [];

  for (const [nome, id] of Object.entries(PLANILHAS)) {
    try {
      const resposta = UrlFetchApp.fetch(
        `https://docs.google.com/spreadsheets/d/${id}/export?format=xlsx`,
        { headers: { Authorization: `Bearer ${token}` }, muteHttpExceptions: true }
      );
      if (resposta.getResponseCode() !== 200) {
        throw new Error(`HTTP ${resposta.getResponseCode()}`);
      }
      substituirArquivo(pasta, resposta.getBlob().setName(`${nome}.xlsx`));
      console.log(`ok: ${nome}`);
    } catch (e) {
      falhas.push(`${nome}: ${e.message}`);
    }
  }

  if (falhas.length) {
    throw new Error(`Falhas na exportação:\n${falhas.join('\n')}`);
  }
}

// Troca a versão do dia anterior pela nova; a anterior vai para a lixeira (recuperável por 30 dias).
function substituirArquivo(pasta, blob) {
  const existentes = pasta.getFilesByName(blob.getName());
  while (existentes.hasNext()) {
    existentes.next().setTrashed(true);
  }
  pasta.createFile(blob);
}

function criarGatilhoDiario() {
  ScriptApp.getProjectTriggers()
    .filter(t => t.getHandlerFunction() === 'exportarPlanilhas')
    .forEach(t => ScriptApp.deleteTrigger(t));
  ScriptApp.newTrigger('exportarPlanilhas')
    .timeBased()
    .everyDays(1)
    .atHour(HORA_EXECUCAO)
    .nearMinute(MINUTO_EXECUCAO)
    .create();
}
