# Plano de Refatoração — Inventario_Tools

**Versão do sistema:** 2.0.0 (em evolução)
**Autor:** Daniel Amorim (com colaboração de Cícero Romão nas consultas SQL)
**Licença:** CC0 1.0 Universal (domínio público)
**Documento atualizado em:** 28/08/2026
**Versão do documento:** 3.0 (reescrito — consistente com o estado atual do código e com os novos problemas identificados)

> Este documento atualiza o plano original (`Plano_Refatoracao_Inventario_Tools.pdf`) e as revisões 1.x/2.0. Ele incorpora as **modificações já feitas no projeto** (branch `QoL`, agora integrada ao `main`, e branch de trabalho `refatoracao_v3.5`) e adiciona **novos problemas de código** encontrados na análise, que não eram abordados nas versões anteriores.

---

## Sumário

1. Análise do Projeto (estado atual)
2. Modificações já realizadas
3. Plano de Refatoração (fases)
4. Novos Problemas Identificados (N1–N9)
5. Novas Features
6. Roadmap de Execução
7. Dependências Novas

---

## 1. Análise do Projeto (estado atual)

### 1.1 Visão Geral

O Inventario_Tools é uma ferramenta desktop em Python para auxiliar técnicos responsáveis por inventário. Conecta-se a bancos de dados Firebird (sistema Sistech), permitindo consultas de valores e produtos problemáticos, e executar comandos de correção de dados diretamente no banco.

O projeto vem sendo evoluído ativamente. A evolução recente concentrou-se na camada de interface (`Inv_Screen/`), no gerenciamento de container de janelas (`ContainerManager`) e na seleção de período. A refatoração estrutural mais profunda (segurança, duplicação, arquitetura, testes) ainda está pendente e é o objeto deste plano.

### 1.2 Funcionalidades Principais

- Conexão com bancos de dados Firebird remotos/locais
- Consultas de valores (Inventário, Vendas, Compras)
- Consultas de problemas em produtos (preço de custo zerado, saldo não zerado, distorção de saldo, classificação nula, quantidade exorbitante, controla estoque, preço custo > venda, etc.)
- Comandos de correção em massa no banco (atualizar preços, corrigir saldos, ajustar estoque, etc.)
- Correção de distorção de saldo entre tabelas IN01LAN e IN01PRO
- Seleção de período (Anual / Mensal / Personalizado) na tela inicial
- Tutorial interativo integrado
- Configuração de tema (Claro/Escuro/Sistema)
- Cópia de valores para a área de transferência

### 1.3 Estrutura de Pastas (atual)

```
Inventario_Tools/
+-- Inventario.py                  # Arquivo principal (entry point)
+-- config.ini                     # Arquivo de configuração
+-- requirements.txt               # Dependências do projeto
+-- Banco_de_Dados/                # Camada de banco de dados
|   +-- Conexao_Banco_Dados/       # ConfiguracaoBanco, BancoDeDados (pool)
|   +-- Tela_Banco_Dados/          # Tela de configuração de conexão + funcs
+-- Comandos/                      # Comandos de correção no BD
|   +-- Comandos_Gerais/           # Tela e lógica dos comandos
|   +-- Distorcao_Saldo/           # Correção de distorção de saldo
+-- Configuracoes/                 # Configurações do sistema (tema)
+-- Consultas/                     # Consultas ao banco (11 tipos + hub)
|   +-- Generics_Functions/        # Funções compartilhadas (prod_get, copy_val...)
|   +-- Consultas_Screen.py        # Hub com os botões de consulta
|   +-- Consultas_Val_Screen.py    # Container base (Toplevel) das consultas
|   +-- <cada consulta>/           # *_Screen.py, *_List.py, *_Func.py
+-- Interface_Tools/               # Componentes reutilizáveis de UI
|   +-- Tk_Tooltip.py
|   +-- Tk_Progress_Bar.py
|   +-- Container_Screen_Managment/# Gerenciamento de Toplevels (ContainerManager)
+-- Inv_Screen/                    # Tela principal (frames)
|   +-- Inv_Top_Frame.py           # Botões BD/Consultas/Comandos + seleção de período
|   +-- Inv_Bot_Frame.py           # Dados da empresa após conexão
+-- Outros/                        # Recursos auxiliares
|   +-- Banco_Images.py            # Imagens embutidas (base64)
|   +-- Periodo_Inventario.py      # Cálculo/formatação de período (datas)
+-- Thread_Manager/                # Concorrência e pool de BD
|   +-- Gerenciador_Thread_BD.py   # Pool de conexões Firebird
|   +-- Query_Operations.py        # query_selector / query_updater / query_executor
|   +-- Thread_Executor.py         # thread_execução
+-- Tutorial/                      # Tutorial interativo
```

