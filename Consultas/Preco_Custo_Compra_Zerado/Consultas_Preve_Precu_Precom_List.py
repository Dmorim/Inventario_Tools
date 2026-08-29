from Interface_Tools.Treeview_Table.Listagem_Treeview import criar_tela_listagem


def List_Treeview_Screen(parent):
    query = "select cdpro, nmpro, saldo, precu from in01pro where precu = 0 and preve = 0 and vldia = 0 and saldo > 0"
    campos = ['Código', 'Descrição', 'Saldo', 'Preço de Custo']

    criar_tela_listagem(parent, 'Lista de Produtos',
                        campos, query, geometry="700x300")
