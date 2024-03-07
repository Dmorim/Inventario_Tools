def dist_saldo_screen(self, Consulta_Screen):
       import customtkinter as ctk
       from Consultas.Consultas_Val_Screen import Consultas_Val_Screen
       from Consultas.Gen_Funcs_Consulta import prod_get, copy_val
       from Consultas.Consultas_Dist_Saldo_List import List_Treeview_Screen
    
       hub = Consultas_Val_Screen(Consulta_Screen, 'Saldo de Estoque')             
       execute_query(self)
       
       val_ven_label = ctk.CTkLabel(hub, text= 'Distorções de Saldo:', width= 20, height= 2, font= ('', 16))
       val_ven_text = ctk.CTkLabel(hub, text= len(self.dist_saldo_list), width= 20, height= 2, font= ('', 14))
       val_ven_button = ctk.CTkButton(hub, text= 'Copiar Valor', width= 15, height= 20, command= lambda: copy_val(val_ven_text))
       listagem_buttn = ctk.CTkButton(hub, text= 'Listar Produtos', width= 15, height= 20, command= lambda: List_Treeview_Screen(self, hub))

       val_ven_label.place(relx= 0.5, y= 15, anchor= 'center')
       val_ven_text.place(relx= 0.5, y= 40, anchor= 'center')
       val_ven_button.place(relx= 0.8, y= 65, anchor= 'center')
       listagem_buttn.place(relx= 0.24, y= 65, anchor= 'center')
       
def execute_query(self):
       from Banco_de_Dados.Inventario_Conn import Connect
       query_casa_dec = "select valor from si01gp where ident = 'FORMATOSALDO'"
       Connect.cursor.execute(query_casa_dec)
       casa_dec = Connect.cursor.fetchone()[0]
       casa_dec = casa_dec.split('.')[1]
       casa_dec = len(casa_dec)
       
       query = f"""
       select p.cdpro,
       p.nmpro,
       cast(sum(iif(l.TPMOV = 'S', l.quant, -l.quant)) as numeric(15,{casa_dec})) as saldo_lan,
       p.saldo as saldo_pro,
       iif(cast(sum(iif(l.TPMOV = 'S', l.quant, -l.quant)) as numeric(15,{casa_dec})) <> cast(p.saldo as numeric (15,3)), 'S', 'N') as distorcao
       from in01lan l left join in01pro p on l.cdpro = p.cdpro
       left join in01com c on c.notfi = l.notfi and c.cdfrn = l.cdfrn and c.serie = l.serie
       where coalesce(l.controlaestoque, 'S') = 'S'
       and coalesce(l.cance,  'N') = 'N'
       and classificacao_produto in ('00', '01', '02', '04', '05', '06')
       and l.venda <> 'R'
       and coalesce(c.alterarsaldo, 'S') = 'S'
       group by p.cdpro, p.saldo, p.nmpro
       """
       self.dist_saldo_list = []
       Connect.cursor.execute(query)
       rows = Connect.cursor.fetchall()
       for row in rows:
              cdpro, nmpro, saldo_lan, saldo_pro, distorcao = row
              if distorcao == 'S':
                     self.dist_saldo_list.append([cdpro, nmpro, saldo_lan, saldo_pro])
                     