"""Renova o token do Databricks que as fontes 'dexp - ' do Tableau Cloud usam, antes que ele vença.

O workspace limita todo token a 14 dias (maxTokenLifetimeDays). O token das fontes leva o comentário
"tableau-cloud". Quando faltam DIAS_ANTES dias ou menos para o mais novo deles vencer (ou se não há nenhum):
  1. cria um token novo de 14 dias;
  2. guarda no cofre do Windows (o anterior fica em token-databricks-anterior);
  3. troca a credencial embutida em todas as fontes 'dexp - ' do Tableau Cloud.
O token antigo não é revogado: vence sozinho e serve de reserva se algo der errado no meio.

A rotina diária (enviar_arquivos.py e rotina_manual.ipynb) chama verificar_e_renovar(). Pela linha de comando,
a partir da pasta daily-experiencia:
  .venv\\Scripts\\python.exe coleta\\token_tableau.py             # renova só se estiver perto de vencer
  .venv\\Scripts\\python.exe coleta\\token_tableau.py --simular   # só mostra quantos dias faltam
  .venv\\Scripts\\python.exe coleta\\token_tableau.py --forcar    # renova agora

Solução definitiva (pendente): service principal com OAuth M2M, cujo segredo não tem o limite de 14 dias.
"""
import argparse
import sys
from datetime import datetime
from pathlib import Path

COMENTARIO = "tableau-cloud"
VALIDADE_DIAS = 14
DIAS_ANTES = 4  # folga para fim de semana e feriado, já que a rotina só roda em dia útil


def vencimento_atual(w):
    """Data de vencimento do token 'tableau-cloud' mais novo, ou None se não houver nenhum válido."""
    venc = [t.expiry_time for t in w.tokens.list() if t.comment == COMENTARIO and t.expiry_time and t.expiry_time > 0]
    return datetime.fromtimestamp(max(venc) / 1000).astimezone() if venc else None


def renovar(cfg, w):
    """Cria o token novo, guarda no cofre e troca a credencial nas fontes. Devolve (atualizadas, fontes com erro)."""
    import keyring
    import tableauserverclient as TSC

    from publicar_tableau import COFRE_DATABRICKS, SERVICO_COFRE, conectar_tableau

    novo = w.tokens.create(comment=COMENTARIO, lifetime_seconds=VALIDADE_DIAS * 24 * 3600)
    anterior = keyring.get_password(SERVICO_COFRE, COFRE_DATABRICKS)
    if anterior:
        keyring.set_password(SERVICO_COFRE, COFRE_DATABRICKS + "-anterior", anterior)
    keyring.set_password(SERVICO_COFRE, COFRE_DATABRICKS, novo.token_value)

    prefixo, host = cfg["tableau"]["prefixo"], cfg["tableau"]["databricks"]["servidor"]
    srv = conectar_tableau(cfg)
    ok, erros = 0, []
    for ds in TSC.Pager(srv.datasources):
        if not ds.name.startswith(prefixo):
            continue
        srv.datasources.populate_connections(ds)
        for c in ds.connections:
            if c.server_address != host or c.username != "token":
                continue
            try:
                c.password, c.embed_password = novo.token_value, True
                srv.datasources.update_connection(ds, c)
                ok += 1
            except Exception as e:  # noqa: BLE001 - uma fonte com erro não impede as outras
                erros.append(f"{ds.name}: {e}")
    return ok, erros


def verificar_e_renovar(cfg, w, simular=False, forcar=False):
    """Renova se faltar pouco para vencer. Devolve uma mensagem para a rotina mostrar."""
    venc = vencimento_atual(w)
    dias = (venc - datetime.now().astimezone()).total_seconds() / 86400 if venc else None
    situacao = f"vence em {venc:%d/%m às %H:%M} (faltam {dias:.1f} dias)" if venc else "nenhum token válido encontrado"
    if not forcar and dias is not None and dias > DIAS_ANTES:
        return f"🔑 Token do Tableau: {situacao}. Renova quando faltarem {DIAS_ANTES} dias."
    if simular:
        return f"🔑 Token do Tableau: {situacao}. Seria renovado agora (simulação)."
    ok, erros = renovar(cfg, w)
    novo = vencimento_atual(w)
    msg = f"🔑 Token do Tableau renovado: {ok} fontes atualizadas; o novo vence em {novo:%d/%m às %H:%M}."
    if erros:
        msg += f"\n⚠️ {len(erros)} fonte(s) com erro, troque a credencial à mão no Tableau Cloud:\n  " + "\n  ".join(erros)
    return msg


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    p = argparse.ArgumentParser(description="Renova o token do Databricks das fontes do Tableau Cloud.")
    p.add_argument("--simular", action="store_true", help="só mostra quantos dias faltam")
    p.add_argument("--forcar", action="store_true", help="renova mesmo que ainda falte tempo")
    a = p.parse_args()
    sys.path.insert(0, str(Path(__file__).resolve().parent))  # com python -I a pasta do script não entra no sys.path
    from enviar_arquivos import carregar_config, cliente
    cfg = carregar_config()
    print(verificar_e_renovar(cfg, cliente(cfg), simular=a.simular, forcar=a.forcar))


if __name__ == "__main__":
    main()
