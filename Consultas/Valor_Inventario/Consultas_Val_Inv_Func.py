from fdb import DatabaseError

from Outros.Logger.Get_Logger import get_logger
from Thread_Manager.Query_Operations import query_selector, query_executor, _nome_query
from Consultas.Generics_Functions.Gen_Funcs_Consulta import banco_codigo_valueform
from Queries.Consulta_Queries import QUERY_INVENTARIO

logger = get_logger(__name__)


def inv_get():
    # Função que executa a query de valor de inventário e retorna o valor obtido
    query = QUERY_INVENTARIO
    nome_query = _nome_query(query)
    logger.info('Consultando valor de inventário. query=%s', nome_query)
    try:
        rows = query_executor(query_selector, query)
        val = rows[0][0] if rows else None
    except DatabaseError as e:
        logger.exception(
            'Erro ao consultar valor de inventário. query=%s', nome_query)
        raise DatabaseError(
            f"Erro ao executar a query de valor de inventário: {e}")

    if val is not None:
        val = banco_codigo_valueform(val)  # Formata o valor obtido
        logger.info(
            'Valor de inventário obtido e formatado. query=%s | valor=%s', nome_query, val)
    else:
        # Se o valor for None, retorna uma string informando que não foi registrado valor de inventário
        val = 'Não foi registrado valor de inventário'
        logger.warning(
            'Nenhum valor de inventário encontrado. query=%s', nome_query)
    return val  # Retorna o valor formatado
