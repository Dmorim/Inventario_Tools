# Plano de Refatoração — Inventario_Tools

**Versão do sistema:** 2.0.0 (em evolução)
**Autor:** Daniel Amorim (com colaboração de Cícero Romão nas consultas SQL)
**Licença:** CC0 1.0 Universal (domínio público)
**Documento atualizado em:** 28/10/2026
**Versão do documento:** 5.5 (atualizado — reflete o estado atual do código na branch
`refatoracao_v3.5`, HEAD `caf23b7`: Dashboard completo com KPI comparativo, curvas suavizadas,
toolbar, tooltip e cópia do valor do KPI por clique; KPI "Previsão de Inventário" rolado a partir
do saldo corrente (B1, `c7ad6a1`); pool endurecido; **212 testes** passando em 15 arquivos.
**Escopo encerrado por decisão do usuário (28/10/2026):** Fase 4 (type hints/`py.typed`) e
Feature 2 (Validação Pré-Inventário) **descartadas**; política atual de `com_ger` (SQL livre)
**definitiva**; Fase 3.3 concluída; `DROP VIEW` das órfãs e rotação da senha do banco **concluídos**)

> Este documento atualiza o plano original (`Plano_Refatoracao_Inventario_Tools.pdf`) e as revisões
> 1.x/2.0/3.0. Ele incorpora as **modificações já feitas no projeto** (branch `QoL` integrada ao
> `main`, e branch de trabalho `refatoracao_v3.5`) e lista **apenas o trabalho que ainda falta**,
> focado no estado real do código em 26/10/2026.

---

## Sumário

1. Análise do Projeto (estado atual)
2. Modificações já realizadas
3. Trabalho Restante (Fases)
4. Novos Problemas Identificados (N1–N9) — status
5. Erros/Dívidas adicionais encontrados na análise
6. Novas Features
7. Roadmap de Execução
8. Dependências Novas

---

## 1. Análise do Projeto (estado atual)

### 1.1 Visão Geral

O Inventario_Tools é uma ferramenta desktop em Python (customtkinter) para auxiliar técnicos de
inventário. Conecta-se a bancos Firebird (fdb) e executa consultas de valores/problemas e comandos
de correção de dados no banco.

A refatoração estrutural avançou substancialmente desde o documento v3.0. A camada de queries foi
**centralizada** em um package `Queries/`, a parametrização contra SQL injection foi aplicada na
maioria das consultas, a configuração foi centralizada em `Config_Manager` (classe `AppConfig`),
funções duplicadas de valor/lista foram unificadas, bugs N1/N2 foram corrigidos e a suíte de testes
começou a ser estabelecida. O restante deste plano concentra-se no que **ainda** precisa ser feito.

### 1.2 Funcionalidades Principais

- Conexão com bancos de dados Firebird remotos/locais
- Consultas de valores (Inventário, Vendas, Compras) e problemas de produtos
- Comandos de correção em massa no banco
- Correção de distorção de saldo entre IN01LAN e IN01PRO
- Seleção de período (Anual / Mensal / Personalizado)
- Tutorial interativo e configuração de tema (Claro/Escuro/Sistema)
- Cópia de valores para a área de transferência

### 1.3 Estrutura de Pastas (atual)

