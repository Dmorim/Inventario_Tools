# Status da Refatoração — Inventario_Tools

**Documento atualizado em:** 26/10/2026  
**Branch de trabalho:** `refatoracao_v3.5`  
**Base do plano:** `docs/Plano_Refatoracao_Inventario_Tools_v2.md` (v5.1)  
**Últimos commits:** `3d7d9ef` ("Harden dashboard and thread workflows"), `02afd20` ("Harden dashboard and thread lifecycle"), `0c43604` ("Harden view cleanup and chart rendering"), `a503daa` ("Unify dashboard entry value calculations")  
**Working tree:** o trabalho de 23/10/2026 foi **commitado pelo usuário** em `3d7d9ef`. Nesta
sessão (26/10/2026) o working tree contém: `requirements.txt` (`numpy`/`scipy` explícitos),
`AGENTS.md`, `AGENTS_SESSAO.md`, este documento e `docs/Mapeamento_Refatoracao_Datas.md`
(sincronia de status); `tests/test_periodo.py` + **novos** `tests/test_dashboard_func.py` e
`tests/test_dashboard_screen_helpers.py` (testes dos helpers puros do Dashboard);
`Dashboard/Dashboard_Screen.py` e `Dashboard/Dashboard_Charts.py` (logging nos `except` de UI +
remoção de código morto no tooltip), além das **edições do usuário** em `Dashboard_Screen.py`
(rótulo "Carregando dados..." escondido ao atualizar os cards) e em `Queries/Consulta_Queries.py`
(`'03'` incluído no universo de `QUERY_DISTORCAO_SALDO`). `config.ini` **desrastreado** em
`a503daa` + `.gitignore` limpo (duplicatas removidas).

> **Decisões registradas (fora de escopo da refatoração):**
> - **SQL Livre (`com_ger`)** — ficará em total responsabilidade do operador. **Não** será aplicada whitelist nem qualquer validação programática. Apenas confirmação com aviso de risco.
> - **Type Hints (Fase 4 / `py.typed`)** — a refatoração **não** cobrirá mais o uso de type hints.

> Este documento verifica o que já foi realizado e lista o que ainda falta, item a item, conforme o plano de refatoração. Legenda: ✅ concluído · 🔄 em andamento/parcial · ⬜ pendente.

---

## Visão geral do progresso

- **Fase 0 (Preparação)** — ✅ concluída.
- **Fase 1 (Segurança e Configuração)** — ✅ concluída (queries parametrizadas, credenciais em config, AppConfig centralizada).
- **Fase 2 (Eliminar Código Duplicado)** — ✅ concluída (funções unificadas, factories de tela e listagem).
- **Fase 3 (Arquitetura e Organização)** — ✅ concluída (imports no topo, hardening de threads, logging estruturado — diretiva revisada em 23/10/2026: log único no início da função, sem par entrada/saída).
- **Fase 4 (Type Hints)** — ❌ fora de escopo (decisão do usuário).
- **Fase 5 (Testes Unitários)** — ✅ **183 testes passando** em 15 arquivos: `test_comandos_func` 12, `test_copy_val` 4, `test_create_views` 5, `test_dashboard_charts` 31, `test_dashboard_func` **23**, `test_dashboard_screen_helpers` **17**, `test_distorcao` 10, `test_formatacao` 4, `test_gerenciador_thread_bd` 10, `test_periodo` 16, `test_periodo_manager` 16, `test_queries` 3, `test_query_operations` 12, `test_thread_executor` 10, `test_validacao` 10. Queries centralizadas cobertas por contrato nominal; pool de BD adicionado aos testes.
- **Fase 6 (PyInstaller)** — ⬜ **sem receita de build válida**: não existe `*.spec`, `build/` nem `dist/` no repositório (o `.gitignore` ignora `*.spec`, `build/`, `dist/`, `*.exe`), então o empacotamento nunca foi validado. Existe `Outros/Auto_py_to_exe config.json`, mas ele está **obsoleto**: caminhos absolutos de outra máquina (`C:/Users/Sup-12/...`), não inclui `Dashboard/`, `Queries/`, `Thread_Manager/`, `Data_Manager/`, `Distorcao_Manager/`, `Inv_Screen/`, `Interface_Tools/`, nem `config.ini`/`Recursos/Firebird/fbclient.dll`, e usa `collect_all` em módulos da stdlib (`base64`, `io`, `datetime`, `ctypes`).
- **N1–N9 (Novos Problemas)** — ✅ 9/9 corrigidos (inclui N4 com health-check).
- **Refatoração de Datas (PeriodoManager)** — ✅ **concluída**: modelo (`PeriodoInventario/PeriodoManager`) pronto e com testes (`tests/test_periodo_manager.py`), Top Frame integrado ao manager, telas de consulta/Comandos/Dashboard migradas para snapshot de período; legado `data_banco_*` removido de `Inventario.py`. Gráfico de tendência do Dashboard com janela fixa de 5 anos-calendário.

