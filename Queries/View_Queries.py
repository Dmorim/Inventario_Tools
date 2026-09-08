"""
Módulo de views SQL (Firebird) auxiliares para o Inventario_Tools.

As views são tabelas virtuais (não materializadas) criadas no banco:
- Não armazenam dados; refletem automaticamente mudanças nas tabelas base.
- V_FAT_VALOR_SAIDA e V_LAN_COM devem existir antes de V_DIFF_ENTRADA_SAIDA_MES.
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

# ============================================================================
# VIEW: V_LAN_COM
# Centraliza o LEFT JOIN entre in01lan (lançamentos) e in01com (compras),
# repetido em diversas queries do projeto.
# ============================================================================

VIEW_V_LAN_COM = """
CREATE OR ALTER VIEW V_LAN_COM AS
SELECT
    l.notfi,
    l.cdfrn,
    l.modelonota,
    l.dtpro,
    l.venda,
    l.cfop,
    l.controlaestoque,
    l.valor,
    l.quant,
    l.despr,
    l.valsub,
    l.alipi_ent,
    l.cance AS lan_cance,
    l.tpmov,
    l.cdpro,
    c.valno AS com_valno,
    c.dtcom AS com_dtcom
FROM in01lan l
LEFT JOIN in01com c
       ON c.notfi = l.notfi
      AND c.cdfrn = l.cdfrn
      AND c.modelonota = l.modelonota
"""

# ============================================================================
# VIEW: V_DIFF_ENTRADA_SAIDA_MES
# Agrupamento mensal da diferença entre entradas e saídas, base para a query
# do dashboard QUERY_DIFERENCA_ENTRADA_SAIDA_AGRUPADO.
# ============================================================================

VIEW_V_DIFF_ENTRADA_SAIDA_MES = """
CREATE OR ALTER VIEW V_DIFF_ENTRADA_SAIDA_MES AS
WITH entradas AS (
    SELECT
        l.notfi,
        l.cdfrn,
        l.modelonota,
        extract(month from l.dtpro) AS mes,
        extract(year from l.dtpro) AS ano,
        COALESCE(MAX(c.com_valno), 0) AS valor_entrada
    FROM in01lan l
    LEFT JOIN V_LAN_COM c
           ON c.notfi = l.notfi
          AND c.cdfrn = l.cdfrn
          AND c.modelonota = l.modelonota
    WHERE COALESCE(l.controlaestoque, 'S') = 'S'
    GROUP BY 1, 2, 3, 4, 5
), saidas AS (
    SELECT
        vs.fatur,
        SUM(vs.valor_saida) AS valor_saida
    FROM V_FAT_VALOR_SAIDA vs
    WHERE COALESCE(vs.cance, 'N') = 'N'
    GROUP BY 1
)
SELECT
    e.mes,
    e.ano,
    SUM(e.valor_entrada) AS valor_entrada,
    SUM(COALESCE(s.valor_saida, 0)) AS valor_saida,
    SUM(e.valor_entrada) - SUM(COALESCE(s.valor_saida, 0)) AS valor_diff
FROM entradas e
LEFT JOIN saidas s
       ON s.fatur = e.notfi
GROUP BY 1, 2
ORDER BY 2, 1
"""
