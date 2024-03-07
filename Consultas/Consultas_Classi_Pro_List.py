def List_Treeview_Screen(parent):
    import customtkinter as ctk
    from tkinter import ttk
    
    toplevel = ctk.CTkToplevel(parent) # Cria a janela toplevel como um Toplevel do parent
    toplevel.title('Lista de Produtos')
    toplevel.geometry("700x300")
    toplevel.resizable(False, False)
    toplevel.focus_set()
    toplevel.transient(parent)
    toplevel.grab_set()
    
    campos = ['Código', 'Descrição', 'Saldo', 'Preço de Custo'] # Cria uma lista com os campos que serão exibidos na Treeview
    
    treeview = ttk.Treeview(toplevel, columns= campos, show= 'headings') # Cria a Treeview com os campos da lista
    treeview.heading(campos[0], text= campos[0])
    treeview.heading(campos[1], text= campos[1])
    treeview.heading(campos[2], text= campos[2])
    treeview.heading(campos[3], text= campos[3])
    treeview.column('#0', width= 0)
    treeview.column(campos[0], width= 50, anchor= 'e') # Define o tamanho e a posição dos campos na Treeview
    treeview.column(campos[1], width= 400, anchor= 'center')
    treeview.column(campos[2], width= 80, anchor= 'center')
    treeview.column(campos[3], width= 140, anchor= 'e')
    
    vsb = ttk.Scrollbar(toplevel, orient= "vertical", command= treeview.yview) # Cria a barra de rolagem vertical
    treeview.configure(yscrollcommand=vsb.set)
    vsb.pack(side= 'right', fill= 'y') # Posiciona a barra de rolagem vertical
    treeview.pack(fill= 'both', expand= True) # Posiciona a Treeview
    
    Treeview_Select(treeview) # Chama a função Treeview_Select passando a Treeview como argumento
    
def Treeview_Select(treeview):
    # Função que consulta no banco de dados os valores da lista
    # Args:
        # treeview: widget Treeview
    
    from Banco_de_Dados.Inventario_Conn import Connect # Importa a classe Connect do módulo Inventario_Conn do pacote Banco_de_Dados
    
    # Realiza a query buscando no banco de dados os campos que serão exibidos na Treeview
    query = "select cdpro, nmpro, saldo, precu from in01pro where classificacao_produto is null or classificacao_produto = ''"
    Connect.cursor.execute(query)
    rows = Connect.cursor.fetchall() # Atribui a variável rows o resultado da consulta
    Treeview_Insert(treeview, rows) # Chama a função Treeview_Insert passando a Treeview e a variável rows como argumentos
    
def Treeview_Insert(treeview, rows):
    # Função que insere os valores obtidos do banco de dados na Treeview
    # Args:
        # treeview: widget Treeview
        # rows: tupla com os valores obtidos do banco de dados
        
    for row in rows: # Loop que percorre a tupla rows
        treeview.insert('', 'end', values= row) # Insere os valores na Treeview
