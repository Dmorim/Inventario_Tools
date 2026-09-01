from customtkinter import CTkToplevel
from tkinter import ttk
from Thread_Manager.Query_Operations import query_selector, query_executor
from Thread_Manager.Thread_Executor import thread_execução


def criar_tela_listagem(parent, titulo, colunas, query, params=None, geometry: str = "500x300") -> CTkToplevel:

    def buscar():
        return query_executor(query_selector, query, params)

    def ao_terminar(rows):
        for row in rows:
            treeview.insert('', 'end', values=row)

    toplevel = CTkToplevel(parent)
    toplevel.title(titulo)
    toplevel.geometry(geometry)
    toplevel.resizable(False, False)
    toplevel.transient(parent)
    toplevel.focus_set()

    treeview = ttk.Treeview(toplevel, columns=colunas, show='headings')

    for col in colunas:
        if col == 'Código':
            treeview.heading(col, text=col)
            treeview.column(col, width=50, anchor='e')
        elif col == 'Descrição':
            treeview.heading(col, text=col)
            treeview.column(col, width=370, anchor='center')
        elif col == 'Saldo':
            treeview.heading(col, text=col)
            treeview.column(col, width=50, anchor='center')
        else:
            treeview.heading(col, text=col)
            treeview.column(col, width=50, anchor='e')

    vsb = ttk.Scrollbar(toplevel, orient="vertical", command=treeview.yview)
    treeview.configure(yscrollcommand=vsb.set)
    vsb.pack(side='right', fill='y')
    treeview.pack(fill='both', expand=True)

    toplevel.protocol("WM_DELETE_WINDOW", lambda: toplevel.destroy())

    treeview.bind("<Double-1>", lambda event: treeview.selection())
    treeview.bind("<Escape>", lambda event: toplevel.destroy())

    thread_execução(toplevel, buscar, ao_terminar)

    return toplevel, treeview
