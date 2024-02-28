def config_screen(self, parent):
    import customtkinter as ctk
    from Configuracoes.Config_Func import on_click_confirm
    
    config = ctk.CTkToplevel(parent)
    config.title('Manutenção')
    config.geometry('190x140+320+110')
    config.focus_set()
    config.transient(parent)
    config.grab_set()
    
    theme_values = ['Claro', 'Escuro', 'Sistema']
    atual_theme = ctk.get_appearance_mode()
    temas_dict = {'Light': 'Claro', 'Dark': 'Escuro', 'System': 'Sistema'}
    
    title_frame = ctk.CTkFrame(config, width= 190, height= 25, border_width= 2, border_color= 'silver', corner_radius= 7)
    bottom_frame = ctk.CTkFrame(config, width= 190, height= 114, border_width= 2, border_color= 'silver', corner_radius= 7)
    
    config_title_label = ctk.CTkLabel(title_frame, text= 'Configurações', font= ('Arial', 14, 'bold'), height= 12)
    
    theme_config_label = ctk.CTkLabel(bottom_frame, text= 'Tema:', font= ('verdana', 12))
    theme_config_cbb = ctk.CTkComboBox(bottom_frame, width= 85, height= 20, font= ('verdana', 12), state='readonly', values= theme_values)
    confirm_button = ctk.CTkButton(config, text= 'Confirmar', width= 25, height= 2, command= lambda: on_click_confirm(self, config, theme_config_cbb))
    cancel_button = ctk.CTkButton(config, text= 'Cancelar', width= 65, height= 2, command= lambda: config.destroy())
    
    theme_config_cbb.set(temas_dict[atual_theme])
    
    title_frame.pack(expand= True, fill= 'both')
    bottom_frame.pack(expand= True, fill= 'both')
    
    config_title_label.place(relx= 0.5, rely= 0.5, anchor= 'center')
    
    theme_config_label.place(x= 10, y= 6)
    theme_config_cbb.place(x= 53, y= 10)
    confirm_button.place(relx= 0.652, rely = 0.815)
    cancel_button.place(relx= 0.302, rely = 0.815)