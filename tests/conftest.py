import sys
from pathlib import Path

import pytest

# Garante que a raiz do projeto esteja no sys.path para os imports (ex.: Banco_de_Dados, ...)
RAIZ = Path(__file__).resolve().parent.parent
if str(RAIZ) not in sys.path:
    sys.path.insert(0, str(RAIZ))


class FakeCursor:
    """Cursor fake que registra a query executada e devolve linhas pré-configuradas."""

    def __init__(self, rows=None):
        self._rows = rows or []
        self.executed = None
        self.params = None

    def execute(self, query, params=None):
        self.executed = query
        self.params = params
        return self

    def fetchall(self):
        return self._rows

    def close(self):
        pass


class FakeConexao:
    """Conexão fake que registra o último cursor e o estado de commit/rollback."""

    def __init__(self, rows=None):
        self._cursor = FakeCursor(rows)
        self.commits = 0
        self.rollbacks = 0

    def cursor(self):
        return self._cursor

    def commit(self):
        self.commits += 1

    def rollback(self):
        self.rollbacks += 1

    def close(self):
        pass


@pytest.fixture
def conexao_fake():
    """Retorna uma FakeConexao para testar query_selector/query_updater."""
    return FakeConexao()


@pytest.fixture
def conexao_fake_com_linhas():
    """Retorna uma FakeConexao com linhas pré-definidas para buscas."""
    return FakeConexao(rows=[(1, 'produto A'), (2, 'produto B')])
