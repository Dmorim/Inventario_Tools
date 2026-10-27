import customtkinter as ctk
from tkinter import TclError, messagebox
import datetime
import json
import os

import pyperclip

from Outros.Logger.Get_Logger import get_logger
from Outros.Periodo_Inventario import periodo_tendencia_ultimos_5_anos
from Thread_Manager.Thread_Executor import thread_execução
from Dashboard.Dashboard_Func import carregar_kpis, carregar_dados_tendencia
from Dashboard.Dashboard_Charts import criar_grafico_tendencia

logger = get_logger(__name__)

COR_BG = ('#f0f2f5', "#171E25")
COR_CARD = ('#ffffff', "#2A2C3D")
COR_TEXTO = ("#001425", "#9abbd6")
COR_SUBTEXTO = ('#7f8c8d', "#b7e2e6")
COR_ENTRADAS = ("#1a90f8", "#11efef")
COR_VENDAS = ("#5CA67B", "#2ecc71")
COR_PREVISAO = '#e67e22'
COR_KPI = ("#DADEE2", "#3E3F3F")
COR_KPI_LABEL = ("#17191A", "#e1e6ec")
OPCOES_TIPO_GRAFICO = ['Barras', 'Linhas']
OPCOES_AGRUPAMENTO = ['Mês', 'Ano']
CAMINHO_FILTROS_DASHBOARD = os.path.join(
    os.path.expanduser('~'), '.inventario_tools_dashboard.json')


def _periodo_anterior(inicio, fim):
    """Intervalo imediatamente anterior, com a mesma duração."""
    try:
        duracao = (fim - inicio).days
        fim_anterior = inicio - datetime.timedelta(days=1)
        inicio_anterior = fim_anterior - datetime.timedelta(days=duracao)
        return (inicio_anterior.strftime('%d.%m.%Y'),
                fim_anterior.strftime('%d.%m.%Y'))
    except Exception:
        logger.debug('Falha ao calcular período anterior.', exc_info=True)
        return None, None


def _carregar_filtros_dashboard():
    tipo = OPCOES_TIPO_GRAFICO[0]
    agrupamento = OPCOES_AGRUPAMENTO[1]
    try:
        if os.path.exists(CAMINHO_FILTROS_DASHBOARD):
            with open(CAMINHO_FILTROS_DASHBOARD, 'r', encoding='utf-8') as arquivo:
                dados = json.load(arquivo)
            tipo_lido = dados.get('tipo_grafico', tipo)
            agrupamento_lido = dados.get('agrupamento', agrupamento)
            if tipo_lido in OPCOES_TIPO_GRAFICO:
                tipo = tipo_lido
            if agrupamento_lido in OPCOES_AGRUPAMENTO:
                agrupamento = agrupamento_lido
    except Exception:
        logger.debug(
            'Falha ao ler filtros salvos do dashboard.', exc_info=True)
    return tipo, agrupamento


def _salvar_filtros_dashboard(tipo, agrupamento):
    try:
        with open(CAMINHO_FILTROS_DASHBOARD, 'w', encoding='utf-8') as arquivo:
            json.dump({'tipo_grafico': tipo, 'agrupamento': agrupamento},
                      arquivo, ensure_ascii=False, indent=2)
    except Exception:
        logger.debug('Falha ao salvar filtros do dashboard.', exc_info=True)


