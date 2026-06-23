def Contr_Estq_Screen(self, Consulta_Screen):
    import customtkinter as ctk
    from Consultas.Consultas_Val_Screen import Consultas_Val_Screen
    from Consultas.Generics_Functions.Gen_Funcs_Consulta import prod_get, copy_val
    from Consultas.Controla_Estoque.Consultas_Contr_Estq_List import List_Treeview_Screen
    from Thread_Manager.Thread_Executor import thread_execução

    query = f"select count (*) from in01lan where controlaestoque = 'N' and dtpro between '{self.data_banco_inicial}' and '{self.data_banco_final}'"

    hub = Consultas_Val_Screen(Consulta_Screen, 'Produtos Controla Estoque')

    val_ven_label = ctk.CTkLabel(
        hub, text='Produtos com Controla Estoque = N', width=20, height=2, font=('', 13))
    val_ven_text = ctk.CTkLabel(
        hub, text="Gerando Quantidade...", width=20, height=2, font=('', 14))
    val_ven_button = ctk.CTkButton(
        hub, text='Copiar Valor', width=15, height=20, command=lambda: copy_val(val_ven_text), state='disabled')
    listagem_buttn = ctk.CTkButton(
        hub, text='Listar Produtos', width=15, height=20, command=lambda: List_Treeview_Screen(self,hub), state='disabled')

    val_ven_label.place(relx=0.5, y=15, anchor='center')
    val_ven_text.place(relx=0.5, y=40, anchor='center')
    val_ven_button.place(relx=0.8, y=65, anchor='center')
    listagem_buttn.place(relx=0.24, y=65, anchor='center')

    def update_val(valor):
        val_ven_text.configure(text=valor)
        val_ven_button.configure(state='normal')
        listagem_buttn.configure(state='normal')

    thread_execução(hub, prod_get, update_val, None, query)
