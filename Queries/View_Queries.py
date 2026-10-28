"""
Módulo de views SQL (Firebird) auxiliares para o Inventario_Tools.

As views são tabelas virtuais (não materializadas) criadas no banco:
- Não armazenam dados; refletem automaticamente mudanças nas tabelas base.
"""

# ============================================================================
# VIEW: V_FAT_VALOR_SAIDA
# Centraliza o cálculo do valor de saída (IIF/COALESCE sobre VALNO/VLNOT e
# impostos), repetido em diversas queries do projeto.
# ============================================================================

VIEW_V_FAT_VALOR_SAIDA = """
CREATE OR ALTER VIEW V_FAT_VALOR_SAIDA AS
SELECT
    f.fatur,
    f.dtemi,
    f.cance,
    f.venda,
    f.emite,
    f.vlnot,
    CAST(IIF(COALESCE(f.VLNOT, 0) = 0,
        (COALESCE(f.VALNO, 0) - COALESCE(f.VALDE, 0) + COALESCE(f.ICANT, 0) +
         COALESCE(f.VALFR, 0) + COALESCE(f.valsg, 0) + COALESCE(f.valip, 0) +
         COALESCE(f.valst, 0)),
        f.VLNOT) AS NUMERIC(14,2)) AS valor_saida
FROM in01fat f
"""
