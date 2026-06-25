def prod_get(query_input: str):
    # Importa as funções para executar a query no banco de dados
    from Thread_Manager.Query_Operations import query_selector, query_executor

    # Retorna o valor obtido
    return query_executor(query_selector, query_input)[0][0]


def copy_val(val_ven_text):
    # Mesmo funcionamento explicado em Consultas/Consultas_Val_Ven_Func.py
    import pyperclip
    copy_text = val_ven_text.cget('text')
    pyperclip.copy(copy_text)


def event_button_consulta(self, event):
    # Função que simula um click no botão de consulta
    # Args:
    # self: Instância da classe que chama a função
    # event: Evento que chama a função

    if self.consulta.cget('state') != 'disabled':
        self.consulta.invoke()


def event_button_comando(self, event):
    # Função que simula um click no botão de comando
    # Args:
    # self: Instância da classe que chama a função
    # event: Evento que chama a função

    if self.comando.cget('state') != 'disabled':
        self.comando.invoke()


def event_screen_close(screen, event, button):
    # Função que simula o fechamento da tela
    # Args:
    # screen: Instância da tela que chama a função
    # event: Evento que chama a função
    button.configure(state='normal')
    screen.destroy()
