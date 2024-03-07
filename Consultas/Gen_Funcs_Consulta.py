def prod_get(query_input: str):
    # Função que executa a query de valor de produto e retorna o valor obtido
    # Args:
        # query_input: Query que será executada no banco de dados
    from Banco_de_Dados.Inventario_Conn import Connect # Importa a conexão com o banco de dados
    from fdb import DatabaseError # Importa a exceção que será usada para tratar erros no banco de dados
    
    try:
        Connect.cursor.execute(query_input) # Executa a query
        val = Connect.cursor.fetchone()[0] # Pega o  primeiro valor obtido
    except DatabaseError as e:
        # Se ocorrer um erro ao acessar o banco de dados, mostra uma mensagem de erro
        from tkinter import messagebox
        messagebox.showerror('Erro', f'Erro ao acessar o banco de dados\n {e}')
        
    return val # Retorna o valor obtido

def copy_val(val_ven_text):
    # Mesmo funcionamento explicado em Consultas/Consultas_Val_Ven_Func.py
    import pyperclip
    copy_text = val_ven_text.cget('text')
    pyperclip.copy(copy_text)
    
def event_button_consulta(self, event):
    # Função que simula um click no botão de consulta
    # Args:
        # self: Instância da classe que chama a função
        # event: Evento que chama a função
        
    if self.consulta.cget('state') != 'disabled':
        self.consulta.invoke()
        
def event_button_comando(self, event):
    # Função que simula um click no botão de comando
    # Args:
        # self: Instância da classe que chama a função
        # event: Evento que chama a função
        
    if self.comando.cget('state') != 'disabled':
        self.comando.invoke()