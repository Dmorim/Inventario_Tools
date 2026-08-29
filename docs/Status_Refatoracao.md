# Status da Refatoração — Inventario_Tools

**Documento atualizado em:** 28/08/2026
**Branch de trabalho:** `refatoracao_v3.5`
**Base do plano:** `docs/Plano_Refatoracao_Inventario_Tools_v2.md` (v3.0)

> Este documento verifica o que já foi realizado e lista o que ainda falta, item a item,
> conforme o plano de refatoração. Legenda: ✅ concluído · 🔄 em andamento/parcial · ⬜ pendente.

---

## Visão geral do progresso

- **Fase 0 (Preparação)** — ✅ concluída.
- **Fase 1 (Segurança e Configuração)** — 🔄 em andamento (parametrização parcial; config centralizada pendente).
- **Fase 2 a 6, N1–N9, Features** — ⬜ majoritariamente pendentes.

O commit `2ea1544` ("Parametrize SQL queries and add pytest tests") consolidou boa parte da
Fase 0 e parte da Fase 1.1 nesta branch. Um refinamento adicional de `Comandos_Func.py`
(linha 16: `DTPRO >= ?` sem aspas) está **sem commit** no working tree.

---

## Fase 0 — Preparação

| Item | Status | Observação |
|---|---|---|
| 0.1 Verificar baseline (projeto roda) na `refatoracao_v3.5` | ✅ | Branch com histórico contínuo, testes passando. |
| 0.2 Criar estrutura `tests/` funcional | ✅ | `tests/__init__.py`, `tests/conftest.py`, `tests/test_formatacao.py`, `tests/test_validacao.py`, `requirements-dev.txt` (commit `2ea1544`). 14 testes passando. |
| 0.3 Registrar comandos em `AGENTS.md` | ✅ | `AGENTS.md` criado (commit `2ea1544`). |

---

## Fase 1 — Segurança e Configuração

### 1.1 Parametrizar queries (SQL Injection) — 🔄 parcial

**Feito (commit `2ea1544`):**
- `Thread_Manager/Query_Operations.py` — `query_selector`/`query_updater`/`query_executor` agora aceitam `params`.
- `Comandos/Comandos_Gerais/Comandos_Func.py` — comandos mapeados como `(query, params)`; placeholders `?` em porcentagem, controla estoque, etc.
- `Consultas/Valor_Entradas/Consultas_Val_Ent_Func.py` e `Consultas/Valor_Vendas/Consultas_Val_Ven_Func.py` — passam `params` para datas/CFOP.
- `Consultas/Generics_Functions/Gen_Funcs_Consulta.py` — `prod_get` aceita `params`.
- `Consultas/Controla_Estoque/Consultas_Contr_Estq_Screen.py` e `Consultas/Quantidade_Exorbitante/Consultas_Quant_Maior_List.py` — ajustados para params.

**Pendências / pontos a revisar:**
- `Consultas_Val_Ent_Func.py:36-37` — datas ainda como `'?'` **entre aspas** (`between '?' AND '?'`); verificar se ligam de fato aos parâmetros.
- `Consultas_Val_Ven_Func.py:34` — datas `(F.DTEMI >= '?')` também **entre aspas**; revisar.
- `Comandos_Func.py:11-12` — operador `{op}` interpolado via f-string (relacionado ao N1).
- **`com_ger` (Comando Geral)** — SQL livre mantido conforme decisão do usuário, com confirmação e aviso de risco (confirmação já existe em `on_click_confirm`).
- **Distorção de Saldo** (`Consultas/Consultas_Dist_Saldo_Screen.py`, `Comandos/Distorcao_Saldo/Comandos_Dist_Saldo.py`) — ainda não parametrizados (EXECUTE BLOCK e INSERT com aspas).

### 1.2 Mover credenciais para config — ⬜ pendente
`Banco_de_Dados/Conexao_Banco_Dados/Inventario_Conn.py:44-45` ainda tem `user='SYSDBA'`, `password='masterkey'` hardcoded. Falta criar `[Credenciais]` no `config.ini` e ler via `Config_Manager`. **Nunca commitar credenciais reais.**

### 1.3 Centralizar leitura de config — ⬜ pendente
`Configuracoes/Config_Manager.py` (classe `AppConfig`) **não existe**. `salvar_diretorio()`/`carregar_diretorio()` ainda releem/reescrevem o arquivo a cada chamada, sem `try/except` e com encoding do locale.

---

## Fase 2 — Eliminar Código Duplicado

| Item | Status | Observação |
|---|---|---|
| 2.1 Unificar `banco_codigo_valueform()` | ⬜ | Ainda duplicada em `Consultas_Val_Inv_Func.py`, `Consultas_Val_Ven_Func.py`, `Consultas_Val_Ent_Func.py`. Falta mover para `Gen_Funcs_Consulta.py` e deletar as 3 cópias. |
| 2.2 Unificar `copy_val()` | ⬜ | 4 cópias (3 com prefixo `'R$ '`, 1 genérica). Falta unificar com parâmetro `prefix`. |
| 2.3 Extrair lógica de listagem (Treeview) | ⬜ | 8 arquivos `*_List*.py`; `Treeview_Select`/`Treeview_Insert` duplicados. Sem factory `ConsultaListagemBase`. |
| 2.4 Extrair padrão de tela de consulta | ⬜ | Boilerplate de Screen repetido; sem `ConsultaScreenBase`. |

---

## Fase 3 — Arquitetura e Organização

