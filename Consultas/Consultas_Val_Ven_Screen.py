def Val_Ven_Screen(self, Consulta_Screen):    
    import customtkinter as ctk
    from Consultas.Consultas_Val_Screen import Consultas_Val_Screen
    from Consultas.Consultas_Val_Ven_Func import ven_get, copy_val
    
    hub = Consultas_Val_Screen(Consulta_Screen, 'Valor das Vendas')
    
    val_ven_label = ctk.CTkLabel(hub, text= 'Valor das Vendas:', width= 20, height= 2, font= ('', 16))
    val_ven_text = ctk.CTkLabel(hub, text= ven_get(self), width= 20, height= 2, font= ('', 14))
    val_ven_button = ctk.CTkButton(hub, text= 'Copiar Valor', width= 15, height= 20, command= lambda: copy_val(val_ven_text))
    
    val_ven_label.place(relx= 0.5, y= 15, anchor= 'center')
    val_ven_text.place(relx= 0.5, y= 40, anchor= 'center')
    val_ven_button.place(relx= 0.5, y= 65, anchor= 'center')