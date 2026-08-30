from Interface_Tools.Container_Screen_Managment.Container_Manager import ContainerManager
from Consultas.Generics_Functions.Gen_Funcs_Consulta import prod_get
from Consultas.Preco_Custo_Zerado.Consultas_ZCusto_List_Screen import List_Treeview_Screen
from Interface_Tools.Consulta_Screen.Consulta_Screen import criar_tela_consulta


def Prod_ZCusto_Screen(Consulta_Screen, consulta_button, container_manager: ContainerManager):
    query = 'select count (*) from in01pro where (precu = 0 or (precu is null) or (precu < 0)) and preve > 0 and saldo > 0'
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
