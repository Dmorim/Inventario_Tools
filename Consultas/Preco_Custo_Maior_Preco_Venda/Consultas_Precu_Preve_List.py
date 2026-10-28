from Interface_Tools.Treeview_Table.Listagem_Treeview import criar_tela_listagem
from Queries.Consulta_Queries import QUERY_LISTA_PRECO_CUSTO_MAIOR_VENDA


def List_Treeview_Screen(parent):
    query = QUERY_LISTA_PRECO_CUSTO_MAIOR_VENDA
    campos = ['Código', 'Descrição', 'Saldo',
              'Preço de Custo', 'Preço de Venda']

    criar_tela_listagem(parent, 'Lista de Produtos',
                        campos, query, geometry="700x300")
