def prod_get(query_input: str):
    from Banco_de_Dados.Inventario_Conn import Connect
    from fdb import DatabaseError
    
    try:
        Connect.cursor.execute(query_input)
        val = Connect.cursor.fetchone()[0]
    except DatabaseError as e:
        from tkinter import messagebox
        messagebox.showerror('Erro', f'Erro ao acessar o banco de dados\n {e}')
        
    return val

def copy_val(val_ven_text):
    import pyperclip
    copy_text = val_ven_text.cget('text')
    pyperclip.copy(copy_text)
    
def event_button_consulta(self, event):
    if self.consulta.cget('state') != 'disabled':
        self.consulta.invoke()
        
def event_button_comando(self, event):
    if self.comando.cget('state') != 'disabled':
        self.comando.invoke()