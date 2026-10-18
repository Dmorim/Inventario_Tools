# Status da Refatoração — Inventario_Tools

**Documento atualizado em:** 18/10/2026  
**Branch de trabalho:** `refatoracao_v3.5`  
**Base do plano:** `docs/Plano_Refatoracao_Inventario_Tools_v2.md` (v5.1)  
**Últimos commits:** `d6bc0ee` ("Add distortion inventory manager") + mudanças de migração de período nas telas de consulta

> **Decisões registradas (fora de escopo da refatoração):**
> - **SQL Livre (`com_ger`)** — ficará em total responsabilidade do operador. **Não** será aplicada whitelist nem qualquer validação programática. Apenas confirmação com aviso de risco.
> - **Type Hints (Fase 4 / `py.typed`)** — a refatoração **não** cobrirá mais o uso de type hints.

> Este documento verifica o que já foi realizado e lista o que ainda falta, item a item, conforme o plano de refatoração. Legenda: ✅ concluído · 🔄 em andamento/parcial · ⬜ pendente.

---

## Visão geral do progresso

- **Fase 0 (Preparação)** — ✅ concluída.
- **Fase 1 (Segurança e Configuração)** — ✅ concluída (queries parametrizadas, credenciais em config, AppConfig centralizada).
- **Fase 2 (Eliminar Código Duplicado)** — ✅ concluída (funções unificadas, factories de tela e listagem).
- **Fase 3 (Arquitetura e Organização)** — ✅ concluída (imports no topo, hardening de threads, logging estruturado).
- **Fase 4 (Type Hints)** — ❌ fora de escopo (decisão do usuário).
- **Fase 5 (Testes Unitários)** — ✅ 69 testes passando (59 originais + 10 de distorção de saldo); queries centralizadas cobertas por contrato nominal; pool de BD adicionado aos testes.
- **Fase 6 (PyInstaller)** — 🔄 config existe mas desatualizada; build pendente (a fazer por último).
- **N1–N9 (Novos Problemas)** — ✅ 9/9 corrigidos (inclui N4 com health-check).
- **Refatoração de Datas (PeriodoManager)** — 🔄 **em andamento**: modelo (`PeriodoInventario/PeriodoManager`) pronto, Top Frame integrado ao manager, **telas de consulta** migradas para snapshot de período. Dashboard e Comandos ainda pendentes.
- **Features** — ✅ Dashboard Visual implementado; ⬜ Validação Pré-Inventário pendente.

---

## Refatoração de Gerenciamento de Datas (roadmap)

Baseado em `docs/roadmap/roadmap_refatoracao_datas.html` (15/10/2026).

### Fase 0 — Preparação e contrato ✅
| Item | Status | Observação |
|---|---|---|
| Contrato API (`obter_periodo`, `atualizar_periodo`) | ✅ | Definido em `Data_Manager/PeriodoManager.py`. |
| Formato para BD padronizado | ✅ | `PeriodoInventario.inicio_formatado/fim_formatado` usam `%d.%m.%Y` (alinhado a `formatar_banco`). |
| Mapeamento de consumidores | 🔄 | `app_self.data_banco_*` mapeado; parcial migrado (Consultas). |

### Fase 1 — Modelo de dados ✅
| Item | Status | Observação |
|---|---|---|
| `PeriodoInventario` (frozen) + validação | ✅ | `Data_Manager/PeriodoInventario.py` — valida período invertido. |
| `PeriodoManager` (single source + listeners) | ✅ | `Data_Manager/PeriodoManager.py` — `obter_periodo`, `atualizar_periodo`, `adicionar/remover/_notificar_listeners`. |
| Testes do modelo/manager | ⬜ | **Faltam** testes para `PeriodoInventario` e `PeriodoManager` (equality, imutabilidade, notificação, idempotência). |

### Fase 2 — Integração à inicialização ✅
| Item | Status | Observação |
|---|---|---|
| Criar manager no `Inventario` | ✅ | `Inventario.py:35` — `self.periodo_manager = PeriodoManager(...)`. |
| Propriedades legadas `data_banco_*` | 🔄 | Ainda presentes (`Inventario.py:47-53`) — **a remover na Fase 7**. |

