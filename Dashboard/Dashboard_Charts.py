from customtkinter import CTkLabel
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib
matplotlib.use('Agg')


COR_SERIES_VENDAS = '#2ecc71'
COR_SERIES_ENTRADAS = '#3498db'
COR_SERIES_DIFERENCA = '#e74c3c'


def _dimensoes_figura(master, dpi=100, minimo=(4.0, 2.0)):
    largura = master.winfo_width()
    altura = master.winfo_height()
    if largura <= 1 or altura <= 1:
        return minimo
    return (max(largura / dpi, minimo[0]), max(altura / dpi, minimo[1]))


def criar_grafico_tendencia(master, dados, tipo='Barras'):
    if not dados or not dados.get('labels'):
        CTkLabel(master, text='Nenhum dado encontrado para o período!',
                 font=('', 13, 'bold'), text_color='#7f8c8d').pack(
            expand=True, fill='both')
        return None

    labels = dados['labels']
    vendas = dados['vendas']
    entradas = dados['entradas']
    diffs = dados['diferenca']
    xs = list(range(len(labels)))

    fig = Figure(figsize=_dimensoes_figura(master), dpi=100, facecolor='white')
    ax = fig.add_subplot(111)

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
        ax.bar([x - largura for x in xs], entradas, largura,
               label='Entradas', color=COR_SERIES_ENTRADAS)
        ax.bar(xs, vendas_negativo, largura,
               label='Vendas', color=COR_SERIES_VENDAS)
        ax.bar([x + largura for x in xs], diffs, largura,
               label='Diferenca', color=COR_SERIES_DIFERENCA)

    ax.set_xticks(xs)
    ax.set_xticklabels(labels, fontsize=7, rotation=45, ha='right')
    ax.axhline(0, color='#bdc3c7', linewidth=0.8)
    ax.grid(axis='y', linestyle='--', alpha=0.4)
    ax.set_axisbelow(True)
    ax.legend(fontsize=8, loc='best')
    ax.set_title('Entradas x Vendas x Diferenca', fontsize=10,
                 fontweight='bold', color='#2c3e50')

    fig.tight_layout()

    canvas = FigureCanvasTkAgg(fig, master=master)
    canvas.draw()
    canvas.get_tk_widget().pack(fill='both', expand=True)
    return canvas
