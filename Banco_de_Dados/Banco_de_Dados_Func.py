def Set_Dados_Padrao(entrys_list):
    # Função para preencher os entrys com os dados padrão
    # Args:
        # entrys_list: list -> Lista de entrys que serão utilizadas para armazenar os dados informados pelo usuário para obtenção dos valores escolhidos
    
    porta = carregar_diretorio('Porta', 'last_dir') # Carrega a última porta utilizada do arquivo config.ini
    fbclient = carregar_diretorio('FBClient', 'dir_banco') # Carrega o último caminho da fbclient utilizado do arquivo config.ini
    entrys_list[0].insert(0, 'localhost') # Insere o host padrão
    entrys_list[1].insert(0, porta if porta else '3050') # Insere a porta padrão
    entrys_list[3].insert(0, fbclient if fbclient else 'C:/Program Files/Firebird/Firebird_3_0/bin/fbclient.dll')

def salvar_diretorio(diretorio, name: str, last_dir):
    # Função para salvar os dados no arquivo config.ini
    # Args:
        # diretorio: str -> Diretório que definirá qual a secção será utilizada no arquivo config.ini
        # name: str -> Nome da subsecção que será salva no arquivo config.ini
        # last_dir: str -> Valor que será salvo no arquivo config.ini
    
    import configparser
    config = configparser.ConfigParser() # Cria um objeto config como instância da classe ConfigParser
    config.read('config.ini') # Lê o arquivo config.ini
    if not config.has_section(diretorio): # Verifica se a secção diretorio existe no arquivo config.ini
        config.add_section(diretorio) # Adiciona a secção diretorio no arquivo config.ini
    config.set(diretorio, name, last_dir) # Seta os valores da secção, subsecção e valor no arquivo config.ini
    with open('config.ini', 'w') as configfile: # Abre o arquivo config.ini em modo de escrita
        config.write(configfile) # Escreve as alterações no arquivo config.ini

def carregar_diretorio(diretorio, dir_busca):
    # Função para carregar os dados do arquivo config.ini
    # Args:
        # diretorio: str -> Diretório que definirá qual a secção será lida no arquivo config.ini
        # dir_busca: str -> Nome da subsecção que será lida no arquivo config.ini
    
    import configparser
    config = configparser.ConfigParser() # Cria um objeto config como instância da classe ConfigParser
    config.read('config.ini') # Lê o arquivo config.ini
    return config[diretorio][dir_busca] if config.has_option(diretorio, dir_busca) else None # Retorna o valor da subsecção dir_busca da secção diretorio do arquivo config.ini se existir, caso contrário retorna None
    
def Caminho_Banco_Dir(self, Banco_Screen, entrys_list):
    # Função para abrir uma janela de seleção de arquivo e obter o caminho do banco de dados
    # Args:
        # Banco_Screen: ctk.CTkToplevel -> Tela que será utilizada como parent da janela de seleção de arquivo
        # entrys_list: list -> Lista de entrys que serão utilizadas para armazenar os dados informados pelo usuário para obtenção dos valores escolhidos
        
    from tkinter import filedialog # Importa a função filedialog da biblioteca tkinter
    
    dir = carregar_diretorio('Banco', 'last_dir') # Carrega o último caminho do banco de dados utilizado do arquivo config.ini
    
    # Abre a janela de seleção de arquivo e obtém o caminho do banco de dados usando como parent a tela Banco_Screen e como caminho padrão o ultimo local usado pelo usuário
    caminho = filedialog.askopenfilename(title= 'Caminho para o banco de dados', parent= Banco_Screen, filetypes= [('Firebird Database', '*.fdb')], initialdir= dir)
    if caminho: # Verifica se o caminho foi obtido
        entrys_list[2].delete(0, 'end') # Deleta o conteúdo do entry
        entrys_list[2].insert(0, caminho) # Insere o caminho obtido no entry
        salvar_diretorio('Banco', 'last_dir', caminho[:caminho.rfind('/')]) # Salva o caminho obtido no arquivo config.ini
        
def Caminho_Fb_Dir(self, Banco_Screen, entrys_list):
    # Função para abrir uma janela de seleção de arquivo e obter o caminho da fbclient
    # Args:
        # Banco_Screen: ctk.CTkToplevel -> Tela que será utilizada como parent da janela de seleção de arquivo
        # entrys_list: list -> Lista de entrys que serão utilizadas para armazenar os dados informados pelo usuário para obtenção dos valores escolhidos
    
    # Funcionamento idêntico ao da função Caminho_Banco_Dir
    from tkinter import filedialog
    
    dir = carregar_diretorio('FBClient', 'last_dir')
    caminho = filedialog.askopenfilename(title= 'Caminho para o fbclient',parent= Banco_Screen, filetypes= [('Firebird Dll', '*.dll')], initialdir= dir)
    if caminho:
        entrys_list[3].delete(0, 'end')
        entrys_list[3].insert(0, caminho)
        salvar_diretorio('FBClient', 'last_dir', caminho[:caminho.rfind('/')])
        