### 1.4 Arquitetura do Código

Convenção **Screen + Func**: cada funcionalidade possui `*_Screen.py` (interface) e `*_Func.py` (lógica/queries). Toda interação com o banco passa por `thread_execução()`, que executa funções em threads e usa callbacks para atualizar a UI na thread principal. As consultas usam um container compartilhado (`Consultas_Val_Screen`) posicionado pelo `ContainerManager`.

O acesso ao banco é centralizado em `BancoDeDados` (classe com estado estático/pool único) e `GerenciadorThreadBD` (pool de conexões Firebird). `Query_Operations` expõe `query_selector` / `query_updater` / `query_executor`.

Fluxo de execução:

```
Inventario.py (entry point)
  +-- Inv_Top_Frame.py -> Botões: Banco (B), Consultas (F1), Comandos (F2) + período
       +-- Banco_de_Dados_Screen -> Conexão ao Firebird (BancoDeDados + GerenciadorThreadBD)
       +-- Consultas_Screen -> Hub com botões de consulta
       |    +-- Cada consulta -> Screen + List + Func -> Thread_Executor
       +-- Comandos_Screen -> Tela com checkboxes -> Comandos_Func (UPDATE em lote)
       +-- Config_Screen -> Configurações de tema
  +-- Inv_Bot_Frame.py -> Preenche dados da empresa após conexão
```

---

## 2. Modificações Já Realizadas

Desde a versão original do plano, o projeto recebeu as seguintes mudanças — todas integradas ao `main` via *pull request* #14 (branch `QoL`). A correção do cálculo de janeiro foi incluída no commit `2e93463` dentro desse mesmo PR. A branch de trabalho da refatoração atualmente em uso é **`refatoracao_v3.5`**.

| Mudança | Arquivos | Commit / Status |
|---|---|---|
| Tela inicial extraída em módulos de frames | `Inv_Screen/Inv_Top_Frame.py`, `Inv_Screen/Inv_Bot_Frame.py` | `d607624` / Feito |
| Seleção de período (Anual/Mensal/Personalizado) via rádios e combos | `Inv_Screen/Inv_Top_Frame.py`, `Outros/Periodo_Inventario.py` | `97fc060`, `7d77a69` / Feito |
| Gerenciador de containers compartilhado entre janelas de consulta | `Interface_Tools/Container_Screen_Managment/Container_Manager.py` | `4aed6a4`, `5c703ee` / Feito |
| Atalhos de teclado F1 (Consultas), F2 (Comandos), B (Banco) | `Inv_Screen/Inv_Top_Frame.py` | `dbf0c1e` / Feito |
| Barra de progresso em telas-chave | `Interface_Tools/Tk_Progress_Bar.py` | `c624549`, `cc41af0` / Feito |
| Correção de janeiro no cálculo de período | `Outros/Periodo_Inventario.py` | `2e93463` / Feito (commitado) |