## 5. Checklist de Migração (anexo ao Mapeamento de Datas) — Status de Execução

Conforme `docs/Mapeamento_Refatoracao_Datas.md` (Item 5), execução em andamento:

- [x] **Mapeamento completo** — Cruzar cada grupo com Plano v2 (checklist de fases) e atualizar `Status_Refatoracao.md` *(executado neste item)*.
- [x] **Eliminação residual** — Garantir que grupos pendentes não calculem `dt_ini`/`dt_fim` localmente (zero resíduos confirmado por varredura).
- [x] **Migrar 6 grupos pendentes**: Classificação, Preço Custo Compra Zerado, Preço Custo Maior PV, Preço Custo Zerado, Produtos Não Zerados, Valor Inventário *(analisados — sem uso de dt_ini/dt_fim; verificação estrutural realizada; migração controlada por padrão já aplicado)*.
- [x] **Revisar parciais**: Valor Entradas/Vendas/`Consultas_Screen` — confirmado consumo via `periodo` (snapshot) e passagem correta para telas migradas.
- [x] **Padronizar prefetch** — Avaliado: Lists pendentes existem para alguns grupos; padrão prefetch já aplicado nos migrados. Aplicação pontual não necessária neste momento (sem resíduos detectados).
- [x] **Testes**: Verificado `tests/test_periodo.py` cobre o período de tendência (4 casos novos na sessão de 26/10/2026); a suíte completa está em **183 passed** (ver Fase 5). `compileall` sem erros.
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
| Visual do gráfico de tendência | ✅ | `d81b381` entregou a base (figura responsiva, paleta/ordem das séries, vendas negativas, `tight_layout`); complementado em `Dashboard/Dashboard_Charts.py`: eixo Y formatado em pt-BR compacto (`R$ 1,9 mi`, `R$ 500 mil`), valores anotados nas barras (≤ 12 pontos), rareamento dos rótulos do X (61 meses → 16, preservando o último), estado vazio e figura/eixos/grade **por tema** e `set_layout_engine('tight')` para re-aplicar o layout a cada draw (inclusive no resize). **Correção de contraste (mesma sessão):** o texto claro do gráfico tinha contraste insuficiente contra as cores das séries (1,50 / 2,26 / 2,74 — ilegível na legenda e nos rótulos de valores); texto passou a neutro (`#ecf0f1` dark / `#212d38` light), a legenda ganhou **moldura opaca** na cor da figura e os rótulos de valores ganharam **caixa de fundo** — contraste agora ≥ 11,9:1, garantido por teste automatizado (WCAG). Coberto por `tests/test_dashboard_charts.py` (22 testes). **Entregue ao usuário no commit `9100308`.** Em 23/10/2026 (Item 8.8): **legenda movida para fora da área de plotagem** (faixa horizontal acima, `ncol=3`) para não cobrir os rótulos de valor e **rótulos de valor também no modo Linhas** (posicionamento anticolisão, ≤ 12 pontos); testes parametrizados para Barras/Linhas + `test_legenda_nao_cobre_rotulos_de_valor` (**28 testes** no arquivo). |
| Divergência KPI "Total de Entradas" × série "Entradas" do gráfico (22/10/2026) | ✅ | **Causa:** fórmulas SQL diferentes — o KPI usava `QUERY_ENTRADAS` (`(valor − desconto) × **quant** + `valsub` + IPI`) e o gráfico usava `SUM(l.valor)` (valor **unitário**, sem quantidade) → 951.529,18 × "278 mil" em 2025. **Não era divergência de período.** **Correção aplicada:** a expressão virou `EXPR_VALOR_ENTRADA` (fonte única) em `Queries/Consulta_Queries.py`, usada por `QUERY_ENTRADAS` **e** pelas duas queries de tendência do Dashboard; caso anti-regressão em `tests/test_queries.py`. **Validado no banco:** KPI = barra do gráfico (Ano) = soma dos meses em 2024 (703.596,11), 2025 (**951.529,18**) e 2026 jan–set (597.393,68); desempenho inalterado (0,08 s/ano; 0,28 s na janela de 5 anos). Suíte: **108 passed**. Efeito colateral: a série "Diferença" de 2025 passa de −1.334.528,84 para **−661.164,35** (mais equilibrada frente às vendas). |
| Varredura de casos semelhantes (22/10/2026) | ✅ | **Sem divergência:** KPI × tela em Inventário/Vendas/Entradas (mesma query), KPI Vendas × gráfico (1.612.693,53 = 1.612.693,53), `dtcom` × `dtpro` nas entradas (280.611,25 = 280.611,25), view `V_FAT_VALOR_SAIDA` do banco × fórmula do código, e os 6 pares query-de-contagem × query-de-listagem (filtros semanticamente iguais). **Divergências latentes (medidas em 5 bancos de cliente):** classe `'03'` → **0 produtos** em todos (divergência teórica, impacto zero); `QUERY_ENTRADAS` não filtra `l.cance` → **0 linhas** canceladas em 2024/2025/2026 (diferença 0,00, sem ação); classe `'07'` → **existe nos 5** (37–187 produtos; 12–43 com saldo > 0) e está fora das **duas** listas → o inventário **subestima** (+0,13% … **+6,86%**) e a distorção **ignora** divergências (até **61%**); novas classes `'08'`/`'10'`/`'99'` também fora dos universos. Detalhes em `AGENTS_SESSAO.md` Itens 9.5/9.6. |
| Rótulos de valor do gráfico — margem de eixo Y (22/10/2026) | ✅ | **Medição (render Agg, sem display):** o tweak `fontsize` 6 → 8 do usuário **não** gera sobreposição nem estouro lateral, mas amplifica um defeito pré-existente — 4–8 rótulos **cortados** (topo 2,1–3,9 px; base 1,5–3,4 px). **Correção aplicada (Plano A):** `MARGEM_Y_ROTULOS = 0.12` + `ax.margins(y=…)` no ramo "Barras" (só quando há rótulos, ≤ 12 pontos) → corte **zerado**; `fontsize=8` mantido. O desenho das séries foi extraído para `_desenhar_series()` (sem Tk), permitindo **teste de regressão com render Agg** (`TestRotulosDeValor`, 6 casos: sem corte, sem colisão, ausência de rótulos > 12 pontos, margem aplicada, modo "Linhas" sem margem). Teste validado: sem a margem, `test_rotulos_de_valor_nao_sao_cortados` **falha**. Suíte: **108 passed**. Em 23/10/2026 (Item 8.8) o modo **Linhas** passou a aplicar a mesma margem e a exibir rótulos (teste substituído por `test_margem_de_rotulos_aplicada_no_modo_linhas`). |
| Erro `-607` ao fechar a app + robustez do encerramento (22/10/2026) | ✅ | **Causa raiz provada** via `RDB$VIEW_RELATIONS` (consultável neste banco, FB 3.0.5): a view órfã `V_DIFF_ENTRADA_SAIDA_MES` **depende** de `V_FAT_VALOR_SAIDA` (coluna `FATUR`) → o Firebird recusava o `DROP VIEW V_FAT_VALOR_SAIDA` feito no encerramento. **Resolvido no banco pelo usuário** (a view foi dropada; `V_LAN_COM` segue órfã, mas não bloqueia). **3 mudanças aplicadas** (aprovadas — só as que afetam o *encerramento*): (1) `Queries/Create_Views.py` — falha tratada **por view** (`rollback` isolado + `logger.exception`) e **relance da primeira exceção original** (uma view travada não impede as demais; o `-607` não é silenciado); (2) `Inventario.py` — o `finally` do `__main__` não é mais interrompido por DDL (`try/except` + `BancoDeDados.fechar()` → o pool **e** o log "Aplicação encerrada." sempre executam; antes as 8 conexões Firebird ficavam abertas); (3) `tests/test_create_views.py` (novo, **5 casos**, fakes puros) — os 3 casos de resiliência **falham** com o código antigo (validado) e passam com o novo. **Não aprovado / inalterado:** o fluxo de **reconexão** (item 2b — hoje mostra errorbox e não reconecta). Detalhes em `AGENTS_SESSAO.md` Item 6.11. |
| Ciclo de vida (dashboard + threads + pool) — `02afd20` (23/10/2026) | ✅ | **Commit do usuário** ("Harden dashboard and thread lifecycle"): (1) `Dashboard_Screen.py` — abertura/fechamento protegidos (`grab` reaplicado de forma segura via `_aplicar_grab_seguro`, `_fechar_dashboard_seguro` libera `grab` + reabilita o botão + destrói a janela), callbacks que checam `winfo_exists()`, KPIs com `kpis.get(...)` e mensagens de erro controladas; (2) `Thread_Manager/Thread_Executor.py` — flag de cancelamento (`cancelado`), checagem de `master` antes/depois de `func`, `_safe_schedule_ui` revalida o widget **dentro** do callback agendado e loga em `debug` quando a UI já não existe, callback de polling 100 ms → **75 ms**; (3) `Thread_Manager/Gerenciador_Thread_BD.py` — `_pegar_conexao` recusa trabalho quando `_fechando` está ativo (inclusive após descartar conexão inválida), `_devolver_conexao` e o decremento de `_operacoes_ativas` não derrubam o `finally`, `time.sleep(0.02)` entre tentativas. **Cobertura acrescentada em 23/10/2026:** `tests/test_thread_executor.py` (**novo**, 10 casos: agenda segura, cancelamento por `winfo_exists()`, resultado/erro via callback, janela destruída) e +7 casos em `tests/test_gerenciador_thread_bd.py` (recusa com `_fechando` — inclusive durante o descarte de conexão inválida —, propagação de erro com contador zerado, devolução ao pool, falha na devolução não derruba o `finally`, `fechar()` fecha o pool). Suíte: **136 passed**. Também em 23/10/2026: removido o código morto `_fechar_dashboard` (`Dashboard_Screen.py`, sem uso). |
| Recursos do `3d7d9ef` — KPI comparativo, curvas suaves, toolbar e tooltip (26/10/2026) | ✅ | **Commit do usuário** ("Harden dashboard and thread workflows"), criado depois da sessão de 23/10/2026, continha **4 recursos não documentados** (descobertos na varredura de 26/10/2026): (1) **KPI comparativo** — `carregar_kpis(ini, fim, ini_ant, fim_ant)` (com `_calcular_kpis`) devolve tupla e cada card mostra **"±x,x% vs período anterior"** (`_periodo_anterior` = mesma duração, terminando no dia anterior ao início do período atual); (2) **curvas suavizadas** no modo Linhas (`_curva_suave` com `scipy.interpolate.make_interp_spline`, 200 pontos), mantendo marcadores/legenda sobre os dados originais; (3) **`NavigationToolbar2Tk`** embaixo do gráfico; (4) **tooltip** (`adicionar_tooltip`) mostrando o valor sob o cursor. **Correção de ambiente (26/10/2026):** `numpy`/`scipy` viraram imports diretos e o `scipy` **não estava** na `.venv` nem no `requirements.txt` → o import de `Dashboard_Charts` falhava (tela do Dashboard) e o `pytest` abortava na coleta; `scipy 1.18.1` instalado e ambos declarados no `requirements.txt`. Baseline revalidada: **139 passed** (31 casos em `test_dashboard_charts.py`), `compileall` limpo. Detalhes em `AGENTS_SESSAO.md` Item 8.9. |
| Item 9.5 — universos de classificação e filtro de cancelamento (22/10/2026) | ✅ | **Item 9.7 DESCARTADO pelo usuário em 23/10/2026** (informou que já foi solucionado): (a) os dois universos de classificação (`QUERY_INVENTARIO` × `QUERY_DISTORCAO_SALDO`) devem ser **iguais** — `'03'` entra na distorção; (b) `'07'` = produtos de **uso e consumo** → fica **fora** dos dois cálculos (e `'08'`/`'10'`/`'99'` também); (c) as queries de **entradas** passam a filtrar `l.cance` (consistência com a distorção). **Impacto medido em 5 bancos cliente (só SELECT): 0,00** — nenhuma mudança numérica hoje (classe `'03'` = 0 produtos; 0 compras canceladas). O diff registrado **não foi aplicado pelo agente**; permanece só como histórico em `AGENTS_SESSAO.md` Item 9.7. |

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
| Atualizar este Status | ✅ | Atualizado em 26/10/2026 (varredura de abertura: HEAD `3d7d9ef`, working tree limpo — o trabalho de 23/10/2026 foi commitado pelo usuário; restaurada a baseline com `scipy` instalado/declarado — **139 passed**; documentados os 4 recursos do `3d7d9ef` — KPI comparativo, curvas suaves, toolbar e tooltip). Registro anterior (23/10/2026): robustez de ciclo de vida do `02afd20`, 17 testes novos (`Thread_Executor` 10 + `GerenciadorThreadBD` 7), remoção do código morto `_fechar_dashboard`, transição de logging (Item 6.2), legenda fora da área + rótulos no modo Linhas (Item 8.8) e descarte do Item 9.7. **Atualização do fim da sessão (26/10/2026):** itens 1 (testes dos helpers do Dashboard, **183 passed**) e 4 (logging nos `except` da UI do Dashboard) aplicados, B3 (código morto do tooltip) removido e distorções do `docs/Plano_*.md` corrigidas — ver "Próximos passos". |

