"""
Criação das views auxiliares no banco de dados Firebird.

Executa as DDLs (CREATE OR REPLACE VIEW) logo após a conexão bem-sucedida.
As views devem ser criadas em ordem de dependência:
V_FAT_VALOR_SAIDA e V_LAN_COM antes de V_DIFF_ENTRADA_SAIDA_MES.
"""

from Thread_Manager.Query_Operations import query_executor, query_updater
from Queries.View_Queries import (
    VIEW_V_FAT_VALOR_SAIDA,
    VIEW_V_LAN_COM,
    VIEW_V_DIFF_ENTRADA_SAIDA_MES,
)
from Outros.Logger.Get_Logger import get_logger

logger = get_logger(__name__)

VIEW_DDL_ORDER = [
    ('V_FAT_VALOR_SAIDA', VIEW_V_FAT_VALOR_SAIDA),
    ('V_LAN_COM', VIEW_V_LAN_COM),
    ('V_DIFF_ENTRADA_SAIDA_MES', VIEW_V_DIFF_ENTRADA_SAIDA_MES),
]


def criar_views():
    """Cria ou atualiza as views auxiliares no banco, na ordem de dependência."""
    for nome, ddl in VIEW_DDL_ORDER:
        try:
            query_executor(query_updater, ddl)
            logger.info('View %s criada/atualizada com sucesso.', nome)
        except Exception:
            logger.exception('Erro ao criar a view %s.', nome)


def deletar_views():
    """Deleta as views auxiliares no banco, na ordem inversa de dependência."""
    for nome, _ in reversed(VIEW_DDL_ORDER):
        try:
            query_executor(query_updater, f"DROP VIEW {nome}")
        except Exception:
            logger.exception('Erro ao deletar a view %s.', nome)
