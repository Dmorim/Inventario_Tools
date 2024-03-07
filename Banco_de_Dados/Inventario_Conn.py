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
        if cls.conn is not None and not cls.conn.closed:
            cls.conn.close()
            
        cls.conn = fdb.connect(
            host= Dados.banco_dados['host'],
            port= int(Dados.banco_dados['port']),
            database= Dados.banco_dados['database'],
            fb_library_name= Dados.banco_dados['fbclient'],
            user= 'SYSDBA',
            password= 'masterkey'
        )
        cls.cursor = cls.conn.cursor()
        