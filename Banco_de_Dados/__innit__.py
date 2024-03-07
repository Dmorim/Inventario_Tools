### Nessa pasta estão os arquivos relacionados as configurações de banco de dados ###

# Path: Banco_de_Dados/__innit__.py
    # Arquivo criado para que o Python entenda que a pasta Banco_de_Dados é um pacote, também aproveitado para documentação geral dos arquivos contidos na pasta.
    
# Path: Banco_de_Dados/Inventario_Conn.py
    # Arquivo onde é lido as informações passadas pelo usuário sobre o caminho do banco de dados e realiza a conexão na classe Connect que é chamada posteriormente para executar consultas e alterações no banco de dados.

# Path: Banco_de_Dados/Banco_de_Dados_Screen.py
    # Arquivo onde é criada a tela de configuração de banco de dados, onde o usuário pode escolher o caminho do banco de dados, bem como porta, servidor, e caminho para a fbclient. A tela é criada com a biblioteca custom tkinter (ctk)
    
# Path: Banco_de_Dados/Banco_de_Dados_Func.py
    # Arquivo onde são definidas as funções que serão utilizadas na tela de configuração de banco de dados, como a função que salva as configurações no arquivo config.ini, as que definem o filedialog, e a função do botão confirmar que salva os dados informados, envia-os para a classe Connect para a criação da banco, depois consulta no banco de dados as informações da empresa e das ultimas vendas feitas para que atualize os labels da tela root e fehce a tela de banco de dados.