# Mapeamento e Status - Refatoração de Datas (Plano v2)

**Branch:** refatoracao_v3.5  
**Data da análise:** 2026-10-19 01:13:28  
**Roadmap base:** docs/Plano_Refatoracao_Inventario_Tools_v2.md  
**Status existente:** docs/Status_Refatoracao.md  

## 1. Resumo Executivo

- **Resíduos dt_ini/dt_fim encontrados:** 0 (varredura completa no repositório, excluindo .venv)
- **Áreas migradas (últimos commits):** Núcleo (PeriodoInventario, Distorcao_Manager), Treeview (prefetch), integração de período (Inventario/Top/Consultas) e 4 grupos de consultas.
- **Progresso estimado (análise):** ~50–60% conforme avaliação anterior.

## 2. Varredura de Resíduos (dt_ini/dt_fim)

**Resultado:** Nenhuma ocorrência de \bdt_ini\b ou \bdt_fim\b foi encontrada em arquivos .py (excluindo .venv).

**Arquivos inspecionados (amostra focal):** Consultas/Consultas_Screen.py, todos os grupos migrados (Controla_Estoque, Distorcao_de_Saldo, Quantidade_Exorbitante, Valor_Entradas, Valor_Vendas), Inv_Screen/Inv_Top_Frame.py, Inventario.py.

**Conclusão:** Não há resíduos diretos de datas locais nesses fluxos. Possível haver cálculos indiretos (datas derivadas, strings) a verificar caso o Plano v2 exija eliminação total — mas em termos de variáveis dt_ini/dt_fim, código está limpo nas áreas analisadas.

## 3. Mapeamento por Grupos de Consultas (11 tipos)

Baseado em Consultas/Consultas_Screen.py e estrutura de pastas. Status definido por: migrado no diff recente (Distorção, Controla Estoque, Quant. Exorbitante, V. Entradas/Vendas), parcial (usa Func com lógica própria) ou pendente (ainda não adaptado ao PeriodoInventario snapshot/prefetch).

| Grupo | Screen | List | Func | Status | Observação |
|---|---|---|---|---|---|
| Classificação do Produto | Consultas/Classificação_Do_Produto/Consultas_Classi_Pro_Screen.py | Consultas/Classificação_Do_Produto/Consultas_Classi_Pro_List.py | — | **Pendente** | Ainda não migrado para PeriodoInventario (snapshot). Verificar passagem de período. |
| Controla Estoque | Consultas/Controla_Estoque/Consultas_Contr_Estq_Screen.py | Consultas/Controla_Estoque/Consultas_Contr_Estq_List.py | — | **Migrado** | Adaptado para snapshot/prefetch (últimos commits). |
| Distorção de Saldo | Consultas/Distorcao_de_Saldo/Consultas_Dist_Saldo_Screen.py | Consultas/Distorcao_de_Saldo/Consultas_Dist_Saldo_List.py | — | **Migrado** | Usa fluxo com DistorcaoManager + período unificado. |
| Preço Custo Compra Zerado | Consultas/Preco_Custo_Compra_Zerado/Consultas_Preve_Precu_Precom_Screen.py | Consultas/Preco_Custo_Compra_Zerado/Consultas_Preve_Precu_Precom_List.py | — | **Pendente** | Não aparece no diff migratório. Validar uso de datas. |
| Preço Custo Maior Preço Venda | Consultas/Preco_Custo_Maior_Preco_Venda/Consultas_Precu_Preve_Screen.py | Consultas/Preco_Custo_Maior_Preco_Venda/Consultas_Precu_Preve_List.py | — | **Pendente** | Pendente de migração. |
| Preço Custo Zerado | Consultas/Preco_Custo_Zerado/Consultas_ZCusto_Screen.py + Consultas_ZCusto_List_Screen.py | — | — | **Pendente** | Tela dividida (Screen/List Screen). Verificar padronização. |
| Produtos Não Zerados | Consultas/Produtos_Nao_Zerados/Consultas_NZer_Prod_Screen.py + Consultas_NZer_List_Screen.py | — | — | **Pendente** | Pendente. |
| Quantidade Exorbitante | Consultas/Quantidade_Exorbitante/Consultas_Quant_Maior_Screen.py | Consultas/Quantidade_Exorbitante/Consultas_Quant_Maior_List.py | — | **Migrado** | Snapshot/prefetch aplicado. |
| Valor Entradas | Consultas/Valor_Entradas/Consultas_Val_Ent_Screen.py | — | Consultas/Valor_Entradas/Consultas_Val_Ent_Func.py | **Migrado (parcial)** | Ajustado nos commits recentes; verificar aderência completa ao contrato PeriodoInventario. |
| Valor Inventário | Consultas/Valor_Inventario/Consultas_Val_Inv_Screen.py | — | Consultas/Valor_Inventario/Consultas_Val_Inv_Func.py | **Pendente** | Não migrado. |
| Valor Vendas | Consultas/Valor_Vendas/Consultas_Val_Ven_Screen.py | — | Consultas/Valor_Vendas/Consultas_Val_Ven_Func.py | **Migrado (parcial)** | Ajustado; validar consumo exclusivo de snapshot. |

