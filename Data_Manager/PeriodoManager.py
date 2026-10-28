from collections.abc import Callable

from Data_Manager.PeriodoInventario import PeriodoInventario

listener_periodo = Callable[[PeriodoInventario], None]


class PeriodoManager:
    def __init__(self, periodo: PeriodoInventario):
        self._periodo = periodo
        self._listeners: list[listener_periodo] = []

    def obter_periodo(self) -> PeriodoInventario:
        return self._periodo

    def atualizar_periodo(self, novo_periodo: PeriodoInventario):
        if novo_periodo == self._periodo:
            return  # Não há alteração no período, não notificar os listeners

        self._periodo = novo_periodo
        self._notificar_listeners()

    def adicionar_listener(self, listener: listener_periodo):
        if listener not in self._listeners:
            self._listeners.append(listener)

    def remover_listener(self, listener: listener_periodo):
        if listener in self._listeners:
            self._listeners.remove(listener)

    def _notificar_listeners(self):
        periodo = self._periodo

        for listener in tuple(self._listeners):
            listener(periodo)
