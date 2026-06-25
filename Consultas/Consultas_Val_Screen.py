def Consultas_Val_Screen(parent, title: str, parent_button):
    import customtkinter as ctk
    from Consultas.Generics_Functions.Gen_Funcs_Consulta import event_screen_close

    hub = ctk.CTkToplevel(parent)
    hub.title(title)
    hub.geometry("250x80+210+160")
    hub.resizable(False, False)
    # hub.grab_set()
    hub.transient(parent)
    hub.focus_set()
    hub.bind("<Escape>", lambda e: event_screen_close(hub, e, parent_button))
    hub.protocol("WM_DELETE_WINDOW", lambda: event_screen_close(
        hub, None, parent_button))
    return hub
