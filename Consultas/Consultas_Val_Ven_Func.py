def banco_codigo_valueform(val):
    val = "{:,.2f}".format(val)
    prs = val.split('.')
    pri = prs[0]
    prd = prs[1]
    pri = pri.replace(",", ".")
    val = pri + ',' + prd
    return val

def ven_get(self):
    from Inventario_Conn import Connect
    from fdb import DatabaseError
    query = f"""
    select
    sum(CAST(iif(F.EMITE = 'S' AND VLNOT > 0, F.VLNOT, iif(coalesce(F.VLNOT, 0) = 0, (COALESCE(F.VALNO, 0) - COALESCE(F.VALDE, 0) + COALESCE(F.ICANT, 0) + coalesce(F.VALFR, 0) + coalesce(F.valsg, 0) + coalesce(F.valip, 0) + coalesce(F.valst, 0)), F.VLNOT)) AS NUMERIC(14,2))) as valor
    from in01fat f 
    where F.FATUR <> '' AND (F.CANCE = 'N' OR F.CANCE IS NULL) AND F.VENDA <> 'R' and (F.VENDA <> 'X') and (F.DTEMI >= '{self.data_banco_inicial}') and (F.DTEMI <= '{self.data_banco_final}')
    """
    
    try:
        Connect.cursor.execute(query)
        valrec = Connect.cursor.fetchone()[0]
    except (DatabaseError, TypeError) as e:
        from tkinter import messagebox
        messagebox.showerror('Erro', f'Erro ao acessar o banco de dados\n {e}')
        
    valrec = banco_codigo_valueform(valrec)
    return valrec
    
def copy_val(val_ven_text):
    import pyperclip
    copy_text = val_ven_text.cget('text')
    copy_text = 'R$ ' + copy_text
    pyperclip.copy(copy_text)