```
Inventario_Tools/
+-- Inventario.py                  # Arquivo principal (entry point)
+-- config.ini                     # Arquivo de configuração
+-- Queries/                       # NOVO — SQL centralizado
|   +-- Consulta_Queries.py        # 20 consultas (SELECT)
|   +-- Comando_Queries.py         # 14 comandos (UPDATE/INSERT)
+-- Banco_de_Dados/                # Camada de banco de dados
|   +-- Conexao_Banco_Dados/       # ConfiguracaoBanco, Inventario_Conn (pool)
|   +-- Tela_Banco_Dados/          # Tela de configuração de conexão + funcs
+-- Comandos/                      # Comandos de correção no BD
|   +-- Comandos_Gerais/           # Tela e lógica dos comandos
|   +-- Distorcao_Saldo/           # Correção de distorção de saldo
+-- Configuracoes/                 # Configurações do sistema (tema)
|   +-- Config_Manager.py          # NOVO — classe AppConfig (leitura/escrita)
+-- Dashboard/                     # NOVO — KPIs e gráfico de tendência
|   +-- Dashboard_Screen.py        # Janela, filtros e cards de KPI
|   +-- Dashboard_Func.py          # KPIs e séries de tendência (queries)
|   +-- Dashboard_Charts.py        # Gráfico (matplotlib) + toolbar + tooltip
+-- Data_Manager/                  # Período (PeriodoManager, PeriodoInventario)
+-- Distorcao_Manager/             # Correção de distorção (DistorcaoManager)
+-- Consultas/                     # Consultas (11 tipos + hub)
|   +-- Generics_Functions/        # Gen_Funcs_Consulta, Distorcao_de_Saldo
|   +-- Consultas_Screen.py        # Hub com os botões de consulta
|   +-- Consultas_Val_Screen.py    # Container base (Toplevel) das consultas
|   +-- <cada consulta>/           # *_Screen.py, *_List.py, *_Func.py
+-- Interface_Tools/               # Componentes reutilizáveis de UI
|   +-- Tk_Tooltip.py
|   +-- Tk_Progress_Bar.py
|   +-- Tk_Status_Animator.py      # NOVO — TextAnimator (animação de status unificada)
|   +-- Container_Screen_Managment/# Gerenciamento de Toplevels (ContainerManager)
|   +-- Consulta_Screen/           # NOVO — factory criar_tela_consulta (Screen+Func)
|   +-- Treeview_Table/            # NOVO — factory criar_tela_listagem
+-- Inv_Screen/                    # Tela principal (frames)
|   +-- Inv_Top_Frame.py
|   +-- Inv_Bot_Frame.py
+-- Outros/                        # Recursos auxiliares
|   +-- Banco_Images.py            # Imagens embutidas (base64)
|   +-- Periodo_Inventario.py      # Cálculo/formatação de período (datas)
|   +-- Logger/Get_Logger.py       # NOVO — logger central (get_logger)
+-- Thread_Manager/                # Concorrência e pool de BD
|   +-- Gerenciador_Thread_BD.py   # Pool de conexões Firebird
|   +-- Query_Operations.py        # query_selector / query_updater / query_executor
|   +-- Thread_Executor.py         # thread_execução
+-- Tutorial/                      # Tutorial interativo
+-- tests/                         # Testes unitários (pytest)
```

### 1.4 Arquitetura do Código

Convenção **Screen + Func**: cada funcionalidade possui `*_Screen.py` (interface) e `*_Func.py`
(lógica/queries). Toda interação com o banco passa por `Query_Operations` (`query_selector`,
`query_updater`, `query_executor` — todos com suporte a `params`) e por
`thread_execução()` (`Thread_Executor`), que executa em thread e usa callbacks para atualizar a UI.
Desde o commit `fc40fdd`, o `Thread_Executor` roteia toda atualização de UI para a main thread via
`_safe_schedule_ui` / `atualizar_ui_main`, com guardas de widget destruído (`winfo_exists` /
`TclError`), e as funções de consulta **não chamam mais `messagebox`** — propagam `DatabaseError`,
tratado na camada de tela via callbacks agendados. A animação de status é consolidada em
`TextAnimator` (commit `584cf56`). As telas de consulta e de listagem usam factories compartilhadas
(`Consulta_Screen.py`, `Treeview_Table/Listagem_Treeview.py`), eliminando grande parte do
boilerplate que antes era duplicado. O logging é central desde `Outros/Logger/Get_Logger.py`
(`get_logger`, nível por `INVENTARIO_LOG_LEVEL`, padrão `INFO`; arquivos em
`logs/AAAAMM/DDMMAAAA_log.txt`); desde 26/10/2026 os `except` de UI do Dashboard registram em
`logger.debug(..., exc_info=True)` (visível só com `INVENTARIO_LOG_LEVEL=DEBUG`).

---

## 2. Modificações Já Realizadas

Todas as mudanças abaixo já estão no código (a maioria na branch `refatoracao_v3.5`, já commitada).
**Não precisam mais ser feitas.**

