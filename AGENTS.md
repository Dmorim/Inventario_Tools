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

## Responsabilidades e convenções (NEXO)

- **Testes do sistema:** passo a responsabilidade da criação, alteração e exclusão dos arquivos de testes do sistema ao agente **NEXO**. Não é necessário pedir autorização para criar, modificar ou apagar testes quando julgar adequado para manter a consistência do sistema.
- **Imports:** devem ser realizados **apenas no topo do arquivo**. Imports **externos** (biblioteca padrão / terceiros) devem vir **primeiro**, seguidos dos imports **internos** do projeto, com linha em branco entre os grupos quando houver ambos.

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

- **Gerar o executável** (PyInstaller, receita `Inv Tools 3.5.0.spec`):
  ```powershell
  .\.venv\Scripts\python.exe -m PyInstaller "Inv Tools 3.5.0.spec" --noconfirm --clean
  ```
  Resultado em `dist\Inv Tools 3.5.0\` (~162 MB: `exe` + `Bin\`). Conferir: **11** arquivos em
  `Bin\Recursos\Firebird`, **167** em `Bin\babel\locale-data` e nenhum `Bin\config.ini` (criado na
  1ª conexão). A receita antiga `Inv Tools 3.0.0.spec` (máquina `C:\Users\Sup-12\...`) foi removida.

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
Dashboard/         KPIs + gráfico de tendência (Dashboard_Screen/Func/Charts)
Data_Manager/      Período (PeriodoManager, PeriodoInventario)
Distorcao_Manager/ Correção de distorção (DistorcaoManager)
Interface_Tools/   Componentes de UI reutilizáveis (ToolTip, ProgressBar, ContainerManager)
Inv_Screen/        Tela principal (Top/Bot frames)
Outros/            Recursos auxiliares (imagens base64, cálculo de período, Logger, Version_Info.txt)
Queries/           SQL centralizado (Consulta_Queries, Comando_Queries, Create_Views)
Recursos/          Firebird (fbclient.dll e bibliotecas)
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
- **Capa de dados do Dashboard (desde 26/10/2026):** `tests/test_dashboard_func.py` (**36 casos**)
  cobre `_extrair_series`, `_previa_inventario`, `_calcular_kpis`, `carregar_kpis`,
  `carregar_dados_tendencia` e `_executar_consulta` (incluindo o `padrao_em_erro` do B2) com
  `monkeypatch` em `_executar_select`/`_executar_consulta`/`_previa_inventario`/`_calcular_kpis`/
  `query_executor` — **nenhum acesso ao Firebird**. Os helpers de UI
  `_periodo_anterior`/`_formatar_variacao` ficam em `tests/test_dashboard_screen_helpers.py`
  (**33 casos**); importar `Dashboard.Dashboard_Screen` **não** abre janela (só define funções).
  Ao mexer nessas funções, rode
  `pytest tests/test_dashboard_func.py tests/test_dashboard_screen_helpers.py`.
- **KPI "Previsão de Inventário" (B1 concluído em 27/10/2026):** é uma **estimativa do inventário
  no fim do período selecionado**, rolando a partir do **saldo corrente** (`hoje`) com base em
  movimentação a custo atual (`precu`), via `QUERY_MOVIMENTO_ESTOQUE_CUSTO`
  (`Dashboard/Dashboard_Func.py`): `fim < hoje` → `inv_corrente - movimento(fim+1 .. hoje)`;
  `fim >= hoje` → `inv_corrente + movimento(hoje+1 .. fim)`. `l.tpmov = 'S'` entra (compras,
  devoluções de venda, transferências de entrada); demais saem. Mesmo custo e mesmo universo de
  classificação de `QUERY_INVENTARIO`. A query antiga
  (`QUERY_DIFERENCA_ANO_ANTERIOR_ATUAL`) foi **removida**; histórico no git (`16e26ec`, `89d702a`,
  `e7d479f`).
  Validação no banco cópia: movimento histórico 4.156.492,44 × saldo 4.207.242,01 (diferença =
  estoque inicial de fev/2021). O card **não** exibe mais o selo "vs período anterior" (substituído
  pelo subtexto fixo "estimativa do período") e o período anterior é calculado com
  `_calcular_kpis(..., incluir_previa=False)`.
  **Falha visível (B2, 26/10/2026):** `_executar_consulta` aceita `padrao_em_erro` (default `0`);
  `_previa_inventario` usa `padrao_em_erro=None` e, se a consulta falhar, retorna `None` e
  `_calcular_kpis` grava `'Erro'` no card. Resultado `NULL` legítimo continua valendo `0`.
  **B1 (27/10/2026):** corrige a contagem dupla do modelo anterior (movimento já contido no saldo
  corrente). Implementado em `c7ad6a1` com testes atualizados em `tests/test_dashboard_func.py`.
- **Logging (convenção desde 26/10/2026):** use `get_logger(__name__)`
  (`Outros/Logger/Get_Logger.py`); nível por `INVENTARIO_LOG_LEVEL` (padrão `INFO`) e arquivos em
  `logs/AAAAMM/DDMMAAAA_log.txt`. Não deixe `except ...: pass` silencioso em código novo: registre
  `logger.debug('<o que falhou>', exc_info=True)` para limpezas de melhor esforço (UI/`destroy`) e
  `logger.exception(...)` para erros que o usuário precisa ver. No Dashboard (26/10/2026) foram
  convertidos 24 pontos em `Dashboard_Screen.py` e 10 em `Dashboard_Charts.py`. **Fase 3.3
  concluída em 28/10/2026:** varredura do app confirma **0 `except: pass`** — os pontos restantes
  foram convertidos ou tratados com `logger.debug`.
- **Dependências do gráfico (desde o commit `3d7d9ef`, 23/10/2026):** `Dashboard_Charts.py`
  importa `numpy` e `scipy` diretamente (`_curva_suave` usa `make_interp_spline` para
  suavizar o modo Linhas). Ambos estão declarados no `requirements.txt` desde 26/10/2026 —
  **antes disso o `scipy` não estava instalado na `.venv`**, o que quebrava o
  `import Dashboard.Dashboard_Charts` (tela do Dashboard) e a coleta do `pytest`.
  Ao criar ambiente novo, instale `requirements.txt` antes de rodar testes.
- **Robustez de ciclo de vida (commit `02afd20`, 23/10/2026):** `thread_execução`
  (`Thread_Manager/Thread_Executor.py`) tem flag de cancelamento e revalida o widget dentro do
  callback agendado; `GerenciadorThreadBD` recusa operações com `_fechando` ativo; o Dashboard
  protege abertura/fechamento (`_aplicar_grab_seguro`, `_fechar_dashboard_seguro`) e nunca deixa
  o botão travado. Coberto desde 23/10/2026 por `tests/test_thread_executor.py` (10 casos, com
  fake de Tk — sem display) e +7 casos em `tests/test_gerenciador_thread_bd.py`. Ao mexer nesses
  caminhos, rode `pytest tests/test_thread_executor.py tests/test_gerenciador_thread_bd.py`.
- **Regras de negócio do "universo de classificação" (decididas pelo usuário em 22/10/2026 —
  Item 9.7, que foi DESCARTADO em 23/10/2026 por já estar solucionado):** `in01pro.classificacao_produto`
  define quais produtos contam como estoque.
  (a) `QUERY_INVENTARIO` e `QUERY_DISTORCAO_SALDO` devem usar o **mesmo** universo —
  **aplicado pelo usuário em 26/10/2026**: ambas usam `'00'`–`'06'` (a distorção passou a incluir
  `'03'`);
  (b) `'07'` = **produto de uso e consumo** → **fora** de qualquer cálculo de inventário
  (e também `'08'`/`'10'`/`'99'`);
  (c) as queries de **entradas** deveriam excluir compras canceladas (`l.cance='S'`), como a
  distorção faz — **não aplicado**: `QUERY_ENTRADAS` e as queries de tendência seguem sem
  `COALESCE(l.cance, 'N') = 'N'`, porque o impacto medido nos 5 bancos cliente foi **0,00**.
  Detalhes em `AGENTS_SESSAO.md` Item 9.7 — o agente não alterou essas queries.
- `config.ini` está no `.gitignore` (config não deve ser versionado para não expor credenciais).
  **Atualização (22/10/2026):** o `config.ini` foi **desrastreado e commitado** pelo usuário
  (`git rm --cached config.ini` + commit `a503daa` — arquivo mantido localmente, agora
  respeitando o `.gitignore`).
  **Rotação da senha do banco CONCLUÍDA em 28/10/2026** — as credenciais antigas que restam no
  histórico do git estão invalidadas. Ver `AGENTS_SESSAO.md` Item 6.10.
- **Escopo encerrado por decisão do usuário (28/10/2026):**
  - **Type hints / `py.typed` (Fase 4)** — **descartados**. O projeto **não** adota type hints;
    não criar `py.typed` nem anotar funções novas por obrigação. Hints já existentes ficam como estão.
  - **Feature 2 (Validação Pré-Inventário)** — **descartada**; o diretório `Validacao/` **não**
    deve ser criado. `tests/test_validacao.py` é outra coisa (validações de entrada) e permanece.
  - **SQL livre (`com_ger`)** — a política atual (aviso de risco + confirmação, sem whitelist)
    é **definitiva**. Não propor sanitização/lista de permissão.
  - **`DROP VIEW`** de `V_LAN_COM`/`V_DIFF_ENTRADA_SAIDA_MES` — **concluído**.
- **`_hoje()` em `Dashboard/Dashboard_Func.py`:** a função `_previa_inventario` **deve** usar
  `hoje = _hoje()` (e não `date.today()` direto) — é o ponto de mock dos testes. Usar
  `date.today()` quebra `tests/test_dashboard_func.py::TestPreviaInventario` quando a data real
  não coincide com a data fixada nos testes.
- **`DistorcaoManager` não é mais singleton (desde `c7ad6a1`):** é criado em `Inventario.py` e
  **injetado por parâmetro** nas telas/comandos. `tests/test_distorcao.py` verifica instâncias
  independentes — não reintroduzir `_instancia`/singleton sem decisão explícita.
- **`docs/Plano_Refatoracao_Inventario_Tools_v2.md` é versionado** (não está no `.gitignore`, ao
  contrário do que este arquivo afirmava até 26/10/2026) — alterações nele aparecem no
  `git status` como modificação normal.
- Não commitar credenciais reais em nenhum arquivo.
