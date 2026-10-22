"""
Módulo centralizado de queries SQL para o Inventario_Tools.

Convenção:
- Queries parametrizadas usam `?` como placeholders (Firebird fdb)
- Documentação inclui parâmetros esperados e telas que usam cada query
"""

# ============================================================================
# QUERIES DE VALOR (Inventário, Vendas, Entradas)
# ============================================================================

QUERY_INVENTARIO = """
    SELECT SUM(CAST(saldo * precu AS NUMERIC(15, 2))) AS valor
    FROM in01pro
    WHERE CAST(saldo AS NUMERIC(15, 2)) > 0 
    AND classificacao_produto IN ('00','01','02','03','04','05','06')
"""
"""
Calcula o valor total do inventário.
Tela: Valor_Inventario/Consultas_Val_Inv_Func.py
Parâmetros: Nenhum
Retorna: sum(valor_inventário)
"""

QUERY_VENDAS = """
    SELECT SUM(valor_saida) AS valor
    FROM V_FAT_VALOR_SAIDA
    WHERE FATUR <> ''
    AND (CANCE = 'N' OR CANCE IS NULL)
    AND VENDA <> 'R'
    AND VENDA <> 'X'
    AND DTEMI >= ?
    AND DTEMI <= ?
"""
"""
Calcula o valor total de vendas em um período.
Tela: Valor_Vendas/Consultas_Val_Ven_Func.py
Parâmetros: (data_inicial, data_final)
Retorna: sum(valor_vendas)
"""

EXPR_VALOR_ENTRADA = """(
        ((CAST(l.valor AS NUMERIC(14, 4)) -
          (CAST(l.valor AS NUMERIC(14, 4)) * CAST((l.despr/100) AS NUMERIC(14,4)))) *
         CAST(l.quant AS NUMERIC(14, 2))) +
        (l.valsub) +
        (((CAST(l.valor AS NUMERIC(14, 2)) -
           (CAST(l.valor AS NUMERIC(14, 2)) * CAST((l.despr/100) AS NUMERIC(14,4)))) *
          CAST(l.quant AS NUMERIC(14, 2))) *
         (CAST(l.alipi_ent AS NUMERIC(14, 2)) / 100))
       )"""

QUERY_ENTRADAS = f"""
    SELECT CAST(
        SUM(
            {EXPR_VALOR_ENTRADA}
        ) AS NUMERIC(14,2)
    ) AS valor
    FROM in01lan l
    INNER JOIN in01com c
            ON c.notfi = l.notfi
           AND c.cdfrn = l.cdfrn
           AND c.modelonota = l.modelonota
    WHERE l.venda = 'C'
    AND l.cfop NOT IN ({{placeholders}})
    AND c.dtcom BETWEEN ? AND ?
    AND CHARACTER_LENGTH(l.cfop) = 5
"""
"""
Calcula o valor total de entradas em um período.
Tela: Valor_Entradas/Consultas_Val_Ent_Func.py
Parâmetros: (*cfop_list, data_inicial, data_final)
Nota: CFOP_LIST contém cerca de 95 valores. Usar com placeholders dinâmicos.
Retorna: sum(valor_entradas)
"""

CFOP_LIST = [
    '1.104', '1.105', '1.116', '1.117', '1.120', '1.126', '1.201', '1.203', '1.204', '1.207', '1.212', '1.304', '1.360', '1.406', '1.407', '1.411', '1.503', '1.504', '1.505', '1.540', '1.543', '1.551', '1.552', '1.555', '1.556', '1.565', '1.592', '1.594', '1.652', '1.653', '1.655', '1.656', '1.908', '1.910', '1.912', '1.920', '1.921', '1.922', '1.923', '1.949',
    '2.104', '2.105', '2.116', '2.117', '2.120', '2.126', '2.128', '2.154', '2.201', '2.203', '2.204', '2.207', '2.212', '2.215', '2.252', '2.255', '2.304', '2.360', '2.406', '2.407', '2.410', '2.411', '2.503', '2.504', '2.505', '2.540', '2.543', '2.551', '2.552', '2.555', '2.556', '2.565', '2.592', '2.594', '2.640', '2.652', '2.653', '2.655', '2.656', '2.908', '2.909', '2.910', '2.911', '2.912', '2.915', '2.916', '2.919', '2.920', '2.921', '2.922', '2.923', '2.925', '2.932', '2.933', '2.949',
]

# ============================================================================
# QUERIES DE CONTAGEM (Produtos com problemas específicos)
# ============================================================================

QUERY_PRECO_CUSTO_ZERADO = """
    SELECT COUNT(*) 
    FROM in01pro 
    WHERE (precu = 0 OR precu IS NULL OR precu < 0) 
    AND preve > 0 
    AND saldo > 0
"""
"""
Conta produtos com preço de custo zerado/nulo/negativo.
Tela: Preco_Custo_Zerado/Consultas_ZCusto_Screen.py
Parâmetros: Nenhum
Retorna: count(produtos)
"""

