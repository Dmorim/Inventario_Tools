from unittest.mock import patch

from Consultas.Generics_Functions.Gen_Funcs_Consulta import copy_val


class FakeLabel:
    """Widget fake com o método cget para simular um label Tk."""

    def __init__(self, text):
        self._text = text

    def cget(self, key):
        if key == 'text':
            return self._text
        raise KeyError(key)


class TestCopyVal:
    def test_copia_sem_prefixo(self):
        with patch('Consultas.Generics_Functions.Gen_Funcs_Consulta.pyperclip.copy') as mock_copy:
            copy_val(FakeLabel('1.234,56'))
            mock_copy.assert_called_once_with('1.234,56')

    def test_copia_com_prefixo(self):
        with patch('Consultas.Generics_Functions.Gen_Funcs_Consulta.pyperclip.copy') as mock_copy:
            copy_val(FakeLabel('1.234,56'), prefix='R$ ')
            mock_copy.assert_called_once_with('R$ 1.234,56')

    def test_copia_valor_vazio(self):
        with patch('Consultas.Generics_Functions.Gen_Funcs_Consulta.pyperclip.copy') as mock_copy:
            copy_val(FakeLabel(''))
            mock_copy.assert_called_once_with('')

    def test_prefixo_vazio_comporta_como_sem_prefixo(self):
        with patch('Consultas.Generics_Functions.Gen_Funcs_Consulta.pyperclip.copy') as mock_copy:
            copy_val(FakeLabel('10,00'), prefix='')
            mock_copy.assert_called_once_with('10,00')
