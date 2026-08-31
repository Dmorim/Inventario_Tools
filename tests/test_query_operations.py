import pytest
from fdb import DatabaseError

from Thread_Manager.Query_Operations import query_selector, query_updater


class TestQuerySelector:
    def test_executa_e_retorna_linhas(self, conexao_fake_com_linhas):
        resultado = query_selector(conexao_fake_com_linhas, "SELECT * FROM in01pro")
        assert resultado == [(1, 'produto A'), (2, 'produto B')]

    def test_registra_consulta(self, conexao_fake):
        query_selector(conexao_fake, "SELECT * FROM in01pro")
        assert conexao_fake._cursor.executed == "SELECT * FROM in01pro"

    def test_consulta_com_params(self, conexao_fake):
        query = "SELECT * FROM in01pro WHERE cdpro = ?"
        params = (123,)
        query_selector(conexao_fake, query, params)
        assert conexao_fake._cursor.params == params

    def test_sem_linhas_retorna_lista_vazia(self, conexao_fake):
        assert query_selector(conexao_fake, "SELECT * FROM in01pro") == []

    def test_fecha_cursor_apos_busca(self, conexao_fake):
        cursor = conexao_fake._cursor
        closed = False
        def track_close():
            nonlocal closed
            closed = True
        cursor.close = track_close
        query_selector(conexao_fake, "SELECT 1")
        assert closed is True

    def test_erro_database_envolve_mensagem(self, conexao_fake):
        def falhar(query, params=None):
            raise DatabaseError("erro original")
        conexao_fake._cursor.execute = falhar
        with pytest.raises(DatabaseError) as exc:
            query_selector(conexao_fake, "SELECT * FROM in01pro")
        assert "Erro ao gerar o select" in str(exc.value)


class TestQueryUpdater:
    def test_executa_e_commit(self, conexao_fake):
        query_updater(conexao_fake, "UPDATE in01pro SET precu = ?", (1.5,))
        assert conexao_fake.commits == 1
        assert conexao_fake.rollbacks == 0

    def test_registra_consulta_e_params(self, conexao_fake):
        query = "UPDATE in01pro SET precu = ?"
        params = (1.5,)
        query_updater(conexao_fake, query, params)
        assert conexao_fake._cursor.executed == query
        assert conexao_fake._cursor.params == params

    def test_erro_faz_rollback(self, conexao_fake):
        def falhar(query, params=None):
            raise DatabaseError("erro original")
        conexao_fake._cursor.execute = falhar
        with pytest.raises(DatabaseError):
            query_updater(conexao_fake, "UPDATE in01pro SET precu = ?", (1.5,))
        assert conexao_fake.rollbacks == 1
        assert conexao_fake.commits == 0

    def test_sucesso_nao_chama_rollback(self, conexao_fake):
        query_updater(conexao_fake, "UPDATE in01pro SET precu = ?", (1.5,))
        assert conexao_fake.rollbacks == 0
