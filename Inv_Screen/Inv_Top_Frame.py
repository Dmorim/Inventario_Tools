import datetime
from customtkinter import CTkFrame, CTkButton, CTkLabel, CTkRadioButton, CTkComboBox, IntVar, CTkImage, StringVar
from tkcalendar import DateEntry

from Consultas.Consultas_Screen import Consulta_Total_Screen
from Comandos.Comandos_Gerais.Comandos_Screen import Comandos_Screen
from Banco_de_Dados.Tela_Banco_Dados.Banco_de_Dados_Screen import Interface_Banco
from Configuracoes.Config_Screen import config_screen
from Tutorial.Tutorial_Screen import tutorial_screen
from Dashboard.Dashboard_Screen import Dashboard_Screen
from Outros.Banco_Images import TelaInicial
from Outros.Periodo_Inventario import TIPO_ANUAL, TIPO_MENSAL, TIPO_PERSONALIZADO, MESES, MESES_REVERSO, periodo_padrao, calcular_periodo
from Consultas.Generics_Functions.Gen_Funcs_Consulta import event_invoke_button
from Data_Manager.PeriodoInventario import PeriodoInventario


def _alternar_controles_periodo(grupo_controles, posicoes, data_setada):
    for controle, posicao in posicoes.items():
        controle.place_forget()
    for controle in grupo_controles[data_setada.get()]:
        controle.place(**posicoes[controle])


