def Classi_Pro_Screen(Consulta_Screen, consulta_button):
    import customtkinter as ctk

    # Importa as funções e variáveis do arquivo Consultas_Val_Screen e Gen_Funcs_Consulta. Bem como a função List_Treeview_Screen para criação da tela de lista
    from Consultas.Consultas_Val_Screen import Consultas_Val_Screen
    from Consultas.Generics_Functions.Gen_Funcs_Consulta import prod_get, copy_val
    from Consultas.Classificação_Do_Produto.Consultas_Classi_Pro_List import List_Treeview_Screen
    from Thread_Manager.Thread_Executor import thread_execução

    # Desabilita o botão de consulta para evitar múltiplas execuções simultâneas
    consulta_button.configure(state='disabled')

    # Query para contar os produtos sem classificação do produto
    query = "select count (*) from in01pro where classificacao_produto is null or classificacao_produto = ''"

    # Cria a tela de consulta com base na função Consultas_Val_Screen
    hub = Consultas_Val_Screen(
        Consulta_Screen, 'Produtos sem Classificação do Produto', consulta_button)

    # Cria os labels e botões da tela de consulta
    val_ven_label = ctk.CTkLabel(
        hub, text='Produtos sem Classificação do Produto:', width=20, height=2, font=('', 13))

    # Cria o label que exibe o valor da consulta usando uma query executada no arquivo Gen_Funcs_Consulta
    val_ven_text = ctk.CTkLabel(
        hub, text="Gerando Quantidade...", width=20, height=2, font=('', 14))

    val_ven_button = ctk.CTkButton(
        hub, text='Copiar Valor', width=15, height=20, command=lambda: copy_val(val_ven_text), state='disabled')
    listagem_buttn = ctk.CTkButton(
        hub, text='Listar Produtos', width=15, height=20, command=lambda: List_Treeview_Screen(hub), state='disabled')

    # Posicionamento dos widgets
    val_ven_label.place(relx=0.5, y=15, anchor='center')
    val_ven_text.place(relx=0.5, y=40, anchor='center')
    val_ven_button.place(relx=0.8, y=65, anchor='center')
    listagem_buttn.place(relx=0.24, y=65, anchor='center')

    def update_val(valor):
        val_ven_text.configure(text=valor)
        val_ven_button.configure(state='normal')
        listagem_buttn.configure(state='normal')

    thread_execução(hub, prod_get, update_val, None, query)
