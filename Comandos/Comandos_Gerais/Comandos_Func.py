# Importar a classe Connect do arquivo Inventario_Conn
from tkinter import messagebox


from Thread_Manager.Query_Operations import query_executor, query_updater
from Thread_Manager.Thread_Executor import thread_execução
from Interface_Tools.Tk_Progress_Bar import ProgressBarHandler
from Thread_Manager.Thread_Executor import atualizar_ui_main
from Outros.Logger.Get_Logger import get_logger
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


def Comandos_Func(self, checkbox_List):
    # Criação de um dicionário associando cada checkbox a um comando
    # Args:
    # self: objeto da classe
    # checkbox_List: lista de checkbox

    self.comandos_query = {
        # Lista de comandos, cada comando é associado a uma checkbox, alguns comandos possuem variáveis que são preenchidas com os valores dos Entry e Combobox
        checkbox_List[0]: (QUERY_UPDATE_PRECU_PORCENTAGEM, (self.porcent_precu,)),
        checkbox_List[1]: (QUERY_UPDATE_PRECU_ARREDONDAMENTO, ()),
        checkbox_List[2]: (QUERY_UPDATE_PRECU_VLDIA.format(operador=self.precu_vldia), ()),
        checkbox_List[3]: (QUERY_UPDATE_PRECU_CUSME.format(operador=self.precu_cusme), ()),
        checkbox_List[4]: (QUERY_UPDATE_PRECU_ZERADO.format(campo=self.precu_vldia_preve), ()),
        checkbox_List[5]: (QUERY_UPDATE_CLASSIFICACAO_NULA, ()),
        checkbox_List[6]: (QUERY_UPDATE_SALDO_NAO_ZERADO, ()),
        checkbox_List[7]: (QUERY_UPDATE_CONTROLAESTOQUE_S, (self.data_banco_inicial,)),
        checkbox_List[8]: (QUERY_UPDATE_QUANTIDADE_ALTA, ()),
        checkbox_List[9]: (QUERY_UPDATE_SALDO_NEGATIVO, ()),
        checkbox_List[10]: (QUERY_UPDATE_DTOPE_IGUAL_DTPRO, ()),
        checkbox_List[11]: (
            QUERY_COMANDO_GERAL.format(comando=self.com_ger), ())
    }


def on_click_confirm(self, comando, checkbox_List, values_List, confirm_button, status_label):
    def executa_comandos():
        resultados = []
        for i, (nome, query, params) in enumerate(operacoes):
            idx = i
            n = nome
            atualizar_ui_main(
                comando,
                lambda i=idx, n=n: status_label.configure(
                    text=f'Executando {i + 1} de {total}: {n}'))
            logger.info(f'Executando comando: {nome}')
            query_executor(query_updater, query, params)
            resultados.append(nome)
        return resultados

    def update_finalizado(_):
        logger.info('Update realizado com sucesso')
        atualizar_ui_main(comando, progress_bar.finalizar)
        status_label.configure(
            text=f'{total} comando(s) executado(s) com sucesso.')
        messagebox.showinfo(
            'Aviso', 'Comandos executados com sucesso', parent=comando)
        comando.destroy()
        logger.info('Comandos finalizados.')

    def update_erro(erro):
        logger.error(f'Erro ao executar os comandos: {erro}')
        atualizar_ui_main(comando, progress_bar.finalizar)
        confirm_button.configure(state='normal', text='Confirmar')
        status_label.configure(text='Erro ao executar os comandos.')
        messagebox.showerror(
            'Erro', f'Erro ao executar os comandos\n{erro}', parent=comando)

    def _montar_operacoes(self, checkbox_List) -> list:
        return montar_operacoes(self, checkbox_List, comando)

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

    if values_List[0].get() != '':  # Verifica se o Entry de porcentagem foi preenchido
        # Preenche a variável porcent_precu com o valor do Entry
        self.porcent_precu = values_List[0].get().replace(
            ',', '.')  # Substitui a vírgula por ponto
    else:
        self.porcent_precu = 1  # Caso o Entry esteja vazio, a porcentagem é 1

    self.MAIORMENOR = {
        'Maior': '>',
        'Menor': '<'
    }

    self.precu_vldia = self.MAIORMENOR.get(values_List[1].get(), '<')
    self.precu_cusme = self.MAIORMENOR.get(values_List[2].get(), '<')

    # Verifica o valor da combobox que seta o preço de custo igual com o preço de compra, ou custo médio ou preço de venda * 0,65 se o saldo estiver zerado
    if values_List[3].get() == 'Preço de Compra':
        self.precu_vldia_preve = 'VLDIA'
    elif values_List[3].get() == 'Custo Médio':
        self.precu_vldia_preve = 'CUSME'
    else:
        self.precu_vldia_preve = 'PREVE - (PREVE * 0.65)'

    self.com_ger = values_List[4].get()

    # Chama a função Comandos_Func para criar os dicionários de comandos
    Comandos_Func(self, checkbox_List)

    # Cria uma messagebox para confirmar a execução dos comandos, a messagem irá contar uma lista com otodos os comandos marcados pelo usuário.
    if not messagebox.askyesno(
            'Aviso', f'Os seguintes comandos serão executados:\n{comandos_true(self)}\nDeseja continuar?', parent=comando):
        return

    confirm_button.configure(state='disabled')
    progress_x, progress_y = centraliza_tela()
    progress_bar = ProgressBarHandler(
        comando, 'Aguarde', x=progress_x, y=progress_y)

    # Monta a lista de operações marcadas, na ordem certa
    operacoes = _montar_operacoes(self, checkbox_List)
    total = len(operacoes)

    if total == 0:
        return

    confirm_button.configure(state='disabled', text='Executando...')

    atualizar_ui_main(comando, progress_bar.create_screen)
    atualizar_ui_main(comando, progress_bar.atualizar_status,
                      'Executando comandos')
    thread_execução(comando, executa_comandos, update_finalizado, update_erro)


