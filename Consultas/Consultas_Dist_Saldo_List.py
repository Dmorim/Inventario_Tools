def List_Treeview_Screen(self, parent):
    import customtkinter as ctk
    from tkinter import ttk
    
    # Cria a tela que vai mostrar a lista de produtos
    # Diferente de outros arquivos, aqui basta a criação da tela e a insersão dos dados que já foram obtidos na query da tela anterior
    toplevel = ctk.CTkToplevel(parent)
    toplevel.title('Lista de Produtos')
    toplevel.geometry("700x300")
    toplevel.resizable(False, False)
    toplevel.transient(parent)
    toplevel.focus_set()
    toplevel.grab_set()
    
    campos = ['Código', 'Descrição', 'Saldo Lan', 'Saldo Pro'] # Cria os campos que vão ser mostrados na tela
    
    treeview = ttk.Treeview(toplevel, columns= campos, show= 'headings') # Cria o treeview que vai mostrar os valores
    treeview.heading(campos[0], text= campos[0])
    treeview.heading(campos[1], text= campos[1])
    treeview.heading(campos[2], text= campos[2])
    treeview.heading(campos[3], text= campos[3])
    treeview.column('#0', width= 0)
    treeview.column(campos[0], width= 50, anchor= 'e')
    treeview.column(campos[1], width= 400, anchor= 'center')
    treeview.column(campos[2], width= 80, anchor= 'center')
    treeview.column(campos[3], width= 80, anchor= 'center')
    
    vsb = ttk.Scrollbar(toplevel, orient= "vertical", command= treeview.yview) # Cria a barra de rolagem
    treeview.configure(yscrollcommand=vsb.set) # Configura a barra de rolagem
    vsb.pack(side= 'right', fill= 'y') # Posiciona a barra de rolagem
    treeview.pack(fill= 'both', expand= True) # Posiciona o treeview
    
    Treeview_Insert(treeview, self.dist_saldo_list) # Insere os valores obtidos na query no treeview
    
def Treeview_Insert(treeview, rows):
    for row in rows:
        treeview.insert('', 'end', values= row)
