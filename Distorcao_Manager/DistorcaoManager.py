from Distorcao_Manager.DistorcaoInventario import DistorcaoInventario


class DistorcaoManager:
    _instancia = None

    def __new__(cls, distorcao: DistorcaoInventario):
        if cls._instancia is None:
            cls._instancia = super().__new__(cls)
        return cls._instancia

    def __init__(self, distorcao: DistorcaoInventario):
        if getattr(self, "_inicializado", False):
            return

        self._distorcoes: list[DistorcaoInventario] = [distorcao]
        self._inicializado = True

    def obter_distorcao(self) -> list:
        return [distorcao.campos_em_lista for distorcao in self._distorcoes]

    def atualizar_distorcao(self, nova_distorcao: DistorcaoInventario):
        if nova_distorcao != self._distorcoes[-1]:
            self._distorcoes.append(nova_distorcao)
