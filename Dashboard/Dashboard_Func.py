from Outros.Logger.Get_Logger import get_logger
from Thread_Manager.Query_Operations import query_selector, query_executor, _nome_query
from Consultas.Generics_Functions.Gen_Funcs_Consulta import banco_codigo_valueform
from Queries.Consulta_Queries import (
    QUERY_INVENTARIO,
    CFOP_LIST,
)

logger = get_logger(__name__)

QUERY_TOTAL_PRODUTOS = """
    SELECT COUNT(*) FROM in01pro
    WHERE classificacao_produto IN ('00','01','02','03','04','05','06')
"""
QUERY_TOTAL_PRODUTOS_ATIVOS = """
    SELECT COUNT(*) FROM in01pro
    WHERE saldo > 0
    AND classificacao_produto IN ('00','01','02','03','04','05','06')
"""
QUERY_TOTAL_PRODUTOS_ZERADOS = """
    SELECT COUNT(*) FROM in01pro
    WHERE saldo <= 0
    AND classificacao_produto IN ('00','01','02','03','04','05','06')
"""
QUERY_TOTAL_MOVIMENTACOES = """
    SELECT COUNT(*) FROM in01lan
"""

QUERY_VENDAS_MES_ANO_AGRUPADO = """
    SELECT mes, ano, sum(valor_saida) AS valor
FROM V_FAT_VALOR_SAIDA
WHERE (cance = 'N' OR cance IS NULL)
  AND fatur <> ''
  AND venda NOT IN ('R','X')
  AND dtemi BETWEEN ? AND ?
GROUP BY 1, 2
ORDER BY 2, 1
"""

QUERY_VENDAS_ANO_AGRUPADO = """
    SELECT extract(year FROM dtemi) AS ano,
       sum(valor_saida) AS valor
FROM V_FAT_VALOR_SAIDA
WHERE (cance = 'N' OR cance IS NULL)
  AND fatur <> ''
  AND venda NOT IN ('R','X')
  AND dtemi BETWEEN ? AND ?
GROUP BY 1
ORDER BY 1

"""

QUERY_ENTRADAS_MES_ANO_AGRUPADO = """
SELECT extract(month FROM com_dtcom) AS mes,
       extract(year  FROM com_dtcom) AS ano,
       CAST(SUM(COALESCE(valor,0)) AS NUMERIC(14,2)) AS valor
FROM V_LAN_COM
WHERE venda = 'C'
  AND CHARACTER_LENGTH(cfop) = 5
  AND cfop NOT IN ({placeholders})
  AND com_dtcom BETWEEN ? AND ?
GROUP BY 1, 2
ORDER BY 2, 1
"""

QUERY_ENTRADAS_ANO_AGRUPADO = """
SELECT extract(year FROM com_dtcom) AS ano,
       CAST(SUM(COALESCE(valor,0)) AS NUMERIC(14,2)) AS valor
FROM V_LAN_COM
WHERE venda = 'C'
  AND CHARACTER_LENGTH(cfop) = 5
  AND cfop NOT IN ({placeholders})
  AND com_dtcom BETWEEN ? AND ?
GROUP BY 1
ORDER BY 1
"""

QUERY_DIFERENCA_ENTRADA_SAIDA_AGRUPADO = """
SELECT mes, ano, valor_entrada, valor_saida, valor_diff
FROM V_DIFF_ENTRADA_SAIDA_MES
WHERE dt BETWEEN ? AND ?
ORDER BY 2, 1
"""

QUERY_DIFERENCA_ANO_AGRUPADO = """
SELECT ano,
       SUM(valor_entrada) AS valor_entrada,
       SUM(valor_saida) AS valor_saida,
       SUM(valor_diff) AS valor_diff
FROM V_DIFF_ENTRADA_SAIDA_MES
WHERE dt BETWEEN ? AND ?
GROUP BY 1
ORDER BY 1
"""

_PLACEHOLDERS_CFOP = ', '.join(['?'] * len(CFOP_LIST))


def _executar_consulta(query, params=None):
    try:
        rows = query_executor(query_selector, query, params)
        return rows[0][0] if rows else 0
    except Exception:
        logger.exception('Erro ao executar query do dashboard: %s',
                         _nome_query(query))
        return 0


