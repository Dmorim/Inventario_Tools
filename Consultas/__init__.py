### Nessa pasta estão todas os arquivos vinculados a tela de Consultas do sistema, acessada pelo menu principal ###

#OBS:
    # A lógica das consultas é a mesma para quase todas as telas, variando apenas a query que é executada
    # Para evitar repetição de comentários, a lógica será explicada apenas uma vez nesse arquivo, com os comentários específicos no arquivo Consultas/Consultas_Classi_Pro_Screen.py
    # As consultas de: Valor de Inventário, Valor de Venda, Valor de Compra e Distorção de saldo seguem lógicas semelhantes, porem adptadas para seus registros, elas terão comentários específicos em seus arquivos.
    # O arquivo Consultas/Consultas_Screen.py terá comentários específicos já que é a tela principal de consultas e tem um funcionamento diferente das outras.

# Logica de funcionamento das consultas:
    # Cada consulta realizada tem seu arquivo responsável por criar a tela, ese arquivo começa com Consultas_ e termina com _Screen.py
    # O modelo da tela criada é gerada pelo arquivo Consultas/Consultas_Val_Screen.py, todas as consultas geram essa tela e adicionam somente os labels e os botões
    # Um dos labels criados tem como valor do seu texto uma função que é importada do arquivo Consultas/Gen_Funcs_Consultas.py, essa função recebe como argumento a query e retorna o valor da consulta em string para ser exibido.
    # As telas podem ter um ou dois botões. O botão que vai ter obrigatóriamente é o botão de copiar valor, que executa uma função em Consultas/Gen_Funcs_Consultas.py que copia o valor da consulta para a área de transferência.
    # O segundo botão que não aparece sempre é o de gerar a lista com os valores da consulta, esse botão chama um arquivo que tem o mesmo nome que o arquivo da consulta realizada, trocando apenas o final _Screen.py por _List.py.
    # O arquivo _List.py tem basicamente o mesmo funcionamento e estrutura para todos os outros, no entanto é feito de maneira individual principalmente por conta da montagem da lista que pode variar de acordo com a consulta realizada.
    # Todos os arquivos List tem uma função para criar a tela, uma segunda função para consultar no banco de dados os valores da lista e uma terceira função responsável por tratar os valores obtidos do banco e montar a lista com eles.
    # O arquivo com os comentários específicos para a listagem está em Consultas/Consultas_Classi_Pro_List.py
    
## Abaixo segue uma lista com cada nome de arquivo e sua respectiva consulta:
    # Consultas/Consultas_Val_Inv_Screen.py -> Consulta o valor de inventário.
    # Consultas/Consultas_Val_Ven_Screen.py -> Consulta o valor de venda.
    # Consultas/Consultas_Val_Ent_Screen.py -> Consulta o valor de compra.
    # Consultas/Consultas_Quant_Maior_Screen.py -> Consulta produtos que tem quantidade lançada maior que 999999 na tabela IN01LAN
    # Consultas/Consultas_ZCusto_Screen.py -> Consulta produtos com o preço de custo zerado.
    # Consultas/Consultas_Preve_Precu_Precom_Screen.py -> Consulta produtos com preço de custo, compra e venda zerados.
    # Consultas/Consultas_Precu_Preve_Screen.py -> Consulta produtos com preço de custo maior que o de venda.
    # Consultas/Consultas_NZer_Prod_Screen.py -> Consulta produtos com saldo não zerados, ou seja, saldos menores que 1, mas maiores que zero.
    # Consultas/Consultas_Dist_Saldo_Screen.py -> Consulta produtos com distorção de saldo.
    # Consultas_Consultas_Contr_Estq_Screen.py -> Consulta produtos com o campo Controla_Estoque com N na tabela IN01LAN.
    # Consultas/Consultas_Consultas_Classi_Pro_Screen.py -> Consulta produtos com classificação de produto vazia.