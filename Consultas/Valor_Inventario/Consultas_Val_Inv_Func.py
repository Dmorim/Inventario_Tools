from fdb import DatabaseError

from Thread_Manager.Query_Operations import query_selector, query_executor
from Consultas.Generics_Functions.Gen_Funcs_Consulta import banco_codigo_valueform
from Queries.Consulta_Queries import QUERY_INVENTARIO


def inv_get():
    # Função que executa a query de valor de inventário e retorna o valor obtido
    try:
        query = QUERY_INVENTARIO
        val = query_executor(query_selector, query)[0][0] if query_executor(
            query_selector, query) else None
    except DatabaseError as e:
        raise DatabaseError(
            f"Erro ao executar a query de valor de inventário: {e}")

    if val is not None:
        val = banco_codigo_valueform(val)  # Formata o valor obtido
    else:
        # Se o valor for None, retorna uma string informando que não foi registrado valor de inventário
        val = 'Não foi registrado valor de inventário'
    return val  # Retorna o valor formatado
