# ADR-002: Cuarentena en la misma tabla de Silver (en lugar de descartar filas)

- **Estado:** Aceptada
- **Fecha:** 2026-10-26

## Contexto

Bronze guarda todos los campos como texto (STRING), tal como llegan de la
fuente. Al pasar a Silver se convierten a su tipo real (números, fechas), se
deduplican por llave de negocio y se validan con el motor de calidad
(24 reglas: 21 en Silver y 3 en Gold).

Hay que decidir qué hacer con las filas que no cumplen las reglas:

1. **Descartarlas:** simple, pero se pierde la evidencia y nadie sabe cuántas
   ni por qué se eliminaron.
2. **Enviarlas a una tabla de cuarentena aparte:** conserva la evidencia, pero
   duplica estructuras y complica la reconciliación de conteos.
3. **Marcarlas en la misma tabla:** conserva la evidencia y mantiene una sola
   tabla por entidad.

## Decisión

Se aplica la opción 3. Ningún registro se elimina: cada tabla Silver agrega tres
columnas.

| Columna | Contenido |
|---|---|
| `estado_calidad` | `VALIDO` o `CUARENTENA` |
| `motivo_cuarentena` | Motivo de la regla incumplida, o `NULL` si es válida. Un solo motivo por registro: el primero que se cumple, en un orden definido por tabla |
| `fecha_procesamiento` | Momento en que Silver procesó el registro |

La capa Gold lee **únicamente las filas `VALIDO`**.

## Motivos

- No se pierde información: toda fila de salida de Silver conserva su evidencia
  y su trazabilidad hacia Bronze.
- La deduplicación y la cuarentena quedan auditadas en tablas de control
  (`hd_deduplicacion_log` y `hd_cuarentena_resumen`), de modo que los conteos
  entre Bronze y Silver se pueden explicar.
- Quien investigue un problema de calidad consulta la misma tabla y filtra por
  `estado_calidad`, sin unir con otra.
- Gold queda protegido: nunca consume filas que no pasaron las reglas.

## Consecuencias

- Toda consulta sobre Silver que alimente métricas debe filtrar por
  `estado_calidad = 'VALIDO'`; en Gold el filtro es obligatorio.
- Un notebook de pruebas corre Silver y Gold contra un Bronze defectuoso
  (esquema `pruebas_calidad`, sin tocar producción) y verifica que ninguna fila
  en cuarentena llegue a Gold.
- Los resultados de cada regla se registran en `hd_dq_resultados` y en `etl_log`.
- Si el volumen de filas inválidas creciera mucho, habría que reconsiderar una
  tabla de cuarentena separada.
