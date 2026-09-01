import threading
import queue
from tkinter import messagebox, TclError


def _safe_schedule_ui(master, func, *args):
    """Agenda uma ação da UI na thread principal apenas se a janela ainda existir."""
    if master is None:
        return False

    try:
        if not master.winfo_exists():
            return False
    except (AttributeError, TclError):
        return False

    try:
        master.after(0, lambda: func(*args))
        return True
    except TclError:
        return False


def thread_execução(master, func, callback, on_erro=None, *args, **kwargs):
    """
    Função para executar uma função em uma thread separada e chamar um callback com o resultado.

    Args:
        master: A janela principal do Tkinter.
        func: A função a ser executada na thread.
        callback: A função a ser chamada com o resultado da execução de func.
        *args: Argumentos posicionais para func.
        **kwargs: Argumentos nomeados para func.
    """

    fila = queue.Queue()

    def thread_target(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            fila.put((True, result))
        except Exception as exc:
            fila.put((False, exc))

    threading.Thread(target=thread_target, args=args,
                     kwargs=kwargs, daemon=True).start()

    def check_thread():
        if master is not None:
            try:
                if not master.winfo_exists():
                    return
            except TclError:
                return

        try:
            success, result = fila.get_nowait()
        except queue.Empty:
            if master is not None:
                try:
                    master.after(100, check_thread)
                except TclError:
                    pass
            return

        if success:
            if callable(callback):
                _safe_schedule_ui(master, callback, result)
        elif on_erro:
            _safe_schedule_ui(master, on_erro, result)
        else:
            _safe_schedule_ui(master, messagebox.showerror, "Erro",
                              f"Ocorreu um erro: {result}")

    check_thread()


def atualizar_ui_main(master, func, *args):
    return _safe_schedule_ui(master, func, *args)
