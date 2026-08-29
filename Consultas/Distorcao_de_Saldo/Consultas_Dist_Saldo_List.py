from Interface_Tools.Treeview_Table.Listagem_Treeview import criar_tela_listagem


def List_Treeview_Screen(self, parent):
    campos = ['Código', 'Descrição', 'Saldo Lan', 'Saldo Pro']
    criar_tela_listagem(parent, 'Lista de Produtos', campos,
                        self.dist_saldo_list, geometry="700x300")
