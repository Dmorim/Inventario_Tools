# Importar a classe Connect do arquivo Inventario_Conn
from tkinter import messagebox


from Thread_Manager.Query_Operations import query_executor, query_updater
from Thread_Manager.Thread_Executor import thread_execução
from Interface_Tools.Tk_Progress_Bar import ProgressBarHandler
from Thread_Manager.Thread_Executor import atualizar_ui_main
from Outros.Logger.Get_Logger import get_logger
from Data_Manager.PeriodoManager import PeriodoManager
from Queries.Comando_Queries import (
    QUERY_UPDATE_PRECU_PORCENTAGEM,
    QUERY_UPDATE_PRECU_ARREDONDAMENTO,
    QUERY_UPDATE_PRECU_VLDIA,
    QUERY_UPDATE_PRECU_CUSME,
    QUERY_UPDATE_PRECU_ZERADO,
    QUERY_UPDATE_CLASSIFICACAO_NULA,
    QUERY_UPDATE_SALDO_NAO_ZERADO,
    QUERY_UPDATE_CONTROLAESTOQUE_S,
    QUERY_UPDATE_QUANTIDADE_ALTA,
    QUERY_UPDATE_SALDO_NEGATIVO,
    QUERY_UPDATE_DTOPE_IGUAL_DTPRO,
    QUERY_COMANDO_GERAL,
)

logger = get_logger(__name__)


