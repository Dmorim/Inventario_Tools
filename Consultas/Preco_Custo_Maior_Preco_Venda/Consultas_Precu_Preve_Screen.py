from Interface_Tools.Container_Screen_Managment.Container_Manager import ContainerManager
from Interface_Tools.Consulta_Screen.Consulta_Screen import criar_tela_consulta
from Consultas.Generics_Functions.Gen_Funcs_Consulta import prod_get
from Consultas.Preco_Custo_Maior_Preco_Venda.Consultas_Precu_Preve_List import List_Treeview_Screen
from Queries.Consulta_Queries import QUERY_PRECO_CUSTO_MAIOR_VENDA


def Precu_Preve_Screen(Consulta_Screen, consulta_button, container_manager: ContainerManager):
    query = QUERY_PRECO_CUSTO_MAIOR_VENDA
    return criar_tela_consulta(Consulta_Screen, consulta_button, container_manager,
                               titulo="Produtos com Preço de Custo maior que o de venda",
                               label_texto="Produtos em que Precu > Preve:",
                               get_func=prod_get,
                               query=query,
                               prefix_copy=None,
                               on_listar=lambda: List_Treeview_Screen(
                                   Consulta_Screen),
                               texto_inicial="Gerando Quantidade...",
                               )