---

## Próximos passos (recomendados)

**✅ Refatoração de datas CONCLUÍDA (19/10/2026):** E5, E6a, E6b, E7, E1a e E8 concluídos.
Suíte completa: **183 passed** em 15 arquivos (detalhamento na Fase 5), `compileall` sem erros.

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

**Gráfico de tendência — vendas para cima (decisão do usuário, 22/10/2026, Item 8.7):** o usuário editou `Dashboard/Dashboard_Charts.py` (rótulos do eixo X: `fontsize` 7 → **9**, `rotation` 45 → **0**, `ha` 'right' → **'center'**) e `Dashboard/Dashboard_Screen.py` (cores dos KPI cards) e passou a desenhar as **vendas para cima, com valor positivo** — decisão deliberada, tomada após rever o gráfico (o comportamento antigo de vendas negativas foi substituído). **Consequência medida:** com as três séries no mesmo hemisfério, os rótulos de valor de meses vizinhos se encostavam (**7,98 px × 7,81 px**) no tamanho **mínimo** da janela (no tamanho padrão não havia colisão). **Correção APLICADA:** a fonte dos rótulos de valor passa a ser adaptada à densidade do gráfico (`_fonte_rotulos_valor`: 8 até 8 pontos; 6 no tamanho mínimo com 12 pontos) → sobreposição **0 px**, **sem alterar o visual no tamanho padrão**. Suíte: **113 passed**.

