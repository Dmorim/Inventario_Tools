# Status da Refatoração — Inventario_Tools

**Documento atualizado em:** 22/10/2026  
**Branch de trabalho:** `refatoracao_v3.5`  
**Base do plano:** `docs/Plano_Refatoracao_Inventario_Tools_v2.md` (v5.1)  
**Últimos commits:** `9100308` ("Improve dashboard chart readability"), `d81b381` ("Improve dashboard trend chart visuals"), `e7d479f` ("Optimize Dashboard database queries")  
**Working tree:** `config.ini` **desrastreado** (`git rm --cached`, staged) + `.gitignore` limpo (duplicatas removidas) — **sem commit** (regra de ouro da sessão)

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
- **Fase 5 (Testes Unitários)** — ✅ 102 testes passando (69 originais + 16 de `PeriodoManager` + 16 de `Dashboard_Charts` + 1 de contrato das queries de entradas); queries centralizadas cobertas por contrato nominal; pool de BD adicionado aos testes.
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
| Propriedades legadas `data_banco_*` | ✅ | Removidas na Fase 7 — `Inventario.py` usa apenas `self.periodo_manager`. |

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
| Desempenho das queries (20/10/2026) | ✅ | Diagnóstico por script temporário (fora do repo, só SELECTs). Gargalos: `V_LAN_COM` (LEFT JOIN forçava scan de `in01lan` — 1,03 M linhas) e `V_DIFF_ENTRADA_SAIDA_MES` (agregava o histórico inteiro). Correção: join direto `in01lan`/`in01com` em `QUERY_ENTRADAS` + tendência e pushdown do filtro de ano na diferença. Resultados idênticos aos anteriores; KPI entradas 7,5 s→0,04 s, tendência 8,5 s→0,04 s, diferença 11,7 s→1,3 s. |
| Caça à performance encerrada (21/10/2026) | ✅ | Medição pós-otimização (só SELECTs; banco = cópia de cliente) provou que **não há correção de SQL de alto retorno restante**: os ~20 s do `KPI previa` são I/O, não defeito de query. Duas hipóteses testadas e derrubadas: (a) filtrar a CTE `saidas` fica mais lento (23,05 s vs 20,86 s) **e muda o KPI** — descartado; (b) o join `s.fatur = e.notfi` **não** explode (`fatur` repetido = 0; pares = 111.757; fan-out máx. = 1). Evidência de I/O: `in01fat COUNT` 15,13 s frio → 0,17 s morno (89x). Alavancas restantes são **de servidor** (`DefaultDbCachePages = 2048` ≈ 16 MB para arquivo de 1,3 GB; máquina com 3,8 GB de RAM) e compactação do `.fdb` — decisão do usuário. |
| Visual do gráfico de tendência | ✅ | `d81b381` entregou a base (figura responsiva, paleta/ordem das séries, vendas negativas, `tight_layout`); complementado em `Dashboard/Dashboard_Charts.py`: eixo Y formatado em pt-BR compacto (`R$ 1,9 mi`, `R$ 500 mil`), valores anotados nas barras (≤ 12 pontos), rareamento dos rótulos do X (61 meses → 16, preservando o último), estado vazio e figura/eixos/grade **por tema** e `set_layout_engine('tight')` para re-aplicar o layout a cada draw (inclusive no resize). **Correção de contraste (mesma sessão):** o texto claro do gráfico tinha contraste insuficiente contra as cores das séries (1,50 / 2,26 / 2,74 — ilegível na legenda e nos rótulos de valores); texto passou a neutro (`#ecf0f1` dark / `#212d38` light), a legenda ganhou **moldura opaca** na cor da figura e os rótulos de valores ganharam **caixa de fundo** — contraste agora ≥ 11,9:1, garantido por teste automatizado (WCAG). Coberto por `tests/test_dashboard_charts.py` (16 testes). **Entregue ao usuário no commit `9100308`.** |
| Divergência KPI "Total de Entradas" × série "Entradas" do gráfico (22/10/2026) | ✅ | **Causa:** fórmulas SQL diferentes — o KPI usava `QUERY_ENTRADAS` (`(valor − desconto) × **quant** + `valsub` + IPI`) e o gráfico usava `SUM(l.valor)` (valor **unitário**, sem quantidade) → 951.529,18 × "278 mil" em 2025. **Não era divergência de período.** **Correção aplicada:** a expressão virou `EXPR_VALOR_ENTRADA` (fonte única) em `Queries/Consulta_Queries.py`, usada por `QUERY_ENTRADAS` **e** pelas duas queries de tendência do Dashboard; caso anti-regressão em `tests/test_queries.py`. **Validado no banco:** KPI = barra do gráfico (Ano) = soma dos meses em 2024 (703.596,11), 2025 (**951.529,18**) e 2026 jan–set (597.393,68); desempenho inalterado (0,08 s/ano; 0,28 s na janela de 5 anos). Suíte: **102 passed**. Efeito colateral: a série "Diferença" de 2025 passa de −1.334.528,84 para **−661.164,35** (mais equilibrada frente às vendas). |
| Varredura de casos semelhantes (22/10/2026) | ✅ | **Sem divergência:** KPI × tela em Inventário/Vendas/Entradas (mesma query), KPI Vendas × gráfico (1.612.693,53 = 1.612.693,53), `dtcom` × `dtpro` nas entradas (280.611,25 = 280.611,25), view `V_FAT_VALOR_SAIDA` do banco × fórmula do código, e os 6 pares query-de-contagem × query-de-listagem (filtros semanticamente iguais). **Divergências latentes (impacto zero nesta base — aguardando decisão de negócio):** classe `'03'` presente em `QUERY_INVENTARIO` e ausente em `QUERY_DISTORCAO_SALDO`; `QUERY_ENTRADAS` não filtra `l.cance` (0 linhas canceladas aqui); classe `'07'` (51 produtos) fora das duas listas. Detalhes em `AGENTS_SESSAO.md` Item 9.5. |

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
Suíte completa: **101 passed** (69 originais + 16 de `PeriodoManager` + 16 de `Dashboard_Charts`), `compileall` sem erros.

