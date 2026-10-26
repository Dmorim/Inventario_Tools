from datetime import date, timedelta

import Dashboard.Dashboard_Screen as dashboard_screen
from Dashboard.Dashboard_Screen import (
    _esconder_loading,
    _formatar_variacao,
    _mostrar_erro_loading,
    _periodo_anterior,
)


class TestPeriodoAnterior:
    def test_mes_completo_retorna_mes_anterior(self):
        assert _periodo_anterior(date(2026, 10, 1), date(2026, 10, 31)) == (
            '31.08.2026', '30.09.2026')

    def test_termina_no_dia_anterior_ao_inicio_do_periodo(self):
        _, fim_anterior = _periodo_anterior(date(2026, 10, 1), date(2026, 10, 31))
        assert fim_anterior == '30.09.2026'

    def test_mantem_a_mesma_duracao_do_periodo_atual(self):
        inicio, fim = date(2026, 3, 10), date(2026, 4, 20)
        inicio_anterior, fim_anterior = _periodo_anterior(inicio, fim)
        atual = (fim - inicio).days + 1
        anterior = (_para_data(fim_anterior)
                    - _para_data(inicio_anterior)).days + 1
        assert anterior == atual
        assert _para_data(fim_anterior) == inicio - timedelta(days=1)

    def test_ano_completo(self):
        assert _periodo_anterior(date(2026, 1, 1), date(2026, 12, 31)) == (
            '01.01.2025', '31.12.2025')

    def test_periodo_de_um_dia(self):
        assert _periodo_anterior(date(2026, 5, 10), date(2026, 5, 10)) == (
            '09.05.2026', '09.05.2026')

    def test_ano_bissexto_e_preservado(self):
        assert _periodo_anterior(date(2024, 3, 1), date(2024, 3, 31)) == (
            '30.01.2024', '29.02.2024')

    def test_sem_sobreposicao_com_o_periodo_atual(self):
        inicio = date(2026, 7, 1)
        fim = date(2026, 7, 31)
        inicio_anterior, _ = _periodo_anterior(inicio, fim)
        assert _para_data(inicio_anterior) < inicio

    def test_entrada_invalida_retorna_none(self):
        assert _periodo_anterior(None, None) == (None, None)
        assert _periodo_anterior(date(2026, 1, 1), 'fim') == (None, None)


class TestFormatarVariacao:
    def test_aumento_usa_sinal_positivo_e_verde(self):
        assert _formatar_variacao(150, 100) == (
            '+50.0% vs período anterior', '#2ecc71')

    def test_queda_usa_sinal_negativo_e_vermelho(self):
        assert _formatar_variacao(50, 100) == (
            '-50.0% vs período anterior', '#e74c3c')

    def test_sem_variacao_mostra_zero(self):
        assert _formatar_variacao(100, 100) == (
            '+0.0% vs período anterior', '#2ecc71')

    def test_queda_total(self):
        assert _formatar_variacao(0, 200) == (
            '-100.0% vs período anterior', '#e74c3c')

    def test_arredonda_em_uma_casa_decimal(self):
        assert _formatar_variacao(101, 100)[0] == '+1.0% vs período anterior'

    def test_periodo_anterior_zero_nao_divide_por_zero(self):
        assert _formatar_variacao(100, 0) == (None, None)

    def test_valores_ausentes_nao_geram_variacao(self):
        assert _formatar_variacao(None, None) == (None, None)

    def test_aceita_strings_numericas(self):
        assert _formatar_variacao('150', '100') == (
            '+50.0% vs período anterior', '#2ecc71')

    def test_base_negativa_usa_valor_absoluto(self):
        assert _formatar_variacao(-50, -100) == (
            '+50.0% vs período anterior', '#2ecc71')


def _para_data(texto):
    dia, mes, ano = (int(parte) for parte in texto.split('.'))
    return date(ano, mes, dia)


class _FakeLabel:
    """Rótulo mínimo para testar o ciclo de vida do 'Carregando dados...'."""

    def __init__(self, manager='pack', existe=True):
        self._manager = manager
        self._existe = existe
        self.chamadas = []
        self.texto = 'Carregando dados...'
        self.cor = None

    def winfo_exists(self):
        return self._existe

    def winfo_manager(self):
        return self._manager

    def pack(self, **kwargs):
        self.chamadas.append(('pack', kwargs))
        self._manager = 'pack'

    def pack_forget(self):
        self.chamadas.append(('pack_forget', {}))
        self._manager = ''

    def grid_forget(self):
        self.chamadas.append(('grid_forget', {}))
        self._manager = ''

    def place_forget(self):
        self.chamadas.append(('place_forget', {}))
        self._manager = ''

    def configure(self, **kwargs):
        self.chamadas.append(('configure', kwargs))
        self.texto = kwargs.get('text', self.texto)
        self.cor = kwargs.get('text_color', self.cor)

    def update_idletasks(self):
        self.chamadas.append(('update_idletasks', {}))

    def nomes(self):
        return [nome for nome, _ in self.chamadas]


class TestEsconderLoading:
    def test_pack_forget_quando_gerenciado_por_pack(self):
        label = _FakeLabel(manager='pack')
        _esconder_loading(label)
        assert label.nomes() == ['pack_forget']
        assert label.winfo_manager() == ''

    def test_grid_forget_quando_gerenciado_por_grid(self):
        label = _FakeLabel(manager='grid')
        _esconder_loading(label)
        assert label.nomes() == ['grid_forget']
        assert label.winfo_manager() == ''

    def test_place_forget_quando_gerenciado_por_place(self):
        label = _FakeLabel(manager='place')
        _esconder_loading(label)
        assert label.nomes() == ['place_forget']
        assert label.winfo_manager() == ''

    def test_sem_gerenciador_nao_chama_forget(self):
        label = _FakeLabel(manager='')
        _esconder_loading(label)
        assert label.nomes() == []

    def test_widget_inexistente_e_ignorado(self):
        label = _FakeLabel(existe=False)
        _esconder_loading(label)
        assert label.nomes() == []

    def test_none_nao_levanta(self):
        _esconder_loading(None)


