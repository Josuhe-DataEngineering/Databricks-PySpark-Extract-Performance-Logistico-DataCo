# Calidad de datos

[← Volver al README](../README.md)

---

## Cuarentena y deduplicación con trazabilidad

Ningún registro se elimina. Cada tabla Silver agrega tres columnas (`estado_calidad`: `VALIDO` o `CUARENTENA`, `motivo_cuarentena` y `fecha_procesamiento`) y **Gold lee únicamente las filas `VALIDO`**.

| Tabla Silver | Grano (una fila por…) | Motivos de cuarentena |
|---|---|---|
| `hd_pedidos` | pedido (`order_id`) | `ORDER_ID_INVALIDO` · `FECHA_PEDIDO_INVALIDA` · `CLIENTE_NO_INFORMADO` · `RIESGO_RETRASO_INVALIDO` · `TIPO_DATO_INVALIDO` · `PEDIDO_SIN_CLIENTE` · `PEDIDO_SIN_UBICACION` |
| `hd_pedido_detalle` | ítem (`order_item_id`) | `ITEM_ID_INVALIDO` · `CANTIDAD_INVALIDA` · `TIPO_DATO_INVALIDO` · `LINEA_SIN_PEDIDO` · `LINEA_SIN_PRODUCTO` |
| `md_clientes` | cliente (`customer_id`) | `CLIENTE_ID_INVALIDO` |
| `md_productos` | producto (`product_card_id`) | `PRODUCTO_ID_INVALIDO` · `TIPO_DATO_INVALIDO` |
| `md_ubicaciones` | combinación geográfica | `UBICACION_INCOMPLETA` · `TIPO_DATO_INVALIDO` |

Cada fila recibe un solo motivo: el primero que se cumple, en un orden definido por tabla. Dos tablas de control en `metadata_dataco` registran cada ejecución:

- **`hd_deduplicacion_log`:** filas de entrada y de salida por tabla, filas agrupadas (informativo) y **duplicados reales**, que debe ser 0.
- **`hd_cuarentena_resumen`:** filas en cuarentena por tabla y motivo.

**Resultado de la última corrida de producción:** 65,752 pedidos, 180,519 líneas de detalle, 20,652 clientes, 118 productos y 3,800 ubicaciones en Silver; **0 duplicados reales y 0 filas en cuarentena**. Gold: 64,385 pedidos vigentes (los cancelados se excluyen por regla de negocio). Las **24 reglas** dieron `CUMPLE`.

---

## Motor declarativo de reglas

El motor se basa en dos tablas: un **catálogo de reglas** (`md_dq_reglas`) y un **historial de resultados** por ejecución (`hd_dq_resultados`).

| Dimensión | Qué verifica | Ejemplos |
|---|---|---|
| **Unicidad** | Una fila por llave de negocio | `order_id`, `order_item_id`, `customer_id`, `product_card_id` |
| **Completitud** | Campos obligatorios informados | Fechas de pedido y de envío |
| **Validez** | Valores dentro del dominio | Riesgo de retraso en {0,1}; cantidad > 0; texto no convertible a número |
| **Integridad referencial** | Las referencias existen | Detalle → pedido y producto, pedido → cliente y ubicación |
| **Consistencia** | Silver y Gold cuadran | Pedidos vigentes = pedidos no cancelados; un resumen por pedido |
| **Actualidad** | El dato llegó a tiempo | El corte cargado coincide con la tabla de control; el volumen diario no cae a menos de la mitad del promedio previo |

Cada regla se define en lenguaje de negocio, con **criticidad**, **umbral** justificado, **decisión** ante incumplimiento, owner y steward (como roles). El criterio es: el dato defectuoso va a **cuarentena** con alerta a Slack sin detener el pipeline; un exceso sobre el umbral solo **advierte**; el pipeline **se detiene** únicamente ante errores propios (duplicados tras deduplicar, llaves rotas en Gold o Silver que no cuadra con Gold).

| Decisión | Reglas |
|---|---|
| **Detener** (7) | DQ-001 a DQ-004 (unicidad en Silver) · DQ-014, DQ-015, DQ-016 (Gold) |
| **Cuarentena** (9) | DQ-005, DQ-006, DQ-008, DQ-009, DQ-011, DQ-012, DQ-013, DQ-023, DQ-024 |
| **Advertir** (8) | DQ-007, DQ-010, DQ-017 a DQ-022 |

Las reglas de integridad referencial **aíslan** las filas defectuosas con una consulta propia (por ejemplo, DQ-024 aparta los pedidos cuya ubicación no existe como válida en `md_ubicaciones`); las demás miden lo que Silver ya aisló al cargar.

**Decisión de diseño:** [ADR-009 · Parámetros de calidad](adr/009-parametros-de-calidad.md)

---

## Pruebas con datos defectuosos

Los tres comportamientos se prueban corriendo **el Workflow real** (no notebooks sueltos) sobre un esquema aislado, `pruebas_calidad`, con datos sintéticos defectuosos generados por código a partir de filas reales. El **mismo Job** se usa para producción y para pruebas: los parámetros de catálogo y esquema redirigen los mismos notebooks a las tablas de prueba, sin tocar los datos ni los logs de producción.

Las cantidades esperadas **no están escritas a mano**: se calculan a partir de los datos inyectados y se guardan junto a ellos (`casos_esperados` y `casos_esperados_dq`).

| Etapa | Qué se prueba | Resultado observado |
|---|---|---|
| **1. Cuarentena** | Un caso por motivo sobre 10,500 filas de Bronze (sanas y defectuosas) | Las filas se apartan con su motivo y el pipeline sigue: DQ-024 aisló 1,000 pedidos, DQ-011 733 líneas, DQ-013 452 pedidos; Gold queda consistente (DQ-014 y DQ-015 en `CUMPLE`); la comparación contra lo esperado coincide en todos los casos |
| **2. Advertir** | Fechas de envío vacías y estados de pedido desconocidos | DQ-007 y DQ-010 quedan en `ADVERTENCIA` con **100 filas detectadas, 100 esperadas**; el pipeline sigue y llega la alerta |
| **3. Detener** | Un cliente duplicado sembrado | DQ-003 detecta **1 duplicado (1 esperado)** y queda `DETENIDO`; Silver termina, Gold no corre y llega la alerta de fallo |

Antes de cada escenario se reinician las tablas Silver y Gold de prueba, porque la dimensión de pedidos Gold es SCD2 y conserva historial entre corridas.

El procedimiento paso a paso está en [`tests_manuales.md`](tests_manuales.md).

> 🚧 *En construcción:* que las corridas de prueba también registren el mensaje de error de la excepción en su propio log (hoy el detalle queda en la salida de la task).

**Decisión de diseño:** [ADR-010 · Modo de prueba por parámetro](adr/010-modo-de-prueba-por-parametro.md)
