import Thread_Manager.Gerenciador_Thread_BD as Gerenciador_Thread_BD

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
    def __init__(self):
        self.__thread_manager = Gerenciador_Thread_BD.GerenciadorThreadBD(
            self._conectar)

    def _conectar(self):
        return fdb.connect(  # Cria a conexão
            host=Dados.banco_dados['host'],  # Informa o host
            port=int(Dados.banco_dados['port']),  # Informa a porta
            # Informa o caminho do banco de dados
            database=Dados.banco_dados['database'],
            # Informa o caminho da fbclient
            fb_library_name=Dados.banco_dados['fbclient'],
            user='SYSDBA',  # Informa o usuário
            password='masterkey',  # Informa a senha
            charset='WIN1252'
        )

    def gerenciador(self):
        return self.__thread_manager
