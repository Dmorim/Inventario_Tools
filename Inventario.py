import customtkinter as ctk

class Inventario:
    def __init__(self, root):
        from Dados_Empresa import Dados_Empresa_Screen
        from Banco_de_Dados_Screen import Interface_Banco
        
        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("dark-blue")
        
        self.root = root
        self.root.title("Configurações de Inventario")
        self.root.geometry("300x200")
        self.root.resizable(False, False)
        self.root.focus()
        
        self.frame_top = ctk.CTkFrame(self.root, width= 600, height= 60, border_width= 2, border_color= 'silver', corner_radius= 2)
        self.frame_top.pack_propagate(False)
        self.frame_top.pack()
        self.frame_bot = ctk.CTkFrame(self.root, width= 600, height= 140, border_width= 2, border_color= 'silver', corner_radius= 5)
        self.frame_bot.pack()
        
        self.database = ctk.CTkButton(self.frame_top, text= 'Selecione o Banco de Dados', width= 100, height= 48, command= lambda: Interface_Banco(self, self.root))
        self.consulta = ctk.CTkButton(self.frame_top, text= 'Consultas', width= 80, height= 48, command= lambda: print('Consulta'))
        self.comando = ctk.CTkButton(self.frame_top, text= 'Comandos', width= 60, height= 48, command= lambda: print('Comando'))
        
        self.database._text_label.configure(wraplength= 100)
        
        self.database.place(x= 8, y= 6)
        self.consulta.place(x= 125, y= 6)
        self.comando.place(x= 215, y= 6)
        
        Dados_Empresa_Screen(self, self.frame_bot)
if __name__ == '__main__':
    root = ctk.CTk()
    app = Inventario(root)
    root.mainloop()