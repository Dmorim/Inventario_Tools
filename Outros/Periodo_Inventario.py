import datetime
from calendar import monthrange

TIPO_ANUAL = 1
TIPO_MENSAL = 2
TIPO_PERSONALIZADO = 3

MESES = {
    1: 'Janeiro',
    2: 'Fevereiro',
    3: 'Março',
    4: 'Abril',
    5: 'Maio',
    6: 'Junho',
    7: 'Julho',
    8: 'Agosto',
    9: 'Setembro',
    10: 'Outubro',
    11: 'Novembro',
    12: 'Dezembro',
}

MESES_REVERSO = {nome: numero for numero, nome in MESES.items()}


def periodo_padrao():
    ano = datetime.date.today().year - 1
    return datetime.date(ano, 1, 1), datetime.date(ano, 12, 31)


def calcular_periodo(tipo, *, ano=None, mes=None, ini=None, fim=None):
    if tipo == TIPO_ANUAL:
        ano = ano or datetime.date.today().year
        return datetime.date(ano, 1, 1), datetime.date(ano, 12, 31)

    if tipo == TIPO_MENSAL:
        hoje = datetime.date.today()
        ano = ano or hoje.year
        mes = mes or hoje.month
        ultimo_dia = monthrange(ano, mes)[1]
        if mes == 1 and hoje.month == 1:
            ano -= 1
        return datetime.date(ano, mes, 1), datetime.date(ano, mes, ultimo_dia)

    if tipo == TIPO_PERSONALIZADO:
        if ini and fim and fim < ini:
            ini, fim = fim, ini
        return ini, fim

    return periodo_padrao()


def formatar_banco(data):
    return data.strftime('%d.%m.%Y')
