from decimal import Decimal

from Dashboard import Dashboard_Func
from Queries.Consulta_Queries import CFOP_LIST, QUERY_INVENTARIO, QUERY_VENDAS


def _fake_select(monkeypatch, retornos):
    """Substitui o acesso ao banco e registra (query, params) de cada chamada."""
    chamadas = []

    def fake(query, params=None):
        chamadas.append((query, params))
        return retornos[len(chamadas) - 1]

    monkeypatch.setattr(Dashboard_Func, '_executar_select', fake)
    return chamadas


def _fake_consulta(monkeypatch, retornos):
    """Substitui `_executar_consulta` e registra (query, params) de cada chamada."""
    chamadas = []

    def fake(query, params=None, **kwargs):
        chamadas.append((query, params))
        return retornos[len(chamadas) - 1]

    monkeypatch.setattr(Dashboard_Func, '_executar_consulta', fake)
    return chamadas


class TestExtrairSeries:
    def test_agrupamento_por_mes_usa_ano_e_mes_como_chave(self):
        valores, rotulos = Dashboard_Func._extrair_series(
            [(1, 2025, 100.5)], 'mes')
        assert valores == {(2025, 1): 100.5}
        assert rotulos == {(2025, 1): '01/2025'}

    def test_agrupamento_por_ano_usa_o_ano_como_chave(self):
        valores, rotulos = Dashboard_Func._extrair_series(
            [(2025, 200)], 'ano')
        assert valores == {(2025,): 200.0}
        assert rotulos == {(2025,): '2025'}

    def test_valor_nulo_vira_zero(self):
        valores, _ = Dashboard_Func._extrair_series([(6, 2024, None)], 'mes')
        assert valores == {(2024, 6): 0.0}

    def test_decimal_e_convertido_para_float(self):
        valores, _ = Dashboard_Func._extrair_series(
            [(3, 2025, Decimal('12.34'))], 'mes')
        assert valores == {(2025, 3): 12.34}
        assert isinstance(valores[(2025, 3)], float)

    def test_sem_linhas_retorna_dicionarios_vazios(self):
        assert Dashboard_Func._extrair_series([], 'mes') == ({}, {})

    def test_chave_repetida_mantem_o_ultimo_valor(self):
        valores, _ = Dashboard_Func._extrair_series(
            [(1, 2025, 10), (1, 2025, 20)], 'mes')
        assert valores == {(2025, 1): 20.0}


class TestPreviaInventario:
    def test_soma_o_movimento_liquido_ao_inventario(self, monkeypatch):
        _fake_consulta(monkeypatch, [600])
        assert Dashboard_Func._previa_inventario(
            10000, '01.01.2025', '31.12.2025') == 10600

    def test_movimento_negativo_reduz_o_inventario(self, monkeypatch):
        _fake_consulta(monkeypatch, [-450.5])
        assert Dashboard_Func._previa_inventario(
            10000, '01.01.2025', '31.12.2025') == 9549.5

    def test_envia_o_periodo_selecionado_para_a_query(self, monkeypatch):
        chamadas = _fake_consulta(monkeypatch, [0])
        Dashboard_Func._previa_inventario(1000, '01.01.2025', '30.06.2025')
        query, params = chamadas[0]
        assert query == Dashboard_Func.QUERY_MOVIMENTO_ESTOQUE_CUSTO
        assert params == ('01.01.2025', '30.06.2025')

    def test_movimento_ausente_mantem_o_inventario(self, monkeypatch):
        _fake_consulta(monkeypatch, [0])
        assert Dashboard_Func._previa_inventario(
            10000, '01.01.2025', '31.12.2025') == 10000

    def test_movimento_nulo_mantem_o_inventario(self, monkeypatch):
        monkeypatch.setattr(Dashboard_Func, 'query_executor',
                            lambda *a, **k: [(None,)])
        assert Dashboard_Func._previa_inventario(
            10000, '01.01.2025', '31.12.2025') == 10000

    def test_decimal_e_convertido_para_float(self, monkeypatch):
        _fake_consulta(monkeypatch, [Decimal('12.50')])
        resultado = Dashboard_Func._previa_inventario(
            10000, '01.01.2025', '31.12.2025')
        assert resultado == 10012.5
        assert isinstance(resultado, float)

    def test_inventario_nulo_e_tratado_como_zero(self, monkeypatch):
        _fake_consulta(monkeypatch, [250])
        assert Dashboard_Func._previa_inventario(
            None, '01.01.2025', '31.12.2025') == 250

    def test_falha_na_consulta_devolve_none(self, monkeypatch):
        _fake_consulta(monkeypatch, [None])
        assert Dashboard_Func._previa_inventario(
            10000, '01.01.2025', '31.12.2025') is None

    def test_pede_none_em_erro_para_nao_mascarar_a_falha(self, monkeypatch):
        kwargs_vistos = []

        def fake(query, params=None, **kwargs):
            kwargs_vistos.append(kwargs)
            return 0

        monkeypatch.setattr(Dashboard_Func, '_executar_consulta', fake)
        Dashboard_Func._previa_inventario(1000, '01.01.2025', '31.12.2025')

        assert kwargs_vistos[0].get('padrao_em_erro', 0) is None


