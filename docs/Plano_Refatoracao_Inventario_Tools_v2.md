# Plano de Refatoração — Inventario_Tools

**Versão do sistema:** 2.0.0 (em evolução)
**Autor:** Daniel Amorim (com colaboração de Cícero Romão nas consultas SQL)
**Licença:** CC0 1.0 Universal (domínio público)
**Documento atualizado em:** 01/09/2026
**Versão do documento:** 5.0 (reescrito — reflete o estado atual do código após o commit `fc40fdd`,
da branch `refatoracao_v3.5`, e das correções de divergências aplicadas nesta revisão)

> Este documento atualiza o plano original (`Plano_Refatoracao_Inventario_Tools.pdf`) e as revisões
> 1.x/2.0/3.0. Ele incorpora as **modificações já feitas no projeto** (branch `QoL` integrada ao
> `main`, e branch de trabalho `refatoracao_v3.5`) e lista **apenas o trabalho que ainda falta**,
> focado no estado real do código em 01/09/2026.

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
boilerplate que antes era duplicado.

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
| **54 testes** passando (`pytest -q` → 54 passed) | Fase 5 | ✅ Feito |

> **Nota sobre branches:** As modificações de UI foram consolidadas no `main` via PR #14
> (merge `48e7fe3`). A refatoração estrutural é conduzida na branch `refatoracao_v3.5`, que já
> contém os commits `2ea1544`, `1a91bfe`, `a997197`, `d9626b8`, `085a37b`, `7178ff7`, `bd3f77d`,
> `72b7e4f`, `34cc7ef`, `584cf56` e `fc40fdd`. O commit `fc40fdd` ainda aguarda push.

---

## 3. Trabalho Restante (Fases)

> As fases abaixo são o refinamento do plano v3.0, mantendo apenas os itens **ainda pendentes**.
> Onde havia ambiguidade, foi registrada a decisão de projeto atual.

### Fase 1 — Segurança e Configuração (restante)

#### 1.2 Mover credenciais para config — ⬜ PENDENTE

As credenciais continuam hardcoded em:
- `Banco_de_Dados/Tela_Banco_Dados/Banco_de_Dados_Func.py:185-192` — `user='SYSDBA'`,
  `password='masterkey'` passados a `ConfiguracaoBanco.definir(...)`.

**Ação:** adicionar seção `[Credenciais]` no `config.ini` (com padrão SYSDBA/masterkey) e ler via
`Config_Manager` (`get_config().get('Credenciais', 'user')`, `'password'`) antes de montar a
conexão. **Nunca commitar credenciais reais.**

#### 1.1 (remanescente) — SQL livre `com_ger`

`Comandos_Func.py:37` executa `QUERY_COMANDO_GERAL.format(comando=self.com_ger)` com SQL digitado
pelo usuário, sem sanitização (apenas aviso + confirmação). Decisão documentada: manter com
**validação por lista de permissão** ou exigir confirmação explícita com aviso de risco.
A confirmação já existe; avaliar bloqueio de comandos destrutivos (ex.: `DROP`, `DELETE` sem WHERE).

#### 1.4 Corrigir inconsistência de `com_ger` ser executado em thread (ver N3)

Resolvido em `fc40fdd` + correções desta revisão: o SQL livre continua sendo executado via
`query_executor(query_updater, ...)` na thread, mas todo o feedback de UI (status, progresso, erros)
é roteado para a main thread via `atualizar_ui_main` / callbacks agendados. ✅

---

### Fase 3 — Arquitetura e Organização (restante)

#### 3.1 Mover imports para o topo dos módulos — 🔄 PARCIAL

Imports lazy ainda espalhados em telas (ex.: `Banco_de_Dados_Screen.py`,
`Comandos_Screen.py`, `Config_Screen.py`, `Consultas_Screen.py`, `Tutorial_Screen.py` importam
`customtkinter` dentro de função) e em `Comandos_Func.py` (`messagebox` dentro de
`montar_operacoes`) e `Consultas_Dist_Saldo_Screen.py`. Remover quando não houver risco de circular;
resolver circulares com injeção de dependência.

