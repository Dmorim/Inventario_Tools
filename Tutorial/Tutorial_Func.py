Tutorial_Ini = """
Olá! Seja bem vindo ao tutorial do programa de Inventario.
Aqui você aprenderá a utilizar as funções do programa. Tenha em mente que esse não é um tutorial para fazer um inventário, mas sim para utilizar o programa de Inventario.
Caso queira aprender a fazer um inventário, confira os tutoriais da Sistech ou então com algum técnico responsável.
Para continuar, clique em Próximo.
"""

tutorial_text_list = [Tutorial_Ini, 'teste 1', 'teste 2', 'teste 3']

def on_click_foward_button(image_list, text_list, image_label, text_label, image_number, text_number, buttons_list):
    image_label.pack_forget()
    image_label.configure(image= image_list[image_number - 1])
    image_label.pack(padx= 5, pady= 5)
    
    text_label.pack_forget()
    text_label.configure(text= text_list[text_number - 1])
    text_label.pack(padx= 5, pady= 5)
    
    buttons_list[0].configure(command= lambda: on_click_foward_button(image_list, text_list, image_label, text_label, image_number + 1, text_number + 1, buttons_list))
    