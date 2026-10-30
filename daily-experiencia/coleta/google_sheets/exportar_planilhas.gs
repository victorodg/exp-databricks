/**
 * Exporta as Google Sheets usadas pelo Daily Experiência BR como .xlsx na pasta "Fontes de Dados\auto\google_sheets"
 * do Drive compartilhado. O Google Drive para desktop sincroniza essa pasta no G:\ e a rotina local envia os
 * arquivos ao Databricks.
 *
 * Instalação (uma vez), com a conta da Natura, no editor do Apps Script (na planilha: Extensões > Apps Script):
 *   1. Cole este arquivo, salve e, em Configurações do projeto, use o fuso horário "America/Sao_Paulo".
 *   2. Execute exportarPlanilhas() uma vez e autorize o acesso pedido. A pasta é criada se ainda não existir.
 *   3. Execute criarGatilhoDiario() para agendar a exportação todo dia.
 * Se alguma planilha falhar, a execução termina com erro e o Google envia um e-mail de aviso ao dono do script.
 * Ao final de cada execução grava _ultima_exportacao.json na mesma pasta (horário e o que deu certo ou errado);
 * é esse arquivo que a rotina local consulta para saber se a exportação do dia já terminou.
 * Ao mudar o horário abaixo, execute criarGatilhoDiario() de novo para recriar o gatilho.
 */
// A pasta "Fontes de Dados" é encontrada a partir do MKT_Reativos.xlsx oficial (Fontes de Dados\EXP BR\MKT),
// e dentro dela o caminho abaixo; assim não é preciso copiar o ID de nenhuma pasta.
const ARQUIVO_REFERENCIA = '1n3X3Njk37qoH0Mprf8SH2fr2AVIBVJYE';
const CAMINHO_DESTINO = ['auto', 'google_sheets'];
const ARQUIVO_STATUS = '_ultima_exportacao.json';
// Horário do gatilho diário. O Google roda gatilhos de horário com até ~15 min de folga em torno do minuto pedido.
const HORA_EXECUCAO = 9;
const MINUTO_EXECUCAO = 0;

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
  // Daily Hispana
  auxiliar_hispana: '1zjTNpqmyoAWu-WLqV2nLzYNJp0Las6u_mMQf3zgLf3c',
  registro_de_grupos_hispana: '1LVISJ8GsoVgBizLomMHWkKmFIur8MfFmoFZFuY3YX7U',
  resenhas_ois: '1FEqQXMCU10tqtJyAd5gULEQD24ZZV1BKOwZyJID7SAE',
  ticket_medio_hispana: '1l9B0QkiZiOXAn545u1Js3gligsA8iOW2HbfSwUpwZZE',
  ticket_medio_por_pais: '1CGjLnV4zgf3toikmBZwt6iXxND9HzQUVy6PxJpHJpAU',
  base_exento: '1XjUlJog7movWv6pm3YKhkkI_zcqVeY8bTex9xbFCwpA',
};

function exportarPlanilhas() {
  const pasta = pastaDestino();
  const token = ScriptApp.getOAuthToken();
  const exportadas = [];
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
      exportadas.push(nome);
      console.log(`ok: ${nome}`);
    } catch (e) {
      falhas.push(`${nome}: ${e.message}`);
    }
  }

  const status = {
    exportado_em: Utilities.formatDate(new Date(), 'America/Sao_Paulo', "yyyy-MM-dd'T'HH:mm:ss"),
    exportadas: exportadas,
    falhas: falhas,
  };
  substituirArquivo(pasta, Utilities.newBlob(JSON.stringify(status, null, 2), 'application/json', ARQUIVO_STATUS));

  if (falhas.length) {
    throw new Error(`Falhas na exportação:\n${falhas.join('\n')}`);
  }
}

function pastaDestino() {
  // MKT_Reativos.xlsx -> MKT -> EXP BR -> Fontes de Dados
  let pasta = DriveApp.getFileById(ARQUIVO_REFERENCIA).getParents().next();
  pasta = pasta.getParents().next().getParents().next();
  for (const nome of CAMINHO_DESTINO) {
    const existentes = pasta.getFoldersByName(nome);
    pasta = existentes.hasNext() ? existentes.next() : pasta.createFolder(nome);
  }
  return pasta;
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
