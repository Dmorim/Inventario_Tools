from fdb import DatabaseError

from Outros.Logger.Get_Logger import get_logger
from Thread_Manager.Query_Operations import query_selector, query_executor, _nome_query
from Consultas.Generics_Functions.Gen_Funcs_Consulta import banco_codigo_valueform
from Queries.Consulta_Queries import QUERY_ENTRADAS, CFOP_LIST

logger = get_logger(__name__)


def ent_get(periodo):
    cfop_list = CFOP_LIST

    # Criação da string com os cfops que serão excluidos da busca
    placeholders = ', '.join(['?'] * len(cfop_list))

    # Query que busca o valor de entradas, exclui os cfops da lista e busca somente as entradas entre as datas informadas
    query = QUERY_ENTRADAS.format(placeholders=placeholders)
    nome_query = _nome_query(query)

    params = (*cfop_list, periodo.inicio_formatado, periodo.fim_formatado)
    logger.info('Consultando valor de entradas. query=%s | params=%s',
                nome_query, params)
    # Tenta executar a query no banco de dados
    try:
        rows = query_executor(query_selector, query, params)
        valent = rows[0][0] if rows else None
    except DatabaseError as e:
        logger.exception(
            'Erro ao consultar valor de entradas. query=%s | params=%s', nome_query, params)
        raise DatabaseError(f"Erro ao acessar o banco de dados\n {e}") from e

    # Se o valor obtido for diferente de None, formata o valor e retorna ele, caso contrário retorna uma string informando que não foi registrado entradas
    if valent is not None:
        valent = banco_codigo_valueform(valent)
    else:
        valent = 'Não foi registrado entradas'
        logger.warning(
            'Nenhum valor de entradas encontrado. query=%s | params=%s', nome_query, params)
    return valent
