import fdb
from Thread_Manager.Gerenciador_Thread_BD import GerenciadorThreadBD


class ConfiguracaoBanco:
    """Guarda os dados de conexão informados pelo usuário na tela."""
    host = ''
    port = ''
    database = ''
    fbclient = ''
    user = ''
    password = ''

    @classmethod
    def definir(cls, host, port, database, fbclient, user, password):
        cls.host = host
        cls.port = port
        cls.database = database
        cls.fbclient = fbclient
        cls.user = user
        cls.password = password

    @property
    def host(self):
        return self.host

    @property
    def port(self):
        try:
            return int(self.port)
        except (ValueError, TypeError):
            return None

    @property
    def database(self):
        return self.database

    @property
    def fbclient(self):
        return self.fbclient

    @property
    def user(self):
        return self.user

    @property
    def password(self):
        return self.password


class BancoDeDados:
    """
    Ponto único de acesso ao banco de dados.
    Nunca é instanciada (sem __init__, sem BancoDeDados()) — todo
    estado vive em atributos de classe, e os métodos são classmethods.
    """
    _gerenciador = None  # único pool da aplicação inteira

    @classmethod
    def conectar(cls):
        """Cria o pool uma única vez. Chamadas seguintes reaproveitam."""
        if cls._gerenciador is not None:
            return cls._gerenciador  # idempotente — já existe, não recria

        cls._gerenciador = GerenciadorThreadBD(cls._criar_conexao)
        return cls._gerenciador

    @staticmethod
    def _criar_conexao():
        return fdb.connect(
            host=ConfiguracaoBanco.host,
            port=ConfiguracaoBanco.port,
            database=ConfiguracaoBanco.database,
            fb_library_name=ConfiguracaoBanco.fbclient,
            user=ConfiguracaoBanco.user,
            password=ConfiguracaoBanco.password,
            charset='WIN1252'
        )

    @classmethod
    def gerenciador(cls):
        """Acesso ao pool em qualquer parte do sistema."""
        if cls._gerenciador is None:
            raise RuntimeError(
                'Banco ainda não conectado — chame BancoDeDados.conectar() primeiro.'
            )
        return cls._gerenciador

    @classmethod
    def executar(cls, funcao, *args, **kwargs):
        """Atalho: evita escrever BancoDeDados.gerenciador().executar(...) toda vez."""
        return cls.gerenciador().executar(funcao, *args, **kwargs)

    @classmethod
    def fechar(cls):
        if cls._gerenciador is not None:
            cls._gerenciador.fechar()
            cls._gerenciador = None

    @classmethod
    def retorna_gerenciador(cls):
        return cls._gerenciador
