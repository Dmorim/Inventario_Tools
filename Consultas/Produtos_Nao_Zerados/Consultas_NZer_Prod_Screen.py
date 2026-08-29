from Interface_Tools.Container_Screen_Managment.Container_Manager import ContainerManager
from Interface_Tools.Consulta_Screen.Consulta_Screen import criar_tela_consulta
from Consultas.Generics_Functions.Gen_Funcs_Consulta import prod_get
from Consultas.Produtos_Nao_Zerados.Consultas_NZer_List_Screen import List_Treeview_Screen


def Prod_NZer_Screen(Consulta_Screen, consulta_button, container_manager: ContainerManager):
    return criar_tela_consulta(Consulta_Screen, consulta_button, container_manager,
                               titulo="Produtos Não Zerados",
                               label_texto="Produtos Não Zerados:",
                               get_func=prod_get,
                               prefix_copy=None,
                               on_listar=lambda: List_Treeview_Screen(
                                   Consulta_Screen),
                               texto_inicial="Gerando Quantidade...",
                               )
