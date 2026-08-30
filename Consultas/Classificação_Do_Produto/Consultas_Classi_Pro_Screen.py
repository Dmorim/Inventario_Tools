from Interface_Tools.Container_Screen_Managment.Container_Manager import ContainerManager
from Interface_Tools.Consulta_Screen.Consulta_Screen import criar_tela_consulta
import customtkinter as ctk
from Consultas.Consultas_Val_Screen import Consultas_Val_Screen
from Consultas.Generics_Functions.Gen_Funcs_Consulta import prod_get, copy_val
from Consultas.Classificação_Do_Produto.Consultas_Classi_Pro_List import List_Treeview_Screen
from Thread_Manager.Thread_Executor import thread_execução


def Classi_Pro_Screen(Consulta_Screen, consulta_button, container_manager: ContainerManager):
    query = "select count (*) from in01pro where classificacao_produto is null or classificacao_produto = ''"
    return criar_tela_consulta(Consulta_Screen, consulta_button, container_manager,
                               titulo="Produtos sem Classificação do Produto",
                               label_texto="Produtos sem Classificação do Produto:",
                               get_func=prod_get,
                               query=query,
                               prefix_copy=None,
                               on_listar=lambda: List_Treeview_Screen(
                                   Consulta_Screen),
                               texto_inicial="Gerando Quantidade...",
                               )
