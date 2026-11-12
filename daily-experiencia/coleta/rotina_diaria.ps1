# Rotina diária do Daily Experiência BR no Databricks: envia os arquivos de entrada ao volume, dispara o job e, quando
# ele termina, exporta o CSAT para a pasta do Drive do painel em Apps Script (..\csat\coleta\exportar_sheets.py).
# Por fim, publica as fontes dexp - no Tableau Cloud (coleta\publicar_tableau.py).
# Grava o que aconteceu em coleta\.estado\logs\AAAA-MM-DD_HHmm.log (fora do Git).
# Rodar à mão:   powershell -ExecutionPolicy Bypass -File coleta\rotina_diaria.ps1
# O agendamento no Windows é feito por coleta\agendar_rotina.ps1.
$ErrorActionPreference = "Stop"
$pasta = Split-Path -Parent $PSScriptRoot
$logs = Join-Path $PSScriptRoot ".estado\logs"
New-Item -ItemType Directory -Force $logs | Out-Null
$log = Join-Path $logs ("{0:yyyy-MM-dd_HHmm}.log" -f (Get-Date))

# A CLI do Databricks (usada no login OAuth) fica fora do PATH quando a tarefa roda pelo Agendador
$cli = Get-ChildItem "$env:LOCALAPPDATA\Microsoft\WinGet\Packages" -Recurse -Filter databricks.exe -ErrorAction SilentlyContinue |
    Select-Object -First 1
if ($cli) { $env:PATH = "$($cli.DirectoryName);$env:PATH" }
$env:PYTHONIOENCODING = "utf-8"

Set-Location $pasta
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
"Rotina iniciada em $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')" | Out-File -Encoding utf8 $log
# linha a linha em UTF-8 (o Tee-Object do PowerShell 5.1 grava em UTF-16)
& "$pasta\.venv\Scripts\python.exe" -I coleta\enviar_arquivos.py @args 2>&1 | ForEach-Object {
    $linha = "$_"
    $linha
    $linha | Out-File -Encoding utf8 -Append $log
}
$codigo = $LASTEXITCODE

# CSAT: depois do job, exporta a gold para a pasta do Drive de onde o Apps Script do painel importa (logic-local\csat)
$csat = Join-Path (Split-Path -Parent $pasta) "csat\coleta\exportar_sheets.py"
if ($codigo -eq 0 -and ($args -notcontains "--simular") -and (Test-Path $csat)) {
    "--- Exportação do CSAT ($(Get-Date -Format 'HH:mm:ss'))" | Out-File -Encoding utf8 -Append $log
    & "$pasta\.venv\Scripts\python.exe" -I $csat --aguardar-job 2>&1 | ForEach-Object {
        $linha = "$_"
        $linha
        $linha | Out-File -Encoding utf8 -Append $log
    }
    if ($LASTEXITCODE -ne 0) { $codigo = $LASTEXITCODE }
}

# Tableau Cloud: publica as fontes dexp - (elas não têm atualização agendada no site). Roda depois da exportação do
# CSAT, que espera o job terminar.
if ($codigo -eq 0 -and ($args -notcontains "--simular") -and (Test-Path $csat)) {
    "--- Publicação no Tableau Cloud ($(Get-Date -Format 'HH:mm:ss'))" | Out-File -Encoding utf8 -Append $log
    # sem -I: o script importa enviar_arquivos da própria pasta coleta
    & "$pasta\.venv\Scripts\python.exe" coleta\publicar_tableau.py 2>&1 | ForEach-Object {
        $linha = "$_"
        $linha
        $linha | Out-File -Encoding utf8 -Append $log
    }
    if ($LASTEXITCODE -ne 0) { $codigo = $LASTEXITCODE }
}
"Rotina terminada em $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') com codigo de saida $codigo" | Out-File -Encoding utf8 -Append $log
exit $codigo
