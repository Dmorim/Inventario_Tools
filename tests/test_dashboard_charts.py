import matplotlib

matplotlib.use('Agg')

from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.figure import Figure

from Dashboard.Dashboard_Charts import (
    CORES_POR_TEMA,
    MARGEM_Y_ROTULOS,
    MAX_PONTOS_COM_VALORES,
    _contraste,
    _desenhar_series,
    _rotulos_eixo_x,
    _valor_compacto,
)

# Tamanhos reais do widget do grafico (Dashboard 1080x560 e minimo 680x520).
TAMANHOS_GRAFICO = (
    ('padrao', (10.6, 3.4)),
    ('minimo', (6.6, 3.0)),
)

TOLERANCIA_PX = 0.5
# No tamanho minimo da janela os rotulos de "diferenca" de grupos vizinhos
# encostam (medido: 0,6 px horizontal x 0,7 px vertical). Acima disso e
# colisao real de rotulo.
TOLERANCIA_SOBREPOSICAO_PX = 1.0


class TestValorCompacto:
    def test_valor_abaixo_de_mil_sem_decimais(self):
        assert _valor_compacto(950) == 'R$ 950'

    def test_milhares_compactado(self):
        assert _valor_compacto(350000) == 'R$ 350 mil'

    def test_milhoes_compactado(self):
        assert _valor_compacto(1900000) == 'R$ 1,9 mi'

    def test_bilhoes_compactado(self):
        assert _valor_compacto(2500000000) == 'R$ 2,5 bi'

    def test_valor_negativo_preserva_sinal(self):
        assert _valor_compacto(-1900000) == '-R$ 1,9 mi'

    def test_valor_negativo_mil(self):
        assert _valor_compacto(-350000) == '-R$ 350 mil'

    def test_sem_simbolo_de_moeda(self):
        assert _valor_compacto(350000, com_simbolo=False) == '350 mil'

    def test_valor_nulo_vira_zero(self):
        assert _valor_compacto(None) == 'R$ 0'

    def test_valor_zero(self):
        assert _valor_compacto(0) == 'R$ 0'


class TestRotulosEixoX:
    def test_poucos_rotulos_sao_mantidos(self):
        labels = ['01/2021', '02/2021', '03/2021']
        assert _rotulos_eixo_x(labels) == labels

    def test_muitos_rotulos_sao_rareados(self):
        labels = [f'{mes:02d}/2021' for mes in range(1, 62)]
        visiveis = _rotulos_eixo_x(labels)
        assert len(visiveis) == 61
        assert sum(1 for rotulo in visiveis if rotulo) <= 16
        assert '' in visiveis

    def test_ultimo_rotulo_e_preservado(self):
        labels = [f'{mes:02d}/2021' for mes in range(1, 62)]
        visiveis = _rotulos_eixo_x(labels)
        assert visiveis[-1] == '61/2021'

    def test_rotulo_com_limite_customizado(self):
        labels = [f'{mes:02d}/2021' for mes in range(1, 13)]
        visiveis = _rotulos_eixo_x(labels, maximo=4)
        assert sum(1 for rotulo in visiveis if rotulo) <= 4
        assert visiveis[-1] == '12/2021'


class TestContraste:
    def test_texto_do_grafico_contrasta_com_a_figura(self):
        for tema, cores in CORES_POR_TEMA.items():
            assert _contraste(cores['texto'], cores['figura']) >= 4.5, tema

    def test_subtexto_contrasta_com_a_figura(self):
        for tema, cores in CORES_POR_TEMA.items():
            assert _contraste(cores['subtexto'], cores['figura']) >= 4.5, tema

    def test_rotulo_de_valor_contrasta_com_a_caixa_de_fundo(self):
        for tema, cores in CORES_POR_TEMA.items():
            assert _contraste(cores['texto'], cores['figura']) >= 4.5, tema


