def Set_Dados_Padrao(entrys_list):
    entrys_list[0].insert(0, 'localhost')
    entrys_list[1].insert(0, '3050')
    entrys_list[3].insert(0, 'C:/Program Files/Firebird/Firebird_3_0/fbclient.dll')
    
def Caminho_Banco_Dir(Banco_Screen, entrys_list):
    from tkinter import filedialog
    caminho = filedialog.askopenfilename(title= 'Caminho para o banco de dados',parent= Banco_Screen, filetypes= [('Firebird Database', '*.fdb')], initialdir= 'C:\\Sistech\\Dados')
    if caminho:
        entrys_list[2].delete(0, 'end')
        entrys_list[2].insert(0, caminho)
        
def Caminho_Fb_Dir(Banco_Screen, entrys_list):
    from tkinter import filedialog
    caminho = filedialog.askopenfilename(title= 'Caminho para o fbclient',parent= Banco_Screen, filetypes= [('Firebird Dll', '*.dll')], initialdir= 'C:\\Program Files\\Firebird\\Firebird_3_0')
    if caminho:
        entrys_list[3].delete(0, 'end')
        entrys_list[3].insert(0, caminho)