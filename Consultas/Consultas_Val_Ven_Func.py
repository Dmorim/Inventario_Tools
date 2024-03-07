def banco_codigo_valueform(val):
    # Função que formata o valor obtido no banco para correta exibição dele na tela do usuário
    # Args:
        # val: Valor passado que vai ser tratado
    
    val = "{:,.2f}".format(val) #Formata o valor com pontos e virgulas
    prs = val.split('.') # Divide o valor em duas strings, uma antes do "." e outra após
    pri = prs[0] # Define a variável antes do "."
    prd = prs[1] # Define a variável depois do "."
    pri = pri.replace(",", ".") # Substitui qualquer virgula existente por ponto
    val = pri + ',' + prd # Junta as duas partes adicionando uma virugla entre elas
    return val # Retorna o valor trabalhado

def ven_get(self):
    # Função que executa a query de valor de vendas e retorna o valor obtido
    # Args:
        # self: Instância da classe que chama a função
    
    from Banco_de_Dados.Inventario_Conn import Connect # Importa a conexão com o banco de dados
    from fdb import DatabaseError # Importa a exceção de erro de banco de dados
    
    # Query que executa a consulta no banco de dados
    query = f"""
    select
    sum(CAST(iif(F.EMITE = 'S' AND VLNOT > 0, F.VLNOT, iif(coalesce(F.VLNOT, 0) = 0, (COALESCE(F.VALNO, 0) - COALESCE(F.VALDE, 0) + COALESCE(F.ICANT, 0) + coalesce(F.VALFR, 0) + coalesce(F.valsg, 0) + coalesce(F.valip, 0) + coalesce(F.valst, 0)), F.VLNOT)) AS NUMERIC(14,2))) as valor
    from in01fat f
    where F.FATUR <> '' AND (F.CANCE = 'N' OR F.CANCE IS NULL) AND F.VENDA <> 'R' and (F.VENDA <> 'X') and (F.DTEMI >= '{self.data_banco_inicial}') and (F.DTEMI <= '{self.data_banco_final}')
    """
    
    # Tenta executar a query no banco de dados
    try:
        Connect.cursor.execute(query)
        valrec = Connect.cursor.fetchone()[0]
    except (DatabaseError, TypeError) as e:
        from tkinter import messagebox
        messagebox.showerror('Erro', f'Erro ao acessar o banco de dados\n {e}')
        
    # Se o valor obtido for diferente de None, formata o valor e retorna ele, caso contrário retorna uma string informando que não foi registrado vendas
    if valrec is not None:
        valrec = banco_codigo_valueform(valrec)
    else:
        valrec = 'Não foi registrado vendas'
    return valrec
    
def copy_val(val_ven_text):
    # Função que copia o valor da consulta para a área de transferência
    # Args:
        # val_ven_text: Label que contém o valor da consulta
        
    import pyperclip
    copy_text = val_ven_text.cget('text') # Obtém o valor do label
    copy_text = 'R$ ' + copy_text # Adiciona o R$ ao valor
    pyperclip.copy(copy_text) # Copia o valor para a área de transferência