from Interface_Tools.Treeview_Table.Listagem_Treeview import criar_tela_listagem


def List_Treeview_Screen(parent):
    query = 'select cdpro, nmpro, saldo, precu from in01pro where saldo between 0.000001 and 0.01'
    campos = ['Código', 'Descrição', 'Saldo', 'Preço de Custo']

    criar_tela_listagem(parent, 'Lista de Produtos',
                        campos, query, geometry="700x300")
