# AGENTS.md — Guia para agentes trabalhando no projeto

> **Sessão de refatoração de datas:** leia também `AGENTS_SESSAO.md` (agente **NEXO**) —
> instruções de sessão: **nunca commitar**, apresentar plano + prévia de código e aguardar
> confirmação antes de qualquer alteração, estado atual do roadmap de datas e cuidados de ambiente.

## Visão geral

Ferramenta desktop em Python/Tkinter (customtkinter) para auxiliar técnicos de inventário.
Conecta-se a bancos Firebird (fdb) e executa consultas e comandos de correção de dados.

Arquivo principal (entry point): `Inventario.py` (classe `Inventario`).

Convenção de código: cada funcionalidade é dividida em pares **Screen + Func**.
- `*_Screen.py` — interface (Tkinter/customtkinter)
- `*_Func.py` — lógica e queries

Todo acesso ao banco passa por `Thread_Manager.Query_Operations` (`query_selector`,
`query_updater`, `query_executor`) e por `thread_execução()` (`Thread_Manager.Thread_Executor`),
que executa em thread e usa callbacks para atualizar a UI na thread principal.

## Comandos

Ambiente virtual: `.venv` (Windows, PowerShell). Use o executável da venv explicitamente:

- **Rodar o programa** (a partir da raiz do projeto):
  ```powershell
  .\.venv\Scripts\python.exe Inventario.py
  ```

- **Rodar os testes** (pytest):
  ```powershell
  .\.venv\Scripts\python.exe -m pytest tests -v
  ```

- **Verificação básica de sintaxe** (não há linter/typecheck configurado):
  ```powershell
  .\.venv\Scripts\python.exe -m compileall -q . -x "\.venv"
  ```

- **Instalar dependências**:
  ```powershell
  .\.venv\Scripts\python.exe -m pip install -r requirements.txt
  # dev (pytest):
  .\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
  ```

## Estrutura de pastas

```
Banco_de_Dados/    Conexão (ConfiguracaoBanco, BancoDeDados) + tela de conexão
Comandos/          Comandos de correção no BD (Comandos_Gerais, Distorcao_Saldo)
Configuracoes/     Configurações do sistema (tema)
Consultas/         Consultas (11 tipos + hub), Generics_Functions, Consultas_Val_Screen
Interface_Tools/   Componentes de UI reutilizáveis (ToolTip, ProgressBar, ContainerManager)
Inv_Screen/        Tela principal (Top/Bot frames)
Outros/            Recursos auxiliares (imagens base64, cálculo de período)
Thread_Manager/    Concorrência e pool de conexões
Tutorial/          Tutorial interativo
tests/             Testes unitários (pytest)
```

## Notas importantes

- Os testes atualmente cobrem funções **puras**, sem interface (formatação de valores,
  validação de entrada). Evite que testes importem telas que dependem de display.
  **Exceção (22/10/2026):** o gráfico do Dashboard é testado por **render Agg**
  (`matplotlib.use('Agg')` + `Figure` + `FigureCanvasAgg` em `tests/test_dashboard_charts.py`)
  — mede caixas de texto, corte nas bordas e sobreposição **sem** abrir display.
  Para isso, o desenho das séries foi extraído para `_desenhar_series()`
  (`Dashboard/Dashboard_Charts.py`), que **não** depende de Tk.
  Atenção: **decisão do usuário (22/10/2026): as vendas vão para CIMA, com valor
  positivo** — o desenho usa os valores como chegam (sem negação). A fonte dos
  rótulos de valor é adaptada à densidade (`_fonte_rotulos_valor`): com as três
  séries no mesmo hemisfério, rótulos de meses vizinhos podem se encostar.
- **Robustez de ciclo de vida (commit `02afd20`, 23/10/2026):** `thread_execução`
  (`Thread_Manager/Thread_Executor.py`) tem flag de cancelamento e revalida o widget dentro do
  callback agendado; `GerenciadorThreadBD` recusa operações com `_fechando` ativo; o Dashboard
  protege abertura/fechamento (`_aplicar_grab_seguro`, `_fechar_dashboard_seguro`) e nunca deixa
  o botão travado. Coberto desde 23/10/2026 por `tests/test_thread_executor.py` (10 casos, com
  fake de Tk — sem display) e +7 casos em `tests/test_gerenciador_thread_bd.py`. Ao mexer nesses
  caminhos, rode `pytest tests/test_thread_executor.py tests/test_gerenciador_thread_bd.py`.
- **Regras de negócio do "universo de classificação" (decididas pelo usuário em 22/10/2026 —
  Item 9.7):** `in01pro.classificacao_produto` define quais produtos contam como estoque.
  (a) `QUERY_INVENTARIO` e `QUERY_DISTORCAO_SALDO` devem usar o **mesmo** universo;
  (b) `'07'` = **produto de uso e consumo** → **fora** de qualquer cálculo de inventário
  (e também `'08'`/`'10'`/`'99'`); (c) as queries de **entradas** devem excluir compras
  canceladas (`l.cance='S'`), como a distorção já faz. A aplicação ainda está **pendente**
  (diff pronto em `AGENTS_SESSAO.md` Item 9.7).
- `Config.ini` e `docs/Plano_Refatoracao_Inventario_Tools_v2.md` estão no `.gitignore`
  (config não deve ser versionado para não expor credenciais).
  **Atualização (22/10/2026):** o `config.ini` foi **desrastreado e commitado** pelo usuário
  (`git rm --cached config.ini` + commit `a503daa` — arquivo mantido localmente, agora
  respeitando o `.gitignore`).
  **Continua pendente a rotação da senha do banco**, pois as credenciais antigas seguem no
  histórico do repositório. Ver `AGENTS_SESSAO.md` Item 6.10.
- Não commitar credenciais reais em nenhum arquivo.