| Mudança | Item do plano v3.0 | Status |
|---|---|---|
| SQL centralizado em `Queries/Consulta_Queries.py` e `Queries/Comando_Queries.py` | Fase 3.2 | ✅ Feito |
| `Query_Operations` com suporte a `params` | Fase 1.1 | ✅ Feito |
| Parametrização de datas/CFOP/porcentagem em consultas e comandos | Fase 1.1 | ✅ Feito |
| `Config_Manager.py` (classe `AppConfig`) com leitura única, RLock, save atômico UTF-8 | Fase 1.3 | ✅ Feito |
| `banco_codigo_valueform` unificado em `Gen_Funcs_Consulta.py` | Fase 2.1 | ✅ Feito |
| `copy_val` unificado em `Gen_Funcs_Consulta.py` | Fase 2.2 | ✅ Feito |
| Factory `criar_tela_listagem` (Treeview) — elimina 7×`Treeview_Select`/8×`Treeview_Insert` | Fase 2.3 | ✅ Feito |
| Factory `criar_tela_consulta` (Container base compartilhado) | Fase 2.4 | ✅ Feito |
| **N1** queries sempre falsas corrigidas (`VLDIA {op} PRECU` / `CUSME {op} PRECU`) | N1 | ✅ Feito |
| **N2** UnboundLocalError em `ven_get` e `ent_get` (retorno no `except`) | N2 | ✅ Feito |
| **N6** config.ini com encoding UTF-8 e sem seções duplicadas | N6 | ✅ Feito |
| **N8** imports/comentários órfãos limpos nos arquivos Valor_* | N8 | ✅ Feito |
| `except:` genérico endurecido para `except DatabaseError` em `Val_Inv_Func.py` | Fase 3.3 | ✅ Feito |
| `print()` de debug removidos (zero `print` no código) | Fase 3.4 | ✅ Feito |
| Botão "Copiar Valor" desabilitado durante consulta (via factory) | N7 | ✅ Feito |
| `obter_caminho_curto_banco_dados` agora `raise RuntimeError` no `except` | Fase 3.3 | ✅ Feito (ver §5.1) |
| Estrutura `tests/` + `conftest.py` + 14 testes passando | Fase 0/5.1 | ✅ Feito |
| `_montar_operacoes()`/`comandos_true()` extraídos e testados (`Comandos_Func.py`) | Fase 5.2 | ✅ Feito |
| Testes de `copy_val()` (mock pyperclip) e `calcular_periodo()`/`formatar_banco()` | Fase 5.2 | ✅ Feito |
| `TextAnimator` (`Tk_Status_Animator.py`) consolidando animação de status | N9/§5.7 | ✅ Feito |
| `Thread_Executor` — `_safe_schedule_ui`/`atualizar_ui_main` com guarda de widget destruído | N3/§5.3 | ✅ Feito |
| `messagebox` removido das funcs de consulta — agora propagam `DatabaseError` | N3/§5.3 | ✅ Feito |
| Porcentagem/decimal **descritos por vírgula** como input; `|d2|` → arredondamento | Fase 1.1 | ✅ Feito |
| `ConfiguracaoBanco.port` tipado como `int \| None` e validado por `isdigit()` | N5/§5.5 | ✅ Feito |
| `propri` vazio tratado — evita `IndexError` | N5/§5.5 | ✅ Feito |
| Race double-destroy reduzida — callbacks de finalização agendados na main thread | N5/§5.5 | ✅ Feito |
| `cor_do_tema` padronizado em minúsculas (set e get) | §5.2 | ✅ Feito |
| `Tk_Tooltip` — valida `bbox("insert")` None antes de desempacotar | N7/§5.6 | ✅ Feito |
| `Consultas_Val_Screen` — `posicionar_container` sem re-lançar `RuntimeError` | N7/§5.6 | ✅ Feito |
| `help_base64_image` sem vírgula inválida (`Banco_Images.py`) | N7/§5.6 | ✅ Feito |
| `Listagem_Treeview` — `grab_set()` + `WM_DELETE_WINDOW` (via `toplevel.protocol`) | N7/§5.6 | ✅ Feito |
| `executa_comandos` — feedback de status via `atualizar_ui_main` (sem `after()` na thread) | N3/§5.3 | ✅ Feito |
| Suíte ampliada para **212 testes** em 15 arquivos (`pytest` → 212 passed; baseline anterior em `caf23b7` era 208 passed + 4 falhas de teste, corrigidas em 28/10/2026) | Fase 5 | ✅ Feito |
| **Feature 1 — Dashboard** (`Dashboard/`): KPIs + KPI comparativo, gráfico de tendência (Barras/Linhas × Mês/Ano), toolbar, tooltip, cópia do KPI por clique e persistência de filtros | Feature 1 | ✅ Feito |
| **Logging** nos `except` de UI do Dashboard (24 em `Dashboard_Screen.py`, 10 em `Dashboard_Charts.py`) e remoção do cálculo morto do tooltip | Fase 3.3 / §5.8 | ✅ Feito (26/10/2026) |
| **Fase 3.3 remanescente** — `except: pass` silenciosos fora do Dashboard | Fase 3.3 | ✅ Feito (28/10/2026 — varredura: **0** `except: pass` no app) |
| **`DROP VIEW`** de `V_LAN_COM` e `V_DIFF_ENTRADA_SAIDA_MES` nas bases cliente | §5.8 | ✅ Concluído (28/10/2026 — operação no banco, fora do código) |
| **Rotação da senha do banco** (credenciais antigas no histórico do git) | Item 6.10 | ✅ Concluído (28/10/2026 — operação de infraestrutura) |

