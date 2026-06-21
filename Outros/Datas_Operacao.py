from datetime import datetime


def obter_data_vigencia():
    ano_atual = datetime.datetime.now().year
    ano_vigencia = ano_atual - 1
    # Definir o primeiro e último dia do ano passado
    primeiro_dia = datetime.datetime(ano_vigencia, 1, 1)
    ultimo_dia = datetime.datetime(ano_vigencia, 12, 31)
    return primeiro_dia.strftime("%d/%m/%Y"), ultimo_dia.strftime("%d/%m/%Y")