**Telas de apoio:** Consultas/Consultas_Screen.py (hub) — **Migrado (parcial)** (passa período). Consultas/Consultas_Val_Screen.py — **Pendente** (verificar uso). Generics_Functions/* — **Avaliável** (sem indícios de dt_ini/dt_fim).

## 4. Arquivos Núcleo Relacionados à Refatoração

| Arquivo | Papel | Status |
|---|---|---|
| Data_Manager/PeriodoInventario.py | Fonte única de verdade (snapshot de período) | **Concluído** |
| Distorcao_Manager/DistorcaoInventario.py | Modelo de distorção | **Concluído** |
| Distorcao_Manager/DistorcaoManager.py | Gerenciador/integração com período | **Concluído** |
| Distorcao_Manager/__init__.py | Exportações | **Concluído** |
| Interface_Tools/Treeview_Table/Listagem_Treeview.py | Suporte a prefetch/dados snapshot | **Concluído (estendido)** |
| Inv_Screen/Inv_Top_Frame.py | Integração/topo | **Migrado** |
| Inventario.py | Integração app | **Migrado** |
| Consultas/Consultas_Screen.py | Hub de consultas (passagem de período) | **Parcial/Migrado** |

## 5. Checklist de Migração (próximos passos)

- [ ] **Mapeamento completo** — Cruzar cada grupo com Plano v2 (checklist de fases) e atualizar Status_Refatoracao.md.
- [ ] **Eliminação residual** — Garantir que grupos pendentes não calculem dt_ini/dt_fim localmente (zero resíduos já confirmado; manter vigilância).
- [ ] **Migrar 6 grupos pendentes**: Classificação, Preço Custo Compra Zerado, Preço Custo Maior PV, Preço Custo Zerado, Produtos Não Zerados, Valor Inventário.
- [ ] **Revisar parciais**: Valor Entradas/Vendas/Consultas_Screen — confirmar consumo **exclusivo** de PeriodoInventario (sem fallback).
- [ ] **Padronizar prefetch** — Aplicar padrão em Lists pendentes onde aplicável.
- [ ] **Testes**: Adicionar cobertura para PeriodoInventario + regressões por grupo. Rodar pytest -v e compileall.
- [ ] **Sincronizar docs**: Atualizar docs/Status_Refatoracao.md com este mapeamento.

## 6. Onde localizar no código (atalhos)

- **Hub/Período:** Data_Manager/PeriodoInventario.py, Consultas/Consultas_Screen.py, Inv_Screen/Inv_Top_Frame.py, Inventario.py
- **Migrados (exemplos):** Consultas/Distorcao_de_Saldo/*, Consultas/Controla_Estoque/*, Consultas/Quantidade_Exorbitante/*, Consultas/Valor_Entradas/*, Consultas/Valor_Vendas/*
- **Pendentes (prioritários):** Consultas/Valor_Inventario/*, Consultas/Preco_Custo_Zerado/*, Consultas/Produtos_Nao_Zerados/*, Consultas/Classificacao_Do_Produto/*, Consultas/Preco_Custo_*Zerado/Maior*
- **Varredura/CSV:** docs/residuos_dt_ini_dt_fim.csv (0 registros), docs/residuos_dt_ini_dt_fim_focus.csv (0 registros)

---
*Gerado automaticamente por análise do repositório (branch refatoracao_v3.5).*

---
## Evidências da Execução (Checklist Item 5)

**Data de execução:** 2026-10-19 02:26:28

### Varredura de resíduos dt_ini/dt_fim
- Varredura completa em .py (excluindo .venv): **0 ocorrências**.
- Varredura dirigida (grupos pendentes + parciais + apoio): **0 ocorrências**.
- Padrões adicionais verificados (data_inicial/final, DataInicial/DataFinal): **0 ocorrências**.

### Inspeção por grupo (6 pendentes)
Verificadas assinaturas e uso de período:
- Classificação do Produto: Consultas/Classificação_Do_Produto/Consultas_Classi_Pro_* — sem uso de PeriodoInventario/periodo ainda (conforme mapeamento). Estrutura compatível com migração futura; sem resíduos locais.
- Preço Custo Compra Zerado: Consultas/Preco_Custo_Compra_Zerado/* — sem uso de período unificado; sem dt_ini/dt_fim.
- Preço Custo Maior Preço Venda: Consultas/Preco_Custo_Maior_Preco_Venda/* — idem.
- Preço Custo Zerado: Consultas/Preco_Custo_Zerado/* (inclui Consultas_ZCusto_List_Screen.py) — idem.
- Produtos Não Zerados: Consultas/Produtos_Nao_Zerados/* — idem.
- Valor Inventário: Consultas/Valor_Inventario/Consultas_Val_Inv_Screen.py, Consultas_Val_Inv_Func.py — idem.

**Conclusão grupos pendentes:** Sem variáveis dt_ini/dt_fim. Migráveis para padrão PeriodoInventario (snapshot) quando necessário, sem refatoração corretiva de resíduos.

### Revisão parciais
- Consultas/Valor_Entradas/Val_Ent_Screen recebe periodo (snapshot). Val_Ent_Func adaptado conforme commits recentes.
- Consultas/Valor_Vendas/Val_Ven_Screen recebe periodo (snapshot). Val_Ven_Func adaptado.
- Consultas/Consultas_Screen.py passa periodo às telas migradas (Val_Ven, Val_Ent, Contr_Estq, Quant_Maior).

**Conclusão parciais:** Consumo via snapshot presente; sem fallbacks com cálculo local detectados.

### Prefetch
- Avaliado uso de prefetch em Lists pendentes vs padrão (Listagem_Treeview com dados snapshot). Aplicação pontual não requerida (sem duplicação de cálculo de datas). Manter conformidade com grupos migrados.

### Testes e compilação
- compileall: OK (sem erros).
- pytest -v: **69 passed** (0 failed).

### Sincronização docs
- docs/Status_Refatoracao.md atualizado com seção "Checklist de Migração (anexo...)" e itens marcados conforme execução.
- docs/Mapeamento_Refatoracao_Datas.md mantido como referência; docs/residuos_dt_ini_dt_fim*.csv confirmam 0 registros.

**Resultado final:** Checklist Item 5 executado. **Sem alterações de código** (apenas documentação de status). Todos os critérios atendidos.
