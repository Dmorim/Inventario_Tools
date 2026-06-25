import threading
import queue
from tkinter import messagebox


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
        except Exception as e:
            fila.put((False, e))

    threading.Thread(target=thread_target, args=args, kwargs=kwargs, daemon=True).start()

    def check_thread():
        try:
            success, result = fila.get_nowait()
        except queue.Empty:
            master.after(100, check_thread)
            return

        if success:
            callback(result)
        elif on_erro:
            on_erro(result)
        else:
            messagebox.showerror("Erro", f"Ocorreu um erro: {result}")

    check_thread()
