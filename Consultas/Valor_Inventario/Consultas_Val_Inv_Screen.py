def hub_val_inv(Consulta_Screen):
    import customtkinter as ctk

    # Importa as funções que vão ser usadas na tela	 dos arquivos Consultas/Consultas_Val_Inv_Func e Consutlas/Consultas_Val_Screen
    from Consultas.Valor_Inventario.Consultas_Val_Inv_Func import inv_get, copy_val
    from Consultas.Consultas_Val_Screen import Consultas_Val_Screen
    from Thread_Manager.Thread_Executor import thread_execução

    hub = Consultas_Val_Screen(Consulta_Screen, 'Valor do Inventário')

    val_inv_label = ctk.CTkLabel(
        hub, text='Valor do Inventário:', width=20, height=2, font=('', 16))
    val_inv_text = ctk.CTkLabel(
        hub, text='Gerando Valor...', width=20, height=2, font=('', 14))
    val_inv_button = ctk.CTkButton(
        hub, text='Copiar Valor', width=15, height=20, command=lambda: copy_val(val_inv_text), state='disabled')

    val_inv_label.place(relx=0.5, y=15, anchor='center')
    val_inv_text.place(relx=0.5, y=40, anchor='center')
    val_inv_button.place(relx=0.5, y=65, anchor='center')

    def update_val_inv(valor):
        val_inv_text.configure(text=valor)
        val_inv_button.configure(state='normal')

    thread_execução(hub, inv_get, update_val_inv)