#### 3.3 (remanescente) — robustez de erros

- ✅ `Inventario_Conn.py` — porta agora `int | None`, validada por `isdigit()` antes de usar.
- ⬜ Adicionar `logging` onde houver tratamento de erro em comandos (ver 3.4).

---

### Fase 4 — Type Hints e Assinaturas — ⬜ PENDENTE

#### 4.1 Adicionar type hints

Hoje há ~21 anotações `-> ` em 7 arquivos (principalmente `Config_Manager.py`, `Tk_Progress_Bar.py`,
factories de tela/listagem e `Comandos_Func.py`). Ainda faltam retornos e parâmetros tipados na
maioria dos módulos (telas, listagens, funcs de consulta).

#### 4.2 Criar `py.typed`

O marker `py.typed` não existe. Criar na raiz para indicar suporte a type checking.

---

### Fase 5 — Testes Unitários (restante)

#### 5.2 Testar funções puras — ✅ COMPLETO (54 testes)

| Função | Arquivo | Status |
|---|---|---|
| `banco_codigo_valueform()` | Gen_Funcs_Consulta.py | ✅ coberto |
| `precu_porcent_entry_validate()` | Comandos_Func.py | ✅ coberto |
| `copy_val()` (mock pyperclip) | Gen_Funcs_Consulta.py | ✅ coberto (`test_copy_val.py`) |
| `calcular_periodo()` / `formatar_banco()` | Outros/Periodo_Inventario.py | ✅ coberto (`test_periodo.py`) |
| `_montar_operacoes()` / `comandos_true()` | Comandos_Func.py | ✅ coberto (`test_comandos_func.py`) |
| `query_updater` / `_safe_schedule_ui` / validações UI | Thread_Manager / Configuracoes | ✅ coberto (`test_query_operations.py`, `test_validacao.py`) |

#### 5.3 Testar queries isoladamente — 🔄 PARCIAL

As fixtures `FakeCursor`/`FakeConexao` já existem em `tests/conftest.py`; `test_query_operations.py`
cobre `query_selector`/`query_updater` isolados. Faltam: testes que validem os **nomes das queries**
centralizadas em `Queries/` (todas as 20 consultas e 14 comandos usados pelas telas).

---

### Fase 6 — Compatibilidade com PyInstaller — ⬜ PENDENTE

- Rodar `pyinstaller` e validar módulos embutidos, `config.ini` via `--add-data`, e `fbclient.dll`.
- Revisar `Auto_py_to_exe config.json` após a reorganização de módulos (`Queries/`, factories).

---

## 4. Novos Problemas Identificados (N1–N9) — status atualizado

> Legenda: ✅ corrigido · 🔄 parcial/em andamento · ⬜ pendente.

| # | Problema | Status | Observação |
|---|---|---|---|
| N1 | Queries de comando sempre falsas | ✅ | Corrigido — `WHERE VLDIA {op} PRECU` / `CUSME {op} PRECU`. |
| N2 | UnboundLocalError em ven_get/ent_get | ✅ | Corrigido — `return None` no `except` de ambos. |
| N3 | Threads chamando Tk (não thread-safe) | ✅ | Roteado via `_safe_schedule_ui`/`atualizar_ui_main`; guarda de widget destruído; `messagebox` fora das funcs; `after()` removido da thread em `executa_comandos` (ver §5.3). |
| N4 | Pool de conexões frágil | ⬜ | `fechar()` usa `Queue.empty()`; `trocar_bd` é código morto; sem health-check. |
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

- `Gerenciador_Thread_BD.fechar()` usa `Queue.empty()` como condição de loop (pode engolir erros e
  não é thread-safe para o pattern).
