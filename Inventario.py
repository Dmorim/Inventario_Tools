from datetime import date
import customtkinter as ctk

from Outros.Logger.Get_Logger import get_logger
from Outros.Periodo_Inventario import periodo_padrao, formatar_banco
from Inv_Screen.Inv_Top_Frame import criar_top_frame
from Inv_Screen.Inv_Bot_Frame import criar_bot_frame
from Configuracoes.Config_Manager import get_config
from Banco_de_Dados.Conexao_Banco_Dados.Inventario_Conn import BancoDeDados
from Queries.Create_Views import deletar_views
from Data_Manager.PeriodoInventario import PeriodoInventario
from Data_Manager.PeriodoManager import PeriodoManager

logger = get_logger(__name__)


class Inventario:
    def __init__(self, root):
        self.color_theme = get_config().get(
            'Tema', 'cor_do_tema', fallback="System")

        ctk.set_appearance_mode(self.color_theme)
        ctk.set_default_color_theme("dark-blue")

        self.root = root
        self.root.title("Configurações de Inventario")
        self.root.geometry("620x200+80+60")
        self.root.resizable(False, False)
        self.root.focus_set()

        entry_alter_list = []

        inicio, fim = periodo_padrao()

        self.periodo_manager = PeriodoManager(PeriodoInventario(inicio, fim))

        self.frame_top = criar_top_frame(self.periodo_manager, root, self.root, entry_alter_list, width=620,
                                         height=60, border_width=2, border_color='silver', corner_radius=2)

        self.frame_bot = criar_bot_frame(root, entry_alter_list, width=620,
                                         height=140, border_width=2, border_color='silver', corner_radius=5)


if __name__ == '__main__':
    try:
        root = ctk.CTk()
        app = Inventario(root)
        root.mainloop()
    except Exception:
        logger.exception('Erro ao iniciar a aplicação.')
        raise
    finally:
        if BancoDeDados.retorna_gerenciador():
            deletar_views()
            gerenciador = BancoDeDados.gerenciador()
            gerenciador.fechar()
        logger.info('Aplicação encerrada.')