> **Nota sobre datas:** A estrutura de datas foi migrada de `Datas_Config.py` para `Outros/Periodo_Inventario.py`. **Este arquivo (`Datas_Config.py`) não existe mais**; as funções equivalentes são `calcular_periodo()`, `periodo_padrao()` e `formatar_banco()` em `Outros/Periodo_Inventario.py`. O plano original (Fase 5 de testes) referenciava `date_treat()` / `data_select_ini()`, que não existem mais.

> **Nota sobre branches:** As modificações acima foram consolidadas no `main` via PR #14 (merge `48e7fe3`). A refatoração estrutural deste plano é conduzida na branch `refatoracao_v3.5`.

---

## 3. Plano de Refatoração

Organizado em fases sequenciais; cada fase gera valor independente. Os problemas N1–N9 (Seção 4) integram as fases correspondentes.

### Fase 0 — Preparação (Pré-requisitos)

- Verificar baseline (projeto roda sem erros) na branch `refatoracao_v3.5`
- Criar estrutura `tests/` funcional (hoje existe um diretório `tests/` **vazio**, sem arquivos)
- Registrar os comandos de execução/lint/teste do projeto em `AGENTS.md`

---

### Fase 1 — Segurança e Configuração

#### 1.1 Parametrizar queries (SQL Injection)

**Problema:** As queries são construídas com f-strings interpolando valores na string e executadas via `cursor.execute(query)` sem parâmetros (`Thread_Manager/Query_Operations.py:9,21`).

**Arquivos afetados:**
- `Comandos/Comandos_Gerais/Comandos_Func.py` (:9, 11, 12, 13, 16, 20)
- `Consultas/Valor_Vendas/Consultas_Val_Ven_Func.py` (datas no WHERE)
- `Consultas/Valor_Entradas/Consultas_Val_Ent_Func.py` (datas + lista CFOP)
- `Consultas/Distorcao_de_Saldo/Consultas_Dist_Saldo_Screen.py` (EXECUTE BLOCK)
- `Comandos/Distorcao_Saldo/Comandos_Dist_Saldo.py`
- `Consultas/Controla_Estoque/*`, `Consultas/Quantidade_Exorbitante/*` (datas)

**Ação:** Implementar caminho parametrizado em `Query_Operations.py` — `cursor.execute(query, params)`. Mover os valores interpolados (datas, porcentagem, operadores, CFOPs) para parâmetros sempre que possível.

**Casos especiais a tratar:**
- **`com_ger` (Comando Geral):** `Comandos_Func.py` executa SQL arbitrário digitado pelo usuário sem validação. Definir política: validar/bloquear por lista de permissão ou exigir confirmação explícita com aviso de risco.
- **CFOP list (`Val_Ent`):** lista estática interpolada em `IN ( ... )` — embora não seja entrada do usuário, deve-se validar como os demais.
- **Comandos de distorção:** `INSERT ... VALUES ('...{item[0]}'...)` só escapa aspas simples de um campo; revisar sanitização de todos os valores interpolados.

#### 1.2 Mover credenciais para config

**Arquivo:** `Banco_de_Dados/Conexao_Banco_Dados/Inventario_Conn.py:44-45`

Credentials `SYSDBA`/`masterkey` hardcoded. Adicionar seção `[Credenciais]` no `config.ini` com `user`/`password` (padrão SYSDBA/masterkey). Ler via `Config_Manager` em `_criar_conexao()`. **Nunca commitar credenciais reais.**

#### 1.3 Centralizar leitura de config

**Problema:** `salvar_diretorio()`/`carregar_diretorio()` importam `configparser` dentro da função e releem o arquivo a cada chamada (`Banco_de_Dados/Tela_Banco_Dados/Banco_de_Dados_Func.py:21-53`). Escritas não são thread-safe e não têm `try/except`. Chamadores: `Inventario.py:13`, `Banco_de_Dados_Func.py`, `Config_Func.py`.

**Ação:** Criar `Configuracoes/Config_Manager.py` com classe `AppConfig` que:
- Carrega `config.ini` uma vez no `__init__`
- Expõe `get(section, key)` e `set(section, key, value)`
- Salva apenas quando necessário (método `save()`)
- Usa caminho absoluto (não relativo ao CWD) e encoding explícito (UTF-8)

