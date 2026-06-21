
class Query_Select:
    def __init__(self):
        pass

    @staticmethod
    def query_selector(conexao, query):
        cursor = conexao.cursor()
        cursor.execute(query)
        return cursor.fetchall()
