def theme_def(cbb_entry):
    from customtkinter import set_appearance_mode
    from Banco_de_Dados.Banco_de_Dados_Func import salvar_diretorio
    
    theme = cbb_entry.get()
    if theme == 'Claro':
        salvar_diretorio('Configurações', 'Cor_do_tema', 'Light')
        set_appearance_mode("Light")
        
    
    elif theme == 'Escuro':
        salvar_diretorio('Configurações', 'Cor_do_tema', 'Dark')
        set_appearance_mode("Dark")
    
    elif theme == 'Sistema':
        salvar_diretorio('Configurações', 'Cor_do_tema', 'System')
        set_appearance_mode("System")

def on_click_confirm(self, config, cbb_entry):
    
    if cbb_entry.get() == self.color_theme:
        return
    else:
        theme_def(cbb_entry)
    
    config.grab_release()
    config.destroy()
       
