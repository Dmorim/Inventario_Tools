def theme_def(cbb_entry):
    # Função chamada para definir o tema do sistema e salvar o valor no arquivo config.ini
    # Args:
        # cbb_entry: combobox do tema
    
    from customtkinter import set_appearance_mode # Importa a função set_appearance_mode do customtkinter
    from Banco_de_Dados.Banco_de_Dados_Func import salvar_diretorio # Importa a função salvar_diretorio do Banco_de_Dados_Func
    
    theme = cbb_entry.get() # Obtem o valor do combobox
    if theme == 'Claro': # Se o valor for claro, define o tema como claro
        salvar_diretorio('Configurações', 'Cor_do_tema', 'Light') # Salva o valor no arquivo config.ini
        set_appearance_mode("Light")
        
    elif theme == 'Escuro': # Se o valor for escuro, define o tema como escuro
        salvar_diretorio('Configurações', 'Cor_do_tema', 'Dark') # Salva o valor no arquivo config.ini
        set_appearance_mode("Dark")
    
    elif theme == 'Sistema': # Se o valor for sistema, define o tema como sistema
        salvar_diretorio('Configurações', 'Cor_do_tema', 'System') # Salva o valor no arquivo config.ini
        set_appearance_mode("System")

def on_click_confirm(self, config, cbb_entry):
    # Função chamada ao apertar o botão de confirmar, se o tema escolhido for diferente do atual,executa a função theme_def e fecha a janela
    # Args:
        # self: objeto da classe
        # config: janela do tkinter
        # cbb_entry: combobox do tema
    
    if cbb_entry.get() == self.color_theme: # Verifica se o tema escolhido é igual ao atual
        return
    else:
        theme_def(cbb_entry) # Executa a função theme_def caso não seja
    
    config.grab_release() # Libera o foco da janela
    config.destroy() # Fecha a janela
       
