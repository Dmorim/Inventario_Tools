import datetime
from customtkinter import CTkFrame, CTkButton, CTkLabel, CTkRadioButton, CTkComboBox, IntVar, CTkImage, StringVar
from tkcalendar import DateEntry

from Consultas.Consultas_Screen import Consulta_Total_Screen
from Comandos.Comandos_Gerais.Comandos_Screen import Comandos_Screen
from Banco_de_Dados.Tela_Banco_Dados.Banco_de_Dados_Screen import Interface_Banco
from Configuracoes.Config_Screen import config_screen
from Tutorial.Tutorial_Screen import tutorial_screen
from Outros.Banco_Images import TelaInicial
from Outros.Periodo_Inventario import TIPO_ANUAL, TIPO_MENSAL, TIPO_PERSONALIZADO, MESES, periodo_padrao
from Consultas.Generics_Functions.Gen_Funcs_Consulta import event_invoke_button


def _alternar_controles_periodo(app_self, grupo_controles, posicoes):
    for controle, posicao in posicoes.items():
        controle.place_forget()
    for controle in grupo_controles[app_self.data_setada.get()]:
        controle.place(**posicoes[controle])


def _create_command_buttons(app_self, master, entrys_list: list):
    gear_image = CTkImage(
        TelaInicial.gear_image_tela_inicial, size=(14, 14))
    help_image = CTkImage(
        TelaInicial.help_image_tela_inicial, size=(14, 14))

    consulta = CTkButton(master, text='Consultas (F1)', width=80, height=48,
                         command=lambda: Consulta_Total_Screen(app_self, master), state='disabled')
    comando = CTkButton(master, text='Comandos (F2)', width=60, height=48,
                        command=lambda: Comandos_Screen(app_self, master), state='disabled')
    database = CTkButton(master, text='Selecione o Banco de Dados', width=100,
                         height=48, command=lambda: Interface_Banco(app_self, master, entrys_list, [consulta, comando]))

    app_self.data_setada = IntVar(value=TIPO_ANUAL)

    def exibir_periodo_atual():
        _alternar_controles_periodo(app_self, grupo_controles, posicoes)

    app_self.exibir_periodo_atual = exibir_periodo_atual

    radio_ano = CTkRadioButton(
        master, text='Inv. Anual', variable=app_self.data_setada, radiobutton_height=14, radiobutton_width=14, height=10, corner_radius=55, font=('', 11, 'bold'), border_width_checked=10, hover_color='lightblue', value=TIPO_ANUAL, command=app_self.exibir_periodo_atual)
    radio_mes = CTkRadioButton(
        master, text='Inv. Mensal', variable=app_self.data_setada, radiobutton_height=14, radiobutton_width=14, height=10, corner_radius=55, font=('', 11, 'bold'), border_width_checked=10, hover_color='lightblue', value=TIPO_MENSAL, command=app_self.exibir_periodo_atual)
    radio_personalizado = CTkRadioButton(
        master, text='Escolha...', variable=app_self.data_setada, radiobutton_height=14, radiobutton_width=14, height=10, corner_radius=55, font=('', 11, 'bold'), border_width_checked=10, hover_color='lightblue', value=TIPO_PERSONALIZADO, command=app_self.exibir_periodo_atual)

    gear_btt = CTkButton(master, text='', width=14, height=14, image=gear_image,
                         command=lambda: config_screen(app_self, master), fg_color='#d04404')
    help_btt = CTkButton(master, text='', width=14, height=14,
                         image=help_image, fg_color='#d04404', command=lambda: tutorial_screen(master))

    hoje = datetime.datetime.now()
    anos = [str(ano) for ano in range(hoje.year - 5, hoje.year)]
    meses = [MESES[mes] for mes in range(1, hoje.month, 1)] if hoje.month > 1 else [
        MESES[12]]

    app_self.ano_combo = CTkComboBox(master, values=anos,
                                     width=90, height=13, font=('', 13), state='readonly')
    app_self.ano_combo.set(str(hoje.year - 1))

    app_self.mes_combo = CTkComboBox(master, values=meses,
                                     width=90, height=13, font=('', 13), state='readonly')
    app_self.mes_combo.set(MESES.get(hoje.month - 1, '')
                           if hoje.month > 1 else MESES.get(12, ''))

    app_self.ini_date = StringVar()
    app_self.end_date = StringVar()

    dat_ini_label = CTkLabel(master, text='De:', width=2, font=('', 12))
    app_self.dat_ini = DateEntry(master, width=11, background='darkblue', foreground='white',
                                 borderwidth=2, textvariable=app_self.ini_date, date_pattern='dd/mm/yyyy', firstweekday='sunday')
    dat_fim_label = CTkLabel(master, text='Até:', width=2, font=('', 12))
    app_self.dat_fim = DateEntry(master, width=11, background='darkblue', foreground='white',
                                 borderwidth=2, textvariable=app_self.end_date, date_pattern='dd/mm/yyyy', firstweekday='sunday')

    inicio, fim = periodo_padrao()
    app_self.dat_ini.set_date(inicio)
    app_self.dat_fim.set_date(fim)

    database._text_label.configure(wraplength=100)
    consulta._text_label.configure(wraplength=70)
    comando._text_label.configure(wraplength=70)

    database.place(relx=0.01, rely=0.1, anchor='nw')
    consulta.place(relx=0.217, rely=0.1, anchor='nw')
    comando.place(relx=0.375, rely=0.1, anchor='nw')

    radio_ano.place(relx=0.522, rely=0.08, anchor='nw')
    radio_mes.place(relx=0.522, rely=0.38, anchor='nw')
    radio_personalizado.place(relx=0.522, rely=0.68, anchor='nw')

    grupo_controles = {
        TIPO_ANUAL: [app_self.ano_combo],
        TIPO_MENSAL: [app_self.mes_combo],
        TIPO_PERSONALIZADO: [dat_ini_label, app_self.dat_ini, dat_fim_label, app_self.dat_fim],
    }
    posicoes = {
        app_self.ano_combo: dict(relx=0.71, rely=0.08, anchor='nw'),
        app_self.mes_combo: dict(relx=0.71, rely=0.32, anchor='nw'),
        dat_ini_label: dict(relx=0.705, rely=0.05, anchor='nw'),
        app_self.dat_ini: dict(relx=0.755, rely=0.1, anchor='nw'),
        dat_fim_label: dict(relx=0.705, rely=0.50, anchor='nw'),
        app_self.dat_fim: dict(relx=0.755, rely=0.53, anchor='nw'),
    }
    exibir_periodo_atual()

    gear_btt.place(relx=0.933, rely=0.1, anchor='nw')
    help_btt.place(relx=0.933, rely=0.5, anchor='nw')

    app_self.root.bind(
        '<F1>', lambda event: event_invoke_button(event, consulta))
    app_self.root.bind(
        '<F2>', lambda event: event_invoke_button(event, comando))
    app_self.root.bind(
        'B', lambda event: event_invoke_button(event, database))


def criar_top_frame(app_self, master, entry_list: list, *args, **kwargs):
    top_frame = CTkFrame(master, *args, **kwargs)
    top_frame.pack()
    _create_command_buttons(app_self, top_frame, entry_list)

    return top_frame
