import customtkinter as ctk

### Aqui temos o arquivo principal do programa, onde é criada a classe Inventário, bem como o widget root e suas funcionalidades ###


class Inventario:
    def __init__(self, root):
        # Importações de outros arquivos do sistema segundo a Lógica: from [Pasta].[Arquivo] import [Classe ou Função]
        from Banco_de_Dados.Tela_Banco_Dados.Banco_de_Dados_Screen import Interface_Banco
        from Inv_Screen.Inv_Top_Frame import criar_top_frame
        from Consultas.Generics_Functions.Gen_Funcs_Consulta import event_button_comando, event_button_consulta
        from Outros.Datas_Config import date_treat, data_select_ini, data_select_fim
        from Outros.Banco_Images import TelaInicial
        from Banco_de_Dados.Tela_Banco_Dados.Banco_de_Dados_Func import carregar_diretorio
        from Interface_Tools.Tk_Tooltip import ToolTip

        # Importações de bibliotecas externas
        from tkcalendar import DateEntry
        import datetime

        # Definição do tema do sistema e da variável correspondente
        self.color_theme = carregar_diretorio('Configurações', 'Cor_do_tema')
        if self.color_theme is None:
            self.color_theme = 'System'

        ctk.set_appearance_mode(self.color_theme)
        ctk.set_default_color_theme("dark-blue")

        # Definiçõa do widget root bem como suas configurações
        self.root = root
        self.root.title("Configurações de Inventario")  # Título da janela
        # Tamanho e posição da janela no seguinte formato "LarguraxAltura+PosiçãoX+PosiçãoY"
        self.root.geometry("530x200+80+60")
        # Impede que a janela seja redimensionada
        self.root.resizable(False, False)
        self.root.focus_set()  # Foca na janela

        entry_alter_list = []

        # Cria-se dois frames, um superior(top) e outro inferior(bot), onde serão inseridos os widgets
        self.frame_top = criar_top_frame(self, root, entry_alter_list, width=530,
                                         height=60, border_width=2, border_color='silver', corner_radius=2)

        # StringVars para armazenar as datas inicial e final
        self.ini_date = ctk.StringVar()
        self.end_date = ctk.StringVar()

        # StringVar para armazenar a data selecionada no DateEntry

        # Variáveis responsáveis por armazenar as imagens usadas na tela

        # Definição das datas inicial e final como o primeiro e último dia do ano passado
        ano_atual = datetime.datetime.now().year
        ano_vigencia = ano_atual - 1
        # Definir o primeiro e último dia do ano passado
        primeiro_dia = datetime.datetime(ano_vigencia, 1, 1)
        ultimo_dia = datetime.datetime(ano_vigencia, 12, 31)

        # Formatar as datas como strings
        primeiro_dia_str = primeiro_dia.strftime('%d/%m/%Y')
        ultimo_dia_str = ultimo_dia.strftime('%d/%m/%Y')

        # Setar as datas
        # self.dat_ini.set_date(primeiro_dia_str)
        # self.dat_fim.set_date(ultimo_dia_str)
        # self.data_banco_inicial = primeiro_dia.strftime('%d.%m.%Y')
        # self.data_banco_final = ultimo_dia.strftime('%d.%m.%Y')

        # Lista de widgets que serão utilizados

        # Binds de eventos utilizados na tela
        self.root.bind(
            '<F1>', lambda event: event_button_consulta(self, event))
        self.root.bind('<F2>', lambda event: event_button_comando(self, event))
        # self.root.bind('<Control-b>', lambda event: Interface_Banco(self,
        #                self.root, entry_alter_list, button_list))
        self.ini_date.trace_add(
            "write", lambda *args: date_treat(self, self.ini_date, 'Inicial'))
        self.end_date.trace_add(
            "write", lambda *args: date_treat(self, self.end_date, 'Final'))
        # self.dat_ini.bind("<<DateEntrySelected>>",
        #                   lambda event: data_select_ini(self, self.ini_date))
        # self.dat_fim.bind("<<DateEntrySelected>>",
        #                   lambda event: data_select_fim(self, self.end_date))


# Condição usada caso o sistema seja executado diretamente, sem ser importado por outro arquivo
if __name__ == '__main__':
    try:
        # Criação do widget root e instanciação da classe Inventario
        root = ctk.CTk()
        app = Inventario(root)
        root.mainloop()
    finally:
        # Fechamento da conexão com o banco de dados
        from Banco_de_Dados.Conexao_Banco_Dados.Inventario_Conn import BancoDeDados
        if BancoDeDados.retorna_gerenciador():
            gerenciador = BancoDeDados.gerenciador()
            gerenciador.fechar()
