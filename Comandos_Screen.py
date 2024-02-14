def Comandos_Screen(self, parent):
    import customtkinter as ctk
    
    comando = ctk.CTkToplevel(parent)
    comando.geometry("550x270+150+135")
    comando.title("Comandos")
    comando.resizable(False, False)
    comando.focus_set()
    comando.grab_set()
    
    frame_l = ctk.CTkFrame(comando, width= 275, height= 270, border_width= 2, border_color= 'silver', corner_radius= 5)
    frame_r = ctk.CTkFrame(comando, width= 275, height= 270, border_width= 2, border_color= 'silver', corner_radius= 5)
    
    
    frame_l.pack_propagate(False)
    frame_l.pack(side= 'left')
    
    frame_r.pack_propagate(False)
    frame_r.pack(side= 'right')