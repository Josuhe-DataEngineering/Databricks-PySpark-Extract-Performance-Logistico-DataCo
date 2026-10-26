"""Pruebas unitarias de modulos_compartidos.transformaciones_silver."""
from datetime import date

from modulos_compartidos.transformaciones_silver import (
    clean_num,
    clean_str,
    dedup_reciente,
    tipo_invalido,
)


def _valores(df, columna):
    return [fila[columna] for fila in df.collect()]


# ---------------------------------------------------------------- clean_str
def test_clean_str_quita_espacios_y_pasa_a_mayusculas(spark):
    df = spark.createDataFrame([("  lima ",), ("Cusco",)], "ciudad STRING")
    resultado = df.select(clean_str("ciudad").alias("r"))
    assert _valores(resultado, "r") == ["LIMA", "CUSCO"]


def test_clean_str_null_pasa_a_vacio_por_defecto(spark):
    df = spark.createDataFrame([(None,)], "ciudad STRING")
    resultado = df.select(clean_str("ciudad").alias("r"))
    assert _valores(resultado, "r") == [""]


def test_clean_str_usa_el_default_indicado(spark):
    df = spark.createDataFrame([(None,)], "ciudad STRING")
    resultado = df.select(clean_str("ciudad", default="sin dato").alias("r"))
    assert _valores(resultado, "r") == ["SIN DATO"]


# ---------------------------------------------------------------- clean_num
def test_clean_num_convierte_texto_valido(spark):
    df = spark.createDataFrame([("123",), (" 45.5 ",)], "monto STRING")
    resultado = df.select(clean_num("monto", "DOUBLE").alias("r"))
    assert _valores(resultado, "r") == [123.0, 45.5]


def test_clean_num_vacio_devuelve_null_no_cero(spark):
    df = spark.createDataFrame([("",), ("   ",), (None,)], "monto STRING")
    resultado = df.select(clean_num("monto", "DOUBLE").alias("r"))
    assert _valores(resultado, "r") == [None, None, None]


def test_clean_num_texto_no_convertible_devuelve_null_no_cero(spark):
    df = spark.createDataFrame([("abc",), ("12x",)], "monto STRING")
    resultado = df.select(clean_num("monto", "INT").alias("r"))
    assert _valores(resultado, "r") == [None, None]


# ------------------------------------------------------------ tipo_invalido
def test_tipo_invalido_detecta_solo_texto_no_convertible(spark):
    df = spark.createDataFrame(
        [("10",), ("abc",), ("",), (None,)], "monto STRING"
    )
    resultado = df.select(tipo_invalido("monto", "INT").alias("r"))
    # Válido, inválido, vacío (no cuenta como inválido) y nulo (tampoco).
    assert _valores(resultado, "r") == [False, True, False, False]


# junto con clean_num: lo inválido es NULL, nunca 0
def test_valor_invalido_queda_null_y_marcado_como_invalido(spark):
    df = spark.createDataFrame([("abc",)], "monto STRING")
    fila = df.select(
        clean_num("monto", "INT").alias("valor"),
        tipo_invalido("monto", "INT").alias("invalido"),
    ).first()
    assert fila["valor"] is None
    assert fila["invalido"] is True


# junto con clean_num: lo vacío es NULL, pero no se marca como inválido
def test_valor_vacio_queda_null_y_no_se_marca_invalido(spark):
    df = spark.createDataFrame([("",)], "monto STRING")
    fila = df.select(
        clean_num("monto", "INT").alias("valor"),
        tipo_invalido("monto", "INT").alias("invalido"),
    ).first()
    assert fila["valor"] is None
    assert fila["invalido"] is False


# ----------------------------------------------------------- dedup_reciente
def test_dedup_reciente_conserva_la_fila_mas_reciente(spark):
    df = spark.createDataFrame(
        [
            (1, "viejo", date(2026, 1, 1)),
            (1, "nuevo", date(2026, 3, 1)),
            (1, "medio", date(2026, 2, 1)),
            (2, "unico", date(2026, 1, 15)),
        ],
        "id INT, valor STRING, fecha_fin_corte DATE",
    )
    resultado = dedup_reciente(df, ["id"], "fecha_fin_corte")
    filas = {f["id"]: f["valor"] for f in resultado.collect()}
    assert filas == {1: "nuevo", 2: "unico"}


def test_dedup_reciente_deja_una_fila_por_clave(spark):
    df = spark.createDataFrame(
        [(1, date(2026, 1, 1)), (1, date(2026, 1, 2)), (2, date(2026, 1, 1))],
        "id INT, fecha_fin_corte DATE",
    )
    resultado = dedup_reciente(df, ["id"], "fecha_fin_corte")
    assert resultado.count() == 2
    assert resultado.select("id").distinct().count() == 2


def test_dedup_reciente_no_deja_columna_auxiliar(spark):
    df = spark.createDataFrame([(1, date(2026, 1, 1))], "id INT, fecha_fin_corte DATE")
    resultado = dedup_reciente(df, ["id"], "fecha_fin_corte")
    assert "rn" not in resultado.columns


def test_dedup_reciente_con_clave_compuesta(spark):
    df = spark.createDataFrame(
        [
            (1, "A", "v1", date(2026, 1, 1)),
            (1, "A", "v2", date(2026, 2, 1)),
            (1, "B", "v3", date(2026, 1, 1)),
        ],
        "id INT, tipo STRING, valor STRING, fecha_fin_corte DATE",
    )
    resultado = dedup_reciente(df, ["id", "tipo"], "fecha_fin_corte")
    filas = {(f["id"], f["tipo"]): f["valor"] for f in resultado.collect()}
    assert filas == {(1, "A"): "v2", (1, "B"): "v3"}
