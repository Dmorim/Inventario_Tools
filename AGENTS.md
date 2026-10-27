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
Outros/            Recursos auxiliares (imagens base64, cálculo de período, Logger)
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
- **Capa de dados do Dashboard (desde 26/10/2026):** `tests/test_dashboard_func.py` (33 casos)
  cobre `_extrair_series`, `_previa_inventario`, `_calcular_kpis`, `carregar_kpis`,
  `carregar_dados_tendencia` e `_executar_consulta` (incluindo o `padrao_em_erro` do B2) com
  `monkeypatch` em `_executar_select`/`_executar_consulta`/`_previa_inventario`/`_calcular_kpis`/
  `query_executor` — **nenhum acesso ao Firebird**. Os helpers de UI
  `_periodo_anterior`/`_formatar_variacao` ficam em `tests/test_dashboard_screen_helpers.py`
  (17 casos); importar `Dashboard.Dashboard_Screen` **não** abre janela (só define funções).
  Ao mexer nessas funções, rode
  `pytest tests/test_dashboard_func.py tests/test_dashboard_screen_helpers.py`.
- **KPI "Previsão de Inventário" (redefinido em 26/10/2026):** é uma **estimativa do inventário
  no fim do período selecionado**, não mais um comparativo entre anos-calendário. Fórmula:
  `inventário_base + movimento líquido do período a custo atual`, via
  `QUERY_MOVIMENTO_ESTOQUE_CUSTO` (`Dashboard/Dashboard_Func.py`), que soma `quant × precu` com
  sinal por `l.tpmov` (`'S'` entra: compras, devoluções de venda, transferências de entrada; as
  demais saem: vendas, devoluções ao fornecedor, ajustes), usando o **mesmo custo e o mesmo
  universo de classificação** de `QUERY_INVENTARIO`. **Premissa explícita do usuário:** a base do
  cliente tem o valor de inventário **normalizado para o ano base do inventário** — o snapshot é
  tratado como o inventário na data **inicial** do período. A query antiga
  (`QUERY_DIFERENCA_ANO_ANTERIOR_ATUAL`, `SUM(ABS(...))` por ano, com `in01com.valno` ×
  `V_FAT_VALOR_SAIDA`) foi **removida**; histórico no git (`16e26ec`, `89d702a`, `e7d479f`).
  Validação no banco cópia: movimento histórico 4.156.492,44 × saldo 4.207.242,01 (diferença =
  estoque inicial de fev/2021). O card **não** exibe mais o selo "vs período anterior" (substituído
  pelo subtexto fixo "estimativa do período") e o período anterior é calculado com
  `_calcular_kpis(..., incluir_previa=False)`.
  **Falha visível (B2, 26/10/2026):** `_executar_consulta` aceita `padrao_em_erro` (default `0`);
  `_previa_inventario` usa `None` e, se a consulta falhar, `_calcular_kpis` grava `'Erro'` no card
  em vez de repetir o inventário. Resultado `NULL` legítimo continua valendo `0`.
  **Premissa contestada (26/10/2026):** medição mostrou que `in01pro.saldo` nesta base é o **saldo
  corrente**, não um valor normalizado para o ano-base; o modelo atual conta o movimento duas vezes
  e erra −21,1% (2024), −8,7% (2025) e −7,7% (2026 jan–set). A correção (rolar o saldo a partir de
  `hoje`) está no **Item 10.2** de `AGENTS_SESSAO.md`, para sessão dedicada — **não aplicar sem
  reescrever `TestPreviaInventario`**.
- **Logging (convenção desde 26/10/2026):** use `get_logger(__name__)`
  (`Outros/Logger/Get_Logger.py`); nível por `INVENTARIO_LOG_LEVEL` (padrão `INFO`) e arquivos em
  `logs/AAAAMM/DDMMAAAA_log.txt`. Não deixe `except ...: pass` silencioso em código novo: registre
  `logger.debug('<o que falhou>', exc_info=True)` para limpezas de melhor esforço (UI/`destroy`) e
  `logger.exception(...)` para erros que o usuário precisa ver. No Dashboard (26/10/2026) foram
  convertidos 24 pontos em `Dashboard_Screen.py` e 10 em `Dashboard_Charts.py`; ainda restam 17
  `except: pass` em outros módulos (ver `docs/Plano_Refatoracao_Inventario_Tools_v2.md` §3.3).
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
  **Continua pendente a rotação da senha do banco**, pois as credenciais antigas seguem no
  histórico do repositório. Ver `AGENTS_SESSAO.md` Item 6.10.
- **`docs/Plano_Refatoracao_Inventario_Tools_v2.md` é versionado** (não está no `.gitignore`, ao
  contrário do que este arquivo afirmava até 26/10/2026) — alterações nele aparecem no
  `git status` como modificação normal.
- Não commitar credenciais reais em nenhum arquivo.
