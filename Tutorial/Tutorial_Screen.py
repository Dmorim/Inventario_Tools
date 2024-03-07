def tutorial_screen(parent):
    import customtkinter as ctk # Importa a biblioteca customtkinter como ctk
    
    # Importa as funções e variáveis do arquivo Tutorial_Func
    from Tutorial.Tutorial_Func import Tutorial_Ini, tutorial_text_list, image_list,  on_click_foward_button, on_click_backwards_button, on_click_volt_ini_button, tut_ini_image
    
    tutorial = ctk.CTkToplevel(parent) # Cria a janela tutorial como um Toplevel do parent
    tutorial.title("Ajuda")
    tutorial.geometry("390x382+80+60")
    tutorial.resizable(False, False)
    tutorial.transient(parent)
    tutorial.focus_set()
    tutorial.grab_set()
    
    # Criação dos frames da tela do tutorial
    image_frame = ctk.CTkFrame(tutorial, width= 390, height= 170, border_width= 2, border_color= 'silver', corner_radius= 5)
    text_frame = ctk.CTkFrame(tutorial, width= 390, height= 160, border_width= 2, border_color= 'silver', corner_radius= 5)
    buttons_frame = ctk.CTkFrame(tutorial, width= 390, height= 40, border_width= 2, border_color= 'silver', corner_radius= 5)
    
    # Criação do label que será utilizado para exibir a imagem
    image_label = ctk.CTkLabel(image_frame, width= 380, height= 160, text= '', image= tut_ini_image)
    
    # Criação do label que será utilizado para exibir o texto
    text_label = ctk.CTkLabel(text_frame, width= 390, height= 160, text= Tutorial_Ini, font= ('', 12), wraplength= 380)
    
    # Criação dos botões da tela do tutorial
    fowrd_button = ctk.CTkButton(tutorial, text= 'Próximo', width= 10, height= 2, command= lambda: on_click_foward_button(image_list, tutorial_text_list, image_label, text_label, 1, 1, buttons_list))
    back_button = ctk.CTkButton(tutorial, text= 'Anterior', width= 10, height= 2, command= lambda: on_click_backwards_button(image_list, tutorial_text_list, image_label, text_label, 1, 1, buttons_list), state= 'disabled')
    volt_ini_button = ctk.CTkButton(tutorial, text= 'Voltar ao Início', width= 15, height= 2, command= lambda: on_click_volt_ini_button(image_list, tutorial_text_list, image_label, text_label, 1, 1, buttons_list))
    sair_button = ctk.CTkButton(tutorial, text= 'Sair do tutorial', width= 10, height= 2, command= tutorial.destroy)
    
    # Criação da lista de botões
    buttons_list = [fowrd_button, back_button, volt_ini_button]
    
    # Posicionamento dos frames
    image_frame.pack()
    text_frame.pack()
    buttons_frame.pack()
    
    # Posicionamento dos widgets
    text_label.pack(fill= 'both', expand= True, padx= 5, pady= 5)
    
    # Posicionamento dos widgets da tela do frame image
    volt_ini_button.place(x= 8, y= 356)
    fowrd_button.place(x= 205, y= 356)
    back_button.place(x= 135, y= 356)
    sair_button.place(x= 298, y= 356)
    
    tutorial.bind('<Escape>', lambda event: tutorial.destroy()) # Associa o evento de apertar a tecla Esc para fechar a janela