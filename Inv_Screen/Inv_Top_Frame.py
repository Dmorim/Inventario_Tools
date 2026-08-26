from customtkinter import CTkFrame, CTkButton, CTkLabel, CTkRadioButton, CTkComboBox, IntVar, CTkImage
import datetime

from Consultas.Consultas_Screen import Consulta_Total_Screen
from Comandos.Comandos_Gerais.Comandos_Screen import Comandos_Screen
from Banco_de_Dados.Tela_Banco_Dados.Banco_de_Dados_Screen import Interface_Banco
from Configuracoes.Config_Screen import config_screen
from Tutorial.Tutorial_Screen import tutorial_screen
from Outros.Banco_Images import TelaInicial


def _create_command_buttons(app_self, master, entrys_list: list):

    data_setada = IntVar(value=0)
    gear_image = CTkImage(
        TelaInicial.gear_image_tela_inicial, size=(14, 14))
    help_image = CTkImage(
        TelaInicial.help_image_tela_inicial, size=(14, 14))

    # Criação dos widgets da tela do frame top, composto por botões, labels e DateEntries
    database = CTkButton(master, text='Selecione o Banco de Dados', width=100,
                         height=48, command=lambda: Interface_Banco(app_self, master, entrys_list, button_list))
    consulta = CTkButton(master, text='Consultas (F1)', width=80, height=48,
                         command=lambda: Consulta_Total_Screen(app_self, master), state='disabled')
    comando = CTkButton(master, text='Comandos (F2)', width=60,
                        height=48, command=lambda: Comandos_Screen(app_self, master), state='disabled')
    radio_ano = CTkRadioButton(
        master, text='Inv. Anual', variable=data_setada, radiobutton_height=14, radiobutton_width=14, height=10, corner_radius=55, font=('', 11, 'bold'), border_width_checked=10, hover_color='lightblue', value=1)
    radio_mes = CTkRadioButton(
        master, text='Inv. Mensal', variable=data_setada, radiobutton_height=14, radiobutton_width=14, height=10, corner_radius=55, font=('', 11, 'bold'), border_width_checked=10, hover_color='lightblue', value=2)
    radio_personalizado = CTkRadioButton(
        master, text='Escolha...', variable=data_setada, radiobutton_height=14, radiobutton_width=14, height=10, corner_radius=55, font=('', 11, 'bold'), border_width_checked=10, hover_color='lightblue', value=3)
    ano_combo = CTkComboBox(master, values=[str(ano) for ano in range(datetime.datetime.now().year - 5, datetime.datetime.now().year)],
                            width=70, height=13, font=('', 12), state='readonly')
    mes_combo = CTkComboBox(master, values=[str(mes) for mes in range(datetime.datetime.now().month, 0, -1)],
                            width=70, height=13, font=('', 12), state='readonly')

    # dat_ini_label = CTkLabel(
    #     master, text='Data Inicial:', width=10, height=2, font=('', 12))
    # dat_ini = DateEntry(master, width=12, background='darkblue', foreground='white',
    #                          borderwidth=2, textvariable=ini_date, date_pattern='dd/mm/yyyy', firstweekday='sunday')
    # dat_fim_label = CTkLabel(
    #     master, text='Data Final:', width=10, height=2, font=('', 12))
    # dat_fim = DateEntry(master, width=12, background='darkblue', foreground='white',
    #                          borderwidth=2, textvariable=end_date, date_pattern='dd/mm/yyyy', firstweekday='sunday')
    gear_btt = CTkButton(master, text='', width=14, height=14, image=gear_image,
                         command=lambda: config_screen(app_self, master), fg_color='#d04404')
    help_btt = CTkButton(master, text='', width=14, height=14,
                         image=help_image, fg_color='#d04404', command=lambda: tutorial_screen(master))

    # Configuração do wraplength(tamanho da linha do texto) dos widgets
    database._text_label.configure(wraplength=100)
    consulta._text_label.configure(wraplength=70)
    comando._text_label.configure(wraplength=70)

    # Posicionamento dos widgets na tela
    database.place(relx=0.01, rely=0.1, anchor='nw')
    consulta.place(relx=0.217, rely=0.1, anchor='nw')
    comando.place(relx=0.375, rely=0.1, anchor='nw')
    # dat_ini_label.place(x=300, y=9)
    # dat_ini.place(x=370, y=6)
    # dat_fim_label.place(x=303, y=35)
    # dat_fim.place(x=370, y=32)

    radio_ano.place(relx=0.522, rely=0.08, anchor='nw')
    radio_mes.place(relx=0.522, rely=0.38, anchor='nw')
    radio_personalizado.place(relx=0.522, rely=0.68, anchor='nw')
    # ano_combo.place(x=385, y=4)
    gear_btt.place(relx=0.933, rely=0.1, anchor='nw')
    help_btt.place(relx=0.933, rely=0.5, anchor='nw')

    button_list = [consulta, comando]


def criar_top_frame(app_self, master, entry_list: list, *args, **kwargs):
    top_frame = CTkFrame(master, *args, **kwargs)
    top_frame.pack()
    _create_command_buttons(app_self, top_frame, entry_list)
    return top_frame
