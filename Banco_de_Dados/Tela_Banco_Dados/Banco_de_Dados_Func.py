import ctypes
from ctypes import wintypes


def Set_Dados_Padrao(entrys_list):
    # Função para preencher os entrys com os dados padrão
    # Args:
    # entrys_list: list -> Lista de entrys que serão utilizadas para armazenar os dados informados pelo usuário para obtenção dos valores escolhidos

    # Carrega a última porta utilizada do arquivo config.ini
    porta = carregar_diretorio('Porta', 'last_dir')
    # Carrega o último caminho da fbclient utilizado do arquivo config.ini
    fbclient = carregar_diretorio('FBClient', 'dir_banco')
    entrys_list[0].insert(0, 'localhost')  # Insere o host padrão
    # Insere a porta padrão
    entrys_list[1].insert(0, porta if porta else '3050')
    entrys_list[3].insert(
        0, fbclient if fbclient else 'C:/Program Files/Firebird/Firebird_3_0/bin/fbclient.dll')


def salvar_diretorio(diretorio, name: str, last_dir):
    # Função para salvar os dados no arquivo config.ini
    # Args:
    # diretorio: str -> Diretório que definirá qual a secção será utilizada no arquivo config.ini
    # name: str -> Nome da subsecção que será salva no arquivo config.ini
    # last_dir: str -> Valor que será salvo no arquivo config.ini

    import configparser
    # Cria um objeto config como instância da classe ConfigParser
    config = configparser.ConfigParser()
    config.read('config.ini')  # Lê o arquivo config.ini
    # Verifica se a secção diretorio existe no arquivo config.ini
    if not config.has_section(diretorio):
        # Adiciona a secção diretorio no arquivo config.ini
        config.add_section(diretorio)
    # Seta os valores da secção, subsecção e valor no arquivo config.ini
    config.set(diretorio, name, last_dir)
    with open('config.ini', 'w') as configfile:  # Abre o arquivo config.ini em modo de escrita
        config.write(configfile)  # Escreve as alterações no arquivo config.ini


def carregar_diretorio(diretorio, dir_busca):
    # Função para carregar os dados do arquivo config.ini
    # Args:
    # diretorio: str -> Diretório que definirá qual a secção será lida no arquivo config.ini
    # dir_busca: str -> Nome da subsecção que será lida no arquivo config.ini

    import configparser
    # Cria um objeto config como instância da classe ConfigParser
    config = configparser.ConfigParser()
    config.read('config.ini')  # Lê o arquivo config.ini
    # Retorna o valor da subsecção dir_busca da secção diretorio do arquivo config.ini se existir, caso contrário retorna None
    return config[diretorio][dir_busca] if config.has_option(diretorio, dir_busca) else None


def Caminho_Banco_Dir(Banco_Screen, entrys_list):
    # Função para abrir uma janela de seleção de arquivo e obter o caminho do banco de dados
    # Args:
    # Banco_Screen: ctk.CTkToplevel -> Tela que será utilizada como parent da janela de seleção de arquivo
    # entrys_list: list -> Lista de entrys que serão utilizadas para armazenar os dados informados pelo usuário para obtenção dos valores escolhidos

    from tkinter import filedialog  # Importa a função filedialog da biblioteca tkinter

    # Carrega o último caminho do banco de dados utilizado do arquivo config.ini
    dir = carregar_diretorio('Banco', 'last_dir')

    # Abre a janela de seleção de arquivo e obtém o caminho do banco de dados usando como parent a tela Banco_Screen e como caminho padrão o ultimo local usado pelo usuário
    caminho = filedialog.askopenfilename(title='Caminho para o banco de dados', parent=Banco_Screen, filetypes=[
                                         ('Firebird Database', '*.fdb')], initialdir=dir)
    if caminho:  # Verifica se o caminho foi obtido
        entrys_list[2].delete(0, 'end')  # Deleta o conteúdo do entry
        entrys_list[2].insert(0, caminho)  # Insere o caminho obtido no entry
        # Salva o caminho obtido no arquivo config.ini
        salvar_diretorio('Banco', 'last_dir', caminho[:caminho.rfind('/')])


def Caminho_Fb_Dir(Banco_Screen, entrys_list):
    # Função para abrir uma janela de seleção de arquivo e obter o caminho da fbclient
    # Args:
    # Banco_Screen: ctk.CTkToplevel -> Tela que será utilizada como parent da janela de seleção de arquivo
    # entrys_list: list -> Lista de entrys que serão utilizadas para armazenar os dados informados pelo usuário para obtenção dos valores escolhidos

    # Funcionamento idêntico ao da função Caminho_Banco_Dir
    from tkinter import filedialog

    dir = carregar_diretorio('FBClient', 'last_dir')
    caminho = filedialog.askopenfilename(title='Caminho para o fbclient', parent=Banco_Screen, filetypes=[
                                         ('Firebird Dll', '*.dll')], initialdir=dir)
    if caminho:
        entrys_list[3].delete(0, 'end')
        entrys_list[3].insert(0, caminho)
        salvar_diretorio('FBClient', 'last_dir', caminho[:caminho.rfind('/')])