> **Nota sobre branches:** As modificações de UI foram consolidadas no `main` via PR #14
> (merge `48e7fe3`). A refatoração estrutural é conduzida na branch `refatoracao_v3.5`, hoje
> sincronizada com `origin/refatoracao_v3.5` no HEAD `228787b` (o commit `fc40fdd`, citado nas
> revisões anteriores, já foi enviado).

---

## 3. Trabalho Restante (Fases)

> As fases abaixo são o refinamento do plano v3.0, mantendo apenas os itens **ainda pendentes**.
> Onde havia ambiguidade, foi registrada a decisão de projeto atual.

### Fase 1 — Segurança e Configuração (restante)

#### 1.2 Mover credenciais para config — ✅ CONCLUÍDO

Status atual: implementado. As credenciais são lidas de `[Credenciais]` via `AppConfig`
(`user_db`/`pass_db` com padrão SYSDBA/masterkey), validadas por `validar_credenciais()`;
`config.ini` segue no `.gitignore`. **Nunca commitar credenciais reais.**

#### 1.1 (remanescente) — SQL livre `com_ger` — ✅ DEFINITIVO (mantido)

`Comandos_Func.py:37` executa `QUERY_COMANDO_GERAL.format(comando=self.com_ger)` com SQL digitado
pelo usuário, sem sanitização (apenas aviso + confirmação). **Decisão do usuário em 28/10/2026: a
política atual é a definitiva** — o SQL livre fica sob total responsabilidade do operador, com
aviso de risco + confirmação explícita. **Não** haverá whitelist, lista de permissão nem bloqueio
programático de comandos destrutivos.

#### 1.4 Corrigir inconsistência de `com_ger` ser executado em thread (ver N3)

Resolvido em `fc40fdd` + correções desta revisão: o SQL livre continua sendo executado via
`query_executor(query_updater, ...)` na thread, mas todo o feedback de UI (status, progresso, erros)
é roteado para a main thread via `atualizar_ui_main` / callbacks agendados. ✅

---

### Fase 3 — Arquitetura e Organização (restante)

#### 3.1 Mover imports para o topo dos módulos — ✅ CONCLUÍDO

Verificado em 26/10/2026: **não há imports lazy** nos módulos da aplicação (nenhum `import`/`from`
dentro de função fora de `tests/`). As telas que antes importavam `customtkinter`/`messagebox`
dentro de funções (`Banco_de_Dados_Screen.py`, `Comandos_Screen.py`, `Config_Screen.py`,
`Consultas_Screen.py`, `Tutorial_Screen.py`, `Comandos_Func.py`,
`Consultas_Dist_Saldo_Screen.py`) já têm os imports no topo; não foi necessário injetar
dependências para quebrar circulares.

#### 3.3 (remanescente) — robustez de erros — ✅ CONCLUÍDO

- ✅ `Inventario_Conn.py` — porta agora `int | None`, validada por `isdigit()` antes de usar.
- ✅ `logging` no tratamento de erros: o **Dashboard** foi concluído em 26/10/2026
  (`Dashboard_Screen.py`: 24 pontos; `Dashboard_Charts.py`: 10 pontos) — todos os `except` de UI
  registram `logger.debug(..., exc_info=True)`, visível apenas com `INVENTARIO_LOG_LEVEL=DEBUG`.
- ✅ **Remanescentes concluídos em 28/10/2026:** a varredura do app (excluindo `tests/`) encontrou
  **0 `except: pass`** — os pontos antes listados (`Comandos_Func.py`, `Banco_de_Dados_Func.py`,
  `Consultas_Val_Screen.py`, `Consultas_Val_Inv_Screen.py`, `Tk_Progress_Bar.py`,
  `Tk_Status_Animator.py`, `Gerenciador_Thread_BD.py`, `Thread_Executor.py`) já estão convertidos
  ou tratados com `logger.debug`. Nada pendente nesta fase.

