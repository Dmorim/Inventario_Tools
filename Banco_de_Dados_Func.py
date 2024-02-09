def Set_Dados_Padrao(entrys_list):
    entrys_list[0].insert(0, 'localhost')
    entrys_list[1].insert(0, '3050')
    entrys_list[3].insert(0, 'C:/Program Files/Firebird/Firebird_3_0/fbclient.dll')
    
def Caminho_Banco_Dir(Banco_Screen, entrys_list):
    from tkinter import filedialog
    caminho = filedialog.askopenfilename(title= 'Caminho para o banco de dados',parent= Banco_Screen, filetypes= [('Firebird Database', '*.fdb')], initialdir= 'C:\\Sistech\\Dados')
    if caminho:
        entrys_list[2].delete(0, 'end')
        entrys_list[2].insert(0, caminho)
        
def Caminho_Fb_Dir(Banco_Screen, entrys_list):
    from tkinter import filedialog
    caminho = filedialog.askopenfilename(title= 'Caminho para o fbclient',parent= Banco_Screen, filetypes= [('Firebird Dll', '*.dll')], initialdir= 'C:\\Program Files\\Firebird\\Firebird_3_0')
    if caminho:
        entrys_list[3].delete(0, 'end')
        entrys_list[3].insert(0, caminho)
        
def on_click_confirm(self, entrys_list, Banco_Screen, entry_alter_list):
    from Inventario_Conn import Dados, Connect
    from fdb import DatabaseError
    for entry in entrys_list:
        if entry.get() == '':
            from tkinter import messagebox
            messagebox.showerror('Erro', 'Preencha todos os campos', parent= Banco_Screen)
            return
        
    for name, var in zip(['host', 'port', 'database', 'fbclient'], entrys_list):
        Dados.banco_dados[name] = var.get()
        
    try:
        Connect.fdb_conn()
    except DatabaseError as e:
        from tkinter import messagebox
        messagebox.showerror('Erro', f'Não foi possível conectar ao banco de dados\n {e}', parent= Banco_Screen)
        return
    
    Banco_Screen.destroy()
    
    try:
        Connect.cursor.execute('SELECT NOME, RSOCIAL, CNPJ, CGF, CODCRT, FONE FROM PROPRI')
        val_brut = Connect.cursor.fetchone()
    except DatabaseError as e:
        from tkinter import messagebox
        messagebox.showerror('Erro', f'Não foi possível buscar os dados\n {e}', parent= Banco_Screen)
        return
    
    nome, rsocial, cnpj, cgf, codcrt, fone = val_brut
    if codcrt == '0':
        codcrt = 'Simples Nacional'
    elif codcrt == '1':
        codcrt = 'Simples Nacional - Excesso de Sublimite de Receita Bruta'
    elif codcrt == '2':
        codcrt = 'Regime Normal'
    val_list = [nome, rsocial, cnpj, cgf, codcrt, fone]
    
    for label, val in zip(entry_alter_list, val_list):
        label.configure(text= val)
    
    
    