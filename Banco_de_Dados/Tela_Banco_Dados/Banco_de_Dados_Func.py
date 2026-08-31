import ctypes
from ctypes import wintypes
from tkinter import filedialog
from tkinter import messagebox

from Configuracoes.Config_Manager import salvar_diretorio, carregar_diretorio
from Queries.Consulta_Queries import QUERY_PROPRI, QUERY_EMISSOES
from Banco_de_Dados.Conexao_Banco_Dados.Inventario_Conn import ConfiguracaoBanco, BancoDeDados
from Thread_Manager.Query_Operations import query_executor, query_selector
from Thread_Manager.Thread_Executor import thread_execução
from Interface_Tools.Tk_Progress_Bar import ProgressBarHandler


def Set_Dados_Padrao(entrys_list):
    if len(entrys_list) != 4:
        raise ValueError(
            "A lista de entrys deve conter exatamente 4 elementos.")

    entrys_dict = {
        entrys_list[0]: carregar_diretorio('Servidor', 'last_dir') or 'localhost',
        entrys_list[1]: carregar_diretorio('Porta', 'last_dir') or '3050',
        entrys_list[2]: '',
        entrys_list[3]: carregar_diretorio(
            'FBClient', 'dir_banco') or 'C:/Program Files/Firebird/Firebird_3_0/bin/fbclient.dll'
    }
    for entry, value in entrys_dict.items():
        entry.delete(0, 'end')
        entry.insert(0, value)


def Caminho_Banco_Dir(Banco_Screen, entrys_list):
    dir = carregar_diretorio('Banco', 'last_dir')

    # Abre a janela de seleção de arquivo e obtém o caminho do banco de dados usando como parent a tela Banco_Screen e como caminho padrão o ultimo local usado pelo usuário
    caminho = filedialog.askopenfilename(title='Caminho para o banco de dados', parent=Banco_Screen, filetypes=[
                                         ('Firebird Database', '*.fdb')], initialdir=dir)
    if caminho:  # Verifica se o caminho foi obtido
        entrys_list[2].delete(0, 'end')  # Deleta o conteúdo do entry
        entrys_list[2].insert(0, caminho)  # Insere o caminho obtido no entry


def Caminho_Fb_Dir(Banco_Screen, entrys_list):
    dir = carregar_diretorio('FBClient', 'last_dir')
    caminho = filedialog.askopenfilename(title='Caminho para o fbclient', parent=Banco_Screen, filetypes=[
                                         ('Firebird Dll', '*.dll')], initialdir=dir)
    if caminho:
        entrys_list[3].delete(0, 'end')
        entrys_list[3].insert(0, caminho)


def _iniciar_animacao(parent, texto_base):
    estados = ['.', '..', '...']
    ciclo = {'i': 0, 'job': None}

    def tick():
        parent.configure(text=f'{texto_base}{estados[ciclo["i"]]}')
        ciclo['i'] = (ciclo['i'] + 1) % len(estados)
        ciclo['job'] = parent.after(500, tick)

    def stop(texto_final=''):
        if ciclo['job'] is not None:
            parent.after_cancel(ciclo['job'])
            ciclo['job'] = None
        parent.configure(text=texto_final)

    tick()  # Inicia a animação
    return stop


