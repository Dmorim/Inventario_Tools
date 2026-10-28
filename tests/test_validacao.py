from Comandos.Comandos_Gerais.Comandos_Func import precu_porcent_entry_validate


class TestPrecuPorcentEntryValidate:
    def test_campo_vazio_aceito(self):
        assert precu_porcent_entry_validate('') is True

    def test_valor_inteiro_aceito(self):
        assert precu_porcent_entry_validate('15') is True

    def test_valor_decimal_virgula_aceito(self):
        assert precu_porcent_entry_validate('15,5') is True

    def test_valor_decimal_ponto_aceito(self):
        # A função troca vírgula por ponto, portanto '.' também é aceito
        assert precu_porcent_entry_validate('15.5') is True

    def test_valor_negativo_rejeitado(self):
        assert precu_porcent_entry_validate('-5') is False

    def test_texto_rejeitado(self):
        assert precu_porcent_entry_validate('abc') is False

    def test_parte_inteira_maior_que_9_digitos_rejeitada(self):
        assert precu_porcent_entry_validate('1234567890') is False

    def test_parte_inteira_com_9_digitos_aceita(self):
        assert precu_porcent_entry_validate('123456789') is True

    def test_parte_decimal_maior_que_11_digitos_rejeitada(self):
        assert precu_porcent_entry_validate('1,123456789012') is False

    def test_parte_decimal_com_11_digitos_aceita(self):
        assert precu_porcent_entry_validate('1,12345678901') is True
