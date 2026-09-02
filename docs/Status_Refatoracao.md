# Status da Refatoração — Inventario_Tools

**Documento atualizado em:** 02/09/2026
**Branch de trabalho:** `refatoracao_v3.5`
**Base do plano:** `docs/Plano_Refatoracao_Inventario_Tools_v2.md` (v5.0)
**Último commit:** `e99bc97` ("Persist DB credentials and add config UI")

> Este documento verifica o que já foi realizado e lista o que ainda falta, item a item,
> conforme o plano de refatoração. Legenda: ✅ concluído · 🔄 em andamento/parcial · ⬜ pendente.

---

## Visão geral do progresso

- **Fase 0 (Preparação)** — ✅ concluída.
- **Fase 1 (Segurança e Configuração)** — ✅ concluída (queries parametrizadas, credenciais em config, AppConfig centralizada).
- **Fase 2 (Eliminar Código Duplicado)** — ✅ concluída (funções unificadas, factories de tela e listagem).
- **Fase 3 (Arquitetura e Organização)** — 🔄 maior parte concluída; imports lazy restam em 1 arquivo.
- **Fase 4 (Type Hints)** — 🔄 parcial (~12/40 arquivos com anotações).
- **Fase 5 (Testes Unitários)** — ✅ 59 testes passando; queries centralizadas cobertas por contrato nominal.
- **Fase 6 (PyInstaller)** — 🔄 config existe mas está desatualizada.
- **N1–N9 (Novos Problemas)** — ✅ 9/9 corrigidos.

A branch `refatoracao_v3.5` acumula **13 commits** desde o estado documentado no status anterior (28/08/2026), consolidando: centralização de queries, factories de UI, unificação de funções, hardening de threads, logging estruturado e persistência de credenciais.

---

## Fase 0 — Preparação

| Item | Status | Observação |
|---|---|---|
| 0.1 Verificar baseline (projeto roda) na `refatoracao_v3.5` | ✅ | Branch com histórico contínuo, 54 testes passando. |
| 0.2 Criar estrutura `tests/` funcional | ✅ | 6 arquivos de teste: `test_formatacao.py`, `test_validacao.py`, `test_comandos_func.py`, `test_copy_val.py`, `test_periodo.py`, `test_query_operations.py`. `conftest.py` com fixtures `FakeCursor`/`FakeConexao`. |
| 0.3 Registrar comandos em `AGENTS.md` | ✅ | `AGENTS.md` presente na raiz. |

---

## Fase 1 — Segurança e Configuração

### 1.1 Parametrizar queries (SQL Injection) — ✅ concluído

Todas as queries de consulta e comando utilizam placeholders `?` para valores dinâmicos. A listagem de CFOP em `Val_Ent_Func.py` usa `.format()` apenas para inserir a lista fixa de placeholders (não dados do usuário), sendo seguro.

**Arquivos parametrizados:**
- `Thread_Manager/Query_Operations.py` — `query_selector`/`query_updater`/`query_executor` aceitam `params`.
- `Queries/Consulta_Queries.py` — 17 constantes SELECT com `?`.
- `Queries/Comando_Queries.py` — 14 constantes UPDATE/INSERT com `?`.
- `Consultas/Valor_Inventario/Consultas_Val_Inv_Func.py` — params para query de inventário.
- `Consultas/Valor_Vendas/Consultas_Val_Ven_Func.py` — params para datas.
- `Consultas/Valor_Entradas/Consultas_Val_Ent_Func.py` — params para CFOP + datas.
- `Consultas/Generics_Functions/Gen_Funcs_Consulta.py` — `prod_get` aceita params.
- `Consultas/Controla_Estoque/Consultas_Contr_Estq_Screen.py` — parametrizado.
- `Consultas/Quantidade_Exorbitante/Consultas_Quant_Maior_List.py` — parametrizado.
- `Comandos/Comandos_Gerais/Comandos_Func.py` — todos os comandos mapeados como `(query, params)`.
- `Comandos/Distorcao_Saldo/Comandos_Dist_Saldo.py` — UPDATE e INSERT parametrizados com `?`.

**Pendência remanescente:**
- **`com_ger` (Comando Geral)** — SQL livre mantido conforme decisão do usuário. Sem sanitização programática; apenas aviso de `showwarning` + confirmação. Risco documentado.

### 1.2 Mover credenciais para config — ✅ concluído

- `Banco_de_Dados/Tela_Banco_Dados/Banco_de_Dados_Func.py:185-192` — lê `user_db` e `pass_db` via `carregar_diretorio('Credenciais', ...)`.
- `config.ini` contém seção `[Credenciais]` com valores padrão (SYSDBA/masterkey).
- `config.ini` está no `.gitignore` (evita exposição de credenciais).
- `validar_credenciais()` valida presença antes de conectar.

