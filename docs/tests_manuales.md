# Pruebas manuales del pipeline

Pruebas ejecutadas a mano contra el pipeline real, con su evidencia. Cada una responde una pregunta concreta sobre el comportamiento del pipeline.

| # | Prueba | Pregunta | Resultado |
|---|---|---|---|
| 1 | Cuarentena | ¿Los datos defectuosos quedan en cuarentena y no llegan a Gold? | Aprobada |
| 2 | Idempotencia | ¿Repetir o traslapar cortes duplica datos o crea versiones falsas? | Aprobada (A, B y C) |
| 3 | Motor de calidad | ¿Cada regla detecta su defecto y aplica su decisión (CUARENTENA, ADVERTIR, DETENER)? | Aprobada (3 escenarios) |
| 4 | Corrida de producción | ¿Los datos reales cumplen las 24 reglas? | Aprobada (24 de 24 en CUMPLE) |

---

## Prueba 1: cuarentena de datos defectuosos

**Objetivo.** Comprobar que cada regla de cuarentena de Silver detecta su defecto, registra el motivo correcto y que ninguna fila en cuarentena llega a Gold.

**Cómo se hizo.** Notebooks en `05_pruebas_calidad/`:

1. `01_crear_esquemas_prueba`: crea el esquema `pruebas_calidad` en los cuatro catálogos y copia solo la estructura de las tablas de control, para no ensuciar los logs reales.
2. `02_generar_bronze_defectuoso`: crea `brz_dataco.pruebas_calidad.raw_supply_chain_defectuosa` desde filas reales de Bronze, con un defecto por caso y claves nuevas (`order_id` desde 9,000,001 y `order_item_id` desde 90,000,001). Es determinista.
3. `03_ejecutar_y_verificar_cuarentena`: corre los notebooks Silver y Gold del pipeline contra ese Bronze y compara tres fuentes por tabla y motivo: lo **esperado** (definido por el generador), lo **registrado** en `hd_cuarentena_resumen` y lo que **hay** en la tabla Silver. No ejecuta `gld_reporte_excel_correo`, porque envía un correo real.

**Casos generados.**

| Caso | Filas | Defecto | Cuarentena esperada |
|---|---|---|---|
| CONTROL_SANO | 1,000 | ninguno | 0 |
| ORDER_ID_INVALIDO | 1,000 | `order_id` vacío, `'0'` o NULL | 1,000 |
| FECHA_PEDIDO_INVALIDA | 1,000 | fecha no parseable | 1,000 |
| CLIENTE_NO_INFORMADO | 1,000 | `order_customer_id` vacío, `'0'` o NULL | 1,000 |
| RIESGO_RETRASO_INVALIDO | 1,000 | `late_delivery_risk` distinto de 0 y 1 | 1,000 |
| CLIENTE_ID_INVALIDO | 1,000 | `customer_id` vacío, `'0'` o NULL | 1 (misma clave 0) |
| PRODUCTO_ID_INVALIDO | 1,000 | `product_card_id` vacío, `'0'` o NULL | 1 (misma clave 0) |
| UBICACION_INCOMPLETA | 1,000 | market, región o país vacío | 1,000 |
| ITEM_ID_INVALIDO | 1,000 | `order_item_id` vacío, `'0'` o NULL | 1 (misma clave 0) |
| CANTIDAD_INVALIDA | 1,000 | cantidad 0 o negativa | 1,000 |
| PRIORIDAD_FECHA_Y_CLIENTE | 100 | dos defectos; gana FECHA_PEDIDO_INVALIDA | suma a FECHA |
| PRIORIDAD_CLIENTE_Y_RIESGO | 100 | dos defectos; gana CLIENTE_NO_INFORMADO | suma a CLIENTE |
| PRIORIDAD_ORDER_ID_Y_FECHA | 100 | dos defectos; gana ORDER_ID_INVALIDO | suma a ORDER_ID |

**Resultado.** El notebook terminó con "PRUEBA DE CUARENTENA APROBADA":

