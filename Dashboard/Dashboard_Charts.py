from customtkinter import CTkLabel
from customtkinter import get_appearance_mode
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
from matplotlib.ticker import FuncFormatter
import matplotlib
import matplotlib.patheffects as path_effects
import numpy as np
from scipy.interpolate import make_interp_spline

from Outros.Logger.Get_Logger import get_logger

matplotlib.use('Agg')

logger = get_logger(__name__)


COR_SERIES_VENDAS = '#2ecc71'
COR_SERIES_ENTRADAS = '#3498db'
COR_SERIES_DIFERENCA = '#e74c3c'

MAX_ROTULOS_EIXO_X = 16
MAX_PONTOS_COM_VALORES = 12
MARGEM_Y_ROTULOS = 0.12
ROTACAO_ROTULOS_BARRAS = 90
MAX_AJUSTES_FOLGA_VERTICAL = 8
FOLGA_MINIMA_PX = 0.5
FONTE_ROTULOS_LINHA = 8
TOLERANCIA_COLISAO_PX = 1.0
CANDIDATOS_ROTULO_LINHA = (
    (0, 7, 'bottom'), (0, -7, 'top'),
    (0, 18, 'bottom'), (0, -18, 'top'),
    (0, 28, 'bottom'), (0, -28, 'top'),
)

CORES_POR_TEMA = {
    'Light': {
        'figura': '#ffffff',
        'texto': '#212d38',
        'subtexto': '#5d6d7e',
        'grade': '#bdc3c7',
    },
    'Dark': {
        'figura': '#2A2C3D',
        'texto': '#ecf0f1',
        'subtexto': '#b7e2e6',
        'grade': '#4a4f63',
    },
}


def _cores():
    return CORES_POR_TEMA.get(get_appearance_mode(), CORES_POR_TEMA['Light'])


def _contraste(cor_a, cor_b):
    def luminancia(cor):
        cor = cor.lstrip('#')
        canais = [int(cor[indice:indice + 2], 16) / 255
                  for indice in (0, 2, 4)]
        ajustados = [
            canal / 12.92 if canal <= 0.03928
            else ((canal + 0.055) / 1.055) ** 2.4
            for canal in canais]
        return (0.2126 * ajustados[0] + 0.7152 * ajustados[1]
                + 0.0722 * ajustados[2])

    lum_a, lum_b = luminancia(cor_a), luminancia(cor_b)
    claro, escuro = max(lum_a, lum_b), min(lum_a, lum_b)
    return (claro + 0.05) / (escuro + 0.05)


def _dimensoes_figura(master, dpi=100, minimo=(4.0, 2.0)):
    largura = master.winfo_width()
    altura = master.winfo_height()
    if largura <= 1 or altura <= 1:
        return minimo
    return (max(largura / dpi, minimo[0]), max(altura / dpi, minimo[1]))


def _valor_compacto(valor, com_simbolo=True):
    numero = float(valor or 0)
    sinal = '-' if numero < 0 else ''
    absoluto = abs(numero)
    if absoluto >= 1_000_000_000:
        texto = f'{absoluto / 1_000_000_000:.1f} bi'
    elif absoluto >= 1_000_000:
        texto = f'{absoluto / 1_000_000:.1f} mi'
    elif absoluto >= 1_000:
        texto = f'{absoluto / 1_000:.0f} mil'
    else:
        texto = f'{absoluto:.0f}'
    prefixo = 'R$ ' if com_simbolo else ''
    return f'{sinal}{prefixo}{texto}'.replace('.', ',')