| Etapa | Ação | Status |
|---|---|---|
| **E5** | Dashboard migrado para snapshot + janela fixa de 5 anos-calendário no gráfico de tendência. | ✅ |
| **E6a/E6b** | Comandos migrado para classe `Funcoes_Comandos` + período snapshot; testes atualizados. | ✅ |
| **E7** | Propriedades legadas de `Inventario.py` removidas; 0 usos de `app_self.data_banco_*`. | ✅ |
| **E1a** | `tests/test_periodo_manager.py` criado (16 testes). | ✅ |
| **E8** | Regressão final + docs sincronizados (sem commit automático). | ✅ |

**Restam apenas testes manuais** (troca de período + reabertura das telas), que exigem execução da aplicação com banco de dados real — fora do escopo automatizado.

**Otimização de desempenho do Dashboard (20/10/2026):** identificado que a abertura do Dashboard somava ~31 s (KPIs) + ~8,5 s (tendência). Causa: as views `V_LAN_COM` (LEFT JOIN) e `V_DIFF_ENTRADA_SAIDA_MES` forçavam varredura completa de `in01lan` (1,03 M linhas). Corrigido com joins diretos `in01lan`→`in01com` em `Queries/Consulta_Queries.py` (`QUERY_ENTRADAS`, usada também na tela Valor de Entradas) e em `Dashboard/Dashboard_Func.py` (tendência de entradas, mês/ano), mantendo os parâmetros posicionais. A `QUERY_DIFERENCA_ANO_ANTERIOR_ATUAL` passou a empurrar o filtro de ano para dentro do CTE de entradas (`l.dtpro BETWEEN ? AND ?`), com `_previa_inventario` enviando o intervalo dos 2 anos. Valores conferidos no banco: idênticos aos originais. **Views órfãs removidas:** `V_LAN_COM` e `V_DIFF_ENTRADA_SAIDA_MES` saíram de `Queries/View_Queries.py` e de `Queries/Create_Views.py` (0 referências no código; `V_FAT_VALOR_SAIDA` permanece em uso). As views **físicas** seguem no banco até um `DROP` explícito. Suíte: **85 passed**, `compileall` limpo.

**Visual do gráfico de tendência (21/10/2026):** o commit `d81b381` já entregou parte do item — figura responsiva ao widget hospedeiro (`_dimensoes_figura` em `Dashboard/Dashboard_Charts.py`), paleta/ordenação das séries, vendas representadas como valor negativo e `tight_layout`. O commit `9100308` do usuário fechou o restante (eixo Y compacto pt-BR, valores nas barras, rareamento do X, cores por tema, `set_layout_engine('tight')` e correção de contraste WCAG). **Nada de código pendente nessa frente.**

**Correção pendente de aprovação (22/10/2026) — fórmula de "Entradas" no gráfico:** o KPI "Total de Entradas" e a série "Entradas" do gráfico usavam **fórmulas diferentes** (`QUERY_ENTRADAS` × `SUM(l.valor)`), o que fazia o gráfico exibir 278 mil contra 951.529,18 do KPI em 2025. **Correção APLICADA:** a expressão virou `EXPR_VALOR_ENTRADA` (fonte única de verdade) em `Queries/Consulta_Queries.py`, usada por `QUERY_ENTRADAS` e pelas queries de tendência do Dashboard. Validado no banco (KPI = barra do gráfico = soma dos meses em 2024/2025/2026), com caso anti-regressão em `tests/test_queries.py`. Detalhes em `AGENTS_SESSAO.md` Item 9.

**Decisões de negócio pendentes (22/10/2026) — sem impacto na base atual:** classe `'03'` (está no valor do inventário, não está na checagem de distorção), filtro `l.cance` ausente em `QUERY_ENTRADAS` e classe `'07'` fora do universo do inventário. Detalhes e medições em `AGENTS_SESSAO.md` Item 9.5.

**Segurança (Item 6.10):** o usuário executou `git rm --cached config.ini` (arquivo mantido localmente, agora respeitando o `.gitignore`) e limpou duplicatas do `.gitignore`. **Rotação da senha do banco segue pendente** — as credenciais continuam no histórico do repositório.

**Aviso:** as sessões anteriores foram commitadas **pelo usuário** na branch `refatoracao_v3.5` (HEAD `9100308`). O agente da sessão **não commita** (regra de ouro) — alterações novas ficam no working tree para revisão manual.