### 1.3 Centralizar leitura de config — ✅ concluído

- `Configuracoes/Config_Manager.py` — classe `AppConfig` com `RLock`, escrita atômica (`os.replace`), encoding UTF-8, dirty tracking.
- Singleton `get_config()` accessor.
- Helpers `salvar_diretorio()` / `carregar_diretorio()` delegam para `AppConfig`.

---

## Fase 2 — Eliminar Código Duplicado

| Item | Status | Observação |
|---|---|---|
| 2.1 Unificar `banco_codigo_valueform()` | ✅ | Unificado em `Gen_Funcs_Consulta.py`. Cópias anteriores removidas. |
| 2.2 Unificar `copy_val()` | ✅ | Unificado em `Gen_Funcs_Consulta.py` com parâmetro `prefix`. |
| 2.3 Extrair lógica de listagem (Treeview) | ✅ | `Interface_Tools/Treeview_Table/Listagem_Treeview.py` — factory `criar_tela_listagem()`. Elimina boilerplate de 8 arquivos `*_List*.py`. |
| 2.4 Extrair padrão de tela de consulta | ✅ | `Interface_Tools/Consulta_Screen/Consulta_Screen.py` — factory `criar_tela_consulta()`. Container base compartilhado. |

---

## Fase 3 — Arquitetura e Organização

| Item | Status | Observação |
|---|---|---|
| 3.1 Mover imports para o topo | 🔄 | Apenas `Comandos/Distorcao_Saldo/Comandos_Dist_Saldo.py` ainda tem 7 imports lazy (dentro de `on_click_dist_saldo` e `on_click_confirm_btt`). Todos os demais arquivos de tela e func estão limpos. |
| 3.2 Separar queries em `Queries.py` | ✅ | `Queries/Consulta_Queries.py` (17 constantes SELECT) + `Queries/Comando_Queries.py` (14 constantes UPDATE/INSERT) = 31 queries centralizadas com docstrings. |
| 3.3 Tratar erros adequadamente | ✅ | `obter_caminho_curto_banco_dados` agora `raise RuntimeError` (fail alto). `except DatabaseError` em todos os `*_Func.py` de consulta (zero `except:` genérico no módulo `Consultas/`). |
| 3.4 Limpar `print()` de debug | ✅ | Zero `print()` no código. Logging estruturado (`get_logger`) em 12 módulos. Handler `TimedRotatingFileHandler` com rotação diária e retenção de 7 dias. |

---

## Fase 4 — Type Hints e Assinaturas

| Item | Status | Observação |
|---|---|---|
| 4.1 Adicionar type hints | 🔄 | ~12 de ~40+ arquivos com anotações. Cobertura boa em `Config_Manager.py`, `Tk_Progress_Bar.py`, `Tk_Status_Animator.py`, `Comandos_Func.py`, `Gen_Funcs_Consulta.py`, `Listagem_Treeview.py`, `Inventario_Conn.py`. Telas e funcs de consulta ainda majoritariamente sem type hints. |
| 4.2 Criar `py.typed` | ⬜ | Não existe. Aplicação desktop (não é pacote distribuível), prioridade baixa. |

---

## Fase 5 — Testes Unitários

### 5.1 Configurar pytest — ✅
`requirements-dev.txt`, `tests/conftest.py` com fixtures, pytest instalado. **54 testes passando.**

### 5.2 Testar funções puras — ✅ completo

| Função | Arquivo | Status |
|---|---|---|
| `banco_codigo_valueform()` | Gen_Funcs_Consulta.py | ✅ coberto (`test_formatacao.py`) |
| `precu_porcent_entry_validate()` | Comandos_Func.py | ✅ coberto (`test_validacao.py`) |
| `copy_val()` (mock pyperclip) | Gen_Funcs_Consulta.py | ✅ coberto (`test_copy_val.py`) |
| `calcular_periodo()` / `formatar_banco()` | Outros/Periodo_Inventario.py | ✅ coberto (`test_periodo.py`) |
| `_montar_operacoes()` / `comandos_true()` | Comandos_Func.py | ✅ coberto (`test_comandos_func.py`) |
| `query_updater` / `_safe_schedule_ui` / validações UI | Thread_Manager / Configuracoes | ✅ coberto (`test_query_operations.py`, `test_validacao.py`) |

### 5.3 Testar queries isoladamente — 🔄 parcial

