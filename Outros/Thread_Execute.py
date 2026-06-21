from Banco_de_Dados.Conexao_Banco_Dados.Inventario_Conn import BancoDeDados


class QueryExecutor:
    def __init__(self):
        pass

    @staticmethod
    def query_executor(funcao, query):
        gerenciador = BancoDeDados.gerenciador()
        gerenciador.executar(funcao, query)
