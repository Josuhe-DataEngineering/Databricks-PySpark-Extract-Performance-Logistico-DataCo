# Capas del Lakehouse

[← Volver al README](../README.md)

---

## Bronze — ingesta cruda

Descarga el archivo desde SharePoint y carga **solo el corte de fechas** definido en una tabla de control. Todas las columnas de negocio se almacenan como **STRING**, sin inferir tipos ni aplicar reglas de negocio, para no perder información del origen; solo las columnas técnicas están tipadas.

Cada fila lleva sus metadatos: fecha de carga, ejecución, origen, archivo, **hash SHA-256 del archivo**, filas del archivo y esquema original en JSON.

Bronze conserva todos los registros, incluidos los duplicados: la deduplicación ocurre en Silver. El proceso es idempotente: si los cortes se traslapan, los días de la ventana se reemplazan y no se duplican. La tabla define una **retención de 365 días** del historial Delta y lleva COMMENT y tags de gobierno (capa, dominio, owner y frecuencia).

Sin permisos para grupos de lectura: solo ingeniería accede.

**Decisión de diseño:** [ADR-005 · Bronze en STRING](adr/005-bronze-en-string.md)

---

## Silver — datos limpios y conformados

Tipado fuerte con conversión segura (un texto no convertible queda en `NULL` y la fila se aísla; nunca se reemplaza por cero), normalización y deduplicación **determinista** por llave de negocio, priorizando el corte más reciente.

Separa el origen en entidades:

| Tabla | Grano |
|---|---|
| `md_clientes` | cliente (`customer_id`) |
| `md_productos` | producto (`product_card_id`) |
| `md_ubicaciones` | combinación geográfica (market, región, país, estado, ciudad y código postal) |
| `hd_pedidos` | pedido (`order_id`) |
| `hd_pedido_detalle` | ítem del pedido (`order_item_id`) |

Las filas que no cumplen una regla **no se eliminan**: pasan a **cuarentena** con su motivo, en las cinco tablas, y Gold lee solo las filas válidas. Cada ejecución deja registro de la deduplicación y de la cuarentena. Cada fila conserva su trazabilidad hacia Bronze.

**Decisiones de diseño:** [ADR-006 · Conversión segura](adr/006-conversion-segura-de-tipos.md) · [ADR-002 · Cuarentena en Silver](adr/002-cuarentena-en-silver.md)

---

## Calidad de datos — compuerta entre capas

Dos tasks de validación (tras Silver y tras Gold) ejecutan el catálogo de reglas y guardan cada resultado en una tabla histórica. La decisión ante un incumplimiento está definida por regla: **detener** el pipeline, enviar a **cuarentena** o solo **advertir**. Si una regla detiene el pipeline, la task falla, se registra el error y el Workflow se detiene.

Detalle completo en [calidad-de-datos.md](calidad-de-datos.md).

---

## Gold — modelo dimensional y KPIs

Esquema estrella listo para análisis, con **grano declarado** en cada tabla:

### Dimensiones (5)

| Tabla | Grano | SCD2 | Llave sustituta |
|---|---|---|---|
| `desc_dim_customers` | cliente | ✅ | Secuencial |
| `desc_dim_products` | producto | ✅ | Secuencial |
| `desc_dim_locations` | combinación geográfica | — | Hash estable |
| `desc_dim_fecha` | día | — | `date_key` |
| `desc_dim_shipping_mode` | modo de envío | — | Hash estable |

### Hechos (2) + resumen

- **`ft_orders`:** pedidos con SCD2 y reglas de negocio.
- **`ft_order_details`:** detalle de pedido (ítem).
- **`ft_order_summary`:** resumen por pedido, base única de los indicadores.

### KPIs (4 vistas)

- **Resumen Ejecutivo:** On-Time Delivery %, Late Delivery Risk %, Shipping Variance, Profit Margin %, Revenue por Cliente, Beneficio por Orden, Lead Time Promedio.
- **Detalle por Región:** con agrupaciones GLOBAL y AMERICAS.
- **Detalle por Orden:** con SCD2, historial por corte.
- **Alertas:** pedidos con riesgo no validado, sospecha de fraude o ambos.

Con agrupaciones de negocio **GLOBAL** (todos los mercados) y **AMERICAS** (LATAM + USCA). Se excluyen los pedidos cancelados y se marcan los sospechosos de fraude.

Las tablas de Gold declaran llaves primarias y foráneas informativas y la llave `NOT NULL`; no llevan `CHECK`, porque Databricks no lo permite junto a una máscara de columna ([ADR-014](adr/014-gobierno-en-gold.md)).

**Decisión de diseño:** [ADR-008 · Llaves sustitutas](adr/008-llaves-sustitutas.md)

---

## Entrega a negocio

Un notebook genera el **Excel de 4 pestañas** con formato condicional tipo semáforo y variación contra el corte anterior, y lo **envía por correo** con una tabla resumen y un gráfico en el cuerpo del mensaje (Microsoft Graph).

---

## Machine Learning 🚧 *En construcción*

La capa Gold alimentará un modelo que predice el **riesgo de retraso** de cada envío. Se entrenará y evaluará **solo con datos reales**, con separación temporal para evitar fuga de datos. El entrenamiento se registrará en **MLflow**, el modelo quedará versionado en **Unity Catalog** y sus predicciones se guardarán en una tabla Gold.

**Decisión de diseño:** [ADR-013 · Datos sintéticos solo para escala](adr/013-datos-sinteticos.md)

---

## Observabilidad

- **Tabla `etl_log`:** cada notebook registra inicio, fin, filas procesadas y estado (`EN_PROCESO → EXITOSO / ERROR`), con un identificador único por ejecución.
- **Manejo de errores:** cada task tiene su task de log que, ante un fallo, registra el detalle técnico y avisa a Slack.
- **Control de corte:** una tabla de parámetros define la ventana a procesar; reprocesar el mismo corte es idempotente.
- **Dashboard AI/BI "Salud del pipeline":** estado de la última ejecución, duración por notebook, tendencia diaria y errores recientes.

<p align="center">
  <img src="dashboard_salud_pipeline.png" alt="Dashboard de salud del pipeline DataCo" width="100%">
</p>

---

## Recorrido de una ejecución

```
prepare_pipeline_control
          │
          ▼
ingest_sharepoint_bronze              (SharePoint → Bronze, por corte)
          │
          ▼
slv_customers · slv_products · slv_locations · slv_orders · slv_order_details     (en paralelo)
          │
          ▼
dq_validaciones_silver                (compuerta de calidad, 21 reglas)
          │
          ▼
gld_customers · gld_fecha · gld_locations · gld_products · gld_shipping_mode      (en paralelo)
          │
          ▼
gld_orders ──▶ gld_order_details ──▶ gld_order_summary    (hechos y base única de KPIs)
          │
          ▼
dq_validaciones_gold                  (compuerta de calidad, 3 reglas)
          │
          ▼
gld_kpi_executive_summary · gld_kpi_order_details · gld_kpi_alerts · gld_kpi_region_detail
          │
          ▼
gld_reporte_excel_correo              (Excel de 4 pestañas + correo vía Graph)
          │
          ▼
finalize_pipeline_control             (cierre de la ejecución)
```