- `test_query_operations.py` cobre `query_selector`/`query_updater` com `FakeCursor`/`FakeConexao`.
- `test_comandos_func.py` importa e valida `QUERY_UPDATE_PRECU_PORCENTAGEM`.
- Testes em `tests/test_queries.py` validam os nomes e o conteúdo não vazio das **20 queries** de `Consulta_Queries.py` e dos **14 comandos** de `Comando_Queries.py`.

---

## Fase 6 — Compatibilidade com PyInstaller

| Item | Status | Observação |
|---|---|---|
| Config `Auto_py_to_exe` | 🔄 | `Outros/Auto_py_to_exe config.json` existe mas contém **caminhos hardcoded desatualizados** (`C:/Users/Sup-12/...`). Faltam `Queries/`, `Thread_Manager/`, `Interface_Tools/`, `Outros/Logger/` nos datas. Sem `.spec` no repo. |
| Validar executável | ⬜ | Não executado após a reorganização de módulos. |

---

## Novos Problemas (N1–N9)

| Item | Status | Observação |
|---|---|---|
| **N1** Queries de comando sempre falsas | ✅ | Corrigido — `WHERE VLDIA {op} PRECU` / `CUSME {op} PRECU` (compara com coluna alvo correta). |
| **N2** UnboundLocalError em ven/ent_get | ✅ | Corrigido — `return None` no `except` de `Ven_get` e `Ent_get`. |
| **N3** Threads chamando Tk | ✅ | Roteado via `_safe_schedule_ui`/`atualizar_ui_main`; guarda de `winfo_exists()`/`TclError`; `messagebox` fora das funcs de consulta; `after()` removido da thread em `executa_comandos`. |
| **N4** Pool de conexões frágil | ✅ | `fechar()` usa `get_nowait()` + `except Empty`; `_conexao_valida()` executa health-check com `SELECT 1 FROM RDB$DATABASE`. Conexões stale são fechadas e substituídas. |
| **N5** Erros de entrada não tratados | ✅ | `ConfiguracaoBanco.port` tipado `int \| None`; `Banco_de_Dados_Func` valida com `isdigit()`. `propri` vazio tratado. Finalização agendada na main thread com guardas. |
| **N6** config.ini encoding/seções | ✅ | UTF-8 via `AppConfig`. Seções consolidadas (`[Banco]`, `[Porta]`, `[FBClient]`, `[Tema]`, `[Servidor]`, `[Credenciais]`). `cor_do_tema` padronizado em minúsculas. |
| **N7** Correções de UI menores | ✅ | `Tk_Tooltip` — `bbox("insert")` validado. `posicionar_container` com `try/except RuntimeError`. `Banco_Images` sem vírgula inválida. `Listagem_Treeview` com ESC + `grab_set()` + `WM_DELETE_WINDOW`. Botão "Copiar Valor" desabilitado durante consulta (via factory). |
| **N8** Limpeza imports Valor_* | ✅ | Imports/comentários órfãos limpos. |
| **N9** Consolidar animação de status | ✅ | `TextAnimator` (`Tk_Status_Animator.py`) consolidando animação. Adotado em `Banco_de_Dados_Func` e `Tk_Progress_Bar`. |

---

## Itens Adicionais Identificados (além do plano original)

| Item | Status | Observação |
|---|---|---|
| Logging estruturado | ✅ | `Outros/Logger/Get_Logger.py` — `QueueHandler` + `TimedRotatingFileHandler`, retenção 7 dias, rotação diária. 12 módulos instrumentados. Zero `print()`. |
| `cor_do_tema` case-sensitivity | ✅ | Padronizado em minúsculas em todo o pipeline (config → leitura → uso). |

---

## Features Futuras

| Feature | Status | Observação |
|---|---|---|
| Dashboard Visual (`Dashboard/`) | ⬜ | Depende de Fase 5.3 (queries testadas) e Fase 4 (type hints para manutenção). |
| Validação Pré-Inventário (`Validacao/`) | ⬜ | Depende de Fases 1–3 (já prontas) e Fase 5.3. |

---

## Próximos passos sugeridos (ordem)

1. **Fase 3.1** — Mover os 7 imports lazy de `Comandos_Dist_Saldo.py` para o topo do módulo.
2. **Fase 1.1 (com_ger)** — Definir política de validação para SQL livre (whitelist de comandos permitidos ou bloqueio de `DROP`/`DELETE` sem `WHERE`).
3. **Fase 6** — Atualizar `Auto_py_to_exe config.json` com caminhos corretos e validar executável.
4. **Fase 4** — Ampliar type hints nos módulos de tela e funcs de consulta.
5. **Fase 4.2** — Criar `py.typed` (baixa prioridade para app desktop).
6. **Features** — Dashboard Visual e Validação Pré-Inventário.