| Item | Status | Observação |
|---|---|---|
| 3.1 Mover imports para o topo | ⬜ | Imports lazy ainda espalhados. |
| 3.2 Separar queries em `Queries.py` | ⬜ | `Consultas/Queries.py` e `Comandos/Queries.py` **não existem**. |
| 3.3 Tratar erros adequadamente | 🔄 | `obter_caminho_curto_banco_dados` (Banco_de_Dados_Func) **ainda sem `return caminho_longo`** no `except`. `Consultas_Val_Inv_Func.py` com `except:` genérico ainda pendente. |
| 3.4 Limpar `print()` de debug | ⬜ | `Gerenciador_Thread_BD.py:17-19`, `Banco_de_Dados_Func.py:278,282`, `Consultas_Dist_Saldo_Screen.py` ainda com `print()`. |

---

## Fase 4 — Type Hints e Assinaturas

| Item | Status | Observação |
|---|---|---|
| 4.1 Adicionar type hints | ⬜ | Apenas ~13 anotações e zero `-> return` na maior parte. |
| 4.2 Criar `py.typed` | ⬜ | `py.typed` não existe. |

---

## Fase 5 — Testes Unitários

### 5.1 Configurar pytest — ✅
`requirements-dev.txt`, `tests/conftest.py` com fixtures, pytest instalado. 14 testes passando (commit `2ea1544`).

### 5.2 Testar funções puras — 🔄 parcial

| Função | Arquivo | Status |
|---|---|---|
| `banco_codigo_valueform()` | Gen_Funcs_Consulta.py / Valor_* | ✅ coberto (`test_formatacao.py`) |
| `precu_porcent_entry_validate()` | Comandos_Func.py | ✅ coberto (`test_validacao.py`) |
| `copy_val()` (mock pyperclip) | Gen_Funcs_Consulta.py | ⬜ não coberto |
| `calcular_periodo()` / `formatar_banco()` | Outros/Periodo_Inventario.py | ⬜ não coberto |
| `_montar_operacoes()` | Comandos_Func.py | ⬜ não coberto |

### 5.3 Testar queries isoladamente — ⬜ pendente
Integração com Firebird em memória ou mocks de `query_selector`/`query_updater` (fixtures para isso já existem em `conftest.py`).

---

## Fase 6 — Compatibilidade com PyInstaller

| Item | Status | Observação |
|---|---|---|
| Validar `pyinstaller` / `config.ini` / `fbclient.dll` | ⬜ | Não executado na branch atual. |

---

## Novos Problemas (N1–N9)

| Item | Status | Observação |
|---|---|---|
| **N1** Queries de comando sempre falsas | ⬜ | `Comandos_Func.py:11-12` ainda `WHERE VLDIA {op} VLDIA` / `WHERE CUSME {op} CUSME` — condição sempre falsa. Falta comparar com a coluna alvo (ex.: `VLDIA > PRECU`), definindo semântica. |
| **N2** UnboundLocalError em ven/ent_get | 🔄 | `Ven_get` (Val_Ven) já foi endurecido (rows check + `except (DatabaseError, TypeError)`), mas `Ent_get` (Val_Ent:43-49) ainda usa `valent` após `except` sem `else` — sujeito a `UnboundLocalError`. |
| **N3** Threads chamando Tk | ⬜ | `Thread_Executor.py:33` ainda faz `master.after(100, check_thread)` sem guarda contra widget destruído; `Comandos_Func.py`/`Banco_de_Dados_Func.py` ainda tocam Tk em threads. |
| **N4** Pool de conexões frágil | ⬜ | `Gerenciador_Thread_BD.py`: leak, `Queue.empty()` não thread-safe, sem health-check; `trocar_bd` não usado. |
| **N5** Erros de entrada não tratados | ⬜ | `int(ConfiguracaoBanco.port)` (Inventario_Conn:41), `propri[0]` IndexError, race double-destroy. |
| **N6** config.ini encoding/seções | ⬜ | Ainda há `[Tema]` + `[Configuração��es]` duplicado (acento corrompido CP1252). Relacionado à Fase 1.3. |
| **N7** Correções de UI menores | ⬜ | Botão "Copiar Valor" (Val_Ent), ESC/WM_DELETE nas listagens, `cm.posicionar_container` sem try/except, `Tk_Tooltip.py:30`, `Banco_Images.py:15`. |
| **N8** Limpeza imports Valor_* | 🔄 | `Val_Ven`/`Val_Ent` ainda têm comentários órfãos de datas importadas; estrutura dos 3 arquivos inconsistentes. |
| **N9** Consolidar animação de status | ⬜ | Dois mecanismos (`Tk_Progress_Bar.py` e `Banco_de_Dados_Func.py` `_iniciar_animacao`), duplicados. |

---

## Features Futuras

| Feature | Status | Observação |
|---|---|---|
| Dashboard Visual (`Dashboard/`) | ⬜ | Depende de Fase 3.2 (queries centralizadas) e 2.1/2.2. |
| Validação Pré-Inventário (`Validacao/`) | ⬜ | Depende de Fases 1–3. |

---

## Próximos passos sugeridos (ordem)

1. Completar **Fase 1.1** nas queries ainda com `'?'` entre aspas (Val_Ven/Val_Ent) e Distorção de Saldo.
2. **N1** — corrigir queries sempre falsas (definir coluna alvo de comparação).
3. **N2** — baldear `Ent_get` contra `UnboundLocalError`.
4. **Fases 1.2 + 1.3 + N6** — `Config_Manager` (`AppConfig`), seção `[Credenciais]`, corrigir encoding/seções do `config.ini`.
5. **Fases 2.1–2.2** — unificar `banco_codigo_valueform` e `copy_val`.
6. **Fase 3.3 + N5, 3.4, N3, N4** — robustez (erros, logging, thread-safe Tk, pool).
7. **Fase 5.2** — ampliar testes (copy_val, calcular_periodo, _montar_operacoes).
