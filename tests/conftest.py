"""Configuración común de pytest: sesión de Spark local y ruta del repo."""
import os
import sys

import pytest
from pyspark.sql import SparkSession

# Permite `import modulos_compartidos` sin instalar el repo como paquete.
RAIZ_REPOSITORIO = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if RAIZ_REPOSITORIO not in sys.path:
    sys.path.insert(0, RAIZ_REPOSITORIO)


@pytest.fixture(scope="session")
def spark():
    sesion = (
        SparkSession.builder
        .master("local[1]")
        .appName("pruebas_transformaciones_silver")
        .config("spark.sql.shuffle.partitions", "1")
        .config("spark.ui.enabled", "false")
        .config("spark.sql.ansi.enabled", "false")
        .getOrCreate()
    )
    yield sesion
    sesion.stop()
