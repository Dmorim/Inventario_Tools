import pyperclip

from Thread_Manager.Query_Operations import query_selector, query_executor


def prod_get(query: str = None, params=None):
    return query_executor(query_selector, query, params)[0][0]


def copy_val(val_ven_text, prefix: str = None):
    copy_text = val_ven_text.cget('text')
    pyperclip.copy(f"{prefix}{copy_text}" if prefix else copy_text)


def event_invoke_button(event, button):
    if button.cget('state') != 'disabled':
        button.invoke()


def event_screen_close(screen, event, button, container_manager):
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
