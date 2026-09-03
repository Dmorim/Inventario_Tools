from Outros.Logger.Get_Logger import get_logger
from Thread_Manager.Query_Operations import query_selector, query_executor, _nome_query
from Consultas.Generics_Functions.Gen_Funcs_Consulta import banco_codigo_valueform
from Queries.Consulta_Queries import (
    QUERY_INVENTARIO,
    QUERY_PRECO_CUSTO_ZERADO,
    QUERY_PRECO_CUSTO_MAIOR_VENDA,
    QUERY_PRECO_CUSTO_VENDA_COMPRA_ZERADOS,
    QUERY_CLASSIFICACAO_NULA,
    QUERY_SALDO_NAO_ZERADO,
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


def _executar_consulta(query, params=None):
    try:
        rows = query_executor(query_selector, query, params)
        return rows[0][0] if rows else 0
    except Exception:
        logger.exception('Erro ao executar query do dashboard: %s',
                         _nome_query(query))
        return 0


def carregar_kpis(ini=None, fim=None):
    logger.info('Carregando KPIs do dashboard.')
    try:
        total_produtos = _executar_consulta(QUERY_TOTAL_PRODUTOS)
        total_ativos = _executar_consulta(QUERY_TOTAL_PRODUTOS_ATIVOS)
        total_zerados = _executar_consulta(QUERY_TOTAL_PRODUTOS_ZERADOS)
        valor_inventario = _executar_consulta(QUERY_INVENTARIO)
        total_movimentacoes = _executar_consulta(QUERY_TOTAL_MOVIMENTACOES)

        preco_custo_zerado = _executar_consulta(QUERY_PRECO_CUSTO_ZERADO)
        preco_custo_maior = _executar_consulta(QUERY_PRECO_CUSTO_MAIOR_VENDA)
        preco_tudo_zerado = _executar_consulta(
            QUERY_PRECO_CUSTO_VENDA_COMPRA_ZERADOS)
        classificacao_nula = _executar_consulta(QUERY_CLASSIFICACAO_NULA)
        saldo_nao_zerado = _executar_consulta(QUERY_SALDO_NAO_ZERADO)

        total_problemas = (preco_custo_zerado + preco_custo_maior +
                           preco_tudo_zerado + classificacao_nula + saldo_nao_zerado)

        if total_produtos > 0:
            saude = round(100 - (total_problemas / total_produtos * 100), 1)
        else:
            saude = 100.0
        saude = max(0, min(100, saude))

        valor_fmt = banco_codigo_valueform(
            valor_inventario) if valor_inventario else 'R$ 0,00'

        kpis = {
            'valor_inventario': valor_fmt,
            'total_produtos': total_produtos,
            'total_ativos': total_ativos,
            'total_zerados': total_zerados,
            'total_movimentacoes': total_movimentacoes,
            'saude': saude,
            'problemas': {
                'Preco custo zerado': preco_custo_zerado,
                'Preco custo > venda': preco_custo_maior,
                'Todos precos zerados': preco_tudo_zerado,
                'Classificacao nula': classificacao_nula,
                'Saldo nao zerado': saldo_nao_zerado,
            },
        }

        logger.info('KPIs carregados: saude=%.1f%% | total_problemas=%d | total_produtos=%d',
                     saude, total_problemas, total_produtos)
        return kpis

    except Exception:
        logger.exception('Erro ao carregar KPIs do dashboard.')
        return {
            'valor_inventario': 'Erro',
            'total_produtos': 0,
            'total_ativos': 0,
            'total_zerados': 0,
            'total_movimentacoes': 0,
            'saude': 0.0,
            'problemas': {},
        }
