# AGENTS_SESSAO.md — Instruções para Próximas Sessões

**Agente responsável:** **NEXO** (sessão de refatoração de datas / Inventario_Tools)
**Última sessão:** 21/10/2026 — **Caça à performance ENCERRADA por medição (decisão do usuário)**.
Medição pós-otimização (script `%TEMP%\opencode\medir_*.py`, só SELECTs, banco = **cópia de cliente**)
mostrou que **não sobrou correção de SQL de alto retorno**: o que resta em `KPI previa` (~20 s)
é **I/O**, não defeito de query. Duas hipóteses foram **testadas e derrubadas**:
(a) filtrar a CTE `saidas` por período → 23,05 s (pior) **e resultado diferente**
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
**Próximo passo (aberto neste momento):** **visual do gráfico do Dashboard** — resize da figura
(hoje fixa em `7.0x2.8`), rótulos densos com 61 meses, contraste da mensagem "Nenhum dado
encontrado", formatação do eixo Y e valores nas barras. Ver Item 8.
**Pendências herdadas:** testes manuais (troca de período + reabertura das telas);
`DROP VIEW V_LAN_COM` / `V_DIFF_ENTRADA_SAIDA_MES` no banco (SQL a cargo do usuário — Item 6.8).
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
