import customtkinter as ctk

class Inventario:
    def __init__(self, root):
        from Banco_de_Dados.Banco_de_Dados_Screen import Interface_Banco
        from Consultas.Consultas_Screen import Consulta_Total_Screen
        from Comandos.Comandos_Screen import Comandos_Screen
        from Consultas.Gen_Funcs_Consulta import event_button_comando, event_button_consulta
        from Configuracoes.Config_Screen import config_screen
        from Datas_Config import date_treat, data_select_ini, data_select_fim
        from Banco_Images import TelaInicial
        
        
        from tkcalendar import DateEntry
        from Tk_Tooltip import ToolTip
        import datetime
        
        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("dark-blue")
        
        self.root = root
        self.root.title("Configurações de Inventario")
        self.root.geometry("510x200")
        self.root.resizable(False, False)
        self.root.focus()
        
        self.frame_top = ctk.CTkFrame(self.root, width= 510, height= 60, border_width= 2, border_color= 'silver', corner_radius= 2)
        self.frame_top.pack_propagate(False)
        self.frame_top.pack()
        self.frame_bot = ctk.CTkFrame(self.root, width= 510, height= 140, border_width= 2, border_color= 'silver', corner_radius= 5)
        self.frame_bot.pack()
        
        self.ini_date = ctk.StringVar()
        self.end_date = ctk.StringVar()
        
        
        gear_image = ctk.CTkImage(TelaInicial.gear_image_tela_inicial, size= (14, 14))
        
        self.database = ctk.CTkButton(self.frame_top, text= 'Selecione o Banco de Dados', width= 100, height= 48, command= lambda: Interface_Banco(self, self.root, entry_alter_list, button_list))
        self.consulta = ctk.CTkButton(self.frame_top, text= 'Consultas (F1)', width= 80, height= 48, command= lambda: Consulta_Total_Screen(self, self.root), state= 'disabled')
        self.comando = ctk.CTkButton(self.frame_top, text= 'Comandos (F2)', width= 60, height= 48, command= lambda: Comandos_Screen(self, self.root), state= 'disabled')
        self.dat_ini_label = ctk.CTkLabel(self.frame_top, text= 'Data Inicial:', width= 10, height= 2, font= ('', 12))
        self.dat_ini = DateEntry(self.frame_top, width= 12, background= 'darkblue', foreground= 'white', borderwidth= 2, textvariable= self.ini_date, date_pattern= 'dd/mm/yyyy')
        self.dat_fim_label = ctk.CTkLabel(self.frame_top, text= 'Data Final:', width= 10, height= 2, font= ('', 12))
        self.dat_fim = DateEntry(self.frame_top, width= 12, background= 'darkblue', foreground= 'white', borderwidth= 2, textvariable= self.end_date)
        self.gear_btt = ctk.CTkButton(self.frame_top, text= '', width= 14, height= 14, image= gear_image, command= lambda: config_screen(self.root), fg_color= 'gray')
        
        self.database._text_label.configure(wraplength= 100)
        self.consulta._text_label.configure(wraplength= 70)
        self.comando._text_label.configure(wraplength= 70)
        
        self.database.place(x= 8, y= 6)
        self.consulta.place(x= 125, y= 6)
        self.comando.place(x= 215, y= 6)
        self.dat_ini_label.place(x= 300, y= 9)
        self.dat_ini.place(x= 370, y= 6)
        self.dat_fim_label.place(x= 303, y= 35)
        self.dat_fim.place(x= 370, y= 32)
        self.gear_btt.place(x= 473, y= 6)
        
        nome_empresa_label = ctk.CTkLabel(self.frame_bot, text= '', width= 20, height= 2, font= ('', 18, 'bold'))
        razao_social_label = ctk.CTkLabel(self.frame_bot, text= 'Razão Social:', width= 20, height= 2, font= ('', 12))
        razao_social_text = ctk.CTkLabel(self.frame_bot, text= '', width= 20, height= 2, font= ('', 12))
        cnpj_label = ctk.CTkLabel(self.frame_bot, text= 'CNPJ:', width= 20, height= 2, font= ('', 12))
        cnpj_text = ctk.CTkLabel(self.frame_bot, text=  '', width= 20, height= 2, font= ('', 12))
        ie_label = ctk.CTkLabel(self.frame_bot, text= 'Inscrição Estadual:', width= 20, height= 2, font= ('', 12))
        ie_text = ctk.CTkLabel(self.frame_bot, text= '', width= 20, height= 2, font= ('', 12))
        regime_label = ctk.CTkLabel(self.frame_bot, text= 'Regime Tributário:', width= 20, height= 2, font= ('', 12))
        regime_text = ctk.CTkLabel(self.frame_bot, text= '', width= 20, height= 2, font= ('', 12))
        fone_label = ctk.CTkLabel(self.frame_bot, text= 'Telefone:', width= 20, height= 2, font= ('', 12))
        fone_text = ctk.CTkLabel(self.frame_bot, text= '', width= 20, height= 2, font= ('', 12))
        ult_emit = ctk.CTkLabel(self.frame_bot, text= 'Última Emissão:', width= 20, height= 2, font= ('', 12))
        ult_emit_text = ctk.CTkLabel(self.frame_bot, text= '', width= 20, height= 2, font= ('', 12))
        credits = ctk.CTkLabel(self.frame_bot, text= 'Desenvolvido por: Daniel Amorim', width= 20, height= 2, font= ('', 11, 'italic'))
        
        ToolTip(credits, 'Com a ajuda de Cicero Romão nas consultas SQL', 700)
        
        ano_atual = datetime.datetime.now().year
        ano_vigencia = ano_atual - 1
        # Definir o primeiro e último dia do ano passado
        primeiro_dia = datetime.datetime(ano_vigencia, 1, 1)
        ultimo_dia = datetime.datetime(ano_vigencia, 12, 31)

        # Formatar as datas como strings
        primeiro_dia_str = primeiro_dia.strftime('%d/%m/%Y')
        ultimo_dia_str = ultimo_dia.strftime('%d/%m/%Y')

        # Setar as datas
        self.dat_ini.set_date(primeiro_dia_str)
        self.dat_fim.set_date(ultimo_dia_str)
        self.data_banco_inicial = primeiro_dia.strftime('%d.%m.%Y')
        self.data_banco_final = ultimo_dia.strftime('%d.%m.%Y')
        
        entry_alter_list = [nome_empresa_label, razao_social_text, cnpj_text, ie_text, regime_text, fone_text, ult_emit_text]
        button_list = [self.consulta, self.comando]
        
        nome_empresa_label.place(relx= 0.5, y= 15, anchor= 'center')
        razao_social_label.place(x= 6, y= 33)
        razao_social_text.place(x= 84, y= 33)
        cnpj_label.place(x= 6, y= 50)
        cnpj_text.place(x= 44, y= 50)
        ie_label.place(x= 6, y= 66)
        ie_text.place(x= 114, y= 66)
        regime_label.place(x= 6, y= 83)
        regime_text.place(x= 113, y= 83)
        fone_label.place(x= 6, y= 100)
        fone_text.place(x= 62, y= 100)
        ult_emit.place(x= 6, y= 118)
        ult_emit_text.place(x= 100, y= 118)
        credits.place(relx= 0.776, rely= 0.96, anchor= 's')
        
        self.root.bind('<F1>', lambda event: event_button_consulta(self, event))
        self.root.bind('<F2>', lambda event: event_button_comando(self, event))
        self.root.bind('<Control-b>', lambda event: Interface_Banco(self, self.root, entry_alter_list, button_list))
        self.ini_date.trace_add("write", lambda *args: date_treat(self, self.ini_date, 'Inicial'))
        self.end_date.trace_add("write", lambda *args: date_treat(self, self.end_date, 'Final'))
        self.dat_ini.bind("<<DateEntrySelected>>", lambda event: data_select_ini(self, self.ini_date))
        self.dat_fim.bind("<<DateEntrySelected>>", lambda event: data_select_fim(self, self.end_date))
        
if __name__ == '__main__':
    try:
        root = ctk.CTk()
        app = Inventario(root)
        root.mainloop()
    finally:
        from Banco_de_Dados.Inventario_Conn import Connect
        if Connect.conn is not None:
            Connect.conn.close()