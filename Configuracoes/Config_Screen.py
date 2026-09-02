import customtkinter as ctk


from Configuracoes.Config_Func import on_click_confirm, set_default_values


def config_screen(self, parent):
    # Cria a janela config como um Toplevel do parent
    config = ctk.CTkToplevel(parent)
    config.title('Manutenção')
    config.geometry('210x150+400+60')
    config.focus_set()
    config.transient(parent)
    config.grab_set()

    # Cria uma lista com os valores dos temas
    theme_values = ['Claro', 'Escuro', 'Sistema']
    atual_theme = ctk.get_appearance_mode()  # Obtem o tema atual
    # Cria um dicionário com os temas e seus valores aceitos pelo customtkinter
    temas_dict = {'Light': 'Claro', 'Dark': 'Escuro', 'System': 'Sistema'}
    # Criação dos frames da tela de configurações
    title_frame = ctk.CTkFrame(config, width=220, height=25,
                               border_width=2, border_color='silver', corner_radius=7)
    bottom_frame = ctk.CTkFrame(config, width=220, height=125,
                                border_width=2, border_color='silver', corner_radius=7)

    # Criação dos widgets da tela da janela config
    config_title_label = ctk.CTkLabel(
        title_frame, text='Configurações', font=('Arial', 14, 'bold'), height=12)

    # Criação dos widgets da tela do frame bottom
    theme_config_label = ctk.CTkLabel(
        bottom_frame, text='Tema:', font=('verdana', 12))
    theme_config_cbb = ctk.CTkComboBox(bottom_frame, width=85, height=20, font=(
        'verdana', 12), state='readonly', values=theme_values)
    user_db_label = ctk.CTkLabel(
        bottom_frame, text='User DB:', font=('verdana', 12))
    user_db_entry = ctk.CTkEntry(
        bottom_frame, width=105, height=23, font=('verdana', 12))
    pass_db_label = ctk.CTkLabel(
        bottom_frame, text='Pass DB:', font=('verdana', 12))
    pass_db_entry = ctk.CTkEntry(
        bottom_frame, width=105, height=23, font=('verdana', 12), show='*')
    confirm_button = ctk.CTkButton(bottom_frame, text='Confirmar', width=25, height=2,
                                   command=lambda: on_click_confirm(self, config, theme_config_cbb, entry_widgets))
    cancel_button = ctk.CTkButton(
        bottom_frame, text='Cancelar', width=65, height=2, command=lambda: config.destroy())

    theme_config_cbb.set(temas_dict[atual_theme])
    set_default_values([user_db_entry, pass_db_entry])

    # Posicionamento dos frames
    title_frame.pack()
    bottom_frame.pack()

    # Posicionamento dos widgets
    config_title_label.place(relx=0.5, rely=0.5, anchor='center')

    # Posicionamento dos widgets da tela do frame bottom
    theme_config_label.place(x=10, y=6)
    theme_config_cbb.place(x=53, y=10)
    user_db_label.place(x=10, y=35)
    user_db_entry.place(x=68, y=38)
    pass_db_label.place(x=10, y=65)
    pass_db_entry.place(x=68, y=68)
    confirm_button.place(relx=0.678, rely=0.799)
    cancel_button.place(relx=0.342, rely=0.799)

    entry_widgets = [user_db_entry, pass_db_entry]

    # Liga a tecla de atalho Esc para fechar a janela
    config.bind('<Escape>', lambda event: config.destroy())
    # Liga a tecla de atalho F5 para confirmar a escolha do tema
    config.bind('<F5>', lambda event: confirm_button.invoke())