def _criar_kpi_card(master, titulo, valor, cor_valor=COR_TEXTO, prefix='',
                    variacao=None, cor_variacao=None):
    card = ctk.CTkFrame(master, fg_color=COR_KPI,
                        corner_radius=8, border_width=1,
                        border_color="#e9e8fa")
    card.pack(side='left', padx=6, pady=4, fill='both', expand=True)

    ctk.CTkLabel(card, text=titulo, font=('', 12),
                 text_color=COR_KPI_LABEL, wraplength=140).pack(
        padx=10, pady=(8, 2), anchor='center')

    valor_texto = prefix + str(valor)

    def _copiar_valor(event=None):
        try:
            texto_copia = f'{titulo}: {valor_texto}'
            pyperclip.copy(texto_copia)
        except Exception:
            logger.debug('Falha ao copiar valor do KPI para o clipboard.', exc_info=True)

    lbl_valor = ctk.CTkLabel(card, text=valor_texto, font=('', 20, 'bold'),
                             text_color=cor_valor, cursor='hand2')
    lbl_valor.pack(padx=10, pady=(2, 0), anchor='center')
    try:
        lbl_valor.bind('<Button-1>', _copiar_valor)
    except Exception:
        logger.debug('Falha ao vincular clique para copia do KPI.', exc_info=True)
    if variacao:
        cor_variacao = cor_variacao or COR_SUBTEXTO
        ctk.CTkLabel(card, text=variacao, font=('', 11, 'bold'),
                     text_color=cor_variacao).pack(padx=10, pady=(0, 8),
                                                   anchor='center')
    else:
        ctk.CTkFrame(card, height=16, fg_color='transparent').pack()
    return card


def _formatar_variacao(atual, anterior):
    try:
        val_atual = float(atual or 0)
        val_anterior = float(anterior or 0)
        if val_anterior == 0:
            return None, None
        perc = ((val_atual - val_anterior) / abs(val_anterior)) * 100
        sinal = '+' if perc >= 0 else ''
        texto = f'{sinal}{perc:.1f}% vs período anterior'
        cor = '#2ecc71' if perc >= 0 else '#e74c3c'
        return texto, cor
    except Exception:
        logger.debug('Falha ao formatar variação do KPI.', exc_info=True)
        return None, None


def _atualizar_dashboard(screen, kpis, cards_frame, kpis_anterior=None):
    try:
        if screen is None or not screen.winfo_exists():
            return
    except (AttributeError, TclError):
        return

    for widget in cards_frame.winfo_children():
        widget.destroy()

    try:
        _criar_kpi_card(cards_frame, 'Valor do Inventário',
                        kpis.get('valor_inventario', '0,00'), COR_TEXTO, 'R$ ')
        v_ven, c_ven = _formatar_variacao(
            kpis.get('valor_vendas_num'), kpis.get('valor_vendas_num_ant'))
        _criar_kpi_card(cards_frame, 'Total de Vendas',
                        kpis.get('valor_vendas', '0,00'), COR_VENDAS, 'R$ ',
                        v_ven, c_ven)
        v_ent, c_ent = _formatar_variacao(
            kpis.get('valor_entradas_num'), kpis.get('valor_entradas_num_ant'))
        _criar_kpi_card(cards_frame, 'Total de Entradas',
                        kpis.get('valor_entradas',
                                 '0,00'), COR_ENTRADAS, 'R$ ',
                        v_ent, c_ent)
        v_v13, c_v13 = _formatar_variacao(
            kpis.get('vendas_130_num'), kpis.get('vendas_130_num_ant'))
        _criar_kpi_card(cards_frame, 'Vendas 1.3',
                        kpis.get('vendas_130', '0,00'), COR_TEXTO, 'R$ ',
                        v_v13, c_v13)
        _criar_kpi_card(cards_frame, 'Previsão de Inventário',
                        kpis.get('previa_inventario',
                                 '0,00'), COR_PREVISAO, 'R$ ',
                        'estimativa do período', COR_SUBTEXTO)
    except Exception:
        logger.exception('Erro ao criar cards do dashboard.')

    try:
        screen.update_idletasks()
        if not screen.winfo_viewable():
            return
        largura = screen.winfo_width()
        altura = screen.winfo_height()
        if largura > 1 and altura > 1:
            screen.geometry(f'{largura}x{altura}')
    except (TclError, AttributeError):
        logger.debug(
            'Falha ao reajustar a geometria do dashboard.', exc_info=True)
    except Exception:
        logger.debug(
            'Falha ao reajustar geometria do dashboard.', exc_info=True)


