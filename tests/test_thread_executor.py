import threading
import time
from tkinter import TclError

from Thread_Manager import Thread_Executor


class MasterFake:
    def __init__(self, existe=True, falhar_after=False):
        self.existe = existe
        self.falhar_after = falhar_after
        self.agendados = []
        self.intervalos = []

    def winfo_exists(self):
        return self.existe

    def after(self, ms, func):
        if self.falhar_after:
            raise TclError('janela destruída')
        self.intervalos.append(ms)
        self.agendados.append(func)


def _aguardar(master, condicao, limite=2.0):
    prazo = time.monotonic() + limite
    while time.monotonic() < prazo:
        if condicao():
            return True
        if master.agendados:
            master.agendados.pop(0)()
        else:
            time.sleep(0.005)
    return condicao()


def test_safe_schedule_ui_retorna_false_sem_master():
    assert Thread_Executor._safe_schedule_ui(None, lambda: None) is False


def test_safe_schedule_ui_nao_agenda_para_janela_inexistente():
    master = MasterFake(existe=False)
    chamadas = []

    assert Thread_Executor._safe_schedule_ui(master, chamadas.append, 1) is False
    assert master.agendados == []
    assert chamadas == []


def test_safe_schedule_ui_retorna_false_quando_after_falha():
    master = MasterFake(falhar_after=True)

    assert Thread_Executor._safe_schedule_ui(master, lambda: None) is False


def test_safe_schedule_ui_executa_callback_agendado():
    master = MasterFake()
    chamadas = []

    assert Thread_Executor._safe_schedule_ui(master, chamadas.append, 7) is True
    master.agendados.pop(0)()

    assert chamadas == [7]


def test_safe_schedule_ui_revalida_janela_antes_de_executar():
    master = MasterFake()
    chamadas = []

    Thread_Executor._safe_schedule_ui(master, chamadas.append, 'ok')
    master.existe = False
    master.agendados.pop(0)()

    assert chamadas == []


def test_safe_schedule_ui_nao_propaga_erro_do_callback():
    master = MasterFake()

    def explodir(_):
        raise RuntimeError('falha no callback')

    Thread_Executor._safe_schedule_ui(master, explodir, 1)
    master.agendados.pop(0)()


def test_thread_execucao_entrega_resultado_ao_callback():
    master = MasterFake()
    resultados = []

    Thread_Executor.thread_execução(master, lambda: 42, resultados.append)

    assert _aguardar(master, lambda: resultados == [42]) is True


def test_thread_execucao_usa_on_erro_quando_funcao_falha():
    master = MasterFake()
    resultados = []
    erros = []

    def falhar():
        raise ValueError('falhou')

    Thread_Executor.thread_execução(
        master, falhar, resultados.append, erros.append)

    assert _aguardar(master, lambda: len(erros) == 1) is True
    assert isinstance(erros[0], ValueError)
    assert resultados == []


def test_thread_execucao_nao_entrega_resultado_apos_janela_destruida():
    master = MasterFake()
    resultados = []
    iniciou = threading.Event()
    liberar = threading.Event()

    def demorada():
        iniciou.set()
        liberar.wait(2)
        return 'tarde'

    Thread_Executor.thread_execução(master, demorada, resultados.append)
    assert iniciou.wait(2) is True
    master.existe = False
    liberar.set()
    _aguardar(master, lambda: False, limite=0.3)

    assert resultados == []


def test_thread_execucao_nao_executa_funcao_com_janela_inexistente():
    master = MasterFake(existe=False)
    executou = []

    Thread_Executor.thread_execução(
        master, lambda: executou.append(1), lambda _: None)
    time.sleep(0.05)

    assert executou == []
