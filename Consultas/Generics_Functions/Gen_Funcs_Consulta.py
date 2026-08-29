def prod_get(query_input: str, params=None):
    # Importa as funções para executar a query no banco de dados
    from Thread_Manager.Query_Operations import query_selector, query_executor

    # Retorna o valor obtido
    return query_executor(query_selector, query_input, params)[0][0]


def copy_val(val_ven_text, prefix: str = None):
    # Mesmo funcionamento explicado em Consultas/Consultas_Val_Ven_Func.py
    import pyperclip
    copy_text = val_ven_text.cget('text')
    pyperclip.copy(f"{prefix}{copy_text}" if prefix else copy_text)


def event_invoke_button(event, button):
    # Função que simula um click no botão de consulta
    # Args:
    # self: Instância da classe que chama a função
    # event: Evento que chama a função
    # button: Botão que chama a função

    if button.cget('state') != 'disabled':
        button.invoke()


def event_screen_close(screen, event, button, container_manager):
    # Função que simula o fechamento da tela
    # Args:
    # screen: Instância da tela que chama a função
    # event: Evento que chama a função
    # button: Botão que chama a função
    # container_manager: Gerenciador de containers

    button.configure(state='normal')
    container_manager.remover_container(screen)
    screen.destroy()


def banco_codigo_valueform(val):
    val = "{:,.2f}".format(val)
    prs = val.split('.')
    pri = prs[0]
    prd = prs[1]
    pri = pri.replace(",", ".")
    val = pri + ',' + prd
    return val
