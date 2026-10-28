import datetime

import pytest

from Data_Manager.PeriodoInventario import PeriodoInventario
from Data_Manager.PeriodoManager import PeriodoManager


def _periodo(inicio, fim):
    return PeriodoInventario(
        datetime.date(*inicio), datetime.date(*fim))


def _manager(periodo_ini=((2024, 1, 1), (2024, 12, 31))):
    return PeriodoManager(_periodo(*periodo_ini))


class TestObterPeriodo:
    def test_retorna_periodo_inicial(self):
        m = _manager()
        p = m.obter_periodo()
        assert p.inicio == datetime.date(2024, 1, 1)
        assert p.fim == datetime.date(2024, 12, 31)

    def test_retorna_snapshot_atual_apos_atualizar(self):
        m = _manager()
        novo = _periodo((2025, 1, 1), (2025, 12, 31))
        m.atualizar_periodo(novo)
        assert m.obter_periodo() is novo

    def test_retorno_eh_imutavel(self):
        m = _manager()
        p = m.obter_periodo()
        with pytest.raises(Exception):
            p.inicio = datetime.date(2023, 1, 1)


class TestFormatoBanco:
    def test_inicio_formatado(self):
        m = _manager()
        assert m.obter_periodo().inicio_formatado == '01.01.2024'

    def test_fim_formatado(self):
        m = _manager()
        assert m.obter_periodo().fim_formatado == '31.12.2024'

    def test_datas_com_um_digito_sao_alinhadas(self):
        m = _manager()
        p = PeriodoInventario(datetime.date(2024, 3, 5),
                              datetime.date(2024, 3, 9))
        assert p.inicio_formatado == '05.03.2024'
        assert p.fim_formatado == '09.03.2024'


class TestValidacaoPeriodo:
    def test_periodo_invertido_gera_erro(self):
        with pytest.raises(ValueError):
            PeriodoInventario(datetime.date(2024, 12, 31),
                              datetime.date(2024, 1, 1))

    def test_periodo_igual_nao_gera_erro(self):
        d = datetime.date(2024, 6, 1)
        p = PeriodoInventario(d, d)
        assert p.inicio == p.fim


class TestIgualdade:
    def test_periodos_iguais_sao_iguais(self):
        a = _periodo((2024, 1, 1), (2024, 12, 31))
        b = _periodo((2024, 1, 1), (2024, 12, 31))
        assert a == b

    def test_periodos_diferentes_nao_sao_iguais(self):
        a = _periodo((2024, 1, 1), (2024, 12, 31))
        b = _periodo((2025, 1, 1), (2025, 12, 31))
        assert a != b


class TestNotificacao:
    def test_atualizar_periodo_notifica_listener(self):
        m = _manager()
        recebidos = []
        m.adicionar_listener(recebidos.append)
        novo = _periodo((2025, 1, 1), (2025, 12, 31))
        m.atualizar_periodo(novo)
        assert recebidos == [novo]

    def test_atualizar_com_periodo_igual_nao_notifica(self):
        m = _manager()
        recebidos = []
        m.adicionar_listener(recebidos.append)
        m.atualizar_periodo(_periodo((2024, 1, 1), (2024, 12, 31)))
        assert recebidos == []

    def test_remover_listener_para_notificar(self):
        m = _manager()
        recebidos = []
        m.adicionar_listener(recebidos.append)
        m.remover_listener(recebidos.append)
        m.atualizar_periodo(_periodo((2025, 1, 1), (2025, 12, 31)))
        assert recebidos == []

    def test_multiplos_listeners_notificados(self):
        m = _manager()
        r1, r2 = [], []
        m.adicionar_listener(r1.append)
        m.adicionar_listener(r2.append)
        novo = _periodo((2025, 1, 1), (2025, 12, 31))
        m.atualizar_periodo(novo)
        assert r1 == [novo]
        assert r2 == [novo]

    def test_adicionar_mesmo_listener_duplica(self):
        m = _manager()
        recebidos = []
        m.adicionar_listener(recebidos.append)
        m.adicionar_listener(recebidos.append)
        novo = _periodo((2025, 1, 1), (2025, 12, 31))
        m.atualizar_periodo(novo)
        assert recebidos == [novo]

    def test_remover_listener_nao_registrado_nao_erro(self):
        m = _manager()
        m.remover_listener(lambda p: None)
