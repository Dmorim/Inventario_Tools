def Comandos_Screen(self, parent):
    import customtkinter as ctk # Importa a biblioteca customtkinter como ctk
    
    from Outros.Tk_Tooltip import ToolTip # Importa a função ToolTip do arquivo Tk_Tooltip da pasta Outros
    from Comandos.Comandos_Func import on_click_confirm, precu_porcent_entry_validate # Importa as funções on_click_confirm e precu_porcent_entry_validate do arquivo Comandos_Func da pasta Comandos
    from Comandos.Comandos_Dist_Saldo import on_click_dist_saldo # Importa a função on_click_dist_saldo do arquivo Comandos_Dist_Saldo da pasta Comandos
    
    comando = ctk.CTkToplevel(parent) # Cria a janela comando como um Toplevel do parent
    comando.geometry("820x292+150+135")
    comando.title("Comandos")
    comando.resizable(False, False)
    comando.transient(parent)
    comando.focus_set()
    comando.grab_set()
    
    # Criação dos frames a esquerda(frame_l) e a direita(frame_r) da janela comando
    frame_l = ctk.CTkFrame(comando, width= 410, height= 260, border_width= 2, border_color= 'silver', corner_radius= 5)
    frame_r = ctk.CTkFrame(comando, width= 410, height= 260, border_width= 2, border_color= 'silver', corner_radius= 5)
    frame_l.pack_propagate(False)
    frame_r.pack_propagate(False)
    
    frame_r.pack(side= 'right', anchor= 'ne')
    frame_l.pack(side= 'left', anchor= 'nw')
    
    # Criação dos botões confirmar e cancelar
    confirm_button = ctk.CTkButton(comando, text= 'Confirmar', width= 60, height= 26, command= lambda: on_click_confirm(self, comando, checkbox_list, values_list))
    cancel_button = ctk.CTkButton(comando, text= 'Cancelar', width= 70, height= 26, command= lambda: comando.destroy())
    
    # Posicionamento dos botões confirmar e cancelar
    confirm_button.place(x= 747, y= 262)
    cancel_button.place(x= 671, y= 262)
    
    # Armazenamento de valores para os combobox
    maior_menor_precu_precom = ['Maior', 'Menor']
    maior_menor_precu_preme = ['Maior', 'Menor']
    precu_precom_cusme_vend = ['Preço de Compra', 'Custo Médio', 'Preço de Venda * 0,65']
    
    # Validação do Entry precu_porcent_entry
    precu_porcent_vcmd = (comando.register(precu_porcent_entry_validate), '%P')
    
    # Itens do Frame Left
    com_precu_label = ctk.CTkLabel(frame_l, text= 'Comandos de Preço de Custo', font= ('verdana', 13, 'bold'))
    precu_porcent_chkbox = ctk.CTkCheckBox(frame_l, text= 'Preço de Custo por porcentagem ', font= ('verdana', 12, 'bold'), checkbox_height= 13, checkbox_width= 13)
    precu_porcent_entry = ctk.CTkEntry(frame_l, font= ('verdana', 12, 'bold'), width= 130, justify= 'center', validate= 'key', validatecommand= precu_porcent_vcmd)
    precu_arrednd_chkbox = ctk.CTkCheckBox(frame_l, text= 'Arredondar Preço de Custo ', font= ('verdana', 12, 'bold'), checkbox_height= 13, checkbox_width= 13)
    precu_precomp_chkbox = ctk.CTkCheckBox(frame_l, text= 'Preço de Custo igual Preço de Compra ', font= ('verdana', 12, 'bold'), checkbox_height= 13, checkbox_width= 13)
    precu_precomp_cbb = ctk.CTkComboBox(frame_l, font= ('verdana', 12, 'bold'), width= 120, state= 'readonly', values= maior_menor_precu_precom)
    precu_preme_chkbox = ctk.CTkCheckBox(frame_l, text= 'Preço de Custo igual Custo Médio ', font= ('verdana', 12, 'bold'), checkbox_height= 13, checkbox_width= 13)
    precu_preme_cbb = ctk.CTkComboBox(frame_l, font= ('verdana', 12, 'bold'), width= 120, state= 'readonly', values= maior_menor_precu_preme)
    precu_igual_chkbox = ctk.CTkCheckBox(frame_l, text= 'Quando zerado preço de custo igual a ', font= ('verdana', 12, 'bold'), checkbox_height= 13, checkbox_width= 13)
    precu_igual_cbb = ctk.CTkComboBox(frame_l, font= ('verdana', 12, 'bold'), width= 120, state= 'readonly', values= precu_precom_cusme_vend)
    com_ger_chkbox = ctk.CTkCheckBox(frame_l, text= '', checkbox_height= 13, checkbox_width= 13)
    com_ger_entry = ctk.CTkEntry(frame_l, font= ('verdana', 12, 'bold'), width= 378, justify= 'left')
    
    # ToolTip dos itens do Frame Left
    ToolTip(precu_porcent_chkbox, 'Multiplica o preço de Custo pelo numero informado', 700)
    ToolTip(precu_precomp_chkbox, 'Deixa Preço de Custo igual a Preço de Compra quando o Preço de Compra for Maior/Menor. Também executará o arredondamento no Preço de Custo', 700)
    ToolTip(precu_preme_chkbox, 'Deixa Preço de Custo igual a Custo Médio quando o Custo Médio for Maior/Menor. Também executará o arredondamento no Preço de Custo', 700)
    ToolTip(precu_igual_chkbox, 'Deixa Preço de Custo igual a Preço de Compra, Custo Médio ou Preço de Venda * 0,65 quando o Preço de Custo for 0 e o saldo for 0', 700)
    ToolTip(com_ger_entry, 'Executará qualquer comando escrito', 700)
    
    # Posicionamento dos itens do Frame Left
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
    
    # Itens do Frame Right
    com_geral_label = ctk.CTkLabel(frame_r, text= 'Comandos Gerais', font= ('verdana', 13, 'bold'))
    classi_pro_null_chkbox = ctk.CTkCheckBox(frame_r, text= 'Corrigir a Classificação de Produto Nula ', font= ('verdana', 12, 'bold'), checkbox_height= 13, checkbox_width= 13)
    saldo_zer_chkbox = ctk.CTkCheckBox(frame_r, text= 'Zerar Produtos Não Zerados ', font= ('verdana', 12, 'bold'), checkbox_height= 13, checkbox_width= 13)
    ctrl_estq_chkbox = ctk.CTkCheckBox(frame_r, text= "Setar Controla Estoque 'S'", font= ('verdana', 12, 'bold'), checkbox_height= 13, checkbox_width= 13)
    quant_alto_chkbox = ctk.CTkCheckBox(frame_r, text= 'Corrigir Quantidade Excessivamente Alta ', font= ('verdana', 12, 'bold'), checkbox_height= 13, checkbox_width= 13)
    saldo_neg_chkbox = ctk.CTkCheckBox(frame_r, text= 'Zerar Saldo Negativo ', font= ('verdana', 12, 'bold'), checkbox_height= 13, checkbox_width= 13)
    dtope_dtpro_chkbox = ctk.CTkCheckBox(frame_r, text= 'Deixar DTOPE igual DTPRO ', font= ('verdana', 12, 'bold'), checkbox_height= 13, checkbox_width= 13)
    dist_saldo_button = ctk.CTkButton(frame_r, text= 'Correção de Distorção de Saldo ', font= ('verdana', 12, 'bold'), width= 390, anchor= 'center', command= lambda: on_click_dist_saldo(self, comando))
    
    # ToolTip dos itens do Frame Right
    ToolTip(classi_pro_null_chkbox, 'Deixa a classificação do produto 00 se ele estiver nulo', 700)
    ToolTip(saldo_zer_chkbox, 'Zerar o Saldo dos Produtos cuja o saldo está entre 0,001 e 0,000001', 700)
    ToolTip(ctrl_estq_chkbox, 'Seta o campo Controla Estoque para S nos produtos que estão com Controla Estoque N', 700)
    ToolTip(quant_alto_chkbox, 'Deixa Quant 1 nos produtos da LAN que estão com a quantidade muito alta', 700)
    ToolTip(saldo_neg_chkbox, 'Zera o saldo dos produtos que estão com saldo negativo', 700)
    ToolTip(dtope_dtpro_chkbox, 'Deixa a Data de Operação igual a Data do Produto em Ajuste de Estoque', 700)
    ToolTip(dist_saldo_button, 'Corrige a distorção de saldo entre LAN e PRO\n É preciso ter gerado a lista de distorções antes de executar a função', 700)
    
    # Posicionamento dos itens do Frame Right
    com_geral_label.place(x= 22, y= 5)
    classi_pro_null_chkbox.place(x= 5, y= 38)
    saldo_zer_chkbox.place(x= 5, y= 68)
    ctrl_estq_chkbox.place(x= 5, y= 98)
    quant_alto_chkbox.place(x= 5, y= 131)
    saldo_neg_chkbox.place(x= 5, y= 166)
    dtope_dtpro_chkbox.place(x= 5, y= 198)
    dist_saldo_button.place(x= 10, y= 226)

    # Lista de valores e checkbox
    values_list = [precu_porcent_entry, precu_precomp_cbb, precu_preme_cbb, precu_igual_cbb, com_ger_entry]
    checkbox_list = [precu_porcent_chkbox, precu_arrednd_chkbox, precu_precomp_chkbox, precu_preme_chkbox, precu_igual_chkbox, classi_pro_null_chkbox, saldo_zer_chkbox, ctrl_estq_chkbox, quant_alto_chkbox, saldo_neg_chkbox, dtope_dtpro_chkbox, com_ger_chkbox]
    
    # Setar valores padrões dos combobox
    precu_precomp_cbb.set('Maior')
    precu_preme_cbb.set('Maior')
    precu_igual_cbb.set('Preço de Compra')
    
    # Verificar se a lista de distorção de saldo está vazia ou foi criada
    if hasattr(self, 'dist_saldo_list'):
        if len(self.dist_saldo_list) == 0:
            dist_saldo_button.configure(state= 'disabled') # Desabilita o botão de distorção de saldo caso não haja produtos com distorções
    else:
        dist_saldo_button.configure(state= 'disabled') # Desabilita o botão de distorção caso a lista de distorção não tenha sido criada
    
    # Atalhos do teclado para sair da tela e executar a função confirmar
    comando.bind("<Escape>", lambda e: comando.destroy())
    comando.bind("<F5>", lambda event: confirm_button.invoke())