from customtkinter import set_appearance_mode
from Configuracoes.Config_Manager import get_config


def theme_def(cbb_entry):
    tema_dict = {
        "Claro": "light",
        "Escuro": "dark",
        "Sistema": "system"
    }

    config = get_config()  # Obtém o objeto de configuração
    # Define o valor do tema no arquivo config.ini
    config.set("Tema", "cor_do_tema", tema_dict.get(cbb_entry.get(), "system"))
    config.save()  # Salva as alterações no arquivo config.ini
    # Define o tema do sistema
    set_appearance_mode(config.get("Tema", "cor_do_tema", fallback="System"))


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
