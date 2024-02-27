def config_screen(parent):
    import customtkinter as ctk
    
    config = ctk.CTkToplevel(parent)
    config.title('Configurações')
    config.geometry('300x200')
    
    config_title_label = ctk.Label(config, text='Configurações', font=('Arial', 14, 'bold'))
    
    
    config_title_label.place(relx=0.5, rely=0.1, anchor='center')