import customtkinter as ctk

from Interface_Tools.Container_Screen_Managment.Container_Manager import ContainerManager
from Consultas.Generics_Functions.Gen_Funcs_Consulta import event_screen_close


def Consultas_Val_Screen(parent, title: str, parent_button, container_manager: ContainerManager):
    cm = container_manager
    hub = ctk.CTkToplevel(parent)
    hub.title(title)
    __posicionar_container(hub, cm)
    hub.resizable(False, False)
    hub.transient(parent)
    hub.focus_set()
    hub.bind("<Escape>", lambda e: event_screen_close(
        hub, e, parent_button, cm))
    hub.protocol("WM_DELETE_WINDOW", lambda: event_screen_close(
        hub, None, parent_button, cm))
    return hub


def __posicionar_container(hub, cm):
    hub.update_idletasks()
    try:
        cm.posicionar_container(hub)
    except RuntimeError:
        pass
