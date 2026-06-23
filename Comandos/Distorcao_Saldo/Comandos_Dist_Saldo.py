def on_click_dist_saldo(self, parent):
    # Função chamada ao apertar o botão de distorção de saldo, cria a tela de distorção de saldo
    # Args:
    # self: objeto da classe
    # parent: janela do tkinter

    # Importações de bibliotecas externas
    import customtkinter as ctk
    from datetime import datetime
    from tkcalendar import DateEntry

    # Importação da função update_executor do arquivo Thread_Manager/Thread_Executor.py

    # Cria a janela distorcao como um Toplevel do parent
    distorcao = ctk.CTkToplevel(parent)
    distorcao.geometry("330x120+150+135")
    distorcao.title("Distorção de Saldo")
    distorcao.resizable(False, False)
    distorcao.transient(parent)
    distorcao.focus_set()
    distorcao.grab_set()

    # Criação dos widgets da tela da janela distorcao
    tipo_distorc_label = ctk.CTkLabel(
        distorcao, text='Tipo de Distorção', font=('verdana', 12, 'bold'))
    tipo_distorc_cbb = ctk.CTkComboBox(distorcao, font=(
        'verdana', 12, 'bold'), width=140, state='readonly', values=['LAN = PRO', 'PRO = LAN'])
    data_label = ctk.CTkLabel(
        distorcao, text='Data da Modificação', font=('verdana', 12, 'bold'))
    data_entry = DateEntry(distorcao, font=('verdana', 11), width=10, background='darkblue',
                           foreground='white', borderwidth=2, format='dd/mm/yyyy', firstweekday='sunday')

    # Criação dos botões confirmar e cancelar
    confirm_button = ctk.CTkButton(distorcao, text='Confirmar', width=60, height=26,
                                   command=lambda: on_click_confirm_btt(self, distorcao, val_list, confirm_button))
    cancel_button = ctk.CTkButton(
        distorcao, text='Cancelar', width=75, height=26, command=lambda: distorcao.destroy())

    # Cria uma lista com os valores dos combobox e entry
    val_list = [tipo_distorc_cbb, data_entry]

    # Seta o valor padrão do combobox e da data
    tipo_distorc_cbb.set('LAN = PRO')
    today_date = datetime.now().strftime("%d/%m/%Y")
    data_entry.set_date(today_date)

    # Posicionamento dos widgets
    tipo_distorc_label.place(x=5, y=5)
    tipo_distorc_cbb.place(x=5, y=40)
    data_label.place(x=160, y=5)
    data_entry.place(x=160, y=42)

    # Posicionamento dos botões confirmar e cancelar
    confirm_button.place(x=255, y=90)
    cancel_button.place(x=175, y=90)


def on_click_confirm_btt(self, parent, val_list, confirm_button):
    # Função chamada ao apertar o botão de confirmar, executa a distorção de saldo
    # Args:
    # self: objeto da classe
    # parent: janela do tkinter
    # val_list: lista de valores da aba distorção de saldo

    from datetime import datetime  # Importa a classe datetime
    from tkinter import messagebox  # Importa a classe messagebox do tkinter

    from Thread_Manager.Query_Operations import query_updater, query_executor
    from Thread_Manager.Thread_Executor import thread_execução

    def executa_distorcao():
        tp_distorc = val_list[0].get()
        if tp_distorc == 'PRO = LAN':  # Verifica se a distorção é PRO = LAN
            for item in self.dist_saldo_list:  # Para cada item na lista de distorção de saldo
                # Cria a query de distorção de saldo, deixando o saldo do produto igual ao saldo do lançamento, onde o código do produto é informado na lista
                query = f"UPDATE IN01PRO SET SALDO = {item[2]} WHERE CDPRO = {item[0]}"
                query_executor(query_updater, query)  # Executa a query
        else:
            for item in self.dist_saldo_list:  # Para cada item na lista de distorção de saldo"
                # Define o tipo de movimento como N se o saldo do produto for maior que o saldo do lançamento, caso contrário, define como S
                tpmov = 'N' if item[2] > item[3] else 'S'
                quant = abs(item[2] - item[3])
                data = datetime.strptime(
                    val_list[1].get(), "%d/%m/%Y").strftime("%d.%m.%Y")
                nmpro = item[1].replace("'", "")
                # Cria a query de distorção de saldo, inserindo um novo lançamento no banco de dados
                query = f"INSERT INTO IN01LAN (NOTFI, CDPRO, VENDA, DTEMI, DTPRO, QUANT, TPMOV, HISTO, NMOPE, DTOPE, HISTORICO_AJUSTE) VALUES ('AJUSTE', '{item[0]}', 'J', '{data}', '{data}', '{quant}', '{tpmov}', 'AJUSTE DE ESTOQUE (DISTORÇÃO DE SALDO)', 'SISTECH', '{data}', 'AJUSTADO LANÇAMENTO {item[0]} - {nmpro}, DISTORÇÃO DE SALDO, AJUSTADO POR SISTECH')"

                query_executor(query_updater, query)  # Executa a query

    def update_finalizado(_):
        messagebox.showinfo(
            'Aviso', 'Distorção de Saldo executada com sucesso', parent=parent)
        parent.destroy()  # Fecha a janela de distorção de saldo

    def update_erro(erro):
        messagebox.showerror(
            'Erro', f'Ocorreu um erro ao executar a distorção de saldo\n{erro}', parent=parent)
        # Habilita o botão de confirmar novamente
        confirm_button.configure(state='normal')

    # Desabilita o botão de confirmar para evitar múltiplos cliques
    confirm_button.configure(state='disabled')

    thread_execução(parent, executa_distorcao, update_finalizado, update_erro)
