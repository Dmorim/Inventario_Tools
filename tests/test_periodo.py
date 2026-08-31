from datetime import date

from Outros.Periodo_Inventario import (
    TIPO_ANUAL,
    TIPO_MENSAL,
    TIPO_PERSONALIZADO,
    calcular_periodo,
    formatar_banco,
    periodo_padrao,
)


class TestFormatarBanco:
    def test_formata_data_brasileira(self):
        assert formatar_banco(date(2025, 3, 1)) == '01.03.2025'

    def test_formata_dia_mes_dois_digitos(self):
        assert formatar_banco(date(2025, 12, 31)) == '31.12.2025'

    def test_formata_retorna_string(self):
        assert isinstance(formatar_banco(date(2025, 1, 1)), str)


class TestCalcularPeriodoAnual:
    def test_ano_explicito(self):
        assert calcular_periodo(TIPO_ANUAL, ano=2024) == (
            date(2024, 1, 1), date(2024, 12, 31))

    def test_sem_ano_usa_ano_corrente(self):
        ini, fim = calcular_periodo(TIPO_ANUAL)
        hoje = date.today()
        assert ini == date(hoje.year, 1, 1)
        assert fim == date(hoje.year, 12, 31)


class TestCalcularPeriodoMensal:
    def test_mes_explicito(self):
        assert calcular_periodo(TIPO_MENSAL, ano=2024, mes=2) == (
            date(2024, 2, 1), date(2024, 2, 29))

    def test_mes_31_dias(self):
        assert calcular_periodo(TIPO_MENSAL, ano=2024, mes=3) == (
            date(2024, 3, 1), date(2024, 3, 31))

    def test_mes_30_dias(self):
        assert calcular_periodo(TIPO_MENSAL, ano=2024, mes=4) == (
            date(2024, 4, 1), date(2024, 4, 30))


class TestCalcularPeriodoPersonalizado:
    def test_ordem_correta(self):
        assert calcular_periodo(
            TIPO_PERSONALIZADO, ini=date(2024, 1, 10), fim=date(2024, 2, 20)) == (
            date(2024, 1, 10), date(2024, 2, 20))

    def test_inverte_quando_fim_menor_que_ini(self):
        assert calcular_periodo(
            TIPO_PERSONALIZADO, ini=date(2024, 2, 20), fim=date(2024, 1, 10)) == (
            date(2024, 1, 10), date(2024, 2, 20))

    def test_datas_iguais(self):
        assert calcular_periodo(
            TIPO_PERSONALIZADO, ini=date(2024, 5, 5), fim=date(2024, 5, 5)) == (
            date(2024, 5, 5), date(2024, 5, 5))


class TestPeriodoPadrao:
    def test_anual_ano_anterior(self):
        ano = date.today().year - 1
        assert periodo_padrao() == (date(ano, 1, 1), date(ano, 12, 31))