QUERY_PRECO_CUSTO_MAIOR_VENDA = """
    SELECT COUNT(*) 
    FROM in01pro 
    WHERE precu > preve 
    AND saldo > 0 
    AND preve > 0
"""
"""
Conta produtos onde preço de custo > preço de venda.
Tela: Preco_Custo_Maior_Preco_Venda/Consultas_Precu_Preve_Screen.py
Parâmetros: Nenhum
Retorna: count(produtos)
"""

QUERY_PRECO_CUSTO_VENDA_COMPRA_ZERADOS = """
    SELECT COUNT(*) 
    FROM in01pro 
    WHERE precu = 0 
    AND preve = 0 
    AND vldia = 0 
    AND saldo > 0
"""
"""
Conta produtos com preço de custo, venda e compra zerados.
Tela: Preco_Custo_Compra_Zerado/Consultas_Preve_Precu_Precom_Screen.py
Parâmetros: Nenhum
Retorna: count(produtos)
"""

QUERY_CLASSIFICACAO_NULA = """
    SELECT COUNT(*) 
    FROM in01pro 
    WHERE classificacao_produto IS NULL 
    OR classificacao_produto = ''
"""
"""
Conta produtos sem classificação definida.
Tela: Classificação_Do_Produto/Consultas_Classi_Pro_Screen.py
Parâmetros: Nenhum
Retorna: count(produtos)
"""

QUERY_QUANTIDADE_EXORBITANTE = """
    SELECT COUNT(*) 
    FROM in01lan 
    WHERE quant > 999999 
    AND dtpro BETWEEN ? AND ?
"""
"""
Conta movimentações com quantidade acima do limite (>999999).
Tela: Quantidade_Exorbitante/Consultas_Quant_Maior_Screen.py
Parâmetros: (data_inicial, data_final)
Retorna: count(movimentações)
"""

QUERY_CONTROLA_ESTOQUE_DESATIVADO = """
    SELECT COUNT(*) 
    FROM in01lan 
    WHERE controlaestoque = 'N' 
    AND dtpro BETWEEN ? AND ?
"""
"""
Conta movimentações com controle de estoque desativado.
Tela: Controla_Estoque/Consultas_Contr_Estq_Screen.py
Parâmetros: (data_inicial, data_final)
Retorna: count(movimentações)
"""

QUERY_SALDO_NAO_ZERADO = """
    SELECT COUNT(*) 
    FROM in01pro 
    WHERE saldo BETWEEN 0.000001 AND 0.01
"""
"""
Conta produtos com saldo não zerado (residual, entre 0.000001 e 0.01).
Tela: Produtos_Nao_Zerados/Consultas_NZer_Prod_Screen.py
Parâmetros: Nenhum
Retorna: count(produtos)
"""

QUERY_DISTORCAO_SALDO = """
    EXECUTE BLOCK
    RETURNS (
        cdpro VARCHAR(50),
        nmpro VARCHAR(255),
        saldo_lan NUMERIC(15,4),
        saldo_pro NUMERIC(15,4)
    )
    AS
    DECLARE VARIABLE formatosaldo INTEGER;
    BEGIN
        SELECT CAST(
                CHAR_LENGTH(
                    SUBSTRING(valor FROM POSITION('.' IN valor) + 1)
                ) AS INTEGER
            )
        FROM si01gp
        WHERE ident = 'FORMATOSALDO'
        INTO :formatosaldo;

        FOR
            SELECT
                x.cdpro,
                x.nmpro,
                x.saldo_lan,
                x.saldo_pro
            FROM (
                SELECT
                    p.cdpro,
                    p.nmpro,
                    SUM(IIF(l.tpmov = 'S', l.quant, -l.quant)) AS saldo_lan,
                    p.saldo AS saldo_pro
                FROM in01lan l
                LEFT JOIN in01pro p ON l.cdpro = p.cdpro
                LEFT JOIN in01com c ON 
                    c.notfi = l.notfi
                    AND c.cdfrn = l.cdfrn
                    AND c.serie = l.serie
                WHERE
                    COALESCE(l.controlaestoque, 'S') = 'S'
                    AND COALESCE(l.cance, 'N') = 'N'
                    AND classificacao_produto IN ('00', '01', '02', '04', '05', '06')
                    AND l.venda <> 'R'
                    AND (COALESCE(c.alterarsaldo, 'S') = 'S' OR l.venda <> 'J')
                GROUP BY
                    p.cdpro,
                    p.nmpro,
                    p.saldo
            ) x
            WHERE
                ROUND(x.saldo_lan, :formatosaldo) <>
                ROUND(x.saldo_pro, :formatosaldo)
            INTO
                :cdpro,
                :nmpro,
                :saldo_lan,
                :saldo_pro
            DO
                SUSPEND;
    END
"""
"""
Identifica produtos com discrepância entre saldo em IN01LAN e IN01PRO.
Tela: Distorcao_de_Saldo/Consultas_Dist_Saldo_Screen.py
Parâmetros: Nenhum (EXECUTE BLOCK)
Retorna: (cdpro, nmpro, saldo_lan, saldo_pro)
Nota: Usa EXECUTE BLOCK (Firebird), não parametrizado (lógica complexa)
"""

