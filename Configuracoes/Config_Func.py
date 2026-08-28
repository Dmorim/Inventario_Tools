def theme_def(cbb_entry):
    # Função chamada para definir o tema do sistema e salvar o valor no arquivo config.ini
    # Args:
    # cbb_entry: combobox do tema

    # Importa a função set_appearance_mode do customtkinter
    from customtkinter import set_appearance_mode
    # Importa a função get_config do arquivo Config_Manager
    from Configuracoes.Config_Manager import get_config
    tema_dict = {
        "Claro": "light",
        "Escuro": "dark",
        "Sistema": "system"
    }

    config = get_config()  # Obtém o objeto de configuração
    # Define o valor do tema no arquivo config.ini
    config.set("Tema", "Cor_do_tema", tema_dict.get(cbb_entry.get(), "system"))
    config.save()  # Salva as alterações no arquivo config.ini
    # Define o tema do sistema
    set_appearance_mode(config.get("Tema", "Cor_do_tema", fallback="System"))


def on_click_confirm(self, config, cbb_entry):
    # Função chamada ao apertar o botão de confirmar, se o tema escolhido for diferente do atual,executa a função theme_def e fecha a janela
    # Args:
    # self: objeto da classe
    # config: janela do tkinter
    # cbb_entry: combobox do tema

    if cbb_entry.get() == self.color_theme:  # Verifica se o tema escolhido é igual ao atual
        return
    else:
        theme_def(cbb_entry)  # Executa a função theme_def caso não seja

    config.grab_release()  # Libera o foco da janela
    config.destroy()  # Fecha a janela