---

### Fase 4 — Type Hints e Assinaturas — ❌ DESCARTADA (decisão do usuário, 28/10/2026)

O projeto **não adotará type hints**. Os itens 4.1 (anotações de retorno/parâmetros) e 4.2
(`py.typed`) estão **fora de escopo** e **não serão executados**. O `py.typed` **não existe** na
raiz e **não deve ser criado**. Os hints já presentes em módulos isolados (`Config_Manager`,
`DistorcaoManager`, `Get_Logger`, `PeriodoInventario`, `PeriodoManager`, etc.) permanecem como
estão — não há trabalho de remoção nem de expansão.

---

### Fase 5 — Testes Unitários (restante)

#### 5.2 Testar funções puras — ✅ COMPLETO (212 testes na suíte, 15 arquivos)

Principais grupos (a suíte completa está detalhada em `docs/Status_Refatoracao.md`, Fase 5):

| Função | Arquivo | Status |
|---|---|---|
| `banco_codigo_valueform()` | Gen_Funcs_Consulta.py | ✅ coberto |
| `precu_porcent_entry_validate()` | Comandos_Func.py | ✅ coberto |
| `copy_val()` (mock pyperclip) | Gen_Funcs_Consulta.py | ✅ coberto (`test_copy_val.py`, 4) |
| `calcular_periodo()` / `formatar_banco()` / `periodo_padrao()` / `periodo_tendencia_ultimos_5_anos()` | Outros/Periodo_Inventario.py | ✅ coberto (`test_periodo.py`, 16) |
| `_montar_operacoes()` / `comandos_true()` | Comandos_Func.py | ✅ coberto (`test_comandos_func.py`, 12) |
| `query_updater` / `_safe_schedule_ui` / validações UI | Thread_Manager / Configuracoes | ✅ coberto (`test_query_operations.py` 12, `test_validacao.py` 10) |
| `PeriodoManager` | Data_Manager/PeriodoManager.py | ✅ coberto (`test_periodo_manager.py`, 16) |
| `_extrair_series()` / `_previa_inventario()` / `_calcular_kpis()` / `carregar_kpis()` / `carregar_dados_tendencia()` | Dashboard/Dashboard_Func.py | ✅ coberto (`test_dashboard_func.py`, 36 — banco mockado) |
| `_periodo_anterior()` / `_formatar_variacao()` | Dashboard/Dashboard_Screen.py | ✅ coberto (`test_dashboard_screen_helpers.py`, 33) |
| `_desenhar_series()` (render Agg, sem display) | Dashboard/Dashboard_Charts.py | ✅ coberto (`test_dashboard_charts.py`, 31) |

#### 5.3 Testar queries isoladamente — ✅ COMPLETO

As fixtures `FakeCursor`/`FakeConexao` já existem em `tests/conftest.py`; `test_query_operations.py`
cobre `query_selector`/`query_updater` isolados. `tests/test_queries.py` (3 casos) valida o
**contrato nominal** das **20 consultas** e **14 comandos** centralizados em `Queries/` (nomes
públicos exatos + conteúdo não vazio) e garante que `EXPR_VALOR_ENTRADA` é a mesma expressão em
`QUERY_ENTRADAS` e nas duas queries de tendência do Dashboard.

---

### Fase 6 — Compatibilidade com PyInstaller — 🔄 EM ANDAMENTO (receita existe, não validada)

O repositório **agora tem receitas**: `Inv Tools 3.0.0.spec` e `Inventario_3.5.0.spec` na raiz.
**Nenhuma delas foi validada** (não existe `build/` nem `dist/`; o `.gitignore` ignora `*.spec`,
`build/`, `dist/` e `*.exe`, então as receitas não estão versionadas). O antigo
`Outros/Auto_py_to_exe config.json` continua **obsoleto**:

- caminhos absolutos da máquina antiga (`C:/Users/Sup-12/...`);
- não inclui os pacotes novos (`Dashboard/`, `Queries/`, `Thread_Manager/`, `Data_Manager/`,
  `Distorcao_Manager/`, `Inv_Screen/`, `Interface_Tools/`) nem `Recursos/Firebird/fbclient.dll`;
- não embute `config.ini` (falta `--add-data`) e não coleta `matplotlib`/`numpy`/`scipy`;
- usa `collect_all` em módulos da stdlib (`base64`, `io`, `datetime`, `ctypes`), o que não faz
  sentido e pode falhar no build.

