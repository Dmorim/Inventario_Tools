from Consultas.Valor_Vendas.Consultas_Val_Ven_Func import ven_get
from Interface_Tools.Consulta_Screen.Consulta_Screen import criar_tela_consulta
from Interface_Tools.Container_Screen_Managment.Container_Manager import ContainerManager


def Val_Ven_Screen(self, Consulta_Screen, consulta_button, container_manager: ContainerManager):
    return criar_tela_consulta(Consulta_Screen, consulta_button, container_manager,
                               titulo="Valor de Vendas",
                               label_texto="Valor de Vendas:",
                               get_func=ven_get,
                               self=self,
                               prefix_copy="R$ ",
                               on_listar=None,
                               texto_inicial="Gerando Valor...",
                               )
