from customtkinter import CTkFrame, CTkLabel

from Interface_Tools.Tk_Tooltip import ToolTip


def _create_company_labels(master, entry_alter_list):
    nome_empresa_label = CTkLabel(
        master, text='', width=20, height=2, font=('', 18, 'bold'))
    razao_social_label = CTkLabel(
        master, text='Razão Social:', width=20, height=2, font=('', 12))
    razao_social_text = CTkLabel(
        master, text='', width=20, height=2, font=('', 12))
    cnpj_label = CTkLabel(
        master, text='CNPJ:', width=20, height=2, font=('', 12))
    cnpj_text = CTkLabel(
        master, text='', width=20, height=2, font=('', 12))
    ie_label = CTkLabel(
        master, text='Inscrição Estadual:', width=20, height=2, font=('', 12))
    ie_text = CTkLabel(
        master, text='', width=20, height=2, font=('', 12))
    regime_label = CTkLabel(
        master, text='Regime Tributário:', width=20, height=2, font=('', 12))
    regime_text = CTkLabel(
        master, text='', width=20, height=2, font=('', 12))
    fone_label = CTkLabel(
        master, text='Telefone:', width=20, height=2, font=('', 12))
    fone_text = CTkLabel(
        master, text='', width=20, height=2, font=('', 12))
    ult_emit = CTkLabel(
        master, text='Última Emissão:', width=20, height=2, font=('', 12))
    ult_emit_text = CTkLabel(
        master, text='', width=20, height=2, font=('', 12))
    credits = CTkLabel(master, text='Desenvolvido por: Daniel Amorim',
                       width=20, height=2, font=('', 11, 'italic'))

    entry_alter_list.extend([nome_empresa_label, razao_social_text,
                             cnpj_text, ie_text, regime_text, fone_text, ult_emit_text])

    nome_empresa_label.place(relx=0.5, rely=0.11, anchor='center')
    razao_social_label.place(relx=0.011, rely=0.20, anchor='nw')
    razao_social_text.place(relx=0.158, rely=0.20, anchor='nw')
    cnpj_label.place(relx=0.011, rely=0.32, anchor='nw')
    cnpj_text.place(relx=0.083, rely=0.32, anchor='nw')
    ie_label.place(relx=0.011, rely=0.43, anchor='nw')
    ie_text.place(relx=0.215, rely=0.43, anchor='nw')
    regime_label.place(relx=0.011, rely=0.55, anchor='nw')
    regime_text.place(relx=0.213, rely=0.55, anchor='nw')
    fone_label.place(relx=0.011, rely=0.67, anchor='nw')
    fone_text.place(relx=0.117, rely=0.67, anchor='nw')
    ult_emit.place(relx=0.011, rely=0.80, anchor='nw')
    ult_emit_text.place(relx=0.189, rely=0.80, anchor='nw')
    credits.place(relx=0.83, rely=0.96, anchor='s')

    ToolTip(credits, 'Com a ajuda de Cicero Romão (RIP) nas consultas SQL', 700)


def criar_bot_frame(master, entry_alter_list, *args, **kwargs):
    bot_frame = CTkFrame(master, *args, **kwargs)
    bot_frame.pack()
    _create_company_labels(bot_frame, entry_alter_list)
    return bot_frame
