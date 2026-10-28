# Rotina diária do Daily Experiência BR no Databricks: envia os arquivos de entrada ao volume e dispara o job.
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
"Rotina terminada em $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') com codigo de saida $codigo" | Out-File -Encoding utf8 -Append $log
exit $codigo
