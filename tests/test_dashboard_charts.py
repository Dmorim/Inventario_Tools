from Dashboard.Dashboard_Charts import (
    CORES_POR_TEMA,
    _contraste,
    _rotulos_eixo_x,
    _valor_compacto,
)


class TestValorCompacto:
    def test_valor_abaixo_de_mil_sem_decimais(self):
        assert _valor_compacto(950) == 'R$ 950'

    def test_milhares_compactado(self):
        assert _valor_compacto(350000) == 'R$ 350 mil'

    def test_milhoes_compactado(self):
        assert _valor_compacto(1900000) == 'R$ 1,9 mi'

    def test_bilhoes_compactado(self):
        assert _valor_compacto(2500000000) == 'R$ 2,5 bi'

    def test_valor_negativo_preserva_sinal(self):
        assert _valor_compacto(-1900000) == '-R$ 1,9 mi'

    def test_valor_negativo_mil(self):
        assert _valor_compacto(-350000) == '-R$ 350 mil'

    def test_sem_simbolo_de_moeda(self):
        assert _valor_compacto(350000, com_simbolo=False) == '350 mil'

    def test_valor_nulo_vira_zero(self):
        assert _valor_compacto(None) == 'R$ 0'

    def test_valor_zero(self):
        assert _valor_compacto(0) == 'R$ 0'


class TestRotulosEixoX:
    def test_poucos_rotulos_sao_mantidos(self):
        labels = ['01/2021', '02/2021', '03/2021']
        assert _rotulos_eixo_x(labels) == labels

    def test_muitos_rotulos_sao_rareados(self):
        labels = [f'{mes:02d}/2021' for mes in range(1, 62)]
        visiveis = _rotulos_eixo_x(labels)
        assert len(visiveis) == 61
        assert sum(1 for rotulo in visiveis if rotulo) <= 16
        assert '' in visiveis

    def test_ultimo_rotulo_e_preservado(self):
        labels = [f'{mes:02d}/2021' for mes in range(1, 62)]
        visiveis = _rotulos_eixo_x(labels)
        assert visiveis[-1] == '61/2021'

    def test_rotulo_com_limite_customizado(self):
        labels = [f'{mes:02d}/2021' for mes in range(1, 13)]
        visiveis = _rotulos_eixo_x(labels, maximo=4)
        assert sum(1 for rotulo in visiveis if rotulo) <= 4
        assert visiveis[-1] == '12/2021'


class TestContraste:
    def test_texto_do_grafico_contrasta_com_a_figura(self):
        for tema, cores in CORES_POR_TEMA.items():
            assert _contraste(cores['texto'], cores['figura']) >= 4.5, tema

    def test_subtexto_contrasta_com_a_figura(self):
        for tema, cores in CORES_POR_TEMA.items():
            assert _contraste(cores['subtexto'], cores['figura']) >= 4.5, tema

    def test_rotulo_de_valor_contrasta_com_a_caixa_de_fundo(self):
        for tema, cores in CORES_POR_TEMA.items():
            assert _contraste(cores['texto'], cores['figura']) >= 4.5, tema
