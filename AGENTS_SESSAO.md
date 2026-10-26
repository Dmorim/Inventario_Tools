# AGENTS_SESSAO.md — Instruções para Próximas Sessões

**Agente responsável:** **NEXO** (sessão de refatoração de datas / Inventario_Tools)
**Última sessão:** 26/10/2026 — **varredura de abertura + restauração da baseline** (plano
aprovado pelo usuário). O working tree estava **limpo** e o trabalho de 23/10/2026 já havia sido
**commitado pelo usuário** em `3d7d9ef` ("Harden dashboard and thread workflows"). A varredura
achou a baseline **quebrada**: `Dashboard/Dashboard_Charts.py:9` importa `scipy.interpolate`
(`_curva_suave`, suavização do modo Linhas) e o `scipy` **não estava instalado** na `.venv` nem
declarado no `requirements.txt` → `import Dashboard.Dashboard_Charts` falhava (a tela do
Dashboard não abriria) e o `pytest` **abortava na coleta** (`tests/test_dashboard_charts.py`).
**Corrigido:** `pip install scipy` (**1.18.1**) + `numpy` e `scipy` declarados no
`requirements.txt`. Baseline após a correção: **139 passed** e `compileall` limpo
(`tests/test_dashboard_charts.py` tem **31 casos**, não 28). O commit `3d7d9ef` trouxe recursos
que **não** estavam documentados (ver **Item 8.9**): KPI cards com variação **"% vs período
anterior"** (`carregar_kpis(..., ini_ant, fim_ant)` + `_calcular_kpis`), **curvas suavizadas** no
modo Linhas, **barra de ferramentas** do matplotlib e **tooltip** ao passar o mouse. Varredura de
período: **0 resíduos** (`dt_ini`/`dt_fim`/`data_banco_*`).

**Continuação da mesma sessão (26/10/2026) — itens 1 e 4 das pendências (plano aprovado):** depois
da varredura, o usuário aprovou dois itens do relatório da sessão e o **B3**. (1) **Testes dos
helpers puros do Dashboard** — `tests/test_dashboard_func.py` (**novo**, 23 casos: `_extrair_series`,
`_previa_inventario`, `_calcular_kpis`, `carregar_kpis`, `carregar_dados_tendencia`, com banco
**mockado**), `tests/test_dashboard_screen_helpers.py` (**novo**, 17 casos: `_periodo_anterior`,
`_formatar_variacao`) e **+4 casos** de `periodo_tendencia_ultimos_5_anos` em `tests/test_periodo.py`
(arquivo com 16). (2) **Logging nos `except` de UI** — 24 pontos em `Dashboard/Dashboard_Screen.py`
e 10 em `Dashboard/Dashboard_Charts.py` passaram de `pass` para `logger.debug(..., exc_info=True)`
com mensagem específica (**0** `pass` soltos nos dois arquivos); como o nível padrão é `INFO`, o
comportamento visível não muda. (3) **B3** — removido o cálculo morto do tooltip (`px`/`py`/`dist`
via `np.hypot`) em `Dashboard_Charts.py`. Baseline: **183 passed** em 15 arquivos; `compileall` OK.
O usuário aplicou em paralelo `'03'` em `QUERY_DISTORCAO_SALDO` (universos agora idênticos) e o
rótulo `loading_label` no Dashboard. Ver **Item 11**.

**Continuação da mesma sessão (26/10/2026) — KPI "Previsão de Inventário" redefinido (plano
aprovado):** o usuário definiu que o KPI deve ser uma **estimativa do inventário no fim do
período** (opção 2 do diagnóstico) e que o selo "vs período anterior" **sai** do card. Diagnóstico
medido no banco cópia: a fórmula antiga (`inventário − Δ|compras − vendas|` entre
anos-calendário) misturava custo de nota com preço de venda, comparava ano cheio com ano parcial
e oscilava **1,8 M** (3.696.805,72 → 5.521.718,82) só mudando o ano de `fim`. **Nova fórmula:**
`inventário_base + Σ(quant × precu × sinal de l.tpmov)` no período selecionado
(`QUERY_MOVIMENTO_ESTOQUE_CUSTO`) — mesmo custo e mesmo universo de classificação de
`QUERY_INVENTARIO`, com sinal `'S'` = entra (compras, devoluções de venda, transferências de
entrada) e as demais saem. **Premissa do usuário:** base do cliente com inventário **normalizado
para o ano base** (o snapshot é o valor na **data inicial** do período). Validação: movimento
histórico **4.156.492,44** × saldo **4.207.242,01** (diferença = estoque inicial de fev/2021);
previsões no banco cópia: 2024 = 4.647.236,00; 2025 = 4.559.194,73; 2026 jan–set = 4.409.961,27.
**Custo:** 23–28 s → **3,4–13,1 s** e **1 chamada** por carga (o período anterior usa
`_calcular_kpis(..., incluir_previa=False)`, pois o KPI não é mais comparado). Removida a
`QUERY_DIFERENCA_ANO_ANTERIOR_ATUAL`. Testes: `TestPreviaInventario` reescrito (7 casos),
`incluir_previa` coberto em `_calcular_kpis`/`carregar_kpis`. Baseline: **203 passed** em 15
arquivos; `compileall` OK. **Commitado pelo usuário em `56093b1`.** *(A premissa do "inventário
normalizado para o ano base" foi **contestada por medição** em 26/10/2026 — ver Item 10.2; a falha
silenciosa da consulta foi corrigida no **Item 12 (B2)**.)*

