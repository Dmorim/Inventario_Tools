from unittest.mock import patch

from Comandos.Comandos_Gerais.Comandos_Func import (
    Comandos_Func,
    comandos_true,
    montar_operacoes,
)
from Queries.Comando_Queries import QUERY_UPDATE_PRECU_PORCENTAGEM


class FakeCheckbox:
    """Checkbox fake: controla o estado marcado/desmarcado via get()."""

    def __init__(self, marcado=0):
        self._marcado = 1 if marcado else 0

    def get(self):
        return self._marcado


def criar_estado(marcados=()):
    """Cria um objeto `self` com os atributos necessários a Comandos_Func.

    `marcados` é uma coleção de índices de checkboxes marcados (ex.: (0, 3)).
    """
    self = type("SelfFake", (), {})()
    self.porcent_precu = '1.5'
    self.precu_vldia = '>'
    self.precu_cusme = '<'
    self.precu_vldia_preve = 'VLDIA'
    self.com_ger = 'UPDATE IN01PRO SET PRECU = 0'
    self.data_banco_inicial = '01.01.2024'
    checkbox_List = [FakeCheckbox(idx in marcados) for idx in range(12)]
    Comandos_Func(self, checkbox_List)
    return self, checkbox_List


class TestComandosFunc:
    def test_monta_dicionario_com_12_comandos(self):
        self, checkbox_List = criar_estado()
        assert len(self.comandos_query) == 12
        for cb in checkbox_List:
            assert cb in self.comandos_query

    def test_comando_porcentagem_recebe_parametro(self):
        self, checkbox_List = criar_estado()
        query, params = self.comandos_query[checkbox_List[0]]
        assert params == ('1.5',)

    def test_comando_operador_vldia_interpolado(self):
        self, checkbox_List = criar_estado()
        self.precu_vldia = '>'
        Comandos_Func(self, checkbox_List)
        query, params = self.comandos_query[checkbox_List[2]]
        assert '> PRECU' in query
        assert params == ()

    def test_comando_geral_recebe_sql_digitado(self):
        self, checkbox_List = criar_estado()
        query, params = self.comandos_query[checkbox_List[11]]
        assert query == self.com_ger
        assert params == ()


class TestComandosTrue:
    def test_retorna_apenas_marcados(self):
        self, checkbox_List = criar_estado((0, 3))
        resultado = comandos_true(self)
        assert QUERY_UPDATE_PRECU_PORCENTAGEM in resultado
        assert 'WHERE CUSME < PRECU' in resultado
        assert 'WHERE VLDIA' not in resultado

    def test_retorna_comandos_marcados(self):
        self, checkbox_List = criar_estado((2, 4))
        resultado = comandos_true(self)
        assert 'WHERE VLDIA > PRECU' in resultado
        assert 'WHERE (PRECU = 0 OR PRECU IS NULL)' in resultado


class TestMontarOperacoes:
    def test_sem_marcados_retorna_vazio(self):
        self, checkbox_List = criar_estado()
        operacoes = montar_operacoes(self, checkbox_List)
        assert operacoes == []

    def test_ordem_segue_checkbox_nao_arredondamento(self):
        self, checkbox_List = criar_estado((5,))
        operacoes = montar_operacoes(self, checkbox_List)
        assert len(operacoes) == 1
        assert operacoes[0][0] == 'Corrigir Classificação Nula'

    def test_comando_2_dispara_arredondamento_apos(self):
        self, checkbox_List = criar_estado((2,))
        operacoes = montar_operacoes(self, checkbox_List)
        nomes = [op[0] for op in operacoes]
        assert nomes == ['Preço de Custo = Preço de Compra',
                         'Arredondar Preço de Custo']

    def test_arredondamento_marcado_inclui_um_so(self):
        self, checkbox_List = criar_estado((1,))
        operacoes = montar_operacoes(self, checkbox_List)
        nomes = [op[0] for op in operacoes]
        # Arredondamento marcado diretamente não deve duplicar
        assert nomes.count('Arredondar Preço de Custo') == 1

    def test_arredondamento_nao_duplica_quando_comando_2_dispara(self):
        self, checkbox_List = criar_estado((1, 2))
        operacoes = montar_operacoes(self, checkbox_List)
        nomes = [op[0] for op in operacoes]
        assert nomes.count('Arredondar Preço de Custo') == 1

    @patch('tkinter.messagebox.showwarning')
    def test_comando_geral_adiciona_e_avisa(self, mock_warning):
        self, checkbox_List = criar_estado((11,))
        operacoes = montar_operacoes(self, checkbox_List, comando=None)
        nomes = [op[0] for op in operacoes]
        assert nomes == ['Comando Geral']
        mock_warning.assert_called_once()
