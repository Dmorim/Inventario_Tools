def Quant_Maior_Screen(Consulta_Screen):    
    import customtkinter as ctk
    from Consultas_Val_Screen import Consultas_Val_Screen
    from Gen_Funcs_Consulta import prod_get, copy_val
    from Consultas_Quant_Maior_List import List_Treeview_Screen
    
    hub = Consultas_Val_Screen(Consulta_Screen, 'Produtos com Quantidade Maior que 999999')
    
    val_ven_label = ctk.CTkLabel(hub, text= 'Produtos com Quant > 999999', width= 20, height= 2, font= ('', 15))
    val_ven_text = ctk.CTkLabel(hub, text= prod_get("Select count (*) from in01lan where quant > 999999 and dtpro between '01.01.2023' and '31.12.2023'"), width= 20, height= 2, font= ('', 14))
    val_ven_button = ctk.CTkButton(hub, text= 'Copiar Valor', width= 15, height= 20, command= lambda: copy_val(val_ven_text))
    listagem_buttn = ctk.CTkButton(hub, text= 'Listar Produtos', width= 15, height= 20, command= lambda: List_Treeview_Screen(hub))
    
    val_ven_label.place(relx= 0.5, y= 15, anchor= 'center')
    val_ven_text.place(relx= 0.5, y= 40, anchor= 'center')
    val_ven_button.place(relx= 0.8, y= 65, anchor= 'center')
    listagem_buttn.place(relx= 0.24, y= 65, anchor= 'center')