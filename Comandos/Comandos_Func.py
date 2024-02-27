def Comandos_Func(self, checkbox_List): 
    self.comandos_query = {
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
    from Banco_de_Dados.Inventario_Conn import Connect
    from tkinter import messagebox
    if values_List[0].get() != '':
        self.porcent_precu = values_List[0].get()
        self.porcent_precu = self.porcent_precu.replace(',', '.')
    else:
        self.porcent_precu = 1
    
    if values_List[1].get() == 'Maior':
        self.precu_vldia = '>'
    else:
        self.precu_vldia = '<'
    
    if values_List[2].get() == 'Maior':
        self.precu_cusme = '>'
    else:
        self.precu_cusme = '<'
    
    if values_List[3].get() == 'Preço de Compra':
        self.precu_vldia_preve = 'VLDIA'
    elif values_List[3].get() == 'Custo Médio':
        self.precu_vldia_preve = 'CUSME'
    else:
        self.precu_vldia_preve = 'PREVE - (PREVE * 0.65)'
        
    self.com_ger = values_List[4].get()

    Comandos_Func(self, checkbox_List)
    cond = messagebox.askyesno('Aviso', f'Os seguintes comandos serão executados {comandos_true(self)}\nDeseja continuar?', parent= comando)
    if cond:
        try:
            for key, value in self.comandos_query.items():
                if key in checkbox_List and key.get() == 1:
                    if key == checkbox_List[2] or key == checkbox_List[3] or key == checkbox_List[4]:
                        Connect.cursor.execute(value)
                        Connect.cursor.execute(self.comandos_query[checkbox_List[1]])
                        Connect.conn.commit()
                    Connect.cursor.execute(value)
                    Connect.conn.commit()
            comando.destroy()
        except Exception as e:
            messagebox.showerror('Erro', f'Erro ao executar os comandos\n{e}', parent= comando)
            return
    else:
        return
    
def comandos_true(self):
    key_list = []
    for key in self.comandos_query.keys():
        if key.get() == 1:
            key_list.append(self.comandos_query[key])
    return key_list

#Validar o valor digitado no Entry como float aceitando virgula na casa decimal e bloqueando o uso de ponto
def precu_porcent_entry_validate(P):
    if P == "":
        return True
    try:
        P = P.replace(",", ".")
        price = float(P)
        int_part, dec_part = str(price).split(".")
        return int_part.isdigit() and dec_part.isdigit() and price >= 0 and len(dec_part) <= 11 and len(int_part) <= 9 # Aceita apenas valores positivos e centavos entre 0 e 9
    except ValueError:
        return False
    
