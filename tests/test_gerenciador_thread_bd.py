import pytest

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


def test_pegar_conexao_recusa_quando_gerenciador_fechando():
    gerenciador = GerenciadorThreadBD(
        lambda: FakeConexao(), minimo=1, maximo=1)
    gerenciador._fechando = True

    with pytest.raises(RuntimeError):
        gerenciador._pegar_conexao(timeout=0.01, tentativas=0)


def test_pegar_conexao_recusa_se_fechamento_ocorrer_no_descarte():
    conexao = FakeConexao()
    gerenciador = GerenciadorThreadBD(
        lambda: conexao, minimo=1, maximo=1)

    def valida(_):
        gerenciador._fechando = True
        return False

    gerenciador._conexao_valida = valida

    with pytest.raises(RuntimeError):
        gerenciador._pegar_conexao(timeout=0.01, tentativas=0)
    assert conexao.closed is True


def test_executar_recusa_quando_gerenciador_fechando():
    gerenciador = GerenciadorThreadBD(
        lambda: FakeConexao(), minimo=1, maximo=1)
    chamadas = []
    gerenciador._fechando = True

    with pytest.raises(RuntimeError):
        gerenciador.executar(lambda conexao: chamadas.append(conexao))
    assert chamadas == []


def test_executar_propaga_erro_e_zera_operacoes_ativas():
    gerenciador = GerenciadorThreadBD(
        lambda: FakeConexao(), minimo=1, maximo=1)

    def falhar(_):
        raise ValueError('falha na operação')

    with pytest.raises(ValueError):
        gerenciador.executar(falhar)
    assert gerenciador._operacoes_ativas == 0


def test_executar_devolve_conexao_ao_pool():
    conexao = FakeConexao()
    gerenciador = GerenciadorThreadBD(
        lambda: conexao, minimo=1, maximo=1)

    assert gerenciador.executar(lambda _: 'ok') == 'ok'
    assert gerenciador._pegar_conexao(
        timeout=0.01, tentativas=0) is conexao


def test_executar_nao_derruba_finally_quando_devolucao_falha():
    gerenciador = GerenciadorThreadBD(
        lambda: FakeConexao(), minimo=1, maximo=1)

    def devolver_com_falha(_):
        raise RuntimeError('pool indisponível')

    gerenciador._devolver_conexao = devolver_com_falha

    assert gerenciador.executar(lambda _: 'ok') == 'ok'
    assert gerenciador._operacoes_ativas == 0


def test_fechar_marca_estado_e_fecha_conexoes():
    conexao = FakeConexao()
    gerenciador = GerenciadorThreadBD(
        lambda: conexao, minimo=1, maximo=1)

    gerenciador.fechar()

    assert gerenciador._fechando is True
    assert conexao.closed is True
    with pytest.raises(RuntimeError):
        gerenciador._pegar_conexao(timeout=0.01, tentativas=0)
