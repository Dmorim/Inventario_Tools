from Distorcao_Manager.DistorcaoInventario import DistorcaoInventario


class DistorcaoManager:

    def __init__(self, distorcao: DistorcaoInventario):
        self._distorcao = distorcao

    def obter_distorcao(self) -> DistorcaoInventario:
        return self._distorcao

    def atualizar_distorcao(
        self,
        nova_distorcao: DistorcaoInventario
    ) -> None:
        self._distorcao = nova_distorcao

    def possui_itens(self) -> bool:
        return self._distorcao.tamanho > 0