- `trocar_bd` definido mas **nunca utilizado** — reutilizaria conexões do banco antigo. Decidir usar
  ou remover.
- Sem health-check/reconexão para conexões obsoletas.
- `_devolver_conexao` pode mascarar o erro original e/ou vazar conexão.

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

- `Gerenciador_Thread_BD.trocar_bd()` — definido, nunca chamado (ver §5.4). ⬜ Pendente de decisão.

---

## 6. Novas Features

> Pendentes — dependem de queries centralizadas e funções unificadas (já prontas) e de
> `Config_Manager` (já pronto). Podem ser iniciadas após a Fase 4/5.

### Feature 1 — Dashboard Visual

Tela principal pós-conexão com KPIs e gráficos resumidos do inventário, no módulo `Dashboard/`
(`Dashboard_Screen.py`, `Dashboard_Func.py`, `Dashboard_Charts.py`) com `matplotlib` +
`FigureCanvasTkAgg`. Saúde do banco: `saude = 100 - (total_problemas / total_produtos * 100)`;
verde > 90%, amarelo 70–90%, vermelho < 70%.

### Feature 2 — Validação Pré-Inventário

Checklist que roda todas as verificações simultaneamente e apresenta o status de cada uma, com
contagem e ação corretiva, no módulo `Validacao/` (`Validacao_Screen.py`, `Validacao_Func.py`,
`Validacao_Itens.py`). Checklist interativo com drill-down, correção em lote, exportação TXT/CSV.

---

## 7. Roadmap de Execução

### 7.1 Ordem Ideal de Execução (restante)

| Passo | Item | Objetivo | Tempo Est. |
|---|---|---|---|
| 1 | **Fase 1.2** — credenciais em `[Credenciais]` | Eliminar hardcode | 1 h |
| 2 | **N4** — robustecer pool (fechamento ordenado, health-check); decidir `trocar_bd` | Confiabilidade | 2 h |
| 3 | **Fase 1.1 remanescente** — política para `com_ger` (SQL livre) | Segurança | 1 h |
| 4 | **Fase 3.1** — imports no topo dos módulos (restam telas) | Organização | 1 h |
| 5 | **Fase 3.3 remanescente** — `logging` no tratamento de erros | Rastreabilidade | 30 min |
| 6 | **Fase 5.3** — testes dos nomes das queries centralizadas (20/14) | Qualidade | 1 h |
| 7 | **Fase 4** — type hints + `py.typed` | Legibilidade | 2 h |
| 8 | **Fase 6** — PyInstaller | Validar executável | 1 h |
| 9 | Feature: Validação Pré-Inventário | Checklist automático | 4 h |
| 10 | Feature: Dashboard Visual | Visão geral com gráficos | 5 h |

### 7.2 Tempo Estimado Total (restante)

| Categoria | Horas Estimadas |
|---|---|
| Refatoração (Fases 1, 3, 4, 5.3, 6, N4) | 9,5 h |
| Feature: Validação Pré-Inventário | 4–5 h |
| Feature: Dashboard Visual | 5–6 h |
| **TOTAL** | **18,5–20,5 h** |

### 7.3 Ganho Esperado

- Eliminação de riscos de SQL injection (já parcial) e do SQL livre não validado
- Correção de bugs reais: pool frágil (N4) — N1, N2, N3, N5, N6, N7, N8, N9 já resolvidos
- Código tipado, testável e com queries centralizadas (base já pronta)
- Suíte de testes ampliada cobrindo funções puras e queries
- Dashboard e Validação automática antes de fechar inventário

---

## 8. Dependências Novas

| Dependência | Versão | Uso | Status |
|---|---|---|---|
| matplotlib | >= 3.7.0 | Gráficos do Dashboard | ⬜ a adicionar |
| pytest | >= 7.0 | Testes unitários (dev) | ✅ já instalado |
| fpdf2 | >= 2.8 | Geração de PDFs (opcional) | ⬜ opcional |
