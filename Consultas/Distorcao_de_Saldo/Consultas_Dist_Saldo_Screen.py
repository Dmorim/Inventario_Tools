def dist_saldo_screen(self, Consulta_Screen, consulta_button):
    def centraliza_tela():
        # Calcula a posição central da tela para o progress bar
        screen_width = Consulta_Screen.winfo_screenwidth()
        screen_height = Consulta_Screen.winfo_screenheight()
        progress_x = (screen_width // 2) - (Consulta_Screen.winfo_width() // 2)
        progress_y = (screen_height // 2) - \
            (Consulta_Screen.winfo_height() // 2)
        return progress_x, progress_y

    import customtkinter as ctk

    # Importa as funções que vão ser usadas na tela dos arquivos Consultas/Consultas_Val_Screen, Consutlas/Gen_Funcs_Consulta e Consultas/Consultas_Dist_Saldo_List
    from Consultas.Consultas_Val_Screen import Consultas_Val_Screen
    from Consultas.Generics_Functions.Gen_Funcs_Consulta import copy_val
    from Consultas.Distorcao_de_Saldo.Consultas_Dist_Saldo_List import List_Treeview_Screen
    from Thread_Manager.Thread_Executor import thread_execução
    from Interface_Tools.Tk_Progress_Bar import ProgressBarHandler

    # Desabilita o botão de consulta para evitar múltiplas execuções simultâneas
    consulta_button.configure(state='disabled')
    progress_x, progress_y = centraliza_tela()

    hub = Consultas_Val_Screen(
        Consulta_Screen, 'Saldo de Estoque', consulta_button)
    progress_bar = ProgressBarHandler(
        hub, "Aguarde", x=progress_x, y=progress_y)

    # Cria os labels e botões da tela
    val_ven_label = ctk.CTkLabel(
        hub, text='Distorções de Saldo:', width=20, height=2, font=('', 16))
    val_ven_text = ctk.CTkLabel(
        hub, text='', width=20, height=2, font=('', 14))

    # Diferente de outras consultas, aqui tanto a query quanto a função que vai tratar os valores da consulta estão no mesmo arquivo
    # Função que executa a query e trata os valores obtidos

    val_ven_button = ctk.CTkButton(
        hub, text='Copiar Valor', width=15, height=20, command=lambda: copy_val(val_ven_text), state='disabled')
    listagem_button = ctk.CTkButton(hub, text='Listar Produtos', width=15,
                                    height=20, command=lambda: List_Treeview_Screen(self, hub), state='disabled')

    # Posiciona os labels e botões na tela
    val_ven_label.place(relx=0.5, y=15, anchor='center')
    val_ven_text.place(relx=0.5, y=40, anchor='center')
    val_ven_button.place(relx=0.8, y=65, anchor='center')
    listagem_button.place(relx=0.24, y=65, anchor='center')

    progress_bar.create_screen()
    progress_bar.atualizar_status("Consultando distorções de saldo...")

    def on_query_complete(empty):
        progress_bar.finalizar()
        val_ven_text.configure(text=len(self.dist_saldo_list))
        val_ven_button.configure(state='normal')
        listagem_button.configure(state='normal')

    def on_query_error(error):
        progress_bar.finalizar()
        val_ven_text.configure(text="Erro ao gerar consulta")
        print(f"Erro ao executar consulta: {error}")

    def execute_query(self):
        from Thread_Manager.Query_Operations import query_selector, query_executor

        query = """
            EXECUTE BLOCK
            RETURNS (
                cdpro VARCHAR(50),
                nmpro VARCHAR(255),
                saldo_lan NUMERIC(15,4),
                saldo_pro NUMERIC(15,4),
                distorcao CHAR(1)
            )
            AS
            DECLARE VARIABLE formatosaldo INTEGER;
            BEGIN

                SELECT CAST(
                        CHAR_LENGTH(
                            SUBSTRING(valor FROM POSITION('.' IN valor) + 1)
                        ) AS INTEGER
                    )
                FROM si01gp
                WHERE ident = 'FORMATOSALDO'
                INTO :formatosaldo;

                FOR
                    SELECT
                        p.cdpro,
                        p.nmpro,
                        SUM(IIF(l.tpmov = 'S', l.quant, -l.quant)) AS saldo_lan,
                        p.saldo AS saldo_pro,
                        IIF(
                            ROUND(SUM(IIF(l.tpmov = 'S', l.quant, -l.quant)), :formatosaldo) <>
                            ROUND(p.saldo, :formatosaldo),
                            'S',
                            'N'
                        ) AS distorcao
                    FROM in01lan l
                    LEFT JOIN in01pro p
                        ON l.cdpro = p.cdpro
                    LEFT JOIN in01com c
                        ON c.notfi = l.notfi
                    AND c.cdfrn = l.cdfrn
                    AND c.serie = l.serie
                    WHERE
                        COALESCE(l.controlaestoque, 'S') = 'S'
                        AND COALESCE(l.cance, 'N') = 'N'
                        AND classificacao_produto IN ('00', '01', '02', '04', '05', '06')
                        AND l.venda <> 'R'
                        AND (COALESCE(c.alterarsaldo, 'S') = 'S' OR l.venda <> 'J')
                    GROUP BY
                        p.cdpro,
                        p.nmpro,
                        p.saldo
                    INTO
                        :cdpro,
                        :nmpro,
                        :saldo_lan,
                        :saldo_pro,
                        :distorcao
                DO
                    SUSPEND;
            END
        """

        rows = query_executor(query_selector, query)

        self.dist_saldo_list = [
            [cdpro, nmpro, saldo_lan, saldo_pro]
            for cdpro, nmpro, saldo_lan, saldo_pro, distorcao in rows
            if distorcao == 'S'
        ]

    thread_execução(hub, execute_query, on_query_complete,
                    on_query_error, self)
