#!/usr/bin/env sh
# Compara as 18 saídas do fluxo MKT com os extracts baixados (rodar na pasta daily-experiencia, no Git Bash).
# Gera um relatório por saída em validacao/relatorios/ e imprime só as linhas com diferença.
set -u
PY=./.venv/Scripts/python.exe
while IFS='|' read -r extract gold; do
  [ -z "$extract" ] && continue
  saida="validacao/relatorios/$gold.md"
  "$PY" -I ferramentas/comparar_extract.py "validacao/extracts/$extract.tdsx" "$gold" > "$saida" 2>&1
  echo "=== $gold"
  grep -E "^Linhas|⚠️|^## |^- |^Só|Error|Traceback" "$saida" | head -60
done <<'EOF'
HC Exp Brasil|dexp_gold_mkt_hc_exp_brasil
Exp Brasil Dynatrace|dexp_gold_mkt_exp_brasil_dynatrace
Requisição Eventual EXP BR|dexp_gold_mkt_requisicao_eventual
Histórico Backlog Diário|dexp_gold_mkt_historico_backlog_diario
MKT Whats GN|dexp_gold_mkt_whats_gn
MKT Whats GV|dexp_gold_mkt_whats_gv
MKT Whats GV Antecipada(1)|dexp_gold_mkt_whats_gv_antecipada
MKT Whats Franquia|dexp_gold_mkt_whats_franquia
MKT Email Experiencia CB|dexp_gold_mkt_email_experiencia_cb
MKT Emails de Lojas|dexp_gold_mkt_emails_de_lojas
MKT - CBCOM|dexp_gold_mkt_cbcom
MKT BRASIL - Email|dexp_gold_mkt_brasil_email
MKT BRASIL - WhatsApp|dexp_gold_mkt_brasil_whatsapp
MKT Brasil Completo|dexp_gold_mkt_brasil_completo
MKT Brasil Completo Nivel|dexp_gold_mkt_brasil_completo_nivel
MKT Brasil Backlog|dexp_gold_mkt_brasil_backlog
Ticket Medio Exp Br|dexp_gold_mkt_ticket_medio
Experiencia Brasil Nivel|dexp_gold_mkt_experiencia_brasil_nivel
EOF