def _esconder_loading(loading_label):
    """Oculta o rótulo de carregamento respeitando o gerenciador de layout."""
    if loading_label is None:
        return
    try:
        if not loading_label.winfo_exists():
            return
        gerenciador = loading_label.winfo_manager()
        if gerenciador == 'pack':
            loading_label.pack_forget()
        elif gerenciador == 'grid':
            loading_label.grid_forget()
        elif gerenciador == 'place':
            loading_label.place_forget()
    except (TclError, AttributeError):
        logger.debug(
            'Falha ao esconder o rótulo de carregamento do Dashboard.',
            exc_info=True)


def _mostrar_erro_loading(loading_label, texto):
    """Exibe uma mensagem de erro no rótulo, garantindo que ele fique visível."""
    if loading_label is None:
        return
    try:
        if not loading_label.winfo_exists():
            return
        if not loading_label.winfo_manager():
            loading_label.pack(pady=(0, 6))
        loading_label.configure(text=texto, text_color='#e74c3c')
        loading_label.update_idletasks()
    except (TclError, AttributeError):
        logger.debug(
            'Falha ao atualizar o rótulo de erro do Dashboard.',
            exc_info=True)


def _chamar_on_concluir(on_concluir):
    if on_concluir is None:
        return
    try:
        on_concluir()
    except Exception:
        logger.exception('Falha ao concluir o carregamento do Dashboard.')


def _carregar_dados(screen, cards_frame, on_erro, ini, fim, ini_ant=None,
                    fim_ant=None, on_concluir=None):
    def on_erro_seguro(exc):
        try:
            if on_erro is not None:
                on_erro(exc)
        finally:
            _chamar_on_concluir(on_concluir)

    def callback(kpis):
        _atualizar_dashboard(screen, kpis, cards_frame)
        _chamar_on_concluir(on_concluir)

    if ini_ant and fim_ant:
        def callback_comparativo(kpis):
            kpis_atual = kpis[0] if isinstance(kpis, tuple) else kpis
            kpis_ant = kpis[1] if isinstance(kpis, tuple) else {}
            if isinstance(kpis_atual, dict) and isinstance(kpis_ant, dict):
                kpis_atual['valor_inventario_num_ant'] = kpis_ant.get(
                    'valor_inventario_num')
                kpis_atual['valor_vendas_num_ant'] = kpis_ant.get(
                    'valor_vendas_num')
                kpis_atual['valor_entradas_num_ant'] = kpis_ant.get(
                    'valor_entradas_num')
                kpis_atual['vendas_130_num_ant'] = kpis_ant.get(
                    'vendas_130_num')
            _atualizar_dashboard(screen, kpis_atual,
                                 cards_frame)
            _chamar_on_concluir(on_concluir)
        thread_execução(screen, carregar_kpis, callback_comparativo,
                        on_erro_seguro, ini, fim, ini_ant, fim_ant)
        return
    thread_execução(screen, carregar_kpis, callback, on_erro_seguro, ini, fim)


def _renderizar_tendencia(screen, trend_frame, dados, tipo):
    try:
        if screen is None or not screen.winfo_exists():
            return
        if trend_frame is None or not trend_frame.winfo_exists():
            return
    except (AttributeError, TclError):
        return

    for widget in trend_frame.winfo_children():
        widget.destroy()
    try:
        criar_grafico_tendencia(trend_frame, dados, tipo)
    except Exception:
        logger.exception('Erro ao desenhar gráfico de tendência.')
        try:
            if trend_frame.winfo_exists():
                ctk.CTkLabel(trend_frame, text='Erro ao desenhar o gráfico.',
                             font=('', 12), text_color='#e74c3c').pack(expand=True)
        except (TclError, AttributeError):
            logger.debug(
                'Falha ao exibir aviso de erro do gráfico.', exc_info=True)
    try:
        screen.update_idletasks()
    except (TclError, AttributeError):
        logger.debug(
            'Falha ao atualizar o layout depois de desenhar o gráfico.',
            exc_info=True)


