import pyperclip

from Outros.Logger.Get_Logger import get_logger
from Thread_Manager.Query_Operations import query_selector, query_executor, _nome_query

logger = get_logger(__name__)


def prod_get(query: str = None, params=None):
    nome_query = _nome_query(query)
    logger.info('Consultando valor genérico. query=%s | params=%s',
                nome_query, params)
    try:
        result = query_executor(query_selector, query, params)
        valor = result[0][0] if result else None
        return valor
    except Exception:
        logger.exception(
            'Erro ao consultar valor genérico. query=%s | params=%s', nome_query, params)
        raise


def copy_val(val_ven_text, prefix: str = None):
    copy_text = val_ven_text.cget('text')
    logger.info('Copiando valor para a área de transferência. prefix=%s | valor=%s',
                prefix, copy_text)
    texto_final = f"{prefix}{copy_text}" if prefix else copy_text
    pyperclip.copy(texto_final)


def event_invoke_button(event, button):
    if button.cget('state') != 'disabled':
        nome_botao = getattr(button, 'cget', lambda *_: 'button')('text')
        logger.info('Invocando botão: %s', nome_botao)
        button.invoke()


def event_screen_close(screen, event, button, container_manager):
    nome_tela = getattr(screen, 'title', lambda: screen)()
    logger.info('Fechando container de consulta: %s', nome_tela)
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