class TestCalcularKpis:
    def test_formata_os_valores_e_calcula_vendas_130(self, monkeypatch):
        valores = iter([1000, 200, 50])
        monkeypatch.setattr(Dashboard_Func, '_executar_consulta',
                            lambda *a, **k: next(valores))
        monkeypatch.setattr(Dashboard_Func, '_previa_inventario',
                            lambda valor, ini, fim: 900)

        kpis = Dashboard_Func._calcular_kpis('01.01.2025', '31.12.2025')

        assert kpis['valor_inventario'] == '1.000,00'
        assert kpis['valor_vendas'] == '200,00'
        assert kpis['valor_entradas'] == '50,00'
        assert kpis['vendas_130'] == '260,00'
        assert kpis['previa_inventario'] == '900,00'

    def test_expoe_os_numeros_sem_formatacao(self, monkeypatch):
        valores = iter([1000, 200, 50])
        monkeypatch.setattr(Dashboard_Func, '_executar_consulta',
                            lambda *a, **k: next(valores))
        monkeypatch.setattr(Dashboard_Func, '_previa_inventario',
                            lambda valor, ini, fim: 900)

        kpis = Dashboard_Func._calcular_kpis('01.01.2025', '31.12.2025')

        assert kpis['valor_inventario_num'] == 1000.0
        assert kpis['valor_vendas_num'] == 200.0
        assert kpis['valor_entradas_num'] == 50.0
        assert kpis['vendas_130_num'] == 260.0
        assert kpis['previa_inventario_num'] == 900.0

    def test_consulta_inventario_sem_parametros_e_vendas_com_periodo(
            self, monkeypatch):
        chamadas = []

        def fake(query, params=None):
            chamadas.append((query, params))
            return 0

        monkeypatch.setattr(Dashboard_Func, '_executar_consulta', fake)
        monkeypatch.setattr(Dashboard_Func, '_previa_inventario',
                            lambda valor, ini, fim: 0)

        Dashboard_Func._calcular_kpis('01.01.2025', '31.12.2025')

        assert chamadas[0] == (QUERY_INVENTARIO, None)
        assert chamadas[1] == (QUERY_VENDAS, ('01.01.2025', '31.12.2025'))

    def test_entradas_recebem_cfops_e_periodo(self, monkeypatch):
        chamadas = []

        def fake(query, params=None):
            chamadas.append((query, params))
            return 0

        monkeypatch.setattr(Dashboard_Func, '_executar_consulta', fake)
        monkeypatch.setattr(Dashboard_Func, '_previa_inventario',
                            lambda valor, ini, fim: 0)

        Dashboard_Func._calcular_kpis('01.01.2025', '31.12.2025')

        query, params = chamadas[2]
        assert query.strip().startswith('SELECT CAST(')
        assert params == (*CFOP_LIST, '01.01.2025', '31.12.2025')

    def test_valores_zerados_continuam_formatados(self, monkeypatch):
        monkeypatch.setattr(Dashboard_Func, '_executar_consulta',
                            lambda *a, **k: 0)
        monkeypatch.setattr(Dashboard_Func, '_previa_inventario',
                            lambda valor, ini, fim: 0)

        kpis = Dashboard_Func._calcular_kpis('01.01.2025', '31.12.2025')

        assert kpis['valor_inventario'] == '0,00'
        assert kpis['valor_vendas'] == '0,00'

    def test_falha_na_previa_mostra_erro_no_card(self, monkeypatch):
        monkeypatch.setattr(Dashboard_Func, '_executar_consulta',
                            lambda *a, **k: 1000)
        monkeypatch.setattr(Dashboard_Func, '_previa_inventario',
                            lambda valor, ini, fim: None)

        kpis = Dashboard_Func._calcular_kpis('01.01.2025', '31.12.2025')

        assert kpis['previa_inventario'] == 'Erro'
        assert kpis['previa_inventario_num'] == 0.0
        assert kpis['valor_inventario'] == '1.000,00'

    def test_sem_previa_nao_consulta_nem_expoe_o_kpi(self, monkeypatch):
        chamadas = []
        monkeypatch.setattr(Dashboard_Func, '_executar_consulta',
                            lambda query, params=None: chamadas.append(params) or 0)

        def previa_nao_deveria_rodar(*args, **kwargs):
            raise AssertionError('_previa_inventario não deveria ser chamada')

        monkeypatch.setattr(Dashboard_Func, '_previa_inventario',
                            previa_nao_deveria_rodar)

        kpis = Dashboard_Func._calcular_kpis(
            '01.01.2024', '31.12.2024', incluir_previa=False)

        assert 'previa_inventario' not in kpis
        assert 'previa_inventario_num' not in kpis
        assert len(chamadas) == 3