---

### Fase 2 — Eliminar Código Duplicado

#### 2.1 Unificar `banco_codigo_valueform()`

Duplicada em 3 arquivos (lógica idêntica):
- `Consultas/Valor_Inventario/Consultas_Val_Inv_Func.py`
- `Consultas/Valor_Vendas/Consultas_Val_Ven_Func.py`
- `Consultas/Valor_Entradas/Consultas_Val_Ent_Func.py`

Mover para `Consultas/Generics_Functions/Gen_Funcs_Consulta.py` e deletar as 3 cópias.

```python
def banco_codigo_valueform(val: float) -> str:
    val = "{:,.2f}".format(val)
    prs = val.split('.')
    pri = prs[0].replace(',', '.')
    return pri + ',' + prs[1]
```

#### 2.2 Unificar `copy_val()`

Existem cópias em 4 arquivos; 3 com prefixo `'R$ '` e a genérica sem prefixo (`Gen_Funcs_Consulta.py`). Unificar em uma única função com parâmetro `prefix` opcional:

```python
def copy_val(label_widget, prefix: str = ''):
    import pyperclip
    text = label_widget.cget("text")
    pyperclip.copy(f'{prefix}{text}' if prefix else text)
```

Arquivos: `Gen_Funcs_Consulta.py`, `Val_Inv_Func.py`, `Val_Ven_Func.py`, `Val_Ent_Func.py`.

#### 2.3 Extrair lógica comum de listagem (Treeview)

O mesmo padrão (Toplevel -> Treeview -> colunas -> query -> popular) repete-se em **8 arquivos** `*_List*.py` (Dist_Saldo, NZer, ZCusto, Classi_Pro, Precu_Preve, Preve_Precu_Precom, Contr_Estq, Quant_Maior), incluindo os helpers `Treeview_Select` (7 cópias) e `Treeview_Insert` (8 cópias).

**Ação:** criar factory/`ConsultaListagemBase` em `Interface_Tools/`:

```python
def criar_tela_listagem(parent, titulo, colunas, query) -> None:
    """Cria tela com Treeview e carrega dados via query."""
```

#### 2.4 Extrair padrão de tela de consulta (Screen)

O container base (`Consultas_Val_Screen`) já é compartilhado, mas os blocos "criar labels -> botões -> update callback -> `thread_execução`" são copiados em várias telas de contagem e nas de valor.

**Ação:** criar classe/helper `ConsultaScreenBase` para reduzir o boilerplate repetido.

---

### Fase 3 — Arquitetura e Organização

#### 3.1 Mover imports para o topo dos módulos

Imports lazy espalhados em praticamente todos os módulos. Remover quando não houver risco de circular; resolver circulares com injeção de dependência.

#### 3.2 Separar queries SQL em módulo dedicado

Criar `Consultas/Queries.py` e `Comandos/Queries.py` centralizando as strings SQL. Hoje o SQL é inline e **duplicado** em cada par Screen/List (vários pares usam o mesmo WHERE). **Não existe** módulo central (`Queries.py`) hoje.

```python
# Consultas/Queries.py
QUERY_VALOR_INVENTARIO = "select sum(...) from in01pro where ..."
QUERY_VALOR_VENDAS = "select sum(...) from in01fat f where ..."
QUERY_PRECO_CUSTO_ZERADO = "select count(*) from in01pro where precu = 0 ..."
```

#### 3.3 Tratar erros adequadamente

- `Consultas/Valor_Inventario/Consultas_Val_Inv_Func.py` — `except:` genérico → `except (DatabaseError, TypeError) as e:`
- `Banco_de_Dados/Tela_Banco_Dados/Banco_de_Dados_Func.py:269-282` — `obter_caminho_curto_banco_dados` **não retorna `caminho_longo`** no `except` (o comentário promete retornar o original); falta `return caminho_longo`
- Adicionar `logging` em vez de `print()` (ver 3.4)

