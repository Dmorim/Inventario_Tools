"""
Criação das views auxiliares no banco de dados Firebird.

Executa as DDLs (CREATE OR REPLACE VIEW) logo após a conexão bem-sucedida.
As views devem ser criadas em ordem de dependência:
V_FAT_VALOR_SAIDA e V_LAN_COM antes de V_DIFF_ENTRADA_SAIDA_MES.
"""

from Thread_Manager.Query_Operations import query_executor, query_updater
from Banco_de_Dados.Conexao_Banco_Dados.Inventario_Conn import BancoDeDados
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

# Ordem inversa para deletar as views
DROP_VIEW_DDL_ORDER = list(VIEW_DDL_ORDER[::-1])


def criar_views():
    """Cria ou atualiza as views auxiliares no banco, na ordem de dependência."""
    for nome, ddl in VIEW_DDL_ORDER:
        try:
            query_executor(query_updater, ddl)
            logger.info('View %s criada/atualizada com sucesso.', nome)
        except Exception:
            logger.exception('Erro ao criar a view %s.', nome)


def _deletar_views_na_conexao(conexao):
    """Remove todas as views usando a mesma conexão e transação controlada."""
    conexao.rollback()
    try:
        for nome, _ in DROP_VIEW_DDL_ORDER:
            cursor = conexao.cursor()
            try:
                cursor.execute(f"DROP VIEW {nome}")
            finally:
                cursor.close()
            conexao.commit()
            logger.info('View %s removida com sucesso.', nome)
    except Exception:
        conexao.rollback()
        raise


def deletar_views():
    """Deleta as views auxiliares na ordem inversa de dependência."""
    gerenciador = BancoDeDados.gerenciador()
    gerenciador.aguardar_operacoes()
    return gerenciador.executar(_deletar_views_na_conexao)
