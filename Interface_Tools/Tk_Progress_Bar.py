from customtkinter import CTkProgressBar, CTkToplevel, CTkLabel
from random import randint


class ProgressBarHandler:
    def __init__(self, parent, title: str, width: int = 400, height: int = 130, x: int = 200, y: int = 150):
        self.parent = parent
        self.title = title
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self._ciclo = {'label': None, 'i': 0}

    def _generate_label_text_list(self) -> list[str]:
        list_of_labels = ['Você pode gerar várias consultas ao mesmo tempo',
                          'Evite fechar a tela com uma consulta/comando em andamento',
                          'O botão "ESC" fecha a maioria das telas no sistema',
                          'Os botões "Listar Produtos" e "Copiar Valor" só são habilitados quando a consulta é concluída',
                          'Você só poderá corrigir uma distorção de saldo depois que gerar ela pelo menos uma vez.',
                          'O valor de compra é gerado após a exclusão de CFOPs específicos',
                          'Belezebufo foi um sapo há 70 milhões de anos e predava dinossauros bebês',
                          'Uma enchente pode ter sido responsável pela extinção dos mamutes',
                          'Se você precisar de uma versão antiga do GP, o owncloud tem uma pasta para isso',
                          'O botão "Gerar Dist. de Saldo" só é habilitado quando a consulta é concluída',
                          'Na aba de comandos, existe um campo vazio para digitar um comando personalizado',
                          'Cuidado ao encontrar Talyta no caminho para a empresa, você pode ter uma surpresa desagradável',
                          'Na dúvida, ligue 22 ou 24',
                          'Se sua impressora não funcionar, veja com Fábio, digo Çávio, quer dizer Sasa...',
                          'O silêncio marca a ausência de Clea',
                          'Exsqueça o inventário',
                          'Uma vez o sábio Romão disse: "Sei o que é isso não" ao ver uma tela de erro do GP',
                          'Com certeza alguém achou que todas as dicas seriam úteis',
                          'Procure o criador do aplicativo caso tenha alguma dúvida, ninguém é tão inteligente quanto ele',
                          'Pendência é só um número',
                          'É Inevitável que certa loja apareça por aqui',
                          'Água aquecida é considerada um tipo de poluição',
                          'Confira sempre se o banco de dados é o correto antes de gerar uma consulta',
                          'Você pode usar a data da última emissão para ter certeza de que o banco não é retaguarda',
                          'Algum dia quem sabe sairá um EscritaTools',
                          'Se algum erro existir, Letícia com certeza terá escrito sobre ele',
                          'Não, eu não sei fazer inventário, se tiver dúvida fale com Taumar :D',
                          'Ao usar o InvTools você concorda que todo inventário gerado com sucesso tem minha participação',
                          'Ao usar o InvTools você concorda que todo inventário gerado com falha não tem nada a ver comigo',
                          'Contadores parecem amigos, mas irão cobrar o arquivo sem autorizar o PDF',
                          'Ajudando o setor dos inventários desde de 2023',
                          'Não, esse programa não cria o arquivo de inventário e envia para o contador',
                          'Mais do que um sistema, um system',
                          'Você consegue encontrar o código fonte e a versão mais recente do InvTools no GitHub',
                          'Aproveite e me siga no GitHub, nunca se sabe o que eu posso criar de útil por lá',
                          'Se você estiver lendo essa mensagem, saíba que você é o suficiente e estou torcendo por ti',
                          ]
        return list_of_labels

    def _iniciar_ciclo_mensagens(self, intervalo_ms: int = 6000):
        msgs = self._generate_label_text_list()
        self._ciclo['i'] = randint(0, len(msgs) - 1)

        def tick():
            self.tip_label.configure(text=f'{msgs[self._ciclo["i"]]}')

            # Sorteia o próximo índice garantindo que seja diferente do atual
            ultimo = self._ciclo['i']
            proximos = [i for i in range(len(msgs)) if i != ultimo]
            self._ciclo['i'] = proximos[randint(0, len(proximos) - 1)]

            self._ciclo['label'] = self.screen.after(intervalo_ms, tick)

        tick()

    def _create_tip_label(self):
        self.tip_label = CTkLabel(
            self.screen,
            text='',
            font=('', 15),
            text_color='gray60',
            wraplength=self.width - 10,   # quebra linha se o texto for longo
            justify='center'
        )
        self.tip_label.place(relx=0.50, rely=0.60, anchor='center')

    def _create_status_label(self):
        self.status_label = CTkLabel(
            self.screen, text="Carregando...", font=("", 16))
        self.status_label.place(relx=0.5, rely=0.3, anchor='center')

    def _create_progress_bar(self):
        self.progress_bar = CTkProgressBar(
            self.screen, mode='indeterminate', width=self.width - 50)
        self.progress_bar.place(relx=0.5, rely=0.8, anchor='center')
        self.progress_bar.start()

    def create_screen(self):
        self.screen = CTkToplevel(self.parent)
        self.screen.title(self.title)
        self.screen.geometry(f"{self.width}x{self.height}+{self.x}+{self.y}")
        self.screen.resizable(False, False)
        self.screen.transient(self.parent)
        self.screen.focus_set()
        self.screen.grab_set()

        self._create_status_label()
        self._create_tip_label()
        self._create_progress_bar()
        self._iniciar_ciclo_mensagens()

        return self

    def atualizar_status(self, novo_status: str):
        self.status_label.configure(text=novo_status)

    def finalizar(self):
        if self._ciclo['label'] is not None:
            self.screen.after_cancel(self._ciclo['label'])
        self.progress_bar.stop()
        self.screen.destroy()
