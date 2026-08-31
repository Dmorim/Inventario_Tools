from Interface_Tools.Container_Screen_Managment.Container_Manager import ContainerManager
from Interface_Tools.Consulta_Screen.Consulta_Screen import criar_tela_consulta
from Consultas.Generics_Functions.Gen_Funcs_Consulta import prod_get
from Consultas.Preco_Custo_Compra_Zerado.Consultas_Preve_Precu_Precom_List import List_Treeview_Screen
from Queries.Consulta_Queries import QUERY_PRECO_CUSTO_VENDA_COMPRA_ZERADOS


def Preve_Precu_Precom_Screen(Consulta_Screen, consulta_button, container_manager: ContainerManager):
    query = QUERY_PRECO_CUSTO_VENDA_COMPRA_ZERADOS
    return criar_tela_consulta(Consulta_Screen, consulta_button, container_manager,
                               titulo="Produtos com Preço de Custo, Venda e Compra zerados",
                               label_texto="Produtos em que Precu, Preve e Precom = 0:",
                               get_func=prod_get,
                               query=query,
                               prefix_copy=None,
                               on_listar=lambda: List_Treeview_Screen(
                                   Consulta_Screen),
                               texto_inicial="Gerando Quantidade...",
                               )
