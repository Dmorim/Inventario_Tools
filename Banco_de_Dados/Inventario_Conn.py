import fdb

# Classe para armazenar os dados de conexão informados pelo usuário
class Dados:
    banco_dados = {
        'host': '',
        'port': '',
        'database': '',
        'fbclient': ''
    }

# Classe para realizar a conexão com o banco de dados    
class Connect:
    conn = None # Variável para armazenar a conexão
    cursor = None # Variável para armazenar o cursor
    @classmethod
    def fdb_conn(cls):
        if cls.conn is not None and not cls.conn.closed: # Verifica se a conexão já foi criada e se está aberta
            cls.conn.close() # Fecha a conexão
            
        cls.conn = fdb.connect( # Cria a conexão
            host= Dados.banco_dados['host'], # Informa o host
            port= int(Dados.banco_dados['port']), # Informa a porta
            database= Dados.banco_dados['database'], # Informa o caminho do banco de dados
            fb_library_name= Dados.banco_dados['fbclient'], # Informa o caminho da fbclient
            user= 'SYSDBA', # Informa o usuário
            password= 'masterkey' # Informa a senha
        )
        cls.cursor = cls.conn.cursor() # Cria o cursor
        