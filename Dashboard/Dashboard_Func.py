from datetime import date, timedelta

from Outros.Logger.Get_Logger import get_logger
from Thread_Manager.Query_Operations import query_selector, query_executor, _nome_query
from Consultas.Generics_Functions.Gen_Funcs_Consulta import banco_codigo_valueform
from Queries.Consulta_Queries import (
    QUERY_INVENTARIO,
    CFOP_LIST,
    QUERY_VENDAS,
    QUERY_ENTRADAS,
    EXPR_VALOR_ENTRADA,
)

logger = get_logger(__name__)


def _hoje():
    return date.today()

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

QUERY_ENTRADAS_MES_ANO_AGRUPADO = f"""
SELECT extract(month FROM c.dtcom) AS mes,
       extract(year  FROM c.dtcom) AS ano,
       CAST(SUM({EXPR_VALOR_ENTRADA}) AS NUMERIC(14,2)) AS valor
FROM in01lan l
INNER JOIN in01com c
        ON c.notfi = l.notfi
       AND c.cdfrn = l.cdfrn
       AND c.modelonota = l.modelonota
WHERE l.venda = 'C'
  AND CHARACTER_LENGTH(l.cfop) = 5
  AND l.cfop NOT IN ({{placeholders}})
  AND c.dtcom BETWEEN ? AND ?
GROUP BY 1, 2
ORDER BY 2, 1
"""

QUERY_ENTRADAS_ANO_AGRUPADO = f"""
SELECT extract(year FROM c.dtcom) AS ano,
       CAST(SUM({EXPR_VALOR_ENTRADA}) AS NUMERIC(14,2)) AS valor
FROM in01lan l
INNER JOIN in01com c
        ON c.notfi = l.notfi
       AND c.cdfrn = l.cdfrn
       AND c.modelonota = l.modelonota
WHERE l.venda = 'C'
  AND CHARACTER_LENGTH(l.cfop) = 5
  AND l.cfop NOT IN ({{placeholders}})
  AND c.dtcom BETWEEN ? AND ?
GROUP BY 1
ORDER BY 1
"""

QUERY_MOVIMENTO_ESTOQUE_CUSTO = """
    SELECT CAST(SUM(IIF(l.tpmov = 'S', l.quant, -l.quant)
                    * COALESCE(p.precu, 0)) AS NUMERIC(15, 2)) AS movimento
    FROM in01lan l
    INNER JOIN in01pro p ON p.cdpro = l.cdpro
    WHERE COALESCE(l.controlaestoque, 'S') = 'S'
      AND COALESCE(l.cance, 'N') = 'N'
      AND p.classificacao_produto IN ('00','01','02','03','04','05','06')
      AND l.dtpro BETWEEN ? AND ?
"""
"""
Movimento líquido do estoque no período, valorizado ao custo atual (precu).

`l.tpmov = 'S'` identifica as linhas que entram no estoque (compras,
devoluções de venda e transferências de entrada); as demais saem (vendas,
devoluções ao fornecedor e ajustes). Usa o mesmo custo e o mesmo universo de
classificação de QUERY_INVENTARIO — no banco de teste o total histórico
(4.156.492,44) converge com o saldo calculado (4.207.242,01).
Tela: Dashboard/Dashboard_Func.py (_previa_inventario)
Parâmetros: (data_inicial, data_final)
Retorna: movimento líquido a custo atual
"""


_PLACEHOLDERS_CFOP = ', '.join(['?'] * len(CFOP_LIST))


