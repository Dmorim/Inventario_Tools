import math
import matplotlib
matplotlib.use('Agg')

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from Outros.Logger.Get_Logger import get_logger

logger = get_logger(__name__)


def _cor_saude(percentual):
    if percentual > 90:
        return '#2ecc71'
    if percentual >= 70:
        return '#f1c40f'
    return '#e74c3c'


def criar_grafico_saude(master, saude):
    logger.info('Criando gráfico de saúde: %.1f%%', saude)
    fig = Figure(figsize=(3.2, 2.2), dpi=100, facecolor='white')
    ax = fig.add_subplot(111)
    ax.set_xlim(-1.2, 1.2)
    ax.set_ylim(-0.3, 1.2)
    ax.set_aspect('equal')
    ax.axis('off')

    n_sectors = 20
    sector_angle = math.pi / n_sectors

    for i in range(n_sectors):
        theta1 = math.pi + i * sector_angle
        theta2 = math.pi + (i + 1) * sector_angle
        fraction = i / n_sectors
        if fraction < 0.3:
            color = '#e74c3c'
        elif fraction < 0.7:
            color = '#f1c40f'
        else:
            color = '#2ecc71'
        x0, y0 = 0, 0
        verts = [(x0, y0)]
        steps = 20
        for s in range(steps + 1):
            t = theta1 + (theta2 - theta1) * s / steps
            verts.append((math.cos(t), math.sin(t)))
        verts.append((x0, y0))
        xs = [v[0] for v in verts]
        ys = [v[1] for v in verts]
        ax.fill(xs, ys, color=color, alpha=0.85)

    cor_agulha = _cor_saude(saude)
    raio = 0.75
    angulo = math.pi + (saude / 100) * math.pi
    ax.plot([0, raio * math.cos(angulo)], [0, raio * math.sin(angulo)],
            color=cor_agulha, linewidth=3, solid_capstyle='round')
    ax.plot(raio * math.cos(angulo), raio * math.sin(angulo),
            'o', color=cor_agulha, markersize=8, zorder=5)
    ax.plot(0, 0, 'o', color='#2c3e50', markersize=10, zorder=6)

    ax.text(0, -0.15, f'{saude:.0f}%', ha='center', va='center',
            fontsize=18, fontweight='bold', color=cor_agulha)
    ax.text(0, -0.27, 'Saude do Banco', ha='center', va='center',
            fontsize=8, color='#7f8c8d')

    fig.subplots_adjust(left=0.05, right=0.95, top=0.95, bottom=0.05)

    canvas = FigureCanvasTkAgg(fig, master=master)
    canvas.draw()
    canvas.get_tk_widget().pack(fill='both', expand=True)
    logger.info('Gráfico de saúde criado.')
    return canvas


def criar_grafico_problemas(master, problemas):
    logger.info('Criando gráfico de problemas.')
    dados = {k: v for k, v in problemas.items() if v > 0}

    if not dados:
        from customtkinter import CTkLabel
        CTkLabel(master, text='Nenhum problema encontrado!',
                 font=('', 14, 'bold'), text_color='#2ecc71').pack(
            expand=True, fill='both')
        return None

    labels = list(dados.keys())
    values = list(dados.values())
    colors = ['#e74c3c', '#e67e22', '#9b59b6', '#3498db', '#1abc9c']
    explode = [0.03] * len(labels)

    fig = Figure(figsize=(4.5, 2.2), dpi=100, facecolor='white')
    ax = fig.add_subplot(111)

    wedges, texts, autotexts = ax.pie(
        values, labels=labels, autopct='%1.0f%%',
        colors=colors[:len(labels)], explode=explode,
        startangle=90, textprops={'fontsize': 6},
        pctdistance=0.75, labeldistance=1.12,
        wedgeprops={'linewidth': 0.5, 'edgecolor': 'white'})

    for at in autotexts:
        at.set_fontsize(5.5)
        at.set_fontweight('bold')
        at.set_color('white')

    ax.set_title('Distribuicao de Problemas', fontsize=9,
                 fontweight='bold', color='#2c3e50', pad=8)

    fig.subplots_adjust(left=0.05, right=0.95, top=0.88, bottom=0.05)

    canvas = FigureCanvasTkAgg(fig, master=master)
    canvas.draw()
    canvas.get_tk_widget().pack(fill='both', expand=True)
    logger.info('Gráfico de problemas criado.')
    return canvas