**Decisões de negócio — Item 9.7 DESCARTADO pelo usuário em 23/10/2026 (considerado solucionado), com
estado revisado em 26/10/2026:** **(a) aplicado pelo usuário em 26/10/2026** — `QUERY_DISTORCAO_SALDO`
passou a incluir `'03'`, então os dois universos são agora **idênticos** (`'00'`–`'06'`);
**(b) nada a fazer** — as duas listas já terminam em `'06'`, portanto `'07'` (uso e consumo),
`'08'`, `'10'` e `'99'` permanecem **fora** dos dois cálculos; **(c) não aplicado** — `QUERY_ENTRADAS`
(`Queries/Consulta_Queries.py:54-69`) e as duas queries de tendência do Dashboard seguem **sem**
`COALESCE(l.cance, 'N') = 'N'` (a distorção filtra em `:221`). Impacto medido nos 5 bancos cliente:
**0,00** (0 compras canceladas no período), por isso não foi alterado. Detalhes em
`AGENTS_SESSAO.md` Item 9.7.

**Gráfico — legenda e rótulos no modo Linhas (23/10/2026, Item 8.8):** a legenda saiu da área de plotagem (faixa horizontal acima, `ncol=3`, título com `pad=32`) e deixou de cobrir rótulos de valor; o modo **Linhas** passou a exibir rótulos com posicionamento anticolisão (≤ 12 pontos). Medição: 0 sobreposições/cortes em 5/7/12 pontos × 2 tamanhos × 3 conjuntos de dados × 2 tipos. Testes: `tests/test_dashboard_charts.py` com **31 casos** (parametrizados Barras/Linhas + `test_legenda_nao_cobre_rotulos_de_valor`). Suíte: **139 passed**.

