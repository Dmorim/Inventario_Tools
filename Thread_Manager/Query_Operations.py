from Banco_de_Dados.Conexao_Banco_Dados.Inventario_Conn import BancoDeDados


def query_selector(conexao, query):
    cursor = conexao.cursor()
    cursor.execute(query)
    return cursor.fetchall()


def query_updater(conexao, query):
    cursor = conexao.cursor()
    cursor.execute(query)
    conexao.commit()


def query_executor(funcao, query):
    gerenciador = BancoDeDados.gerenciador()
    gerenciador.executar(funcao, query)
