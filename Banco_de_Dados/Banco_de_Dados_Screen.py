def Interface_Banco(self, root, entry_alter_list, button_list):
    import customtkinter as ctk # Importa a biblioteca customtkinter como ctk
    
    # Importa as funções Set_Dados_Padrao, Caminho_Banco_Dir, Caminho_Fb_Dir, on_click_confirm do arquivo Banco_de_Dados_Func
    from Banco_de_Dados.Banco_de_Dados_Func import Set_Dados_Padrao, Caminho_Banco_Dir, Caminho_Fb_Dir, on_click_confirm
    
    # Cria a tela Banco_Screen como TopLevel e define suas configurações
    Banco_Screen = ctk.CTkToplevel(root)
    Banco_Screen.title("Configurações de Banco de Dados")
    Banco_Screen.geometry("370x225")
    Banco_Screen.resizable(False, False)
    Banco_Screen.transient(root) # Define a tela como transiente, ou seja, como janela filha da janela root
    Banco_Screen.focus_set()
    Banco_Screen.grab_set() # Impede que a janela root seja acessada enquanto a janela Banco_Screen estiver aberta
    
    # Cria um frame frame_in dentro da tela Banco_Screen e define suas configurações
    frame_in = ctk.CTkFrame(Banco_Screen, width= 366, height= 180, border_width= 2, border_color= 'silver', corner_radius= 5)
    frame_in.pack_propagate(False)
    frame_in.pack(padx= 5, pady= 25)
    
    # Cria os widgets da tela Banco_Screen
    sel_banco_label = ctk.CTkLabel(Banco_Screen, text= 'Conexão com o Banco de Dados', width= 20, height= 2, font= ('', 14, 'bold'))
    confirm_button = ctk.CTkButton(Banco_Screen, width= 25, height= 7, text= 'Confirmar', command= lambda: on_click_confirm(self, entrys_list, Banco_Screen, entry_alter_list, button_list), text_color= 'silver')
    cancel_button = ctk.CTkButton(Banco_Screen, width= 75, height= 7, text= 'Cancelar', command= lambda: Banco_Screen.destroy(), text_color= 'silver')    
    
    # Posiciona os widgets na tela Banco_Screen
    sel_banco_label.place(relx= 0.5, y= 9, anchor= 'center')
    confirm_button.place(x= 298, y= 202)
    cancel_button.place(x= 218, y= 202)
    
    # Cria os widgets do frame frame_in
    serv_label = ctk.CTkLabel(frame_in, text= 'Servidor', width= 20, height= 2, font= ('', 12))
    serv_entry = ctk.CTkEntry(frame_in, width= 115, font= ('', 12), fg_color = ('lightblue', 'silver'), text_color= 'black')
    porta_label = ctk.CTkLabel(frame_in, text= 'Porta', width= 20, height= 2, font= ('', 12))
    porta_entry = ctk.CTkEntry(frame_in, width= 115, font= ('', 12), fg_color = ('lightblue', 'silver'), text_color= 'black')
    caminho_bd_label = ctk.CTkLabel(frame_in, text= 'Caminho do banco de dados', width= 20, height= 2, font= ('', 12))
    caminho_bd_entry = ctk.CTkEntry(frame_in, width= 312, font= ('', 12), fg_color = ('lightblue', 'silver'), text_color= 'black')
    caminho_bd_file_button = ctk.CTkButton(frame_in, width= 30, height= 24, text= '...', command= lambda: Caminho_Banco_Dir(self, Banco_Screen, entrys_list))
    caminho_fb_label = ctk.CTkLabel(frame_in, text= 'Caminho da FBClient', width= 20, height= 2, font= ('', 12))
    caminho_fb_entry = ctk.CTkEntry(frame_in, width= 312, font= ('', 12), fg_color = ('lightblue', 'silver'), text_color= 'black')
    caminho_fb_file_button = ctk.CTkButton(frame_in, width= 30, height= 24, text= '...', command= lambda: Caminho_Fb_Dir(self, Banco_Screen, entrys_list))
    
    # Posiciona os widgets no frame frame_in
    serv_label.place(x= 8, y= 5)
    serv_entry.place(x= 6, y= 22)
    porta_label.place(x= 240, y= 5)
    porta_entry.place(x= 240, y= 22)
    caminho_bd_label.place(x= 8, y= 60)
    caminho_bd_entry.place(x= 6, y= 77)
    caminho_bd_file_button.place(x= 322, y= 79)
    caminho_fb_label.place(x= 8, y= 115)
    caminho_fb_entry.place(x= 6, y= 132)
    caminho_fb_file_button.place(x= 322, y= 134)
    
    # Lista de entrys que serão utilizadas para armazenar os dados informados pelo usuário para obtenção dos valores escolhidos
    entrys_list = [serv_entry, porta_entry, caminho_bd_entry, caminho_fb_entry]
    
    # Chama a função Set_Dados_Padrao do arquivo Banco_de_Dados_Func para preencher os entrys com os dados padrão
    Set_Dados_Padrao(entrys_list)
    
    # Define a tecla de atalho para fechar a tela e para confirmar a seleção
    Banco_Screen.bind("<Escape>", lambda e: Banco_Screen.destroy())
    Banco_Screen.bind("<F5>", lambda event: confirm_button.invoke())
    