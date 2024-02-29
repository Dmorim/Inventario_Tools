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


tutorial_text_list = [Tutorial_Ini, Tutorial_01, Tutorial_02, Tutorial_03, Tutorial_04, Tutorial_05]

def on_click_foward_button(image_list, text_list, image_label, text_label, image_number, text_number, buttons_list):
    image_label.pack_forget()
    image_label.configure(image= image_list[image_number - 1])
    image_label.pack(padx= 5, pady= 5)
    
    text_label.pack_forget()
    text_label.configure(text= text_list[text_number - 1])
    text_label.pack(padx= 5, pady= 5)
    
    buttons_list[0].configure(command= lambda: on_click_foward_button(image_list, text_list, image_label, text_label, image_number + 1, text_number + 1, buttons_list))
    