def banco_codigo_valueform(val):
    val = "{:,.2f}".format(val)
    prs = val.split('.')
    pri = prs[0]
    prd = prs[1]
    pri = pri.replace(",", ".")
    val = pri + ',' + prd
    return val

def ven_get():
    from Inventario_Conn import Connect
    from fdb import DatabaseError
    
    try:
        Connect.cursor.execute("select sum(cast(vlrec as numeric (15,2))) as valor from in01fat where dtemi between '01.01.2023' and '31.12.2023' and emite = 'S' and cance <> 'S'")
        valrec = Connect.cursor.fetchone()[0]
    except DatabaseError as e:
        from tkinter import messagebox
        messagebox.showerror('Erro', f'Erro ao acessar o banco de dados\n {e}')
        
    valrec = banco_codigo_valueform(valrec)
    return valrec
    
def copy_val(val_ven_text):
    import pyperclip
    copy_text = val_ven_text.cget('text')
    copy_text = 'R$ ' + copy_text
    pyperclip.copy(copy_text)