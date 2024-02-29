from customtkinter import CTkImage
from Outros.Banco_Images import Tutorial

Tutorial_Ini = """
Olá! Seja bem vindo ao tutorial do programa de Inventario.
Aqui você aprenderá a utilizar as funções do programa. Tenha em mente que esse não é um tutorial para fazer um inventário, mas sim para utilizar o programa de Inventario.
Caso queira aprender a fazer um inventário, confira os tutoriais da Sistech ou então com algum técnico responsável.
Para continuar, clique em Próximo.
"""
Tutorial_01 = """
Começamos com nossa tela inicial, dividida em duas partes somente a primeira exige algum nível de interação.
Temos três botões, cada um será explicado posteriormente, além de escolha de datas, o botão de configurações e ajuda.
As datas seleciondas irão determinar a data que o sistema irá gerar os dados, ela vem de padrão o ano anterior por completo.
A parte de baixo é onde será exibido diversas informações bastante úteis sobre a empresa selecionada.
"""
Tutorial_02 = """
A primeira coisa a se fazer para começar a usar o sistema é selecionar o banco de dados que você vai trabalhar, você faz isso clicando no botão Selecione o Banco de Dados ou apertando CTRL + B no seu teclado.
"""
Tutorial_03 = """
A tela de seleção de banco de dados já vem pré-preenchida com a maioria dos dados de maneira padrão, cabendo a você apenas escolher o caminho do banco de dados, ou trocar a porta e/ou caminho para fbclient
Com todos os caminhos selecionados, basta clicar em confirmar que o sistema fará a conexão, vale lembrar que caso já exista alguma base conectada, o sistema irá desconectar dessa para conectar na escolhida.
"""
Tutorial_04 = """
Caso haja problema de conexão com o banco de dados uma mensagem com o erro será exibida possibilitando você corrigir os dados da conexão.
"""
Tutorial_05 = """
Com a conexão estabelecida, além dos dados da empresa serem transportados para a tela inicial, os botões de Consultas e Comandos também ficam disponíveis para serem utilizados.
"""
Tutorial_06 = """
Passando para a próxima tela, temos a tela de Consultas, onde é possível fazer diversas consultas na base conectada.
Vale ressaltar que nessa tela não é possível fazer alterações na base de dados, apenas consultar os valores atuais dela.
"""
Tutorial_07 = """
Temos a possibilidade de fazer consultas de valores, com o valor do inventário, valor de vendas e valor de compras. E também consultas relacionadas a produtos, essas tendo a opção de listar os produtos encontrado.
Caso encontre dificuldade em entender o que cada consulta faz, basta passar o mouse por cima dela que uma Tooltip lhe informara o que for preciso.
"""
Tutorial_08 = """
Concluindo, temos a tela de Comandos, onde é possível fazer alterações e correções na base de dados.
"""
Tutorial_09 = """
Na tela você pode você pode ver todos os comandos que podem ser executados e assim como na tela de Consultas, basta passar o mouse por cima deles para saber o que cada um faz.
Além disso há um comando vazio em que você pode digitar o comando que deseja executar.
Todos os comandos marcados serão executados, antes de serem executados, o sistema irá perguntar se você tem certeza que deseja executar os comandos e exibir eles em uma lista.
"""
Tutorial_10 = """
Esse por fim é o final do tutorial, espero que tenha sido útil e que você tenha aprendido a utilizar o programa de Inventario. Caso tenha alguma dúvida, não hesite em perguntar.
"""

tutorial_text_list = [Tutorial_01, Tutorial_02, Tutorial_03, Tutorial_04, Tutorial_05, Tutorial_06, Tutorial_07, Tutorial_08, Tutorial_09, Tutorial_10]

tut_ini_image = CTkImage(Tutorial.tut_img_ini_tutorial, size= (390, 170))
tut_01_image = CTkImage(Tutorial.tut_img_01_tutorial, size= (390, 170))
tut_02_image = CTkImage(Tutorial.tut_img_02_tutorial, size= (390, 170))
tut_03_image = CTkImage(Tutorial.tut_img_03_tutorial, size= (390, 170))
tut_04_image = CTkImage(Tutorial.tut_img_04_tutorial, size= (390, 170))
tut_05_image = CTkImage(Tutorial.tut_img_05_tutorial, size= (390, 170))
tut_06_image = CTkImage(Tutorial.tut_img_06_tutorial, size= (390, 170))
tut_07_image = CTkImage(Tutorial.tut_img_07_tutorial, size= (390, 170))
tut_08_image = CTkImage(Tutorial.tut_img_08_tutorial, size= (390, 170))
tut_09_image = CTkImage(Tutorial.tut_img_09_tutorial, size= (390, 170))
tut_10_image = CTkImage(Tutorial.tut_img_10_tutorial, size= (390, 170))


image_list = [tut_01_image, tut_02_image, tut_03_image, tut_04_image, tut_05_image, tut_06_image, tut_07_image, tut_08_image, tut_09_image, tut_10_image]

def on_click_foward_button(image_list, text_list, image_label, text_label, image_number, text_number, buttons_list):
    image_label.pack_forget()
    image_label.configure(image= image_list[image_number - 1])
    image_label.pack(padx= 5, pady= 5)
    
    text_label.pack_forget()
    text_label.configure(text= text_list[text_number - 1])
    text_label.pack(padx= 5, pady= 5)
    
    buttons_list[0].configure(command= lambda: on_click_foward_button(image_list, text_list, image_label, text_label, image_number + 1, text_number + 1, buttons_list))
    buttons_list[1].configure(state= "normal")
    buttons_list[1].configure(command= lambda: on_click_backwards_button(image_list, text_list, image_label, text_label, image_number - 1, text_number - 1, buttons_list))
    if image_number == 10:
        buttons_list[0].configure(state= "disabled")
        
def on_click_backwards_button(image_list, text_list, image_label, text_label, image_number, text_number, buttons_list):
    image_label.pack_forget()
    image_label.configure(image= image_list[image_number - 1])
    image_label.pack(padx= 5, pady= 5)
    
    text_label.pack_forget()
    text_label.configure(text= text_list[text_number - 1])
    text_label.pack(padx= 5, pady= 5)
    
    buttons_list[0].configure(command= lambda: on_click_foward_button(image_list, text_list, image_label, text_label, image_number + 1, text_number + 1, buttons_list))
    buttons_list[1].configure(command= lambda: on_click_backwards_button(image_list, text_list, image_label, text_label, image_number - 1, text_number - 1, buttons_list))
    if image_number == 0:
        buttons_list[1].configure(state= "disabled")
    
def on_click_volt_ini_button(image_list, text_list, image_label, text_label, image_number, text_number, buttons_list):
    image_label.pack_forget()
    image_label.configure(image= tut_ini_image)
    image_label.pack(padx= 5, pady= 5)
    
    text_label.pack_forget()
    text_label.configure(text= Tutorial_Ini)
    text_label.pack(padx= 5, pady= 5)
    
    buttons_list[0].configure(command= lambda: on_click_foward_button(image_list, text_list, image_label, text_label, image_number, text_number, buttons_list))
    buttons_list[0].configure(state= 'normal')
    buttons_list[1].configure(state= "disabled")
    buttons_list[1].configure(command= lambda: on_click_backwards_button(image_list, text_list, image_label, text_label, image_number, text_number, buttons_list))    