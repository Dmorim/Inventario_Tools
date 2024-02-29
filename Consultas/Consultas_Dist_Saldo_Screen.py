def dist_saldo_screen(Consulta_Screen):
    import customtkinter as ctk
    from Consultas.Consultas_Val_Screen import Consultas_Val_Screen
    from Consultas.Gen_Funcs_Consulta import prod_get, copy_val
    from Consultas.Consultas_Dist_Saldo_List import List_Treeview_Screen
    
    hub = Consultas_Val_Screen(Consulta_Screen, 'Produtos Não Zerados')
    
    query = """
    SELECT COUNT(IIF(saldo_lan <> p.saldo, 'S', NULL)) AS distorcao
    FROM (
    SELECT l.cdpro, 
           SUM(IIF(l.TPMOV = 'S', l.quant, -l.quant)) AS saldo_lan
    FROM in01lan l 
    GROUP BY l.cdpro
    ) AS subquery
    LEFT JOIN in01pro p ON subquery.cdpro = p.cdpro
    where p.classificacao_produto in ('00','01', '02', '03', '04', '05', '06')
    """
    
    val_ven_label = ctk.CTkLabel(hub, text= 'Produtos Não Zerados:', width= 20, height= 2, font= ('', 16))
    val_ven_text = ctk.CTkLabel(hub, text= prod_get(query), width= 20, height= 2, font= ('', 14))
    val_ven_button = ctk.CTkButton(hub, text= 'Copiar Valor', width= 15, height= 20, command= lambda: copy_val(val_ven_text))
    listagem_buttn = ctk.CTkButton(hub, text= 'Listar Produtos', width= 15, height= 20, command= lambda: List_Treeview_Screen(hub))
    
    val_ven_label.place(relx= 0.5, y= 15, anchor= 'center')
    val_ven_text.place(relx= 0.5, y= 40, anchor= 'center')
    val_ven_button.place(relx= 0.8, y= 65, anchor= 'center')
    listagem_buttn.place(relx= 0.24, y= 65, anchor= 'center')