def _granularidade_de(agrupamento_var):
    return 'mes' if agrupamento_var.get() == 'Mês' else 'ano'


def _recarregar_tendencia(screen, trend_frame, tipo_var, estado, gran, ini, fim,
                          on_concluir=None):
    estado['seq'] += 1
    seq = estado['seq']

    def callback(dados):
        if seq != estado['seq']:
            _chamar_on_concluir(on_concluir)
            return
        estado['cache'][gran] = dados
        _renderizar_tendencia(screen, trend_frame, dados, tipo_var.get())
        _chamar_on_concluir(on_concluir)

    def on_erro(exc):
        if seq != estado['seq']:
            _chamar_on_concluir(on_concluir)
            return
        logger.exception('Erro ao carregar gráfico de tendência.')
        try:
            for widget in trend_frame.winfo_children():
                widget.destroy()
            ctk.CTkLabel(trend_frame, text=f'Erro ao carregar gráfico: {exc}',
                         font=('', 12), text_color='#e74c3c').pack(expand=True)
        except (TclError, AttributeError):
            logger.debug(
                'Falha ao exibir aviso de erro da tendência.', exc_info=True)
        _chamar_on_concluir(on_concluir)

    thread_execução(screen, carregar_dados_tendencia, callback, on_erro,
                    ini, fim, gran)


def _aplicar_grab_seguro(screen, tentativas=0):
    try:
        if screen is None or not screen.winfo_exists():
            return
        if screen.winfo_viewable():
            try:
                screen.grab_release()
            except Exception:
                logger.debug('Falha ao liberar o grab do dashboard.',
                             exc_info=True)
            try:
                screen.grab_set()
                return
            except Exception:
                logger.debug(
                    'Falha ao aplicar grab_set no dashboard.', exc_info=True)
                return
        if tentativas < 10:
            try:
                screen.after(100, lambda t=tentativas +
                             1: _aplicar_grab_seguro(screen, t))
            except Exception:
                logger.debug('Falha ao reagendar o grab do dashboard.',
                             exc_info=True)
        else:
            try:
                screen.grab_set()
            except Exception:
                logger.debug(
                    'Falha ao aplicar grab_set no dashboard (ultima tentativa).', exc_info=True)
    except (TclError, AttributeError):
        logger.debug(
            'Falha ao aplicar grab do dashboard (widget indisponível).',
            exc_info=True)
    except Exception:
        logger.debug(
            'Erro ao agendar grab seguro do dashboard.', exc_info=True)


