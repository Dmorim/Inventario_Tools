# AGENTS_SESSAO.md — Instruções para Próximas Sessões

**Agente responsável:** **NEXO** (sessão de refatoração de datas / Inventario_Tools)
**Última sessão:** 22/10/2026 — sessão de **diagnóstico do Dashboard** (sem alteração de
código de produção): o KPI "Total de Entradas" (951.529,18 em 2025) e a série "Entradas" do
gráfico (rótulo "278 mil") usam **fórmulas SQL diferentes** — o gráfico soma o valor
**unitário** (`SUM(l.valor)`) e ignora a **quantidade**, o desconto, o `valsub` e o IPI.
Correção proposta (fonte única de verdade para a expressão) **aguardando aprovação** do
usuário — ver **Item 9**. Também: o usuário commitou `9100308` ("Improve dashboard chart
readability"), que fechou o visual do gráfico do Dashboard (itens A–G + contraste WCAG), e
executou `git rm --cached config.ini` (Item 6.10 — desrastreamento feito; **rotação da senha
ainda pendente**).
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
**Próximo passo (neste momento):** **correção da fórmula de "Entradas" no gráfico** — ✅
**APLICADA e validada no banco** (Item 9.2; KPI e gráfico agora coincidem em 2024/2025/2026).
**Restam apenas decisões de negócio** sobre as divergências latentes do Item 9.5 (classe `'03'`
na distorção, filtro `l.cance` nas entradas, classe `'07'` no inventário) — o agente **não
decide** isso sozinho. Nenhuma outra etapa de código aberta.
**Pendências herdadas:** testes manuais (troca de período + reabertura das telas);
`DROP VIEW V_LAN_COM` / `V_DIFF_ENTRADA_SAIDA_MES` no banco (SQL a cargo do usuário — Item 6.8);
**rotação da senha do banco** (`config.ini` já foi desrastreado — Item 6.10).
**Branch:** `refatoracao_v3.5`
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

Estado de referência saudável: **69 passed**, `compileall` sem erros.
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

### 6.2 Loggers — somente logs de saída
- **Registrar apenas logs de saída/resultados**: valores finais, respostas de consulta,
  totals, conclusões, erros e exceções.
- **NUNCA criar log de início de função** (não registrar "iniciando...", "entrando em...",
  "chamado por..." nem qualquer linha de entrada/execução).
- Quando um logger for adicionado a uma função, ele deve aparecer **uma única vez**, no
  ponto de retorno/conclusão ou no tratamento de erro — não na abertura do corpo.
- **Uma única camada registra cada evento:** a infraestrutura (`Query_Operations`,
  `Thread_Executor`) registra conclusões de query/thread em `debug`; o módulo de negócio
  (ex.: `ven_get`, `prod_get`, `carregar_kpis`) registra o resultado final em `info`.
  Nunca ambos em `info` para o mesmo evento (duplicação de linha no arquivo de log).
- **Nível de log configurável por env var:** `INVENTARIO_LOG_LEVEL` (`DEBUG`, `INFO`...)
  com fallback `INFO` — lido em `Outros/Logger/Get_Logger.py`. Para diagnóstico, rodar a
  aplicação com `$env:INVENTARIO_LOG_LEVEL='DEBUG'` (PowerShell) sem alterar código.
- Estado atual (19/10/2026): **53 chamadas de logger** no código de produção
  (24 exception, 15 info, 6 warning, 5 debug, 3 error) — todas de saída/conclusão/erro.

### 6.3 Segurança e dados
- **Nunca** gravar credenciais em arquivo versionado; `Config.ini` está no `.gitignore`.
- Não commitar chaves, senhas ou `Config.ini` de forma alguma.

### 6.4 Testes
- Testes cobrem funções **puras**; não fazer testes importarem telas com UI/display.
- **Não alterar testes existentes** sem aprovação explícita; acrescentar casos novos apenas
  com plano prévio (regra Item 3).

### 6.5 Cuidados com o ambiente (lições desta sessão)
- **PowerShell 5.1**: NÃO usar `&&`, `| head`, `| tail`, `rg` (não existem). Usar
  `; if ($?) {...}`, `Select-Object -Last N`, e o Python da venv para varreduras.
- **Encoding de caminhos**: existem pastas com acento (ex.: `Consultas/Classificação_Do_Produto`)
  que o console mostra como `??`. Para acessar no Python, usar escape `'\xe7\xe3o'` ou walk,
  nunca digitar o caminho acentuado literalmente no shell.
- Scripts gerados temporários: prefira `docs/` ou temp; não deixar soltos na raiz.

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

### 6.9 SQL de DROP das views órfãs (a executar pelo usuário)
`V_LAN_COM` e `V_DIFF_ENTRADA_SAIDA_MES` já saíram do código (0 referências) mas seguem
físicas no banco. Executar **manualmente**, na ordem (a segunda depende da primeira):

```sql
DROP VIEW V_DIFF_ENTRADA_SAIDA_MES;
DROP VIEW V_LAN_COM;
```

O app não cria nem recria essas views (`Queries/Create_Views.py` só gerencia
`V_FAT_VALOR_SAIDA`). Não remover `V_FAT_VALOR_SAIDA` — está em uso.

### 6.10 `config.ini` versionado apesar do `.gitignore` — **desrastreado em 22/10/2026**
- `.gitignore` lista `config.ini`/`*.ini`, **mas** o arquivo já estava **rastreado** — o
  `.gitignore` só se aplica a arquivos **não** rastreados. `git ls-files config.ini` confirma.
- Consequência: `config.ini` (com `user_db`/`pass_db` e `dir_banco`) está no **histórico**
  do repositório (13+ commits, desde `1a91bfe`).
- **Ação do usuário em 22/10/2026:** `git rm --cached config.ini` — arquivo **mantido localmente**,
  agora respeitando o `.gitignore` (staged, aguardando commit do usuário). O `.gitignore` também
  foi limpo das linhas duplicadas (`config.ini`/`*.ini` apareciam 3×).
- **AINDA PENDENTE:** **rotacionar a senha do banco** — o histórico do repositório continua
  contendo as credenciais antigas. Limpar o histórico exigiria reescrita — **não fazer sem
  decisão explícita**.
- O agente **não** executa comandos de git que alterem índice/histórico sem aprovação.

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

### 9.2 Correção — ✅ APLICADA em 22/10/2026 (sem commit)

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

**Nota de ambiente:** `RDB$VIEWS` e `RDB$INDEX_FIELDS` **não são consultáveis** neste banco
("Table unknown") — mesmo bloqueio do Item 6.7. A view do banco foi conferida **funcionalmente**
(agregando `valor_saida` × fórmula do código), não por definição textual.

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
