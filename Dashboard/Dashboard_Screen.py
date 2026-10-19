import customtkinter as ctk

from Outros.Logger.Get_Logger import get_logger
from Outros.Periodo_Inventario import periodo_tendencia_ultimos_5_anos
from Thread_Manager.Thread_Executor import thread_execução
from Dashboard.Dashboard_Func import carregar_kpis, carregar_dados_tendencia
from Dashboard.Dashboard_Charts import criar_grafico_tendencia

logger = get_logger(__name__)

COR_BG = ('#f0f2f5', "#171E25")
COR_CARD = ('#ffffff', "#2A2C3D")
COR_TEXTO = ('#2c3e50', "#5fabe9")
COR_SUBTEXTO = ('#7f8c8d', "#b7e2e6")
COR_DESTAQUE = '#3498db'
COR_KPI = ("#393B3D", "#3E3F3F")
COR_KPI_LABEL = ("#b7e2e6", "#e1e6ec")
OPCOES_TIPO_GRAFICO = ['Barras', 'Linhas']
OPCOES_AGRUPAMENTO = ['Mês', 'Ano']


def _fechar_dashboard(screen, button):
    button.configure(state='normal')
    screen.destroy()


def _criar_kpi_card(master, titulo, valor, cor_valor=COR_TEXTO, prefix=''):
    card = ctk.CTkFrame(master, fg_color=COR_KPI,
                        corner_radius=8, border_width=1,
                        border_color="#e9e8fa")
    card.pack(side='left', padx=6, pady=4, fill='both', expand=True)

    ctk.CTkLabel(card, text=titulo, font=('', 12),
                 text_color=COR_KPI_LABEL, wraplength=140).pack(
        padx=10, pady=(8, 2), anchor='center')
    ctk.CTkLabel(card, text=prefix + str(valor), font=('', 20, 'bold'),
                 text_color=cor_valor).pack(padx=10, pady=(2, 8), anchor='center')
    return card


def _atualizar_dashboard(screen, kpis, cards_frame):
    for widget in cards_frame.winfo_children():
        widget.destroy()

    _criar_kpi_card(cards_frame, 'Valor do Inventario',
                    kpis['valor_inventario'], COR_DESTAQUE, 'R$ ')
    _criar_kpi_card(cards_frame, 'Total de Vendas',
                    kpis['valor_vendas'], COR_TEXTO, 'R$ ')
    _criar_kpi_card(cards_frame, 'Total de Entradas',
                    kpis['valor_entradas'], COR_TEXTO, 'R$ ')
    _criar_kpi_card(cards_frame, 'Vendas 1.3',
                    kpis['vendas_130'], COR_TEXTO, 'R$ ')
    _criar_kpi_card(cards_frame, 'Previsão de Inventario',
                    kpis['previa_inventario'], COR_TEXTO, 'R$ ')

    screen.update_idletasks()
    screen.geometry(f'{screen.winfo_width()}x{screen.winfo_height()}')


def _carregar_dados(screen, cards_frame, on_erro, ini, fim):
    logger.info('Iniciando carregamento assincrono dos dados do dashboard.')

    def callback(kpis):
        _atualizar_dashboard(screen, kpis, cards_frame)

    thread_execução(screen, carregar_kpis, callback, on_erro, ini, fim)


def _recarregar_tendencia(screen, trend_frame, tipo_var, agrupamento_var, estado, ini, fim):
    estado['seq'] += 1
    seq = estado['seq']
    tipo = tipo_var.get()
    gran = 'mes' if agrupamento_var.get() == 'Mês' else 'ano'

    def callback(dados):
        if seq != estado['seq']:
            return
        for widget in trend_frame.winfo_children():
            widget.destroy()
        criar_grafico_tendencia(trend_frame, dados, tipo)
        screen.update_idletasks()

    def on_erro(exc):
        if seq != estado['seq']:
            return
        logger.exception('Erro ao carregar gráfico de tendência.')
        for widget in trend_frame.winfo_children():
            widget.destroy()
        ctk.CTkLabel(trend_frame, text=f'Erro ao carregar gráfico: {exc}',
                     font=('', 12), text_color='#e74c3c').pack(expand=True)

    thread_execução(screen, carregar_dados_tendencia, callback, on_erro,
                    ini, fim, gran)


