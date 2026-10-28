from Interface_Tools.Container_Screen_Managment.Container_Manager import ContainerManager
from Consultas.Generics_Functions.Gen_Funcs_Consulta import prod_get
from Consultas.Preco_Custo_Zerado.Consultas_ZCusto_List_Screen import List_Treeview_Screen
from Interface_Tools.Consulta_Screen.Consulta_Screen import criar_tela_consulta
from Queries.Consulta_Queries import QUERY_PRECO_CUSTO_ZERADO


def Prod_ZCusto_Screen(Consulta_Screen, consulta_button, container_manager: ContainerManager):
    query = QUERY_PRECO_CUSTO_ZERADO
    return criar_tela_consulta(Consulta_Screen, consulta_button, container_manager,
                               titulo="Produtos com Preço de Custo zerado",
                               label_texto="Produtos com Preço de Custo zerado:",
                               get_func=prod_get,
                               query=query,
                               prefix_copy=None,
                               on_listar=lambda: List_Treeview_Screen(
                                   Consulta_Screen),
                               texto_inicial="Gerando Quantidade...",
                               )
