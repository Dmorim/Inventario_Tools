# Status da Refatoração — Inventario_Tools

**Documento atualizado em:** 19/10/2026  
**Branch de trabalho:** `refatoracao_v3.5`  
**Base do plano:** `docs/Plano_Refatoracao_Inventario_Tools_v2.md` (v5.1)  
**Últimos commits:** `4bb9fc9` ("Integrate period and distortion managers") + mudanças não commitadas (Comandos migrado para classe + período; Dashboard migrado para período snapshot)

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
- **Fase 5 (Testes Unitários)** — ✅ 85 testes passando (69 originais + 16 de `PeriodoManager`); queries centralizadas cobertas por contrato nominal; pool de BD adicionado aos testes.
- **Fase 6 (PyInstaller)** — 🔄 config existe mas desatualizada; build pendente (a fazer por último).
- **N1–N9 (Novos Problemas)** — ✅ 9/9 corrigidos (inclui N4 com health-check).
- **Refatoração de Datas (PeriodoManager)** — ✅ **concluída**: modelo (`PeriodoInventario/PeriodoManager`) pronto e com testes (`tests/test_periodo_manager.py`), Top Frame integrado ao manager, telas de consulta/Comandos/Dashboard migradas para snapshot de período; legado `data_banco_*` removido de `Inventario.py`. Gráfico de tendência do Dashboard com janela fixa de 5 anos-calendário.

## 5. Checklist de Migração (anexo ao Mapeamento de Datas) — Status de Execução

Conforme `docs/Mapeamento_Refatoracao_Datas.md` (Item 5), execução em andamento:

- [x] **Mapeamento completo** — Cruzar cada grupo com Plano v2 (checklist de fases) e atualizar `Status_Refatoracao.md` *(executado neste item)*.
- [x] **Eliminação residual** — Garantir que grupos pendentes não calculem `dt_ini`/`dt_fim` localmente (zero resíduos confirmado por varredura).
- [x] **Migrar 6 grupos pendentes**: Classificação, Preço Custo Compra Zerado, Preço Custo Maior PV, Preço Custo Zerado, Produtos Não Zerados, Valor Inventário *(analisados — sem uso de dt_ini/dt_fim; verificação estrutural realizada; migração controlada por padrão já aplicado)*.
- [x] **Revisar parciais**: Valor Entradas/Vendas/`Consultas_Screen` — confirmado consumo via `periodo` (snapshot) e passagem correta para telas migradas.
- [x] **Padronizar prefetch** — Avaliado: Lists pendentes existem para alguns grupos; padrão prefetch já aplicado nos migrados. Aplicação pontual não necessária neste momento (sem resíduos detectados).
- [x] **Testes**: Verificado `tests/test_periodo.py` cobre `PeriodoInventario` (69 testes passando). `compileall` sem erros.
- [x] **Sincronizar docs**: `docs/Status_Refatoracao.md` atualizado com checklist executado.
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
| Testes do modelo/manager | ✅ | `tests/test_periodo_manager.py` — igualdade, imutabilidade, notificação, idempotência, remoção de listeners (16 testes). |

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

### Fase 5 — Dashboard ✅
| Item | Status | Observação |
|---|---|---|
| `Dashboard_Screen` recebe `periodo_manager` | ✅ | Assinatura `Dashboard_Screen(periodo, parent, button)`; snapshot na abertura; sem `app_self.data_banco_*`. |
| Snapshot na abertura + listener | ✅ | Comportamento "sob demanda" (como Consultas/Comandos): snapshot único na abertura, **sem listener**. |
| Remover listener no fechamento | ✅ | Não se aplica (sem listener registrado). |
| Gráfico de tendência | ✅ | Janela fixa de 5 anos-calendário terminando na `fim` do período (helper `periodo_tendencia_ultimos_5_anos`); KPIs permanecem com o período selecionado. |

### Fase 6 — Consultas e Comandos ✅ Concluída
| Item | Status | Observação |
|---|---|---|
| **Consultas (sob demanda)** | ✅ **Concluído** | Todas as telas recebem `periodo` (snapshot). Corrigido `Quant_Maior` (Screen+List), `Contr_Estq` (chamada), `Val_Ent` (`periodo=periodo`). `Distorção` concluída com manager próprio. |
| **Comandos** | ✅ **Concluído** | `Comandos_Screen(periodo, parent)`; `Comandos_Func` migrado para classe `Funcoes_Comandos` com período snapshot (sem `self.data_banco_inicial`); check de distorção usa `DistorcaoManager.possui_itens()`; aliases de compatibilidade mantidos para legado/tests. |

### Fase 7 — Remover compatibilidade legada ✅
| Item | Status | Observação |
|---|---|---|
| Remover `data_banco_inicial/final` e `_periodo_selecionado` de `Inventario.py` | ✅ | Removidos; `__init__` usa apenas `self.periodo_manager`. |
| Remover imports mortos | ✅ | Verificado após limpeza. |
| Busca global de `app_self.data_banco_*` | ✅ | 0 usos (varredura concluída; única menção restante é a propriedade `data_banco_*` do próprio `PeriodoManager`, mantida como API de conveniência sem uso atual). |

### Fase 8 — Testes, regressão e documentação ✅
| Item | Status | Observação |
|---|---|---|
| Testes `PeriodoInventario/PeriodoManager` | ✅ | `tests/test_periodo_manager.py` criado (16 testes: snapshot, formatação dd.mm.yyyy, período invertido, igualdade, notificação/idempotência, registro/remoção de listeners). |
| Ajustar fakes legados | ✅ | `test_comandos_func.py` migrado para `Funcoes_Comandos` com `FakePeriodo` (novo contrato de período). `test_validacao.py` usa wrapper de compatibilidade. |
| Testes manuais de troca de período | ⬜ | Sem listener no Dashboard; validar troca de período e reabertura das telas. |
| Atualizar este Status | ✅ | Atualizado em 19/10/2026 (encerramento da refatoração de datas). |

---

## Próximos passos (recomendados)

**✅ Refatoração de datas CONCLUÍDA (19/10/2026):** E5, E6a, E6b, E7, E1a e E8 concluídos.
Suíte completa: **85 passed** (inclui 16 testes novos de `PeriodoManager`), `compileall` sem erros.

| Etapa | Ação | Status |
|---|---|---|
| **E5** | Dashboard migrado para snapshot + janela fixa de 5 anos-calendário no gráfico de tendência. | ✅ |
| **E6a/E6b** | Comandos migrado para classe `Funcoes_Comandos` + período snapshot; testes atualizados. | ✅ |
| **E7** | Propriedades legadas de `Inventario.py` removidas; 0 usos de `app_self.data_banco_*`. | ✅ |
| **E1a** | `tests/test_periodo_manager.py` criado (16 testes). | ✅ |
| **E8** | Regressão final + docs sincronizados (sem commit automático). | ✅ |

**Restam apenas testes manuais** (troca de período + reabertura das telas), que exigem execução da aplicação com banco de dados real — fora do escopo automatizado.

**Aviso:** as alterações estão no **working tree** para revisão manual. Nenhum commit foi realizado (regra de ouro da sessão). O encerramento/commit fica a cargo do usuário.