# ============================================================================
# QUERIES DE LISTAGEM (Telas Treeview)
# ============================================================================

QUERY_LISTA_PRECO_CUSTO_ZERADO = """
    SELECT cdpro, nmpro, saldo, precu 
    FROM in01pro 
    WHERE (precu = 0 OR precu IS NULL OR precu < 0)
    AND preve > 0 
    AND saldo > 0
"""
"""
Lista de produtos com preço de custo zerado.
Tela: Preco_Custo_Zerado/Consultas_ZCusto_List_Screen.py
Retorna: (cdpro, nmpro, saldo, precu)
"""

QUERY_LISTA_PRECO_CUSTO_MAIOR_VENDA = """
    SELECT cdpro, nmpro, precu, preve, saldo 
    FROM in01pro 
    WHERE precu > preve 
    AND saldo > 0 
    AND preve > 0
"""
"""
Lista de produtos com preço de custo > preço de venda.
Tela: Preco_Custo_Maior_Preco_Venda/Consultas_Precu_Preve_List.py
Retorna: (cdpro, nmpro, precu, preve, saldo)
"""

QUERY_LISTA_PRECO_ZERADO = """
    SELECT cdpro, nmpro, saldo, precu 
    FROM in01pro 
    WHERE precu = 0 
    AND preve = 0 
    AND vldia = 0 
    AND saldo > 0
"""
"""
Lista de produtos com preço de custo, venda e compra zerados.
Tela: Preco_Custo_Compra_Zerado/Consultas_Preve_Precu_Precom_List.py
Retorna: (cdpro, nmpro, saldo, precu)
"""

QUERY_LISTA_CLASSIFICACAO_NULA = """
    SELECT cdpro, nmpro, saldo, precu 
    FROM in01pro 
    WHERE classificacao_produto IS NULL 
    OR classificacao_produto = ''
"""
"""
Lista de produtos sem classificação.
Tela: Classificação_Do_Produto/Consultas_Classi_Pro_List.py
Retorna: (cdpro, nmpro, saldo, precu)
"""

QUERY_LISTA_SALDO_NAO_ZERADO = """
    SELECT cdpro, nmpro, saldo 
    FROM in01pro 
    WHERE saldo BETWEEN 0.000001 AND 0.01
"""
"""
Lista de produtos não zerados (saldo residual).
Tela: Produtos_Nao_Zerados/Consultas_NZer_List_Screen.py
Retorna: (cdpro, nmpro, saldo)
"""

QUERY_LISTA_QUANTIDADE_EXORBITANTE = """
    SELECT l.cdpro, p.nmpro, l.quant, l.dtpro 
    FROM in01lan l
    LEFT JOIN in01pro p ON l.cdpro = p.cdpro
    WHERE l.quant > 999999 
    AND l.dtpro BETWEEN ? AND ?
"""
"""
Lista de movimentações com quantidade exorbitante.
Tela: Quantidade_Exorbitante/Consultas_Quant_Maior_List.py
Parâmetros: (data_inicial, data_final)
Retorna: (cdpro, nmpro, quant, dtpro)
"""

QUERY_LISTA_CONTROLA_ESTOQUE = """
    SELECT l.cdpro, p.nmpro, l.quant, l.dtpro 
    FROM in01lan l
    LEFT JOIN in01pro p ON l.cdpro = p.cdpro
    WHERE l.controlaestoque = 'N' 
    AND l.dtpro BETWEEN ? AND ?
"""
"""
Lista de movimentações com controle de estoque desativado.
Tela: Controla_Estoque/Consultas_Contr_Estq_List.py
Parâmetros: (data_inicial, data_final)
Retorna: (cdpro, nmpro, quant, dtpro)
"""

# ============================================================================
# QUERIES AUXILIARES (Banco de Dados, Configuração)
# ============================================================================

QUERY_PROPRI = """
    SELECT NOME, RSOCIAL, CNPJ, CGF, CODCRT, FONE 
    FROM PROPRI
"""
"""
Consulta dados da empresa (propriedade).
Tela: Banco_de_Dados/Tela_Banco_Dados/Banco_de_Dados_Func.py
Parâmetros: Nenhum
Retorna: (NOME, RSOCIAL, CNPJ, CGF, CODCRT, FONE)
"""

QUERY_EMISSOES_MAXIMA = """
    SELECT DTEMI 
    FROM V_FAT_VALOR_SAIDA
    WHERE VENDA IN ('V', 'A', 'W', 'D')
    AND EMITE = 'S'
    AND CANCE <> 'S'
    ORDER BY DTEMI DESC
    ROWS 1
"""
"""
Busca a data máxima de emissão (último movimento).
Tela: Banco_de_Dados/Tela_Banco_Dados/Banco_de_Dados_Func.py
Parâmetros: Nenhum
Retorna: max_date
"""
