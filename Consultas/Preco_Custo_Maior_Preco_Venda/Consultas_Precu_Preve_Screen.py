from Interface_Tools.Container_Screen_Managment.Container_Manager import ContainerManager
from Interface_Tools.Consulta_Screen.Consulta_Screen import criar_tela_consulta
import customtkinter as ctk
from Consultas.Consultas_Val_Screen import Consultas_Val_Screen
from Consultas.Generics_Functions.Gen_Funcs_Consulta import prod_get, copy_val
from Consultas.Preco_Custo_Maior_Preco_Venda.Consultas_Precu_Preve_List import List_Treeview_Screen
from Thread_Manager.Thread_Executor import thread_execução


def Precu_Preve_Screen(Consulta_Screen, consulta_button, container_manager: ContainerManager):
    query = 'select count (*) from in01pro where precu > preve and saldo > 0 and preve > 0'
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
