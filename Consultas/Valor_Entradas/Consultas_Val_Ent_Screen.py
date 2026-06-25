def Val_Ent_Screen(self, Consulta_Screen, consulta_button):
    import customtkinter as ctk

    # Importa as funções que vão ser usadas na tela dos arquivos Consultas/Consultas_Val_Ent_Func e Consutlas/Consultas_Val_Screen
    from Consultas.Consultas_Val_Screen import Consultas_Val_Screen
    from Consultas.Valor_Entradas.Consultas_Val_Ent_Func import ent_get, copy_val
    from Thread_Manager.Thread_Executor import thread_execução

    # Desabilita o botão de consulta para evitar múltiplas execuções simultâneas
    consulta_button.configure(state='disabled')

    hub = Consultas_Val_Screen(
        Consulta_Screen, 'Valor das Compras', consulta_button)

    val_ven_label = ctk.CTkLabel(
        hub, text='Valor das Compras:', width=20, height=2, font=('', 16))
    val_ven_text = ctk.CTkLabel(
        hub, text='Gerando Valor...', width=20, height=2, font=('', 14))
    val_ven_button = ctk.CTkButton(
        hub, text='Copiar Valor', width=15, height=20, command=lambda: copy_val(val_ven_text))

    val_ven_label.place(relx=0.5, y=15, anchor='center')
    val_ven_text.place(relx=0.5, y=40, anchor='center')
    val_ven_button.place(relx=0.5, y=65, anchor='center')

    def update_val_ent(valor):
        val_ven_text.configure(text=valor)
        val_ven_button.configure(state='normal')

    thread_execução(hub, ent_get, update_val_ent, None, self)
