from Interface_Tools.Treeview_Table.Listagem_Treeview import criar_tela_listagem


def List_Treeview_Screen(parent, distorcao):
    campos = ['Código', 'Descrição', 'Saldo Lan', 'Saldo Pro']
    criar_tela_listagem(parent, 'Lista de Produtos', campos,
                        distorcao.obter_distorcao().campos_em_lista, geometry="700x300")
