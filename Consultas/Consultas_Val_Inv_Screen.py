def hub_val_inv(Consulta_Screen):
    import customtkinter as ctk
    from Consultas.Consultas_Val_Inv_Func import inv_get, copy_val
    from Consultas.Consultas_Val_Screen import Consultas_Val_Screen
    
    hub = Consultas_Val_Screen(Consulta_Screen, 'Valor do Inventário')
    
    val_inv_label = ctk.CTkLabel(hub, text= 'Valor do Inventário:', width= 20, height= 2, font= ('', 16))
    val_inv_text = ctk.CTkLabel(hub, text= inv_get(), width= 20, height= 2, font= ('', 14))
    val_inv_button = ctk.CTkButton(hub, text= 'Copiar Valor', width= 15, height= 20, command= lambda: copy_val(val_inv_text))
    
    val_inv_label.place(relx= 0.5, y= 15, anchor= 'center')
    val_inv_text.place(relx= 0.5, y= 40, anchor= 'center')
    val_inv_button.place(relx= 0.5, y= 65, anchor= 'center')