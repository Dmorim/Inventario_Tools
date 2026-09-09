import matplotlib
matplotlib.use('Agg')

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from Outros.Logger.Get_Logger import get_logger

logger = get_logger(__name__)

COR_SERIES_VENDAS = '#3498db'
COR_SERIES_ENTRADAS = '#2ecc71'
COR_SERIES_DIFERENCA = '#e74c3c'


def criar_grafico_tendencia(master, dados, tipo='Barras'):
    logger.info('Criando gráfico de tendência. tipo=%s', tipo)
    if not dados or not dados.get('labels'):
        from customtkinter import CTkLabel
        CTkLabel(master, text='Nenhum dado encontrado para o período!',
                 font=('', 13, 'bold'), text_color='#7f8c8d').pack(
            expand=True, fill='both')
        return None

    labels = dados['labels']
    vendas = dados['vendas']
    entradas = dados['entradas']
    diffs = dados['diferenca']
    xs = list(range(len(labels)))

    fig = Figure(figsize=(7.0, 2.8), dpi=100, facecolor='white')
    ax = fig.add_subplot(111)

    if tipo == 'Linhas':
        ax.plot(xs, vendas, marker='o', label='Vendas',
                color=COR_SERIES_VENDAS, linewidth=2)
        ax.plot(xs, entradas, marker='s', label='Entradas',
                color=COR_SERIES_ENTRADAS, linewidth=2)
        ax.plot(xs, diffs, marker='^', label='Diferenca',
                color=COR_SERIES_DIFERENCA, linewidth=2)
    else:
        largura = 0.25
        ax.bar([x - largura for x in xs], vendas, largura,
               label='Vendas', color=COR_SERIES_VENDAS)
        ax.bar(xs, entradas, largura,
               label='Entradas', color=COR_SERIES_ENTRADAS)
        ax.bar([x + largura for x in xs], diffs, largura,
               label='Diferenca', color=COR_SERIES_DIFERENCA)

    ax.set_xticks(xs)
    ax.set_xticklabels(labels, fontsize=7, rotation=45, ha='right')
    ax.axhline(0, color='#bdc3c7', linewidth=0.8)
    ax.grid(axis='y', linestyle='--', alpha=0.4)
    ax.set_axisbelow(True)
    ax.legend(fontsize=8, loc='best')
    ax.set_title('Vendas x Entradas x Diferenca', fontsize=10,
                 fontweight='bold', color='#2c3e50')

    fig.subplots_adjust(left=0.08, right=0.97, top=0.9, bottom=0.26)

    canvas = FigureCanvasTkAgg(fig, master=master)
    canvas.draw()
    canvas.get_tk_widget().pack(fill='both', expand=True)
    logger.info('Gráfico de tendência criado.')
    return canvas
