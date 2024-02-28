import datetime
def date_treat(self, var, cond: str):
    data = var.get()
    data = data.replace('/', '')
    if len(data) != 8:
        return
    if len(data) == 8 or len(data) == 10:  
        try:
            data_str = datetime.datetime.strptime(data, "%d%m%Y")
            data_formatada = data_str.strftime("%d/%m/%Y")
        except ValueError:
            from tkinter import messagebox
            messagebox.showerror('Erro', 'Data inválida')
            return
    
    if len(data) > 10:
        data = data[:10]
        data = datetime.datetime.strptime(data, "%d/%m/%Y")
        data_formatada = data.strftime("%d/%m/%Y")
    
    var.set(data_formatada)
    if cond == 'Inicial':
        data_select_ini(self, var)
    elif cond == 'Final':
        data_select_fim(self, var)
    
def data_select_ini(self, var_inicial):
    data = var_inicial.get()
    data = datetime.datetime.strptime(data, "%d/%m/%Y")
    data = data.strftime("%d.%m.%Y")
    self.data_banco_inicial = data


def data_select_fim(self, var_final):
    data = var_final.get()
    data = datetime.datetime.strptime(data, "%d/%m/%Y")
    data = data.strftime("%d.%m.%Y")
    self.data_banco_final = data