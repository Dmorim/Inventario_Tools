from customtkinter import CTkProgressBar, CTkToplevel, CTkLabel


class ProgressBarHandler:
    def __init__(self, parent, title: str, width: int = 300, height: int = 100, x: int = 200, y: int = 150):
        self.parent = parent
        self.title = title
        self.width = width
        self.height = height
        self.x = x
        self.y = y

    def _generate_label_text_list(self) -> list[str]:
        list_of_labels = ['Você pode gerar várias consultas ao mesmo tempo',
                          'Evite fechar a tela com uma consulta/comando em andamento',
                          'O botão "ESC" fecha a maioria das telas no sistema',
                          'Os botões "Listar Produtos" e "Copiar Valor" só são habilitados quando a consulta é concluída',
                          'Você só poderá corrigir uma distorção de saldo depois que gerar ela pelo menos uma vez.',
                          'O valor de compra é gerado após a exclusão de CFOPs específicos',
                          ]
        return list_of_labels

    def _create_loading_label(self):
        self.loading_label = CTkLabel(
            self.screen, text="Carregando...", font=("", 16))
        self.loading_label.place(relx=0.5, rely=0.4, anchor='center')

    def _create_progress_bar(self):
        self.progress_bar = CTkProgressBar(
            self.screen, mode='indeterminate', width=self.width - 50)
        self.progress_bar.place(relx=0.5, rely=0.5, anchor='center')
        self.progress_bar.start()

    def create_screen(self):
        self.screen = CTkToplevel(self.parent)
        self.screen.title(self.title)
        self.screen.geometry(f"{self.width}x{self.height}+{self.x}+{self.y}")
        self.screen.resizable(False, False)
        self.screen.transient(self.parent)
        self.screen.focus_set()
        self.screen.grab_set()

        self._create_progress_bar()
