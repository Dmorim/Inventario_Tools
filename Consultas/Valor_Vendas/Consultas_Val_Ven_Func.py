from Thread_Manager.Query_Operations import query_selector, query_executor
from fdb import DatabaseError
from Consultas.Generics_Functions.Gen_Funcs_Consulta import banco_codigo_valueform


def ven_get(self):
    query = """
    select
    sum(CAST(iif(F.EMITE = 'S' AND VLNOT > 0, F.VLNOT, iif(coalesce(F.VLNOT, 0) = 0, (COALESCE(F.VALNO, 0) - COALESCE(F.VALDE, 0) + COALESCE(F.ICANT, 0) + coalesce(F.VALFR, 0) + coalesce(F.valsg, 0) + coalesce(F.valip, 0) + coalesce(F.valst, 0)), F.VLNOT)) AS NUMERIC(14,2))) as valor
    from in01fat f
    where F.FATUR <> '' AND (F.CANCE = 'N' OR F.CANCE IS NULL) AND F.VENDA <> 'R' and (F.VENDA <> 'X') and (F.DTEMI >= ?) and (F.DTEMI <= ?)
    """

    # Define os parâmetros da query
    params = (self.data_banco_inicial, self.data_banco_final)

    # Tenta executar a query no banco de dados
    try:
        rows = query_executor(query_selector, query, params)
        valrec = rows[0][0] if rows else None
    except (DatabaseError, TypeError) as e:
        from tkinter import messagebox
        messagebox.showerror('Erro', f'Erro ao acessar o banco de dados\n {e}')

    # Se o valor obtido for diferente de None, formata o valor e retorna ele, caso contrário retorna uma string informando que não foi registrado vendas
    if valrec is not None:
        valrec = banco_codigo_valueform(valrec)
    else:
        valrec = 'Não foi registrado vendas'
    return valrec
