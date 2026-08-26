def t():
    # Criação dos widgets da tela do frame bot, composto por labels
    nome_empresa_label = ctk.CTkLabel(
        self.frame_bot, text='', width=20, height=2, font=('', 18, 'bold'))
    razao_social_label = ctk.CTkLabel(
        self.frame_bot, text='Razão Social:', width=20, height=2, font=('', 12))
    razao_social_text = ctk.CTkLabel(
        self.frame_bot, text='', width=20, height=2, font=('', 12))
    cnpj_label = ctk.CTkLabel(
        self.frame_bot, text='CNPJ:', width=20, height=2, font=('', 12))
    cnpj_text = ctk.CTkLabel(
        self.frame_bot, text='', width=20, height=2, font=('', 12))
    ie_label = ctk.CTkLabel(
        self.frame_bot, text='Inscrição Estadual:', width=20, height=2, font=('', 12))
    ie_text = ctk.CTkLabel(self.frame_bot, text='',
                           width=20, height=2, font=('', 12))
    regime_label = ctk.CTkLabel(
        self.frame_bot, text='Regime Tributário:', width=20, height=2, font=('', 12))
    regime_text = ctk.CTkLabel(
        self.frame_bot, text='', width=20, height=2, font=('', 12))
    fone_label = ctk.CTkLabel(
        self.frame_bot, text='Telefone:', width=20, height=2, font=('', 12))
    fone_text = ctk.CTkLabel(
        self.frame_bot, text='', width=20, height=2, font=('', 12))
    ult_emit = ctk.CTkLabel(
        self.frame_bot, text='Última Emissão:', width=20, height=2, font=('', 12))
    ult_emit_text = ctk.CTkLabel(
        self.frame_bot, text='', width=20, height=2, font=('', 12))
    credits = ctk.CTkLabel(self.frame_bot, text='Desenvolvido por: Daniel Amorim',
                           width=20, height=2, font=('', 11, 'italic'))

    # Posicionamento dos widgets na tela
    nome_empresa_label.place(relx=0.5, y=15, anchor='center')
    razao_social_label.place(x=6, y=33)
    razao_social_text.place(x=84, y=33)
    cnpj_label.place(x=6, y=50)
    cnpj_text.place(x=44, y=50)
    ie_label.place(x=6, y=66)
    ie_text.place(x=114, y=66)
    regime_label.place(x=6, y=83)
    regime_text.place(x=113, y=83)
    fone_label.place(x=6, y=100)
    fone_text.place(x=62, y=100)
    ult_emit.place(x=6, y=118)
    ult_emit_text.place(x=100, y=118)
    credits.place(relx=0.83, rely=0.96, anchor='s')

    # Criação de um tooltip para o label de créditos
    ToolTip(credits, 'Com a ajuda de Cicero Romão (RIP) nas consultas SQL', 700)


def criar_bot_frame(master, *args, **kwargs):
    bot_frame = CTkFrame(master, *args, **kwargs)
    bot_frame.pack()
    return bot_frame