class TestCarregarKpis:
    def test_sem_comparacao_devolve_um_dicionario(self, monkeypatch):
        monkeypatch.setattr(
            Dashboard_Func, '_calcular_kpis',
            lambda ini, fim, incluir_previa=True: {'valor_inventario': '1,00'})

        assert Dashboard_Func.carregar_kpis('01.01.2025', '31.12.2025') == {
            'valor_inventario': '1,00'}

    def test_com_periodo_anterior_devolve_tupla_de_dois_periodos(
            self, monkeypatch):
        periodos = []

        def fake(ini, fim, incluir_previa=True):
            periodos.append((ini, fim, incluir_previa))
            return {'valor_inventario': fim}

        monkeypatch.setattr(Dashboard_Func, '_calcular_kpis', fake)

        atual, anterior = Dashboard_Func.carregar_kpis(
            '01.01.2025', '31.12.2025', '01.01.2024', '31.12.2024')

        assert atual == {'valor_inventario': '31.12.2025'}
        assert anterior == {'valor_inventario': '31.12.2024'}
        assert periodos == [('01.01.2025', '31.12.2025', True),
                            ('01.01.2024', '31.12.2024', False)]

    def test_comparacao_exige_os_dois_limites_do_periodo_anterior(
            self, monkeypatch):
        monkeypatch.setattr(
            Dashboard_Func, '_calcular_kpis',
            lambda ini, fim, incluir_previa=True: {'valor_inventario': '1,00'})

        assert isinstance(
            Dashboard_Func.carregar_kpis('01.01.2025', '31.12.2025',
                                         '01.01.2024', None),
            dict)


class TestCarregarDadosTendencia:
    def test_une_as_series_por_mes_e_preenche_periodos_ausentes(
            self, monkeypatch):
        _fake_select(monkeypatch, [
            [(1, 2025, 100), (2, 2025, 200)],
            [(1, 2025, 150), (3, 2025, 60)],
        ])

        dados = Dashboard_Func.carregar_dados_tendencia(
            '01.01.2025', '31.12.2025', 'mes')

        assert dados['labels'] == ['01/2025', '02/2025', '03/2025']
        assert dados['vendas'] == [100.0, 200.0, 0.0]
        assert dados['entradas'] == [150.0, 0.0, 60.0]

    def test_diferenca_e_entradas_menos_vendas(self, monkeypatch):
        _fake_select(monkeypatch, [
            [(1, 2025, 100), (2, 2025, 200)],
            [(1, 2025, 150), (3, 2025, 60)],
        ])

        dados = Dashboard_Func.carregar_dados_tendencia(
            '01.01.2025', '31.12.2025', 'mes')

        assert dados['diferenca'] == [50.0, -200.0, 60.0]

    def test_agrupamento_por_ano_ordena_anos_das_duas_series(
            self, monkeypatch):
        _fake_select(monkeypatch, [
            [(2025, 100)],
            [(2024, 50)],
        ])

        dados = Dashboard_Func.carregar_dados_tendencia(
            '01.01.2024', '31.12.2025', 'ano')

        assert dados['labels'] == ['2024', '2025']
        assert dados['vendas'] == [0.0, 100.0]
        assert dados['entradas'] == [50.0, 0.0]
        assert dados['diferenca'] == [50.0, -100.0]

    def test_envia_os_cfops_e_o_periodo_para_as_entradas(self, monkeypatch):
        chamadas = _fake_select(monkeypatch, [[(1, 2025, 1)], [(1, 2025, 1)]])

        Dashboard_Func.carregar_dados_tendencia(
            '01.01.2025', '31.12.2025', 'mes')

        assert chamadas[0][1] == ('01.01.2025', '31.12.2025')
        assert chamadas[1][1] == (*CFOP_LIST, '01.01.2025', '31.12.2025')

    def test_erro_de_banco_devolve_series_vazias_sem_propagar(
            self, monkeypatch):
        def fake(query, params=None):
            raise RuntimeError('falha simulada')

        monkeypatch.setattr(Dashboard_Func, '_executar_select', fake)

        assert Dashboard_Func.carregar_dados_tendencia(
            '01.01.2025', '31.12.2025', 'mes') == {
            'labels': [], 'vendas': [], 'entradas': [], 'diferenca': []}


class TestExecutarConsulta:
    def test_falha_usa_o_padrao_em_erro_informado(self, monkeypatch):
        def falhar(*args, **kwargs):
            raise RuntimeError('falha simulada')

        monkeypatch.setattr(Dashboard_Func, 'query_executor', falhar)

        assert Dashboard_Func._executar_consulta(
            'SELECT 1', None, padrao_em_erro=None) is None

    def test_falha_sem_padrao_mantem_zero(self, monkeypatch):
        def falhar(*args, **kwargs):
            raise RuntimeError('falha simulada')

        monkeypatch.setattr(Dashboard_Func, 'query_executor', falhar)

        assert Dashboard_Func._executar_consulta('SELECT 1') == 0

    def test_resultado_nulo_nao_e_tratado_como_erro(self, monkeypatch):
        monkeypatch.setattr(Dashboard_Func, 'query_executor',
                            lambda *a, **k: [(None,)])

        assert Dashboard_Func._executar_consulta(
            'SELECT 1', None, padrao_em_erro=None) == 0
