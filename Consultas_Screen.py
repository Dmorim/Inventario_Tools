def Consulta_Total_Screen(self, root):
    import customtkinter as ctk
    
    Consulta_Screen = ctk.CTkToplevel(root)
    Consulta_Screen.title("Consultas no Banco de Dados")
    Consulta_Screen.geometry("340x225")
    Consulta_Screen.resizable(False, False)
    Consulta_Screen.focus()
    Consulta_Screen.grab_set()
    
    title_label = ctk.CTkLabel(Consulta_Screen, text= 'Consultas no Banco de Dados', width= 200, height= 2, font= ('', 18, 'bold'), text_color= 'silver')
    val_inv_button = ctk.CTkButton(Consulta_Screen, text= 'Gerar valor do Inventário', width= 200, height= 25, command= lambda: print('Valor do Inventário'), text_color= 'silver', font = ('', 15, 'bold'))
    val_ven_button = ctk.CTkButton(Consulta_Screen, text= 'Gerar valor das Vendas', width= 200, height= 25, command= lambda: print('Valor das Vendas'), text_color= 'silver', font = ('', 15, 'bold'))
    val_com_button = ctk.CTkButton(Consulta_Screen, text= 'Gerar valor das Compras', width= 200, height= 25, command= lambda: print('Valor das Compras'), text_color= 'silver', font = ('', 15, 'bold'))
    saldo_nzerado_button = ctk.CTkButton(Consulta_Screen, text= 'Produtos com Saldo Não Zerado', width= 200, height= 25, command= lambda: print('Produtos com Saldo Não Zerado'), text_color= 'silver', font = ('', 13, 'bold'))
    precu_zer_button = ctk.CTkButton(Consulta_Screen, text= 'Produtos com Preço de Custo Zerado', width= 200, height= 25, command= lambda: print('Produtos com Preço Zerado'), text_color= 'silver', font = ('', 13, 'bold'))
    precuplus_zer_button = ctk.CTkButton(Consulta_Screen, text= 'Produtos com Preço de Custo, Compra e Venda Zerado', width= 200, height= 25, command= lambda: print('Produtos com Preço + Zerado'), text_color= 'silver', font = ('', 11, 'bold'))
    
    
    title_label.place(relx= 0.5, y= 10, anchor= 'center')
    val_inv_button.place(relx= 0.5, y= 50, anchor= 'center')
    val_ven_button.place(relx= 0.5, y= 79, anchor= 'center')
    val_com_button.place(relx= 0.5, y= 108, anchor= 'center')
    saldo_nzerado_button.place(relx= 0.5, y= 137, anchor= 'center')
    precu_zer_button.place(relx= 0.5, y= 166, anchor= 'center')
    precuplus_zer_button.place(relx= 0.5, y= 195, anchor= 'center')