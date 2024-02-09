def Consultas_Val_Screen(parent):
    import customtkinter as ctk
    
    hub = ctk.CTkToplevel(parent)
    hub.title("Valor do Inventário")
    hub.geometry("250x80")
    hub.resizable(False, False)
    hub.grab_set()
    hub.focus_set()
    return hub