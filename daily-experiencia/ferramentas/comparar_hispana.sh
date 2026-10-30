#!/usr/bin/env sh
# Compara as 9 saídas do fluxo Hispana com os extracts baixados (rodar na pasta daily-experiencia, no Git Bash).
# Gera um relatório por saída em validacao/relatorios/ e imprime só as linhas com diferença.
set -u
PY=./.venv/Scripts/python.exe
while IFS='|' read -r extract gold; do
  [ -z "$extract" ] && continue
  saida="validacao/relatorios/$gold.md"
  "$PY" -I ferramentas/comparar_extract.py "validacao/extracts_hispana/$extract.tdsx" "$gold" > "$saida" 2>&1
  echo "=== $gold"
  grep -E "^Linhas|⚠️|^## |^- |^Só|Error|Traceback" "$saida" | head -60
done <<'EOF'
Ticket Medio Hispana|dexp_gold_hispana_ticket_medio
AppSheets Resenhas OIs|dexp_gold_hispana_appsheets_resenhas
Experiencia Hispana - Chamados Servicenow|dexp_gold_hispana_chamados_servicenow
Resenhas OIS|dexp_gold_hispana_resenhas
MKT Hispana Completo|dexp_gold_hispana_completo
Base MKT Lojas OIS|dexp_gold_hispana_base_mkt_lojas
Base MKT HC OIS|dexp_gold_hispana_base_mkt_hc
Base MKT OIS|dexp_gold_hispana_base_mkt
Experiencia Hispana Produtividade|dexp_gold_hispana_produtividade
EOF
