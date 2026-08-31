from Interface_Tools.Treeview_Table.Listagem_Treeview import criar_tela_listagem
from Queries.Consulta_Queries import QUERY_LISTA_QUANTIDADE_EXORBITANTE


def List_Treeview_Screen(self, parent):
    query = QUERY_LISTA_QUANTIDADE_EXORBITANTE
    params = (self.data_banco_inicial, self.data_banco_final)
    colunas = ['Código', 'Nota', 'Saldo', 'TPMOV', 'DTPRO']

    criar_tela_listagem(
        parent, 'Lista de Produtos', colunas, query, params, geometry="700x300")
