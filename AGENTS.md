# AGENTS.md — Guia para agentes trabalhando no projeto

## Visão geral

Ferramenta desktop em Python/Tkinter (customtkinter) para auxiliar técnicos de inventário.
Conecta-se a bancos Firebird (fdb) e executa consultas e comandos de correção de dados.

Arquivo principal (entry point): `Inventario.py` (classe `Inventario`).

Convenção de código: cada funcionalidade é dividida em pares **Screen + Func**.
- `*_Screen.py` — interface (Tkinter/customtkinter)
- `*_Func.py` — lógica e queries

Todo acesso ao banco passa por `Thread_Manager.Query_Operations` (`query_selector`,
`query_updater`, `query_executor`) e por `thread_execução()` (`Thread_Manager.Thread_Executor`),
que executa em thread e usa callbacks para atualizar a UI na thread principal.

## Comandos

Ambiente virtual: `.venv` (Windows, PowerShell). Use o executável da venv explicitamente:

- **Rodar o programa** (a partir da raiz do projeto):
  ```powershell
  .\.venv\Scripts\python.exe Inventario.py
  ```

- **Rodar os testes** (pytest):
  ```powershell
  .\.venv\Scripts\python.exe -m pytest tests -v
  ```

- **Verificação básica de sintaxe** (não há linter/typecheck configurado):
  ```powershell
  .\.venv\Scripts\python.exe -m compileall -q . -x "\.venv"
  ```

- **Instalar dependências**:
  ```powershell
  .\.venv\Scripts\python.exe -m pip install -r requirements.txt
  # dev (pytest):
  .\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
  ```

## Estrutura de pastas

```
Banco_de_Dados/    Conexão (ConfiguracaoBanco, BancoDeDados) + tela de conexão
Comandos/          Comandos de correção no BD (Comandos_Gerais, Distorcao_Saldo)
Configuracoes/     Configurações do sistema (tema)
Consultas/         Consultas (11 tipos + hub), Generics_Functions, Consultas_Val_Screen
Interface_Tools/   Componentes de UI reutilizáveis (ToolTip, ProgressBar, ContainerManager)
Inv_Screen/        Tela principal (Top/Bot frames)
Outros/            Recursos auxiliares (imagens base64, cálculo de período)
Thread_Manager/    Concorrência e pool de conexões
Tutorial/          Tutorial interativo
tests/             Testes unitários (pytest)
```

## Notas importantes

- Os testes atualmente cobrem funções **puras**, sem interface (formatação de valores,
  validação de entrada). Evite que testes importem telas que dependem de display.
- `Config.ini` e `docs/Plano_Refatoracao_Inventario_Tools_v2.md` estão no `.gitignore`
  (config não deve ser versionado para não expor credenciais).
- Não commitar credenciais reais em nenhum arquivo.
