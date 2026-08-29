from Consultas.Valor_Inventario.Consultas_Val_Inv_Func import inv_get
from Interface_Tools.Consulta_Screen.Consulta_Screen import criar_tela_consulta
from Interface_Tools.Container_Screen_Managment.Container_Manager import ContainerManager


def hub_val_inv(Consulta_Screen, consulta_button, container_manager: ContainerManager):
    return criar_tela_consulta(Consulta_Screen, consulta_button, container_manager,
                               titulo="Valor de Inventário",
                               label_texto="Valor de Inventário:",
                               get_func=inv_get,
                               prefix_copy="R$ ",
                               on_listar=None,
                               texto_inicial="Gerando Valor...",
                               )
