from Interface_Tools.Treeview_Table.Listagem_Treeview import criar_tela_listagem


def List_Treeview_Screen(self, parent):
    query = "select cdpro, notfi, saldo, tpmov, dtpro from in01lan where quant > 999999 and dtpro between ? and ?"
    params = (self.data_banco_inicial, self.data_banco_final)
    colunas = ['Código', 'Nota', 'Saldo', 'TPMOV', 'DTPRO']

    criar_tela_listagem(
        parent, 'Lista de Produtos', colunas, query, params, geometry="700x300")
