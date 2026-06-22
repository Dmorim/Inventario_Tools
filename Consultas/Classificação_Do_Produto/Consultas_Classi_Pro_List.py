def List_Treeview_Screen(parent):

    def Treeview_Select(treeview):
        from Thread_Manager.Query_Operations import query_selector, query_executor
        from Thread_Manager.Thread_Executor import thread_execução

        query = (
            "select cdpro, nmpro, saldo, precu from in01pro "
            "where classificacao_produto is null or classificacao_produto = ''"
        )

        # Apenas a busca vai para a thread — não toca em nenhum widget aqui dentro
        def buscar():
            return query_executor(query_selector, query)

        # O resultado chega aqui já na thread principal — seguro inserir no widget
        def ao_terminar(rows):
            Treeview_Insert(treeview, rows)

        thread_execução(treeview, buscar, ao_terminar)

    def Treeview_Insert(treeview, rows):
        # Função que insere os valores obtidos do banco de dados na Treeview
        # Args:
        # treeview: widget Treeview
        # rows: tupla com os valores obtidos do banco de dados

        for row in rows:  # Loop que percorre a tupla rows
            # Insere os valores na Treeview
            treeview.insert('', 'end', values=row)

    import customtkinter as ctk
    from tkinter import ttk

    # Cria a janela toplevel como um Toplevel do parent
    toplevel = ctk.CTkToplevel(parent)
    toplevel.title('Lista de Produtos')
    toplevel.geometry("700x300")
    toplevel.resizable(False, False)
    toplevel.focus_set()
    toplevel.transient(parent)
    toplevel.grab_set()

    # Cria uma lista com os campos que serão exibidos na Treeview
    campos = ['Código', 'Descrição', 'Saldo', 'Preço de Custo']

    # Cria a Treeview com os campos da lista
    treeview = ttk.Treeview(toplevel, columns=campos, show='headings')
    treeview.heading(campos[0], text=campos[0])
    treeview.heading(campos[1], text=campos[1])
    treeview.heading(campos[2], text=campos[2])
    treeview.heading(campos[3], text=campos[3])
    treeview.column('#0', width=0)
    # Define o tamanho e a posição dos campos na Treeview
    treeview.column(campos[0], width=50, anchor='e')
    treeview.column(campos[1], width=400, anchor='center')
    treeview.column(campos[2], width=80, anchor='center')
    treeview.column(campos[3], width=140, anchor='e')

    # Cria a barra de rolagem vertical
    vsb = ttk.Scrollbar(toplevel, orient="vertical", command=treeview.yview)
    treeview.configure(yscrollcommand=vsb.set)
    vsb.pack(side='right', fill='y')  # Posiciona a barra de rolagem vertical
    treeview.pack(fill='both', expand=True)  # Posiciona a Treeview

    # Chama a função para preencher a Treeview com os dados do banco de dados
    Treeview_Select(treeview)
