import customtkinter as ctk

class Inventario:
    def __init__(self, root):
        self.root = root
        self.root.title("Configurações de Inventario")
        self.root.geometry("300x200")
        self.root.resizable(False, False)
        self.root.focus()
        
        self.frame_top = ctk.CTkFrame(self.root, width= 600, height= 60, border_width= 2, border_color= 'silver', corner_radius= 2)
        self.frame_top.pack()
        self.frame_bot = ctk.CTkFrame(self.root, width= 600, height= 140, border_width= 2, border_color= 'silver', corner_radius= 5)
        self.frame_bot.pack()
        
if __name__ == '__main__':
    root = ctk.CTk()
    app = Inventario(root)
    root.mainloop()