class TestMostrarErroLoading:
    def test_exibe_texto_em_vermelho(self):
        label = _FakeLabel(manager='pack')
        _mostrar_erro_loading(label, 'Erro ao carregar dados: falha')
        assert label.texto == 'Erro ao carregar dados: falha'
        assert label.cor == '#e74c3c'

    def test_reempacota_quando_estava_escondido(self):
        label = _FakeLabel(manager='')
        _mostrar_erro_loading(label, 'Erro')
        assert label.nomes() == ['pack', 'configure', 'update_idletasks']
        assert label.winfo_manager() == 'pack'

    def test_nao_reempacota_quando_ja_visivel(self):
        label = _FakeLabel(manager='pack')
        _mostrar_erro_loading(label, 'Erro')
        assert label.nomes() == ['configure', 'update_idletasks']

    def test_widget_inexistente_ou_none_e_ignorado(self):
        label = _FakeLabel(existe=False)
        _mostrar_erro_loading(label, 'Erro')
        _mostrar_erro_loading(None, 'Erro')
        assert label.nomes() == []


class _TipoVar:
    def __init__(self, valor='Barras'):
        self._valor = valor

    def get(self):
        return self._valor


class TestCarregarDadosAvisaConclusao:
    """O contador de cargas pendentes depende destes avisos de conclusão."""

    def _instalar_thread_fake(self, monkeypatch):
        registro = {}

        def fake_thread(master, func, callback, on_erro=None, *args, **kwargs):
            registro['callback'] = callback
            registro['on_erro'] = on_erro

        monkeypatch.setattr(dashboard_screen, 'thread_execução', fake_thread)
        monkeypatch.setattr(
            dashboard_screen, '_atualizar_dashboard', lambda *a, **k: None)
        return registro

    def test_sucesso_avisa_conclusao(self, monkeypatch):
        registro = self._instalar_thread_fake(monkeypatch)
        conclusoes = []
        dashboard_screen._carregar_dados(
            object(), object(), None, '01.10.2026', '31.10.2026',
            on_concluir=lambda: conclusoes.append(1))
        registro['callback']({})
        assert conclusoes == [1]

    def test_sucesso_comparativo_avisa_conclusao(self, monkeypatch):
        registro = self._instalar_thread_fake(monkeypatch)
        conclusoes = []
        dashboard_screen._carregar_dados(
            object(), object(), None, '01.10.2026', '31.10.2026',
            '01.09.2026', '30.09.2026',
            on_concluir=lambda: conclusoes.append(1))
        registro['callback'](({'valor_vendas_num': 10},
                              {'valor_vendas_num': 5}))
        assert conclusoes == [1]

    def test_erro_avisa_conclusao_e_repassa_excecao(self, monkeypatch):
        registro = self._instalar_thread_fake(monkeypatch)
        erros = []
        conclusoes = []
        dashboard_screen._carregar_dados(
            object(), object(), erros.append, '01.10.2026', '31.10.2026',
            on_concluir=lambda: conclusoes.append(1))
        falha = RuntimeError('sem conexão')
        registro['on_erro'](falha)
        assert conclusoes == [1]
        assert erros == [falha]


class TestRecarregarTendenciaAvisaConclusao:
    def _instalar(self, monkeypatch):
        registro = {}
        monkeypatch.setattr(
            dashboard_screen, 'thread_execução',
            lambda master, func, callback, on_erro=None, *args, **kwargs:
                registro.update(callback=callback, on_erro=on_erro))
        monkeypatch.setattr(
            dashboard_screen, '_renderizar_tendencia', lambda *a, **k: None)
        monkeypatch.setattr(
            dashboard_screen.ctk, 'CTkLabel',
            lambda *a, **k: _FakeLabel(manager=''))
        return registro

    def test_callback_grava_cache_e_avisa_conclusao(self, monkeypatch):
        registro = self._instalar(monkeypatch)
        conclusoes = []
        estado = {'seq': 0, 'cache': {}}
        dashboard_screen._recarregar_tendencia(
            object(), object(), _TipoVar(), estado, 'mes', 'ini', 'fim',
            on_concluir=lambda: conclusoes.append(1))
        registro['callback']([1, 2])
        assert conclusoes == [1]
        assert estado['cache']['mes'] == [1, 2]

    def test_resposta_obsoleta_avisa_conclusao_sem_gravar_cache(
            self, monkeypatch):
        registro = self._instalar(monkeypatch)
        conclusoes = []
        estado = {'seq': 0, 'cache': {}}
        dashboard_screen._recarregar_tendencia(
            object(), object(), _TipoVar(), estado, 'mes', 'ini', 'fim',
            on_concluir=lambda: conclusoes.append(1))
        estado['seq'] += 1
        registro['callback']([1, 2])
        assert conclusoes == [1]
        assert estado['cache'] == {}

    def test_erro_avisa_conclusao(self, monkeypatch):
        registro = self._instalar(monkeypatch)
        conclusoes = []
        estado = {'seq': 0, 'cache': {}}
        dashboard_screen._recarregar_tendencia(
            object(), object(), _TipoVar(), estado, 'mes', 'ini', 'fim',
            on_concluir=lambda: conclusoes.append(1))
        registro['on_erro'](RuntimeError('falha'))
        assert conclusoes == [1]
        assert estado['cache'] == {}