- Los 9 motivos coinciden entre lo esperado, lo registrado en el log y lo que hay en Silver.
- Los casos con dos defectos se asignan al motivo de mayor prioridad.
- El grupo de control quedó completo como `VALIDO`.
- `duplicados_reales` fue 0 en todas las tablas Silver.
- Ninguna fila en cuarentena llegó a Gold, y las dimensiones Gold contienen exactamente las filas `VALIDO` de Silver.

**Limitación conocida.** Los casos con clave igual a 0 (`CLIENTE_ID_INVALIDO`, `PRODUCTO_ID_INVALIDO`, `ITEM_ID_INVALIDO`) producen una sola fila en cuarentena, porque la deduplicación agrupa por clave antes de aplicar la regla. El resultado esperado ya lo refleja.

---

## Prueba 2: idempotencia de las cargas

**Objetivo.** Comprobar que repetir o traslapar ventanas ya cargadas no duplica datos en Bronze, Silver, Gold ni en los snapshots de KPI, y que no crea versiones falsas en las tablas SCD2.

**Cómo se hizo.** Se tomó una foto del estado del pipeline con `05_pruebas_calidad/04_foto_estado_pipeline` (44 métricas de datos y 2 de traza, guardadas en `metadata_dataco.pruebas_calidad.hd_foto_idempotencia`). Para cada escenario se movió la ventana en `md_pipeline_control`, se ejecutó el Workflow completo y se comparó la foto nueva contra la anterior.

### Escenario A: repetir una ventana ya cargada (22 → 28 de enero de 2018)

Sin cambios en Bronze (180,314 filas), con 480 / 480 / 64,184 en los conteos de la ventana. **Aprobado.**

### Escenario B: ventana traslapada con días nuevos (25 → 31 de enero de 2018)

| Métrica | Antes | Después |
|---|---|---|
| Bronze, filas | 180,314 | 180,519 (igual a `filas_archivo`) |
| Bronze, duplicados por línea | 0 | 0 |
| Silver, pedidos válidos | 65,547 | 65,752 |
| Silver, pedidos en cuarentena | 0 | 0 |
| Gold, pedidos vigentes | 64,184 | 64,385 (+205 nuevos − 4 cancelados) |
| Gold, versiones cerradas de pedidos | 0 | 0 |
| Gold, pedidos vigentes repetidos | 0 | 0 |
| KPI, snapshots | 3 | 4 (nuevo 2018-01-31, marcado como último) |

El corte 22 → 28 pasó de 480 a 206 filas porque los días 25 a 28 pasaron al corte 25 → 31: `replaceWhere` reemplazó los días traslapados sin duplicar. **Aprobado.**

### Escenario C: repetir una ventana ya cargada después de otras (22 → 28)

Se compararon las 44 métricas de datos contra el resultado del escenario B: **las 44 salieron iguales**. Solo cambió la traza (+1 ejecución y +21 registros en `hd_etl_log`, una corrida completa bien registrada). No se duplicó ningún snapshot y el último siguió siendo 2018-01-31. **Aprobado.**

**Conclusión.** Repetir un corte, traslapar días ya cargados y volver a ejecutar una ventana vieja no duplica datos ni crea versiones nuevas en pedidos existentes.

**Nota.** Tras el escenario B, Bronze llega hasta el 31 de enero y deja de estar alineado a domingo. Se corrige con la recarga histórica final.

---

## Prueba 3: motor de calidad de datos

**Objetivo.** Comprobar que `dq_validaciones` detecta defectos inyectados a propósito y que toma la decisión configurada en cada regla: **CUARENTENA** (aísla las filas y el pipeline sigue), **ADVERTIR** (avisa y sigue) o **DETENER** (corta el pipeline y alerta).

**Catálogo.** 24 reglas (DQ-001 a DQ-024): 21 se evalúan sobre Silver y 3 sobre Gold.

| Decisión | Reglas |
|---|---|
| DETENER (7) | DQ-001, DQ-002, DQ-003, DQ-004, DQ-014, DQ-015, DQ-016 |
| CUARENTENA (9) | DQ-005, DQ-006, DQ-008, DQ-009, DQ-011, DQ-012, DQ-013, DQ-023, DQ-024 |
| ADVERTIR (8) | DQ-007, DQ-010, DQ-017, DQ-018, DQ-019, DQ-020, DQ-021, DQ-022 |