#### 3.4 Limpar `print()` de debug

- `Thread_Manager/Gerenciador_Thread_BD.py:17-19` (banner + bug cosmético de concatenação sem espaço)
- `Banco_de_Dados/Tela_Banco_Dados/Banco_de_Dados_Func.py:278,282`
- `Consultas/Distorcao_de_Saldo/Consultas_Dist_Saldo_Screen.py`

Substituir por `logging.debug()` / `logging.info()`.

---

### Fase 4 — Type Hints e Assinaturas

#### 4.1 Adicionar type hints

Hoje há apenas ~13 anotações de parâmetro no projeto inteiro e **zero** `-> return`. Tipar parâmetros, retornos e variáveis de classe em todos os módulos.

#### 4.2 Criar `py.typed`

Criar marker `py.typed` na raiz para indicar suporte a type checking.

---

### Fase 5 — Testes Unitários

#### 5.1 Configurar pytest

Adicionar `pytest` ao `requirements-dev.txt`; criar `conftest.py` com fixtures para mock de conexão Firebird. O diretório `tests/` atualmente está **vazio** — precisa ser populado.

#### 5.2 Testar funções puras (sem UI)

| Função | Arquivo (atual) | Tipo de Teste |
|---|---|---|
| `banco_codigo_valueform()` | Gen_Funcs_Consulta.py | Formatação de valores |
| `copy_val()` | Gen_Funcs_Consulta.py | Mock pyperclip |
| `precu_porcent_entry_validate()` | Comandos_Func.py | Validação de entrada |
| `calcular_periodo()` / `formatar_banco()` | Outros/Periodo_Inventario.py | Formatação de datas (antigo Datas_Config) |
| `_montar_operacoes()` | Comandos_Func.py | Lógica de ordenação |

#### 5.3 Testar queries isoladamente

Testes de integração com Firebird em memória (se suportado) ou mocks de `query_selector`/`query_updater`.

---

### Fase 6 — Compatibilidade com PyInstaller

- Rodar `pyinstaller` e validar módulos embutidos, `config.ini` via `--add-data`, e `fbclient.dll` em runtime
- Revisar `Auto_py_to_exe config.json` após reorganização de módulos

---

## 4. Novos Problemas Identificados (N1–N9)

Itens que não eram abordados no plano original. Devem ser tratados em conjunto com as fases acima.

### N1. Queries de comando sempre falsas (lógica quebrada)

**Arquivo:** `Comandos/Comandos_Gerais/Comandos_Func.py:11-12`

```sql
-- linha 11
UPDATE IN01PRO SET PRECU = VLDIA WHERE VLDIA {op} VLDIA AND VLDIA > 0
-- linha 12
UPDATE IN01PRO SET PRECU = CUSME WHERE CUSME {op} CUSME AND CUSME > 0
```

Com `op` = `>` ou `<`, a condição `VLDIA > VLDIA` (ou `<`) é **sempre falsa** → os comandos "Preço de Custo = Preço de Compra" e "Preço de Custo = Custo Médio" **nunca executam**. Falta a coluna de comparação alvo.

**Ação:** corrigir a condição para comparar contra a coluna correta (ex.: `WHERE VLDIA > PRECU`), definindo a semântica desejada com o usuário.

### N2. UnboundLocalError em ven_get / ent_get

**Arquivos:** `Consultas/Valor_Vendas/Consultas_Val_Ven_Func.py`, `Consultas/Valor_Entradas/Consultas_Val_Ent_Func.py`

Se `query_executor` lançar erro, o `except` mostra o `messagebox`, mas o fluxo continua para `if valrec is not None:` (`valrec`/`valent`), onde a variável **nunca foi atribuída** → `UnboundLocalError` na thread de trabalho.

**Ação:** retornar/finalizar no `except` (e padronizar `else`), evitando uso de variável não atribuída.

