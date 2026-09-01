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
        logger.info(
            'Consulta genérica concluída. query=%s | valor_encontrado=%s', nome_query, valor is not None)
        return valor
    except Exception:
        logger.exception(
            'Erro ao consultar valor genérico. query=%s | params=%s', nome_query, params)
        raise


def copy_val(val_ven_text, prefix: str = None):
    copy_text = val_ven_text.cget('text')
    texto_final = f"{prefix}{copy_text}" if prefix else copy_text
    logger.info(
        'Copiando valor para a área de transferência. prefix=%s | valor=%s', prefix, copy_text)
    pyperclip.copy(texto_final)


def event_invoke_button(event, button):
    if button.cget('state') != 'disabled':
        logger.info('Evento de clique disparado para botão: %s',
                    getattr(button, 'cget', lambda *_: 'button')('text'))
        button.invoke()


def event_screen_close(screen, event, button, container_manager):
    logger.info('Fechando container de consulta: %s',
                getattr(screen, 'title', lambda: screen))
    button.configure(state='normal')
    container_manager.remover_container(screen)
    screen.destroy()


def banco_codigo_valueform(val):
    logger.debug('Formatando valor monetário: %s', val)
    val = "{:,.2f}".format(val)
    prs = val.split('.')
    pri = prs[0]
    prd = prs[1]
    pri = pri.replace(",", ".")
    val = pri + ',' + prd
    return val
