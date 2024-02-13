def Consultas_Val_Screen(parent, title: str):
    import customtkinter as ctk
    
    hub = ctk.CTkToplevel(parent)
    hub.title(title)
    hub.geometry("250x80+210+160")
    hub.resizable(False, False)
    hub.grab_set()
    hub.focus_set()
    return hub