### Fase 3 — Top Frame ✅ (parcial)
| Item | Status | Observação |
|---|---|---|
| Widgets locais, assinatura limpa | ✅ | `Inv_Top_Frame.py` recebe `periodo_manager`. |
| Leitura → `PeriodoInventario` → `atualizar_periodo()` | ✅ | `obter_periodo_dos_controles()` + `atualizar_periodo_manager()` chamados em `abrir_tela()`. |
| Conexão a eventos | 🔄 | Atualização ocorre no clique dos botões (abertura de telas). Radios/comboboxes/DateEntry **não** atualizam o manager em tempo real (não obrigatório, pois telas são abertas sob demanda). |

### Fase 4 — Ações dos botões 🔄
| Item | Status | Observação |
|---|---|---|
| Callbacks explícitos | 🔄 | Top Frame chama telas diretamente via `abrir_tela()`. Pode ser refatorado para `TopFrameActions` (opcional). |

### Fase 5 — Dashboard 🔴 Pendente
| Item | Status | Observação |
|---|---|---|
| `Dashboard_Screen` recebe `periodo_manager` | ⬜ | Ainda depende de `app_self.data_banco_*`. |
| Snapshot na abertura + listener | ⬜ | Necessário (tela longeva, usuário pode trocar período). |
| Remover listener no fechamento | ⬜ | WM_DELETE_WINDOW/ESC. |

### Fase 6 — Consultas e Comandos 🔄 Parcial
| Item | Status | Observação |
|---|---|---|
| **Consultas (sob demanda)** | ✅ **Concluído** | Todas as telas recebem `periodo` (snapshot). Corrigido `Quant_Maior` (Screen+List), `Contr_Estq` (chamada), `Val_Ent` (`periodo=periodo`). `Distorção` concluída com manager próprio. |
| **Comandos** | ⬜ **Pendente** | `Comandos_Screen/Comandos_Func` usam `self.data_banco_inicial` (herdado de objeto legado). Botão de correção de distorção verifica `hasattr(self, 'dist_saldo_list')` — migrar para `DistorcaoManager.possui_itens()`. Passar `periodo` (snapshot) no clique, sem listener. |

### Fase 7 — Remover compatibilidade legada ⬜
| Item | Status | Observação |
|---|---|---|
| Remover `data_banco_inicial/final` e `_periodo_selecionado` de `Inventario.py` | ⬜ | Aguardando migração completa (Comandos/Dashboard). |
| Remover imports mortos | ⬜ | Após limpeza. |
| Busca global de `app_self.data_banco_*` | ⬜ | Verificar 0 usos fora do legado. |

### Fase 8 — Testes, regressão e documentação ⬜
| Item | Status | Observação |
|---|---|---|
| Testes `PeriodoInventario/PeriodoManager` | ⬜ | Criar `tests/test_periodo_manager.py` (igualdade, imutabilidade, período invertido, formatação dd.mm.yyyy, notificação, idempotência, registro/remoção de listeners). |
| Ajustar fakes legados | ⬜ | `test_comandos_func.py` usa `self.data_banco_inicial` (mudar para contrato com `periodo.inicio_formatado`). |
| Testes manuais de troca de período | ⬜ | Após Dashboard. |
| Atualizar este Status | 🔄 | Em andamento. |

---

## Próximos passos (recomendados)

Ordem pragmática (fecha Fase 6 primeiro, depois reativo):

| Etapa | Ação | Estimativa |
|---|---|---|
| **E6a** | **Comandos**: `Comandos_Screen(periodo, parent)`; `Comandos_Func` receber `periodo` (ou `inicio_formatado`); migrar check de distorção para `DistorcaoManager.possui_itens()`; atualizar chamada em `Inv_Top_Frame`. | 30–40 min |
| **E6b** | Corrigir fake em `test_comandos_func.py` para novo contrato de período. | 5 min |
| **E5** | **Dashboard**: `Dashboard_Screen(periodo_manager, parent, button)`; snapshot + listener com remoção no fechamento (WM_DELETE_WINDOW/ESC); manter proteção por `seq`. Ajustar `Inv_Top_Frame` para passar `periodo_manager`. | 1h30–2h |
| **E7** | Remover propriedades legadas de `Inventario.py`, buscar usos restantes de `app_self.data_banco_*`. | 15–30 min |
| **E1a** | Criar `tests/test_periodo_manager.py` (cobrir Fase 1). | 30 min |
| **E8** | Testes de regressão + commit consolidado + atualizar Status/roadmap. | 20 min |

**Próximo passo imediato:** **E6a — Migrar Comandos para usar `periodo` (snapshot)**.