def _previa_inventario(valor_inventario, ini, fim):
    """Estima o inventário no fim do período pelo modelo B1.

    Rola a partir do saldo corrente (`hoje`) com base em movimentação a custo atual
    (`precu`), mesmo universo de classificação de QUERY_INVENTARIO:

    - fim < hoje: inv_corrente - movimento(fim+1 .. hoje)
    - fim >= hoje: inv_corrente + movimento(hoje+1 .. fim)

    `l.tpmov = 'S'` entra no estoque; demais saem.
    Devolve None quando a consulta falha, para o card sinalizar o erro em vez
    de exibir o inventário como se fosse uma estimativa válida.
    """

    hoje = date.today()
    try:
        fim_data = date.fromisoformat(str(fim))
    except Exception:
        try:
            # compatibilidade com formatos dd.mm.aaaa usados no projeto
            partes = str(fim).split('.')
            if len(partes) == 3:
                fim_data = date(int(partes[2]), int(partes[1]), int(partes[0]))
            else:
                raise
        except Exception:
            fim_data = hoje

    try:
        if fim_data < hoje:
            ini_mov = fim_data + timedelta(days=1)
            fim_mov = hoje
            movimento = _executar_consulta(
                QUERY_MOVIMENTO_ESTOQUE_CUSTO, (ini_mov.isoformat(), fim_mov.isoformat()),
                padrao_em_erro=None)
            if movimento is None:
                return None
            return float(valor_inventario or 0) - float(movimento or 0)
        ini_mov = hoje + timedelta(days=1)
        fim_mov = fim_data
        if ini_mov > fim_mov:
            return float(valor_inventario or 0)
        movimento = _executar_consulta(
            QUERY_MOVIMENTO_ESTOQUE_CUSTO, (ini_mov.isoformat(), fim_mov.isoformat()),
            padrao_em_erro=None)
        if movimento is None:
            return None
        return float(valor_inventario or 0) + float(movimento or 0)
    except Exception:
        logger.exception('Erro ao calcular previsão B1 do inventário.')
        return None


def _executar_consulta(query, params=None, padrao_em_erro=0):
    try:
        rows = query_executor(query_selector, query, params)
        valor = rows[0][0] if rows else None
        return valor if valor is not None else 0
    except Exception:
        logger.exception('Erro ao executar query do dashboard: %s',
                         _nome_query(query))
        return padrao_em_erro


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


def _calcular_kpis(ini, fim, incluir_previa=True):
    valor_inventario = _executar_consulta(QUERY_INVENTARIO)
    valor_vendas = _executar_consulta(QUERY_VENDAS, (ini, fim))
    valor_entradas = _executar_consulta(
        QUERY_ENTRADAS.format(placeholders=_PLACEHOLDERS_CFOP), (*CFOP_LIST, ini, fim))
    valor_vendas_130 = float(valor_vendas) * 1.3

    valor_fmt_inventario = banco_codigo_valueform(
        valor_inventario) if valor_inventario else '0,00'
    valor_fmt_vendas = banco_codigo_valueform(
        valor_vendas) if valor_vendas else '0,00'
    valor_fmt_entradas = banco_codigo_valueform(
        valor_entradas) if valor_entradas else '0,00'
    valor_fmt_vendas_130 = banco_codigo_valueform(
        valor_vendas_130) if valor_vendas_130 else '0,00'

    kpis = {
        'valor_inventario': valor_fmt_inventario,
        'valor_vendas': valor_fmt_vendas,
        'valor_entradas': valor_fmt_entradas,
        'vendas_130': valor_fmt_vendas_130,
        'valor_inventario_num': float(valor_inventario or 0),
        'valor_vendas_num': float(valor_vendas or 0),
        'valor_entradas_num': float(valor_entradas or 0),
        'vendas_130_num': float(valor_vendas_130 or 0),
    }

    # A previsão depende do período e só faz sentido no período selecionado;
    # no período anterior ela não é exibida nem comparada.
    if incluir_previa:
        valor_previa_inventario = _previa_inventario(
            valor_inventario, ini, fim)
        if valor_previa_inventario is None:
            kpis['previa_inventario'] = 'Erro'
            kpis['previa_inventario_num'] = 0.0
        else:
            kpis['previa_inventario'] = (
                banco_codigo_valueform(valor_previa_inventario)
                if valor_previa_inventario else '0,00')
            kpis['previa_inventario_num'] = float(valor_previa_inventario)
    return kpis


def carregar_kpis(ini=None, fim=None, ini_ant=None, fim_ant=None):
    try:
        if ini_ant and fim_ant:
            return (_calcular_kpis(ini, fim),
                    _calcular_kpis(ini_ant, fim_ant, incluir_previa=False))
        return _calcular_kpis(ini, fim)

    except Exception:
        logger.exception('Erro ao carregar KPIs do dashboard.')
        return {
            'valor_inventario': 'Erro',
            'valor_vendas': 0,
            'valor_entradas': 0,
            'vendas_130': '0,00',
            'previa_inventario': 'Erro',
        }