Para concluir: partir do `.spec` mais recente (`Inventario_3.5.0.spec`), garantir `--add-data` de
`config.ini`, `Recursos/Firebird/fbclient.dll` e do backend do matplotlib, gerar o executável em
máquina limpa e só então versionar a receita (removendo `*.spec` do `.gitignore`).

---

## 4. Novos Problemas Identificados (N1–N9) — status atualizado

> Legenda: ✅ corrigido · 🔄 parcial/em andamento · ⬜ pendente.

| # | Problema | Status | Observação |
|---|---|---|---|
| N1 | Queries de comando sempre falsas | ✅ | Corrigido — `WHERE VLDIA {op} PRECU` / `CUSME {op} PRECU`. |
| N2 | UnboundLocalError em ven_get/ent_get | ✅ | Corrigido — `return None` no `except` de ambos. |
| N3 | Threads chamando Tk (não thread-safe) | ✅ | Roteado via `_safe_schedule_ui`/`atualizar_ui_main`; guarda de widget destruído; `messagebox` fora das funcs; `after()` removido da thread em `executa_comandos` (ver §5.3). |
| N4 | Pool de conexões frágil | ✅ | Health-check (`_conexao_valida` com `SELECT 1 FROM RDB$DATABASE`), descarte/reposição de conexões stale, reposição na devolução e `fechar()` seguro; código morto `trocar_bd` removido. |
| N5 | Erros de entrada não tratados | ✅ | Porta `int \| None` validada; PROPRI vazio tratado; finalização agendada na main thread (ver §5.5). |
| N6 | config.ini encoding/seções | ✅ | Encoding UTF-8 e seções consolidadas; tema padronizado `cor_do_tema` (ver §5.2). |
| N7 | Correções de UI menores | ✅ | Todos os itens resolvidos (ver §5.6). |
| N8 | Limpeza imports Valor_* | ✅ | Imports/comentários órfãos limpos. |
| N9 | Consolidar animação de status duplicada | ✅ | `TextAnimator` (`Tk_Status_Animator.py`) adotado em `Banco_de_Dados_Func` e `Tk_Progress_Bar` (ver §5.7). |

---

## 5. Erros/Dívidas adicionais encontrados na análise

Itens não cobertos (ou subestimados) no plano v3.0, verificados no estado atual do código.

### 5.1 `obter_caminho_curto_banco_dados` — divergência de comportamento

O plano v3.0 previa que o `except` retornasse `caminho_longo` (fallback silencioso). O código atual
`raise RuntimeError(f"Erro ao obter o caminho curto: {e}")` (`Banco_de_Dados_Func.py:221-222`).
Comportamento **mais seguro** (falha alto), mas **diverge do plano**. Decisão mantida: `raise`.
O chamador (`on_click_confirm`) já captura e exibe mensagem amigável ao usuário. ✅

### 5.2 Case-sensitivity do tema (config.ini)

Inconsistência de capitalização entre:
- `config.ini:11` → `cor_do_tema` (minúscula)
- `Inventario.py:15` → lê `'cor_do_tema'` (minúscula)
- `Config_Func.py` → usava `'Cor_do_tema'` (maiúscula) no `get`, agora usa `cor_do_tema`.

Padronizado tudo para `cor_do_tema` em minúsculas. ✅

### 5.3 N3 — Chamadas Tk em threads e ausência de guarda de widget destruído

Resolvido nos commits `34cc7ef`/`fc40fdd` e nas correções desta revisão:

- ✅ `Thread_Manager/Thread_Executor.py` — `_safe_schedule_ui` verifica `winfo_exists()` e captura
  `TclError`; `check_thread` faz `master.after(...)` somente após validar o widget.
- ✅ Comandos/Conexão — progresso e callbacks são agendados na main thread
  (`atualizar_ui_main`); erros exibidos por callbacks agendados.
- ✅ Funcs de consulta (`Val_Inv_Func`, `Val_Ven_Func`, `Val_Ent_Func`) não chamam mais
  `messagebox` — propagam `DatabaseError`; a tela trata via callback seguro.
- ✅ `Comandos_Func.executa_comandos` — remanescente `comando.after(5, ...)` substituído por
  `atualizar_ui_main(comando, lambda ...)`.

### 5.4 N4 — Pool de conexões

