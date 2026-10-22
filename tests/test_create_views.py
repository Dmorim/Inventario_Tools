from unittest.mock import patch

import pytest

from Queries import Create_Views


class ErroSimulado(Exception):
    """Erro de banco simulado para os testes de remoção de views."""


class CursorFake:
    def __init__(self, conexao):
        self.conexao = conexao

    def execute(self, query):
        self.conexao.comandos.append(query)
        for nome, erro in self.conexao.erros_por_view.items():
            if nome in query.upper():
                raise erro

    def close(self):
        self.conexao.cursors_fechados += 1


class ConexaoFake:
    """Conexão fake que falha no DROP de views específicas."""

    def __init__(self, erros_por_view=None):
        self.erros_por_view = erros_por_view or {}
        self.comandos = []
        self.commits = 0
        self.rollbacks = 0
        self.cursors_fechados = 0

    def cursor(self):
        return CursorFake(self)

    def commit(self):
        self.commits += 1

    def rollback(self):
        self.rollbacks += 1


def _executar(conexao, views):
    with patch.object(Create_Views, 'DROP_VIEW_DDL_ORDER',
                      [(nome, '') for nome in views]):
        return Create_Views._deletar_views_na_conexao(conexao)


class TestDeletarViews:
    def test_remocao_com_sucesso_remove_todas(self):
        conexao = ConexaoFake()
        _executar(conexao, ['V_A', 'V_B'])
        assert conexao.comandos == ['DROP VIEW V_A', 'DROP VIEW V_B']
        assert conexao.commits == 2
        assert conexao.cursors_fechados == 2

    def test_falha_em_uma_view_nao_impede_as_demais(self):
        erro = ErroSimulado('falha simulada')
        conexao = ConexaoFake({'V_A': erro})
        with pytest.raises(ErroSimulado):
            _executar(conexao, ['V_A', 'V_B'])
        assert 'DROP VIEW V_A' in conexao.comandos
        assert 'DROP VIEW V_B' in conexao.comandos

    def test_excecao_original_e_relancada(self):
        erro = ErroSimulado('falha simulada')
        conexao = ConexaoFake({'V_A': erro})
        with pytest.raises(ErroSimulado) as excecao:
            _executar(conexao, ['V_A'])
        assert excecao.value is erro

    def test_erro_e_registrado_no_log(self):
        erro = ErroSimulado('falha simulada')
        conexao = ConexaoFake({'V_A': erro})
        with patch.object(Create_Views, 'logger') as logger_fake:
            with pytest.raises(ErroSimulado):
                _executar(conexao, ['V_A'])
        chamadas = logger_fake.exception.call_args_list
        assert chamadas
        modelo, argumentos = chamadas[0][0]
        assert 'V_A' in modelo % argumentos

    def test_rollback_apos_falha_e_commit_apenas_das_validas(self):
        erro = ErroSimulado('falha simulada')
        conexao = ConexaoFake({'V_A': erro})
        with pytest.raises(ErroSimulado):
            _executar(conexao, ['V_A', 'V_B'])
        assert conexao.commits == 1
        assert conexao.rollbacks == 2
        assert conexao.cursors_fechados == 2