### N3. Threads chamando Tk (não thread-safe)

Vários pontos fazem chamadas Tk a partir de threads de trabalho (viola threadsafety do Tk):
- `Comandos_Func.py` — `progress_bar.create_screen()`, `atualizar_status()`, `comando.after()` dentro de `executa_comandos` (thread)
- `Banco_de_Dados_Func.py` — `progress_bar.create_screen()` em `executa_conexao` (thread)
- Messagebox chamados de dentro de threads em `Val_Ven`/`Val_Ent`/`Val_Inv` Func

**Inclui:** risco de `TclError: bad window path name` ao fechar uma tela enquanto a query ainda roda, pois `Thread_Executor.py:29-41` faz `master.after(100, check_thread)` sem guarda contra widget destruído.

**Ação:** garantir que toda manipulação de Tk ocorra na thread principal (via `master.after(0, ...)`/callbacks), e adicionar guarda de widget destruído no polling do `Thread_Executor`.

### N4. Pool de conexões frágil

**Arquivo:** `Thread_Manager/Gerenciador_Thread_BD.py`

- Leak de conexões se a inicialização falhar parcialmente
- `fechar()` usa `Queue.empty()` (não thread-safe) e engole erros
- Sem health-check/reconexão — conexões obsoletas são reutilizadas
- `_devolver_conexao` pode mascarar o erro original e/ou vazar conexão
- `trocar_bd` definido mas nunca usado — reutilizaria conexões do banco antigo

**Ação:** robustecer o pool (fechamento ordenado, health-check, tratamento de erros), decidir se `trocar_bd` deve ser usado ou removido.

### N5. Erros de entrada não tratados

- `Banco_de_Dados/Conexao_Banco_Dados/Inventario_Conn.py:41` — `int(ConfiguracaoBanco.port)` lança `ValueError` se a porta não for numérica (mensagem não amigável)
- `Banco_de_Dados/Tela_Banco_Dados/Banco_de_Dados_Func.py:171` — `propri[0]` lança `IndexError` se a query PROPRI não retornar linhas
- Race double-destroy em `_disparar_queries` (callbacks podem chamar `finalizar()` duas vezes → `destroy()` duplo)

**Ação:** validar porta, tratar consulta PROPRI vazia, e adicionar salvaguarda para não finalizar/destroy mais de uma vez.

### N6. config.ini — encoding e seções duplicadas

O arquivo contém `[Tema]` e `[Configurações]` redundantes (`config.ini:11-15`), e a seção é gravada em CP1252 (round-trip com encoding do locale em `Banco_de_Dados_Func.py:38`), o que **corrompe o nome da seção** (aparece como `[Configura��es]` — acento corrompido). O padrão `'System'` em `Inventario.py:16-17` mascara a falha ao ler o tema.

**Ação:** consolidar numa única seção de tema e gravar com encoding UTF-8 explícito (alinhado à Fase 1.3 – Config_Manager).

### N7. Correções de UI menores

- `Consultas/Valor_Entradas/Consultas_Val_Ent_Screen.py` — botão "Copiar Valor" nunca é desabilitado durante a consulta (as demais telas desabilitam)
- Telas de listagem (`*_List*.py`, 8 arquivos) não tratam ESC/WM_DELETE e não liberam `grab_set()`
- `Consultas/Consultas_Val_Screen.py:12` chama `cm.posicionar_container(hub)` sem `try/except` — `ContainerManager` pode lançar `RuntimeError` quando não há posição livre
- `Interface_Tools/Tk_Tooltip.py:30` usa `self.widget.bbox("insert")` que pode retornar vazio e quebrar o unpack → `ValueError`
- `Outros/Banco_Images.py:15` — `help_base64_image` começa com vírgula inválida (funciona só porque `base64.b64decode` ignora caracteres inválidos por padrão; é frágil e deve ser removida)

**Ação:** tratar os pontos acima conforme descrito.

### N8. Limpeza de imports/lixo em arquivos de Valor