def Dashboard_Screen(periodo, parent, button):
    button.configure(state='disabled')

    screen = ctk.CTkToplevel(parent)
    screen.title('Dashboard - Visao Geral do Inventario')
    screen.geometry('1080x560+80+60')
    screen.minsize(680, 520)
    screen.resizable(True, True)
    screen.transient(parent)
    screen.focus_set()
    screen.grab_set()

    screen.protocol('WM_DELETE_WINDOW',
                    lambda: _fechar_dashboard(screen, button))
    screen.bind('<Escape>',
                lambda e: _fechar_dashboard(screen, button))

    title_label = ctk.CTkLabel(
        screen, text='Dashboard - Visao Geral do Inventario',
        font=('', 20, 'bold'), text_color=COR_TEXTO)
    title_label.pack(pady=(12, 4))

    loading_label = ctk.CTkLabel(
        screen, text='Carregando dados...',
        font=('', 13), text_color=COR_SUBTEXTO)
    loading_label.pack(pady=(0, 6))

    content_frame = ctk.CTkFrame(screen, fg_color=COR_BG)
    content_frame.pack(fill='both', expand=True, padx=10, pady=(0, 10))

    cards_frame = ctk.CTkFrame(content_frame, fg_color=COR_BG)
    cards_frame.pack(fill='x', pady=(0, 4))

    controls_frame = ctk.CTkFrame(content_frame, fg_color=COR_BG)
    controls_frame.pack(fill='x', pady=(6, 0))

    tipo_label = ctk.CTkLabel(
        controls_frame, text='Tipo de gráfico:',
        font=('', 12), text_color=COR_SUBTEXTO)
    tipo_label.pack(side='left', padx=(0, 4))
    tipo_var = ctk.StringVar(value=OPCOES_TIPO_GRAFICO[0])
    tipo_combo = ctk.CTkComboBox(
        controls_frame, variable=tipo_var, values=OPCOES_TIPO_GRAFICO,
        width=110, font=('', 12), state='readonly')
    tipo_combo.pack(side='left', padx=(0, 18))

    agrupamento_label = ctk.CTkLabel(
        controls_frame, text='Agrupar por:',
        font=('', 12), text_color=COR_SUBTEXTO)
    agrupamento_label.pack(side='left', padx=(0, 4))
    agrupamento_var = ctk.StringVar(value=OPCOES_AGRUPAMENTO[1])
    agrupamento_combo = ctk.CTkComboBox(
        controls_frame, variable=agrupamento_var, values=OPCOES_AGRUPAMENTO,
        width=100, font=('', 12), state='readonly')
    agrupamento_combo.pack(side='left')

    trend_frame = ctk.CTkFrame(
        content_frame, fg_color=COR_CARD, corner_radius=8,
        border_width=1, border_color='#e0e0e0')
    trend_frame.pack(fill='both', expand=True, pady=(6, 0))

    estado = {'seq': 0}

    ini_kpi = periodo.inicio_formatado
    fim_kpi = periodo.fim_formatado
    ini_tendencia, fim_tendencia = periodo_tendencia_ultimos_5_anos(periodo.fim)

    def carregar_tendencia(_=None):
        _recarregar_tendencia(screen, trend_frame,
                              tipo_var, agrupamento_var, estado,
                              ini_tendencia, fim_tendencia)

    tipo_combo.configure(command=carregar_tendencia)
    agrupamento_combo.configure(command=carregar_tendencia)

    def on_erro(exc):
        loading_label.configure(text=f'Erro ao carregar dados: {exc}')
        logger.exception('Erro ao carregar dados do dashboard.')

    _carregar_dados(
        screen, cards_frame, on_erro,
        ini_kpi, fim_kpi)
    carregar_tendencia()