class Funcoes_Comandos:
    def __init__(self, periodo=None):
        self.periodo = periodo
        self.comandos_query = {}
        self.porcent_precu: float = 1.0
        self.precu_vldia: str = '<'
        self.precu_cusme: str = '<'
        self.precu_vldia_preve: str = '<'
        self.com_ger: str = ''

        self.MAIORMENOR = {
            'Maior': '>',
            'Menor': '<'
        }

    def Comandos_Func(self, checkbox_List):
        periodo = None
        if self.periodo is not None:
            if hasattr(self.periodo, 'obter_periodo'):
                periodo = self.periodo.obter_periodo()
            elif hasattr(self.periodo, 'get_periodo'):
                periodo = self.periodo.get_periodo()
        if periodo is None:
            try:
                periodo = PeriodoManager.get_periodo()
            except Exception:
                periodo = None

        inicio_formatado = getattr(
            periodo, 'inicio_formatado', None) if periodo else None

        self.comandos_query = {
            checkbox_List[0]: (QUERY_UPDATE_PRECU_PORCENTAGEM, (self.porcent_precu,)),
            checkbox_List[1]: (QUERY_UPDATE_PRECU_ARREDONDAMENTO, ()),
            checkbox_List[2]: (QUERY_UPDATE_PRECU_VLDIA.format(operador=self.precu_vldia), ()),
            checkbox_List[3]: (QUERY_UPDATE_PRECU_CUSME.format(operador=self.precu_cusme), ()),
            checkbox_List[4]: (QUERY_UPDATE_PRECU_ZERADO.format(campo=self.precu_vldia_preve), ()),
            checkbox_List[5]: (QUERY_UPDATE_CLASSIFICACAO_NULA, ()),
            checkbox_List[6]: (QUERY_UPDATE_SALDO_NAO_ZERADO, ()),
            checkbox_List[7]: (QUERY_UPDATE_CONTROLAESTOQUE_S, (inicio_formatado,)),
            checkbox_List[8]: (QUERY_UPDATE_QUANTIDADE_ALTA, ()),
            checkbox_List[9]: (QUERY_UPDATE_SALDO_NEGATIVO, ()),
            checkbox_List[10]: (QUERY_UPDATE_DTOPE_IGUAL_DTPRO, ()),
            checkbox_List[11]: (
                QUERY_COMANDO_GERAL.format(comando=self.com_ger), ())
        }

    def executa_comandos(self, comando, operacoes, total, status_label):
        resultados = []
        for i, (nome, query, params) in enumerate(operacoes):
            idx = i
            n = nome
            atualizar_ui_main(
                comando,
                lambda i=idx, n=n: status_label.configure(
                    text=f'Executando {i + 1} de {total}: {n}'))
            query_executor(query_updater, query, params)
            resultados.append(nome)
        return resultados

    def on_click_confirm(self, comando, checkbox_List, values_List, confirm_button, status_label):
        def update_finalizado(_):
            logger.info('Finalizando execução dos comandos.')
            atualizar_ui_main(comando, progress_bar.finalizar)
            status_label.configure(
                text=f'{total} comando(s) executado(s) com sucesso.')
            messagebox.showinfo(
                'Aviso', 'Comandos executados com sucesso', parent=comando)
            comando.destroy()

        def update_erro(erro):
            logger.error(f'Erro ao executar os comandos: {erro}')
            atualizar_ui_main(comando, progress_bar.finalizar)
            confirm_button.configure(state='normal', text='Confirmar')
            status_label.configure(text='Erro ao executar os comandos.')
            messagebox.showerror(
                'Erro', f'Erro ao executar os comandos\n{erro}', parent=comando)

        def _montar_operacoes(checkbox_List) -> list:
            return self.montar_operacoes(checkbox_List, comando)

        def centraliza_tela():
            comando.update_idletasks()

            janela_w = 400
            janela_h = 130

            widget_x = comando.winfo_rootx()
            widget_y = comando.winfo_rooty()
            widget_w = comando.winfo_width()
            widget_h = comando.winfo_height()

            x = widget_x + (widget_w - janela_w) // 2
            y = widget_y + (widget_h - janela_h) // 2

            return x, y

        if values_List[0].get() != '':
            self.porcent_precu = values_List[0].get().replace(',', '.')
        else:
            self.porcent_precu = 1

        self.precu_vldia = self.MAIORMENOR.get(values_List[1].get(), '<')
        self.precu_cusme = self.MAIORMENOR.get(values_List[2].get(), '<')

        if values_List[3].get() == 'Preço de Compra':
            self.precu_vldia_preve = 'VLDIA'
        elif values_List[3].get() == 'Custo Médio':
            self.precu_vldia_preve = 'CUSME'
        else:
            self.precu_vldia_preve = 'PREVE - (PREVE * 0.65)'

        self.com_ger = values_List[4].get()

        self.Comandos_Func(checkbox_List)

        if not messagebox.askyesno(
                'Aviso', f'Os seguintes comandos serão executados:\n{self.comandos_true()}\nDeseja continuar?', parent=comando):
            return

        confirm_button.configure(state='disabled')
        progress_x, progress_y = centraliza_tela()
        progress_bar = ProgressBarHandler(
            comando, 'Aguarde', x=progress_x, y=progress_y)

        operacoes = _montar_operacoes(checkbox_List)
        total = len(operacoes)

        if total == 0:
            return

        confirm_button.configure(state='disabled', text='Executando...')

        atualizar_ui_main(comando, progress_bar.create_screen)
        atualizar_ui_main(comando, progress_bar.atualizar_status,
                          'Executando comandos')
        thread_execução(comando, self.executa_comandos,
                        update_finalizado, update_erro, comando, operacoes, total, status_label)

    def montar_operacoes(self, checkbox_List, comando=None) -> list:
        nomes = [
            'Preço de Custo por Porcentagem',
            'Arredondar Preço de Custo',
            'Preço de Custo = Preço de Compra',
            'Preço de Custo = Custo Médio',
            'Preço de Custo zerado',
            'Corrigir Classificação Nula',
            'Zerar Produtos Não Zerados',
            "Setar Controla Estoque 'S'",
            'Corrigir Quantidade Alta',
            'Zerar Saldo Negativo',
            'DTOPE igual DTPRO',
            'Comando Geral',
        ]

        operacoes = []
        arredondamento_adicionado = False
        if not self.comandos_query:
            return operacoes
        try:
            query_arredondamento = self.comandos_query[checkbox_List[1]][0]
        except Exception:
            query_arredondamento = None

        for key, query_param in self.comandos_query.items():
            if key not in checkbox_List or key.get() != 1:
                continue

            try:
                nome = nomes[checkbox_List.index(key)]
            except Exception:
                nome = str(key)

            if key == checkbox_List[1]:
                if not arredondamento_adicionado:
                    operacoes.append((nome, query_param[0], query_param[1]))
                    arredondamento_adicionado = True
            elif key == checkbox_List[11]:
                try:
                    messagebox.showwarning(
                        'Aviso', 'O comando geral irá executar exatamente como digitado, qualquer erro ou consequência do seu uso é de responsabilidade do operador', icon='warning', parent=comando)
                except Exception:
                    pass
                operacoes.append((nome, query_param[0], query_param[1]))
            else:
                operacoes.append((nome, query_param[0], query_param[1]))

                if key in (checkbox_List[2], checkbox_List[3], checkbox_List[4]):
                    if not arredondamento_adicionado and query_arredondamento is not None:
                        operacoes.append(
                            ('Arredondar Preço de Custo', query_arredondamento, ()))
                        arredondamento_adicionado = True

        return operacoes

    def comandos_true(self) -> str:
        key_list = []
        for key in self.comandos_query.keys():
            try:
                if key.get() == 1:
                    key_list.append(self.comandos_query[key][0])
            except Exception:
                continue
        return "".join(key_list)

    @staticmethod
    def precu_porcent_entry_validate(P):
        if P == "":
            return True
        try:
            P2 = P.replace(",", ".")
            price = float(P2)
            s = str(price)
            if '.' not in s:
                s = f"{s}.0"
            int_part, dec_part = s.split(".")
            int_part_clean = int_part.lstrip('+-')
            dec_part_clean = dec_part.rstrip('0') or '0'
            return int_part_clean.isdigit() and dec_part_clean.isdigit() and price >= 0 and len(dec_part_clean) <= 11 and len(int_part_clean) <= 9
        except ValueError:
            return False