def on_click_confirm(entrys_list, Banco_Screen, entry_alter_list, button_list):
    # Função realizada ao clicar no botão de confirmar da tela Banco_Screen
    # Args:
    # entrys_list: list -> Lista de entrys que serão utilizadas para armazenar os dados informados pelo usuário para obtenção dos valores escolhidos
    # Banco_Screen: ctk.CTkToplevel -> Tela que será utilizada como parent da janela de seleção de arquivo
    # entry_alter_list: list -> Lista de labels que serão utilizadas para armazenar os valores obtidos do banco de dados
    # button_list: list -> Lista de botões que serão utilizados para habilitar ou desabilitar a interação do usuário com a tela

    # Importa as classes Dados e Connect do arquivo Inventario_Conn
    from Banco_de_Dados.Conexao_Banco_Dados.Inventario_Conn import ConfiguracaoBanco, BancoDeDados
    from Thread_Manager.Query_Operations import query_executor, query_selector

    from fdb import DatabaseError  # Importa a exceção DatabaseError da biblioteca fdb

    # Verifica se todos os entrys foram preenchidos
    for entry in entrys_list:
        if entry.get() == '':
            from tkinter import messagebox
            messagebox.showerror(
                'Erro', 'Preencha todos os campos', parent=Banco_Screen)
            return

    ConfiguracaoBanco.definir(
        host=entrys_list[0].get(),
        port=entrys_list[1].get(),
        database=obter_caminho_curto_banco_dados(entrys_list[2].get()),
        fbclient=entrys_list[3].get()
    )

    # Tenta realizar a conexão com o banco de dados
    try:
        # Verifica se o gerenciador de conexões ainda não foi criado
        if BancoDeDados.retorna_gerenciador() == None:
            Gerenciador = BancoDeDados.conectar()  # Cria o gerenciador de conexões
        else:
            # Troca a conexão do gerenciador de conexões para a nova conexão criada
            Gerenciador = BancoDeDados.retorna_gerenciador()
            Gerenciador = Gerenciador.trocar_bd(BancoDeDados._criar_conexao)

    except Exception as e:
        # Caso ocorra um erro, exibe uma mensagem de erro
        from tkinter import messagebox
        messagebox.showerror(
            'Erro', f'Não foi possível conectar ao banco de dados\n {e}', parent=Banco_Screen)
        return  # Para a execução função

    # Salva os valores dos entrys no arquivo config.ini
    salvar_diretorio('Porta', 'last_dir', entrys_list[1].get())
    salvar_diretorio('FBClient', 'dir_banco', entrys_list[3].get())

    query_propri = "SELECT NOME, RSOCIAL, CNPJ, CGF, CODCRT, FONE FROM PROPRI"
    query_emissoes = "SELECT MAX(DTEMI) FROM IN01LAN WHERE VENDA IN ('V', 'A', 'W') AND TPMOV = 'N'"

    # Tenta buscar os dados da empresa no banco de dados
    try:
        # Atribui a variável val_brut o resultado da consulta dos dados da empresa
        val_brut = query_executor(query_selector, query_propri)
    except Exception as e:
        # Mesmo Funcionamento do bloco try anterior
        from tkinter import messagebox
        messagebox.showerror(
            'Erro', f'Não foi possível buscar os dados\n {e}', parent=Banco_Screen)
        return

    try:
        data = query_executor(query_selector, query_emissoes)

    except DatabaseError as e:
        # Mesmo Funcionamento do bloco try anterior
        from tkinter import messagebox
        messagebox.showerror(
            'Erro', f'Não foi possível buscar as datas\n {e}', parent=Banco_Screen)
        return

    # Desempacota os valores brutos dos dados da empresa obtidos do banco de dados
    nome, rsocial, cnpj, cgf, codcrt, fone = val_brut
    if codcrt == '0':
        codcrt = 'Simples Nacional'  # Converte o valor de codcrt para um valor mais legível
    elif codcrt == '1':
        # Converte o valor de codcrt para um valor mais legível
        codcrt = 'Simples Nacional - Excesso de Sublimite de Receita Bruta'
    elif codcrt == '2':
        codcrt = 'Regime Normal'  # Converte o valor de codcrt para um valor mais legível

    # Verifica se a lista datas está vazia, se não estiver, pega a maior data, se estiver, retorna 'Sem emissões'
    max_data = data if data is not None else 'Sem emissões'
    if max_data != 'Sem emissões':  # Verifica se max_data é diferente de 'Sem emissões'
        # Converte max_data para o formato 'dd/mm/aaaa'
        max_data = max_data.strftime('%d/%m/%Y')

    # Cria uma lista com os valores obtidos
    val_list = [nome, rsocial, cnpj, cgf, codcrt, fone, max_data]

    Banco_Screen.destroy()  # Fecha a tela Banco_Screen
    # Altera os valores dos labels com os valores obtidos, vale resaltar que a iteração vai ser item a item, portanto a ordem dos labels na lista deve ser igual a ordem dos valores na lista.
    for label, val in zip(entry_alter_list, val_list):
        label.configure(text=val)  # Altera o texto do label

    for button in button_list:  # Itera sobre a lista de botões
        # Verifica se o estado do botão é 'disabled'
        if button.cget('state') == 'disabled':
            # Altera o estado do botão para 'normal'
            button.configure(state='normal')


def obter_caminho_curto_banco_dados(caminho_longo):
    try:
        buffer = ctypes.create_unicode_buffer(wintypes.MAX_PATH)
        ctypes.windll.kernel32.GetShortPathNameW(
            ctypes.c_wchar_p(caminho_longo),
            buffer,
            wintypes.MAX_PATH
        )

        print(f"Caminho curto: {buffer.value}")
        return buffer.value
    except Exception as e:
        # Retorna o original se falhar
        print(f"Erro ao obter caminho curto: {e}")