**Arquivos:** `Consultas/Valor_Vendas/Consultas_Val_Ven_Func.py`, `Consultas/Valor_Entradas/Consultas_Val_Ent_Func.py`

Após a migração da lógica de datas, restaram trechos órfãos/desorganizados:
- Bloco de comentários e linhas vazias referentes à importação removida de datas em `Consultas_Val_Ven_Func.py` (linhas 25–29)
- Imports e organização inconsistente entre os três arquivos `Valor_*_Func.py`

**Ação:** limpar comentários órfãos, padronizar imports no topo e alinhar a estrutura dos três arquivos de valor.

### N9. Consolidar animação de status duplicada

**Arquivos:** `Interface_Tools/Tk_Progress_Bar.py` (`_iniciar_ciclo_mensagens`) e `Banco_de_Dados/Tela_Banco_Dados/Banco_de_Dados_Func.py` (`_iniciar_animacao`/`parar_animacao`, linhas 95–111)

Existem dois mecanismos independentes de animação via `after()`/`tick()` para feedback de status. São a mesma ideia (animar um `Label` com `.`/`..`/`...` e suportar cancelamento).

**Ação:** consolidar em um único helper de animação reutilizável (ex.: em `Interface_Tools/`), eliminando a duplicação e o ciclo de `after` não cancelado.

---

## 5. Novas Features

Implementadas após a refatoração base (Fases 1–3), pois dependem de queries centralizadas e funções unificadas.

### Feature 1 — Dashboard Visual

Tela principal pós-conexão com KPIs e gráficos resumidos do inventário.

| Métrica | Query | Tipo de Visual |
|---|---|---|
| Valor total do Inventário | QUERY_VALOR_INVENTARIO | KPI Card |
| Valor total de Vendas | QUERY_VALOR_VENDAS | KPI Card |
| Valor total de Compras | QUERY_VALOR_ENTRADAS | KPI Card |
| Preço Custo Zerado | QUERY_PRECO_CUSTO_ZERADO | Card + Barra |
| Saldo Não Zerado | QUERY_PRODUTOS_NAO_ZERADOS | Card + Barra |
| Classificação Nula | QUERY_CLASSIFICACAO_NULA | Card + Barra |
| Qtd > 999999 | QUERY_QUANTIDADE_EXCESSIVA | Card + Barra |
| Distorções de Saldo | QUERY_DISTORCAO_SALDO | Card + Barra |
| Total problemas | Soma dos anteriores | Card status |

**Estrutura de pastas** (módulo `Dashboard/`):

```
Dashboard/
+-- __init__.py
+-- Dashboard_Screen.py    # Tela principal com gráficos
+-- Dashboard_Func.py      # Queries de resumo e formatação
+-- Dashboard_Charts.py    # Funções de criação de gráficos
```

**Arquivos a modificar:** `Inv_Screen/Inv_Top_Frame.py` (botão "Dashboard"), `Inventario.py`, `requirements.txt` (adicionar `matplotlib`).

Gráficos com `matplotlib` + CustomTkinter via `FigureCanvasTkAgg`. Saúde do banco: `saude = 100 - (total_problemas / total_produtos * 100)`; verde > 90%, amarelo 70–90%, vermelho < 70%.

### Feature 2 — Validação Pré-Inventário

Checklist que roda todas as verificações de uma vez e apresenta o status de cada uma, com contagem e ação corretiva.

**Estrutura de pastas:**

```
Validacao/
+-- __init__.py
+-- Validacao_Screen.py    # Tela do checklist
+-- Validacao_Func.py      # Lógica de validação e scoring
+-- Validacao_Itens.py     # Definição de cada regra
```

**Regras de validação:**

