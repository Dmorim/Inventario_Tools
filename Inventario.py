import datetime
import customtkinter as ctk

from Outros.Logger.Get_Logger import get_logger
from Outros.Periodo_Inventario import (TIPO_ANUAL, TIPO_MENSAL, TIPO_PERSONALIZADO,
                                       calcular_periodo, periodo_padrao, formatar_banco, MESES_REVERSO)
from Inv_Screen.Inv_Top_Frame import criar_top_frame
from Inv_Screen.Inv_Bot_Frame import criar_bot_frame
from Configuracoes.Config_Manager import get_config
from Banco_de_Dados.Conexao_Banco_Dados.Inventario_Conn import BancoDeDados

logger = get_logger(__name__)


class Inventario:
    def __init__(self, root):
        self.color_theme = get_config().get(
            'Tema', 'cor_do_tema', fallback="System")

        ctk.set_appearance_mode(self.color_theme)
        ctk.set_default_color_theme("dark-blue")

        self.root = root
        self.root.title("Configurações de Inventario")
        self.root.geometry("530x200+80+60")
        self.root.resizable(False, False)
        self.root.focus_set()

        self.entry_alter_list = []

        self.frame_top = criar_top_frame(self, root, self.entry_alter_list, width=530,
                                         height=60, border_width=2, border_color='silver', corner_radius=2)

        self.frame_bot = criar_bot_frame(root, self.entry_alter_list, width=530,
                                         height=140, border_width=2, border_color='silver', corner_radius=5)

    def _periodo_selecionado(self):
        tipo = self.data_setada.get()

        if tipo == TIPO_MENSAL:
            mes = MESES_REVERSO.get(self.mes_combo.get())
            if mes is None:
                mes = datetime.date.today().month
            return calcular_periodo(TIPO_MENSAL, mes=mes)

        if tipo == TIPO_PERSONALIZADO:
            return calcular_periodo(TIPO_PERSONALIZADO,
                                    ini=self.dat_ini.get_date(),
                                    fim=self.dat_fim.get_date())

        if tipo == TIPO_ANUAL:
            ano = int(self.ano_combo.get()) if self.ano_combo.get(
            ) else datetime.date.today().year
            return calcular_periodo(TIPO_ANUAL, ano=ano)

        return periodo_padrao()

    @property
    def data_banco_inicial(self):
        return formatar_banco(self._periodo_selecionado()[0])

    @property
    def data_banco_final(self):
        return formatar_banco(self._periodo_selecionado()[1])


if __name__ == '__main__':
    logger.info('Iniciando aplicação Inventario Tools.')
    try:
        root = ctk.CTk()
        app = Inventario(root)
        logger.info('Janela principal criada com sucesso.')
        root.mainloop()
    except Exception:
        logger.exception('Erro ao iniciar a aplicação.')
        raise
    finally:
        if BancoDeDados.retorna_gerenciador():
            logger.info('Fechando pool de conexões do banco.')
            gerenciador = BancoDeDados.gerenciador()
            gerenciador.fechar()
        logger.info('Aplicação encerrada.')
