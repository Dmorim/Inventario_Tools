from fdb import DatabaseError

from Thread_Manager.Query_Operations import query_selector, query_executor
from Consultas.Generics_Functions.Gen_Funcs_Consulta import banco_codigo_valueform
from Queries.Consulta_Queries import QUERY_VENDAS


def ven_get(self) -> str:
    query = QUERY_VENDAS
    # Define os parâmetros da query
    params = (self.data_banco_inicial, self.data_banco_final)

    # Tenta executar a query no banco de dados
    try:
        rows = query_executor(query_selector, query, params)
        valrec = rows[0][0] if rows else None
    except (DatabaseError, TypeError) as e:
        raise DatabaseError(f"Erro ao acessar o banco de dados\n {e}") from e

    # Se o valor obtido for diferente de None, formata o valor e retorna ele, caso contrário retorna uma string informando que não foi registrado vendas
    if valrec is not None:
        valrec = banco_codigo_valueform(valrec)
    else:
        valrec = 'Não foi registrado vendas'
    return valrec
