def List_Treeview_Screen(self, parent):
    import customtkinter as ctk
    from tkinter import ttk
    toplevel = ctk.CTkToplevel(parent)
    toplevel.title('Lista de Produtos')
    toplevel.geometry("700x300")
    toplevel.resizable(False, False)
    toplevel.transient(parent)
    toplevel.focus_set()
    toplevel.grab_set()
    
    campos = ['Código', 'Descrição', 'Saldo Lan', 'Saldo Pro']
    
    treeview = ttk.Treeview(toplevel, columns= campos, show= 'headings')
    treeview.heading(campos[0], text= campos[0])
    treeview.heading(campos[1], text= campos[1])
    treeview.heading(campos[2], text= campos[2])
    treeview.heading(campos[3], text= campos[3])
    treeview.column('#0', width= 0)
    treeview.column(campos[0], width= 50, anchor= 'e')
    treeview.column(campos[1], width= 400, anchor= 'center')
    treeview.column(campos[2], width= 80, anchor= 'center')
    treeview.column(campos[3], width= 80, anchor= 'center')
    
    vsb = ttk.Scrollbar(toplevel, orient= "vertical", command= treeview.yview)
    treeview.configure(yscrollcommand=vsb.set)
    vsb.pack(side= 'right', fill= 'y')
    treeview.pack(fill= 'both', expand= True)
    
    Treeview_Select(self, treeview)
    
def Treeview_Select(self, treeview):
    from Banco_de_Dados.Inventario_Conn import Connect
    self.dist_saldo_list = []
    query = "select l.cdpro, p.nmpro, sum(iif(l.TPMOV = 'S', l.quant, -l.quant)) as saldo_lan, p.saldo as saldo_pro, iif(sum(iif(l.TPMOV = 'S', l.quant, -l.quant)) <> p.saldo, 'S', 'N') as distorcao  from in01lan l left join in01pro p on l.cdpro = p.cdpro where p.classificacao_produto in ('00','01', '02', '03', '04', '05', '06') group by l.cdpro, p.saldo, p.nmpro"
    Connect.cursor.execute(query)
    rows = Connect.cursor.fetchall()
    for row in rows:
        cdpro, nmpro, saldo_lan, saldo_pro, distorcao = row
        if distorcao == 'S':
            self.dist_saldo_list.append([cdpro, nmpro, saldo_lan, saldo_pro])
    Treeview_Insert(treeview, self.dist_saldo_list)
    
def Treeview_Insert(treeview, rows):
    for row in rows:
        treeview.insert('', 'end', values= row)