def _create_command_buttons(periodo_manager, master, root, entrys_list: list):
    def obter_periodo_dos_controles():
        tipo = data_setada.get()

        if tipo == TIPO_MENSAL:
            mes = MESES_REVERSO.get(mes_combo.get())
            if mes is None:
                mes = datetime.date.today().month
            return calcular_periodo(TIPO_MENSAL, mes=mes)

        elif tipo == TIPO_PERSONALIZADO:
            return calcular_periodo(TIPO_PERSONALIZADO,
                                    ini=date_entry_ini.get_date(),
                                    fim=date_entry_fim.get_date())

        elif tipo == TIPO_ANUAL:
            ano = int(ano_combo.get()) if ano_combo.get(
            ) else datetime.date.today().year
            return calcular_periodo(TIPO_ANUAL, ano=ano)

        return periodo_padrao()

    def atualizar_periodo_manager():
        inicio, fim = obter_periodo_dos_controles()
        periodo_manager.atualizar_periodo(PeriodoInventario(inicio, fim))

    def abrir_tela(tela, *args):
        atualizar_periodo_manager()
        tela(periodo_manager, *args)

    def exibir_periodo_atual():
        _alternar_controles_periodo(grupo_controles, posicoes, data_setada)

    gear_image = CTkImage(
        TelaInicial.gear_image_tela_inicial, size=(14, 14))
    help_image = CTkImage(
        TelaInicial.help_image_tela_inicial, size=(14, 14))

    consulta = CTkButton(master, text='Consultas (F1)', width=80, height=48,
                         command=lambda: abrir_tela(Consulta_Total_Screen, root), state='normal')
    comando = CTkButton(master, text='Comandos (F2)', width=60, height=48,
                        command=lambda: abrir_tela(Comandos_Screen, root), state='disabled')
    database = CTkButton(master, text='Selecione o Banco de Dados', width=100,
                         height=48, command=lambda: Interface_Banco(master, entrys_list, [consulta, comando, dashboard]))
    dashboard = CTkButton(master, text='Dashboard (F3)', width=70, height=48,
                          command=lambda: abrir_tela(Dashboard_Screen, root, dashboard), state='disabled')

    data_setada = IntVar(value=TIPO_ANUAL)

    radio_ano = CTkRadioButton(
        master, text='Inv. Anual', variable=data_setada, radiobutton_height=14, radiobutton_width=14, height=10, corner_radius=55, font=('', 11, 'bold'), border_width_checked=10, hover_color='lightblue', value=TIPO_ANUAL, command=exibir_periodo_atual)
    radio_mes = CTkRadioButton(
        master, text='Inv. Mensal', variable=data_setada, radiobutton_height=14, radiobutton_width=14, height=10, corner_radius=55, font=('', 11, 'bold'), border_width_checked=10, hover_color='lightblue', value=TIPO_MENSAL, command=exibir_periodo_atual)
    radio_personalizado = CTkRadioButton(
        master, text='Escolha...', variable=data_setada, radiobutton_height=14, radiobutton_width=14, height=10, corner_radius=55, font=('', 11, 'bold'), border_width_checked=10, hover_color='lightblue', value=TIPO_PERSONALIZADO, command=exibir_periodo_atual)

    gear_btt = CTkButton(master, text='', width=14, height=14, image=gear_image,
                         command=lambda: config_screen(master), fg_color='#d04404')
    help_btt = CTkButton(master, text='', width=14, height=14,
                         image=help_image, fg_color='#d04404', command=lambda: tutorial_screen(master))

    hoje = datetime.datetime.now()
    anos = [str(ano) for ano in range(hoje.year - 5, hoje.year)]
    meses = [MESES[mes] for mes in range(1, hoje.month, 1)] if hoje.month > 1 else [
        MESES[12]]

    ano_combo = CTkComboBox(master, values=anos,
                            width=90, height=13, font=('', 13), state='readonly')
    ano_combo.set(str(hoje.year - 1))

    mes_combo = CTkComboBox(master, values=meses,
                            width=90, height=13, font=('', 13), state='readonly')
    mes_combo.set(MESES.get(hoje.month - 1, '')
                  if hoje.month > 1 else MESES.get(12, ''))

    ini_date = StringVar()
    end_date = StringVar()

    dat_ini_label = CTkLabel(master, text='De:', width=2, font=('', 12))
    date_entry_ini = DateEntry(master, width=11, background='darkblue', foreground='white',
                               borderwidth=2, textvariable=ini_date, date_pattern='dd/mm/yyyy', firstweekday='sunday')
    dat_fim_label = CTkLabel(master, text='Até:', width=2, font=('', 12))
    date_entry_fim = DateEntry(master, width=11, background='darkblue', foreground='white',
                               borderwidth=2, textvariable=end_date, date_pattern='dd/mm/yyyy', firstweekday='sunday')

    database._text_label.configure(wraplength=100)
    consulta._text_label.configure(wraplength=70)
    comando._text_label.configure(wraplength=70)
    dashboard._text_label.configure(wraplength=70)

    database.place(relx=0.01, rely=0.1, anchor='nw')
    consulta.place(relx=0.187, rely=0.1, anchor='nw')
    comando.place(relx=0.322, rely=0.1, anchor='nw')
    dashboard.place(relx=0.449, rely=0.1, anchor='nw')

    radio_ano.place(relx=0.580, rely=0.08, anchor='nw')
    radio_mes.place(relx=0.580, rely=0.38, anchor='nw')
    radio_personalizado.place(relx=0.580, rely=0.68, anchor='nw')

    grupo_controles = {
        TIPO_ANUAL: [ano_combo],
        TIPO_MENSAL: [mes_combo],
        TIPO_PERSONALIZADO: [dat_ini_label, date_entry_ini, dat_fim_label, date_entry_fim],
    }
    posicoes = {
        ano_combo: dict(relx=0.75, rely=0.08, anchor='nw'),
        mes_combo: dict(relx=0.75, rely=0.32, anchor='nw'),
        dat_ini_label: dict(relx=0.745, rely=0.05, anchor='nw'),
        date_entry_ini: dict(relx=0.795, rely=0.1, anchor='nw'),
        dat_fim_label: dict(relx=0.745, rely=0.50, anchor='nw'),
        date_entry_fim: dict(relx=0.795, rely=0.53, anchor='nw'),
    }

    exibir_periodo_atual()

    gear_btt.place(relx=0.933, rely=0.1, anchor='nw')
    help_btt.place(relx=0.933, rely=0.5, anchor='nw')

    root.bind(
        '<F1>', lambda event: event_invoke_button(event, consulta))
    root.bind(
        '<F2>', lambda event: event_invoke_button(event, comando))
    root.bind(
        '<F3>', lambda event: event_invoke_button(event, dashboard))
    root.bind(
        'B', lambda event: event_invoke_button(event, database))


def criar_top_frame(periodo_manager, master, root, entry_list: list, *args, **kwargs):
    top_frame = CTkFrame(master, *args, **kwargs)
    top_frame.pack()
    _create_command_buttons(periodo_manager, top_frame, root, entry_list)

    return top_frame
