def on_click_dist_saldo(self, parent):
    import customtkinter as ctk
    from tkcalendar import DateEntry
    
    distorcao = ctk.CTkToplevel(parent)
    distorcao.geometry("330x120+150+135")
    distorcao.title("Distorção de Saldo")
    distorcao.resizable(False, False)
    distorcao.transient(parent)
    distorcao.focus_set()
    distorcao.grab_set()
    
    tipo_distorc_label = ctk.CTkLabel(distorcao, text= 'Tipo de Distorção', font= ('verdana', 12, 'bold'))
    tipo_distorc_cbb = ctk.CTkComboBox(distorcao, font= ('verdana', 12, 'bold'), width= 140, state= 'readonly', values= ['LAN = PRO', 'PRO = LAN'])
    data_label = ctk.CTkLabel(distorcao, text= 'Data da Modificação', font= ('verdana', 12, 'bold'))
    data_entry = DateEntry(distorcao, font= ('verdana', 11), width= 10, background= 'darkblue', foreground= 'white', borderwidth= 2, format= 'dd/mm/yyyy', firstweekday= 'sunday')
    
    confirm_button = ctk.CTkButton(distorcao, text= 'Confirmar', width= 60, height= 26, command= lambda: on_click_confirm_btt(self, distorcao, val_list))
    cancel_button = ctk.CTkButton(distorcao, text= 'Cancelar', width= 75, height= 26, command= lambda: distorcao.destroy())
    
    val_list = [tipo_distorc_cbb, data_entry]
    tipo_distorc_cbb.set('LAN = PRO')
    
    tipo_distorc_label.place(x= 5, y= 5)
    tipo_distorc_cbb.place(x= 5, y= 40)
    data_label.place(x= 160, y= 5)
    data_entry.place(x= 160, y= 42)
    
    confirm_button.place(x= 255, y= 90)
    cancel_button.place(x= 175, y= 90)
    
def on_click_confirm_btt(self, parent, val_list):
    from Banco_de_Dados.Inventario_Conn import Connect
    from datetime import datetime
    from tkinter import messagebox
    
    tp_distorc = val_list[0].get()
    data = val_list[1].get()
    data = datetime.strptime(data, "%d/%m/%Y")
    data = data.strftime("%d.%m.%Y")
    
    if tp_distorc == 'PRO = LAN':
        for item in self.dist_saldo_list:
            query = f"UPDATE IN01PRO SET SALDO = {item[2]} WHERE CDPRO = {item[0]}"
            
            try:
                Connect.cursor.execute(query)
                Connect.conn.commit()
            except Exception as e:
                messagebox.showerror('Erro', f'Erro ao executar a distorção\n{e}', parent= parent)
                return
            
        messagebox.showinfo('Aviso', 'Distorção de Saldo executada com sucesso', parent= parent) 
        parent.destroy()
    
    else:
        for item in self.dist_saldo_list:
            if item[2] > item[3]:
               tpmov = 'N'
               quant = item[2] - item[3]  
                         
            if item[2] < item[3]:
                tpmov = 'S'
                quant = item[3] - item[2]
            
            nmpro = item[1]
            nmpro = nmpro.replace("'", "")
            
            query = f"INSERT INTO IN01LAN (NOTFI, CDPRO, VENDA, DTEMI, DTPRO, QUANT, TPMOV, HISTO, NMOPE, DTOPE, HISTORICO_AJUSTE) VALUES ('AJUSTE', '{item[0]}', 'J', '{data}', '{data}', '{quant}', '{tpmov}', 'AJUSTE DE ESTOQUE (DISTORÇÃO DE SALDO)', 'SISTECH', '{data}', 'AJUSTADO LANÇAMENTO {item[0]} - {nmpro}, DISTORÇÃO DE SALDO, AJUSTADO POR SISTECH')"
            
            try:
                Connect.cursor.execute(query)
                Connect.conn.commit()
            except Exception as e:
                messagebox.showerror('Erro', f'Erro ao executar a distorção\n{e}', parent= parent)
                return
                 
        messagebox.showinfo('Aviso', 'Distorção de Saldo executada com sucesso', parent= parent)   
        parent.destroy()