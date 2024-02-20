def Set_Dados_Padrao(entrys_list):
    entrys_list[0].insert(0, 'localhost')
    entrys_list[1].insert(0, carregar_diretorio('Porta', entrys_list[1].get()) if carregar_diretorio('Porta', entrys_list[1].get()) is not None else '3050')
    entrys_list[3].insert(0, 'C:/Program Files (x86)/Firebird/Firebird_3_0/fbclient.dll')
    salvar_diretorio('Porta', entrys_list[1].get())  # Add this line to save the port in config.ini

def salvar_diretorio(diretorio, last_dir):
    import configparser
    config = configparser.ConfigParser()
    config.read('config.ini')
    config[diretorio] = {'last_dir': last_dir}
    with open('config.ini', 'w') as configfile:
        config.write(configfile)

def carregar_diretorio(diretorio, dir_busca):
    import configparser
    config = configparser.ConfigParser()
    config.read('config.ini')
    return config[diretorio][dir_busca] if config.has_option(diretorio, dir_busca) else None
    
def Caminho_Banco_Dir(self, Banco_Screen, entrys_list):
    from tkinter import filedialog
    
    dir = carregar_diretorio('Banco', 'last_dir')
    caminho = filedialog.askopenfilename(title= 'Caminho para o banco de dados',parent= Banco_Screen, filetypes= [('Firebird Database', '*.fdb')], initialdir= dir)
    if caminho:
        entrys_list[2].delete(0, 'end')
        entrys_list[2].insert(0, caminho)
        salvar_diretorio('Banco', caminho[:caminho.rfind('/')])
        
def Caminho_Fb_Dir(self, Banco_Screen, entrys_list):
    from tkinter import filedialog
    
    dir = carregar_diretorio('FBClient', 'last_dir')
    caminho = filedialog.askopenfilename(title= 'Caminho para o fbclient',parent= Banco_Screen, filetypes= [('Firebird Dll', '*.dll')], initialdir= dir)
    if caminho:
        entrys_list[3].delete(0, 'end')
        entrys_list[3].insert(0, caminho)
        salvar_diretorio('FBClient', caminho[:caminho.rfind('/')])
        
def on_click_confirm(self, entrys_list, Banco_Screen, entry_alter_list, button_list):
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
    
    try:
        Connect.cursor.execute("SELECT FIRST 1 DTEMI FROM IN01FAT WHERE VENDA = 'V' and EMITE = 'S' ORDER BY DTEMI DESC")
        result = Connect.cursor.fetchone()
        datas = [result[0]] if result is not None else []

        Connect.cursor.execute("SELECT FIRST 1 DTEMI FROM IN01FAT WHERE VENDA = 'A' and EMITE = 'S' ORDER BY DTEMI DESC")
        result = Connect.cursor.fetchone()
        if result is not None:
            datas.append(result[0])

        Connect.cursor.execute("SELECT FIRST 1 DTEMI FROM IN01FAT WHERE VENDA = 'S' and EMITE = 'W' ORDER BY DTEMI DESC")
        result = Connect.cursor.fetchone()
        if result is not None:
            datas.append(result[0])
            
    except DatabaseError as e:
        from tkinter import messagebox
        messagebox.showerror('Erro', f'Não foi possível buscar as datas\n {e}', parent= Banco_Screen)
        return
    
    nome, rsocial, cnpj, cgf, codcrt, fone = val_brut
    if codcrt == '0':
        codcrt = 'Simples Nacional'
    elif codcrt == '1':
        codcrt = 'Simples Nacional - Excesso de Sublimite de Receita Bruta'
    elif codcrt == '2':
        codcrt = 'Regime Normal'
    
    max_data = max(datas) if datas else 'Sem emissões'
    if max_data != 'Sem emissões':
        max_data = max_data.strftime('%d/%m/%Y')
    
    val_list = [nome, rsocial, cnpj, cgf, codcrt, fone, max_data]
    
    for label, val in zip(entry_alter_list, val_list):
        label.configure(text= val)
    
    for button in button_list:
        if button.cget('state') == 'disabled':
            button.configure(state = 'normal')
    