import fdb
from Outros.Logger.Get_Logger import get_logger
from Thread_Manager.Gerenciador_Thread_BD import GerenciadorThreadBD

logger = get_logger(__name__)


class ConfiguracaoBanco:
    """Guarda os dados de conexão informados pelo usuário na tela."""
    host = ''
    port = ''
    database = ''
    fbclient = ''
    user = ''
    password = ''

    @classmethod
    def definir(cls, host, port: int | None, database, fbclient, user, password):
        cls.host = host
        cls.port = port
        cls.database = database
        cls.fbclient = fbclient
        cls.user = user
        cls.password = password


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
            logger.debug(
                'Pool de conexões já existente; reutilizando conexão atual.')
            return cls._gerenciador  # idempotente — já existe, não recria

        logger.info('Inicializando pool de conexões do banco de dados.')
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
            logger.info('Encerrando pool de conexões do banco.')
            cls._gerenciador.fechar()
            cls._gerenciador = None

    @classmethod
    def retorna_gerenciador(cls):
        return cls._gerenciador
