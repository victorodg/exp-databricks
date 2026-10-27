"""Definição das tabelas silver: cada uma é uma tabela bronze com colunas renomeadas e tipadas.

Cada coluna é (nome na silver, nome na bronze, tipo). Tipos: texto, data_hora, data, inteiro.
Colunas da bronze que não estão na lista (ex.: coluna_<n> sem cabeçalho) não passam para a silver.
"""
from pyspark.sql import functions as F

from dexp import tableau as tb

CONVERSORES = {
    # O Prep tira os espaços do fim dos textos ao ler as planilhas ('Pay ' vira 'Pay'); os do começo ficam.
    "texto": lambda nome: F.rtrim(F.col(f"`{nome}`")),
    "data_hora": lambda nome: tb.data_hora(F.col(f"`{nome}`")),
    "data": lambda nome: tb.data(F.col(f"`{nome}`")),
    "inteiro": tb.inteiro,
}


def tipar(df, colunas):
    """Seleciona e tipa as colunas; mantém `_versao` (versão do arquivo de origem na bronze)."""
    return df.select([CONVERSORES[tipo](bronze).alias(silver) for silver, bronze, tipo in colunas] + ["_versao"])


_SALESFORCE_COMUM = [
    ("numero_da_ocorrencia", "numero_do_caso", "texto"),
    ("primeira_categoria", "primeira_categoria", "texto"),
    ("segunda_categoria", "segunda_categoria", "texto"),
    ("motivo", "motivo", "texto"),
    ("etapa", "etapa", "texto"),
    ("experience", "classificacao_do_problema_sistemico", "texto"),
    ("aplicativo_com_problemas", "aplicativo_com_problemas", "texto"),
    ("data_de_criacao", "data_hora_de_abertura", "data_hora"),
    ("data_do_sla", "data_alvo_sla", "data_hora"),
    ("termino_real", "data_hora_de_fechamento", "data_hora"),
    ("solucao", "solucao", "texto"),
    ("proprietario", "proprietario", "texto"),
    ("etapa_1", "etapa_2", "texto"),
    ("status_da_atividade", "status", "texto"),
    ("chamado", "chamado", "texto"),
    ("caso_pai_chamado", "caso_pai_chamado", "texto"),
]

_SALESFORCE_HISTORICO = _SALESFORCE_COMUM + [
    ("usuario_que_realizou_alteracao", "usuario_que_realizou_alteracao_nome_completo", "texto"),
    ("nome_da_conta_cpf", "nome_da_conta_cpf", "texto"),
    ("id_caso_completo", "id_caso_completo", "texto"),
    ("modificado_pela_ultima_vez_por", "modificado_pela_ultima_vez_por_nome_completo", "texto"),
    ("data_inicio", "data_inicio", "data_hora"),
    ("data_fim", "data_fim", "data_hora"),
    ("tipo_de_registro_do_caso", "tipo_de_registro_do_caso", "texto"),
]

_DYNAMICS_COMUM = [
    ("tarefa_id", "nao_modificar_tarefa", "texto"),
    ("soma_de_verificacao", "nao_modificar_soma_de_verificacao_da_linha", "texto"),
    ("data_de_modificacao", "nao_modificar_data_de_modificacao", "data_hora"),
    ("data_de_criacao", "data_de_criacao", "data_hora"),
    ("data_do_sla", "data_do_sla", "data_hora"),
    ("termino_real", "termino_real", "data_hora"),
    ("modificado_por", "modificado_por", "texto"),
    ("proprietario", "proprietario", "texto"),
    ("status_da_atividade", "status_da_atividade", "texto"),
    ("solucao", "solucao", "texto"),
    ("referente", "referente", "texto"),
    ("etapa", "etapa", "texto"),
    ("numero_da_ocorrencia", "numero_da_ocorrencia_referente_ocorrencia", "texto"),
    ("assunto", "assunto", "texto"),
    ("primeira_categoria", "primeira_categoria_referente_ocorrencia", "texto"),
    ("segunda_categoria", "segunda_categoria_referente_ocorrencia", "texto"),
    ("motivo", "motivo_referente_ocorrencia", "texto"),
    ("central_de_atendimento", "central_de_atendimento_referente_ocorrencia", "texto"),
    ("codigo_natura", "codigo_natura_cliente_contato", "texto"),
    ("numero_do_documento", "numero_do_documento_cliente_contato", "texto"),
    ("experience", "experience", "texto"),
    ("ticket_externo", "ticket_externo", "texto"),
]

_REVIEWS_GOOGLE_PLAY = [
    ("package_name", "package_name", "texto"),
    ("app_version_code", "app_version_code", "inteiro"),
    ("app_version_name", "app_version_name", "texto"),
    ("reviewer_language", "reviewer_language", "texto"),
    ("device", "device", "texto"),
    ("review_submit_date_and_time", "review_submit_date_and_time", "texto"),
    ("review_submit_millis_since_epoch", "review_submit_millis_since_epoch", "inteiro"),
    ("review_last_update_date_and_time", "review_last_update_date_and_time", "texto"),
    ("review_last_update_millis_since_epoch", "review_last_update_millis_since_epoch", "inteiro"),
    ("star_rating", "star_rating", "inteiro"),
    ("review_title", "review_title", "texto"),
    ("review_text", "review_text", "texto"),
    ("developer_reply_date_and_time", "developer_reply_date_and_time", "texto"),
    ("developer_reply_millis_since_epoch", "developer_reply_millis_since_epoch", "inteiro"),
    ("developer_reply_text", "developer_reply_text", "texto"),
    ("review_link", "review_link", "texto"),
]

