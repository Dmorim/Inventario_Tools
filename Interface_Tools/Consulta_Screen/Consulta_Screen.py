from customtkinter import CTkLabel, CTkButton

from Consultas.Generics_Functions.Gen_Funcs_Consulta import copy_val
from Thread_Manager.Thread_Executor import thread_execução
from Consultas.Consultas_Val_Screen import Consultas_Val_Screen


def criar_tela_consulta(parent, consulta_button, container_manager, *args,
                        titulo, label_texto, get_func,
                        prefix_copy=None, on_listar=None, texto_inicial="Gerando Quantidade...", **kwargs):
    consulta_button.configure(state='disabled')
    hub = Consultas_Val_Screen(
        parent, titulo, consulta_button, container_manager)

    label = CTkLabel(hub, text=label_texto, width=20, height=2, font=('', 16))
    texto = CTkLabel(hub, text=texto_inicial,
                     width=20, height=2, font=('', 14))
    copiar = CTkButton(hub, text='Copiar Valor', command=lambda: copy_val(
        texto, prefix_copy), state='disabled', width=15, height=20)

    if on_listar:
        listar = CTkButton(hub, text='Listar Produtos',
                           command=on_listar, state='disabled')

    label.place(relx=0.5, y=15, anchor='center')
    texto.place(relx=0.5, y=40, anchor='center')
    copiar.place(relx=0.5, y=65, anchor='center')

    def update(valor):
        texto.configure(text=valor)
        copiar.configure(state='normal')
        if on_listar:
            listar.configure(state='normal')

    thread_execução(hub, get_func, update, None, *args, **kwargs)
    return hub
