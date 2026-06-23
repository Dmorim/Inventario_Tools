def Comandos_Func(self, checkbox_List):
    # Criação de um dicionário associando cada checkbox a um comando
    # Args:
    # self: objeto da classe
    # checkbox_List: lista de checkbox

    self.comandos_query = {
        # Lista de comandos, cada comando é associado a uma checkbox, alguns comandos possuem variáveis que são preenchidas com os valores dos Entry e Combobox
        checkbox_List[0]: f'UPDATE IN01PRO SET PRECU = PRECU * {self.porcent_precu}',
        checkbox_List[1]: f'UPDATE IN01PRO SET PRECU = CAST(PRECU AS NUMERIC(15, 2))',
        checkbox_List[2]: f'UPDATE IN01PRO SET PRECU = VLDIA WHERE VLDIA {self.precu_vldia} VLDIA AND VLDIA > 0',
        checkbox_List[3]: f'UPDATE IN01PRO SET PRECU = CUSME WHERE CUSME {self.precu_cusme} CUSME AND CUSME > 0',
        checkbox_List[4]: f'UPDATE IN01PRO SET PRECU = {self.precu_vldia_preve} WHERE (PRECU = 0 OR PRECU IS NULL) AND SALDO > 0 AND PREVE <> 0',
        checkbox_List[5]: f'UPDATE IN01PRO SET CLASSIFICACAO_PRODUTO = 00 WHERE CLASSIFICACAO_PRODUTO IS NULL',
        checkbox_List[6]: f'UPDATE IN01PRO SET SALDO = 0 WHERE SALDO BETWEEN 0.000001 AND 0.01',
        checkbox_List[7]: f"UPDATE IN01LAN SET CONTROLAESTOQUE = 'S' WHERE (CONTROLAESTOQUE IS NULL OR CONTROLAESTOQUE = 'N') AND DTPRO >= '{self.data_banco_inicial}'",
        checkbox_List[8]: f'UPDATE IN01LAN SET QUANT = 1 WHERE QUANT > 999999 OR VALOR > 999999',
        checkbox_List[9]: f'UPDATE IN01PRO SET SALDO = 0 WHERE SALDO < 0',
        checkbox_List[10]: f"UPDATE IN01LAN SET DTOPE = DTPRO WHERE VENDA = 'J' AND DTOPE <> DTPRO",
        checkbox_List[11]: self.com_ger
    }


def on_click_confirm(self, comando, checkbox_List, values_List, confirm_button, status_label):
    # Função chamada ao apertar o botão de confirmar, itera sobre os itens da combobox e executa os comandos marcados
    # Args:
    # self: objeto da classe
    # comando: janela do tkinter
    # checkbox_List: lista de checkbox da aba comandos
    # values_List: lista de valores da aba comandos

    def executa_comandos():
        resultados = []
        for i, (nome, query) in enumerate(operacoes):
            idx = i
            n   = nome
            comando.after(0, lambda i=idx, n=n: status_label.configure(
                text=f'Executando {i + 1} de {total}: {n}'))
            query_executor(query_updater, query)
            resultados.append(nome)
        return resultados

    def update_finalizado(_):
        status_label.configure(text=f'{total} comando(s) executado(s) com sucesso.')
        messagebox.showinfo('Aviso', 'Comandos executados com sucesso', parent=comando)
        comando.destroy()

    def update_erro(erro):
        confirm_button.configure(state='normal', text='Confirmar')
        status_label.configure(text='Erro ao executar os comandos.')
        messagebox.showerror('Erro', f'Erro ao executar os comandos\n{erro}', parent=comando)

    def _montar_operacoes(self, checkbox_List) -> list:
        """
        Retorna uma lista de (nome_legível, query) para cada checkbox marcada,
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
        query_arredond = self.comandos_query[checkbox_List[1]]

        for i, (key, query) in enumerate(self.comandos_query.items()):
            if key not in checkbox_List or key.get() != 1:
                continue

            nome = nomes[checkbox_List.index(key)]

            if key == checkbox_List[1]:
                # Arredondamento marcado diretamente — só adiciona se ainda não foi
                if not arredondamento_adicionado:
                    operacoes.append((nome, query))
                    arredondamento_adicionado = True
            else:
                operacoes.append((nome, query))

                # Checkboxes 2, 3 e 4 disparam arredondamento após si mesmos
                if key in (checkbox_List[2], checkbox_List[3], checkbox_List[4]):
                    if not arredondamento_adicionado:
                        operacoes.append(('Arredondar Preço de Custo', query_arredond))
                        arredondamento_adicionado = True

        return operacoes


    # Importar a classe Connect do arquivo Inventario_Conn
    from Thread_Manager.Query_Operations import query_executor, query_updater
    from Thread_Manager.Thread_Executor import thread_execução
    from tkinter import messagebox  # Importar a classe messagebox do tkinter

    if values_List[0].get() != '':  # Verifica se o Entry de porcentagem foi preenchido
        # Preenche a variável porcent_precu com o valor do Entry
        self.porcent_precu = values_List[0].get().replace(
            ',', '.')  # Substitui a vírgula por ponto
    else:
        self.porcent_precu = 1  # Caso o Entry esteja vazio, a porcentagem é 1

    self.precu_vldia = '>' if values_List[1].get() == 'Maior' else '<'
    self.precu_cusme = '>' if values_List[2].get() == 'Maior' else '<'

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
    
    # Monta a lista de operações marcadas, na ordem certa
    operacoes = _montar_operacoes(self, checkbox_List)
    total = len(operacoes)

    if total == 0:
        return

    confirm_button.configure(state='disabled', text='Executando...')

    thread_execução(comando, executa_comandos, update_finalizado, update_erro)


def comandos_true(self) -> str:
    # Função que retorna uma lista com todos os comandos marcados pelo usuário

    key_list = []  # Cria uma lista vazia
    for key in self.comandos_query.keys():  # Itera sobre os itens do dicionário de comandos
        if key.get() == 1:  # Verifica se a checkbox está marcada
            # Adiciona o comando a lista
            key_list.append(self.comandos_query[key])
    return "\n".join(key_list)  # Retorna a lista como uma string

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