**Recursos do `3d7d9ef` documentados em 26/10/2026:** o commit do usuário inclui **KPI comparativo** ("±x,x% vs período anterior"), **curvas suavizadas** no modo Linhas (`scipy.interpolate.make_interp_spline`), **barra de ferramentas** do matplotlib e **tooltip** sob o cursor. A varredura de abertura encontrou a baseline **quebrada** porque o `scipy` não estava instalado na `.venv` nem declarado no `requirements.txt` (o `pytest` abortava na coleta e a tela do Dashboard não importava); corrigido com `scipy 1.18.1` + `numpy`/`scipy` no `requirements.txt` e revalidado com **139 passed**. Detalhes em `AGENTS_SESSAO.md` Item 8.9.

**Testes e logging do Dashboard (26/10/2026, itens 1 e 4 das pendências):** a capa de dados do Dashboard deixou de ser não testada. Foram adicionados **44 testes**: `tests/test_dashboard_func.py` (23 — `_extrair_series`, `_previa_inventario`, `_calcular_kpis`, `carregar_kpis`, `carregar_dados_tendencia`, com `_executar_select`/`_executar_consulta`/`_previa_inventario`/`_calcular_kpis` mockados — **nenhum acesso ao Firebird**), `tests/test_dashboard_screen_helpers.py` (17 — `_periodo_anterior`, `_formatar_variacao`) e **4 novos** casos de `periodo_tendencia_ultimos_5_anos` em `tests/test_periodo.py` (agora 16). No **item 4**, os `except` silenciosos da UI passaram a registrar `logger.debug(..., exc_info=True)` com mensagem específica: **24** pontos em `Dashboard/Dashboard_Screen.py` e **10** em `Dashboard/Dashboard_Charts.py` (0 `pass` soltos restantes nos dois arquivos). Como o nível padrão do logger é `INFO`, o comportamento visível **não muda** — as mensagens só aparecem com `INVENTARIO_LOG_LEVEL=DEBUG`. **B3 aprovado e aplicado:** removido o cálculo morto (`px`, `py`, `dist` via `np.hypot`) do tooltip do gráfico. Vale registrar a inconsistência visual **mantida de propósito**: `_formatar_variacao` imprime ponto decimal (`'+50.0%'`), enquanto os valores usam vírgula — os testes fixam o comportamento atual. Suíte: **183 passed** em 15 arquivos; `compileall` OK. **Não commitado.**

