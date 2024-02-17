def banco_codigo_valueform(val):
    val = "{:,.2f}".format(val)
    prs = val.split('.')
    pri = prs[0]
    prd = prs[1]
    pri = pri.replace(",", ".")
    val = pri + ',' + prd
    return val

def ent_get():
    from Inventario_Conn import Connect
    from fdb import DatabaseError
    query = """
    select cast(sum(((cast(LAN.valor AS numeric(14, 4)) - (cast(LAN.valor AS numeric(14, 4)) * CAST((LAN.despr/100) AS NUMERIC(14,4)))) * cast(LAN.quant AS numeric(14, 2))) + (LAN.valsub) + (((cast(LAN.valor AS numeric(14, 2)) - (cast(LAN.valor AS numeric(14, 2)) * CAST((LAN.despr/100) AS NUMERIC(14,4)))) * cast(LAN.quant AS numeric(14, 2))) * (cast(LAN.alipi_ent AS numeric(14, 2)) / 100))) as numeric (14,2))
    from in01lan lan
    left join in01com com
    ON (LAN.NOTFI = COM.NOTFI) AND (LAN.CDFRN = COM.CDFRN) AND (LAN.MODELONOTA = COM.MODELONOTA)
    where lan.venda = 'C'
    and lan.cfop not in ('1.540', '1.543', '1.565', '1.592', '1.594', '2.640', '1.360', '1.652', '1.949', '1.910', '1.922', '1.551', '1.555', '1.556', '1.908', '1.920', '1.921', '1.406', '2.255', '1.120', '2.911', '2.916', '1.923', '1.304', '2.932', '2.933', '1.552', '2.410', '2.909', '2.922', '2.925', '1.503', '2.923', '1.407', '1.912', '2.915', '1.201', '1.203', '1.204', '1.207', '1.104', '1.117', '1.116', '1.504', '1.212', '1.126', '1.105', '1.505', '1.656', '1.655', '1.653', '1.411', '2.406', '2.551', '2.555', '2.949', '2.910')
    and com.dtcom between '01.01.2023' AND '31.12.2023'
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