# Agenda a rotina diária (coleta\rotina_diaria.ps1) no Agendador de Tarefas do Windows, para o usuário atual.
# A tarefa só roda com o usuário logado (precisa do G:\ do Google Drive e do login OAuth do Databricks) e, se o
# computador estiver desligado no horário, roda assim que ele for ligado.
# Uso:      powershell -ExecutionPolicy Bypass -File coleta\agendar_rotina.ps1 -Horario 10:30
# Remover:  Unregister-ScheduledTask -TaskName "Daily Experiencia BR - envio Databricks" -Confirm:$false
param([string]$Horario = "10:30")
$ErrorActionPreference = "Stop"
$nome = "Daily Experiencia BR - envio Databricks"
$rotina = Join-Path $PSScriptRoot "rotina_diaria.ps1"

$acao = New-ScheduledTaskAction -Execute "powershell.exe" `
    -Argument "-NoProfile -ExecutionPolicy Bypass -WindowStyle Hidden -File `"$rotina`"" `
    -WorkingDirectory (Split-Path -Parent $PSScriptRoot)
$gatilho = New-ScheduledTaskTrigger -Daily -At $Horario
$config = New-ScheduledTaskSettingsSet -StartWhenAvailable -ExecutionTimeLimit (New-TimeSpan -Hours 1) `
    -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries
$principal = New-ScheduledTaskPrincipal -UserId "$env:USERDOMAIN\$env:USERNAME" -LogonType Interactive -RunLevel Limited

Register-ScheduledTask -TaskName $nome -Action $acao -Trigger $gatilho -Settings $config -Principal $principal `
    -Description "Envia os arquivos do Daily Experiência BR ao Databricks e dispara o job (logs em coleta\.estado\logs)." -Force | Out-Null
Get-ScheduledTask -TaskName $nome | Get-ScheduledTaskInfo | Select-Object TaskName, NextRunTime