✅ Resolvido (ver N4 na seção 4): health-check por conexão (`_conexao_valida` com
`SELECT 1 FROM RDB$DATABASE`), descarte/reposição de conexões stale, reposição na devolução,
`fechar()` seguro e `_devolver_conexao` sem mascarar o erro original. O código morto `trocar_bd`
foi **removido** (não existe mais em `Thread_Manager/`).

### 5.5 N5 — Erros de entrada

- ✅ `Inventario_Conn.py` — `ConfiguracaoBanco.port` tipado `int | None`; `Banco_de_Dados_Func`
  valida com `isdigit()` antes de converter.
- ✅ `Banco_de_Dados_Func.py` — `propri` vazio tratado (sem `IndexError`).
- ✅ `_disparar_queries` — callbacks de finalização agendados na main thread com guardas; risco de
  double-destroy reduzido.

### 5.6 N7 — Correções de UI menores

- ✅ `Interface_Tools/Tk_Tooltip.py` — `bbox("insert")` validado; retorna sem erro se `None`.
- ✅ `Consultas/Consultas_Val_Screen.py` — `cm.posicionar_container(hub)` em `try/except RuntimeError`
  (posição padrão do Tk quando não há espaço livre).
- ✅ `Outros/Banco_Images.py` — `help_base64_image` sem vírgula inicial inválida.
- ✅ `Interface_Tools/Treeview_Table/Listagem_Treeview.py` — ESC, `grab_set()` e
  `WM_DELETE_WINDOW` (agora via `toplevel.protocol`, não `treeview.bind`).

### 5.7 N9 — Consolidação de animação de status

✅ Criado `Interface_Tools/Tk_Status_Animator.py` (classe `TextAnimator`) consolidando a animação de
`.`, `..`, `...` via `after()` com cancelamento de jobs anteriores. Adotado em
`Banco_de_Dados_Func._iniciar_animacao` e `Tk_Progress_Bar._iniciar_ciclo_mensagens`,
eliminando a duplicação e o ciclo de `after` não cancelado.

### 5.8 Código morto

- ✅ `Gerenciador_Thread_BD.trocar_bd()` — **removido** (não existe mais no código; ver §5.4).
- ✅ `Dashboard/Dashboard_Charts.py` — cálculo morto do tooltip (`px`, `py`, `dist` via
  `np.hypot`) removido em 26/10/2026, sem mudança de comportamento.
- ✅ Views físicas `V_LAN_COM` e `V_DIFF_ENTRADA_SAIDA_MES` — removidas de
  `Queries/View_Queries.py` e `Queries/Create_Views.py` (0 referências no código) e **dropadas
  nas bases cliente** (concluído em 28/10/2026).

---

## 6. Novas Features

> **Feature 1 concluída.** A **Feature 2 foi descartada por decisão do usuário em 28/10/2026** e
> não será implementada.

### Feature 1 — Dashboard Visual — ✅ IMPLEMENTADO

Módulo `Dashboard/` (`Dashboard_Screen.py`, `Dashboard_Func.py`, `Dashboard_Charts.py`) entregue e
em produção: cards de KPI (**Valor do Inventário**, **Total de Vendas**, **Total de Entradas**,
**Vendas 1.3** e **Previsão de Inventário**), gráfico
de tendência dos últimos 5 anos (Barras/Linhas × Mês/Ano, curvas suavizadas com
`scipy.make_interp_spline`, valores nas barras, toolbar e tooltip), cópia do valor do card por
clique, filtros persistidos em `~/.inventario_tools_dashboard.json` e carregamento em thread
(KPIs e tendência separados).
Os quatro primeiros cards mostram variação percentual vs período anterior; a **Previsão de
Inventário** é uma **estimativa do fim do período** rolada a partir do **saldo corrente**
(`hoje`): `fim < hoje` → `inv_corrente − movimento(fim+1..hoje)`; `fim >= hoje` →
`inv_corrente + movimento(hoje+1..fim)`, sempre a custo atual (`tpmov`/`precu`) e no mesmo
universo de `QUERY_INVENTARIO`. Exibe o subtexto fixo "estimativa do período", sem comparativo.
Falha da consulta aparece como `Erro` no card (B2). O **B1** (contagem dupla do modelo anterior,
erro até −21,1% em 2024) foi **concluído em 27/10/2026** (`c7ad6a1`).

**Não implementado da proposta original:** o indicador de *saúde do banco*
(`saude = 100 - (total_problemas / total_produtos * 100)` com faixas verde/amarelo/vermelho)
**não** existe no Dashboard atual — o gráfico mostra vendas/entradas/diferença, não problemas de
cadastro. Se for retomado, deve virar item próprio.

