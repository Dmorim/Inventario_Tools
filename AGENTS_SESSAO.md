# AGENTS_SESSAO.md — Instruções para Próximas Sessões

**Agente responsável:** **NEXO** (sessão de refatoração de datas / Inventario_Tools)
**Última sessão:** 19/10/2026 — E6a/E6b (Comandos → classe `Funcoes_Comandos` + período snapshot; testes atualizados) e E5 (Dashboard → snapshot + gráfico de tendência com janela fixa de 5 anos-calendário até a data final) concluídos; 69 testes passando.
**Próxima sessão (pendente):** etapa **E7** — remover propriedades legadas `data_banco_*` de `Inventario.py` (verificar 0 usos restantes).
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

## 5. ESTADO ATUAL DA REFATORAÇÃO DE DATAS

**Concluído (resumo):**
- Mapeamento dos 11 grupos de consultas vs Plano v2; varredura `dt_ini`/`dt_fim` com **0 resíduos**.
- Telas de consulta migradas para snapshot de período.
- **Comandos (E6a/E6b):** `Comandos_Screen(periodo, parent)`; lógica migrada para a classe `Funcoes_Comandos` (período snapshot, sem `self.data_banco_inicial`); check de distorção via `DistorcaoManager.possui_itens()`; aliases de compatibilidade no módulo (`Comandos_Func`, `montar_operacoes`, `comandos_true`, `on_click_confirm`, `precu_porcent_entry_validate`) preservam legado/tests; `tests/test_comandos_func.py` migrado para `Funcoes_Comandos` + `FakePeriodo`.
- **Dashboard (E5):** `Dashboard_Screen(periodo, parent, button)` — comportamento "sob demanda" (snapshot na abertura, **sem listener**); KPIs usam o período selecionado; **gráfico de tendência usa janela fixa de 5 anos-calendário terminando na data final** (helper `Outros/Periodo_Inventario.periodo_tendencia_ultimos_5_anos`).
- Testes e `compileall` verdes (**69 passed**).

**Ainda pendente (próximos passos):**

| Etapa | O que é | Prioridade |
|---|---|---|
| **E7** | Remover propriedades legadas `data_banco_*` de `Inventario.py` (linhas ~47-53); confirmar 0 usos de `app_self.data_banco_*` | **Próximo passo imediato** |
| **E1a** | Criar `tests/test_periodo_manager.py` (igualdade, imutabilidade, notificação de listeners) | pode ser feito a qualquer momento |
| **E8** | Regressão final + docs (sem commit automático) | ao final |

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
