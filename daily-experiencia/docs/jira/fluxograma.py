"""Desenha o fluxograma do Exp BR no Databricks (antes e agora) em PNG."""
import sys
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

TINTA, CINZA, LINHA = "#1f2933", "#52606d", "#9aa5b1"
FUNDOS = {"time": "#eef4fb", "dbx": "#fdf1e7", "tab": "#edf7f1", "antigo": "#f4f4f5"}
BORDAS = {"time": "#4c78a8", "dbx": "#e8743b", "tab": "#3a9a68", "antigo": "#8d939b"}

fig, ax = plt.subplots(figsize=(16, 9.6), dpi=150)
ax.set_xlim(0, 160); ax.set_ylim(0, 96); ax.axis("off")
fig.patch.set_facecolor("white")

def caixa(x, y, w, h, titulo, texto, tipo):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.4,rounding_size=1.2",
                                fc="white", ec=BORDAS[tipo], lw=1.6))
    ax.text(x + w / 2, y + h - 2.4, titulo, ha="center", va="top", fontsize=10.5, weight="bold", color=TINTA)
    ax.text(x + w / 2, y + h - 6.2, texto, ha="center", va="top", fontsize=8.6, color=CINZA, linespacing=1.35)

def seta(x1, y1, x2, y2, rot=None, cor=LINHA):
    ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle="-|>", mutation_scale=14, lw=1.6, color=cor,
                                 connectionstyle="arc3,rad=0"))
    if rot:
        ax.text((x1 + x2) / 2, (y1 + y2) / 2 + 1.4, rot, ha="center", va="bottom", fontsize=8, color=CINZA, style="italic")

def faixa(x, y, w, h, titulo, hora, tipo):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.3,rounding_size=1.5", fc=FUNDOS[tipo], ec="none"))
    ax.text(x + 1.5, y + h - 1.6, titulo, ha="left", va="top", fontsize=11.5, weight="bold", color=BORDAS[tipo])
    if hora:
        ax.text(x + w - 1.5, y + h - 1.6, hora, ha="right", va="top", fontsize=9, color=BORDAS[tipo])

ax.text(1, 94.5, "Daily Experiência BR: fluxo de dados no Databricks", fontsize=16, weight="bold", color=TINTA, va="top")

# ---- Agora
faixa(1, 31, 45, 56, "1. Coleta (time)", "~8h até 9h15", "time")
faixa(49, 31, 70, 56, "2. Databricks", "job de ~25 min", "dbx")
faixa(122, 31, 37, 56, "3. Tableau Cloud", "9h30", "tab")

caixa(7, 70, 36, 11, "MKTZap", "notebook de extração baixa os relatórios\ne grava os consolidados no Drive", "time")
caixa(7, 57.5, 36, 10, "Bases do time no Drive", "MKT Brasil Completo, Dynamics,\nSalesforce, ServiceNow, Resenhas", "time")
caixa(7, 45, 36, 10, "Google Sheets", "Apps Script exporta as planilhas\n(AppSheets, Dynatrace, Expurgo…)", "time")
caixa(7, 32.6, 36, 10.6, "rotina_manual.ipynb", "confere a exportação, envia o que\nmudou e dispara o job", "time")
ax.plot([4.5, 4.5], [75.5, 37.5], color=LINHA, lw=1.6)
for y in (75.5, 62.5, 50):
    ax.plot([4.5, 6.6], [y, y], color=LINHA, lw=1.6)
seta(4.5, 37.5, 6.6, 37.5)
ax.text(3.2, 56, "tudo fica no Drive", rotation=90, ha="center", va="center", fontsize=8, color=CINZA, style="italic")

caixa(52, 70, 30, 11, "Volume de entrada", "dexp_landing: uma pasta\npor arquivo e por dia", "dbx")
caixa(52, 56.5, 30, 11, "Bronze", "arquivos como chegaram,\ncom a versão de cada um", "dbx")
caixa(52, 43, 30, 11, "Silver", "colunas renomeadas e tipadas,\nsem linhas vazias", "dbx")
caixa(86, 63, 30, 18, "Gold", "regras de negócio dos\nfluxos do Prep\n\n24 tabelas, uma por saída\n(MKT, Dynamics, Resenhas…)", "dbx")
caixa(86, 43, 30, 14.5, "Views dexp_vw_*", "mesmos nomes de campo\nque o painel já usava\n\nconsultáveis por SQL", "dbx")
seta(43.4, 37.5, 51.6, 74, "envio")
seta(67, 70, 67, 67.9); seta(67, 56.5, 67, 54.4)
seta(82.4, 50, 85.6, 70)
seta(101, 63, 101, 57.9)

caixa(125, 59, 31, 22, "18 fontes publicadas", "\"dexp - …\" (extração)\natualização agendada\ntodo dia às 9h30\n\nquem consulta não precisa\nde acesso ao Databricks", "tab")
caixa(125, 38, 31, 15, "Painel", "Daily Experiência BR\n(versão Databricks)", "tab")
seta(116.4, 50, 124.6, 66)
seta(140.5, 59, 140.5, 53.4)

# ---- Antes
faixa(1, 2, 158, 25, "Antes: Tableau Prep", "", "antigo")
caixa(4, 5, 38, 15, "Coleta", "MKTZap baixado e consolidado\n(cópia manual para as pastas oficiais)\n+ bases do Drive e Google Sheets", "antigo")
caixa(50, 5, 52, 15, "2 fluxos do Tableau Prep (9h05)", "251 etapas e 755 ações, editáveis só pela tela,\nsem histórico de mudanças e sem testes;\nresultado intermediário não consultável", "antigo")
caixa(110, 5, 46, 15, "24 fontes em 4. DATASOURCES", "lidas pelo painel de produção\n(5 painéis de WhatsApp separados)", "antigo")
seta(42.4, 12.5, 49.6, 12.5); seta(102.4, 12.5, 109.6, 12.5)

fig.savefig(sys.argv[1], bbox_inches="tight", facecolor="white")
print("ok")
