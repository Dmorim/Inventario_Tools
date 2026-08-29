from Interface_Tools.Treeview_Table.Listagem_Treeview import criar_tela_listagem


def List_Treeview_Screen(self, parent):

    query = f"select cdpro, notfi, cfop, dtpro, dtope, controlaestoque from in01lan where controlaestoque = 'N' and dtpro between ? and ?"
    params = (self.data_banco_inicial, self.data_banco_final)
    campos = ['Código', 'Nota', 'CFOP', 'DTPRO', 'DTOPE', 'C.Estoque']

    criar_tela_listagem(parent, 'Lista de Produtos', campos,
                        query, params=params, geometry="700x300")
