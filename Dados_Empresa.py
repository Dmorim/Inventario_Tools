def dados_empresa_screen(self, frame_bot):
    import customtkinter as ctk
    
    nome_empresa_label = ctk.CTkLabel(frame_bot, text= 'Empresa X', width= 20, height= 2, font= ('', 18, 'bold'))
    razao_social_label = ctk.CTkLabel(frame_bot, text= 'Razão Social:', width= 20, height= 2, font= ('', 12))
    razao_social_text = ctk.CTkLabel(frame_bot, text= 'Lorem Ipsilum Lorem La', width= 20, height= 2, font= ('', 12))
    cnpj_label = ctk.CTkLabel(frame_bot, text= 'CNPJ:', width= 20, height= 2, font= ('', 12))
    cnpj_text = ctk.CTkLabel(frame_bot, text= '00.000.000/0000-00', width= 20, height= 2, font= ('', 12))
    ie_label = ctk.CTkLabel(frame_bot, text= 'Inscrição Estadual:', width= 20, height= 2, font= ('', 12))
    ie_text = ctk.CTkLabel(frame_bot, text= '00.000.000-00', width= 20, height= 2, font= ('', 12))
    regime_label = ctk.CTkLabel(frame_bot, text= 'Regime Tributário:', width= 20, height= 2, font= ('', 12))
    regime_text = ctk.CTkLabel(frame_bot, text= 'Simples Nacional', width= 20, height= 2, font= ('', 12))
    
    nome_empresa_label.place(relx= 0.5, y= 15, anchor= 'center')
    razao_social_label.place(x= 6, y= 33)
    razao_social_text.place(x= 84, y= 33)
    cnpj_label.place(x= 6, y= 50)
    cnpj_text.place(x= 44, y= 50)
    ie_label.place(x= 6, y= 66)
    ie_text.place(x= 114, y= 66)
    regime_label.place(x= 6, y= 83)
    regime_text.place(x= 113, y= 83)