def _dados_tendencia(total):
    # Decisao do usuario (22/10/2026): as vendas vao para cima, com valor
    # positivo; o grafico desenha os valores como chegam.
    entradas = ([951529.18, 703596.11, 597393.68] * (total // 3 + 1))[:total]
    vendas = ([1612693.53, 1200000.0, 900000.0] * (total // 3 + 1))[:total]
    diferencas = [entrada - venda for entrada, venda in zip(entradas, vendas)]
    labels = [f'{mes:02d}/2025' for mes in range(1, total + 1)]
    return labels, entradas, vendas, diferencas


def _renderizar(figsize, total, tipo='Barras'):
    fig = Figure(figsize=figsize, dpi=100, facecolor='#ffffff')
    ax = fig.add_subplot(111)
    labels, entradas, vendas, diferencas = _dados_tendencia(total)
    _desenhar_series(ax, labels, entradas, vendas, diferencas, tipo,
                      CORES_POR_TEMA['Light'])
    ax.set_xticks(range(total))
    ax.set_xticklabels(labels, fontsize=7, rotation=45, ha='right')
    fig.set_layout_engine('tight')
    canvas = FigureCanvasAgg(fig)
    canvas.draw()
    return fig, ax, canvas.get_renderer()


class TestRotulosDeValor:
    def test_rotulos_de_valor_sao_desenhados(self):
        fig, ax, renderer = _renderizar((10.6, 3.4), 12)
        assert len(ax.texts) == 12 * 3
        fig.clear()

    def test_rotulos_de_valor_nao_sao_cortados(self):
        for nome, figsize in TAMANHOS_GRAFICO:
            for total in (5, 7, 12):
                fig, ax, renderer = _renderizar(figsize, total)
                area = ax.get_window_extent(renderer)
                for texto in ax.texts:
                    caixa = texto.get_window_extent(renderer)
                    assert caixa.y1 <= area.y1 + TOLERANCIA_PX, (nome, total)
                    assert caixa.y0 >= area.y0 - TOLERANCIA_PX, (nome, total)
                    assert caixa.x0 >= area.x0 - TOLERANCIA_PX, (nome, total)
                    assert caixa.x1 <= area.x1 + TOLERANCIA_PX, (nome, total)
                fig.clear()

    def test_rotulos_de_valor_nao_se_sobrepoem(self):
        for nome, figsize in TAMANHOS_GRAFICO:
            fig, ax, renderer = _renderizar(figsize, 12)
            caixas = [texto.get_window_extent(renderer) for texto in ax.texts]
            for indice, caixa in enumerate(caixas):
                for outra in caixas[indice + 1:]:
                    sobreposicao_x = min(caixa.x1, outra.x1) - max(caixa.x0,
                                                                   outra.x0)
                    sobreposicao_y = min(caixa.y1, outra.y1) - max(caixa.y0,
                                                                   outra.y0)
                    colide = (sobreposicao_x > TOLERANCIA_SOBREPOSICAO_PX
                              and sobreposicao_y
                              > TOLERANCIA_SOBREPOSICAO_PX)
                    assert not colide, nome
            fig.clear()

    def test_rotulos_desaparecem_acima_do_limite_de_pontos(self):
        total = MAX_PONTOS_COM_VALORES + 1
        fig, ax, renderer = _renderizar((10.6, 3.4), total)
        assert len(ax.texts) == 0
        fig.clear()

    def test_margem_de_rotulos_aplicada_no_eixo_y(self):
        assert MARGEM_Y_ROTULOS > 0
        fig, ax, renderer = _renderizar((10.6, 3.4), 12)
        assert ax.margins()[1] == MARGEM_Y_ROTULOS
        fig.clear()

    def test_modo_linhas_nao_altera_a_margem(self):
        fig, ax, renderer = _renderizar((10.6, 3.4), 12, tipo='Linhas')
        assert ax.margins()[1] == matplotlib.rcParams['axes.ymargin']
        assert len(ax.texts) == 0
        fig.clear()
