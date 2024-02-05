def Interface_Banco(self, root):
    import customtkinter as ctk
    Banco_Screen = ctk.CTkToplevel(root)
    Banco_Screen.title("Configurações de Banco de Dados")
    Banco_Screen.geometry("500x200")
    Banco_Screen.resizable(False, False)
    Banco_Screen.focus()
    Banco_Screen.grab_set()
    
    sel_banco_label = ctk.CTkLabel(Banco_Screen, text= 'Conexão com o Banco de Dados', width= 20, height= 2, font= ('', 14), text_color= 'silver')
    serv_label = ctk.CTkLabel(Banco_Screen, text= 'Servidor:', width= 20, height= 2, font= ('', 12))
    serv_entry = ctk.CTkEntry(Banco_Screen, width= 146, font= ('', 12))
    
    sel_banco_label.place(relx= 0.5, y= 9, anchor= 'center')
    serv_label.place(x= 2, y= 28)
    serv_entry.place(x= 2, y= 46)