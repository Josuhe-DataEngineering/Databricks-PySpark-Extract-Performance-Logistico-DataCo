# ADR-006: Conversión segura de tipos, con NULL y cuarentena en vez de cero

- **Estado:** Aceptada
- **Fecha:** 2026-10-26

## Contexto

Silver convierte las columnas de texto de Bronze a su tipo real (enteros,
decimales, fechas). Hay que decidir qué hacer cuando un valor está vacío o no
se puede convertir.

## Alternativas

1. **Reemplazar por un valor por defecto (por ejemplo, 0):** nunca falla, pero
   el cero entra a sumas y promedios como si fuera un dato real.
2. **Fallar la carga:** detecta el problema, pero una sola celda mala detiene
   todo el pipeline.
3. **Convertir a `NULL` y aislar la fila en cuarentena:** el pipeline sigue y
   el problema queda registrado.

## Decisión

Se aplica la opción 3, con funciones del módulo compartido (ADR-003):

- `clean_num` usa `try_cast(NULLIF(TRIM(col), '') AS tipo)`: un valor vacío o no
  convertible da `NULL`, **nunca 0**.
- `tipo_invalido` marca las celdas con texto no vacío que no se pueden
  convertir; esa fila recibe el motivo `TIPO_DATO_INVALIDO` en cuarentena.
- Un identificador `NULL` o igual a 0 se trata como inválido (por ejemplo,
  `ORDER_ID_INVALIDO`, `ITEM_ID_INVALIDO`).

## Motivos

- Un cero inventado contamina los indicadores sin dejar rastro; un `NULL` es
  honesto y las reglas de calidad pueden contarlo.
- El error se ve y se mide (`hd_cuarentena_resumen`) en lugar de ocultarse.
- Una celda defectuosa no detiene el pipeline.

## Consecuencias

- Las consultas de Gold solo leen filas `VALIDO`, por lo que los `NULL` por
  conversión fallida no llegan a los indicadores.
- La conversión está cubierta por pruebas automáticas (por ejemplo, vacío y
  texto no convertible dan `NULL`, nunca 0).