def on_click_confirm(self, entrys_list, Banco_Screen, entry_alter_list, button_list):
    # Função realizada ao clicar no botão de confirmar da tela Banco_Screen
    # Args:
        # entrys_list: list -> Lista de entrys que serão utilizadas para armazenar os dados informados pelo usuário para obtenção dos valores escolhidos
        # Banco_Screen: ctk.CTkToplevel -> Tela que será utilizada como parent da janela de seleção de arquivo
        # entry_alter_list: list -> Lista de labels que serão utilizadas para armazenar os valores obtidos do banco de dados
        # button_list: list -> Lista de botões que serão utilizados para habilitar ou desabilitar a interação do usuário com a tela
    
    from Banco_de_Dados.Inventario_Conn import Dados, Connect # Importa as classes Dados e Connect do arquivo Inventario_Conn
    
    from fdb import DatabaseError # Importa a exceção DatabaseError da biblioteca fdb
    
    # Verifica se todos os entrys foram preenchidos
    for entry in entrys_list:
        if entry.get() == '':
            from tkinter import messagebox
            messagebox.showerror('Erro', 'Preencha todos os campos', parent= Banco_Screen)
            return
        
    # Armazena os valores dos entrys na classe Dados do arquivo Inventario_Conn
    for name, var in zip(['host', 'port', 'database', 'fbclient'], entrys_list):
        Dados.banco_dados[name] = var.get()
        
    # Tenta realizar a conexão com o banco de dados
    try:
        Connect.fdb_conn()
    except Exception as e:
        # Caso ocorra um erro, exibe uma mensagem de erro
        from tkinter import messagebox
        messagebox.showerror('Erro', f'Não foi possível conectar ao banco de dados\n {e}', parent= Banco_Screen)
        return # Para a execução função
    
    # Salva os valores dos entrys no arquivo config.ini
    salvar_diretorio('Porta', 'last_dir', entrys_list[1].get()) 
    salvar_diretorio('FBClient', 'dir_banco', entrys_list[3].get())
    
    # Tenta buscar os dados da empresa no banco de dados
    try:
        Connect.cursor.execute('SELECT NOME, RSOCIAL, CNPJ, CGF, CODCRT, FONE FROM PROPRI')
        val_brut = Connect.cursor.fetchone()
    except Exception as e:
        # Mesmo Funcionamento do bloco try anterior
        from tkinter import messagebox
        messagebox.showerror('Erro', f'Não foi possível buscar os dados\n {e}', parent= Banco_Screen)
        return
    
    try:
        # Realiza 3 consultas no banco de dados para buscar a data da ultima emissão de Nota Fiscal, Cupom Fiscal e NFC-e, após obter salva o valor em uma lista
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
        # Mesmo Funcionamento do bloco try anterior
        from tkinter import messagebox
        messagebox.showerror('Erro', f'Não foi possível buscar as datas\n {e}', parent= Banco_Screen)
        return
    
    # Desempacota os valores brutos dos dados da empresa obtidos do banco de dados
    nome, rsocial, cnpj, cgf, codcrt, fone = val_brut
    if codcrt == '0':
        codcrt = 'Simples Nacional' # Converte o valor de codcrt para um valor mais legível
    elif codcrt == '1':
        codcrt = 'Simples Nacional - Excesso de Sublimite de Receita Bruta' # Converte o valor de codcrt para um valor mais legível
    elif codcrt == '2':
        codcrt = 'Regime Normal' # Converte o valor de codcrt para um valor mais legível
    
    max_data = max(datas) if datas else 'Sem emissões' # Verifica se a lista datas está vazia, se não estiver, pega a maior data, se estiver, retorna 'Sem emissões'
    if max_data != 'Sem emissões': # Verifica se max_data é diferente de 'Sem emissões'
        max_data = max_data.strftime('%d/%m/%Y') # Converte max_data para o formato 'dd/mm/aaaa'
    
    val_list = [nome, rsocial, cnpj, cgf, codcrt, fone, max_data] # Cria uma lista com os valores obtidos
    
    Banco_Screen.destroy() # Fecha a tela Banco_Screen
    for label, val in zip(entry_alter_list, val_list): # Altera os valores dos labels com os valores obtidos, vale resaltar que a iteração vai ser item a item, portanto a ordem dos labels na lista deve ser igual a ordem dos valores na lista.
        label.configure(text= val) # Altera o texto do label
    
    for button in button_list: # Itera sobre a lista de botões
        if button.cget('state') == 'disabled': # Verifica se o estado do botão é 'disabled'
            button.configure(state = 'normal') # Altera o estado do botão para 'normal'
            

    