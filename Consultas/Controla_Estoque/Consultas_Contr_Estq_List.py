from Interface_Tools.Treeview_Table.Listagem_Treeview import criar_tela_listagem
from Queries.Consulta_Queries import QUERY_LISTA_CONTROLA_ESTOQUE


def List_Treeview_Screen(periodo, parent):

    query = QUERY_LISTA_CONTROLA_ESTOQUE
    params = (periodo.inicio_formatado, periodo.fim_formatado)
    campos = ['Código', 'Nota', 'CFOP', 'DTPRO', 'DTOPE', 'C.Estoque']

    criar_tela_listagem(parent, 'Lista de Produtos', campos,
                        query, params=params, geometry="700x300")
