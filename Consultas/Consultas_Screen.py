def Consulta_Total_Screen(self, root):
    import customtkinter as ctk
    
    # Importação de todas as telas de consultas + ToolTip
    from Outros.Tk_Tooltip import ToolTip
    from Consultas.Consultas_Val_Inv_Screen import hub_val_inv
    from Consultas.Consultas_Val_Ven_Screen import Val_Ven_Screen
    from Consultas.Consultas_Val_Ent_Screen import Val_Ent_Screen
    from Consultas.Consultas_NZer_Prod_Screen import Prod_NZer_Screen
    from Consultas.Consultas_ZCusto_Screen import Prod_ZCusto_Screen
    from Consultas.Consultas_Classi_Pro_Screen import Classi_Pro_Screen
    from Consultas.Consultas_Precu_Preve_Screen import Precu_Preve_Screen
    from Consultas.Consultas_Preve_Precu_Precom_Screen import Preve_Precu_Precom_Screen
    from Consultas.Consultas_Contr_Estq_Screen import Contr_Estq_Screen
    from Consultas.Consultas_Quant_Maior_Screen import Quant_Maior_Screen
    from Consultas.Consultas_Dist_Saldo_Screen import dist_saldo_screen
    
    Consulta_Screen = ctk.CTkToplevel(root) # Cria a tela principal
    Consulta_Screen.title("Consultas no Banco de Dados")
    Consulta_Screen.geometry("790x225")
    Consulta_Screen.resizable(False, False)
    Consulta_Screen.transient(root)
    Consulta_Screen.focus_set()
    Consulta_Screen.grab_set()
    
    # Cria os frames que vão conter os botões, o frame à esquerda (frame_l) e o frame à direita (frame_r
    frame_l = ctk.CTkFrame(Consulta_Screen, width= 395, height= 203, border_width= 2, border_color= 'silver')
    frame_r = ctk.CTkFrame(Consulta_Screen, width= 395, height= 203, border_width= 2, border_color= 'silver')
    
    # Posiciona os frames
    frame_l.pack(side= 'left', anchor= 'sw')
    frame_r.pack(side= 'right', anchor= 'se')
    
    # Criação dos botões e Labels da aba esquerda
    title_label = ctk.CTkLabel(Consulta_Screen, text= 'Consultas no Banco de Dados', width= 200, height= 2, font= ('', 18, 'bold'))
    val_inv_button = ctk.CTkButton(frame_l, text= 'Gerar valor do Inventário', width= 380, height= 25, command= lambda: hub_val_inv(Consulta_Screen), text_color= 'silver', font = ('', 15, 'bold'))
    val_ven_button = ctk.CTkButton(frame_l, text= 'Gerar valor das Vendas', width= 380, height= 25, command= lambda: Val_Ven_Screen(self, Consulta_Screen), text_color= 'silver', font = ('', 15, 'bold'))
    val_com_button = ctk.CTkButton(frame_l, text= 'Gerar valor das Compras', width= 380, height= 25, command= lambda: Val_Ent_Screen(self, Consulta_Screen), text_color= 'silver', font = ('', 15, 'bold'))
    ctrl_estoq = ctk.CTkButton(frame_l, text= 'Produtos com Controla Estoque = N', width= 380, height= 25, command= lambda: Contr_Estq_Screen(self, Consulta_Screen), text_color= 'silver', font = ('', 14, 'bold'))
    saldo_nzerado_button = ctk.CTkButton(frame_l, text= 'Produtos com Saldo Não Zerado', width= 380, height= 25, command= lambda: Prod_NZer_Screen(Consulta_Screen), text_color= 'silver', font = ('', 14, 'bold'))
    dist_saldo_button = ctk.CTkButton(frame_l, text= 'Distorções de Saldo', width= 380, height= 25, command= lambda: dist_saldo_screen(self, Consulta_Screen), text_color= 'silver', font = ('', 14, 'bold'))
    
    # Criação dos botões e Labels da aba direita
    precu_zer_button = ctk.CTkButton(frame_r, text= 'Produtos com Preço de Custo Zerado', width= 380, height= 25, command= lambda: Prod_ZCusto_Screen(Consulta_Screen), text_color= 'silver', font = ('', 14, 'bold'))
    classif_prod_null = ctk.CTkButton(frame_r, text= 'Produtos com Classificação do Produto nula', width= 380, height= 25, command= lambda: Classi_Pro_Screen(Consulta_Screen), text_color= 'silver', font = ('', 14, 'bold'))
    quant_maior = ctk.CTkButton(frame_r, text= 'Produtos com Quantidade Maior que 999999', width= 380, height= 25, command= lambda: Quant_Maior_Screen(self, Consulta_Screen), text_color= 'silver', font = ('', 13, 'bold'))
    precu_maior_preve = ctk.CTkButton(frame_r, text= 'Produtos com Preço de Custo Maior que o de Venda', width= 380, height= 25, command= lambda: Precu_Preve_Screen(Consulta_Screen), text_color= 'silver', font = ('', 13, 'bold'))
    precuplus_zer_button = ctk.CTkButton(frame_r, text= 'Produtos com Preço de Custo, Compra e Venda Zerado', width= 380, height= 25, command= lambda: Preve_Precu_Precom_Screen(Consulta_Screen), text_color= 'silver', font = ('', 13, 'bold'))
    
    # Criação dos ToolTips
    ToolTip(val_inv_button, "Gera o valor do inventário com base no saldo e preço de custo dos produtos")
    ToolTip(ctrl_estoq, "Produtos em que o campo controla estoque é igual a N")
    ToolTip(saldo_nzerado_button, "Produtos com saldo entre 0,01 e 0,000001")
    ToolTip(precu_zer_button, "Produtos com preço de custo zerado")
    ToolTip(classif_prod_null, "Produtos com classificação do produto nula")
    ToolTip(quant_maior, "Produtos com quantidade ou valor maior que 999999 na IN01LAN")
    ToolTip(precu_maior_preve, "Produtos com preço de custo maior que o de venda")
    ToolTip(precuplus_zer_button, "Produtos com preço de custo, compra e venda zerados")
    ToolTip(dist_saldo_button, "Produtos com saldo de lançamento diferente do saldo de produto. \n Essa consulta pode demorar algum tempo.")
    
    # Posicionamento de todos os widgets na tela
    title_label.place(relx= 0.5, y= 10, anchor= 'center')
    
    val_inv_button.place(relx= 0.5, y= 26, anchor= 'center')
    val_ven_button.place(relx= 0.5, y= 58, anchor= 'center')
    val_com_button.place(relx= 0.5, y= 89, anchor= 'center')
    ctrl_estoq.place(relx= 0.5, y= 120, anchor= 'center')
    saldo_nzerado_button.place(relx= 0.5, y= 152, anchor= 'center')
    dist_saldo_button.place(relx= 0.5, y= 183, anchor= 'center')
    
    
    precu_zer_button.place(relx= 0.5, y= 26, anchor= 'center')
    classif_prod_null.place(relx= 0.5, y= 58, anchor= 'center')
    quant_maior.place(relx= 0.5, y= 89, anchor= 'center')
    precu_maior_preve.place(relx= 0.5, y= 120, anchor= 'center')
    precuplus_zer_button.place(relx= 0.5, y= 152, anchor= 'center')
    
    Consulta_Screen.bind("<Escape>", lambda e: Consulta_Screen.destroy()) # Fecha a tela com o botão ESC