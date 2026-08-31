from Interface_Tools.Container_Screen_Managment.Container_Manager import ContainerManager
from Interface_Tools.Consulta_Screen.Consulta_Screen import criar_tela_consulta
from Consultas.Generics_Functions.Gen_Funcs_Consulta import prod_get
from Consultas.Controla_Estoque.Consultas_Contr_Estq_List import List_Treeview_Screen
from Queries.Consulta_Queries import QUERY_CONTROLA_ESTOQUE_DESATIVADO


def Contr_Estq_Screen(self, Consulta_Screen, consulta_button, container_manager: ContainerManager):
    query = QUERY_CONTROLA_ESTOQUE_DESATIVADO
    params = (self.data_banco_inicial, self.data_banco_final)
    return criar_tela_consulta(Consulta_Screen, consulta_button, container_manager,
                               titulo="Produtos Controla Estoque",
                               label_texto="Produtos com Controla Estoque = N:",
                               get_func=prod_get,
                               query=query,
                               params=params,
                               prefix_copy=None,
                               on_listar=lambda: List_Treeview_Screen(
                                   self, Consulta_Screen),
                               texto_inicial="Gerando Quantidade...",
                               )
