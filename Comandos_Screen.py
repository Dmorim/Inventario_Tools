def Comandos_Screen(self, parent):
    import customtkinter as ctk
    from Tk_Tooltip import ToolTip
    from Comandos_Func import on_click_confirm, precu_porcent_entry_validate
    
    comando = ctk.CTkToplevel(parent)
    comando.geometry("820x272+150+135")
    comando.title("Comandos")
    comando.resizable(False, False)
    comando.focus_set()
    comando.grab_set()
    
    frame_l = ctk.CTkFrame(comando, width= 410, height= 240, border_width= 2, border_color= 'silver', corner_radius= 5)
    frame_r = ctk.CTkFrame(comando, width= 410, height= 240, border_width= 2, border_color= 'silver', corner_radius= 5)
    frame_l.pack_propagate(False)
    frame_r.pack_propagate(False)
    
    frame_r.pack(side= 'right', anchor= 'ne')
    frame_l.pack(side= 'left', anchor= 'nw')
    
    confirm_button = ctk.CTkButton(comando, text= 'Confirmar', width= 60, height= 26, command= lambda: on_click_confirm(self, comando, checkbox_list, values_list))
    cancel_button = ctk.CTkButton(comando, text= 'Cancelar', width= 70, height= 26, command= lambda: comando.destroy())
    
    confirm_button.place(x= 747, y= 242)
    cancel_button.place(x= 671, y= 242)
    
    #Items do Frame Left
    maior_menor_precu_precom = ['Maior', 'Menor']
    maior_menor_precu_preme = ['Maior', 'Menor']
    precu_precom_cusme_vend = ['Preço de Compra', 'Custo Médio', 'Preço de Venda * 0,65']
    
    precu_porcent_vcmd = (comando.register(precu_porcent_entry_validate), '%P')
    
    com_precu_label = ctk.CTkLabel(frame_l, text= 'Comandos de Preço de Custo', font= ('verdana', 13, 'bold'))
    precu_porcent_chkbox = ctk.CTkCheckBox(frame_l, text= 'Preço de Custo por porcentagem ', font= ('verdana', 12, 'bold'), checkbox_height= 13, checkbox_width= 13)
    precu_porcent_entry = ctk.CTkEntry(frame_l, font= ('verdana', 12, 'bold'), width= 130, justify= 'center', validate= 'key', validatecommand= precu_porcent_vcmd)
    precu_arrednd_chkbox = ctk.CTkCheckBox(frame_l, text= 'Arredondar Preço de Custo ', font= ('verdana', 12, 'bold'), checkbox_height= 13, checkbox_width= 13)
    precu_precomp_chkbox = ctk.CTkCheckBox(frame_l, text= 'Preço de Custo igual Preço de Compra ', font= ('verdana', 12, 'bold'), checkbox_height= 13, checkbox_width= 13)
    precu_precomp_cbb = ctk.CTkComboBox(frame_l, font= ('verdana', 12, 'bold'), width= 120, state= 'readonly', values= maior_menor_precu_precom)
    precu_preme_chkbox = ctk.CTkCheckBox(frame_l, text= 'Preço de Custo igual Preço Médio ', font= ('verdana', 12, 'bold'), checkbox_height= 13, checkbox_width= 13)
    precu_preme_cbb = ctk.CTkComboBox(frame_l, font= ('verdana', 12, 'bold'), width= 120, state= 'readonly', values= maior_menor_precu_preme)
    precu_igual_chkbox = ctk.CTkCheckBox(frame_l, text= 'Quando zerado preço de custo igual a ', font= ('verdana', 12, 'bold'), checkbox_height= 13, checkbox_width= 13)
    precu_igual_cbb = ctk.CTkComboBox(frame_l, font= ('verdana', 12, 'bold'), width= 120, state= 'readonly', values= precu_precom_cusme_vend)
    com_ger_chkbox = ctk.CTkCheckBox(frame_l, text= '', checkbox_height= 13, checkbox_width= 13)
    com_ger_entry = ctk.CTkEntry(frame_l, font= ('verdana', 12, 'bold'), width= 378, justify= 'left')
    
    ToolTip(precu_porcent_chkbox, 'Multiplica o preço de Custo pelo numero informado', 700)
    ToolTip(precu_precomp_chkbox, 'Também executará o arredondamento no Preço de Custo', 700)
    ToolTip(precu_preme_chkbox, 'Também executará o arredondamento no Preço de Custo', 700)
    ToolTip(com_ger_entry, 'Executará qualquer comando escrito', 700)
    
    com_precu_label.place(x= 22, y= 5)
    precu_porcent_chkbox.place(x= 5, y= 38)
    precu_porcent_entry.place(x= 244, y= 36)
    precu_arrednd_chkbox.place(x= 5, y= 68)
    precu_precomp_chkbox.place(x= 5, y= 98)
    precu_precomp_cbb.place(x= 280, y= 96)
    precu_preme_chkbox.place(x= 5, y= 133)
    precu_preme_cbb.place(x= 280, y= 131)
    precu_igual_chkbox.place(x= 5, y= 168)
    precu_igual_cbb.place(x= 280, y= 166)
    com_ger_chkbox.place(x= 5, y= 204)
    com_ger_entry.place(x= 23, y= 202)
    
    #Itens do Frame Right
    
    com_geral_label = ctk.CTkLabel(frame_r, text= 'Comandos Gerais', font= ('verdana', 13, 'bold'))
    classi_pro_null_chkbox = ctk.CTkCheckBox(frame_r, text= 'Corrigir a Classificação de Produto Nula ', font= ('verdana', 12, 'bold'), checkbox_height= 13, checkbox_width= 13)
    saldo_zer_chkbox = ctk.CTkCheckBox(frame_r, text= 'Zerar Produtos Não Zerados ', font= ('verdana', 12, 'bold'), checkbox_height= 13, checkbox_width= 13)
    ctrl_estq_chkbox = ctk.CTkCheckBox(frame_r, text= "Setar Controla Estoque 'S'", font= ('verdana', 12, 'bold'), checkbox_height= 13, checkbox_width= 13)
    quant_alto_chkbox = ctk.CTkCheckBox(frame_r, text= 'Corrigir Quantidade Excessivamente Alta ', font= ('verdana', 12, 'bold'), checkbox_height= 13, checkbox_width= 13)
    saldo_neg_chkbox = ctk.CTkCheckBox(frame_r, text= 'Zerar Saldo Negativo ', font= ('verdana', 12, 'bold'), checkbox_height= 13, checkbox_width= 13)
    dtope_dtpro_chkbox = ctk.CTkCheckBox(frame_r, text= 'Deixar DTOPE igual DTPRO ', font= ('verdana', 12, 'bold'), checkbox_height= 13, checkbox_width= 13)
    
    ToolTip(saldo_zer_chkbox, 'Zerar o Saldo dos Produtos cuja o saldo está entre 0,001 e 0,000001', 700)
    ToolTip(quant_alto_chkbox, 'Deixa Quant 1 nos produtos da LAN que estão com a quantidade muito alta', 700)
    ToolTip(dtope_dtpro_chkbox, 'Deixa a Data de Operação igual a Data do Produto em Ajuste de Estoque', 700)
    
    com_geral_label.place(x= 22, y= 5)
    classi_pro_null_chkbox.place(x= 5, y= 38)
    saldo_zer_chkbox.place(x= 5, y= 68)
    ctrl_estq_chkbox.place(x= 5, y= 98)
    quant_alto_chkbox.place(x= 5, y= 131)
    saldo_neg_chkbox.place(x= 5, y= 166)
    dtope_dtpro_chkbox.place(x= 5, y= 198)
    
    values_list = [precu_porcent_entry, precu_precomp_cbb, precu_preme_cbb, precu_igual_cbb, com_ger_entry]
    checkbox_list = [precu_porcent_chkbox, precu_arrednd_chkbox, precu_precomp_chkbox, precu_preme_chkbox, precu_igual_chkbox, classi_pro_null_chkbox, saldo_zer_chkbox, ctrl_estq_chkbox, quant_alto_chkbox, saldo_neg_chkbox, dtope_dtpro_chkbox, com_ger_chkbox]
    
    precu_precomp_cbb.set('Maior')
    precu_preme_cbb.set('Maior')
    precu_igual_cbb.set('Preço de Compra')
    
    comando.bind("<Escape>", lambda e: comando.destroy())