import threading
import queue
from tkinter import messagebox, TclError

from Outros.Logger.Get_Logger import get_logger

logger = get_logger(__name__)


def _safe_schedule_ui(master, func, *args, **kwargs):
    """Agenda uma ação da UI na thread principal apenas se a janela ainda existir."""
    if master is None:
        logger.debug('Não foi possível agendar callback na UI: master=None.')
        return False

    try:
        if not master.winfo_exists():
            logger.debug('Tentativa de agendar callback em UI inexistente.')
            return False
    except (AttributeError, TclError):
        logger.debug('Master da UI inválido ao tentar agendar callback.')
        return False

    def _executar():
        try:
            if master is None:
                return
            try:
                if not master.winfo_exists():
                    return
            except (AttributeError, TclError):
                return
            func(*args, **kwargs)
        except Exception:
            logger.exception('Erro ao executar callback agendado na UI.')

    try:
        master.after(0, _executar)
        return True
    except (TclError, AttributeError):
        logger.debug('Falha ao agendar callback na thread principal.')
        return False


def thread_execução(master, func, callback, on_erro=None, *args, **kwargs):
    """
    Função para executar uma função em uma thread separada e chamar um callback com o resultado.
    """

    fila = queue.Queue()
    cancelado = {'flag': False}

    def thread_target(*args, **kwargs):
        try:
            if cancelado['flag']:
                return
            if master is not None:
                try:
                    if not master.winfo_exists():
                        return
                except (AttributeError, TclError):
                    pass
            result = func(*args, **kwargs)
            if cancelado['flag']:
                return
            fila.put((True, result))
            logger.debug('Thread %s concluída com sucesso.',
                         getattr(func, '__name__', repr(func)))
        except Exception as exc:
            if cancelado['flag']:
                return
            logger.exception('Thread %s falhou.', getattr(
                func, '__name__', repr(func)))
            try:
                fila.put((False, exc))
            except Exception:
                pass

    try:
        t = threading.Thread(target=thread_target, args=args,
                             kwargs=kwargs, daemon=True)
        t.start()
    except Exception:
        logger.exception('Falha ao iniciar thread de execução.')
        return

    def check_thread():
        if cancelado['flag']:
            return
        if master is not None:
            try:
                if not master.winfo_exists():
                    cancelado['flag'] = True
                    return
            except (AttributeError, TclError):
                cancelado['flag'] = True
                return

        try:
            success, result = fila.get_nowait()
        except queue.Empty:
            if master is not None:
                try:
                    master.after(75, check_thread)
                    return
                except (TclError, AttributeError):
                    cancelado['flag'] = True
                    return
            cancelado['flag'] = True
            return

        if cancelado['flag']:
            return
        if success:
            if callable(callback):
                _safe_schedule_ui(master, callback, result)
        elif on_erro:
            _safe_schedule_ui(master, on_erro, result)
        else:
            try:
                _safe_schedule_ui(master, messagebox.showerror, "Erro",
                                  f"Ocorreu um erro: {result}")
            except Exception:
                logger.exception('Erro ao exibir mensagem de erro.')

    try:
        check_thread()
    except Exception:
        logger.exception('Falha ao iniciar verificação de thread.')


def atualizar_ui_main(master, func, *args, **kwargs):
    return _safe_schedule_ui(master, func, *args, **kwargs)
