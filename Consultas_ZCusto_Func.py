def prod_get():
    from Inventario_Conn import Connect
    from fdb import DatabaseError
    query = """
    select count (*) from in01pro where precu = 0 or (precu is null) or (precu < 0)
    """
    
    try:
        Connect.cursor.execute(query)
        val = Connect.cursor.fetchone()[0]
    except DatabaseError as e:
        from tkinter import messagebox
        messagebox.showerror('Erro', f'Erro ao acessar o banco de dados\n {e}')
        
    return val
    
def copy_val(val_ven_text):
    import pyperclip
    copy_text = val_ven_text.cget('text')
    copy_text = 'R$ ' + copy_text
    pyperclip.copy(copy_text)