def Dashboard_Screen(periodo, parent, button):
    try:
        if button is not None:
            try:
                button.configure(state='disabled')
            except (TclError, AttributeError):
                logger.debug(
                    'Falha ao desabilitar o botão do Dashboard.',
                    exc_info=True)

        screen = ctk.CTkToplevel(parent)
        screen.title('Dashboard - Visao Geral do Inventario')
        screen.geometry('1080x560+80+60')
        screen.minsize(680, 520)
        screen.resizable(True, True)
        try:
            screen.transient(parent)
        except (TclError, AttributeError):
            logger.debug('Falha ao definir o Dashboard como transient.',
                         exc_info=True)
        try:
            screen.focus_set()
        except (TclError, AttributeError):
            logger.debug('Falha ao focar o Dashboard.', exc_info=True)

        try:
            screen.update_idletasks()
        except (TclError, AttributeError):
            logger.debug('Falha ao atualizar o layout do Dashboard.',
                         exc_info=True)

        def _fechar_dashboard_seguro():
            try:
                if button is not None:
                    try:
                        button.configure(state='normal')
                    except (TclError, AttributeError):
                        logger.debug(
                            'Falha ao reabilitar o botão ao fechar o Dashboard.',
                            exc_info=True)
            finally:
                try:
                    screen.grab_release()
                except Exception:
                    logger.debug(
                        'Falha ao liberar o grab ao fechar o Dashboard.',
                        exc_info=True)
                try:
                    if screen.winfo_exists():
                        screen.destroy()
                except Exception:
                    logger.debug(
                        'Falha ao destruir a janela do Dashboard.',
                        exc_info=True)
                    try:
                        screen.destroy()
                    except Exception:
                        logger.debug(
                            'Falha ao destruir a janela do Dashboard na '
                            'segunda tentativa.', exc_info=True)

        screen.protocol('WM_DELETE_WINDOW', _fechar_dashboard_seguro)
        screen.bind('<Escape>', lambda e: _fechar_dashboard_seguro())

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

        tipo_salvo, agrupamento_salvo = _carregar_filtros_dashboard()
        tipo_label = ctk.CTkLabel(
            controls_frame, text='Tipo de gráfico:',
            font=('', 12), text_color=COR_SUBTEXTO)
        tipo_label.pack(side='left', padx=(9, 4))
        tipo_var = ctk.StringVar(value=tipo_salvo)
        tipo_combo = ctk.CTkComboBox(
            controls_frame, variable=tipo_var, values=OPCOES_TIPO_GRAFICO,
            width=110, font=('', 12), state='readonly')
        tipo_combo.pack(side='left', padx=(0, 18))

        agrupamento_label = ctk.CTkLabel(
            controls_frame, text='Agrupar por:',
            font=('', 12), text_color=COR_SUBTEXTO)
        agrupamento_label.pack(side='left', padx=(0, 4))
        agrupamento_var = ctk.StringVar(value=agrupamento_salvo)
        agrupamento_combo = ctk.CTkComboBox(
            controls_frame, variable=agrupamento_var, values=OPCOES_AGRUPAMENTO,
            width=100, font=('', 12), state='readonly')
        agrupamento_combo.pack(side='left')

        btn_maximizar = ctk.CTkButton(
            controls_frame, text='Maximizar', width=95,
            command=lambda: _alternar_maximizar(screen, btn_maximizar))
        btn_maximizar.pack(side='right', padx=(0, 9))

        trend_frame = ctk.CTkFrame(
            content_frame, fg_color=COR_CARD, corner_radius=8,
            border_width=1, border_color='#e0e0e0')
        trend_frame.pack(fill='both', expand=True, pady=(6, 0))

        def _alternar_maximizar(janela, botao):
            try:
                estado_janela = janela.state()
                if estado_janela == 'zoomed':
                    janela.state('normal')
                    botao.configure(text='Maximizar')
                else:
                    try:
                        janela.state('zoomed')
                    except Exception:
                        largura = janela.winfo_screenwidth() - 10
                        altura = janela.winfo_screenheight() - 40
                        janela.geometry(f'{largura}x{altura}+0+0')
                    botao.configure(text='Restaurar')
            except Exception:
                logger.debug(
                    'Falha ao alternar maximizar do dashboard.', exc_info=True)

        estado = {'seq': 0, 'cache': {}, 'pendentes': 0, 'erro': False}

        def _iniciar_carga():
            estado['pendentes'] = estado.get('pendentes', 0) + 1

        def _concluir_carga():
            estado['pendentes'] = max(0, estado.get('pendentes', 0) - 1)
            if estado['pendentes'] == 0 and not estado.get('erro'):
                _esconder_loading(loading_label)

        try:
            ini_kpi = periodo.inicio_formatado
            fim_kpi = periodo.fim_formatado
            ini_kpi_ant, fim_kpi_ant = _periodo_anterior(
                periodo.inicio, periodo.fim)
            ini_tendencia, fim_tendencia = periodo_tendencia_ultimos_5_anos(
                periodo.fim)
        except Exception:
            logger.exception('Erro ao calcular períodos do dashboard.')
            try:
                if button is not None:
                    button.configure(state='normal')
            except Exception:
                logger.debug(
                    'Falha ao reabilitar o botão após erro de período.',
                    exc_info=True)
            try:
                if screen.winfo_exists():
                    screen.destroy()
            except Exception:
                logger.debug(
                    'Falha ao destruir a janela após erro de período.',
                    exc_info=True)
            try:
                messagebox.showerror(
                    'Dashboard', 'Não foi possível calcular os períodos para o dashboard.')
            except Exception:
                logger.debug(
                    'Falha ao exibir mensagem de erro de período.',
                    exc_info=True)
            return

        def carregar_tendencia(_=None):
            try:
                if agrupamento_var is None:
                    return
                try:
                    _salvar_filtros_dashboard(
                        tipo_var.get(), agrupamento_var.get())
                except Exception:
                    logger.debug(
                        'Falha ao salvar os filtros do dashboard.',
                        exc_info=True)
                gran = _granularidade_de(agrupamento_var)
                dados = estado.get('cache', {}).get(gran)
                if dados is not None:
                    _renderizar_tendencia(
                        screen, trend_frame, dados, tipo_var.get())
                    return
                _iniciar_carga()
                _recarregar_tendencia(
                    screen, trend_frame, tipo_var, estado,
                    gran, ini_tendencia, fim_tendencia,
                    on_concluir=_concluir_carga)
            except Exception:
                logger.exception(
                    'Erro ao agendar carregamento da tendência do dashboard.')
                estado['erro'] = True
                _mostrar_erro_loading(
                    loading_label, 'Erro ao iniciar o gráfico do dashboard.')

        try:
            tipo_combo.configure(command=carregar_tendencia)
            agrupamento_combo.configure(command=carregar_tendencia)
        except (TclError, AttributeError):
            logger.debug(
                'Falha ao ligar os eventos dos combos do Dashboard.',
                exc_info=True)

        def on_erro(exc):
            estado['erro'] = True
            _mostrar_erro_loading(
                loading_label, f'Erro ao carregar dados: {exc}')
            logger.exception('Erro ao carregar dados do dashboard.')

        try:
            screen.update_idletasks()
        except (TclError, AttributeError):
            logger.debug(
                'Falha ao atualizar o layout antes de carregar os dados.',
                exc_info=True)

        try:
            _aplicar_grab_seguro(screen)
        except Exception:
            logger.debug('Falha ao agendar grab do dashboard.', exc_info=True)

        try:
            _iniciar_carga()
            _carregar_dados(
                screen, cards_frame, on_erro,
                ini_kpi, fim_kpi, ini_kpi_ant, fim_kpi_ant,
                on_concluir=_concluir_carga)
        except Exception:
            logger.exception(
                'Erro ao iniciar carregamento dos KPIs do dashboard.')
            estado['erro'] = True
            _mostrar_erro_loading(
                loading_label, 'Erro ao iniciar carregamento dos dados.')

        try:
            carregar_tendencia()
        except Exception:
            logger.exception(
                'Erro ao iniciar carregamento da tendência do dashboard.')
    except Exception:
        logger.exception('Falha crítica ao abrir o Dashboard.')
        try:
            if button is not None:
                try:
                    button.configure(state='normal')
                except (TclError, AttributeError):
                    logger.debug(
                        'Falha ao reabilitar o botão após falha crítica.',
                        exc_info=True)
        except Exception:
            logger.debug(
                'Falha ao reabilitar o botão do Dashboard (falha crítica).',
                exc_info=True)
        try:
            messagebox.showerror(
                'Dashboard', 'Não foi possível abrir o Dashboard.')
        except Exception:
            logger.debug(
                'Falha ao exibir mensagem de falha crítica do Dashboard.',
                exc_info=True)
        return
