def config_screen(self, parent):
    import customtkinter as ctk # Importa a biblioteca customtkinter como ctk
    from Configuracoes.Config_Func import on_click_confirm # Importa a função on_click_confirm do arquivo Config_Func
    
    config = ctk.CTkToplevel(parent) # Cria a janela config como um Toplevel do parent
    config.title('Manutenção')
    config.geometry('190x140+320+110')
    config.focus_set()
    config.transient(parent)
    config.grab_set()
    
    theme_values = ['Claro', 'Escuro', 'Sistema'] # Cria uma lista com os valores dos temas
    atual_theme = ctk.get_appearance_mode() # Obtem o tema atual
    temas_dict = {'Light': 'Claro', 'Dark': 'Escuro', 'System': 'Sistema'} # Cria um dicionário com os temas e seus valores aceitos pelo customtkinter
    
    # Criação dos frames da tela de configurações
    title_frame = ctk.CTkFrame(config, width= 190, height= 25, border_width= 2, border_color= 'silver', corner_radius= 7)
    bottom_frame = ctk.CTkFrame(config, width= 190, height= 114, border_width= 2, border_color= 'silver', corner_radius= 7)
    
    # Criação dos widgets da tela da janela config
    config_title_label = ctk.CTkLabel(title_frame, text= 'Configurações', font= ('Arial', 14, 'bold'), height= 12)
    
    # Criação dos widgets da tela do frame bottom
    theme_config_label = ctk.CTkLabel(bottom_frame, text= 'Tema:', font= ('verdana', 12))
    theme_config_cbb = ctk.CTkComboBox(bottom_frame, width= 85, height= 20, font= ('verdana', 12), state='readonly', values= theme_values)
    confirm_button = ctk.CTkButton(config, text= 'Confirmar', width= 25, height= 2, command= lambda: on_click_confirm(self, config, theme_config_cbb))
    cancel_button = ctk.CTkButton(config, text= 'Cancelar', width= 65, height= 2, command= lambda: config.destroy())
    
    # Seta o valor padrão do combobox
    theme_config_cbb.set(temas_dict[atual_theme])
    
    # Posicionamento dos frames
    title_frame.pack(expand= True, fill= 'both')
    bottom_frame.pack(expand= True, fill= 'both')
    
    # Posicionamento dos widgets
    config_title_label.place(relx= 0.5, rely= 0.5, anchor= 'center')
    
    # Posicionamento dos widgets da tela do frame bottom
    theme_config_label.place(x= 10, y= 6)
    theme_config_cbb.place(x= 53, y= 10)
    confirm_button.place(relx= 0.652, rely = 0.815)
    cancel_button.place(relx= 0.302, rely = 0.815)
    
    config.bind('<Escape>', lambda event: config.destroy()) # Liga a tecla de atalho Esc para fechar a janela
    config.bind('<F5>', lambda event: confirm_button.invoke()) # Liga a tecla de atalho F5 para confirmar a escolha do tema