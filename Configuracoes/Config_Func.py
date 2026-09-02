from customtkinter import set_appearance_mode
from Configuracoes.Config_Manager import get_config


def _theme_def(cbb_entry):
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


def _db_def(entry_widgets):
    config = get_config()
    user_db = entry_widgets[0].get()
    pass_db = entry_widgets[1].get()

    config.set("Credenciais", "user_db", user_db)
    config.set("Credenciais", "pass_db", pass_db)
    config.save()


def set_default_values(entry_widgets):
    config = get_config()
    user_db = config.get("Credenciais", "user_db", fallback="")
    pass_db = config.get("Credenciais", "pass_db", fallback="")

    entry_widgets[0].insert(0, user_db)
    entry_widgets[1].insert(0, pass_db)


def on_click_confirm(self, config, cbb_entry, entry_widgets):

    if cbb_entry.get() == self.color_theme:
        return
    else:
        _theme_def(cbb_entry)

    _db_def(entry_widgets)

    config.grab_release()  # Libera o foco da janela
    config.destroy()  # Fecha a janela