**Cómo se hizo.** No se creó un Job aparte: se usó el **mismo Workflow** con el parámetro `modo_prueba`. Con `modo_prueba = true`, la condición `es_modo_prueba` omite `prepare_pipeline_control`, `gld_reporte_excel_correo` y `finalize_pipeline_control`, y `ancla_pipeline` mantiene activa la cadena Silver. Así se prueba el pipeline real, sin duplicarlo.

Parámetros de cada corrida de prueba (la pantalla de ejecución debe mostrar "(override)" en todos):

| Parámetro | Valor |
|---|---|
| `modo_prueba` | `true` |
| `id_ejecucion_manual` | un identificador único por escenario |
| `bronze_schema` | `pruebas_calidad` |
| `bronze_table` | `raw_supply_chain_defectuosa` |
| `silver_schema`, `gold_schema`, `metadata_schema` | `pruebas_calidad` |

Procedimiento:

1. `05_pruebas_calidad/01_crear_esquemas_prueba` crea el esquema `pruebas_calidad` en los cuatro catálogos y copia solo la estructura de las tablas de control.
2. `02_generar_bronze_defectuoso` crea 10,500 filas defectuosas a partir de filas reales. Las cantidades esperadas se **calculan desde los datos**, no se escriben a mano, y quedan en `casos_esperados` y `casos_esperados_dq`.
3. **Antes de cada escenario** se borran las tablas Silver y Gold del esquema `pruebas_calidad`, porque la dimensión Gold con SCD2 conserva versiones entre corridas.
4. Se lanza el Job con los parámetros de arriba y se compara lo detectado en `hd_dq_resultados` contra lo esperado.

### Escenario A: CUARENTENA (`PRUEBA-CABLEADO-3`)

| Regla | Filas detectadas o aisladas |
|---|---|
| DQ-024 (pedido sin ubicación válida) | 1,000 |
| DQ-011 | 733 |
| DQ-012 | 1 |
| DQ-013 | 452 |
| DQ-005 y DQ-006 | 1,200 |
| DQ-008 | 1,067 |
| DQ-009 | 1,000 |

Los 9 motivos de cuarentena de `casos_esperados` coinciden con lo registrado. DQ-014 y DQ-015 (Gold) dieron CUMPLE: confirman que las filas en cuarentena no llegaron a Gold. DQ-005, 006, 008 y 009 solo miden, porque Silver ya aisló esas filas al cargar.

### Escenario B: ADVERTIR (`PRUEBA-ADVERTIR-1`)

DQ-007 y DQ-010 quedaron en **ADVERTENCIA** con 100 filas detectadas frente a 100 esperadas. El pipeline continuó.

### Escenario C: DETENER (`PRUEBA-DETENER-1`)

Se sembró un duplicado del `customer_id` 20758 en `md_clientes`.

- DQ-003 quedó **DETENIDO**: 1 fila detectada frente a 1 esperada.
- Silver terminó, pero las tasks de Gold no corrieron porque dependen de `dq_validaciones_silver`.
- Llegó la alerta a Slack con el `log_id`.

**Alcance y limitaciones.**

- De las reglas DETENER solo se forzó la falla de DQ-003. Las de Gold (DQ-014, 015 y 016) no se forzaron.
- DQ-022 no tiene escenario de prueba propio.
- Los `log_error_*` escriben en la tabla de log de producción, así que en modo prueba la fila de la task fallida queda en `EN_PROCESO` sin mensaje de error.
- El reintento automático de las tasks de calidad en serverless puede duplicar la fila de log de esa task.

---

## Prueba 4: corrida normal de producción

**Objetivo.** Comprobar que, con los datos reales y sin parámetros de prueba, las 24 reglas se cumplen.

**Resultado.** La ejecución terminó en verde: las **24 reglas en CUMPLE**, con 0 filas incumpliendo. Es el caso inverso de la Prueba 3: allí las reglas detectan defectos inyectados; aquí confirman que los datos reales no los tienen.