def _rotulos_eixo_x(labels, maximo=MAX_ROTULOS_EIXO_X):
    total = len(labels)
    if total <= maximo:
        return list(labels)
    passo = -(-total // maximo)
    indices = list(range(0, total, passo))
    if indices[-1] != total - 1:
        indices = indices[:-1] + [total - 1]
    visiveis = [''] * total
    for indice in indices:
        visiveis[indice] = labels[indice]
    return visiveis


def _anotar_barras(ax, container, valores, cor, fundo, fontsize=8):
    ax.bar_label(container,
                 labels=[_valor_compacto(valor, com_simbolo=False)
                         for valor in valores],
                 fontsize=fontsize, padding=2, color=cor,
                 rotation=ROTACAO_ROTULOS_BARRAS,
                 path_effects=[path_effects.withStroke(linewidth=2.5,
                                                       foreground=fundo)])


def _curva_suave(xs, valores, pontos=200):
    if len(xs) <= 2:
        return xs, list(valores)
    xs_arr = np.asarray(xs, dtype=float)
    ys_arr = np.asarray(valores, dtype=float)
    x_novo = np.linspace(xs_arr.min(), xs_arr.max(), pontos)
    spline = make_interp_spline(xs_arr, ys_arr, k=min(3, len(xs_arr) - 1))
    return x_novo, spline(x_novo)


def _fonte_rotulos_valor(ax, total_pontos):
    """Fonte dos rotulos de valor, adaptada a densidade do grafico.

    Com as vendas para cima (decisao do usuario) as tres series ficam no
    mesmo hemisferio e os rotulos de meses vizinhos podem se encostar. A
    fonte encolhe conforme o grafico fica denso, para que o rotulo caiba na
    vaga disponivel entre dois pontos.
    """
    if total_pontos <= 8:
        return 8
    figura = ax.get_figure()
    largura_px = figura.get_size_inches()[0] * figura.dpi
    vao_px = (largura_px * 0.85) / total_pontos
    # ~5,25 px de largura por unidade de fonte ("R$ 952 mil" mede ~42 px em 8)
    fonte = int((vao_px * 0.75 - 2) / 5.25)
    return max(6, min(8, fonte))


def _colide_caixas(caixa_a, caixa_b, tolerancia=TOLERANCIA_COLISAO_PX):
    sobreposicao_x = min(caixa_a.x1, caixa_b.x1) - max(caixa_a.x0,
                                                       caixa_b.x0)
    sobreposicao_y = min(caixa_a.y1, caixa_b.y1) - max(caixa_a.y0,
                                                       caixa_b.y0)
    return (sobreposicao_x > tolerancia
            and sobreposicao_y > tolerancia)


def _anotar_ponto(ax, texto, x, valor, deslocamento, cor, fundo, fontsize):
    deslocamento_x, deslocamento_y, alinhamento = deslocamento
    return ax.annotate(
        texto, (x, valor), xytext=(deslocamento_x, deslocamento_y),
        textcoords='offset points', ha='center', va=alinhamento,
        fontsize=fontsize, color=cor,
        path_effects=[path_effects.withStroke(linewidth=2.5,
                                              foreground=fundo)])


def _anotar_linhas(ax, xs, series, cor, fundo, fontsize=8, renderer=None):
    """Rotulos de valor das linhas, sem colisao e dentro da area do grafico."""
    figura = ax.get_figure()
    if renderer is None:
        figura.canvas.draw()
        renderer = figura.canvas.get_renderer()
    area = ax.get_window_extent(renderer)
    caixas = []
    for valores in series:
        for x, valor in zip(xs, valores):
            texto = _valor_compacto(valor, com_simbolo=False)
            for deslocamento in CANDIDATOS_ROTULO_LINHA:
                anotacao = _anotar_ponto(
                    ax, texto, x, valor, deslocamento, cor, fundo, fontsize)
                caixa = anotacao.get_window_extent(renderer)
                dentro = (caixa.x0 >= area.x0 and caixa.x1 <= area.x1
                          and caixa.y0 >= area.y0 and caixa.y1 <= area.y1)
                if dentro and not any(_colide_caixas(caixa, outra)
                                      for outra in caixas):
                    caixas.append(caixa)
                    break
                anotacao.remove()
            else:
                anotacao = _anotar_ponto(
                    ax, texto, x, valor, CANDIDATOS_ROTULO_LINHA[0],
                    cor, fundo, fontsize)
                caixas.append(anotacao.get_window_extent(renderer))


def _expandir_folga_vertical(ax, renderer):
    """Abre o eixo Y o suficiente para nenhum rotulo ser cortado.

    Devolve True se o limite foi alterado (o chamador precisa redesenhar e
    medir de novo).
    """
    caixas = [texto.get_window_extent(renderer) for texto in ax.texts]
    if not caixas:
        return False
    area = ax.get_window_extent(renderer)
    acima = max(caixa.y1 for caixa in caixas) - area.y1
    abaixo = area.y0 - min(caixa.y0 for caixa in caixas)
    if acima <= FOLGA_MINIMA_PX and abaixo <= FOLGA_MINIMA_PX:
        return False
    inferior, superior = ax.get_ylim()
    faixa = superior - inferior
    ax.set_ylim(
        inferior - max(0.0, abaixo) / area.height * faixa,
        superior + max(0.0, acima) / area.height * faixa)
    return True


def _configurar_legenda(ax, cores):
    legenda = ax.legend(fontsize=9, loc='lower center',
                        bbox_to_anchor=(0.5, 1.01), ncol=3, framealpha=1,
                        borderpad=0.4, handletextpad=0.6, columnspacing=1.2)
    moldura = legenda.get_frame()
    moldura.set_facecolor(cores['figura'])
    moldura.set_edgecolor(cores['grade'])
    moldura.set_linewidth(0.8)
    for texto in legenda.get_texts():
        texto.set_color(cores['texto'])
    return legenda


def _desenhar_series(ax, labels, entradas, vendas, diffs, tipo, cores):
    xs = list(range(len(labels)))
    # Vendas, entradas e diferenca vao todas para cima (decisao do usuario
    # em 22/10/2026): os valores sao desenhados como chegam.

    if tipo == 'Linhas':
        for serie, cor in ((entradas, COR_SERIES_ENTRADAS),
                           (vendas, COR_SERIES_VENDAS),
                           (diffs, COR_SERIES_DIFERENCA)):
            xs_s, ys_s = _curva_suave(xs, serie)
            ax.plot(xs_s, ys_s, color=cor, linewidth=2, solid_capstyle='round',
                    solid_joinstyle='round')
        for serie, marcador, cor, rotulo in ((entradas, 's', COR_SERIES_ENTRADAS,
                                               'Entradas'),
                                              (vendas, 'o', COR_SERIES_VENDAS,
                                               'Vendas'),
                                              (diffs, '^', COR_SERIES_DIFERENCA,
                                               'Diferenca')):
            ax.plot(xs, serie, marker=marcador, linestyle='none', color=cor,
                    markersize=5, label=rotulo)
        if len(labels) <= MAX_PONTOS_COM_VALORES:
            ax.margins(y=MARGEM_Y_ROTULOS)
        return

    largura = 0.25
    barra_entradas = ax.bar([x - largura for x in xs], entradas, largura,
                            label='Entradas', color=COR_SERIES_ENTRADAS)
    barra_vendas = ax.bar(xs, vendas, largura,
                          label='Vendas', color=COR_SERIES_VENDAS)
    barra_diferenca = ax.bar([x + largura for x in xs], diffs, largura,
                             label='Diferenca', color=COR_SERIES_DIFERENCA)
    if len(labels) <= MAX_PONTOS_COM_VALORES:
        # Margem extra no eixo Y: os rotulos de valor ficam acima/abaixo das
        # barras e, sem folga, sao cortados nas bordas do grafico.
        ax.margins(y=MARGEM_Y_ROTULOS)
        fonte = _fonte_rotulos_valor(ax, len(labels))
        _anotar_barras(ax, barra_entradas, entradas, cores['texto'],
                       cores['figura'], fonte)
        _anotar_barras(ax, barra_vendas, vendas, cores['texto'],
                       cores['figura'], fonte)
        _anotar_barras(ax, barra_diferenca, diffs, cores['texto'],
                       cores['figura'], fonte)


def adicionar_tooltip(grafico_frame):
    """Tooltip ao passar o mouse sobre barras/pontos do gráfico."""
    try:
        canvas = None
        figura = None
        for widget in grafico_frame.winfo_children():
            if hasattr(widget, 'figure'):
                canvas = widget
                figura = widget.figure
                break
        if canvas is None or figura is None:
            return
        ax = figura.axes[0] if figura.axes else None
        if ax is None:
            return

        tooltip = None
        def _criar_tooltip():
            nonlocal tooltip
            if tooltip is not None:
                try:
                    tooltip.destroy()
                except Exception:
                    logger.debug('Falha ao destruir tooltip antigo.',
                                 exc_info=True)
            tooltip = CTkLabel(grafico_frame, text='', font=('', 9),
                               text_color='#ffffff', fg_color='#1f1f1f',
                               corner_radius=4)
            tooltip.place(x=0, y=0)
            tooltip.lower()

        _criar_tooltip()

        def _formatar(valor):
            return _valor_compacto(valor, com_simbolo=True)

        def _on_move(event):
            if event.inaxes != ax or event.xdata is None or event.ydata is None:
                if tooltip is not None:
                    try:
                        tooltip.place_forget()
                    except Exception:
                        logger.debug('Falha ao esconder o tooltip do gráfico.',
                                     exc_info=True)
                return
            melhor = None
            melhor_dist = None
            for cont in ax.containers:
                try:
                    for barra in cont.patches:
                        bbox = barra.get_bbox()
                        if bbox.xmin <= event.xdata <= bbox.xmax and event.ydata >= 0:
                            dist = abs(event.xdata - bbox.xmid)
                            if melhor_dist is None or dist < melhor_dist:
                                melhor_dist = dist
                                melhor = ('bar', barra.get_height())
                except Exception:
                    logger.debug('Falha ao ler barra do gráfico para o tooltip.',
                                 exc_info=True)
                    continue
            for linha in ax.lines:
                try:
                    dados_x = linha.get_xdata()
                    dados_y = linha.get_ydata()
                    if len(dados_x) == 0:
                        continue
                    idx = np.argmin(np.abs(np.array(dados_x) - event.xdata))
                    dist = abs(float(dados_x[idx]) - float(event.xdata))
                    if melhor_dist is None or dist < melhor_dist:
                        melhor_dist = dist
                        melhor = ('line', float(dados_y[idx]), int(idx))
                except Exception:
                    logger.debug('Falha ao ler linha do gráfico para o tooltip.',
                                 exc_info=True)
                    continue
            if melhor is None or melhor_dist is None or melhor_dist > 0.4:
                if tooltip is not None:
                    try:
                        tooltip.place_forget()
                    except Exception:
                        logger.debug('Falha ao esconder o tooltip (sem alvo).',
                                     exc_info=True)
                return
            if melhor[0] == 'bar':
                texto = _formatar(melhor[1])
            else:
                texto = _formatar(melhor[1])
            try:
                tooltip.configure(text=texto)
                tooltip.place(x=event.guiEvent.x + 12, y=event.guiEvent.y - 12)
                tooltip.lift()
            except Exception:
                logger.debug('Falha ao posicionar o tooltip do gráfico.',
                             exc_info=True)

        def _on_leave(event):
            if tooltip is not None:
                try:
                    tooltip.place_forget()
                except Exception:
                    logger.debug('Falha ao esconder o tooltip ao sair do gráfico.',
                                 exc_info=True)

        canvas.mpl_connect('motion_notify_event', _on_move)
        canvas.mpl_connect('axes_leave_event', _on_leave)
    except Exception:
        logger.debug('Falha ao registrar o tooltip do gráfico.', exc_info=True)


def criar_grafico_tendencia(master, dados, tipo='Barras'):
    cores = _cores()

    if not dados or not dados.get('labels'):
        CTkLabel(master, text='Nenhum dado encontrado para o período!',
                 font=('', 13, 'bold'),
                 text_color=cores['subtexto']).pack(
            expand=True, fill='both')
        return None

    labels = dados['labels']
    vendas = dados['vendas']
    entradas = dados['entradas']
    diffs = dados['diferenca']
    xs = list(range(len(labels)))

    fig = Figure(figsize=_dimensoes_figura(master), dpi=100,
                 facecolor=cores['figura'])
    ax = fig.add_subplot(111)
    ax.set_facecolor(cores['figura'])

    _desenhar_series(ax, labels, entradas, vendas, diffs, tipo, cores)

    ax.set_xticks(xs)
    ax.set_xticklabels(_rotulos_eixo_x(labels), fontsize=9, rotation=0,
                       ha='center')
    ax.axhline(0, color=cores['grade'], linewidth=0.8)
    ax.grid(axis='y', linestyle='--', alpha=0.4, color=cores['grade'])
    ax.set_axisbelow(True)
    _configurar_legenda(ax, cores)
    ax.set_title('Entradas x Vendas x Diferenca', fontsize=10,
                 fontweight='bold', color=cores['texto'], pad=32)
    ax.tick_params(colors=cores['texto'], labelsize=7)
    ax.yaxis.set_major_formatter(
        FuncFormatter(lambda valor, _posicao: _valor_compacto(valor)))
    for borda in ax.spines.values():
        borda.set_color(cores['grade'])

    fig.set_layout_engine('tight')

    canvas = FigureCanvasTkAgg(fig, master=master)
    canvas.draw()
    if tipo == 'Linhas' and len(labels) <= MAX_PONTOS_COM_VALORES:
        _anotar_linhas(ax, xs, (entradas, vendas, diffs), cores['texto'],
                       cores['figura'], FONTE_ROTULOS_LINHA,
                       canvas.get_renderer())
        canvas.draw()
    elif tipo != 'Linhas' and len(labels) <= MAX_PONTOS_COM_VALORES:
        # Rotulos verticais sao mais altos que largos: abre o eixo Y medindo
        # as caixas ja renderizadas para nao cortar nenhum valor.
        for _ in range(MAX_AJUSTES_FOLGA_VERTICAL):
            if not _expandir_folga_vertical(ax, canvas.get_renderer()):
                break
            canvas.draw()
    canvas.get_tk_widget().pack(fill='both', expand=True)
    try:
        toolbar = NavigationToolbar2Tk(canvas, master)
        toolbar.update()
        toolbar.pack(side='bottom', fill='x')
    except Exception:
        logger.debug('Falha ao montar a barra de ferramentas do gráfico.',
                     exc_info=True)
    try:
        adicionar_tooltip(master)
    except Exception:
        logger.debug('Falha ao adicionar tooltip ao gráfico.', exc_info=True)
    return canvas