**Decisão de negócio aplicada pelo usuário (`'03'` na distorção, 26/10/2026):** `QUERY_DISTORCAO_SALDO` passou a incluir `classificacao_produto = '03'`, alinhando o universo com `QUERY_INVENTARIO` (`'00'`–`'06'` em ambas).

**KPI "Previsão de Inventário" redefinido (26/10/2026, plano aprovado):** o KPI deixou de ser `inventário − Δ|compras − vendas|` entre anos-calendário e passou a ser uma **estimativa do inventário no fim do período selecionado**: `inventário_base + Σ(quant × precu)` com sinal por `l.tpmov` (`'S'` entra: compras, devoluções de venda e transferências de entrada; as demais saem: vendas, devoluções ao fornecedor e ajustes), via `QUERY_MOVIMENTO_ESTOQUE_CUSTO`. Usa o **mesmo custo (`precu`) e o mesmo universo de classificação** de `QUERY_INVENTARIO`; premissa do usuário: base do cliente com inventário **normalizado para o ano base** (o snapshot é tratado como valor na **data inicial** do período). Diagnóstico medido no banco cópia: a fórmula antiga oscilava **1,8 M** (3.696.805,72 com `fim=31.12.2025` → 5.521.718,82 com `fim=30.09.2026`), misturava custo de nota (`in01com.valno`) com preço de venda (`V_FAT_VALOR_SAIDA`) e usava `SUM(ABS(...))`. Reconciliação do novo critério no histórico completo: movimento a custo atual **4.156.492,44** × saldo **4.207.242,01** (diferença = estoque inicial de fev/2021). Previsões no banco cópia: 2024 = **4.647.236,00**; 2025 = **4.559.194,73**; 2026 jan–set = **4.409.961,27**. Custo da query: **23–28 s → 3,4–13,1 s**, e o período anterior não calcula mais a previsão (`_calcular_kpis(..., incluir_previa=False)`). O card perdeu o selo "vs período anterior" (subtexto fixo "estimativa do período"). `QUERY_DIFERENCA_ANO_ANTERIOR_ATUAL` foi **removida**. Testes: `TestPreviaInventario` reescrito (7 casos) + cobertura de `incluir_previa`; suíte **203 passed** em 16 arquivos; `compileall` OK. **Não commitado.**

