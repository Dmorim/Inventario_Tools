from Interface_Tools.Container_Screen_Managment.Container_Manager import ContainerManager
from Interface_Tools.Consulta_Screen.Consulta_Screen import criar_tela_consulta
from Consultas.Generics_Functions.Gen_Funcs_Consulta import prod_get
from Consultas.Quantidade_Exorbitante.Consultas_Quant_Maior_List import List_Treeview_Screen


def Quant_Maior_Screen(self, Consulta_Screen, consulta_button, container_manager: ContainerManager):
    query = f"Select count (*) from in01lan where quant > 999999 and dtpro between ? and ?"
    params = (self.data_banco_inicial, self.data_banco_final)
    return criar_tela_consulta(Consulta_Screen, consulta_button, container_manager,
                               titulo="Produtos com Quantidade Maior que 999999",
                               label_texto="Produtos com Quant > 999999:",
                               get_func=prod_get,
                               query=query,
                               params=params,
                               prefix_copy=None,
                               on_listar=lambda: List_Treeview_Screen(
                                   self, Consulta_Screen),
                               texto_inicial="Gerando Quantidade...",
                               )
