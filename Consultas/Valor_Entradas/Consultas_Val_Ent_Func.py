from fdb import DatabaseError

from Outros.Logger.Get_Logger import get_logger
from Thread_Manager.Query_Operations import query_selector, query_executor, _nome_query
from Consultas.Generics_Functions.Gen_Funcs_Consulta import banco_codigo_valueform
from Queries.Consulta_Queries import QUERY_ENTRADAS

logger = get_logger(__name__)


def ent_get(self):
    cfop_list = ['1.104', '1.105', '1.116', '1.117', '1.120', '1.126', '1.201', '1.203', '1.204', '1.207', '1.212', '1.304', '1.360', '1.406', '1.407', '1.411', '1.503', '1.504', '1.505', '1.540', '1.543', '1.551', '1.552', '1.555', '1.556', '1.565', '1.592', '1.594', '1.652', '1.653', '1.655', '1.656', '1.908', '1.910', '1.912', '1.920', '1.921', '1.922', '1.923', '1.949', '2.104', '2.105', '2.116', '2.117', '2.120', '2.126', '2.128',
                 '2.154', '2.201', '2.203', '2.204', '2.207', '2.212', '2.215', '2.252', '2.255', '2.304', '2.360', '2.406', '2.407', '2.410', '2.411', '2.503', '2.504', '2.505', '2.540', '2.543', '2.551', '2.552', '2.555', '2.556', '2.565', '2.592', '2.594', '2.640', '2.652', '2.653', '2.655', '2.656', '2.908', '2.909', '2.910', '2.911', '2.912', '2.915', '2.916', '2.919', '2.920', '2.921', '2.922', '2.923', '2.925', '2.932', '2.933', '2.949']

    logger.info('Consultando valor de entradas no período: %s até %s. query=%s',
                self.data_banco_inicial, self.data_banco_final, 'QUERY_ENTRADAS')

    # Criação da string com os cfops que serão excluidos da busca
    placeholders = ', '.join(['?'] * len(cfop_list))

    # Query que busca o valor de entradas, exclui os cfops da lista e busca somente as entradas entre as datas informadas
    query = QUERY_ENTRADAS.format(placeholders=placeholders)
    nome_query = _nome_query(query)

    params = (*cfop_list, self.data_banco_inicial, self.data_banco_final)
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
        logger.info('Valor de entradas obtido e formatado. query=%s | valor=%s', nome_query, valent)
    else:
        valent = 'Não foi registrado entradas'
        logger.warning(
            'Nenhum valor de entradas encontrado. query=%s | params=%s', nome_query, params)
    return valent
