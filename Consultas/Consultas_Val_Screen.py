from Interface_Tools.Container_Screen_Managment.Container_Manager import ContainerManager


def Consultas_Val_Screen(parent, title: str, parent_button, container_manager: ContainerManager):
    import customtkinter as ctk
    from Consultas.Generics_Functions.Gen_Funcs_Consulta import event_screen_close

    cm = container_manager

    hub = ctk.CTkToplevel(parent)
    hub.title(title)
    cm.posicionar_container(hub)
    hub.resizable(False, False)
    # hub.grab_set()
    hub.transient(parent)
    hub.focus_set()
    hub.bind("<Escape>", lambda e: event_screen_close(
        hub, e, parent_button, cm))
    hub.protocol("WM_DELETE_WINDOW", lambda: event_screen_close(
        hub, None, parent_button, cm))
    return hub