def _executar_select(query, params=None):
    try:
        return query_executor(query_selector, query, params)
    except Exception:
        logger.exception('Erro ao executar select do dashboard: %s',
                         _nome_query(query))
        return []


def _extrair_series(rows, granularidade, com_diferenca=False):
    valores = {}
    rotulos = {}
    for row in rows:
        if granularidade == 'mes':
            mes, ano = int(row[0]), int(row[1])
            chave = (ano, mes)
            rotulos[chave] = f'{mes:02d}/{ano}'
            dados = row[2:]
        else:
            ano = int(row[0])
            chave = (ano,)
            rotulos[chave] = str(ano)
            dados = row[1:]

        if com_diferenca:
            valores[chave] = [float(v or 0) for v in dados]
        else:
            valores[chave] = float(dados[0] or 0)

    return valores, rotulos


def carregar_dados_tendencia(ini, fim, granularidade):
    logger.info('Carregando dados de tendência. granularidade=%s | período=%s..%s',
                granularidade, ini, fim)
    try:
        if granularidade == 'mes':
            vendas_rows = _executar_select(
                QUERY_VENDAS_MES_ANO_AGRUPADO, (ini, fim))
            entradas_query = QUERY_ENTRADAS_MES_ANO_AGRUPADO.format(
                placeholders=_PLACEHOLDERS_CFOP)
            entradas_rows = _executar_select(
                entradas_query, (*CFOP_LIST, ini, fim))
            diff_rows = _executar_select(
                QUERY_DIFERENCA_ENTRADA_SAIDA_AGRUPADO, (ini, fim))
        else:
            vendas_rows = _executar_select(
                QUERY_VENDAS_ANO_AGRUPADO, (ini, fim))
            entradas_query = QUERY_ENTRADAS_ANO_AGRUPADO.format(
                placeholders=_PLACEHOLDERS_CFOP)
            entradas_rows = _executar_select(
                entradas_query, (*CFOP_LIST, ini, fim))
            diff_rows = _executar_select(
                QUERY_DIFERENCA_ANO_AGRUPADO, (ini, fim))

        vendas, rotulos = _extrair_series(vendas_rows, granularidade)
        entradas, _ = _extrair_series(entradas_rows, granularidade)
        diffs, rotulos_diff = _extrair_series(
            diff_rows, granularidade, com_diferenca=True)

        rotulos_merge = dict(rotulos)
        rotulos_merge.update(rotulos_diff)

        periodos = sorted(set(vendas) | set(entradas) | set(diffs))
        labels = [rotulos_merge[periodo] for periodo in periodos]

        dados = {
            'labels': labels,
            'vendas': [vendas.get(periodo, 0) for periodo in periodos],
            'entradas': [entradas.get(periodo, 0) for periodo in periodos],
            'diferenca': [diffs.get(periodo, [0, 0, 0])[2]
                          for periodo in periodos],
        }
        return dados

    except Exception:
        logger.exception('Erro ao carregar dados de tendência.')
        return {'labels': [], 'vendas': [], 'entradas': [], 'diferenca': []}


def carregar_kpis(ini=None, fim=None):
    logger.info('Carregando KPIs do dashboard.')
    try:
        total_produtos = _executar_consulta(QUERY_TOTAL_PRODUTOS)
        total_ativos = _executar_consulta(QUERY_TOTAL_PRODUTOS_ATIVOS)
        total_zerados = _executar_consulta(QUERY_TOTAL_PRODUTOS_ZERADOS)
        valor_inventario = _executar_consulta(QUERY_INVENTARIO)
        total_movimentacoes = _executar_consulta(QUERY_TOTAL_MOVIMENTACOES)

        valor_fmt = banco_codigo_valueform(
            valor_inventario) if valor_inventario else 'R$ 0,00'

        kpis = {
            'valor_inventario': valor_fmt,
            'total_produtos': total_produtos,
            'total_ativos': total_ativos,
            'total_zerados': total_zerados,
            'total_movimentacoes': total_movimentacoes,
        }
        return kpis

    except Exception:
        logger.exception('Erro ao carregar KPIs do dashboard.')
        return {
            'valor_inventario': 'Erro',
            'total_produtos': 0,
            'total_ativos': 0,
            'total_zerados': 0,
            'total_movimentacoes': 0,
        }
