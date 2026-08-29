from Interface_Tools.Treeview_Table.Listagem_Treeview import criar_tela_listagem


def List_Treeview_Screen(parent):
    query = "select cdpro, nmpro, saldo, precu, preve from in01pro where precu > preve and saldo > 0 and preve > 0 order by cdpro asc"
    campos = ['Código', 'Descrição', 'Saldo',
              'Preço de Custo', 'Preço de Venda']

    criar_tela_listagem(parent, 'Lista de Produtos',
                        campos, query, geometry="700x300")
