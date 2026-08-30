from Thread_Manager.Query_Operations import query_selector, query_executor
from Consultas.Generics_Functions.Gen_Funcs_Consulta import banco_codigo_valueform


def inv_get():
    # Função que executa a query de valor de inventário e retorna o valor obtido
    try:
        query = "select sum (cast(saldo * precu as numeric (15, 2))) as valor from in01pro where cast (saldo as numeric (15, 2)) > 0 and classificacao_produto in ('00','01','02','03','04','05','06')"
        val = query_executor(query_selector, query)[0][0] if query_executor(
            query_selector, query) else None
    except:
        from tkinter import messagebox
        messagebox.showerror('Erro', 'Erro ao acessar o banco de dados')
        return

    if val is not None:
        val = banco_codigo_valueform(val)  # Formata o valor obtido
    else:
        # Se o valor for None, retorna uma string informando que não foi registrado valor de inventário
        val = 'Não foi registrado valor de inventário'
    return val  # Retorna o valor formatado