### Feature 2 — Validação Pré-Inventário — ❌ DESCARTADA (decisão do usuário, 28/10/2026)

O checklist automático de validação pré-inventário (módulo `Validacao/` com
`Validacao_Screen.py`, `Validacao_Func.py`, `Validacao_Itens.py`) **não será implementado**.
O diretório `Validacao/` não existe no repositório e **não deve ser criado**.
`tests/test_validacao.py` **não** pertence a esta feature — cobre as validações de entrada
(`precu_porcent_entry_validate` e afins) e **permanece**.

---

## 7. Roadmap de Execução

### 7.1 Ordem Ideal de Execução (restante)

| Passo | Item | Objetivo | Tempo Est. |
|---|---|---|---|
| 1 | **Fase 6** — PyInstaller: validar `Inventario_3.5.0.spec` (add-data de `config.ini`, `fbclient.dll`, matplotlib), versionar a receita | Validar executável | 1 h |
| 2 | **Testes manuais** — troca de período + reabertura das telas (exigem a app aberta com banco real) | Homologação | 30 min |

**Fora do código / já resolvidos:**

| Item | Situação em 28/10/2026 |
|---|---|
| **Fase 1.1 remanescente** — política para `com_ger` (SQL livre) | ✅ **Definitiva como está** — aviso + confirmação; sem whitelist (decisão do usuário) |
| **Fase 3.3 remanescente** — `logging` nos `except: pass` | ✅ **Concluída** — 0 `except: pass` no app |
| **`DROP VIEW`** de `V_LAN_COM` e `V_DIFF_ENTRADA_SAIDA_MES` | ✅ **Concluído** |
| **Fase 4** — type hints + `py.typed` | ❌ **Descartada** (decisão do usuário) |
| **Feature 2** — Validação Pré-Inventário | ❌ **Descartada** (decisão do usuário) |
| **Item 10.1** — paralelizar consultas dentro de `_calcular_kpis` | ⏹️ **Encerrado sem código** (ganho de décimos; decisão do usuário) |
| **Item 10.2 (B1)** — previsão rolada a partir do saldo corrente | ✅ **Concluído** em 27/10/2026 (`c7ad6a1`) |
| **Item 6.10** — rotação da senha do banco | ✅ **Concluído** |

Já concluídos desde a revisão anterior: **Fase 1.2** (credenciais em `[Credenciais]`), **N4**
(pool), **Fase 3.1** (imports no topo), **Fase 5.2/5.3** (testes puros e de queries) e
**Feature 1 — Dashboard**.

### 7.2 Tempo Estimado Total (restante)

| Categoria | Horas Estimadas |
|---|---|
| Refatoração (Fase 6 — PyInstaller) | 1,0 h |
| Homologação manual (período + telas) | 0,5 h |
| **TOTAL** | **1,5 h** |

### 7.3 Ganho Esperado

- Bugs estruturais já corrigidos: N1–N9 e o pool de conexões (N4)
- Queries centralizadas e parametrizadas, com contrato coberto por teste
- Suíte de testes ampliada: **212 testes** cobrindo funções puras, Dashboard, threads e contrato
  das queries
- Dashboard entregue e com KPI de previsão reconciliado com o saldo corrente
- SQL livre (`com_ger`) mantido **por decisão do usuário** — risco aceito e documentado

---

## 8. Dependências Novas

| Dependência | Versão | Uso | Status |
|---|---|---|---|
| matplotlib | (sem pin em `requirements.txt`) | Gráficos do Dashboard | ✅ declarado |
| numpy | (sem pin em `requirements.txt`) | Cálculos do gráfico (`Dashboard_Charts.py`) | ✅ declarado |
| scipy | 1.18.1 na `.venv` (sem pin) | Curvas suavizadas (`make_interp_spline`) | ✅ declarado |
| customtkinter / tkcalendar / Pillow / fdb / pyperclip | (sem pin) | UI, calendário, imagens, Firebird, clipboard | ✅ declarado |
| pytest | >= 7.0 | Testes unitários (dev) | ✅ já instalado (`requirements-dev.txt`) |
| fpdf2 | >= 2.8 | Geração de PDFs (opcional) | ⬜ não usado (0 referências no código) |

> O `matplotlib` é usado com backend `Agg` em `Dashboard_Charts.py`, o que também importa para o
> empacotamento (Fase 6).
