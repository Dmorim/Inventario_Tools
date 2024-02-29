def tutorial_screen(parent):
    import customtkinter as ctk
    from Tutorial.Tutorial_Func import Tutorial_Ini, tutorial_text_list, on_click_foward_button
    from Outros.Banco_Images import Tutorial
    
    tutorial = ctk.CTkToplevel(parent)
    tutorial.title("Ajuda")
    tutorial.geometry("390x382+80+60")
    tutorial.resizable(False, False)
    tutorial.transient(parent)
    tutorial.focus_set()
    tutorial.grab_set()
    
    tut_01_image = ctk.CTkImage(Tutorial.tut_img_01_tutorial, size= (390, 170))
    tut_02_image = ''
    tut_03_image = ''
    tut_04_image = ''
    
    image_list = [tut_01_image, tut_02_image, tut_03_image, tut_04_image, '', '']
    
    image_frame = ctk.CTkFrame(tutorial, width= 390, height= 170, border_width= 2, border_color= 'silver', corner_radius= 5)
    text_frame = ctk.CTkFrame(tutorial, width= 390, height= 160, border_width= 2, border_color= 'silver', corner_radius= 5)
    buttons_frame = ctk.CTkFrame(tutorial, width= 390, height= 40, border_width= 2, border_color= 'silver', corner_radius= 5)
    
    image_label = ctk.CTkLabel(image_frame, width= 380, height= 160, image= tut_01_image, text= '')
    
    text_label = ctk.CTkLabel(text_frame, width= 390, height= 160, text= Tutorial_Ini, font= ('', 12), wraplength= 380)
    
    fowrd_button = ctk.CTkButton(tutorial, text= 'Próximo', width= 10, height= 2, command= lambda: on_click_foward_button(image_list, tutorial_text_list, image_label, text_label, 2, 2, buttons_list))
    back_button = ctk.CTkButton(tutorial, text= 'Anterior', width= 10, height= 2, command= lambda: print('prev'))
    
    buttons_list = [fowrd_button, back_button]
    
    image_frame.pack()
    text_frame.pack()
    buttons_frame.pack()
    
    image_label.pack(padx= 5, pady= 5)
    text_label.pack(fill= 'both', expand= True, padx= 5, pady= 5)
    
    fowrd_button.place(x= 205, y= 356)
    back_button.place(x= 135, y= 356)