**Sessão anterior:** 23/10/2026 — **varredura de abertura** (somente leitura + sincronia de
docs) seguida de **limpeza de código morto + testes de threads/pool** (plano aprovado pelo
usuário). No início da sessão o working tree estava **limpo** e o trabalho das sessões
anteriores já havia sido **commitado pelo usuário** em `0c43604` ("Harden view cleanup and
chart rendering") e `02afd20` ("Harden dashboard and thread lifecycle"). Baseline confirmada:
**113 passed** no início; **130 passed** após os testes novos, `compileall` sem erros;
**136 passed** após a correção do gráfico (23/10/2026); **139 passed** após o refinamento
dos rótulos (barras verticais + halo nas linhas, mesma data).
O commit `02afd20` (não documentado até então) endureceu o ciclo de vida:
(1) `Dashboard_Screen.py` — abertura/fechamento protegidos, `grab` reaplicado por
`_aplicar_grab_seguro`, `_fechar_dashboard_seguro` (libera `grab` + reabilita o botão +
destrói), callbacks com `winfo_exists()` e KPIs via `kpis.get(...)`; (2) `Thread_Executor.py`
— flag `cancelado`, checagem de `master` antes/depois de `func`, revalidação do widget dentro
do callback agendado, polling 100 ms → **75 ms**; (3) `Gerenciador_Thread_BD.py` —
`_pegar_conexao` recusa trabalho com `_fechando`, falha ao devolver conexão não derruba o
`finally`, `sleep(0.02)` entre tentativas. **Cobertura automatizada acrescentada em 23/10/2026:**
`tests/test_thread_executor.py` (**novo**, 10 casos — agenda segura, cancelamento por
`winfo_exists()`, resultado/erro via callback, janela destruída) e +**7 casos** em
`tests/test_gerenciador_thread_bd.py` (recusa com `_fechando`, descarte durante fechamento,
propagação de erro com contador zerado, devolução ao pool, falha na devolução não derruba o
`finally`, `fechar()` fecha o pool). Suíte: **130 passed**. O código morto `_fechar_dashboard`
(`Dashboard_Screen.py`) foi **removido** (não tinha uso). **Transição de logging (23/10/2026,
diretiva nova do usuário):** os logs de **resultado** (`info`/`debug` de sucesso) deixaram de
ficar no fim da função e passaram a ser **um único log no início**, no presente, anunciando a
operação (mesmo nível e mesmo contexto); o log de conclusão da mesma função foi **removido**
(sem par entrada/saída). Exceções permanecem no `except`; `warning`/`error` de condição
detectada permanecem no ponto de detecção; loops que logavam por item (views) passaram a logar
**1×**; nenhuma linha de log foi adicionada (conversão 1:1 — contagem inalterada). Detalhes em
**Item 6.2** (reescrito). **Gráfico do Dashboard (23/10/2026):** a legenda saiu da área de
plotagem (faixa horizontal acima do gráfico, `ncol=3`) e deixou de cobrir os rótulos de valor;
o **modo Linhas** passou a exibir rótulos de valor com posicionamento anticolisão; os rótulos
das **barras** passaram a ser **verticais (90°)** com folga automática no eixo Y (não cobrem
mais as barras vizinhas) e os das **linhas** usam **fonte 8 com halo**. Suíte:
**139 passed**. Detalhes no **Item 8.8**. **Nada de código pendente.** O **Item 9.7 foi
descartado pelo usuário** em 23/10/2026 (considerado solucionado).

**Sessão anterior:** 22/10/2026 — sessão de **diagnóstico do Dashboard** (sem alteração de
código de produção): o KPI "Total de Entradas" (951.529,18 em 2025) e a série "Entradas" do
gráfico (rótulo "278 mil") usavam **fórmulas SQL diferentes** — o gráfico somava o valor
**unitário** (`SUM(l.valor)`) e ignorava a **quantidade**, o desconto, o `valsub` e o IPI.
**Correção APLICADA, validada no banco e commitada pelo usuário** em `a503daa`
("Unify dashboard entry value calculations"): a expressão virou `EXPR_VALOR_ENTRADA`
(fonte única de verdade) — KPI e gráfico coincidem em 2024/2025/2026 (Item 9.2). O mesmo
commit **desrastreou o `config.ini`** (Item 6.10 — feito; **rotação da senha ainda pendente**).
**Fechamento da sessão (22/10/2026):** varredura de abertura + sincronia de docs/AGENTS
(`docs/Status_Refatoracao.md`, `docs/Mapeamento_Refatoracao_Datas.md`, `AGENTS.md`).

**2ª parte da mesma sessão (22/10/2026) — revisão do tweak `fontsize` do gráfico + Item 9.5
medido em 5 bancos de cliente:**
- **Gráfico (Item 8.6):** o tweak do usuário (`fontsize` 6 → 8 nos rótulos de valor das barras)
  **não** gera sobreposição nem estouro lateral em nenhum tamanho real, mas **amplifica um
  defeito pré-existente**: 4–8 rótulos ficavam **cortados** (topo 2,1–3,9 px; base 1,5–3,4 px).
  Correção **aplicada (Plano A aprovado pelo usuário)**: constante `MARGEM_Y_ROTULOS = 0.12` +
  `ax.margins(y=...)` no ramo "Barras" (só quando há rótulos, ≤ `MAX_PONTOS_COM_VALORES`) →
  corte **zerado** em todos os cenários. O desenho das séries foi **extraído** para
  `_desenhar_series(ax, labels, entradas, vendas, diffs, tipo, cores)` (sem Tk), o que permitiu
  **teste de regressão com render Agg** (`TestRotulosDeValor`, 6 casos). `fontsize=8` **mantido**.
  Suíte: **113 passed** (108 + 5 de `tests/test_create_views.py`).
- **Item 9.5 (medição, 5 bancos de cliente — ABC AUTO PECAS, CASA DO SHAMPOO FILIAL 0001-54,
  CASA DO SHAMPOO MATRIZ C:\ e D:\, SHAMPOO & CIA MATRIZ):** classe `'03'` → **0 produtos** em
  todos os bancos (divergência **teórica**, impacto zero); filtro `l.cance` → **0 linhas** de
  compra canceladas em 2024/2025/2026 (diferença **0,00**, sem ação); classe `'07'` → **existe
  em todos** (37/180/187/187/89 produtos; 12/43/34/34/24 com saldo > 0) e está fora dos **dois**
  universos → o inventário **subestima** (+5.283,10 / +0,13% … **+135.531,77 / +6,86%**) e a
  distorção **ignora** divergências (3/35/85/84/65 de 4/46/140/190/263 → até **61%** em MATRIZ).
  Novas classes fora dos universos: `'08'` (11/5/8/8 produtos), `'10'` e `'99'` (59 produtos,
  24 com saldo, 3.676,99; 40 divergentes).

**3ª parte da mesma sessão (22/10/2026) — erro `-607` ao fechar a app + robustez do
encerramento (Item 6.11):**
- **Causa raiz provada:** a view órfã `V_DIFF_ENTRADA_SAIDA_MES` **depende** de
  `V_FAT_VALOR_SAIDA` (coluna `FATUR`) → o Firebird recusa o `DROP VIEW V_FAT_VALOR_SAIDA` que a
  app faz no encerramento. Prova via `RDB$VIEW_RELATIONS` (consultável neste banco, FB 3.0.5).
  **Resolvido pelo usuário no banco** (Item 6.9 — `V_DIFF_ENTRADA_SAIDA_MES` já dropada);
  `V_LAN_COM` segue órfã, mas **não bloqueia** nada.
- **3 mudanças aprovadas e aplicadas** (só as que tornam o **encerramento** robusto; o item 2b
  — fluxo de **reconexão** — **não** foi aprovado e segue inalterado):
  (1) `Queries/Create_Views.py` — falha tratada **por view** (`rollback` isolado +
  `logger.exception`) e **relance da primeira exceção original**; (2) `Inventario.py` — o `finally`
  não pode ser interrompido por DDL (`try/except` + `BancoDeDados.fechar()` → o pool **e** o
  log "Aplicação encerrada." sempre executam); (3) `tests/test_create_views.py` (novo, **5
  casos**) — os 3 casos de resiliência **falham** com o código antigo (validado).
- Alteração **do usuário** (não tocada) em `Dashboard/Dashboard_Screen.py`: cores dos KPI cards
  (`COR_ENTRADAS`/`COR_VENDAS`/`COR_PREVISAO`, sem `COR_DESTAQUE`).
- **Item 9.5 — decisão do usuário registrada no Item 9.7, mas o Item 9.7 foi DESCARTADO em
  23/10/2026** (o usuário informou que já foi solucionado): normalizar os dois universos de
  classificação (incluir `'03'` na distorção), manter `'07'` (uso e consumo) **fora** de
  qualquer cálculo de inventário, e incluir o filtro `l.cance` nas queries de entradas.
  Impacto medido em 5 bancos cliente: **0,00** (nenhuma mudança numérica hoje). O diff
  registrado no Item 9.7 **não foi aplicado pelo agente**.
**Contexto histórico:** 21/10/2026 — **caça à performance ENCERRADA por medição** (decisão do
usuário); em seguida, o usuário commitou `d81b381` ("Improve dashboard trend chart visuals"),
que entregou a **base** do visual do gráfico do Dashboard — complementada na sessão de 21/10/2026
(itens A–G do Item 8). Medição pós-otimização (script `%TEMP%\opencode\medir_*.py`, só SELECTs,
banco = **cópia de cliente**) mostrou que **não sobrou correção de SQL de alto retorno**: o que
resta em `KPI previa` (~20 s) é **I/O**, não defeito de query. Duas hipóteses foram **testadas e
derrubadas**: (a) filtrar a CTE `saidas` por período → 23,05 s (pior) **e resultado diferente**
(2024: 3.190.616,54 → 3.124.194,69), ou seja, **mudaria o KPI** — não fazer;
(b) join `s.fatur = e.notfi` explodindo → **falso**: `fatur` repetido = 0, pares do join = 111.757,
maior fan-out = 1 (join um-para-um, limpo).
Evidência de I/O: `in01fat COUNT total` = 15,13 s frio → **0,17 s morno** (89x); qualquer
`COUNT(*)` com `GROUP BY` em `in01lan` custa 18–21 s. Servidor com `DefaultDbCachePages = 2048`
(≈16 MB) para arquivo de **1,3 GB** e máquina com **3,8 GB de RAM**.
**Alavancas restantes ficam FORA do código** (servidor do cliente): elevar `DefaultDbCachePages`
e/ou compactar o `.fdb` (`gbak`/`gfix`). Decisão do usuário, não da sessão.
**Não remedir:** o que foi apurado aqui está consolidado no Item 6.7.
Sessão anterior (20/10/2026): otimização de desempenho (views `V_LAN_COM`/`V_DIFF_ENTRADA_SAIDA_MES`
removidas → entradas 22 s→0,04 s, diferença 41 s→1,3 s). Sessão de 19/10/2026: refatoração de datas concluída.
**Próximo passo (neste momento):** nenhuma etapa de código aberta além do **B2**, aplicado em
26/10/2026 e aguardando revisão/commit do usuário (ver **Item 12**). O **Item 9.7 foi descartado
pelo usuário** em 23/10/2026 (considerado solucionado; em 26/10/2026 o usuário aplicou `'03'` na
distorção, deixando os dois universos idênticos); a correção da legenda/rótulos do modo
Linhas foi aplicada no Item 8.8; os **itens 1 e 4** das pendências (testes dos helpers do Dashboard
+ logging nos `except` de UI) e o **B3** foram aplicados em 26/10/2026 (ver **Item 11**). **Fila de
ideias para sessões futuras: Item 10** — o **Item 10.1** (paralelizar as consultas do Dashboard em
threads separadas) foi **medido** em 26/10/2026: KPIs e tendência já rodam em threads distintas e o
ganho do paralelismo intra-bloco é de **décimos de segundo** (§10.1) — **ENCERRADO em 26/10/2026
sem código, por decisão do usuário**; o **Item 10.2** (B1 — modelo de previsão rolado a partir do
saldo atual) foi
**registrado para uma sessão dedicada** (§10.2).
**Pendências herdadas:** testes manuais (troca de período + reabertura das telas);
`DROP VIEW V_LAN_COM` / `V_DIFF_ENTRADA_SAIDA_MES` no banco (SQL a cargo do usuário — Item 6.8);
**rotação da senha do banco** (`config.ini` já desrastreado **e commitado** — Item 6.10);
**17 `except ...: pass`** ainda silenciosos fora do Dashboard (`Comandos_Func` 3,
`Banco_de_Dados_Func` 1, `Consultas_Val_Screen` 1, `Consultas_Val_Inv_Screen` 2,
`Tk_Progress_Bar` 3, `Tk_Status_Animator` 2, `Gerenciador_Thread_BD` 3, `Thread_Executor` 2);
**PyInstaller** sem receita válida (`Outros/Auto_py_to_exe config.json` obsoleto).
**Branch:** `refatoracao_v3.5` · **HEAD:** `56093b1` · **baseline:** **209 passed** em 15 arquivos
(o HEAD tinha **203**; +6 casos do **B2** em `tests/test_dashboard_func.py`)
**Working tree (nada commitado — regra de ouro):** o trabalho **desta sessão** (26/10/2026):
`Dashboard/Dashboard_Func.py` e `tests/test_dashboard_func.py` (**B2** — ver Item 12), além da
sincronia de status em `AGENTS.md`, `AGENTS_SESSAO.md` e `docs/Status_Refatoracao.md`. O trabalho
anterior está **commitado pelo usuário** em `56093b1` ("Harden dashboard KPIs and test coverage") e
o de 23/10/2026 em `3d7d9ef`; `requirements.txt`, `Dashboard/Dashboard_Charts.py` (logging + B3),
`tests/test_periodo.py` etc. seguem commitados.
**Arquivo complementar ao:** `AGENTS.md` (leia os dois antes de iniciar).

---

## 1. REGRA DE OURO — SEM COMMITS

- **NUNCA** executar `git commit`, `git add`, `git push`, `git stash`, `git checkout`, `git reset`
  ou qualquer comando que altere o histórico/estado do git.
- Alterações ficam no working tree para revisão manual do usuário.
- Se o usuário pedir commit explicitamente, pergunte confirmação final antes de executar.

---

## 2. REGRA DE OURO — INÍCIO DE CADA SESSÃO: VARREDURA + SINCRONIA (DOCS + AGENTS)

**No começo de toda sessão nova, antes de qualquer tarefa:**

1. **Varrer o código** para apurar o estado real do momento:
   - `git log --oneline -5` e `git diff --stat` (ver o que mudou desde a última sessão,
     **somente leitura**);
   - varredura de períodos/resíduos (`dt_ini`/`dt_fim`, usos de `periodo`, `PeriodoInventario`)
     nos escopos relevantes;
   - rodar `.\.venv\Scripts\python.exe -m pytest tests -v` e
     `.\.venv\Scripts\python.exe -m compileall -q . -x "\.venv"` para confirmar a baseline.
2. **Comparar** o apurado com o que dizem os arquivos da pasta `docs/`
   (`Status_Refatoracao.md`, `Mapeamento_Refatoracao_Datas.md`,
   `Plano_Refatoracao_Inventario_Tools_v2.md`, `roadmap/`).
3. **Atualizar os itens de `docs/`** para corresponderem ao momento atual do código:
   marcar/desmarcar checks, ajustar status (✅/🔄/⬜), datas e observações conforme a
   realidade encontrada — nunca deixar docs afirmando algo que o código não confirma.
4. **Atualizar também os arquivos de agentes** (`AGENTS.md` e `AGENTS_SESSAO.md`):
   corrigir/incluir comandos, convenções, estado atual da refatoração e lições de ambiente
   apuradas na varredura, para que a próxima sessão comece com informações fiéis ao código.
   Como estas são alterações de documentação de status/instruções, basta registrar as
   alterações no relatório final da sessão; a regra de plano + prévia do Item 3 abaixo
   continua valendo para mudanças em código (`.py`).

---

## 3. REGRA DE OURO — PLANO ANTES DE EXECUTAR QUALQUER MUDANÇA

Antes de **qualquer** alteração em arquivo de código (`.py`) ou documentação relevante
(exceto a sincronia rotineira de status de `docs/` prevista no Item 2):

1. **Exibir o plano** da mudança: arquivos a tocar, motivo, escopo.
2. **Exibir prévia do código** na forma de diff proposto (`oldString` → `newString`
   ou bloco antes/depois com referência `arquivo.py:linha`).
3. **AGUARDAR confirmação explícita** do usuário (ex.: "SIM", "aprovado").
4. Só então aplicar com a ferramenta de edição.
5. Nunca alterar arquivos não mencionados no plano aprovado.

**Análise somente leitura** (leitura, grep, varredura, testes) pode ser feita sem pedir
permissão, mas qualquer **escrita** exige plano + prévia + confirmação.

---

## 4. COMANDOS DE VERIFICAÇÃO (obrigatório após mudanças de código)

```powershell
# Sintaxe (sem linter configurado no projeto):
.\.venv\Scripts\python.exe -m compileall -q . -x "\.venv"

# Testes:
.\.venv\Scripts\python.exe -m pytest tests -v
```

Estado de referência saudável: **183 passed** em 15 arquivos, `compileall` sem erros (exige
`requirements.txt` instalado — `matplotlib`/`numpy`/`scipy` são importados por
`Dashboard/Dashboard_Charts.py`).
Se testes falharem após mudança, o plano foi executado incorretamente — informar o usuário.

---

## 5. ESTADO ATUAL DA REFATORAÇÃO DE DATAS — ✅ CONCLUÍDA (19/10/2026)

**Resumo das etapas concluídas:**
- Mapeamento dos 11 grupos de consultas vs Plano v2; varredura `dt_ini`/`dt_fim` com **0 resíduos**.
- Telas de consulta migradas para snapshot de período.
- **Comandos (E6a/E6b):** `Comandos_Screen(periodo, parent)`; lógica migrada para a classe `Funcoes_Comandos` (período snapshot, sem `self.data_banco_inicial`); check de distorção via `DistorcaoManager.possui_itens()`; aliases de compatibilidade no módulo (`Comandos_Func`, `montar_operacoes`, `comandos_true`, `on_click_confirm`, `precu_porcent_entry_validate`) preservam legado/tests; `tests/test_comandos_func.py` migrado para `Funcoes_Comandos` + `FakePeriodo`.
- **Dashboard (E5):** `Dashboard_Screen(periodo, parent, button)` — comportamento "sob demanda" (snapshot na abertura, **sem listener**); KPIs usam o período selecionado; **gráfico de tendência usa janela fixa de 5 anos-calendário terminando na data final** (helper `Outros/Periodo_Inventario.periodo_tendencia_ultimos_5_anos`).
- **E7:** propriedades legadas `data_banco_*`/`_periodo_selecionado` removidas de `Inventario.py`; 0 usos de `app_self`/`dist_saldo_list`.
- **E1a:** `tests/test_periodo_manager.py` criado (16 testes: snapshot, formatação `%d.%m.%Y`, período invertido, igualdade, notificação/idempotência, registro/remoção de listeners).
- **E8:** regressão final — **85 testes passando**, `compileall` sem erros; docs sincronizados.

**Apenas testes manuais restam** (troca de período + reabertura das telas) — exigem execução da aplicação com banco real. **Nenhum commit realizado** (working tree para revisão do usuário).

**Referências-chave do padrão de período (já migrado — use como modelo):**
- `Data_Manager/PeriodoInventario.py` — snapshot frozen (`inicio_formatado`/`fim_formatado` com `%d.%m.%Y`).
- `Data_Manager/PeriodoManager.py` — single source + listeners (`obter_periodo`, `atualizar_periodo`).
- Exemplo de assinatura migrada: `Consultas_Contr_Estq_Screen.py:8`
  `def Contr_Estq_Screen(periodo, Consulta_Screen, consulta_button, container_manager)` e
  `params = (periodo.inicio_formatado, periodo.fim_formatado)` na linha 10.
- Hub que injeta período: `Consultas/Consultas_Screen.py:18` (`Consulta_Total_Screen(periodo, root)`).
- Classe migrada: `Comandos/Comandos_Gerais/Comandos_Func.py` (`Funcoes_Comandos`).
- Dashboard migrado: `Dashboard/Dashboard_Screen.py`.
- Suporte a prefetch: `Interface_Tools/Treeview_Table/Listagem_Treeview.py`.

---

## 6. OUTRAS INSTRUÇÕES DERIVADAS DESTA SESSÃO

### 6.1 Convenções de código
- Seguir o par **Screen + Func** e o estilo dos arquivos vizinhos; nunca introduzir
  bibliotecas novas sem verificar se o projeto já usa.
- Não adicionar comentários no código (regra do projeto), a menos que o usuário peça.
- Zero `print()` no código de produção (padrão já adotado); usar `get_logger` quando aplicável.
- Acesso ao banco sempre via `Thread_Manager.Query_Operations` + `thread_execução()`.

### 6.2 Loggers — log único no início da função
> **Diretiva alterada pelo usuário em 23/10/2026** (substitui a regra antiga de "somente logs de
> saída"). O usuário consultou os pares e decidiu que os logs devem ser registrados **no começo
> da função**.

- **Log de resultado vira log de entrada:** função que tinha `info`/`debug` de sucesso no fim
  passa a ter **um único log no início** do corpo, no presente, anunciando a operação e
  preservando o contexto útil (`query`, `params`, `prefix`, nome da tela/botão).
- **Sem par entrada/saída:** o log de conclusão da **mesma** função é **removido** — não se
  registra "iniciou" e "concluiu" para o mesmo fluxo. A contagem de logs não aumenta
  (conversão 1:1; a maioria dos pontos manteve o nível original).
- **Exceções continuam no `except`:** `logger.exception` permanece no tratamento do erro (não
  há como registrar um erro antes de ele acontecer). O mesmo vale para `warning`/`error` de
  **condição detectada** no meio da execução (ex.: "nenhum valor encontrado", "credenciais
  ausentes", guarda de lista inválida) — ficam no ponto de detecção, não no início.
- **Sem sequências duplicadas:** um evento não é anunciado duas vezes. Regras aplicadas:
  - callback que só delega não repete o log do fluxo que ele chama;
  - `Thread_Executor` anuncia **uma vez** (no `thread_target`, não também em `thread_execução`);
  - loops que logavam por item (ex.: criação/remoção de views) passam a logar **1×** no início;
  - infraestrutura (`Query_Operations`) registra a execução SQL em **`debug`**; módulos de
    negócio (`ven_get`, `prod_get`, `conectar`, comandos, dashboard) em **`info`**. Em `INFO`
    não há linha duplicada; em `DEBUG` a sequência negócio → SQL é intencional (granularidades
    e níveis diferentes).
- **Funções que só têm `exception`/`error`/`warning` NÃO ganham log de entrada** (não havia log
  de resultado para converter). Nesta etapa o Dashboard permanece assim; instrumentar esses
  fluxos com log de início seria uma decisão separada (aumenta volume).
- **Nível de log configurável por env var:** `INVENTARIO_LOG_LEVEL` (`DEBUG`, `INFO`...)
  com fallback `INFO` — lido em `Outros/Logger/Get_Logger.py`. Para diagnóstico, rodar a
  aplicação com `$env:INVENTARIO_LOG_LEVEL='DEBUG'` (PowerShell) sem alterar código.
- **`except` de melhor esforço não fica silencioso (desde 26/10/2026):** onde o código só tenta
  limpar/posicionar algo e pode falhar sem prejuízo (UI, `destroy`, `place_forget`, `grab`), usar
  `logger.debug('<o que falhou>', exc_info=True)` em vez de `pass`. Nível `debug` mantém o volume
  zero no padrão (`INFO`); as mensagens só aparecem com `INVENTARIO_LOG_LEVEL=DEBUG`. Aplicado ao
  Dashboard — 24 pontos em `Dashboard_Screen.py` e 10 em `Dashboard_Charts.py` (**Item 11**).
  Restam 17 `except ...: pass` em outros módulos, a avaliar caso a caso.
- Estado atual (26/10/2026, após a transição): **112 chamadas de logger** no código de produção
  (36 `exception`, 15 `info`, 5 `warning`, 53 `debug`, 3 `error`) — as de resultado já no início da
  função; nenhuma duplicação entrada+saída. O salto de 12 → 53 `debug` vem dos `except` do
  Dashboard convertidos no **Item 11**.

### 6.3 Segurança e dados
- **Nunca** gravar credenciais em arquivo versionado; `Config.ini` está no `.gitignore`.
- Não commitar chaves, senhas ou `Config.ini` de forma alguma.

### 6.4 Testes
- Testes cobrem funções **puras**; não fazer testes importarem telas com UI/display.
  Exceções já existentes: `tests/test_dashboard_charts.py` (render **Agg**, sem display) e
  `tests/test_dashboard_screen_helpers.py` (importa `Dashboard_Screen`, mas só chama
  `_periodo_anterior`/`_formatar_variacao` — o import não cria janela).
- **Não alterar testes existentes** sem aprovação explícita; acrescentar casos novos apenas
  com plano prévio (regra Item 3).
- Ao mexer nos dados do Dashboard, rode também
  `pytest tests/test_dashboard_func.py tests/test_dashboard_screen_helpers.py` (40 casos, banco
  mockado — ver **Item 11**).

### 6.5 Cuidados com o ambiente (lições desta sessão)
- **PowerShell 5.1**: NÃO usar `&&`, `| head`, `| tail`, `rg` (não existem). Usar
  `; if ($?) {...}`, `Select-Object -Last N`, e o Python da venv para varreduras.
- **Encoding de caminhos**: existem pastas com acento (ex.: `Consultas/Classificação_Do_Produto`)
  que o console mostra como `??`. Para acessar no Python, usar escape `'\xe7\xe3o'` ou walk,
  nunca digitar o caminho acentuado literalmente no shell.
- Scripts gerados temporários: prefira `docs/` ou temp; não deixar soltos na raiz.
- **Dependências (`26/10/2026`):** o `requirements.txt` precisa estar instalado **e** atualizado
  quando o código ganha import novo. `scipy` (usado por `_curva_suave` no gráfico) ficou fora do
  `requirements.txt` entre `3d7d9ef` e 26/10/2026: `compileall` **não detecta** isso (não importa
  módulos) — quem detecta é `pytest` (falha de coleta) e a execução do app (tela do Dashboard).

### 6.6 Documentação
- Manter sincronizados: `docs/Status_Refatoracao.md`, `docs/Mapeamento_Refatoracao_Datas.md`,
  `docs/Plano_Refatoracao_Inventario_Tools_v2.md` (este último é a fonte do plano geral) e
  os arquivos de agentes (`AGENTS.md`/`AGENTS_SESSAO.md`) — ver Item 2.
- Ao concluir etapa de refatoração, marcar checklist correspondente nos docs com justificativa.

### 6.7 Desempenho de queries no Firebird (lições de 20/10/2026)
- **`LEFT JOIN` em view derruba o planner:** `V_LAN_COM` faz `LEFT JOIN in01com`; usá-la com
  filtro de data na coluna da `in01com` obriga varredura completa de `in01lan`
  (~1 M linhas ≈ 8–10 s). Quando o filtro de data pela `in01com` já elimina o que não tem
  compra, um **`INNER JOIN in01lan`/`in01com` direto** deixa o planner dirigir pela
  `in01com` (≈ 2 mil linhas) → milissegundos, mesmo resultado.
- **Pushdown de período em CTE de agregação:** `V_DIFF_ENTRADA_SAIDA_MES` agrega o histórico
  inteiro; filtrar por ano **dentro** do CTE de entradas (`l.dtpro BETWEEN ? AND ?`) mantém
  semântica idêntica e cai de ~12 s para ~1,3 s. Filtrar também as saídas **muda o resultado**
  (notas emitidas fora da janela) — não fazer.
- **Diagnóstico antes de otimizar:** scripts temporários em `%TEMP%\opencode\` (fora do repo)
  conectando direto por `fdb` com credenciais do `config.ini` (nunca imprimir senha),
  medindo frio/morno com `perf_counter` por query. Método que isolou os gargalos.
- **`RDB$INDEX_FIELDS` não é consultável neste banco** (Firebird 3.0.5 / cliente): falha com
  "Table unknown". Para inspecionar índices, usar fallback só com `RDB$INDICES`
  (`RDB$RELATION_NAME`, `RDB$INDEX_NAME`, `RDB$UNIQUE_FLAG`).
- **`EXPLAIN PLAN` INDISPONÍVEL neste ambiente (21/10/2026):** qualquer variante
  (`EXPLAIN PLAN`, minúsculas, sem `?`) retorna `Token unknown - line 1, column 1 - EXPLAIN`.
  **Causa:** conflito de versões — a `fbclient.dll` **do projeto** é **3.0.13**
  (`Recursos/Firebird/fbclient.dll`) e o **servidor** é **3.0.5**. Não é problema do código.
  Consequência: **não há plano de execução**; diagnosticar só por cronometragem
  (`perf_counter`), como nos scripts `%TEMP%\opencode\medir_*.py`.
  Observações correlatas: `MON$SQL_DIALECT` e `fdb.connect(dialect=...)` **não existem**
  nesta versão do driver; há **dois servidores Firebird rodando** (3.0.5 e um 2.5 Fortes).

### 6.8 Desempenho pós-otimização — o que NÃO remedir (lições de 21/10/2026)
- **`KPI previa` (`QUERY_DIFERENCA_ANO_ANTERIOR_ATUAL`) ~20 s é I/O, não SQL.** O join é
  um-para-um (`fatur` repetido = **0**; pares do join = **111.757** < entradas 115.847;
  maior fan-out = **1**). Nada a otimizar na query.
  *(Histórico: essa query foi **substituída** em 26/10/2026 por `QUERY_MOVIMENTO_ESTOQUE_CUSTO`
  — ver o bloco de abertura do arquivo; as medições abaixo continuam válidas como registro.)*
- **NÃO filtrar a CTE `saidas` por período.** Testado: fica **mais lento** (23,05 s vs 20,86 s)
  **e muda o KPI** (2024: 3.190.616,54 → 3.124.194,69; 2025: 3.701.052,83 → 3.596.048,63).
  Já era alertado no Item 6.7; agora está medido.
- **Assinatura de I/O:** `in01fat COUNT total` = 15,13 s **frio** → 0,17 s **morno** (89x).
  Qualquer `COUNT(*)` com `GROUP BY` em `in01lan` custa 18–21 s. `in01lan` **não** melhora
  com cache (18,51 s → 18,23 s) — pista não investigada (sem `EXPLAIN`).
- **Contexto de ambiente:** `DefaultDbCachePages = 2048` (≈**16 MB**) para arquivo de **1,3 GB**;
  máquina com **3,8 GB de RAM**; `.fdb` com 240k linhas em `in01fat` ocupando ~5,4 KB/linha
  (arquivo inchado).
- **Alavancas restantes são de SERVIDOR, não de código:** elevar `DefaultDbCachePages`
  e/ou compactar o `.fdb` (`gbak`+`gfix`). Exigem parar o serviço; **decisão do usuário**.
- **Banco de teste é cópia de cliente:** nos scripts de diagnóstico, **somente SELECT** —
  nada de DDL/DML.

### 6.9 SQL de DROP das views órfãs — **parcialmente executado pelo usuário em 22/10/2026**
`V_LAN_COM` e `V_DIFF_ENTRADA_SAIDA_MES` já saíram do código (0 referências). Ordem obrigatória
(a segunda depende da primeira):

```sql
DROP VIEW V_DIFF_ENTRADA_SAIDA_MES;   -- depende de V_FAT_VALOR_SAIDA (coluna FATUR)
DROP VIEW V_LAN_COM;                  -- independente (só in01lan/in01com)
```

**Estado em 22/10/2026 (verificado por sondagem, só SELECT):** no banco do app
(`S_ABC AUTO PECAS`) o usuário **já dropou `V_DIFF_ENTRADA_SAIDA_MES`** → a dependência que
causava o `-607` **não existe mais**. **`V_LAN_COM` continua no banco** (órfã, **não bloqueia
nada** — não depende de `V_FAT_VALOR_SAIDA`); pode ser dropada quando o usuário quiser.
Nos outros 2 bancos testados (SHAMPOO FILIAL, SHAMPOO MATRIZ C:) as 3 views não existem.

O app não cria nem recria essas views (`Queries/Create_Views.py` só gerencia
`V_FAT_VALOR_SAIDA`). Não remover `V_FAT_VALOR_SAIDA` — está em uso.

### 6.10 `config.ini` versionado apesar do `.gitignore` — **desrastreado e commitado em 22/10/2026**
- `.gitignore` lista `config.ini`/`*.ini`, **mas** o arquivo já estava **rastreado** — o
  `.gitignore` só se aplica a arquivos **não** rastreados. `git ls-files config.ini` confirma.
- Consequência: `config.ini` (com `user_db`/`pass_db` e `dir_banco`) está no **histórico**
  do repositório (13+ commits, desde `1a91bfe`).
- **Ação do usuário em 22/10/2026:** `git rm --cached config.ini` — arquivo **mantido localmente**,
  agora respeitando o `.gitignore`. O `.gitignore` também foi limpo das linhas duplicadas
  (`config.ini`/`*.ini` apareciam 3×). **Commitado em `a503daa`** ("Unify dashboard entry value
  calculations") — `git ls-files config.ini` **não retorna mais nada**.
- **AINDA PENDENTE:** **rotacionar a senha do banco** — o histórico do repositório continua
  contendo as credenciais antigas. Limpar o histórico exigiria reescrita — **não fazer sem
  decisão explícita**.
- O agente **não** executa comandos de git que alterem índice/histórico sem aprovação.

### 6.11 Encerramento do app — `-607` ao fechar e robustez do `finally` (22/10/2026)

**Sintoma:** ao fechar a app, `DatabaseError -607` ("unsuccessful metadata update — cannot
delete COLUMN V_FAT_VALOR_SAIDA.FATUR — there are 1 dependencies") em
`Queries/Create_Views.py` (`cursor.execute("DROP VIEW V_FAT_VALOR_SAIDA")`), disparado por
`Inventario.py` (`deletar_views()` dentro do `finally` do `__main__`).

**Causa raiz (provada via `RDB$VIEW_RELATIONS`):** a view órfã `V_DIFF_ENTRADA_SAIDA_MES`
(CTE `saidas`: `SELECT vs.fatur … FROM V_FAT_VALOR_SAIDA vs`) **depende** de
`V_FAT_VALOR_SAIDA` → o Firebird recusa o `DROP VIEW V_FAT_VALOR_SAIDA` que a app faz no
encerramento. **Resolvido no banco** pelo usuário (Item 6.9).

**Defeitos de código corrigidos (aprovados pelo usuário — só o que afeta o encerramento):**
- `Inventario.py` (`finally` do `__main__`) — o `finally` **não pode** ser interrompido por DDL:
  `deletar_views()` passou a ser envolvido em `try/except` (com `logger.exception`) e o
  fechamento usa `BancoDeDados.fechar()` (fecha o pool **e** zera a referência). Antes, a
  exceção abortava o `finally`: `gerenciador.fechar()` (8 conexões Firebird nesta máquina) e o
  log "Aplicação encerrada." **nunca** executavam.
- `Queries/Create_Views.py` (`_deletar_views_na_conexao`) — a falha agora é tratada **por
  view** (`rollback` isolado + `logger.exception`) e a **primeira exceção original** é relançada
  ao final: uma view travada não impede as demais, e o chamador continua recebendo o erro
  original (tipo e mensagem preservados — o `-607` **não** é silenciado).
- `tests/test_create_views.py` (novo, **5 casos**, puro/fake — sem display e sem banco):
  os 3 casos de resiliência **falham** com o código antigo (validado) e passam com o novo.

**Item 2b (reconexão) NÃO foi aprovado:** o fluxo "falha ao deletar views → errorbox e não
reconecta" (`Banco_de_Dados/Tela_Banco_Dados/Banco_de_Dados_Func.py`) segue **inalterado**.

**Lição de ambiente (nova):** `RDB$VIEW_RELATIONS` **é consultável** neste banco (FB 3.0.5)
— ao contrário de `RDB$VIEWS` e `RDB$DEPENDENCIES` (FB 4+, "Table unknown"). É a forma de
**provar** de qual view/coluna vem uma dependência de metadata update:
`SELECT TRIM(RDB$VIEW_NAME), TRIM(RDB$RELATION_NAME) FROM RDB$VIEW_RELATIONS`.

---

## 8. VISUAL DO GRÁFICO DO DASHBOARD — ✅ CONCLUÍDO em 21/10/2026

**Arquivo-alvo:** `Dashboard/Dashboard_Charts.py` (lógica do gráfico — ver também `Dashboard/Dashboard_Screen.py`).

### 8.1 Já entregue por `d81b381` (commit do usuário)
- `criar_grafico_tendencia(master, dados, tipo)` — figura com tamanho **responsivo** ao widget
  hospedeiro via `_dimensoes_figura(master)` (fallback `(4.0, 2.0)` se o widget ainda não
  foi mapeado).
- Paleta/ordem das séries: `COR_SERIES_ENTRADAS` (azul), `COR_SERIES_VENDAS` (verde),
  `COR_SERIES_DIFERENCA` (vermelho).
- **Vendas representadas como valor negativo** (`vendas_negativo = [-v for v in vendas]`),
  com `axhline(0)` e grade em Y.
- `tight_layout()` + `canvas.get_tk_widget().pack(fill='both', expand=True)`.

### 8.2 Itens planejados — ✅ todos entregues em 21/10/2026 (ver 8.2.1)
1. **Eixo Y formatado** — hoje mostra o número cru (ex.: `3000000.0`); deve exibir
   compacto em pt-BR (`R$ 1,2 mi`, `R$ 350 mil`) via `matplotlib.ticker.FuncFormatter`.
2. **Valores nas barras** — anotação do valor por barra; **apenas quando o nº de pontos for
   pequeno** (≤ 12), para não poluir a visualização com 61 meses.
3. **Rareamento dos rótulos do X** — com granularidade "Mês" são até **61 rótulos**
   (`MM/AAAA`); mostrar no máximo ~15-18 (passo calculado), sempre preservando o último.
4. **Contraste do estado vazio** — "Nenhum dado encontrado para o período!" usa cor fixa
   `#7f8c8d`; passar a cor **por tema** (tupla claro/escuro), como `COR_SUBTEXTO` no
   `Dashboard_Screen.py`.
5. **Re-layout no resize** — o TkAgg do matplotlib 3.11 (`_backend_tk.resize`) redimensiona a
   figura e redesenha, mas **não** reaplica o `tight_layout`; usar `fig.set_layout_engine('tight')`
   para o layout ser recalculado a cada draw.

### 8.2.1 Status — ✅ CONCLUÍDO em 21/10/2026 (itens A–G, **sem commit**)
Alterado `Dashboard/Dashboard_Charts.py` (a função `criar_grafico_tendencia` manteve a assinatura)
e criado `tests/test_dashboard_charts.py` (**13 testes** → suíte com **98 passed**).

| Item | Entregue |
|---|---|
| A | Eixo Y com `FuncFormatter` → `R$ 1,9 mi`, `R$ 500 mil`, `R$ 2,5 bi` (pt-BR, vírgula decimal) |
| B | `ax.bar_label` nas barras, **só quando ≤ 12 pontos** (`MAX_PONTOS_COM_VALORES`) |
| C | `_rotulos_eixo_x` rareia os rótulos (61 → 16) e **garante ≤ `maximo`**, preservando o último |
| D | Estado vazio com cor **por tema** (`CORES_POR_TEMA['*']['subtexto']`) |
| E | Figura, eixos, grade, títulos, ticks e legenda **por tema** (`ctk.get_appearance_mode()`) |
| F | `fig.set_layout_engine('tight')` — layout recalculado a cada draw (inclusive no resize) |
| G | `tests/test_dashboard_charts.py` — 13 casos puros (helpers sem UI) |

**Complemento na mesma sessão (contraste — ver Item 8.4):** mais 3 casos de teste
(`TestContraste`) → suíte com **101 passed**.

Helpers puros (testáveis sem display): `_valor_compacto(valor, com_simbolo=True)`,
`_rotulos_eixo_x(labels, maximo=MAX_ROTULOS_EIXO_X)` e `_contraste(cor_a, cor_b)` (WCAG).

### 8.3 Aprendizados desta sessão (gráfico)
- **Separador decimal pt-BR:** `f'{1.9:.1f}'` gera `1.9`; o projeto usa vírgula
  (mesma convenção de `banco_codigo_valueform`). Converter com `.replace('.', ',')`.
- **`ax.bar_label(..., labels=[...])`:** quando `labels` é passado, o `fmt` é **ignorado** —
  passar a lista já formatada; `color=`/`fontsize=`/`padding=` são repassados ao `ax.text`.
- **Limite de rótulos estrito:** preservando o último rótulo, a contagem podia passar do limite
  (12 rótulos com `maximo=4` → 5). A solução escolhida troca o penúltimo pelo último
  (`indices = indices[:-1] + [total - 1]`), garantindo **≤ `maximo`**.
- **Verificação sem display:** a figura pode ser inspecionada por código
  (`ax.get_xticklabels()`, `ax.get_yticklabels()`, `ax.texts`, `figure.get_facecolor()`,
  `figure.get_layout_engine()`) — script temporário em `%TEMP%\opencode\diagnostico_grafico.py`.
  Atenção: **não abrir PNG para "validar" o visual** — a verificação é por introspecção.

### 8.4 Correção de contraste do texto do gráfico (21/10/2026, **sem commit**)
**Sintoma relatado pelo usuário:** "os labels no rótulo do gráfico estão com cores claras que se
misturam com as cores do próprio rótulo, impedindo sua leitura" — elemento apontado: **legenda**.

**Diagnóstico por medição (WCAG):** o texto claro do gráfico (`#b7e2e6` no dark) tem contraste
excelente contra a **figura** (9,85:1), mas **insuficiente contra as cores das séries**:
verde `#2ecc71` → **1,50**, azul `#3498db` → **2,26**, vermelho `#e74c3c` → **2,74**.
Onde o texto encosta nos marcadores coloridos (legenda) ou nas barras (rótulos de valores),
o texto se dissolve. No tema light o mesmo vale contra o vermelho (2,87).

**Correção aplicada:**
| Onde | Antes | Depois |
|---|---|---|
| Cor do texto | `#b7e2e6` (dark) / `#2c3e50` (light) — ciano parecido com a série azul | neutro `#ecf0f1` (dark) / `#212d38` (light); o ciano virou `subtexto` (só estado vazio) |
| Legenda | sem moldura, texto colado nos marcadores | **moldura opaca** (`facecolor` = figura, `edgecolor` = grade, `alpha=1`) + texto 9pt → contraste **11,99:1** (dark) / **14,03:1** (light) |
| Rótulos de valor das barras | texto direto sobre a barra | **caixa de fundo** (`bbox` na cor da figura, `alpha=0,85`) → legível sobre qualquer série |
| Estado vazio | chave `estado_vazio` | removida (valor duplicava `subtexto`); passa a usar `subtexto` |

**Regressão garantida por teste:** helper puro `_contraste(cor_a, cor_b)` (WCAG 2.1) em
`Dashboard_Charts.py` + `TestContraste` em `tests/test_dashboard_charts.py` exigindo
**≥ 4,5:1** entre `texto`/`subtexto` e a figura, nos **dois** temas → **101 testes**.

**Lição:** em gráfico com séries coloridas, **nunca** usar a cor "de texto do tema" sobre as
séries — ou dar superfície própria (moldura/caixa), ou garantir contraste por medição.

### 8.5 Ambiente/verificação do gráfico
- `matplotlib` 3.11.2; o backend Tk foi reorganizado (`backends/backend_tkagg.py` só reexporta;
  a classe `FigureCanvasTk` está em `backends/_backend_tk.py`).
- `FigureCanvasTk.resize` → `_resize_figure_for_canvas_size` → `figure.set_size_inches` +
  `ResizeEvent` + `draw_idle`: o gráfico **acompanha** o redimensionamento da janela.
- `Dashboard_Charts.py` chama `matplotlib.use('Agg')` **depois** de importar o `backend_tkagg` —
  inofensivo (o canvas Tk é instanciado explicitamente), mas desnecessário.
- Testes: manter os helpers de formatação **puros** (sem UI) para permitir `pytest` sem display.

### 8.6 Tweak `fontsize` 6 → 8 nos rótulos de valor — REVISADO em 22/10/2026 (Plano A aplicado)

**Contexto:** alteração **do usuário** (não commitada) em `_anotar_barras`:
`fontsize=6` → `fontsize=8` nos rótulos de valor das barras.

**Medição (render Agg, sem display; scripts `%TEMP%\opencode\revisao_fontsize*.py`)** —
tamanhos reais do widget do gráfico: **padrão** 10,6 × 3,4 pol (janela 1080×560) e
**mínimo** 6,6 × 3,0 pol (janela 680×520); fallback do código 4,0 × 2,0 pol.

| Cenário | Resultado |
|---|---|
| `fontsize` 6 → 8: sobreposição / estouro lateral | **nenhum** nos tamanhos reais |
| `fontsize` 8 **sem** margem de eixo Y | 4–8 rótulos **cortados**: topo 2,1–3,9 px e base 1,5–3,4 px |
| `fontsize` 8 **com** `ax.margins(y=0.12)` | corte **zerado** em todos os cenários |

**Correção aplicada (Plano A, aprovado pelo usuário):**
- `Dashboard/Dashboard_Charts.py` — constante `MARGEM_Y_ROTULOS = 0.12`; `ax.margins(y=MARGEM_Y_ROTULOS)`
  dentro do ramo "Barras" e **apenas** quando `len(labels) <= MAX_PONTOS_COM_VALORES` (ou seja,
  só quando há rótulos de valor); **`fontsize=8` mantido**.
- O desenho das séries foi **extraído** para `_desenhar_series(ax, labels, entradas, vendas, diffs,
  tipo, cores)` — **sem Tk**, o que permite testá-lo isoladamente. `criar_grafico_tendencia`
  ficou só com figura/canvas/estado vazio.
- `tests/test_dashboard_charts.py` — nova classe `TestRotulosDeValor` (**6 casos**): render com
  `Figure` + `FigureCanvasAgg` nos **dois** tamanhos reais, com 5/7/12 pontos, exigindo
  (a) rótulos **não cortados** (dentro da área dos eixos), (b) **sem colisão** de rótulos,
  (c) rótulos **ausentes** acima de 12 pontos, (d) margem de Y aplicada e (e) modo "Linhas"
  **sem** margem e **sem** rótulos.

**Validação do próprio teste:** removendo temporariamente `ax.margins(y=MARGEM_Y_ROTULOS)`,
`test_rotulos_de_valor_nao_sao_cortados` **falha** (o teste pega a regressão) — restaurado em
seguida. Suíte: **108 passed**; `compileall` limpo.

**Limite medido (registrado, não é bug):** no tamanho **mínimo** da janela com **12 pontos**, os
rótulos de "Diferença" de grupos vizinhos **encostam** (0,6 px horizontal × 0,7 px vertical —
canto, sem colisão visual); no tamanho padrão não há contato. O teste admite até 1 px de
sobreposição em cada eixo.

**Contrato vigente (decisão do usuário em 22/10/2026):** as vendas vão **para cima, com valor
positivo** — o desenho usa os valores como chegam (`dados['vendas']` **não** é negado).
Um teste com vendas já negativas **inverte as barras** e produz falsos positivos de sobreposição.

### 8.7 Edição do usuário em 22/10/2026 (10:39) — vendas para cima + ajuste dos rótulos

**Alterações do usuário** em `Dashboard/Dashboard_Charts.py` (10:39 e 11:26) e
`Dashboard/Dashboard_Screen.py` (10:49 — cores dos KPI cards, `COR_ENTRADAS`/`COR_VENDAS`/
`COR_PREVISAO`):
- `ax.set_xticklabels(...)`: `fontsize` 7 → **9**, `rotation` 45 → **0**, `ha` 'right' → **'center'**
  (rótulos do eixo X horizontais e maiores).
- **As vendas passam a ser desenhadas para CIMA, com valor positivo** — *decisão deliberada do
  usuário, tomada após rever o gráfico* (11:26). **Não é regressão**: o comportamento antigo
  (vendas negativas, commit `9100308`) foi **descrito de forma invertida** nos docs desta sessão
  e **corrigido** aqui.

**Consequência medida (render Agg, 12 pontos, tamanho mínimo 6,6 × 3,0 pol):** com as três séries
(Entradas, Vendas e Diferença) no mesmo hemisfério, os rótulos de valor de **meses vizinhos** de
séries diferentes passaram a se encostar: **7,98 px × 7,81 px** de sobreposição (rótulo "Entradas"
de um mês sobre o rótulo "Vendas" do mês seguinte). No tamanho padrão (10,6 × 3,4 pol) não há
colisão (a vaga por ponto dobra).

**Correção aplicada — fonte adaptada à densidade (`_fonte_rotulos_valor`):** o tamanho da fonte
dos rótulos de valor passa a ser calculado pela vaga disponível por ponto
(`fonte = (vaga_px × 0,75 − 2) / 5,25`, com limite entre 6 e 8): **8** até 8 pontos, **6** no
tamanho mínimo com 12 pontos → a sobreposição cai a **0 px** (restam ~2,5 px de folga).
No tamanho padrão o cálculo devolve **8** (o rótulo cabe com folga) — o visual do gráfico do
usuário **não muda**. Suíte: **113 passed**.

> ⚠️ **Armadilha para as próximas sessões:** com vendas para cima, rótulos de Entradas/Vendas de
> **mesmos valores** (ou de meses vizinhos) podem se encostar. Ao mexer em rótulos do gráfico,
> rode `pytest tests/test_dashboard_charts.py` — o teste `test_rotulos_de_valor_nao_se_sobrepoem`
> renderiza nos **dois** tamanhos reais da janela e mede as caixas de texto.

**Efeito colateral da mudança do usuário nos rótulos do eixo X** (medido em render Agg, 12 pontos):
| tamanho | maior sobreposição horizontal entre rótulos do eixo X |
|---|---|
| padrão (10,6 × 3,4 pol) | **0,00 px** — cabe |
| mínimo (6,6 × 3,0 pol) | **6,64 px** — os rótulos **se sobrepõem** |

Motivo: com `rotation=0` e `fontsize=9`, cada rótulo ("01/2025") ocupa ≈45 px e a vaga por ponto
no tamanho mínimo é ≈48 px. `_rotulos_eixo_x` só rareia acima de `MAX_ROTULOS_EIXO_X = 16`
(12 pontos → sem rareio). **Pendente de decisão do usuário** (é a alteração visual dele):
- (a) manter e reduzir o `fontsize` do eixo X quando há muitos pontos (ex.: 7 com > 8 pontos);
- (b) voltar a `rotation=45` quando o número de pontos for alto;
- (c) rarear antes (baixar `MAX_ROTULOS_EIXO_X`) — perde meses no eixo X.
Nenhuma das opções foi aplicada (mudança em `.py` exige plano + aprovação).

### 8.8 Legenda fora da área + rótulos nos dois modos (23/10/2026) — APLICADO

**Pedido do usuário:** resolver o *overlapping* da legenda com os valores no gráfico de barras
e fazer o gráfico de linhas **também exibir os valores**.

**Medição do problema (render Agg, sem display):** com `loc='best'`, a legenda cobria rótulos
de valor em **4 de 6** cenários reais (5/7/12 pontos × tamanhos padrão 10,6×3,4 pol e mínimo
6,6×3,0 pol) — **1 a 2 rótulos cobertos**. O modo Linhas não desenhava rótulo algum (o ramo
saía antes de qualquer anotação).

**Correções aplicadas em `Dashboard/Dashboard_Charts.py`:**
- `_configurar_legenda(ax, cores)`: legenda em **faixa horizontal acima do gráfico**
  (`loc='lower center'`, `bbox_to_anchor=(0.5, 1.01)`, `ncol=3`), mantendo moldura opaca e
  cores por tema; título com `pad=32` para ficar acima da legenda.
- `_anotar_linhas(...)`: rótulos de valor no modo Linhas com **posicionamento anticolisão** —
  candidatos acima/abaixo (+7, −7, +18, −18, +28, −28 pt), validando cada caixa contra a área
  do eixo e contra os rótulos já postos (`TOLERANCIA_COLISAO_PX = 1,0`). Mesmo limite de
  `MAX_PONTOS_COM_VALORES = 12`.
- `_desenhar_series`: o ramo Linhas também aplica `ax.margins(y=MARGEM_Y_ROTULOS)` quando há
  rótulos.

**Refinamento após retorno do usuário (mesma data):** o usuário reportou que as **barras
continuavam com overlap** e que a fonte dos valores nas linhas poderia ser mais bonita.
Medição: o rótulo horizontal mede **~42–47 px**, mas a vaga de cada barra tem **~19 px**
(12 meses) → **12 rótulos ficavam por cima das barras vizinhas**; quando Entradas ≈ Vendas
havia **até 12 colisões rótulo × rótulo**. Aumentar margem Y não resolve (o problema é a
largura do texto). Correções aplicadas:
- **Barras:** rótulos **verticais (`ROTACAO_ROTULOS_BARRAS = 90`)** — ~10 px de largura, cabem
  na vaga da própria barra; `_expandir_folga_vertical(...)` mede as caixas já renderizadas e
  abre o eixo Y iterativamente (`MAX_AJUSTES_FOLGA_VERTICAL = 8`) para nenhum valor ser cortado.
  Custo medido: eixo Y **+28%** no caso de 12 pontos.
- **Linhas:** fonte fixa **8** (`FONTE_ROTULOS_LINHA`, sem encolher para 6) e **halo/contorno**
  na cor do fundo (`path_effects.withStroke`, 2,5 px) em vez da caixa quadrada — visual mais
  limpo.

**Medição final:** 0 sobreposições legenda × rótulos/ticks/título, legenda dentro da figura,
0 rótulos cortados, 0 colisões entre rótulos e **0 rótulos sobre outras barras** em 2 conjuntos
de dados (normal e séries quase iguais) × 2 tamanhos × 5/7/12 pontos, nos **dois** tipos.

**Testes (`tests/test_dashboard_charts.py`):** `TestRotulosDeValor` parametrizada para
**Barras e Linhas** (contagem, não-corte, não-sobreposição, ausência acima de 12 pontos),
`test_modo_linhas_nao_altera_a_margem` virou `test_margem_de_rotulos_aplicada_no_modo_linhas`,
`test_legenda_nao_cobre_rotulos_de_valor` (legenda × rótulos × ticks × título, 5/7/12 pontos ×
2 tamanhos × 2 tipos) e, no refinamento, `test_rotulos_de_barras_sao_verticais`,
`test_rotulos_de_barras_nao_cobrem_outras_barras` e
`test_rotulos_de_linhas_usam_halo_e_fonte_8`. Suíte: **139 passed**; `compileall` limpo.

### 8.9 Recursos do commit `3d7d9ef` documentados em 26/10/2026

O commit `3d7d9ef` ("Harden dashboard and thread workflows") foi criado pelo usuário depois da
sessão de 23/10/2026 e contém, além do que o Item 8.8 já descrevia, quatro recursos que **não
estavam registrados** (descobertos na varredura de abertura de 26/10/2026):

| Recurso | Onde | O que faz |
|---|---|---|
| **KPI comparativo** | `Dashboard/Dashboard_Screen.py` (`_periodo_anterior`, `_formatar_variacao`, `_criar_kpi_card(..., variacao, cor_variacao)`, `_atualizar_dashboard(..., kpis_anterior)`) + `Dashboard/Dashboard_Func.py` (`_calcular_kpis`, `carregar_kpis(ini, fim, ini_ant, fim_ant)`) | cada card exibe **"±x,x% vs período anterior"**; o período anterior tem a **mesma duração** e termina no dia anterior ao início do período atual (verde se ≥ 0, vermelho se < 0). Com `ini_ant`/`fim_ant`, `carregar_kpis` devolve **tupla** `(atual, anterior)`; as chaves `*_num_ant` são montadas no callback de `_carregar_dados` |
| **Curvas suavizadas** | `Dashboard/Dashboard_Charts.py` (`_curva_suave`, `numpy` + `scipy.interpolate.make_interp_spline`, 200 pontos) | no modo **Linhas**, o traçado é uma spline (k = min(3, n−1)); os **pontos/marcadores e a legenda** continuam sendo plotados com os dados originais (`linestyle='none'`), para o tooltip e os rótulos usarem os valores reais |
| **Barra de ferramentas** | `criar_grafico_tendencia` (`NavigationToolbar2Tk`, `side='bottom'`) | controles padrão do matplotlib (zoom/pan/salvar) embaixo do gráfico; falha é silenciada (`try/except`) |
| **Tooltip** | `adicionar_tooltip` (`CTkLabel` via `place`) | mostra o valor (`R$ …`) sob o cursor em barras/pontos; registrado por `mpl_connect('motion_notify_event'/'axes_leave_event')` |

**Dependência nova:** `numpy` e `scipy` passaram a ser imports **diretos** de `Dashboard_Charts.py`
(antes o numpy só vinha como dependência transitiva do matplotlib). Em **26/10/2026** o `scipy`
foi **instalado** na `.venv` (1.18.1) e ambos foram **declarados no `requirements.txt`** — sem
isso o módulo não importava e a suíte abortava na coleta.

**Observações (sem ação tomada):**
- `Dashboard_Screen.py:11` importava `adicionar_tooltip` sem usar (o tooltip é registrado dentro
  de `criar_grafico_tendencia`) — **o usuário removeu esse import do código em 26/10/2026**
  (alteração dele no working tree; o agente não tocou no arquivo).
- `tests/test_dashboard_charts.py` tem **31 casos** (o doc anterior dizia 28); a suíte total
  continua **139 passed**.

---

## 9. KPI "Total de Entradas" × série "Entradas" do gráfico — DIVERGÊNCIA DE FÓRMULA (22/10/2026)

**Sintoma relatado pelo usuário:** KPI "Total de Entradas" = **951.529,18** (período 2025),
mas o gráfico de tendência exibe **"278 mil"**.

### 9.1 Diagnóstico (medido no banco — cópia do cliente, só SELECTs)

**Não é divergência de período** — é divergência de **fórmula**:

| Origem | Query | Valor da expressão |
|---|---|---|
| KPI do card "Total de Entradas" (`Dashboard_Func.py:219`) e tela "Valor de Entradas" (`Consultas_Val_Ent_Func.py:18`) | `QUERY_ENTRADAS` (`Queries/Consulta_Queries.py:43`) | `((valor − valor×despr/100) × quant) + valsub + (((valor − valor×despr/100) × quant) × alipi_ent/100)` |
| Série "Entradas" do gráfico (`Dashboard_Func.py:177,182`) | `QUERY_ENTRADAS_MES_ANO_AGRUPADO` / `QUERY_ENTRADAS_ANO_AGRUPADO` (`Dashboard/Dashboard_Func.py:39,56`) | `SUM(COALESCE(l.valor,0))` → valor **unitário**, **sem `quant`** |

**Decomposição medida em 2025** (`in01lan` ⋈ `in01com`, 6.207 linhas):
| Componente | Valor |
|---|---|
| A — `SUM(l.valor)` (o que o gráfico mostra) | 278.164,69 |
| B — `(valor − desconto) × quant` | 872.107,18 |
| C — `valsub` | 72.019,00 |
| D — IPI sobre B | 7.402,99 |
| **B + C + D (o que o KPI mostra)** | **951.529,18** |

`VENDAS` **não** tem o problema: KPI e gráfico usam a mesma `SUM(valor_saida)` sobre
`V_FAT_VALOR_SAIDA` com os mesmos filtros.

**Verificações colaterais:** `dtcom` vs `dtpro` como filtro de período → **resultados
idênticos** (o join `in01com` já restringe às compras). Período do usuário = **2025**
(`periodo_padrao()` = último ano cheio). O gráfico usa janela fixa de 5 anos
(`periodo_tendencia_ultimos_5_anos`) → 7 pontos no modo "Ano" (rótulo "278 mil" = 278.164,69
formatado por `_valor_compacto`).

### 9.2 Correção — ✅ APLICADA em 22/10/2026 (commitada pelo usuário em `a503daa`)

**Fonte única de verdade:** a expressão passou para `EXPR_VALOR_ENTRADA` em
`Queries/Consulta_Queries.py`, usada por `QUERY_ENTRADAS` **e** pelas duas queries de tendência
do Dashboard. As duas telas não podem mais divergir.

- `Queries/Consulta_Queries.py` — novo `EXPR_VALOR_ENTRADA`; `QUERY_ENTRADAS` virou f-string
  (`{{placeholders}}` preserva o `.format(placeholders=...)` já usado em runtime).
- `Dashboard/Dashboard_Func.py` — `QUERY_ENTRADAS_MES_ANO_AGRUPADO` e
  `QUERY_ENTRADAS_ANO_AGRUPADO` passaram a usar `EXPR_VALOR_ENTRADA`.
- `tests/test_queries.py` — caso anti-regressão `test_queries_de_entradas_compartilham_a_mesma_expressao`.
- **Contrato dos testes:** `tests/test_queries.py` só exige que os nomes `QUERY_*` existam e
  sejam não vazios → `EXPR_VALOR_ENTRADA` (não começa com `QUERY_`) não quebra o contrato;
  `_nome_query` (`Thread_Manager/Query_Operations.py:11`) compara o SQL **em runtime** com as
  constantes do módulo → continua identificando `QUERY_ENTRADAS` / `QUERY_ENTRADAS_ANO_AGRUPADO`.

**Validação no banco (cópia do cliente, só SELECT):**
| Período | KPI | Barra do gráfico (Ano) | Soma dos meses | Iguais |
|---|---|---|---|---|
| 2024 | 703.596,11 | 703.596,11 | — | ✅ |
| 2025 | **951.529,18** | **951.529,18** | **951.529,18** | ✅ |
| 2026 (jan–set) | 597.393,68 | 597.393,68 | — | ✅ |

Desempenho inalterado (0,08 s por ano; 0,28 s na janela de 5 anos). Suíte: **102 passed**;
`compileall` limpo.

### 9.3 Efeito colateral esperado (comunicado ao usuário)

Com a fórmula unificada, a série "Diferença" (`entradas − vendas`) deixa de ser dominada por
vendas: em 2025, entradas 951.529,18 × vendas 1.612.693,53 → diferença **−661.164,35**
(antes: 278.164,69 − 1.612.693,53 = −1.334.528,84). O gráfico fica mais legível e
comparativo com o KPI.

### 9.4 Scripts de diagnóstico (temporários, fora do repo)

`%TEMP%\opencode\diagnostico_kpi_entradas.py`, `diagnostico_entradas_decomposicao.py`,
`prototipo_grafico_entradas.py`, `validacao_pos_correcao.py`,
`diagnostico_casos_similares.py`, `diagnostico_casos_similares2.py` — conectam por `fdb` com as
credenciais do `config.ini` (nunca imprimir a senha), **somente SELECT**.

### 9.5 Varredura de casos semelhantes (22/10/2026) — resultado

**Varredura feita:** SQL fora de `Queries/` (só o Dashboard tem); pares query-de-contagem ×
query-de-listagem; universos de classificação; filtros de cancelamento; semântica de data;
view `V_FAT_VALOR_SAIDA`; fórmulas "de entradas" em todo o app.

**✅ Sem divergência (verificado no banco):**
| Item | Resultado |
|---|---|
| KPI "Valor do Inventário" × tela Valor do Inventário | mesma `QUERY_INVENTARIO` |
| KPI "Total de Vendas" × tela Valor de Vendas | mesma `QUERY_VENDAS` |
| KPI "Total de Entradas" × tela Valor de Entradas | mesma `QUERY_ENTRADAS` |
| KPI Vendas × série Vendas do gráfico | **1.612.693,53 = 1.612.693,53** |
| `dtcom` (data da compra) × `dtpro` (data do movimento) nas entradas | **280.611,25 = 280.611,25** (2025) |
| View `V_FAT_VALOR_SAIDA` no banco × fórmula do código | 9.912.968,64 vs 9.912.968,65 (arredondamento) |
| 6 pares contagem × listagem (`Preço Custo Zerado`, `Preço Custo > PV`, `Classificação Nula`, `Quantidade Exorbitante`, `Controle Estoque`, `Saldo Não Zerado`) | filtros **semanticamente iguais** (as diferenças detectadas são só o prefixo de alias `L.`) |

**⚠️ Divergências latentes (encontradas, com impacto ZERO nesta base):**
1. **Universo de classificação** — `QUERY_INVENTARIO` (`'00','01','02','03','04','05','06'`) ×
   `QUERY_DISTORCAO_SALDO` (`'00','01','02','04','05','06'` — **sem `'03'`**). Se um cliente
   tiver produtos de classe `'03'` com saldo > 0, o **valor do inventário** os conta e a
   **checagem de distorção** os ignora. Nesta base: **0 produtos** classe `'03'` → sem impacto.
   *Decisão de negócio necessária* (o `'03'` é inventário?).
2. **Filtro de cancelamento (`l.cance`)** — `QUERY_ENTRADAS` **não** filtra `cance`;
   `QUERY_DISTORCAO_SALDO` filtra (`COALESCE(l.cance,'N')='N'`). Nesta base: **0 linhas** de
   compra com `cance='S'` em 2025 → sem impacto. *(KPI e gráfico seguem coerentes entre si.)*
3. **Classe `'07'`** — existe nesta base (51 produtos) e está fora das **duas** listas → coerente,
   mas os produtos `'07'` **não** entram no valor do inventário (nenhum deles tem saldo > 0).
   *Confirmação de negócio necessária.*

**ℹ️ Não é bug, mas é uma terceira noção de "entradas"** — o KPI "Previsão de Inventário"
(`QUERY_DIFERENCA_ANO_ANTERIOR_ATUAL`, `Dashboard_Func.py:75`) calcula entradas como
`MAX(c.valno)` (valor da **nota**), e não pela expressão `EXPR_VALOR_ENTRADA` (valor extendido).
Conceito diferente (diferença entradas−saídas por nota) — **não misturar** com o KPI
"Total de Entradas".
*(Histórico: em 26/10/2026 o KPI passou a usar `QUERY_MOVIMENTO_ESTOQUE_CUSTO`, que não usa
`in01com`/`V_FAT_VALOR_SAIDA`; a observação acima vale para o código anterior a essa data.)*

**Nota de ambiente:** `RDB$VIEWS` e `RDB$INDEX_FIELDS` **não são consultáveis** neste banco
("Table unknown") — mesmo bloqueio do Item 6.7. A view do banco foi conferida **funcionalmente**
(agregando `valor_saida` × fórmula do código), não por definição textual.

### 9.6 Item 9.5 medido em 5 bancos de cliente (22/10/2026) — só SELECT

Script: `%TEMP%\opencode\medir_item95.py`. Bancos: **ABC AUTO PECAS**, **CASA DO SHAMPOO FILIAL
0001-54**, **CASA DO SHAMPOO MATRIZ** (C:\ e D:\), **SHAMPOO & CIA MATRIZ**.

| Tema | ABC AUTO PECAS | SHAMPOO FILIAL 0001-54 | SHAMPOO MATRIZ C:\ | SHAMPOO MATRIZ D:\ | SHAMPOO & CIA MATRIZ |
|---|---|---|---|---|---|
| Classe `'03'` (produtos) | 0 | 0 | 0 | 0 | 0 |
| Classe `'07'` — produtos | 37 | 180 | 187 | 187 | 89 |
| Classe `'07'` — com saldo > 0 | 12 | 43 | 34 | 34 | 24 |
| Inventário **sem** `'07'` (subestimativa) | +5.283,10 (+0,13%) | +9.543,39 (+0,70%) | +16.656,87 (+1,15%) | +16.656,87 (+1,15%) | **+135.531,77 (+6,86%)** |
| Distorção: divergentes **com** `'07'` | 3 de 4 | 35 de 46 | 85 de 140 | 84 de 190 | **65 de 263 (até 61%)** |
| Linhas de compra com `l.cance='S'` (2024/2025/2026) | 0 | 0 | 0 | 0 | 0 |

**Leitura:**
- **Classe `'03'`** — divergência **teórica**: **0 produtos** em todos os 5 bancos. Continua sem
  impacto; a decisão "o `'03'` é inventário?" permanece **aberta** (não custa nada decidir).
- **Filtro `l.cance`** — **0 linhas** canceladas em todos os bancos e anos → diferença **0,00**;
  **nenhuma ação** necessária (manter o filtro da distorção e a ausência na entradas).
- **Classe `'07'`** — **existe em todos os 5** e está fora dos **dois** universos → o app
  **subestima o inventário** (até **+6,86%**) e a checagem de distorção **ignora** divergências
  (até **61%** em MATRIZ). **É a divergência de maior impacto real.**
- **Novos achados (fora dos dois universos):** classe `'08'` (11/5/8/8 produtos; 8 e 4
  divergentes) e classes `'10'`/`'99'` (59 produtos, 24 com saldo, 3.676,99; 40 divergentes).

**Recomendação do agente (a decisão é do usuário):** incluir `'07'` — e avaliar `'08'`/`'10'`/`'99'`
— no universo do inventário **e** da distorção (as duas listas devem compartilhar o mesmo
universo); `'03'` sem ação imediata; `l.cance` sem ação.

### 9.7 DECISÃO DO USUÁRIO sobre o Item 9.5 (22/10/2026) — **DESCARTADO em 23/10/2026**

> **Descarte (23/10/2026):** o usuário informou que o item **já foi solucionado** e pediu para
> descartá-lo. O diff abaixo **não foi aplicado pelo agente** e permanece apenas como registro
> histórico da decisão. **Atualização (26/10/2026):** o usuário aplicou a parte (a) por conta
> própria — `QUERY_DISTORCAO_SALDO` passou a incluir `'03'`, então os universos de
> `QUERY_INVENTARIO` e da distorção são agora **idênticos** (`'00'`–`'06'`); a parte (c)
> (`l.cance` nas entradas) **continua não aplicada**, com impacto medido de **0,00**.

**Decisão (palavras do usuário):** *"Normalize a distorção e o inventário, inclua `'03'` na
distorção. `'07'` indica produtos de uso e consumo, eles não são inclusos em **NENHUM** cálculo
de inventário, caso esteja mal preenchido é função do cliente ajustar. Distorção filtra `l.cance`
por conta que ela também inclui vendas em sua consulta, mas aceito incluir na query de entradas
para consistência."*

**Tradução em regras de negócio (para as próximas sessões):**
1. **Os dois universos de classificação devem ser IGUAIS** (normalização) →
   `QUERY_INVENTARIO` e `QUERY_DISTORCAO_SALDO` passam a usar a **mesma** lista.
2. **`'03'` entra na distorção** (fecha o ponto cego: hoje o app valia o `'03'` no inventário
   mas nunca checava a distorção dele).
3. **`'07'` = produtos de uso e consumo** → fica **fora dos DOIS** cálculos (inventário **e**
   distorção). Nada a mudar no código. `'08'`/`'10'`/`'99'` seguem **fora** dos dois (mesmo
   espírito: são itens de uso/promocional — `CESTO EXPOSITOR`, `DISPLAY DE TORRE`, `AMOSTRA SACHE`).
4. **Filtro `l.cance` entra nas entradas** (consistência com a distorção).

**Medição de impacto (5 bancos cliente, só SELECT, 22/10/2026 — script
`%TEMP%\opencode\verificar_item95_decisao.py`):**
- Classe `'03'`: **0 produtos** em **todos** os 5 bancos → normalizar a lista **não muda**
  a distorção de nenhum cliente (nada a checar).
- Filtro `l.cance` nas entradas (KPI "Total de Entradas"): **diferença 0,00** em 2024, 2025 e
  2026 nos 5 bancos (ex.: ABC AUTO PEÇAS 2025 → 7.238.255,54 com e sem o filtro).
  → a mudança é **numéricamente neutra** hoje; o ganho é **consistência** (se um cliente
  cancelar uma compra, o KPI deixa de contar aquela nota).
- Filtro `l.cance` nas **séries do gráfico** (anual e mensal) — também **0,00** nos 5 bancos
  (script `%TEMP%\opencode\verificar_item95_parte2.py`, item `[B2]`/`[B3]`).
- Filtro `l.cance` na **CTE `entradas` da query de previsão** (KPI "Previsão de Inventário")
  — **0,00** nos 5 bancos (script `%TEMP%\opencode\verificar_item95_cte.py`): a **query
  completa não roda** nos bancos cliente (a view `V_FAT_VALOR_SAIDA` só existe enquanto o app
  está conectado — criada na conexão, removida no encerramento), então a **CTE foi medida
  isolada** (só `entradas` + `entradas_com_valor`), com e sem o filtro:
  - ABC AUTO PEÇAS 2025 → 59.999 notas / 7.298.081,40 **igual** nos dois casos;
    2026 → 40.104 notas / 4.878.494,52 **igual**.
  - SHAMPOO FILIAL 2025 → 25.251 notas / 847.695,29 **igual**; MATRIZ 2025 → 42.042 notas /
    1.357.467,09 **igual**; MATRIZ 2026 → 3.539 notas / 102.387,46 **igual**;
    SHAMPOO & CIA 2025 → 26.094 notas / 844.402,67 **igual**.
  - a contagem de **notas** também não muda → nenhuma compra cancelada existe nesses bancos.

> **Conclusão do Item 9.5:** as três "noções" de entradas (KPI, séries do gráfico e previsão)
> recebem o filtro `l.cance` **sem qualquer alteração numérica** em 5 bancos de cliente.
> A mudança é de **consistência/semântica**, não de valor.

**Diff registrado (NÃO APLICADO — item descartado pelo usuário em 23/10/2026):**
- `Queries/Consulta_Queries.py:222` — `'00','01','02','04','05','06'` → `'00','01','02','03','04','05','06'`
  (normaliza com `QUERY_INVENTARIO:17`).
- `Queries/Consulta_Queries.py` (`QUERY_ENTRADAS`) — `+ AND COALESCE(l.cance, 'N') = 'N'`.
- `Dashboard/Dashboard_Func.py` (`QUERY_ENTRADAS_MES_ANO_AGRUPADO` e
  `QUERY_ENTRADAS_ANO_AGRUPADO`) — `+ AND COALESCE(l.cance, 'N') = 'N'`
  (as séries do gráfico **precisam** ir junto, senão o KPI e o gráfico divergem de novo — a
  classe de bug do Item 9.2).
- `Dashboard/Dashboard_Func.py` (`QUERY_DIFERENCA_ANO_ANTERIOR_ATUAL`, CTE `entradas`) —
  `+ AND COALESCE(l.cance, 'N') = 'N'` → simetria com a CTE `saidas`, que já filtra
  `COALESCE(vs.cance,'N')='N'` (`vs.cance` vem de `in01fat.cance`). **Ponto em aberto:**
  o usuário aprovou o filtro "na query de entradas"; esta query é a **3ª noção** de entradas
  (Item 9.5) — confirmar se entra.
- `tests/test_queries.py` — 2 casos de contrato: (a) os dois universos são **iguais** e
  contêm `'03'` e **não** contêm `'07'`; (b) as 3 queries de entradas filtram `l.cance`.

**Estado:** decisão tomada, impacto medido, diff preparado — **nada aplicado, nada commitado**.

### 9.8 Amostras dos produtos fora dos universos (22/10/2026, só SELECT)
Script `%TEMP%\opencode\exemplos_classes.py`. Amostra por cliente (maior valor primeiro):
- **ABC AUTO PEÇAS (`'07'`)** — `PNEU 175/75R13` (4.096,20), `AMORTECEDOR TS CB` (712,50),
  `CAIXA SOM` (265,46), `KIT FERRAMENTA`, `REBITE`, `PORTA LAPIS`, `CHAVEIRO`, `MOUSE PAD`,
  `CANETA` → **mistura de mercadoria de revenda com brindes/uso interno**.
- **SHAMPOO FILIAL (`'07'`)** — `OX CREMOSA` (3.816,34), `MASCARA BOMBA FIOS`,
  `SUPERMASCARA`, `NOVA OX CREMOSA`, `PLACA MAE`, `MOP 360`, `CONJUNTO PROMOCIONAL` (224,43),
  `DISPLAY CHAO IMPALA` (207,64) → cosméticos de revenda + promocional.
- **SHAMPOO MATRIZ (`'07'`)** — `NOVA OX CREMOSA` (3.624,61), `MATERIAL DE CONSTRUCAO`
  (2.414,23), `PROVADORES KISS MAQUIGENS` (2.345,66), `GABINETE/SSD` (2.150,00),
  `UDA GAMER` (1.396,00), `MASCARA PROMOCIONAL`, `PROMOcao BRINDES`, `SSD 480G`.
- **SHAMPOO & CIA (`'07'`)** — `SACHE KIT FATTORE PROMOCIONAL` (**99.597,60**),
  `SACHES DIVERSOS` (26.359,02), `DISPLAY EXPOSITOR DE CHAO STUDIO 35` (5.603,00),
  `SACOLA POL. IMP.`, `AMOSTRA SACHE` → **~93% do valor da classe é amostra/promocional**.
- **Classes pequenas** — `'08'`: `CESTO EXPOSITOR - AZUL` (677,60), `MEMORIA DDR4 4GB` (580,00);
  `'99'` (só SHAMPOO & CIA): `REFIL MASCARA MANDIOCA` (1.536,00), `DISPLAY DE TORRE` (1.162,00);
  `'10'`: 2 produtos, 1 com saldo (60,00).

---

## 7. FLUXO PADRÃO DE TRABALHO RESUMIDO

1. **(Início de sessão)** Ler `AGENTS.md` + este arquivo + `docs/Status_Refatoracao.md`;
   varrer o código (git log/diff, resíduos, testes) e **atualizar `docs/` e os arquivos de
   agentes** (`AGENTS.md`/`AGENTS_SESSAO.md`) para refletirem o momento atual do código
   (ver Item 2).
2. Executar somente-leitura (análise/varredura) do que for pedido.
3. **Montar plano** + **prévia de código (diff)** → **aguardar confirmação**.
4. Aplicar alterações aprovadas.
5. Rodar `compileall` + `pytest -v`.
6. Atualizar docs de status (se a mudança afetar status).
7. **Não commitar.** Relatar o que foi feito e o que ficou pendente.

---

## 10. FILA DE IDEIAS PARA SESSÕES FUTURAS

### 10.1 Paralelizar as consultas do Dashboard em threads separadas — ⏹️ **ENCERRADO sem código** (medido em 26/10/2026)

**Pedido do usuário (26/10/2026):** "introduzir threads separadas nas consultas do banco de dados
dentro do dashboard, **apenas se esse já não for o caso**". A apuração abaixo foi feita na sessão
de 26/10/2026 (somente leitura) e **nada foi alterado**.

**O que JÁ é paralelo hoje:**
- A **UI (Tk) nunca executa query**: tudo passa por `thread_execução()`
  (`Thread_Manager/Thread_Executor.py`), que cria uma `threading.Thread` por chamada.
- **KPIs × tendência já rodam em duas threads independentes**, disparadas na abertura do
  Dashboard (`Dashboard_Screen.py:448` `_carregar_dados` → `carregar_kpis`; `:461`
  `carregar_tendencia` → `_recarregar_tendencia` → `carregar_dados_tendencia`).
- O **pool** (`Thread_Manager/Gerenciador_Thread_BD.py`) já suporta operações concorrentes:
  `Queue` de conexões, limite `min(max(cpu*2, 2), 50)`, contador `_operacoes_ativas` e
  `aguardar_operacoes()`; cada `query_executor` pega/devolve uma conexão. **Não há infra nova a
  criar** para consultas paralelas.

**O que NÃO é paralelo (o que o pedido alcança):**
- Dentro de cada thread, as consultas são **sequenciais** (`_executar_consulta` /
  `_executar_select`, uma de cada vez):
  - `carregar_kpis` (`Dashboard/Dashboard_Func.py:250`) → `_calcular_kpis` (`:216`): inventário
    → vendas → entradas → **previsão** (`_previa_inventario`, `QUERY_MOVIMENTO_ESTOQUE_CUSTO`,
    a mais pesada). Desde 26/10/2026 a previsão só roda no **período atual**
    (`incluir_previa=False` no anterior) → **7 consultas sequenciais**, 1 pesada.
  - `carregar_dados_tendencia` (`:174`): vendas → entradas (2 consultas sequenciais).
- Não há `ThreadPoolExecutor`/`concurrent.futures` no código (nenhum uso hoje).

**Onde mexer (registro histórico, caso seja retomado algum dia):** `Dashboard/Dashboard_Func.py` — `_calcular_kpis` (3 consultas
independentes + previsão que depende só de `valor_inventario`) e `carregar_dados_tendencia`
(vendas × entradas independentes). As duas chamadas de `_calcular_kpis` (atual × anterior) também
são independentes entre si. *(Atualização 26/10/2026: a previsão deixou de ser calculada no
período anterior, então a 2ª chamada tem só 3 consultas leves.)*

**Cuidados obrigatórios:**
- **Não tocar em Tk** dentro das threads: os callbacks de UI devem continuar no `callback` externo
  do `thread_execução` (padrão atual, Item 6.2/`02afd20`).
- **Preservar a semântica de erro** de `_executar_consulta` (falha de uma consulta → log + retorna
  `0`, sem derrubar o bloco inteiro) e a de `carregar_dados_tendencia` (erro → séries vazias).
- **Consumo do pool**: cada consulta paralela ocupa 1 conexão; com 2 blocos × N consultas dá para
  passar do pool desta máquina (8 conexões) — dimensionar `max_workers` ou serializar parte.
- **Sem ganho garantido:** pelo Item 6.7/6.8 a `previa` (~20 s) é **I/O do servidor**
  (`DefaultDbCachePages = 2048`, máquina com 3,8 GB de RAM); paralelizar pode apenas **contender**
  pelo mesmo disco. **Medir antes e depois** (só SELECT, banco = cópia de cliente,
  `perf_counter`), como nas sessões de 20–21/10/2026.
- Ganho plausível só se: (a) o tempo total cair para o da consulta mais lenta, ou (b) a previsão
  do período atual rodar junto com a do período anterior.

**Medição feita em 26/10/2026** (banco = cópia de cliente, **somente SELECT**; script
`%TEMP%\opencode\medir_paralelo.py`):
- Bloco de KPIs do período atual (4 consultas, 1 pesada): **0,26–0,33 s** no total. As 4 consultas
  em **série** custam **0,17–0,24 s**; em **paralelo**, **0,10–0,14 s**. A previsão domina
  (**0,09–0,14 s**).
- Tendência (vendas × entradas): **0,08–0,09 s** — paralelizar economiza ~0,04 s.
- Ou seja, o ganho absoluto é de **décimos de segundo** por carga (a tela responde em ~0,3–0,4 s
  nesta base). O gargalo real continua sendo **I/O do servidor** (Item 6.7: 3,4–13,1 s de previsão
  na base de 1,3 GB), onde 2 workers tendem a **contender** pelo mesmo disco, não a acelerar.

**Status:** ⏹️ **ENCERRADO em 26/10/2026 — sem código** (decisão do usuário: "vamos deixar como está
atualmente"). A opção de **2 workers** em `_calcular_kpis`/`carregar_dados_tendencia` foi descartada;
se algum dia for retomada, exige **remedir na base grande** e preservar a semântica de erro (incluindo
o `padrao_em_erro` do B2). Nenhum arquivo foi alterado por este item.

---

### 10.2 B1 — Previsão de inventário: rolar o saldo atual em vez de somar o movimento ao saldo — **sessão dedicada** (registrado em 26/10/2026)

**Origem:** verificação do KPI "Previsão de Inventário" (commit `56093b1`) na sessão de 26/10/2026.
A premissa documentada no código ("o snapshot é o inventário na **data inicial** do período") **não
se sustenta** nesta base: `in01pro.saldo` é o **saldo corrente do ERP** (o mesmo que
`QUERY_INVENTARIO` soma), não um valor normalizado para o ano-base. Como o modelo atual faz
`saldo_corrente + movimento_do_período`, o movimento é contado **duas vezes** (o saldo já o contém).

**Erro medido** (referência = saldo corrente rolado para a data final do período; diferença
`previsão atual − referência`, negativa = subestima):

| Período | Erro | Erro relativo |
|---|---|---|
| 2024 | −318.799,10 | **−21,1%** |
| 2025 | −129.391,38 | −8,7% |
| 2026 (jan–set) | −105.387,32 | −7,7% |

**Modelo proposto (B1):**
- `fim < hoje` → `inventário_corrente − movimento(fim+1 .. hoje)` (rolar **para trás**);
- `fim ≥ hoje` → `inventário_corrente + movimento(hoje+1 .. fim)` (rolar **para frente**);
- deixa de usar `ini`; **1 consulta**, a mesma `QUERY_MOVIMENTO_ESTOQUE_CUSTO`.
- Resíduo medido da referência: **≈ +0,03%** (o histórico converge com o saldo: 4.156.492,44 ×
  4.207.242,01; a diferença é o estoque inicial de fev/2021).

**Cuidados/custos medidos:**
- Ancorar em **`hoje`** é mais barato do que em `MAX(dtpro)`: **0,24 s** sem join × **0,72 s** com
  join nesta base (na base de 1,3 GB, `MAX(dtpro)` com join pode custar segundos).
- `hoje` precisa ser **injetável** (parâmetro com default `date.today()`) para testes determinísticos;
  a assinatura de `_previa_inventario` muda e os casos de `TestPreviaInventario` precisam ser
  reescritos (hoje eles pressupõem "soma movimento ao inventário", inclusive
  `test_soma_o_movimento_liquido_ao_inventario` e `test_envia_o_periodo_selecionado_para_a_query`).
- **Preservar o B2:** falha de consulta continua devolvendo `None` → card mostra `Erro`
  (`_executar_consulta(..., padrao_em_erro=None)`).
- Atualizar os docstrings de `QUERY_MOVIMENTO_ESTOQUE_CUSTO`, `_previa_inventario` e os textos em
  `AGENTS.md`/`docs/Plano_Refatoracao_Inventario_Tools_v2.md` que hoje descrevem a premissa
  "normalizada para o ano base" (que este item **derruba**).
- O banco de teste tem movimento em **outubro/2026** e **1 linha com data 2027-07-21** (+418,30):
  o rolar para frente até um `fim` futuro deve incluir esses lançamentos — decidir com o usuário se
  lançamentos futuros entram (recomendação: entrar, é o que o ERP tem lançado).

**Fora de escopo aqui:** mudar o rótulo do card (hoje o subtexto é fixo "estimativa do período") e
qualquer alteração de SQL de valorização.

---

## 11. ITENS 1 E 4 DAS PENDÊNCIAS + B3 — **APLICADOS em 26/10/2026** (sem commit)

**Origem:** relatório de pendências produzido na varredura desta mesma sessão. O usuário aprovou os
**itens 1 e 4** e o **B3**; as correções de documentação foram autorizadas junto.

### 11.1 Item 1 — testes dos helpers puros do Dashboard (44 casos novos)

| Arquivo | Casos | Cobre |
|---|---|---|
| `tests/test_dashboard_func.py` (**novo**) | 23 na criação (hoje **33**: +4 na redefinição do KPI e +6 no B2) | `_extrair_series` (chave ano/mês, `None`→0, `Decimal`→`float`, série vazia, chave repetida), `_previa_inventario` (soma do movimento, parâmetros enviados, vazio/NULL, `Decimal`, falha → `None`), `_executar_consulta` (`padrao_em_erro`), `_calcular_kpis` (formatação pt-BR, números crus, `vendas_130` = ×1,30, parâmetros de cada query, zeros, `'Erro'` na previsão), `carregar_kpis` (sem/com comparação, limites incompletos) e `carregar_dados_tendencia` (união por mês/ano, preenchimento de períodos ausentes, `diferenca = entradas - vendas`, CFOPs, erro → séries vazias) |
| `tests/test_dashboard_screen_helpers.py` (**novo**) | 17 | `_periodo_anterior` (mês, ano, 1 dia, bissexto, duração, sem sobreposição, entrada inválida) e `_formatar_variacao` (sinal/cor, zero, queda total, 1 casa, base zero/`None`, strings, base negativa) |
| `tests/test_periodo.py` (editado) | +4 | `periodo_tendencia_ultimos_5_anos` (agora **16 casos** no arquivo) |

**Como:** tudo por `monkeypatch` em `_executar_select` / `_executar_consulta` /
`_previa_inventario` / `_calcular_kpis` — **nenhum acesso ao Firebird** e nenhum display aberto.
`tests/test_dashboard_screen_helpers.py` importa `Dashboard.Dashboard_Screen` apenas para pegar as
funções puras (o import não instancia Tk).

### 11.2 Item 4 — logging em vez de `except: pass` na UI do Dashboard

- **24 pontos** em `Dashboard/Dashboard_Screen.py` (geometria, `grab`, botão, fechar, combos,
  `loading_label`, `messagebox`, filtros) e **10** em `Dashboard/Dashboard_Charts.py` (tooltip,
  toolbar, registro de eventos) trocados de `pass` para `logger.debug('<o que falhou>',
  exc_info=True)`. **0** `pass` soltos restantes nos dois arquivos.
- **Sem mudança de comportamento:** o nível padrão do logger é `INFO`; as mensagens só aparecem com
  `INVENTARIO_LOG_LEVEL=DEBUG` (ver Item 6.2).

### 11.3 B3 — código morto no tooltip (aprovado junto)

- Removidas 3 linhas mortas do loop de linhas em `adicionar_tooltip`
  (`Dashboard_Charts.py`): `px`/`py` via `ax.transData.transform` e `dist` via `np.hypot`
  (o valor era sobrescrito logo abaixo por `dist = abs(dados_x[idx] - event.xdata)`).

### 11.4 Validação e estado

- `compileall` OK; `pytest tests -q` → **183 passed** em 15 arquivos (139 anteriores + 44).
- **Docs sincronizados:** `docs/Status_Refatoracao.md` (Fase 5 por arquivo, working tree, Fase 6,
  item 9.7 e parágrafos desta sessão), `docs/Plano_Refatoracao_Inventario_Tools_v2.md` (v5.2 —
  Fases 3.1/3.3/5.2/5.3/6, §5.4/§5.8, Features 1/2, roadmap/horas e §8) e `AGENTS.md` (estrutura,
  capa de dados do Dashboard, convenção de logging).
- **Edições do usuário encontradas no caminho (não revertidas):** `loading_label` em
  `Dashboard_Screen.py` e `'03'` em `QUERY_DISTORCAO_SALDO` (`Queries/Consulta_Queries.py`).
- **Não commitado.** Nada de git foi alterado por esta sessão.

---

## 12. B2 — FALHA SILENCIOSA DA PREVISÃO DE INVENTÁRIO — **APLICADO em 26/10/2026** (sem commit)

**Problema:** se `QUERY_MOVIMENTO_ESTOQUE_CUSTO` falhasse, `_executar_consulta` registrava o erro e
devolvia **0**; `_previa_inventario` então devolvia `saldo + 0` e o card "Previsão de Inventário"
mostrava o **valor do inventário** como se fosse uma estimativa válida — erro invisível.

**Correção (2 arquivos):**
- `Dashboard/Dashboard_Func.py`
  - `_executar_consulta(query, params=None, padrao_em_erro=0)`: novo parâmetro; o `except` devolve
    `padrao_em_erro` (default **0** preserva todo o comportamento existente).
  - `_previa_inventario`: chama com `padrao_em_erro=None` e devolve **`None`** quando a consulta
    falha (+docstring). Resultado **NULL** legítimo continua virando **0** (não é erro).
  - `_calcular_kpis`: quando a previsão é `None`, grava `previa_inventario = 'Erro'` e
    `previa_inventario_num = 0.0`. `Dashboard_Screen._atualizar_dashboard` já lê a string pronta —
    **nenhuma mudança na UI**.
- `tests/test_dashboard_func.py` (**+6 casos**, 27 → 33 no arquivo): `test_falha_na_consulta_devolve_none`,
  `test_pede_none_em_erro_para_nao_mascarar_a_falha`, `test_falha_na_previa_mostra_erro_no_card`,
  `test_falha_usa_o_padrao_em_erro_informado`, `test_falha_sem_padrao_mantem_zero`,
  `test_resultado_nulo_nao_e_tratado_como_erro`; `_fake_consulta` passou a aceitar `**kwargs`
  (o novo parâmetro) e `test_movimento_nulo_mantem_o_inventario` agora fakes `query_executor`
  retornando `[(None,)]`, exercitando o caminho real (NULL → 0).

**Validação:** `pytest tests -q` → **209 passed**; `compileall` OK.

**Limitação conhecida (não tratada):** se `QUERY_INVENTARIO` falhar, `valor_inventario` vira 0 (card
de inventário mostra `'0,00'`) e a previsão passa a ser **só o movimento**. O B2 cobre a falha da
consulta **da previsão**; sinalizar a falha do inventário nos dois cards é decisão à parte.

**Não commitado.** Nada de git foi alterado por esta sessão.

