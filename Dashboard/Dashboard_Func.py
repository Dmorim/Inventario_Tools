from Outros.Logger.Get_Logger import get_logger
from Thread_Manager.Query_Operations import query_selector, query_executor, _nome_query
from Consultas.Generics_Functions.Gen_Funcs_Consulta import banco_codigo_valueform
from Queries.Consulta_Queries import (
    QUERY_INVENTARIO,
    CFOP_LIST,
    QUERY_VENDAS,
    QUERY_ENTRADAS,
)

logger = get_logger(__name__)

QUERY_VENDAS_MES_ANO_AGRUPADO = """
    SELECT extract(month FROM dtemi) AS mes,
       extract(year  FROM dtemi) AS ano,
       sum(valor_saida) AS valor
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

QUERY_DIFERENCA_ANO_ANTERIOR_ATUAL = """
select SUM(abs(valor_diff)) AS valor_diff
from V_DIFF_ENTRADA_SAIDA_MES
where ano in (?, ?)
group by ano
order by ano ASC
"""


_PLACEHOLDERS_CFOP = ', '.join(['?'] * len(CFOP_LIST))


def _previa_inventario(valor_inventario, fim):
    """
    Calcula a previsão do inventário gerado subtraindo do valor do inventario atual a diferença de entradas/saídas do ano do inventário e anterior
    """

    ano = int(fim[-4:])
    valores = _executar_select(
        QUERY_DIFERENCA_ANO_ANTERIOR_ATUAL, (ano - 1, ano))

    valor_diferenca_anterior = valores[0][0] if valores else 0
    valor_diferenca_atual = valores[1][0] if len(valores) > 1 else 0

    diferenca_em_diferenca = valor_diferenca_atual - valor_diferenca_anterior
    valor_previa = valor_inventario - diferenca_em_diferenca
    return valor_previa


def _executar_consulta(query, params=None):
    try:
        rows = query_executor(query_selector, query, params)
        valor = rows[0][0] if rows else None
        return valor if valor is not None else 0
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
        raise


def _extrair_series(rows, granularidade):
    valores = {}
    rotulos = {}
    for row in rows:
        if granularidade == 'mes':
            mes, ano = int(row[0]), int(row[1])
            chave = (ano, mes)
            rotulos[chave] = f'{mes:02d}/{ano}'
            valor = row[2]
        else:
            ano = int(row[0])
            chave = (ano,)
            rotulos[chave] = str(ano)
            valor = row[1]

        valores[chave] = float(valor or 0)

    return valores, rotulos


def carregar_dados_tendencia(ini, fim, granularidade):

    def __executar_consulta_mes():
        return (_executar_select(QUERY_VENDAS_MES_ANO_AGRUPADO, (ini, fim)),
                _executar_select(QUERY_ENTRADAS_MES_ANO_AGRUPADO.format(
                    placeholders=_PLACEHOLDERS_CFOP), (*CFOP_LIST, ini, fim)))

    def __executar_consulta_ano():
        return (_executar_select(QUERY_VENDAS_ANO_AGRUPADO, (ini, fim)),
                _executar_select(QUERY_ENTRADAS_ANO_AGRUPADO.format(
                    placeholders=_PLACEHOLDERS_CFOP), (*CFOP_LIST, ini, fim)))

    try:
        vendas_rows, entradas_rows = __executar_consulta_mes(
        ) if granularidade == 'mes' else __executar_consulta_ano()

        vendas, rotulos_vendas = _extrair_series(vendas_rows, granularidade)
        entradas, rotulos_entradas = _extrair_series(
            entradas_rows, granularidade)

        rotulos_merge = {}
        rotulos_merge.update(rotulos_vendas)
        rotulos_merge.update(rotulos_entradas)

        periodos = sorted(set(vendas) | set(entradas))
        labels = [rotulos_merge.get(periodo, str(periodo))
                  for periodo in periodos]

        dados = {
            'labels': labels,
            'vendas': [vendas.get(periodo, 0) for periodo in periodos],
            'entradas': [entradas.get(periodo, 0) for periodo in periodos],
            'diferenca': [entradas.get(periodo, 0) - vendas.get(periodo, 0)
                          for periodo in periodos],
        }
        return dados

    except Exception:
        logger.exception('Erro ao carregar dados de tendência.')
        return {'labels': [], 'vendas': [], 'entradas': [], 'diferenca': []}


def carregar_kpis(ini=None, fim=None):
    try:
        valor_inventario = _executar_consulta(QUERY_INVENTARIO)
        valor_vendas = _executar_consulta(QUERY_VENDAS, (ini, fim))
        valor_entradas = _executar_consulta(
            QUERY_ENTRADAS.format(placeholders=_PLACEHOLDERS_CFOP), (*CFOP_LIST, ini, fim))
        valor_vendas_130 = float(valor_vendas) * 1.3
        valor_previa_inventario = _previa_inventario(valor_inventario, fim)

        valor_fmt_inventario = banco_codigo_valueform(
            valor_inventario) if valor_inventario else '0,00'
        valor_fmt_vendas = banco_codigo_valueform(
            valor_vendas) if valor_vendas else '0,00'
        valor_fmt_entradas = banco_codigo_valueform(
            valor_entradas) if valor_entradas else '0,00'
        valor_fmt_vendas_130 = banco_codigo_valueform(
            valor_vendas_130) if valor_vendas_130 else '0,00'
        valor_fmt_previa_inventario = banco_codigo_valueform(
            valor_previa_inventario) if valor_previa_inventario else '0,00'

        kpis = {
            'valor_inventario': valor_fmt_inventario,
            'valor_vendas': valor_fmt_vendas,
            'valor_entradas': valor_fmt_entradas,
            'vendas_130': valor_fmt_vendas_130,
            'previa_inventario': valor_fmt_previa_inventario,
        }
        return kpis

    except Exception:
        logger.exception('Erro ao carregar KPIs do dashboard.')
        return {
            'valor_inventario': 'Erro',
            'valor_vendas': 0,
            'valor_entradas': 0,
            'vendas_130': '0,00',
            'previa_inventario': 'Erro',
        }
