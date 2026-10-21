from customtkinter import CTkLabel
from customtkinter import get_appearance_mode
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from matplotlib.ticker import FuncFormatter
import matplotlib
matplotlib.use('Agg')


COR_SERIES_VENDAS = '#2ecc71'
COR_SERIES_ENTRADAS = '#3498db'
COR_SERIES_DIFERENCA = '#e74c3c'

MAX_ROTULOS_EIXO_X = 16
MAX_PONTOS_COM_VALORES = 12

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


def _anotar_barras(ax, container, valores, cor, fundo):
    ax.bar_label(container,
                 labels=[_valor_compacto(valor, com_simbolo=False)
                         for valor in valores],
                 fontsize=6, padding=2, color=cor,
                 bbox=dict(facecolor=fundo, edgecolor='none',
                           alpha=0.85, pad=1.2))


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

    vendas_negativo = [-v for v in vendas]

    if tipo == 'Linhas':
        ax.plot(xs, entradas, marker='s', label='Entradas',
                color=COR_SERIES_ENTRADAS, linewidth=2)
        ax.plot(xs, vendas_negativo, marker='o', label='Vendas',
                color=COR_SERIES_VENDAS, linewidth=2)
        ax.plot(xs, diffs, marker='^', label='Diferenca',
                color=COR_SERIES_DIFERENCA, linewidth=2)
    else:
        largura = 0.25
        barra_entradas = ax.bar([x - largura for x in xs], entradas, largura,
                                 label='Entradas', color=COR_SERIES_ENTRADAS)
        barra_vendas = ax.bar(xs, vendas_negativo, largura,
                               label='Vendas', color=COR_SERIES_VENDAS)
        barra_diferenca = ax.bar([x + largura for x in xs], diffs, largura,
                                 label='Diferenca', color=COR_SERIES_DIFERENCA)
        if len(labels) <= MAX_PONTOS_COM_VALORES:
            _anotar_barras(ax, barra_entradas, entradas, cores['texto'],
                           cores['figura'])
            _anotar_barras(ax, barra_vendas, vendas_negativo, cores['texto'],
                           cores['figura'])
            _anotar_barras(ax, barra_diferenca, diffs, cores['texto'],
                           cores['figura'])

    ax.set_xticks(xs)
    ax.set_xticklabels(_rotulos_eixo_x(labels), fontsize=7, rotation=45,
                       ha='right')
    ax.axhline(0, color=cores['grade'], linewidth=0.8)
    ax.grid(axis='y', linestyle='--', alpha=0.4, color=cores['grade'])
    ax.set_axisbelow(True)
    legenda = ax.legend(fontsize=9, loc='best', framealpha=1,
                        borderpad=0.5, handletextpad=0.8, labelspacing=0.4)
    moldura = legenda.get_frame()
    moldura.set_facecolor(cores['figura'])
    moldura.set_edgecolor(cores['grade'])
    moldura.set_linewidth(0.8)
    for texto in legenda.get_texts():
        texto.set_color(cores['texto'])
    ax.set_title('Entradas x Vendas x Diferenca', fontsize=10,
                 fontweight='bold', color=cores['texto'])
    ax.tick_params(colors=cores['texto'], labelsize=7)
    ax.yaxis.set_major_formatter(
        FuncFormatter(lambda valor, _posicao: _valor_compacto(valor)))
    for borda in ax.spines.values():
        borda.set_color(cores['grade'])

    fig.set_layout_engine('tight')

    canvas = FigureCanvasTkAgg(fig, master=master)
    canvas.draw()
    canvas.get_tk_widget().pack(fill='both', expand=True)
    return canvas
