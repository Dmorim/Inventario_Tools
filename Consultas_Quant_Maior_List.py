def List_Treeview_Screen(parent):
    import customtkinter as ctk
    from tkinter import ttk
    
    toplevel = ctk.CTkToplevel(parent)
    toplevel.title('Lista de Produtos')
    toplevel.geometry("700x300")
    toplevel.resizable(False, False)
    toplevel.focus_set()
    toplevel.grab_set()
    
    campos = ['Código', 'Nota', 'Saldo', 'TPMOV', 'DTPRO']
    
    treeview = ttk.Treeview(toplevel, columns= campos, show= 'headings')
    treeview.heading(campos[0], text= campos[0])
    treeview.heading(campos[1], text= campos[1])
    treeview.heading(campos[2], text= campos[2])
    treeview.heading(campos[3], text= campos[3])
    treeview.heading(campos[4], text= campos[4])
    treeview.column('#0', width= 0)
    treeview.column(campos[0], width= 50, anchor= 'center')
    treeview.column(campos[1], width= 100, anchor= 'center')
    treeview.column(campos[2], width= 80, anchor= 'center')
    treeview.column(campos[3], width= 80, anchor= 'center')
    treeview.column(campos[4], width= 140, anchor= 'center')
    
    vsb = ttk.Scrollbar(toplevel, orient= "vertical", command= treeview.yview)
    treeview.configure(yscrollcommand=vsb.set)
    vsb.pack(side= 'right', fill= 'y')
    treeview.pack(fill= 'both', expand= True)
    
    Treeview_Select(treeview)
    
def Treeview_Select(treeview):
    from Inventario_Conn import Connect
    query = "select cdpro, notfi, saldo, tpmov, dtpro from in01lan where quant > 999999 and dtpro between '01.01.2023' and '31.12.2023'"
    Connect.cursor.execute(query)
    rows = Connect.cursor.fetchall()
    Treeview_Insert(treeview, rows)
    
def Treeview_Insert(treeview, rows):
    for row in rows:
        treeview.insert('', 'end', values= row)
