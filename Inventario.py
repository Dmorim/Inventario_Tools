import customtkinter as ctk

class Inventario:
    def __init__(self, root):
        from Banco_de_Dados_Screen import Interface_Banco
        from Consultas_Screen import Consulta_Total_Screen
        
        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("dark-blue")
        
        self.root = root
        self.root.title("Configurações de Inventario")
        self.root.geometry("350x200")
        self.root.resizable(False, False)
        self.root.focus()
        
        self.frame_top = ctk.CTkFrame(self.root, width= 350, height= 60, border_width= 2, border_color= 'silver', corner_radius= 2)
        self.frame_top.pack_propagate(False)
        self.frame_top.pack()
        self.frame_bot = ctk.CTkFrame(self.root, width= 350, height= 140, border_width= 2, border_color= 'silver', corner_radius= 5)
        self.frame_bot.pack()
        
        self.database = ctk.CTkButton(self.frame_top, text= 'Selecione o Banco de Dados', width= 100, height= 48, command= lambda: Interface_Banco(self, self.root, entry_alter_list))
        self.consulta = ctk.CTkButton(self.frame_top, text= 'Consultas', width= 80, height= 48, command= lambda: Consulta_Total_Screen(self, self.root))
        self.comando = ctk.CTkButton(self.frame_top, text= 'Comandos', width= 60, height= 48, command= lambda: print('Comando'))
        
        self.database._text_label.configure(wraplength= 100)
        
        self.database.place(x= 8, y= 6)
        self.consulta.place(x= 125, y= 6)
        self.comando.place(x= 215, y= 6)
        
        
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
        
        entry_alter_list = [nome_empresa_label, razao_social_text, cnpj_text, ie_text, regime_text, fone_text]
        
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
        
if __name__ == '__main__':
    try:
        root = ctk.CTk()
        app = Inventario(root)
        root.mainloop()
    finally:
        from Inventario_Conn import Connect
        Connect.conn.close()