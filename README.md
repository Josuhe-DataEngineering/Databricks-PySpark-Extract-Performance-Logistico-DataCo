<div align="center">

# 🏗️ DataCo Supply Chain · Data Lakehouse

### Plataforma de datos **ELT end-to-end** sobre Databricks Lakehouse — de SSIS on-premise a un Lakehouse cloud gobernado, con calidad declarativa, observabilidad, infraestructura como código y Machine Learning

De SharePoint al correo del área de negocio: ingesta, modelo dimensional con historial, calidad de datos, gobierno, un reporte ejecutivo que se envía solo y un modelo que anticipa retrasos en los envíos.

<br>

![Databricks](https://img.shields.io/badge/Databricks-FF3621?style=for-the-badge&logo=databricks&logoColor=white)
![Delta Lake](https://img.shields.io/badge/Delta_Lake-00ADD4?style=for-the-badge&logo=delta&logoColor=white)
![PySpark](https://img.shields.io/badge/PySpark-E25A1C?style=for-the-badge&logo=apachespark&logoColor=white)
![Unity Catalog](https://img.shields.io/badge/Unity_Catalog-FF3621?style=for-the-badge&logo=databricks&logoColor=white)
![MLflow](https://img.shields.io/badge/MLflow-0194E2?style=for-the-badge&logo=mlflow&logoColor=white)
![GitHub Actions](https://img.shields.io/badge/CI-GitHub_Actions-2088FF?style=for-the-badge&logo=githubactions&logoColor=white)
![Microsoft Graph](https://img.shields.io/badge/Microsoft_Graph-0078D4?style=for-the-badge&logo=microsoft&logoColor=white)
![Slack](https://img.shields.io/badge/Alertas-Slack-4A154B?style=for-the-badge&logo=slack&logoColor=white)

</div>

> 🚧 **En construcción** marca lo que está diseñado pero todavía no está implementado en este repositorio. Lo demás ya corre de punta a punta.

---

## 🎯 En una línea

Tomé un reporte logístico que se armaba a mano cada semana cruzando exports en Excel (2–3 horas de un analista) y lo convertí en una **plataforma de datos gobernada de punta a punta** sobre Databricks Lakehouse: ingesta desde SharePoint, procesamiento en capas con calidad de datos automática, siete indicadores de negocio, un Excel ejecutivo enviado por correo y un modelo de riesgo de retraso, con trazabilidad, alertas y despliegue como código.

## ⭐ Lo que resuelve

- **Antes:** proceso manual, lento y con cifras distintas entre áreas según el corte.
- **Ahora:** una sola corrida reproducible, con reglas de negocio centralizadas, calidad validada antes de publicar, historial de cambios, datos sensibles protegidos y entrega automática al área.

---

## 🧭 Pipeline de un vistazo

```
SharePoint ──▶ 🥉 Bronze ──▶ 🥈 Silver ──▶ ✅ Calidad ──▶ 🥇 Gold ──▶ ✅ Calidad ──▶ 📊 Excel + 📧 Correo
             (crudo, todo    (tipado,      (12 reglas   (modelo      (5 reglas      (reporte ejecutivo
              STRING +        dedupe,       + cuarentena) estrella +    de consistencia) automático)
              metadatos)      cuarentena)                 KPIs)
                                                                   └──▶ 🤖 ML: riesgo de retraso
                    └──── 📋 etl_log + 🚨 alertas Slack + 📈 dashboard de salud en cada task ────┘
```

| | |
|---|---|
| **Fuente** | Archivo en SharePoint Online, descargado vía Microsoft Graph |
| **Procesamiento** | PySpark + Spark SQL sobre Delta Lake |
| **Arquitectura** | Data Lakehouse con modelo medallón |
| **Orquestación** | Databricks Workflow (compute Serverless, en abanico, con dos compuertas de calidad) |
| **Modelo** | Esquema estrella con **SCD2** en dimensiones y hechos clave |
| **Calidad** | 18 reglas declarativas en seis dimensiones, cuarentena en las 5 tablas Silver y log de deduplicación; el dato defectuoso va a cuarentena con alerta y solo los errores propios del pipeline lo detienen |
| **Gobierno** | 🚧 *En construcción:* clasificación en 4 niveles, tags, máscara de PII, row filter y GRANT por rol en Unity Catalog |
| **Observabilidad** | Tabla `etl_log`, alerta a Slack ante cualquier fallo, vistas de salud y dashboard AI/BI |
| **Infraestructura** | 🚧 *En construcción:* Databricks Asset Bundles, ambientes dev y prod y CI/CD con GitHub Actions |
| **Entrega** | Excel de 4 pestañas enviado por correo (Microsoft Graph) |
| **ML** | 🚧 *En construcción:* modelo de riesgo de retraso con MLflow, registrado en Unity Catalog |

---

## 🔧 Qué hace cada capa

### 🥉 Bronze — ingesta cruda
Descarga el archivo desde SharePoint y carga **solo el corte de fechas** definido en una tabla de control. Todas las columnas se almacenan como **STRING**, sin inferir tipos ni aplicar reglas de negocio, para no perder información del origen. Cada fila lleva sus metadatos técnicos: fecha de carga, ejecución, origen, archivo, **hash SHA-256 del archivo**, filas del archivo y esquema original en JSON. El proceso es idempotente: si los cortes se traslapan, los días de la ventana se reemplazan y no se duplican. La tabla define una **retención de 12 meses** del historial Delta y lleva COMMENT y tags de gobierno (capa, dominio, owner y frecuencia). 🚧 *En construcción:* acceso restringido a ingeniería.

### 🥈 Silver — datos limpios y conformados
Tipado fuerte, normalización y deduplicación por llave de negocio. Separa el origen en entidades: clientes, productos, ubicaciones, pedidos y detalle de pedido. Las filas que no cumplen una regla **no se eliminan**: pasan a **cuarentena** con su motivo, en las cinco tablas, y Gold lee solo las filas válidas. Cada ejecución deja registro de la deduplicación y de la cuarentena. Cada fila conserva su trazabilidad hacia Bronze.

### ✅ Calidad de datos — compuerta entre capas
Dos tasks de validación (tras Silver y tras Gold) ejecutan el catálogo de reglas y guardan cada resultado en una tabla histórica. La decisión ante un incumplimiento está definida por regla: **detener** el pipeline, enviar a **cuarentena** o solo **advertir**.

### 🥇 Gold — modelo dimensional y KPIs
Esquema estrella listo para análisis, con **grano declarado** en cada tabla:
- **5 dimensiones** (clientes y productos con historial SCD2; ubicaciones, fecha y modo de envío) con llaves sustitutas estables por hash.
- **2 tablas de hechos** (pedidos con SCD2 y reglas de negocio; detalle de pedido).
- **Resumen por pedido** como base única de los indicadores.
- **4 vistas de KPIs:** Resumen Ejecutivo, Detalle por Región, Detalle por Orden (SCD2) y Alertas, con historial por corte.
- 🚧 *En construcción:* cada tabla documentará en su COMMENT el grano, el owner y la versión del KPI.

### 📊 Entrega a negocio
Un notebook genera el **Excel de 4 pestañas** con formato condicional tipo semáforo y variación contra el corte anterior, y lo **envía por correo** con una tabla resumen y un gráfico en el cuerpo del mensaje.

### 🤖 Machine Learning &nbsp; 🚧 *En construcción*
> 🚧 Esta capa está en desarrollo; el pipeline de datos de arriba ya corre de punta a punta sin ella.

La capa Gold alimentará un modelo que predice el **riesgo de retraso** de cada envío. Las variables se construirán sin fuga de datos, el entrenamiento se registrará en **MLflow**, el modelo quedará versionado en **Unity Catalog** y sus predicciones se guardarán en una tabla Gold.

---

## 📐 Los 7 indicadores

On-Time Delivery % · Late Delivery Risk % · Shipping Variance · Profit Margin % · Revenue por Cliente · Beneficio por Orden · Lead Time Promedio

Con agrupaciones de negocio **GLOBAL** (todos los mercados) y **AMERICAS** (LATAM + USCA), y reglas de alcance: se excluyen los pedidos cancelados y se marcan los sospechosos de fraude.

---

## 🗂️ Modelo dimensional

```
        dim_customers        dim_products
              │                    │
              ▼                    ▼
  dim_fecha ─▶ fact_orders ◀─ fact_order_details ◀─ dim_products
              ▲       ▲
        dim_locations  dim_shipping_mode
```

Las dimensiones de clientes y productos y la tabla de hechos de pedidos usan **SCD2** sobre una lista explícita de columnas de seguimiento: conservan el historial, de modo que cada pedido puede analizarse con los atributos vigentes en su momento. 🚧 *En construcción:* llaves primarias y foráneas informativas, restricciones `NOT NULL` y `CHECK`, y un `COMMENT` en cada tabla y columna.

---

## 🛡️ Calidad de datos

### Cuarentena y deduplicación con trazabilidad

Ningún registro se elimina. Cada tabla Silver agrega tres columnas (`estado_calidad`: `VALIDO` o `CUARENTENA`, `motivo_cuarentena` y `fecha_procesamiento`) y **Gold lee únicamente las filas `VALIDO`**.

| Tabla Silver | Grano (una fila por…) | Motivos de cuarentena |
|---|---|---|
| `hd_pedidos` | pedido (`order_id`) | `ORDER_ID_INVALIDO` · `FECHA_PEDIDO_INVALIDA` · `CLIENTE_NO_INFORMADO` · `RIESGO_RETRASO_INVALIDO` |
| `hd_pedido_detalle` | ítem del pedido (`order_item_id`) | `ITEM_ID_INVALIDO` · `CANTIDAD_INVALIDA` |
| `md_clientes` | cliente (`customer_id`) | `CLIENTE_ID_INVALIDO` |
| `md_productos` | producto (`product_card_id`) | `PRODUCTO_ID_INVALIDO` |
| `md_ubicaciones` | combinación geográfica (market, región, país, estado, ciudad y código postal) | `UBICACION_INCOMPLETA` |

Cada fila recibe un solo motivo: el primero que se cumple, en un orden definido por tabla. Dos tablas de control en `metadata_dataco` registran cada ejecución:

- **`hd_deduplicacion_log`:** filas de entrada y de salida por tabla, filas agrupadas (informativo) y **duplicados reales**, que debe ser 0.
- **`hd_cuarentena_resumen`:** filas en cuarentena por tabla y motivo.

**Resultado de la última carga:** 180,314 filas de Bronze → 65,547 pedidos, 180,314 líneas de detalle, 20,447 clientes, 118 productos y 3,800 ubicaciones; **0 duplicados reales** y 0 filas en cuarentena. Gold: 64,184 pedidos vigentes (los cancelados se excluyen por regla de negocio).

### Motor declarativo de reglas

El motor se basa en dos tablas: un **catálogo de reglas** y un **historial de resultados** por ejecución.

| Dimensión | Qué verifica | Ejemplos |
|---|---|---|
| **Unicidad** | Una fila por llave de negocio | `order_id`, `order_item_id`, `customer_id`, `product_card_id` |
| **Completitud** | Campos obligatorios informados | Fechas de pedido y de envío |
| **Validez** | Valores dentro del dominio | Riesgo de retraso en {0,1}; cantidad > 0 |
| **Integridad referencial** | Las referencias existen | Detalle → pedido, pedido → cliente |
| **Consistencia** | Silver y Gold cuadran | Pedidos vigentes = pedidos no cancelados; un resumen por pedido |
| **Actualidad** | El dato llegó a tiempo | El último corte cargado respeta el umbral de frescura |

Cada regla se define en lenguaje de negocio, con **criticidad**, **umbral** justificado, **decisión** ante incumplimiento, owner y steward. El criterio es: el dato defectuoso va a **cuarentena** con alerta a Slack sin detener el pipeline; un exceso sobre el umbral solo **advierte**; el pipeline **se detiene** únicamente ante errores propios (duplicados tras deduplicar, llaves rotas en Gold o Silver que no cuadra con Gold).

Dos tasks de validación (tras Silver y tras Gold) ejecutan el catálogo y guardan cada resultado en la tabla histórica, para ver la tendencia por ejecución.

### 🧪 Pruebas con datos defectuosos

Cada comportamiento se prueba con **datos sintéticos** en un esquema aislado (`pruebas_calidad`), con el resultado esperado definido de antemano. Los datos reales y los logs de producción no se tocan: los mismos notebooks de Silver y Gold corren apuntando, por parámetro, al esquema de prueba.

| Etapa | Qué se prueba | Volumen | Resultado esperado |
|---|---|---|---|
| **1. Cuarentena** | Los 9 motivos, un caso por motivo | 1,000 filas por motivo y 1,000 filas sanas de control | La fila se aparta con su motivo y el pipeline sigue |
| **1b. Prioridad** | Filas con dos defectos a la vez | 100 filas por combinación | Gana el primer motivo en el orden de la regla |
| **2. Advertir** | Un exceso sobre el umbral | 1,000 filas o más | El pipeline sigue; queda una advertencia en el historial y llega la alerta a Slack |
| **3. Detener** | Errores propios del pipeline (duplicados tras deduplicar, llaves rotas en Gold, Silver ≠ Gold) | 1,000 filas o más | La task falla, se registra el error y el Workflow se detiene |

El notebook de verificación compara, por tabla y motivo, lo **esperado**, lo **registrado en el log** y lo **realmente guardado en Silver**, y termina con error si algún conteo no coincide. Las filas defectuosas se generan por código, a partir de filas reales con una semilla fija, así que la prueba es reproducible. El conteo esperado depende del grano de cada tabla: 1,000 filas con `customer_id` en cero producen una sola fila en cuarentena, porque comparten la misma llave.

---

## 🔐 Gobierno de datos (Unity Catalog) &nbsp; 🚧 *En construcción*

- **Clasificación en 4 niveles** (Público, Interno, Confidencial, Restringido) aplicada por atributo y convertida en **tags** de Unity Catalog, alineada con la Ley 29733 de protección de datos personales.
- **Enmascaramiento dinámico** del correo del cliente y **filtro de filas** según el grupo del usuario (`dac_lectores`).
- **GRANT por rol:** Bronze solo para ingeniería; Silver para analistas avanzados; Gold para consumo.
- **Owner por rol** y steward en los tags de cada tabla, **diccionario de datos** como tabla consultable y **linaje** completo Bronze → Silver → Gold.
---

## 📈 Observabilidad

- **Tabla `etl_log`:** cada notebook registra inicio, fin, filas procesadas y estado (`EN_PROCESO → EXITOSO / ERROR`), con un identificador único por ejecución.
- **Manejo de errores:** cada task tiene su task de log que, ante un fallo, registra el detalle técnico y **avisa a Slack**. El Workflow se detiene cuando una task falla.
- **Control de corte:** una tabla de parámetros define la ventana a procesar; reprocesar el mismo corte es idempotente.
- **Dashboard AI/BI "Salud del pipeline":** estado de la última ejecución, duración por notebook, tendencia diaria y errores recientes.

<p align="center">
  <img src="docs/dashboard_salud_pipeline.png" alt="Dashboard de salud del pipeline DataCo" width="100%">
</p>

---

## 🔄 Tubería de datos de punta a punta

Pipeline orquestado como un único Databricks Workflow en abanico: dentro de cada capa, las tasks que no dependen entre sí (las 5 de Silver y las 7 de Gold) se ejecutan en paralelo. Entre capas, las tasks de calidad **`dq_validaciones_silver`** y **`dq_validaciones_gold`** validan los datos y detienen el flujo si una regla crítica falla. Cada task tiene su `log_error` que, ante un fallo, registra la excepción en `hd_etl_log` y notifica a Slack.

<p align="center">
  <img src="docs/workflow.png" alt="Tubería de datos DataCo en abanico: cada task de negocio con su task log_error, de la ingesta al envío del correo" width="100%">
</p>

**Recorrido de una ejecución**

```
prepare_pipeline_control
      │
      ▼
ingest_sharepoint_bronze                      (SharePoint → Bronze, por corte)
      │
      ├─▶ slv_customer · slv_products · slv_locations · slv_orders · slv_order_details
      │
      ▼
dq_validaciones_silver                        (compuerta de calidad)
      │
      ├─▶ gld_customers · gld_products · gld_locations · gld_fecha · gld_shipping_mode
      │        gld_orders · gld_order_details
      │
      ▼
gld_order_summary                             (base única de los KPIs)
      │
      ├─▶ gld_kpi_executive_summary · gld_kpi_region_detail
      │        gld_kpi_order_details · gld_kpi_alerts
      │
      ▼
dq_validaciones_gold                          (compuerta de calidad)
      │
      ▼
gld_reporte_excel_correo                      (Excel de 4 pestañas + correo vía Graph)
      │
      ▼
finalize_pipeline_control                     (cierre de la ejecución)
```

---

## ⚙️ Infraestructura como código y CI/CD &nbsp; 🚧 *En construcción*

- **Databricks Asset Bundles:** el Job, sus tasks, dependencias, parámetros, reintentos, notificaciones y reglas de salud (por ejemplo, alerta si la ejecución supera los 20 minutos) se describen en YAML y se despliegan con un solo comando.
- **Ambientes dev y prod** separados por catálogo, con el mismo código y distinto destino.
- **GitHub Actions:** en cada pull request se validan el bundle y el estilo del código; al fusionar a `main` se despliega.
- **Secretos** solo en Databricks Secret Scopes; ningún secreto ni dato sensible en el repositorio.

---

## 🛠️ Stack

| Área | Tecnología |
|---|---|
| Plataforma | Databricks · Serverless |
| Procesamiento | PySpark · Spark SQL |
| Almacenamiento | Delta Lake |
| Catálogo y gobierno | Unity Catalog |
| Ingesta y correo | Microsoft Graph API |
| Secretos | Databricks Secret Scopes |
| Alertas | Webhook de Slack |
| Reportería | openpyxl · matplotlib · Dashboards AI/BI |
| Machine Learning 🚧 | MLflow · Unity Catalog Models |
| IaC y CI/CD 🚧 | Databricks Asset Bundles · GitHub Actions |

---

## 📁 Organización del repositorio

```
00_metadata/                  # control del pipeline (prepare / finalize), logs y observabilidad (tablas de calidad, vistas de salud)
01_ingest_sharepoint_bronze/  # ingesta a Bronze + logs
02_silver_dimensiones/        # clientes, productos, ubicaciones + logs
02_silver_hechos/             # pedidos, detalle de pedido + logs
03_gold_dimensiones/          # 5 dimensiones (clientes, fecha, ubicaciones, productos, modo de envío) + logs
03_gold_hechos/               # pedidos, detalle de pedido, resumen por pedido + logs
03_gold_kpis/                 # 4 KPIs (resumen ejecutivo, alertas, detalle de pedido, detalle por región) + logs
04_reporte_excel_correo/      # reporte Excel enviado por correo + logs
05_pruebas_calidad/           # datos sintéticos defectuosos y verificación de cada regla
06_calidad_datos/             # motor de validaciones (23 reglas) + logs
requerimientos/               # especificación no técnica del proyecto
docs/                         # diagrama del workflow, dashboard de salud y pruebas manuales (🚧 ADRs: decisiones de arquitectura)
05_ml/                        # 🚧 variables, entrenamiento, registro y predicciones
resources/                    # 🚧 Asset Bundle (Job, ambientes, reglas de salud)
.github/workflows/            # 🚧 CI/CD con GitHub Actions
```

Cada carpeta separa el notebook de negocio (`01_negocio/`) de su notebook de manejo de errores (`02_logs/`). 🚧 *En construcción:* cada notebook declarará en su cabecera la capa, sus entradas y salidas, su owner y las reglas de calidad asociadas.

---

## 📚 Decisiones de arquitectura (ADRs) &nbsp; 🚧 *En construcción*

Cada decisión relevante está documentada en `docs/adr/` con su contexto, la alternativa descartada y su consecuencia:

- Bronze en STRING y sin inferencia de tipos, y su retención.
- Cuarentena en lugar de eliminación de filas.
- Prefijos de tabla (`md_`, `hd_`, `desc_`) y excepciones documentadas.
- Llaves sustitutas por hash estable en dimensiones.
- Parámetros de calidad: umbrales y decisión por regla.
- Por qué un Lakehouse para un volumen moderado: gobierno, trazabilidad y reproducibilidad, no escala.

---

## 🧩 Contexto del proyecto

Proyecto que **migra un proceso tradicional** (SQL Server Integration Services sobre Data Warehouse on-premise) a una **arquitectura Lakehouse en la nube**, conservando las reglas de negocio del reporte original. 
El dataset es público (*DataCo Smart Supply Chain*, Kaggle) y la infraestructura es real.

---

<div align="center">

**Josuhe Sosa Lara** · Data Engineering · Lima, Perú

*Dataset público · infraestructura real · construido de punta a punta sobre Databricks Lakehouse.*

</div>