def on_click_confirm(entrys_list, Banco_Screen, entry_alter_list, button_list, confirm_button, status_label):
    def centraliza_tela():
        # Calcula a posição central da tela para o progress bar
        screen_width = Banco_Screen.winfo_screenwidth()
        screen_height = Banco_Screen.winfo_screenheight()
        progress_x = (screen_width // 2) - (Banco_Screen.winfo_width() // 2)
        progress_y = (screen_height // 2) - (Banco_Screen.winfo_height() // 2)
        return progress_x, progress_y

    def executa_conexao():
        progress_bar.create_screen()
        progress_bar.atualizar_status("Conectando ao banco de dados...")
        if BancoDeDados.retorna_gerenciador() is not None:
            BancoDeDados.fechar()  # Cria o gerenciador de conexões

        BancoDeDados.conectar()  # Cria o gerenciador de conexões

        salvar_diretorio('Servidor', 'last_dir', entrys_list[0].get())
        salvar_diretorio('Porta', 'last_dir', entrys_list[1].get())
        salvar_diretorio('FBClient', 'dir_banco', entrys_list[3].get())

    def ao_conectar(_):
        parar_animacao('Conectado ao banco de dados')  # Para a animação
        _disparar_queries()

    def ao_conectar_erro(erro):
        parar_animacao('Erro ao conectar ao banco de dados')  # Para a animação
        progress_bar.finalizar()
        confirm_button.configure(state='normal')
        messagebox.showerror(
            'Erro', f'Não foi possível conectar ao banco de dados\n {erro}', parent=Banco_Screen)

    def _disparar_queries():
        resultados = {}

        parar_propri = _iniciar_animacao(
            status_label, 'Buscando dados da empresa')
        parar_emissoes = [None]

        def finalizar():
            propri = resultados['propri']
            datas = resultados['datas']

            nome, rsocial, cnpj, cgf, codcrt, fone = propri[0]

            codcrt_map = {
                '0': 'Simples Nacional',
                '1': 'Simples Nacional - Excesso de Sublimite de Receita Bruta',
                '2': 'Regime Normal'
            }

            codcrt = codcrt_map.get(codcrt, codcrt)
            max_data = datas[0][0].strftime(
                '%d/%m/%Y') if datas and datas[0][0] is not None else 'Sem emissões'

            val_list = [nome, rsocial, cnpj, cgf, codcrt, fone, max_data]
            progress_bar.finalizar()
            Banco_Screen.destroy()

            for label, val in zip(entry_alter_list, val_list):
                label.configure(text=val)

            for button in button_list:
                if button.cget('state') == 'disabled':
                    button.configure(state='normal')

        def buscar_propri():
            return query_executor(query_selector, query_propri)

        def finalizar_propri(rows):
            parar_propri('Dados da empresa obtidos')
            resultados['propri'] = rows
            parar_emissoes[0] = _iniciar_animacao(
                status_label, 'Buscando datas de emissão')
            if 'datas' in resultados:
                parar_emissoes[0]('Datas de emissão obtidas')
                progress_bar.atualizar_status("Datas de emissão obtidas")
                finalizar()

        def falha_propri(erro):
            parar_propri('Erro ao buscar dados da empresa')
            confirm_button.configure(state='normal')
            messagebox.showerror(
                'Erro', f'Não foi possível buscar os dados da empresa\n {erro}', parent=Banco_Screen)

        def buscar_datas():
            return query_executor(query_selector, query_emissoes)

        def ao_terminar_datas(rows):
            resultados['datas'] = rows
            if 'propri' in resultados:
                if parar_emissoes[0]:
                    parar_emissoes[0]('Datas de emissão obtidas')
                    progress_bar.atualizar_status("Datas de emissão obtidas")
                finalizar()

        def falha_datas(erro):
            if parar_emissoes[0]:
                parar_emissoes[0]('Erro ao buscar datas de emissão')
            confirm_button.configure(state='normal')
            messagebox.showerror(
                'Erro', f'Não foi possível buscar as datas de emissão\n {erro}', parent=Banco_Screen)

        thread_execução(Banco_Screen, buscar_propri,
                        finalizar_propri, falha_propri)
        thread_execução(Banco_Screen, buscar_datas,
                        ao_terminar_datas, falha_datas)

    # Verifica se todos os entrys foram preenchidos
    for entry in entrys_list:
        if entry.get() == '':
            messagebox.showerror(
                'Erro', 'Preencha todos os campos', parent=Banco_Screen)
            return

    ConfiguracaoBanco.definir(
        host=entrys_list[0].get(),
        port=entrys_list[1].get(),
        database=obter_caminho_curto_banco_dados(entrys_list[2].get()),
        fbclient=entrys_list[3].get(),
        user='SYSDBA',
        password='masterkey'
    )

    progress_x, progress_y = centraliza_tela()
    progress_bar = ProgressBarHandler(
        Banco_Screen, "Aguarde", x=progress_x, y=progress_y)

    # Desabilita o botão de confirmar para evitar múltiplos cliques
    confirm_button.configure(state='disabled')

    parar_animacao = _iniciar_animacao(
        status_label, 'Conectando ao banco de dados')

    query_propri = QUERY_PROPRI
    query_emissoes = QUERY_EMISSOES

    thread_execução(Banco_Screen, executa_conexao,
                    ao_conectar, ao_conectar_erro)
    # Salva os valores dos entrys no arquivo config.ini


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
        raise RuntimeError(f"Erro ao obter o caminho curto: {e}")
