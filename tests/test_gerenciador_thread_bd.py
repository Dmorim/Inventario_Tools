from Thread_Manager.Gerenciador_Thread_BD import GerenciadorThreadBD


class FakeCursor:
    def __init__(self, falha=False):
        self.falha = falha
        self.executed = []
        self.closed = False

    def execute(self, query):
        if self.falha:
            raise RuntimeError('conexão stale')
        self.executed.append(query)

    def close(self):
        self.closed = True


class FakeConexao:
    def __init__(self, falha=False):
        self.closed = False
        self.cursor_fake = FakeCursor(falha)

    def cursor(self):
        return self.cursor_fake

    def close(self):
        self.closed = True


def test_health_check_executa_ping_firebird():
    conexao = FakeConexao()
    gerenciador = GerenciadorThreadBD(
        lambda: FakeConexao(), minimo=1, maximo=1)

    assert gerenciador._conexao_valida(conexao) is True
    assert conexao.cursor_fake.executed == ['SELECT 1 FROM RDB$DATABASE']
    assert conexao.cursor_fake.closed is True


def test_pegar_substitui_conexao_stale():
    conexao_stale = FakeConexao(falha=True)
    conexao_nova = FakeConexao()
    criadas = iter([conexao_stale, conexao_nova])
    gerenciador = GerenciadorThreadBD(
        lambda: next(criadas), minimo=1, maximo=1)

    assert gerenciador._pegar_conexao(
        timeout=0.01, tentativas=0) is conexao_nova
    assert conexao_stale.closed is True


def test_health_check_falho_na_devolucao_repoe_pool():
    conexao_stale = FakeConexao(falha=True)
    conexao_nova = FakeConexao()
    criadas = iter([conexao_nova])
    gerenciador = GerenciadorThreadBD(
        lambda: next(criadas), minimo=1, maximo=1)

    gerenciador._devolver_conexao(conexao_stale)

    assert conexao_stale.closed is True
    assert gerenciador._pegar_conexao(
        timeout=0.01, tentativas=0) is conexao_nova
