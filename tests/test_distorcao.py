import dataclasses

import pytest

from Distorcao_Manager import DistorcaoInventario, DistorcaoManager


def _distorcao_exemplo():
    return DistorcaoInventario(
        cdpro=['001', '002'],
        nmpro=['Produto A', 'Produto B'],
        saldo_lan=[10.0, 20.0],
        saldo_pro=[15.0, 20.0],
    )


class TestDistorcaoInventario:
    def test_tamanho(self):
        assert _distorcao_exemplo().tamanho == 2

    def test_campos_em_lista(self):
        assert _distorcao_exemplo().campos_em_lista == [
            ('001', 'Produto A', 10.0, 15.0),
            ('002', 'Produto B', 20.0, 20.0),
        ]

    def test_converte_listas_para_tuplas(self):
        distorcao = _distorcao_exemplo()
        assert isinstance(distorcao.cdpro, tuple)
        assert isinstance(distorcao.nmpro, tuple)
        assert isinstance(distorcao.saldo_lan, tuple)
        assert isinstance(distorcao.saldo_pro, tuple)

    def test_dados_vazios(self):
        distorcao = DistorcaoInventario([], [], [], [])
        assert distorcao.tamanho == 0
        assert distorcao.campos_em_lista == []

    def test_tamanhos_divergentes_geram_erro(self):
        with pytest.raises(ValueError):
            DistorcaoInventario(['001'], ['A', 'B'], [1.0], [2.0])

    def test_frozen(self):
        distorcao = _distorcao_exemplo()
        with pytest.raises(dataclasses.FrozenInstanceError):
            distorcao.cdpro = ()


class TestDistorcaoManager:
    @pytest.fixture(autouse=True)
    def _resetar_singleton(self):
        DistorcaoManager._instancia = None
        yield
        DistorcaoManager._instancia = None

    def test_singleton_reutiliza_instancia(self):
        gerenciador_1 = DistorcaoManager(_distorcao_exemplo())
        gerenciador_2 = DistorcaoManager(DistorcaoInventario([], [], [], []))
        assert gerenciador_1 is gerenciador_2

    def test_primeira_instancia_guarda_dados(self):
        gerenciador = DistorcaoManager(_distorcao_exemplo())
        assert gerenciador.obter_distorcao().tamanho == 2

    def test_reconstrucao_nao_reseta_dados(self):
        gerenciador = DistorcaoManager(_distorcao_exemplo())
        DistorcaoManager(DistorcaoInventario([], [], [], []))
        assert gerenciador.obter_distorcao().tamanho == 2

    def test_atualizar_distorcao(self):
        gerenciador = DistorcaoManager(DistorcaoInventario([], [], [], []))
        assert gerenciador.possui_itens() is False

        gerenciador.atualizar_distorcao(_distorcao_exemplo())
        assert gerenciador.possui_itens() is True
        assert gerenciador.obter_distorcao().campos_em_lista[0][0] == '001'
