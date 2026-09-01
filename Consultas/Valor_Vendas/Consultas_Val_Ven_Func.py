from fdb import DatabaseError

from Outros.Logger.Get_Logger import get_logger
from Thread_Manager.Query_Operations import query_selector, query_executor, _nome_query
from Consultas.Generics_Functions.Gen_Funcs_Consulta import banco_codigo_valueform
from Queries.Consulta_Queries import QUERY_VENDAS

logger = get_logger(__name__)


def ven_get(self) -> str:
    query = QUERY_VENDAS
    nome_query = _nome_query(query)
    # Define os parâmetros da query
    params = (self.data_banco_inicial, self.data_banco_final)
    logger.info('Consultando valor de vendas no período: %s até %s. query=%s',
                self.data_banco_inicial, self.data_banco_final, nome_query)

    # Tenta executar a query no banco de dados
    try:
        rows = query_executor(query_selector, query, params)
        valrec = rows[0][0] if rows else None
    except (DatabaseError, TypeError) as e:
        logger.exception(
            'Erro ao consultar valor de vendas. query=%s | params=%s', nome_query, params)
        raise DatabaseError(f"Erro ao acessar o banco de dados\n {e}") from e

    # Se o valor obtido for diferente de None, formata o valor e retorna ele, caso contrário retorna uma string informando que não foi registrado vendas
    if valrec is not None:
        valrec = banco_codigo_valueform(valrec)
        logger.info(
            'Valor de vendas obtido e formatado. query=%s | valor=%s', nome_query, valrec)
    else:
        valrec = 'Não foi registrado vendas'
        logger.warning(
            'Nenhum valor de vendas encontrado. query=%s | params=%s', nome_query, params)
    return valrec
