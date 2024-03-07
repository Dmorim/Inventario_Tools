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
    
def on_click_confirm(self, comando, checkbox_List, values_List):
    # Função chamada ao apertar o botão de confirmar, itera sobre os itens da combobox e executa os comandos marcados
    # Args:
        # self: objeto da classe
        # comando: janela do tkinter
        # checkbox_List: lista de checkbox da aba comandos
        # values_List: lista de valores da aba comandos
    
    from Banco_de_Dados.Inventario_Conn import Connect # Importar a classe Connect do arquivo Inventario_Conn
    from tkinter import messagebox # Importar a classe messagebox do tkinter
    
    if values_List[0].get() != '': # Verifica se o Entry de porcentagem foi preenchido
        self.porcent_precu = values_List[0].get() # Preenche a variável porcent_precu com o valor do Entry
        self.porcent_precu = self.porcent_precu.replace(',', '.') # Substitui a virgula por ponto
    else:
        self.porcent_precu = 1 # Caso o Entry esteja vazio, a porcentagem é 1
        
    if values_List[1].get() == 'Maior': # Verifica o valor da combobox que seta o preço de custo igual com o preço de compra
        self.precu_vldia = '>' # Se for maior, a variável precu_vldia recebe '>'
    else:
        self.precu_vldia = '<' # Se for menor, a variável precu_vldia recebe '<'
    
    if values_List[2].get() == 'Maior': # Verifica o valor da combobox que seta o preço de custo igual com o custo médio
        self.precu_cusme = '>' # Se for maior, a variável precu_cusme recebe '>'
    else:
        self.precu_cusme = '<' # Se for menor, a variável precu_cusme recebe '<'
    
    if values_List[3].get() == 'Preço de Compra': # Verifica o valor da combobox que seta o preço de custo igual com o preço de compra, ou custo médio ou preço de venda * 0,65 se o saldo estiver zerado
        self.precu_vldia_preve = 'VLDIA' # Se for preço de compra, a variável precu_vldia_preve recebe 'VLDIA'
    elif values_List[3].get() == 'Custo Médio':
        self.precu_vldia_preve = 'CUSME' # Se for custo médio, a variável precu_vldia_preve recebe 'CUSME'
    else:
        self.precu_vldia_preve = 'PREVE - (PREVE * 0.65)' # Se for preço de venda * 0,65, a variável precu_vldia_preve recebe 'PREVE - (PREVE * 0.65)'
        
    self.com_ger = values_List[4].get() # Preenche a variável com_ger com o valor do Entry
    
    Comandos_Func(self, checkbox_List) # Chama a função Comandos_Func para criar os dicionários de comandos
    
    # Cria uma messagebox para confirmar a execução dos comandos, a messagem irá contar uma lista com otodos os comandos marcados pelo usuário.
    cond = messagebox.askyesno('Aviso', f'Os seguintes comandos serão executados:\n{comandos_true(self)}\nDeseja continuar?', parent= comando)
    if cond:
        # Caso o usuário confirme o messagebox:
        
        try:
            for key, value in self.comandos_query.items(): # Itera sobre os itens do dicionário de comandos
                if key in checkbox_List and key.get() == 1: # Verifica se a checkbox está marcada
                    if key == checkbox_List[2] or key == checkbox_List[3] or key == checkbox_List[4]: # Verifica os casos especiais dos checkboxes 2, 3 e 4, onde alem de executar os comandos dele, também executa o comando do checkbox 1
                        Connect.cursor.execute(value)
                        Connect.cursor.execute(self.comandos_query[checkbox_List[1]])
                        Connect.conn.commit()
                    Connect.cursor.execute(value) # Executa o comando
                    Connect.conn.commit() # Commita a transação
            comando.destroy() # Fecha a janela
        except Exception as e:
            # Caso ocorra um erro, uma messagebox é criada com a mensagem de erro
            messagebox.showerror('Erro', f'Erro ao executar os comandos\n{e}', parent= comando)
            return
    else:
        return
    
def comandos_true(self):
    # Função que retorna uma lista com todos os comandos marcados pelo usuário
    
    key_list = [] # Cria uma lista vazia
    for key in self.comandos_query.keys(): # Itera sobre os itens do dicionário de comandos
        if key.get() == 1: # Verifica se a checkbox está marcada
            key_list.append(self.comandos_query[key]) # Adiciona o comando a lista
    return key_list # Retorna a lista

#Validar o valor digitado no Entry como float aceitando virgula na casa decimal e bloqueando o uso de ponto
def precu_porcent_entry_validate(P):
    if P == "": # Aceita o campo vazio
        return True
    try:
        P = P.replace(",", ".") # Substitui a virgula por ponto
        price = float(P) # Tenta converter o valor para float
        int_part, dec_part = str(price).split(".") # Separa a parte inteira da parte decimal
        
        # Verifica se a parte inteira e a parte decimal são digitos e se o valor é positivo bem como seus tamanhos máximos permitos
        return int_part.isdigit() and dec_part.isdigit() and price >= 0 and len(dec_part) <= 11 and len(int_part) <= 9
    except ValueError:
        return False