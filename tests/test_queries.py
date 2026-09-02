from Queries import Comando_Queries, Consulta_Queries


CONSULTAS_ESPERADAS = {
    'QUERY_INVENTARIO',
    'QUERY_VENDAS',
    'QUERY_ENTRADAS',
    'QUERY_PRECO_CUSTO_ZERADO',
    'QUERY_PRECO_CUSTO_MAIOR_VENDA',
    'QUERY_PRECO_CUSTO_VENDA_COMPRA_ZERADOS',
    'QUERY_CLASSIFICACAO_NULA',
    'QUERY_QUANTIDADE_EXORBITANTE',
    'QUERY_CONTROLA_ESTOQUE_DESATIVADO',
    'QUERY_SALDO_NAO_ZERADO',
    'QUERY_DISTORCAO_SALDO',
    'QUERY_LISTA_PRECO_CUSTO_ZERADO',
    'QUERY_LISTA_PRECO_CUSTO_MAIOR_VENDA',
    'QUERY_LISTA_PRECO_ZERADO',
    'QUERY_LISTA_CLASSIFICACAO_NULA',
    'QUERY_LISTA_SALDO_NAO_ZERADO',
    'QUERY_LISTA_QUANTIDADE_EXORBITANTE',
    'QUERY_LISTA_CONTROLA_ESTOQUE',
    'QUERY_PROPRI',
    'QUERY_EMISSOES_MAXIMA',
}

COMANDOS_ESPERADOS = {
    'QUERY_UPDATE_PRECU_PORCENTAGEM',
    'QUERY_UPDATE_PRECU_ARREDONDAMENTO',
    'QUERY_UPDATE_PRECU_VLDIA',
    'QUERY_UPDATE_PRECU_CUSME',
    'QUERY_UPDATE_PRECU_ZERADO',
    'QUERY_UPDATE_CLASSIFICACAO_NULA',
    'QUERY_UPDATE_SALDO_NAO_ZERADO',
    'QUERY_UPDATE_CONTROLAESTOQUE_S',
    'QUERY_UPDATE_QUANTIDADE_ALTA',
    'QUERY_UPDATE_SALDO_NEGATIVO',
    'QUERY_UPDATE_DTOPE_IGUAL_DTPRO',
    'QUERY_ATUALIZA_SALDO_PRODUTO',
    'QUERY_INSERE_AJUSTE_LAN',
    'QUERY_COMANDO_GERAL',
}


def _nomes_de_queries(modulo):
    return {
        nome for nome, valor in vars(modulo).items()
        if nome.startswith('QUERY_') and isinstance(valor, str)
    }


def test_consulta_queries_mantem_contrato_publico():
    nomes = _nomes_de_queries(Consulta_Queries)
    assert nomes == CONSULTAS_ESPERADAS
    assert all(getattr(Consulta_Queries, nome).strip() for nome in nomes)


def test_comando_queries_mantem_contrato_publico():
    nomes = _nomes_de_queries(Comando_Queries)
    assert nomes == COMANDOS_ESPERADOS
    assert all(getattr(Comando_Queries, nome).strip() for nome in nomes)
