# Pruebas manuales del pipeline

Pruebas ejecutadas a mano contra el pipeline real, con su evidencia. Cada una responde una pregunta concreta sobre el comportamiento del pipeline.

| # | Prueba | Pregunta | Resultado |
|---|---|---|---|
| 1 | Cuarentena | ¿Los datos defectuosos quedan en cuarentena y no llegan a Gold? | Aprobada |
| 2 | Idempotencia | ¿Repetir o traslapar cortes duplica datos o crea versiones falsas? | Aprobada (A, B y C) |

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
