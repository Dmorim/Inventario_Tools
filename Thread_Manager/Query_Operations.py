from fdb import DatabaseError

from Banco_de_Dados.Conexao_Banco_Dados.Inventario_Conn import BancoDeDados
from Outros.Logger.Get_Logger import get_logger
from Queries.Comando_Queries import *  # noqa: F401,F403
from Queries.Consulta_Queries import *  # noqa: F401,F403

logger = get_logger(__name__)


def _nome_query(query):
    if not isinstance(query, str):
        return 'SQL_CUSTOMIZADO'

    query_normalizado = ' '.join(query.split())
    for nome, valor in globals().items():
        if nome.startswith('QUERY_') and isinstance(valor, str):
            valor_normalizado = ' '.join(valor.split())
            base_valor = valor_normalizado.split('{', 1)[0].strip()
            if query_normalizado == valor_normalizado:
                return nome
            if base_valor and query_normalizado.startswith(base_valor):
                return nome

    return 'SQL_CUSTOMIZADO'


def query_selector(conexao, query, params=None):
    nome_query = _nome_query(query)
    logger.debug('Executando SELECT: %s | params=%s', nome_query, params)
    try:
        cursor = conexao.cursor()
        cursor.execute(query, params)
        resultado = cursor.fetchall()
        return resultado
    except DatabaseError as e:
        logger.exception('Erro no SELECT: %s | params=%s', nome_query, params)
        raise DatabaseError(f"Erro ao gerar o select: {e}")
    finally:
        if 'cursor' in locals():
            cursor.close()
        conexao.rollback()


def query_updater(conexao, query, params=None):
    nome_query = _nome_query(query)
    logger.debug('Executando operação SQL: %s | params=%s', nome_query, params)
    try:
        cursor = conexao.cursor()
        cursor.execute(query, params)
        conexao.commit()
        return
    except DatabaseError as e:
        conexao.rollback()
        logger.exception(
            'Erro na operação SQL: %s | params=%s', nome_query, params)
        raise DatabaseError(f"Erro ao gerar a operação: {e}")
    finally:
        if 'cursor' in locals():
            cursor.close()


def query_executor(funcao, query, params=None):
    gerenciador = BancoDeDados.gerenciador()
    return gerenciador.executar(funcao, query, params)