| # | Regra | Severidade | Ação Corretiva |
|---|---|---|---|
| 1 | Preço de custo zerado com saldo > 0 | Crítico | Comando 'Preço Custo zerado' |
| 2 | Classificação do produto nula | Alto | Comando 'Corrigir Classificação' |
| 3 | Saldo entre 0 e 0.01 | Alto | Comando 'Zerar Não Zerados' |
| 4 | Saldo negativo | Crítico | Comando 'Zerar Saldo Negativo' |
| 5 | Quantidade > 999999 | Médio | Comando 'Corrigir Qtd Alta' |
| 6 | Preço custo > preço venda | Médio | Manual |
| 7 | Controla estoque = N | Baixo | Comando 'Setar Controla Estoque' |
| 8 | Distorção de saldo | Crítico | Tela de distorção |
| 9 | Preços custo/compra/venda zerados | Médio | Manual |
| 10 | DTOPE diferente de DTPRO | Baixo | Comando 'DTOPE = DTPRO' |

**Funcionalidades-chave:** checklist interativo com status/contagem, drill-down, correção em lote, exportação TXT/CSV e revalidação.

---

## 6. Roadmap de Execução

### 6.1 Ordem Ideal de Execução

A execução deve considerar que os **novos problemas (N1–N9)** integram as fases correspondentes. Ordem sugerida:

| Passo | Item | Objetivo | Tempo Est. |
|---|---|---|---|
| 1 | Fase 0 — Preparação | Baseline e estrutura de testes | 30 min |
| 2 | Fases 2.1–2.2 — Unificar funções | Eliminar duplicação | 2 h |
| 3 | **N1** — Corrigir queries sempre falsas | Corrigir lógica quebrada | 30 min |
| 4 | Fase 1.1 + **N2** — Parametrizar queries | Corrigir SQL injection + UnboundLocal | 3 h |
| 5 | Fases 3.3–3.4 + **N5** — Tratar erros/logging | Melhorar robustez | 1.5 h |
| 6 | Fase 3.2 — Queries centralizadas | Base para features | 2 h |
| 7 | Fases 1.2–1.3 + **N6** — Config centralizada | Organizar config | 2 h |
| 8 | Fase 4 — Type hints | Melhorar legibilidade | 2 h |
| 9 | Fases 2.3–2.4 + **N7** — Patterns de UI | Reutilizar código | 3 h |
| 10 | **N8** — Limpeza imports Valor_* | Organizar imports | 30 min |
| 11 | **N9** — Consolidar animação | Eliminar duplicação de status | 1 h |
| 12 | **N3** — Thread-safe Tk | Corrigir chamadas Tk em threads | 2 h |
| 13 | **N4** — Pool de conexões | Robustecer pool | 2 h |
| 14 | Fase 3.1 — Lazy imports | Organizar imports | 1 h |
| 15 | Fase 5 — Testes unitários | Garantir qualidade | 3 h |
| 16 | Fase 6 — PyInstaller | Validar executável | 1 h |
| 17 | Feature: Validação Pré-Inventário | Checklist automático | 4 h |
| 18 | Feature: Dashboard Visual | Visão geral com gráficos | 5 h |

### 6.2 Tempo Estimado Total

| Categoria | Horas Estimadas |
|---|---|
| Refatoração (Fases 0–6 + N1–N9) | 28–32 h |
| Feature: Validação Pré-Inventário | 4–5 h |
| Feature: Dashboard Visual | 5–6 h |
| **TOTAL** | **37–43 h** |

### 6.3 Ganho Esperado

- Redução de ~40% em código duplicado
- Eliminação de riscos de SQL injection
- Correção de bugs reais (comandos sempre falsos, UnboundLocalError, Tk em threads)
- Código tipado, testável e com queries centralizadas
- Dashboard e Validação automática antes de fechar inventário
- Base sólida para futuras expansões

---

## 7. Dependências Novas

| Dependência | Versão | Uso |
|---|---|---|
| matplotlib | >= 3.7.0 | Gráficos do Dashboard |
| pytest | >= 7.0 | Testes unitários (dev) |
| fpdf2 | >= 2.8 | Geração de PDFs (opcional) |