**Distorções documentais corrigidas (26/10/2026):** o `docs/Plano_Refatoracao_Inventario_Tools_v2.md` estava congelado em 13/10/2026 (v5.1, commit `e2c46ce`, "59 testes"). Foi atualizado para v5.2 (HEAD `3d7d9ef`, **183 testes**): Fase 3.1 (imports) marcada como **concluída** (0 imports lazy no app), Fase 3.3 com o estado real do logging (Dashboard feito; **17 `except: pass`** restantes em 8 arquivos), Fase 5.2/5.3 como **completas** (tabela de testes por arquivo; contrato das 20 consultas/14 comandos), Fase 6 corrigida (existe `Outros/Auto_py_to_exe config.json`, mas **obsoleto** — caminhos `C:/Users/Sup-12`, sem `Dashboard/`/`Queries/`/`fbclient.dll`/`config.ini`, `collect_all` em módulos da stdlib), §5.4/§5.8 (`trocar_bd` **já removido**; pendente só o `DROP VIEW` físico de `V_LAN_COM`/`V_DIFF_ENTRADA_SAIDA_MES`), Feature 1 (Dashboard **implementado**, com a ressalva de que o indicador de "saúde do banco" da proposta **nunca** foi feito), Feature 2 (módulo `Validacao/` **não existe**), roadmap/horas (18,5–20,5 h → **9,5–10,5 h**) e §8 (matplotlib/numpy/scipy **declarados**; `fpdf2` **não usado**).

**Fica em aberto (Item 9.7 — DESCARTADO em 23/10/2026):** a dúvida sobre o filtro `l.cance` na CTE `entradas` da `QUERY_DIFERENCA_ANO_ANTERIOR_ATUAL` (KPI "Previsão de Inventário") — é a **3ª noção** de entradas (usa `c.valno`, não `EXPR_VALOR_ENTRADA`); a CTE `saidas` já filtra `COALESCE(vs.cance,'N')='N'`, então a mudança seria por simetria. **Impacto medido: 0,00** (a CTE foi medida isolada nos 5 bancos cliente, porque a query completa depende da view temporária `V_FAT_VALOR_SAIDA`). O usuário descartou o item; **nenhuma alteração foi feita**.

**Fila de ideias para sessões futuras (26/10/2026):** registrado em `AGENTS_SESSAO.md` **Item 10.1** — *avaliar* a paralelização das consultas do Dashboard em threads separadas. Apuração: **KPIs e tendência já rodam em duas threads distintas** (uma `threading.Thread` por `thread_execução`) e o pool de conexões já suporta concorrência; o que **não** é paralelo são as consultas **dentro** de cada bloco (`_calcular_kpis` = 4 consultas sequenciais, ×2 com o KPI comparativo; `carregar_dados_tendencia` = 2). Nada foi alterado; a sessão futura deve **medir antes** (a `previa` é I/O do servidor — Item 6.8). *(Atualização 26/10/2026: com a previsão só no período atual, são **7 consultas sequenciais** no total, 1 pesada.)*

**Segurança (Item 6.10):** o `config.ini` foi **desrastreado e commitado** pelo usuário (`git rm --cached config.ini` + commit `a503daa`; arquivo mantido localmente, agora respeitando o `.gitignore`), com o `.gitignore` limpo de duplicatas. **Rotação da senha do banco segue pendente** — as credenciais continuam no histórico do repositório.

**Aviso:** as sessões anteriores foram commitadas **pelo usuário** na branch `refatoracao_v3.5` (HEAD `3d7d9ef`; working tree estava **limpo** no início da sessão de 26/10/2026). O agente da sessão **não commita** (regra de ouro) — as alterações desta sessão (`requirements.txt`, `AGENTS.md`, `AGENTS_SESSAO.md`, docs de status, `Dashboard/Dashboard_Charts.py`, `Dashboard/Dashboard_Screen.py`, `tests/test_periodo.py` e os **dois arquivos novos de teste**) ficam no working tree para revisão manual, além das edições do usuário em `Dashboard_Screen.py` e `Queries/Consulta_Queries.py`.