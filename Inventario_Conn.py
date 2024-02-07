import fdb

class Dados:
    banco_dados = {
        'host': '',
        'port': '',
        'database': '',
        'fbclient': ''
    }
    
class Connect:
    conn = None
    cursor = None
    @classmethod
    def fdb_conn(cls):
        if cls.conn is not None:
            cls.conn.close()
        try:
            cls.conn = fdb.connect(
                host= Dados.banco_dados['host'],
                port= int(Dados.banco_dados['port']),
                database= Dados.banco_dados['database'],
                fb_library_name= Dados.banco_dados['fbclient'],
                user= 'SYSDBA',
                password= 'masterkey'
            )
        except (fdb.DatabaseError, TypeError) as e:
            from tkinter import messagebox
            messagebox.showerror('Erro de Conexão', f'Não foi possível conectar ao banco de dados \n {e}')
        cls.cursor = cls.conn.cursor()
    