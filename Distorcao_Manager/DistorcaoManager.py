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

        self._distorcao = distorcao
        self._inicializado = True

    def obter_distorcao(self) -> DistorcaoInventario:
        return self._distorcao

    def atualizar_distorcao(
        self,
        nova_distorcao: DistorcaoInventario
    ) -> None:
        self._distorcao = nova_distorcao

    def possui_itens(self) -> bool:
        return self._distorcao.tamanho > 0
