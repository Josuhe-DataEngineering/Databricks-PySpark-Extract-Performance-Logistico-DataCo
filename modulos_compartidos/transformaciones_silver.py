"""Transformaciones compartidas de la capa Silver.

Una sola copia para los 5 notebooks Silver (slv_customers, slv_products,
slv_locations, slv_orders y slv_orders_details).
"""

from pyspark.sql import functions as F, Window


def clean_str(col_name: str, default: str = "") -> F.Column:
    """UPPER(TRIM(ISNULL(col, default))): texto en mayúsculas y sin espacios."""
    return F.upper(F.trim(F.coalesce(F.col(col_name).cast("string"), F.lit(default))))


def clean_num(col_name: str, cast_type) -> F.Column:
    """Convierte a número. Vacío o texto no convertible -> NULL (nunca 0)."""
    texto = f"NULLIF(TRIM(CAST(`{col_name}` AS STRING)), '')"
    return F.expr(f"try_cast({texto} AS {cast_type})")


def tipo_invalido(col_name: str, cast_type) -> F.Column:
    """Verdadero si la celda trae texto (no vacío) que no se puede convertir al tipo."""
    texto = f"NULLIF(TRIM(CAST(`{col_name}` AS STRING)), '')"
    return F.expr(f"{texto} IS NOT NULL AND try_cast({texto} AS {cast_type}) IS NULL")


def dedup_reciente(df, partition_cols: list, orden_col: str):
    """Conserva una fila por clave: la de mayor valor en orden_col."""
    w = Window.partitionBy(*partition_cols).orderBy(F.col(orden_col).desc())
    return (
        df.withColumn("rn", F.row_number().over(w))
          .filter(F.col("rn") == 1)
          .drop("rn")
    )