# tabela silver -> (tabelas bronze unidas, colunas)
TABELAS = {
    "salesforce_cf_legado": (["salesforce_cf"], _SALESFORCE_COMUM),
    "salesforce_cf_criados": (["salesforce_cf_criados"], _SALESFORCE_HISTORICO),
    "salesforce_cf_encerrados": (["salesforce_cf_encerrados"], _SALESFORCE_HISTORICO),
    "dynamics_criados_em": (["dynamics_criados_em"], _DYNAMICS_COMUM + [
        ("problema_de_sistema", "problema_de_sistema_referente_ocorrencia", "texto"),
        ("opcao_menu", "opcao_menu_referente_ocorrencia", "texto"),
        ("problema_de_sistema_fv", "problema_de_sistema_fv_referente_ocorrencia", "texto"),
        ("problema_site_natura", "problema_site_natura_referente_ocorrencia", "texto"),
    ]),
    "dynamics_termino_real": (["dynamics_termino_real"], _DYNAMICS_COMUM),
    "servicenow_incidentes": (["servicenow_incidentes"], [
        ("numero", "number", "texto"),
        ("aberto_por", "opened_by", "texto"),
        ("aberto_em", "opened_at", "data_hora"),
        ("descricao_resumida", "short_description", "texto"),
        ("solicitante", "caller_id", "texto"),
        ("prioridade", "priority", "texto"),
        ("status", "state", "texto"),
        ("categoria", "category", "texto"),
        ("grupo_de_atribuicao", "assignment_group", "texto"),
        ("atribuido_a", "assigned_to", "texto"),
        ("atualizado_em", "sys_updated_on", "data_hora"),
        ("atualizado_por", "sys_updated_by", "texto"),
        ("canal", "contact_type", "texto"),
        ("codigo_de_resolucao", "close_code", "texto"),
        ("descricao", "description", "texto"),
        ("subcategoria", "subcategory", "texto"),
        ("termino_real", "work_end", "texto"),
        ("inicio_real", "work_start", "texto"),
        ("ultima_reabertura_em", "reopened_time", "data_hora"),
        ("encerrado", "closed_at", "data_hora"),
        ("resolvido", "resolved_at", "data_hora"),
        ("resolvido_por", "resolved_by", "texto"),
        ("perc_tempo_de_negocio_decorrido", "u_sla_business_percentage", "texto"),
        ("motivo_para_estar_em_espera", "hold_reason", "texto"),
        ("servico", "business_service", "texto"),
        ("jira", "u_jira", "texto"),
        ("ticket_externo", "u_external_ticket", "texto"),
        ("problema", "problem_id", "texto"),
        ("prazo", "due_date", "data_hora"),
        ("anotacoes_de_resolucao", "close_notes", "texto"),
    ]),
    "tribos_dynamics": (["tribos_base_dynamics"], [
        ("experience", "experience", "texto"),
        ("plataforma", "plataforma", "texto"),
        ("tribo", "tribo", "texto"),
        ("macro", "macro", "texto"),
    ]),
    "tribos_grupos_servicenow": (["tribos_grupos_servicenow"], [
        ("grupo_de_atribuicao", "grupo_de_atribuicao_no_service_now", "texto"),
        ("nomenclatura_aba", "nomenclatura_para_criar_aba_no_service_now", "texto"),
        ("nomenclatura_aba_2", "nomenclatura_para_criar_aba_no_service_now_2", "texto"),
        ("tribo", "tribo", "texto"),
        ("responsavel", "responsavel", "texto"),
        ("gerente_responsavel", "gerente_responsavel", "texto"),
    ]),
    "expurgo_dynamics": (["expurgo_dynamics"], [
        ("numero_da_ocorrencia", "numero_da_ocorrencia_referente_ocorrencia", "texto"),
        ("nivel_de_atendimento", "nivel_de_atendimento", "texto"),
        ("data_expurgo", "data_expurgo", "data"),
        ("mes_de_expurgo", "mes_de_expurgo", "texto"),
        ("motivo", "motivo", "texto"),
    ]),
    "resenhas_appsheets": (["resenhas_appsheets"], [
        ("id", "coluna_1", "texto"),
        ("aplicativo", "aplicativo", "texto"),
        ("loja", "loja", "texto"),
        ("nome_do_respondente", "nome_do_respondente", "texto"),
        ("classificacao_de_estrelas", "classificacao_de_estrelas", "texto"),
        ("data_da_resposta", "data_da_resposta", "data"),
        ("categoria_da_resposta", "categoria_da_resposta", "texto"),
        ("categoria_da_resposta_2", "categoria_da_resposta_2", "texto"),
        ("classificacao_da_resposta", "classificacao_da_resposta", "texto"),
        ("comentario_postado", "comentario_postado", "texto"),
        ("resposta_fornecida", "resposta_fornecida", "texto"),
        ("classificacao_do_ofensor", "classificacao_do_ofensor", "texto"),
        ("idioma", "idioma", "texto"),
        ("resp_pela_resposta", "resp_pela_resposta", "texto"),
        ("data_da_resposta_exp", "data_da_resposta_exp", "data_hora"),
        ("observacao", "observacao", "texto"),
    ]),
    "resenhas_google_play": (["app_natura", "app_avon", "consultoria_natura", "forca_de_vendas"], _REVIEWS_GOOGLE_PLAY),
}
