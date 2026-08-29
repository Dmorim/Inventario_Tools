from Consultas.Generics_Functions.Gen_Funcs_Consulta import banco_codigo_valueform


class TestBancoCodigoValueform:
    def test_formata_valor_inteiro(self):
        assert banco_codigo_valueform(1000) == '1.000,00'

    def test_formata_valor_decimal(self):
        assert banco_codigo_valueform(1234.56) == '1.234,56'

    def test_formata_centavos(self):
        assert banco_codigo_valueform(0.5) == '0,50'

    def test_versoes_sao_equivalentes(self):
        for valor in (0, 0.5, 1000, 1234.56, 999999.99):
            assert banco_codigo_valueform(
                valor) == banco_codigo_valueform(valor)
