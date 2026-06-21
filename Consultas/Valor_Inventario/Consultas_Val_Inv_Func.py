def banco_codigo_valueform(val):
    # Mesmo funcionamento explicado em Consultas/Consultas_Val_Ven_Func.py
    val = "{:,.2f}".format(val)
    prs = val.split('.')
    pri = prs[0]
    prd = prs[1]
    pri = pri.replace(",", ".")
    val = pri + ',' + prd
    return val


def inv_get():
    # Função que executa a query de valor de inventário e retorna o valor obtido
    from Thread_Manager.Query_Operations import query_selector, query_executor
    try:
        query = "select sum (cast(saldo * precu as numeric (15, 2))) as valor from in01pro where cast (saldo as numeric (15, 2)) > 0 and classificacao_produto in ('00','01','02','03','04','05','06')"
        val = query_executor(query_selector, query)[0][0]
    except:
        from tkinter import messagebox
        messagebox.showerror('Erro', 'Erro ao acessar o banco de dados')
        return

    if val is not None:
        val = banco_codigo_valueform(val)  # Formata o valor obtido
    else:
        # Se o valor for None, retorna uma string informando que não foi registrado valor de inventário
        val = 'Não foi registrado  valor de inventário'
    return val  # Retorna o valor formatado


def copy_val(val_inv_text):
    # Mesmo funcionamento explicado em Consultas/Consultas_Val_Ven_Func.py
    import pyperclip
    copy_text = val_inv_text.cget('text')
    copy_text = 'R$ ' + copy_text
    pyperclip.copy(copy_text)
