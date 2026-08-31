"""
Módulo centralizado de queries SQL para os comandos de correção de dados.

Convenção:
- Queries parametrizadas usam `?` como placeholders (Firebird fdb)
- Queries dinâmicas com valores fixos ou opcionais usam `.format()`
- Documentação inclui parâmetros esperados e telas que usam cada query
"""

# ============================================================================
# COMANDOS DE AJUSTE DE PREÇO DE CUSTO
# ============================================================================

QUERY_UPDATE_PRECU_PORCENTAGEM = """
    UPDATE IN01PRO
    SET PRECU = PRECU * ?
"""
"""
Ajusta o preço de custo por uma porcentagem informada pelo usuário.
Tela: Comandos/Comandos_Gerais/Comandos_Func.py
Parâmetros: (porcentagem,)
Retorna: atualização em massa de IN01PRO
"""

QUERY_UPDATE_PRECU_ARREDONDAMENTO = """
    UPDATE IN01PRO
    SET PRECU = CAST(PRECU AS NUMERIC(15, 2))
"""
"""
Arredonda o preço de custo para 2 casas decimais.
Tela: Comandos/Comandos_Gerais/Comandos_Func.py
Parâmetros: Nenhum
Retorna: atualização em massa de IN01PRO
"""

QUERY_UPDATE_PRECU_VLDIA = """
    UPDATE IN01PRO
    SET PRECU = VLDIA
    WHERE VLDIA {operador} PRECU AND VLDIA > 0
"""
"""
Ajusta PRECU para VLDIA quando a comparação respectiva for atendida.
Tela: Comandos/Comandos_Gerais/Comandos_Func.py
Parâmetros: operador (>, <)
Retorna: atualização em massa de IN01PRO
"""

QUERY_UPDATE_PRECU_CUSME = """
    UPDATE IN01PRO
    SET PRECU = CUSME
    WHERE CUSME {operador} PRECU AND CUSME > 0
"""
"""
Ajusta PRECU para CUSME quando a comparação respectiva for atendida.
Tela: Comandos/Comandos_Gerais/Comandos_Func.py
Parâmetros: operador (>, <)
Retorna: atualização em massa de IN01PRO
"""

QUERY_UPDATE_PRECU_ZERADO = """
    UPDATE IN01PRO
    SET PRECU = {campo}
    WHERE (PRECU = 0 OR PRECU IS NULL) AND SALDO > 0 AND PREVE <> 0
"""
"""
Ajusta PRECU a partir do campo informado quando o custo estiver zerado.
Tela: Comandos/Comandos_Gerais/Comandos_Func.py
Parâmetros: campo (VLDIA, CUSME, PREVE - (PREVE * 0.65))
Retorna: atualização em massa de IN01PRO
"""

# ============================================================================
# COMANDOS DE CORREÇÃO DE CLASSIFICAÇÃO E SALDO
# ============================================================================

QUERY_UPDATE_CLASSIFICACAO_NULA = """
    UPDATE IN01PRO
    SET CLASSIFICACAO_PRODUTO = 00
    WHERE CLASSIFICACAO_PRODUTO IS NULL
"""
"""
Corrige classificação nula para 00.
Tela: Comandos/Comandos_Gerais/Comandos_Func.py
Parâmetros: Nenhum
Retorna: atualização em massa de IN01PRO
"""

QUERY_UPDATE_SALDO_NAO_ZERADO = """
    UPDATE IN01PRO
    SET SALDO = 0
    WHERE SALDO BETWEEN 0.000001 AND 0.01
"""
"""
Zera produtos com saldo residual muito pequeno.
Tela: Comandos/Comandos_Gerais/Comandos_Func.py
Parâmetros: Nenhum
Retorna: atualização em massa de IN01PRO
"""

QUERY_UPDATE_CONTROLAESTOQUE_S = """
    UPDATE IN01LAN
    SET CONTROLAESTOQUE = 'S'
    WHERE (CONTROLAESTOQUE IS NULL OR CONTROLAESTOQUE = 'N')
    AND DTPRO >= ?
"""
"""
Ativa controle de estoque a partir de uma data informada.
Tela: Comandos/Comandos_Gerais/Comandos_Func.py
Parâmetros: (data_banco_inicial,)
Retorna: atualização em massa de IN01LAN
"""

QUERY_UPDATE_QUANTIDADE_ALTA = """
    UPDATE IN01LAN
    SET QUANT = 1
    WHERE QUANT > 999999 OR VALOR > 999999
"""
"""
Corrige movimentações com quantidade ou valor fora do limite esperado.
Tela: Comandos/Comandos_Gerais/Comandos_Func.py
Parâmetros: Nenhum
Retorna: atualização em massa de IN01LAN
"""

QUERY_UPDATE_SALDO_NEGATIVO = """
    UPDATE IN01PRO
    SET SALDO = 0
    WHERE SALDO < 0
"""
"""
Zera saldos negativos.
Tela: Comandos/Comandos_Gerais/Comandos_Func.py
Parâmetros: Nenhum
Retorna: atualização em massa de IN01PRO
"""

QUERY_UPDATE_DTOPE_IGUAL_DTPRO = """
    UPDATE IN01LAN
    SET DTOPE = DTPRO
    WHERE VENDA = 'J' AND DTOPE <> DTPRO
"""
"""
Corrige DTOPE para DTPRO quando a venda for do tipo J.
Tela: Comandos/Comandos_Gerais/Comandos_Func.py
Parâmetros: Nenhum
Retorna: atualização em massa de IN01LAN
"""

# ============================================================================
# COMANDOS DE DISTORÇÃO DE SALDO
# ============================================================================

QUERY_ATUALIZA_SALDO_PRODUTO = """
    UPDATE IN01PRO
    SET SALDO = ?
    WHERE CDPRO = ?
"""
"""
Ajusta o saldo do produto para o valor informado.
Tela: Comandos/Distorcao_Saldo/Comandos_Dist_Saldo.py
Parâmetros: (novo_saldo, cdpro)
Retorna: atualização de um produto específico
"""

QUERY_INSERE_AJUSTE_LAN = """
    INSERT INTO IN01LAN (
        NOTFI, CDPRO, VENDA, DTEMI, DTPRO, QUANT, TPMOV,
        HISTO, NMOPE, DTOPE, HISTORICO_AJUSTE
    )
    VALUES ('AJUSTE', ?, 'J', ?, ?, ?, ?, 'AJUSTE DE ESTOQUE (DISTORÇÃO DE SALDO)',
            'SISTECH', ?, ?)
"""
"""
Cria um lançamento de ajuste para corrigir a distorção de saldo.
Tela: Comandos/Distorcao_Saldo/Comandos_Dist_Saldo.py
Parâmetros: (cdpro, data_emissao, data_producao, quant, tpmov, data_ajuste, historico)
Retorna: inserção em IN01LAN
"""

# ============================================================================
# COMANDO GERAL
# ============================================================================

QUERY_COMANDO_GERAL = "{comando}"
"""
Template para execução de comando geral digitado pelo usuário.
Tela: Comandos/Comandos_Gerais/Comandos_Func.py
Parâmetros: comando (string SQL livre)
Retorna: execução direta do comando informado pelo operador
"""
