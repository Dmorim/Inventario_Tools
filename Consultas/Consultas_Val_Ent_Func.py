def banco_codigo_valueform(val):
    val = "{:,.2f}".format(val)
    prs = val.split('.')
    pri = prs[0]
    prd = prs[1]
    pri = pri.replace(",", ".")
    val = pri + ',' + prd
    return val

def ent_get(self):
    from Inventario_Conn import Connect
    from fdb import DatabaseError
    cfop_list = ['1.104', '1.105', '1.116', '1.117', '1.120', '1.126', '1.201', '1.203', '1.204', '1.207', '1.212', '1.304', '1.360', '1.406', '1.407', '1.411', '1.503', '1.504', '1.505', '1.540', '1.543', '1.551', '1.552', '1.555', '1.556', '1.565', '1.592', '1.594', '1.652', '1.653', '1.655', '1.656', '1.908', '1.910', '1.912', '1.920', '1.921', '1.922', '1.923', '1.949', '2.104', '2.105', '2.116', '2.117', '2.120', '2.126', '2.128', '2.154', '2.201', '2.203', '2.204', '2.207', '2.212', '2.215', '2.252', '2.255', '2.304', '2.360', '2.406', '2.407', '2.410', '2.411', '2.503', '2.504', '2.505', '2.540', '2.543', '2.551', '2.552', '2.555', '2.556', '2.565', '2.592', '2.594', '2.640', '2.652', '2.653', '2.655', '2.656', '2.908', '2.909', '2.910', '2.911', '2.912', '2.915', '2.916', '2.919', '2.920', '2.921', '2.922', '2.923', '2.925', '2.932', '2.933', '2.949']
    cfop_str = ', '.join(f"'{cfop}'" for cfop in cfop_list)
    query = f"""
    select cast(sum(((cast(LAN.valor AS numeric(14, 4)) - (cast(LAN.valor AS numeric(14, 4)) * CAST((LAN.despr/100) AS NUMERIC(14,4)))) * cast(LAN.quant AS numeric(14, 2))) + (LAN.valsub) + (((cast(LAN.valor AS numeric(14, 2)) - (cast(LAN.valor AS numeric(14, 2)) * CAST((LAN.despr/100) AS NUMERIC(14,4)))) * cast(LAN.quant AS numeric(14, 2))) * (cast(LAN.alipi_ent AS numeric(14, 2)) / 100))) as numeric (14,2))
    from in01lan lan
    left join in01com com
    ON (LAN.NOTFI = COM.NOTFI) AND (LAN.CDFRN = COM.CDFRN) AND (LAN.MODELONOTA = COM.MODELONOTA)
    where lan.venda = 'C'
    and lan.cfop not in ({cfop_str})
    and com.dtcom between '{self.data_banco_inicial}' AND '{self.data_banco_final}'
    and character_length(lan.cfop) = 5
    """
    
    try:
        Connect.cursor.execute(query)
        valent = Connect.cursor.fetchone()[0]
    except DatabaseError as e:
        from tkinter import messagebox
        messagebox.showerror('Erro', f'Erro ao acessar o banco de dados\n {e}')
    
    if valent != None:   
        valent = banco_codigo_valueform(valent)
    else:
        valent = 'Não foi registrado entradas'
    return valent
    
def copy_val(val_ven_text):
    import pyperclip
    copy_text = val_ven_text.cget('text')
    copy_text = 'R$ ' + copy_text
    pyperclip.copy(copy_text)