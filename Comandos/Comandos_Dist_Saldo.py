def on_click_dist_saldo(self, parent):
    # Função chamada ao apertar o botão de distorção de saldo, cria a tela de distorção de saldo
    # Args:
        # self: objeto da classe
        # parent: janela do tkinter
        
    # Importações de bibliotecas externas
    import customtkinter as ctk
    from datetime import datetime
    from tkcalendar import DateEntry
    
    distorcao = ctk.CTkToplevel(parent) # Cria a janela distorcao como um Toplevel do parent
    distorcao.geometry("330x120+150+135")
    distorcao.title("Distorção de Saldo")
    distorcao.resizable(False, False)
    distorcao.transient(parent)
    distorcao.focus_set()
    distorcao.grab_set()
    
    # Criação dos widgets da tela da janela distorcao
    tipo_distorc_label = ctk.CTkLabel(distorcao, text= 'Tipo de Distorção', font= ('verdana', 12, 'bold'))
    tipo_distorc_cbb = ctk.CTkComboBox(distorcao, font= ('verdana', 12, 'bold'), width= 140, state= 'readonly', values= ['LAN = PRO', 'PRO = LAN'])
    data_label = ctk.CTkLabel(distorcao, text= 'Data da Modificação', font= ('verdana', 12, 'bold'))
    data_entry = DateEntry(distorcao, font= ('verdana', 11), width= 10, background= 'darkblue', foreground= 'white', borderwidth= 2, format= 'dd/mm/yyyy', firstweekday= 'sunday')
    
    # Criação dos botões confirmar e cancelar
    confirm_button = ctk.CTkButton(distorcao, text= 'Confirmar', width= 60, height= 26, command= lambda: on_click_confirm_btt(self, distorcao, val_list))
    cancel_button = ctk.CTkButton(distorcao, text= 'Cancelar', width= 75, height= 26, command= lambda: distorcao.destroy())
    
    # Cria uma lista com os valores dos combobox e entry
    val_list = [tipo_distorc_cbb, data_entry]
    
    # Seta o valor padrão do combobox e da data
    tipo_distorc_cbb.set('LAN = PRO')
    today_date = datetime.now().strftime("%d/%m/%Y")
    data_entry.set_date(today_date)
    
    # Posicionamento dos widgets
    tipo_distorc_label.place(x= 5, y= 5)
    tipo_distorc_cbb.place(x= 5, y= 40)
    data_label.place(x= 160, y= 5)
    data_entry.place(x= 160, y= 42)
    
    # Posicionamento dos botões confirmar e cancelar
    confirm_button.place(x= 255, y= 90)
    cancel_button.place(x= 175, y= 90)
    
def on_click_confirm_btt(self, parent, val_list):
    # Função chamada ao apertar o botão de confirmar, executa a distorção de saldo
    # Args:
        # self: objeto da classe
        # parent: janela do tkinter
        # val_list: lista de valores da aba distorção de saldo
    
    from Banco_de_Dados.Inventario_Conn import Connect # Importa a classe Connect do arquivo Inventario_Conn
    
    from datetime import datetime # Importa a classe datetime
    from tkinter import messagebox # Importa a classe messagebox do tkinter
    
    # Obtem os valores de tipo de distorção e data
    tp_distorc = val_list[0].get()
    data = val_list[1].get()
    data = datetime.strptime(data, "%d/%m/%Y")
    data = data.strftime("%d.%m.%Y") # Formata a data para o formato do banco de dados
    
    if tp_distorc == 'PRO = LAN': # Verifica se a distorção é PRO = LAN
        for item in self.dist_saldo_list: # Para cada item na lista de distorção de saldo
            query = f"UPDATE IN01PRO SET SALDO = {item[2]} WHERE CDPRO = {item[0]}" # Cria a query de distorção de saldo, deixando o saldo do produto igual ao saldo do lançamento, onde o código do produto é informado na lista
            
            try:
                Connect.cursor.execute(query) # Executa a query
                Connect.conn.commit() # Commita a transação
            except Exception as e:
                # Cria uma messagebox informando que houve um erro ao executar a distorção
                messagebox.showerror('Erro', f'Erro ao executar a distorção\n{e}', parent= parent)
                return
            
        # Cria uma messagebox informando que a distorção foi executada com sucesso
        messagebox.showinfo('Aviso', 'Distorção de Saldo executada com sucesso', parent= parent) 
        parent.destroy()
    
    else:
        # Caso a distorção seja LAN = PRO
        for item in self.dist_saldo_list: # Para cada item na lista de distorção de saldo
            
            # Verifica se o saldo do lançamento é maior ou menor que o saldo do produto
            if item[2] > item[3]:
               tpmov = 'N' # Se for maior, o tipo de movimento é N, categorizando uma saída
               quant = item[2] - item[3]
                         
            if item[2] < item[3]:
                tpmov = 'S' # Se for menor, o tipo de movimento é S, categorizando uma entrada
                quant = item[3] - item[2]
            
            nmpro = item[1] # Preenche a variável nmpro com o nome do produto
            nmpro = nmpro.replace("'", "") # Remove as aspas simples do nome do produto para evitar erro na query
            
            # Cria a query de distorção de saldo, inserindo um novo lançamento no banco de dados
            query = f"INSERT INTO IN01LAN (NOTFI, CDPRO, VENDA, DTEMI, DTPRO, QUANT, TPMOV, HISTO, NMOPE, DTOPE, HISTORICO_AJUSTE) VALUES ('AJUSTE', '{item[0]}', 'J', '{data}', '{data}', '{quant}', '{tpmov}', 'AJUSTE DE ESTOQUE (DISTORÇÃO DE SALDO)', 'SISTECH', '{data}', 'AJUSTADO LANÇAMENTO {item[0]} - {nmpro}, DISTORÇÃO DE SALDO, AJUSTADO POR SISTECH')"
            
            try:
                Connect.cursor.execute(query) # Executa a query
                Connect.conn.commit() # Commita a transação
            except Exception as e:
                # Mesmo tratamento de erro da query anterior
                messagebox.showerror('Erro', f'Erro ao executar a distorção\n{e}', parent= parent)
                return
                 
        messagebox.showinfo('Aviso', 'Distorção de Saldo executada com sucesso', parent= parent) # Cria uma messagebox informando que a distorção foi executada com sucesso
        parent.destroy() # Fecha a janela de distorção de saldo