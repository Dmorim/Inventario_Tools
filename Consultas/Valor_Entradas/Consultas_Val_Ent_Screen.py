from Consultas.Valor_Entradas.Consultas_Val_Ent_Func import ent_get
from Interface_Tools.Container_Screen_Managment.Container_Manager import ContainerManager
from Interface_Tools.Consulta_Screen.Consulta_Screen import criar_tela_consulta


def Val_Ent_Screen(self, Consulta_Screen, consulta_button, container_manager: ContainerManager):
    return criar_tela_consulta(Consulta_Screen, consulta_button, container_manager,
                               titulo="Valor das Compras",
                               label_texto="Valor das Compras:",
                               get_func=ent_get,
                               self=self,
                               prefix_copy="R$ ",
                               on_listar=None,
                               texto_inicial="Gerando Valor...",
                               )