def montar_operacoes(self, checkbox_List, comando=None) -> list:
    """
    Retorna uma lista de (nome_legível, query, params) para cada checkbox marcada,
    na ordem correta — respeitando a dependência do arredondamento.
    """

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
    query_arredondamento = self.comandos_query[checkbox_List[1]][0]

    for key, query_param in self.comandos_query.items():
        if key not in checkbox_List or key.get() != 1:
            continue

        nome = nomes[checkbox_List.index(key)]

        if key == checkbox_List[1]:
            if not arredondamento_adicionado:
                operacoes.append((nome, query_param[0], query_param[1]))
                arredondamento_adicionado = True
        elif key == checkbox_List[11]:
            messagebox.showwarning(
                'Aviso', 'O comando geral irá executar exatamente como digitado, qualquer erro ou consequência do seu uso é de responsabilidade do operador', icon='warning', parent=comando)
            operacoes.append((nome, query_param[0], query_param[1]))
        else:
            operacoes.append((nome, query_param[0], query_param[1]))

            # Checkboxes 2, 3 e 4 disparam arredondamento após si mesmos
            if key in (checkbox_List[2], checkbox_List[3], checkbox_List[4]):
                if not arredondamento_adicionado:
                    operacoes.append(
                        ('Arredondar Preço de Custo', query_arredondamento, ()))
                    arredondamento_adicionado = True

    return operacoes


def comandos_true(self) -> str:
    # Função que retorna uma lista com todos os comandos marcados pelo usuário

    key_list = []  # Cria uma lista vazia
    for key in self.comandos_query.keys():  # Itera sobre os itens do dicionário de comandos
        if key.get() == 1:  # Verifica se a checkbox está marcada
            # Adiciona o comando a lista
            key_list.append(self.comandos_query[key][0])
    return "".join(key_list)  # Retorna a lista como uma string

# Validar o valor digitado no Entry como float aceitando virgula na casa decimal e bloqueando o uso de ponto


def precu_porcent_entry_validate(P):
    if P == "":  # Aceita o campo vazio
        return True
    try:
        P = P.replace(",", ".")  # Substitui a virgula por ponto
        price = float(P)  # Tenta converter o valor para float
        # Separa a parte inteira da parte decimal
        int_part, dec_part = str(price).split(".")

        # Verifica se a parte inteira e a parte decimal são digitos e se o valor é positivo bem como seus tamanhos máximos permitos
        return int_part.isdigit() and dec_part.isdigit() and price >= 0 and len(dec_part) <= 11 and len(int_part) <= 9
    except ValueError:
        return False