# Aliases de compatibilidade (legado/tests)
def Comandos_Func(self, checkbox_List, periodo=None):
    try:
        if periodo is not None:
            fc = Funcoes_Comandos(periodo)
        else:
            fc = Funcoes_Comandos(getattr(self, 'periodo', None))
    except Exception:
        fc = Funcoes_Comandos(periodo)
    try:
        fc.porcent_precu = getattr(self, 'porcent_precu', '1')
        fc.precu_vldia = getattr(self, 'precu_vldia', '<')
        fc.precu_cusme = getattr(self, 'precu_cusme', '<')
        fc.precu_vldia_preve = getattr(self, 'precu_vldia_preve', '<')
        fc.com_ger = getattr(self, 'com_ger', '')
    except Exception:
        pass
    fc.Comandos_Func(checkbox_List)
    try:
        self.comandos_query = fc.comandos_query
        self.porcent_precu = fc.porcent_precu
        self.precu_vldia = fc.precu_vldia
        self.precu_cusme = fc.precu_cusme
        self.precu_vldia_preve = fc.precu_vldia_preve
        self.com_ger = fc.com_ger
    except Exception:
        pass


def comandos_true(self):
    fc = Funcoes_Comandos(getattr(self, 'periodo', None))
    fc.comandos_query = getattr(self, 'comandos_query', {})
    return fc.comandos_true()


def montar_operacoes(self, checkbox_List, comando=None):
    fc = Funcoes_Comandos(getattr(self, 'periodo', None))
    fc.comandos_query = getattr(self, 'comandos_query', {})
    return fc.montar_operacoes(checkbox_List, comando=comando)


def on_click_confirm(periodo, comando, checkbox_List, values_List, confirm_button, status_label):
    fc = Funcoes_Comandos(periodo)
    return fc.on_click_confirm(comando, checkbox_List, values_List, confirm_button, status_label)


def precu_porcent_entry_validate(P):
    return Funcoes_Comandos.precu_porcent_entry_validate(P)
