from fdb import DatabaseError

from Banco_de_Dados.Conexao_Banco_Dados.Inventario_Conn import BancoDeDados


def query_selector(conexao, query, params=None):
    try:
        cursor = conexao.cursor()
        cursor.execute(query, params)
        return cursor.fetchall()
    except DatabaseError as e:
        raise DatabaseError(f"Erro ao gerar o select: {e}")
    finally:
        if 'cursor' in locals():
            cursor.close()


def query_updater(conexao, query, params=None):
    try:
        cursor = conexao.cursor()
        cursor.execute(query, params)
        conexao.commit()
        return
    except DatabaseError as e:
        conexao.rollback()
        raise DatabaseError(f"Erro ao gerar a operação: {e}")
    finally:
        if 'cursor' in locals():
            cursor.close()


def query_executor(funcao, query, params=None):
    gerenciador = BancoDeDados.gerenciador()
    return gerenciador.executar(funcao, query, params)
