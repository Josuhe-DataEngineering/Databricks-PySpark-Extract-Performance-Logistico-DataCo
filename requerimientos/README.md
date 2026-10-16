<div align="center">

<img src="https://img.shields.io/badge/ESPECIFICACI%C3%93N%20NO%20T%C3%89CNICA-1B3139?style=for-the-badge&logoColor=white" alt="header"/>

# Reporte de Performance Logístico y Riesgo de Entrega por Región

<img src="https://img.shields.io/badge/Plataforma-Data_Lakehouse_en_Databricks-0078D4?style=for-the-badge&logo=databricks&logoColor=white" alt="Databricks"/>
<img src="https://img.shields.io/badge/Prioridad-Alta-E8412C?style=for-the-badge" alt="Alta"/>
<img src="https://img.shields.io/badge/%C3%81rea-Supply_Chain-1B3139?style=for-the-badge" alt="Supply Chain"/>

<br/>

📄 [Descargar versión Word](./Especificacion_No_Tecnica_DataCo_Databricks.docx)

</div>

---

<details open>
<summary><strong>📑 Tabla de Contenidos</strong></summary>

| N° | Sección | Descripción |
|:--:|---------|-------------|
| I | [Historia de los Cambios](#i-historia-de-los-cambios) | Control de versiones del documento |
| II | [Origen de la Solicitud](#ii-origen-de-la-solicitud) | Datos del solicitante y clasificación |
| III | [Detalle de la Solicitud](#iii-detalle-de-la-solicitud) | Descripción, alcance, indicadores, reglas, calidad, ML |
| IV | [Propuesta de Solución](#iv-propuesta-de-solución-para-ser-llenado-por-el-proveedor) | Arquitectura Lakehouse, modelo de datos, entregables |

</details>

---

## I. Historia de los Cambios

<table>
<thead>
<tr>
<th align="center">Versión</th>
<th align="center">Fecha</th>
<th>Responsable de la modificación</th>
<th>Breve descripción del (los) cambio(s) del documento</th>
</tr>
</thead>
<tbody>
<tr>
<td align="center"><strong>1</strong></td>
<td align="center">01/10/2026</td>
<td>Ingeniería de Datos</td>
<td>Versión inicial del requerimiento sobre Databricks Data Lakehouse, incluye el requerimiento de modelo predictivo de riesgo de entrega.</td>
</tr>
<tr>
<td align="center">2</td>
<td align="center"></td>
<td></td>
<td></td>
</tr>
<tr>
<td align="center">3</td>
<td align="center"></td>
<td></td>
<td></td>
</tr>
</tbody>
</table>

---

## II. Origen de la Solicitud

<table>
<tbody>
<tr>
<td><strong>Asunto:</strong></td>
<td colspan="3">Reporte de Performance Logístico y Riesgo de Entrega por Región</td>
</tr>
<tr>
<td><strong>Fecha de la Solicitud:</strong></td>
<td>01/10/2026</td>
<td><strong>Tipo de solicitud:</strong></td>
<td>Nuevo reporte y modelo predictivo</td>
</tr>
<tr>
<td><strong>Nombre de quien realiza la Solicitud:</strong></td>
<td>[Nombre del KU]</td>
<td><strong>Firma:</strong></td>
<td></td>
</tr>
<tr>
<td><strong>Área:</strong></td>
<td>Operaciones / Logística</td>
<td><strong>Módulo:</strong></td>
<td>Supply Chain</td>
</tr>
<tr>
<td><strong>Prioridad:</strong></td>
<td>Alta (X) &nbsp; Media () &nbsp; Baja ()</td>
<td></td>
<td></td>
</tr>
</tbody>
</table>

---

## III. Detalle de la Solicitud

### Descripción del Cambio Propuesto

> **Responsable: KU**

Actualmente el área de Operaciones no cuenta con una vista consolidada que permita medir, con periodicidad semanal, el performance de entrega de la cadena logística ni el nivel de riesgo de entregas tardías que se produce a nivel de orden y región. Esta información se arma manualmente en Excel cruzando exportaciones del ERP, proceso que toma entre 2 y 3 horas por semana a un analista de BI y que genera diferencias entre áreas que trabajan con cortes distintos.

Se requiere consolidar esta información en una plataforma de datos con arquitectura **Data Lakehouse sobre Databricks**, que alimente un reporte automático semanal para el equipo de Supply Chain y las gerencias regionales (LATAM, Europe, USCA, Pacific Asia, Africa), de modo que puedan decidir con oportunidad sobre la priorización de envíos, la selección de modos de transporte y la gestión de reclamos por entregas tardías.

Adicionalmente, se requiere pasar de **medir** el retraso a **anticiparlo**: un modelo predictivo que estime, para cada orden, la probabilidad de entrega tardía con la información disponible al momento de crearla.

---

### Alcance de la Solicitud

<table>
<thead>
<tr>
<th>Componente</th>
<th>Descripción</th>
<th>Resultado esperado</th>
</tr>
</thead>
<tbody>
<tr>
<td><img src="https://img.shields.io/badge/Componente_1-Reporte-0078D4?style=flat-square" alt="C1"/></td>
<td>Ingesta, limpieza, modelado y cálculo de los 7 indicadores logísticos.</td>
<td>Excel de 4 pestañas enviado por correo cada semana.</td>
</tr>
<tr>
<td><img src="https://img.shields.io/badge/Componente_2-Calidad_y_Gobierno-1B3139?style=flat-square" alt="C2"/></td>
<td>Validación de datos entre capas, trazabilidad, clasificación y protección de datos personales.</td>
<td>Cifras confiables, auditables y con acceso controlado por rol.</td>
</tr>
<tr>
<td><img src="https://img.shields.io/badge/Componente_3-Predicci%C3%B3n-E8412C?style=flat-square" alt="C3"/></td>
<td>Modelo de clasificación del riesgo de entrega tardía por orden.</td>
<td>Probabilidad de retraso por orden disponible para el reporte y las alertas.</td>
</tr>
</tbody>
</table>

---

### Presentación

El reporte final se entrega en formato Excel y consta de **4 pestañas**:

| Pestaña | Contenido |
|---------|-----------|
| **RESUMEN EJECUTIVO** | KPIs totalizados por mercado (market), con variación contra el corte anterior. |
| **DETALLE REGIÓN** | Grano región + modo de envío con sus 7 indicadores. |
| **DETALLE ORDEN** | Máximo grano, usado por el área para decisiones puntuales y reclamos. |
| **ALERTAS** | Órdenes que cumplen el criterio de riesgo crítico y, cuando el modelo predictivo esté en operación, su probabilidad de retraso estimada. |

Adicionalmente, el equipo de Ingeniería de Datos dispone de un **tablero de salud** de la plataforma (estado de cada ejecución, duración, filas procesadas y errores) para uso interno.

---

### Origen de la Información

La información se consume desde archivos CSV descargados de Kaggle y publicados en una biblioteca de SharePoint Online corporativa, para simular el flujo de un entorno real:

`\\sharepoint.corp\sites\SupplyChain\ExportsDiarios\`

| Archivo | Descripción |
|---------|-------------|
| **DataCoSupplyChainDataset.csv** | Dataset principal de órdenes, envíos, clientes, productos y financieros (+180,000 registros, 53 columnas). Actualización semanal. |
| **DescriptionDataCoSupplyChain.csv** | Diccionario de datos con la descripción de cada variable del dataset principal. |
| **tokenized_access_logs.csv** | Datos de clickstream (no estructurado). Uso complementario; no forma parte del reporte principal. |

> **Fuente:** Kaggle – [DataCo Smart Supply Chain for Big Data Analysis](https://www.kaggle.com/datasets/shashwatwork/dataco-smart-supply-chain-for-big-data-analysis)

---

### Particularidades de la Fuente

- El dataset principal viene en formato CSV separado por coma, con codificación **Latin-1**. Se debe cuidar el tratamiento de acentos en nombres de ciudades y países.
- Las fechas de orden y envío vienen en formato `mm/dd/yyyy HH:MM` y deben convertirse a fecha y hora.
- La fuente se entrega por **cortes de fechas**, y los cortes consecutivos pueden traslaparse. Reprocesar una ventana no debe duplicar registros.
- Existen registros con `customer_id` nulo o con `order_status = 'SUSPECTED_FRAUD'` que deben tratarse con criterio (ver reglas de negocio).
- Pueden existir filas duplicadas. La llave natural de la línea de orden es `order_id + order_item_id`.
- El campo `late_delivery_risk` viene precalculado en el CSV. Se debe validar si coincide con el cálculo propio (`days_real > days_scheduled`).
- El archivo contiene datos personales de clientes (nombre, correo, dirección) y un campo de contraseña (`customer_password`). **Este último no debe ingresar a las capas de análisis**; los datos personales deben quedar protegidos según su clasificación.

---

### Desarrollo del Reporte

<img src="https://img.shields.io/badge/7_INDICADORES_LOG%C3%8DSTICOS-0078D4?style=for-the-badge" alt="KPIs"/>

El analista actualmente descarga el CSV principal manualmente, lo pega en un libro maestro de Excel y aplica tablas dinámicas con fórmulas para obtener los indicadores. Se solicita automatizar este cálculo de modo que el resultado sea **idéntico** al del trabajo manual.

<table>
<thead>
<tr>
<th align="center">N°</th>
<th>Indicador</th>
<th>Fórmula</th>
<th>Consideración / Granularidad</th>
</tr>
</thead>
<tbody>
<tr>
<td align="center">1</td>
<td><strong>On-Time Delivery %</strong></td>
<td><code>Σ (órdenes donde days_real ≤ days_scheduled) / Σ (total órdenes)</code></td>
<td>Calcular por región y por modo de envío. La granularidad más fina es la orden individual.</td>
</tr>
<tr>
<td align="center">2</td>
<td><strong>Late Delivery Risk %</strong></td>
<td><code>Σ (late_delivery_risk = 1) / Σ (total órdenes)</code></td>
<td>El campo ya viene precalculado en el CSV. Comparar contra el cálculo propio como validación cruzada.</td>
</tr>
<tr>
<td align="center">3</td>
<td><strong>Shipping Variance</strong></td>
<td><code>days_for_shipping_real – days_for_shipment_scheduled</code></td>
<td>Si el resultado es positivo, la entrega se retrasó. Promediar a nivel región.</td>
</tr>
<tr>
<td align="center">4</td>
<td><strong>Profit Margin %</strong></td>
<td><code>(order_profit_per_order / sales) × 100</code></td>
<td>Hay órdenes con margen negativo (pérdida). No filtrar, solo resaltar.</td>
</tr>
<tr>
<td align="center">5</td>
<td><strong>Revenue por Cliente</strong></td>
<td><code>Σ (sales) / COUNT(DISTINCT customer_id)</code></td>
<td>Segmentar por customer_segment. Un mismo cliente puede tener múltiples órdenes.</td>
</tr>
<tr>
<td align="center">6</td>
<td><strong>Beneficio por Orden</strong></td>
<td><code>sales – (product_price × order_item_quantity – order_profit_per_order)</code></td>
<td>Validar con 5 órdenes de muestra que el cálculo cierre.</td>
</tr>
<tr>
<td align="center">7</td>
<td><strong>Lead Time Promedio</strong></td>
<td><code>AVG(days_for_shipping_real) agrupado por shipping_mode</code></td>
<td>Considerar solo órdenes con delivery_status distinto de 'Shipping canceled'.</td>
</tr>
</tbody>
</table>

---

### Reglas de Negocio

<table>
<thead>
<tr>
<th>Regla</th>
<th>Detalle</th>
</tr>
</thead>
<tbody>
<tr>
<td><strong>Agrupaciones</strong></td>
<td>GLOBAL = LATAM + Europe + USCA + Pacific Asia + Africa. &nbsp; AMERICAS = LATAM + USCA. Cada indicador se publica por mercado y en ambas agrupaciones.</td>
</tr>
<tr>
<td><strong>Alcance por order_status</strong></td>
<td>Excluir las órdenes con <code>order_status = 'CANCELED'</code>. Las órdenes <code>'SUSPECTED_FRAUD'</code> se incluyen y se marcan visualmente.</td>
</tr>
<tr>
<td><strong>Shipping canceled</strong></td>
<td>Las órdenes con <code>delivery_status = 'Shipping canceled'</code> se muestran en el detalle, pero <strong>no</strong> entran al cálculo de On-Time Delivery % ni de Lead Time.</td>
</tr>
<tr>
<td><strong>Fecha de corte</strong></td>
<td>Siempre el domingo anterior a la ejecución. Los indicadores se calculan acumulados hasta el corte.</td>
</tr>
<tr>
<td><strong>Historial</strong></td>
<td>Cada corte conserva su propia fotografía de indicadores para poder comparar contra el corte anterior y reconstruir cualquier reporte pasado.</td>
</tr>
<tr>
<td><strong>Historia de cambios</strong></td>
<td>Si cambia un atributo relevante de un cliente, producto u orden, debe conservarse la versión anterior con su vigencia.</td>
</tr>
<tr>
<td><strong>Alerta de riesgo crítico</strong></td>
<td>Orden con <code>late_delivery_risk = 1</code> cuya región tiene On-Time Delivery % menor a 70%.</td>
</tr>
</tbody>
</table>

#### Formato condicional esperado en el Excel final

| Condición | Formato |
|-----------|---------|
| On-Time Delivery % < 70% | 🔴 Celda en rojo |
| On-Time Delivery % entre 70% y 89.9% | 🟡 Celda en amarillo |
| Late Delivery Risk % > 55% | 🔴 Celda en rojo |
| Profit Margin % < 0 (pérdida) | 🔴 Fila completa en rojo claro |
| Shipping Variance > 5 días | 🔴 Texto rojo en la fila |

---

### Frecuencia de Actualización

> 📅 **Semanal**, todos los lunes, con corte al domingo anterior.
>
> 📧 Envío por correo al grupo de distribución **`BI_Rpt_PerformanceLogistico_DataCo`** antes de las **8:00 am**.

---

### Requerimientos de Calidad de Datos

<img src="https://img.shields.io/badge/CALIDAD_DE_DATOS-1B3139?style=for-the-badge" alt="DQ"/>

Los datos deben validarse entre capas antes de publicarse en el reporte. Principios solicitados:

- Ningún registro defectuoso se elimina: se **aísla en cuarentena** con su motivo, para su revisión posterior.
- La ejecución **se detiene únicamente por errores propios del proceso** (por ejemplo, un duplicado que sobrevivió a la deduplicación o un hecho sin su dimensión). Un dato defectuoso de la fuente no detiene el reporte.
- Cuando una regla supera su umbral de tolerancia, se **notifica** al equipo, sin detener la ejecución.
- Cada validación deja evidencia histórica: regla, ejecución, filas evaluadas, filas que incumplen, porcentaje y decisión.

<table>
<thead>
<tr>
<th>Dimensión de calidad</th>
<th>Regla de negocio</th>
<th>Si no se cumple</th>
</tr>
</thead>
<tbody>
<tr>
<td><strong>Unicidad</strong></td>
<td>Cada orden, línea de orden, cliente y producto aparece una sola vez.</td>
<td>⛔ Detener la ejecución</td>
</tr>
<tr>
<td><strong>Completitud</strong></td>
<td>Toda orden tiene fecha de orden y cliente informado; toda orden tiene fecha de envío.</td>
<td>⚠️ Cuarentena / Advertencia</td>
</tr>
<tr>
<td><strong>Validez</strong></td>
<td><code>late_delivery_risk</code> solo toma valor 0 o 1; la cantidad de cada línea es mayor que 0; <code>order_status</code> pertenece a los valores conocidos.</td>
<td>⚠️ Cuarentena / Advertencia</td>
</tr>
<tr>
<td><strong>Integridad referencial</strong></td>
<td>Toda línea apunta a una orden y a un producto existentes; toda orden apunta a un cliente existente (tolerancia mínima 99.5%); todo hecho apunta a sus dimensiones.</td>
<td>⚠️ Cuarentena / ⛔ Detener</td>
</tr>
<tr>
<td><strong>Consistencia</strong></td>
<td>Las órdenes vigentes del reporte son iguales a las órdenes válidas no canceladas de la capa limpia; un solo resumen por orden; fecha de envío no anterior a fecha de orden.</td>
<td>⛔ Detener / ⚠️ Advertencia</td>
</tr>
<tr>
<td><strong>Actualidad</strong></td>
<td>El último corte cargado corresponde al corte esperado según la tabla de control.</td>
<td>⚠️ Advertencia</td>
</tr>
</tbody>
</table>

---

### Requerimientos de Gobierno y Seguridad

<img src="https://img.shields.io/badge/GOBIERNO_Y_SEGURIDAD-1B3139?style=for-the-badge" alt="GOV"/>

- **Clasificación** de cada atributo en cuatro niveles (Público, Interno, Confidencial, Restringido), alineada con la Ley N.° 29733 de Protección de Datos Personales del Perú.
- **Protección de datos personales:** el correo del cliente se enmascara para los usuarios sin autorización y el acceso a filas se restringe según el grupo del usuario.
- **Acceso por rol:** la capa cruda solo para Ingeniería de Datos; la capa limpia para analistas avanzados; la capa de consumo para usuarios del reporte.
- **Credenciales** (SharePoint, correo, alertas) fuera del código, en un almacén de secretos.
- **Propiedad y documentación:** cada tabla tiene un responsable (owner), un steward, su grano y su descripción de negocio. El linaje de datos debe ser consultable de la fuente al reporte.

---

### Requerimiento de Modelo Predictivo (Machine Learning)

<img src="https://img.shields.io/badge/MACHINE_LEARNING-E8412C?style=for-the-badge&logo=mlflow&logoColor=white" alt="ML"/>

El área requiere anticipar cuáles órdenes tienen mayor probabilidad de llegar tarde, para actuar antes del retraso (cambiar el modo de envío, priorizar el despacho o avisar al cliente).

<table>
<thead>
<tr>
<th width="200">Aspecto</th>
<th>Detalle</th>
</tr>
</thead>
<tbody>
<tr>
<td><strong>Problema</strong></td>
<td>Clasificación binaria: ¿la orden llegará tarde? (variable objetivo: <code>late_delivery_risk</code>, 0 o 1).</td>
</tr>
<tr>
<td><strong>Unidad de predicción</strong></td>
<td>Una orden.</td>
</tr>
<tr>
<td><strong>Información permitida</strong></td>
<td>Solo atributos conocidos <strong>al crear la orden</strong>: modo de envío, días programados, mercado, región, país, cantidad de líneas y unidades, monto, descuento, categoría y departamento del producto, segmento del cliente, mes y día de la semana.</td>
</tr>
<tr>
<td><strong>Información prohibida</strong></td>
<td>Días reales de envío y estado de entrega: son resultados que se conocen después y producirían una predicción engañosa (fuga de datos).</td>
</tr>
<tr>
<td><strong>Validación</strong></td>
<td>Partición <strong>temporal</strong>: se entrena con las órdenes más antiguas y se valida con las más recientes, nunca de forma aleatoria.</td>
</tr>
<tr>
<td><strong>Comparación</strong></td>
<td>El modelo debe superar a una regla simple de referencia (por ejemplo, el promedio de retraso por modo de envío).</td>
</tr>
<tr>
<td><strong>Métricas</strong></td>
<td>AUC-ROC y AUC-PR, junto con precisión y recuperación al umbral elegido, e informe del desbalance de clases.</td>
</tr>
<tr>
<td><strong>Trazabilidad</strong></td>
<td>Cada experimento registra parámetros, métricas, variables y versión de los datos. El modelo se versiona y queda gobernado en el catálogo de datos.</td>
</tr>
<tr>
<td><strong>Resultado</strong></td>
<td>Tabla de predicciones con la probabilidad por orden, el modelo y la versión que la generó, incorporada a la pestaña ALERTAS.</td>
</tr>
<tr>
<td><strong>Operación</strong></td>
<td>La predicción se ejecuta como un paso más del proceso semanal. Si no hay un modelo vigente, el paso falla de forma controlada sin afectar los 7 indicadores.</td>
</tr>
</tbody>
</table>

---

### Requerimientos No Funcionales

<table>
<thead>
<tr>
<th width="180">Requerimiento</th>
<th>Descripción</th>
</tr>
</thead>
<tbody>
<tr>
<td><strong>Idempotencia</strong></td>
<td>Ejecutar el mismo corte más de una vez deja el resultado idéntico, sin duplicados ni versiones espurias del historial.</td>
</tr>
<tr>
<td><strong>Trazabilidad</strong></td>
<td>De cada cifra se debe poder llegar al archivo, corte y ejecución de origen.</td>
</tr>
<tr>
<td><strong>Observabilidad</strong></td>
<td>Cada paso registra inicio, fin, filas procesadas y estado. Ante cualquier fallo se alerta al equipo.</td>
</tr>
<tr>
<td><strong>Reproducibilidad</strong></td>
<td>La misma entrada produce el mismo resultado (reglas deterministas y llaves estables).</td>
</tr>
<tr>
<td><strong>Seguridad</strong></td>
<td>Sin secretos en el código ni contraseñas de clientes en el análisis; acceso por rol.</td>
</tr>
<tr>
<td><strong>Retención</strong></td>
<td>Historial de cambios de las tablas durante 365 días, para auditoría y reconstrucción de cortes anteriores.</td>
</tr>
<tr>
<td><strong>Mantenibilidad</strong></td>
<td>Lógica común reutilizable, convención de nombres uniforme y documentación de decisiones de arquitectura.</td>
</tr>
<tr>
<td><strong>Despliegue repetible</strong></td>
<td>La definición del proceso y su despliegue entre ambientes (desarrollo y producción) es versionada como código.</td>
</tr>
</tbody>
</table>

---

### Consideraciones Técnicas Sugeridas (para el equipo de TI)

<img src="https://img.shields.io/badge/STACK_TECNOL%C3%93GICO-0078D4?style=for-the-badge&logo=databricks&logoColor=white" alt="Tech"/>

| Capacidad | Tecnología |
|-----------|------------|
| Arquitectura | **Data Lakehouse en Databricks** con patrón medallón de 3 capas: Bronze → Silver → Gold |
| Gobierno | **Unity Catalog**: un catálogo por capa más un catálogo de metadatos de control |
| Almacenamiento | **Delta Lake** (transacciones, historial y time-travel) |
| Extracción | **Microsoft Graph** para SharePoint Online, credenciales en **Secret Scopes** |
| Orquestación | **Databricks Workflows** sobre cómputo **serverless** con tareas en paralelo |
| Transformaciones | **PySpark y Spark SQL**; dimensiones SCD tipo 2 donde se requiera historial |
| Idempotencia | Reemplazo de la ventana de fechas (`replaceWhere`) en lugar de agregar filas |
| Auditoría | Tablas de control + tablero **AI/BI** de salud del proceso |
| Alertas | **Slack** y correo ante cualquier fallo; envío del reporte con Microsoft Graph |
| Machine Learning | **MLflow** (experimentos) y registro de modelos en **Unity Catalog** |
| CI/CD | **Databricks Asset Bundles** y **GitHub Actions**; código versionado en GitHub |

---

### Justificación

> **Responsable: KU**

- Reducir las 2-3 horas semanales que el analista invierte armando el reporte a mano, liberando tiempo para análisis de valor.
- Eliminar las diferencias de cifras entre áreas que hoy trabajan con cortes distintos del mismo dato.
- Detectar órdenes con riesgo de entrega tardía el mismo día en que ocurren, y no 2-3 días después como ocurre hoy.
- Anticipar el retraso con un modelo predictivo, para pasar de una gestión reactiva a una preventiva.
- Contar con datos gobernados y trazables, con protección de los datos personales de clientes.

---

### Impacto en el Proyecto si el cambio no se implementa

> **Responsable: KU**

- El tiempo de reacción ante alertas de entrega sigue siendo de 48-72 horas.
- El cálculo de la venta afectada por entregas tardías continúa haciéndose a destiempo, impactando las decisiones de la semana siguiente.
- Se mantiene el riesgo de errores por copy/paste manual.
- Los datos personales de clientes continúan circulando en archivos sin control de acceso.

---

### Alternativas de Solución si el cambio no se implementa

> **Responsable: KU**

| Plan | Descripción | Limitación |
|------|-------------|------------|
| **Plan B 1** | Construir el reporte conectando Power BI directamente al CSV. | No pasa por el Lakehouse, no cumple con la política de consolidar datos en la plataforma corporativa, y no ofrece historial ni trazabilidad. |
| **Plan B 2** | Mantener el proceso manual con macros de Excel mejoradas. | No resuelve las diferencias de corte entre áreas. |
| **Plan B 3** | Una base de datos relacional con paquetes de integración en servidor propio. | Requiere infraestructura y mantenimiento, y no cubre de forma nativa el modelo predictivo ni el gobierno de datos. |

---

### Casos de Prueba que aseguren el desarrollo

> **Responsable: KU** — Propuesta de periodo de prueba:

<table>
<thead>
<tr>
<th align="center">N°</th>
<th>Caso de prueba</th>
<th>Criterio de aceptación</th>
</tr>
</thead>
<tbody>
<tr>
<td align="center">1</td>
<td>Ejecución en paralelo con el proceso manual durante 2 semanas (2 ejecuciones).</td>
<td>Los 7 indicadores coinciden con el Excel manual; se acepta diferencia ≤ 0.5% atribuible a redondeos.</td>
</tr>
<tr>
<td align="center">2</td>
<td>Reprocesamiento: correr dos veces el mismo corte.</td>
<td>Las tablas finales quedan idénticas; sin filas duplicadas ni versiones nuevas del historial.</td>
</tr>
<tr>
<td align="center">3</td>
<td>Traslape de cortes: cargar una ventana que incluye días ya cargados.</td>
<td>Los días repetidos se reemplazan, no se duplican; el conteo por orden y línea de orden se mantiene.</td>
</tr>
<tr>
<td align="center">4</td>
<td>Manejo de errores: provocar que el CSV no esté presente en SharePoint.</td>
<td>El proceso falla de forma controlada, se registra el error, se avisa por Slack y las tablas finales no se corrompen.</td>
</tr>
<tr>
<td align="center">5</td>
<td>Muestreo: tomar 5 órdenes al azar del detalle.</td>
<td>Cada uno de los 7 indicadores coincide con el cálculo manual sobre el CSV original.</td>
</tr>
<tr>
<td align="center">6</td>
<td>Registros defectuosos: introducir una orden sin fecha o sin cliente.</td>
<td>La orden queda en cuarentena con su motivo y no aparece en el reporte; el proceso continúa.</td>
</tr>
<tr>
<td align="center">7</td>
<td>Duplicado propio: forzar un duplicado después de la deduplicación.</td>
<td>La validación de unicidad detiene la ejecución y deja evidencia.</td>
</tr>
<tr>
<td align="center">8</td>
<td>Cambio de un atributo de cliente entre cortes.</td>
<td>Se crea una nueva versión vigente y se conserva la anterior con su vigencia.</td>
</tr>
<tr>
<td align="center">9</td>
<td>Datos personales: consultar con un usuario sin autorización.</td>
<td>El correo aparece enmascarado; no existe ningún campo de contraseña en ninguna capa de análisis.</td>
</tr>
<tr>
<td align="center">10</td>
<td>Modelo predictivo: evaluación sobre el periodo más reciente.</td>
<td>Supera a la regla de referencia; no usa variables posteriores a la creación de la orden; queda registrado y versionado.</td>
</tr>
<tr>
<td align="center">11</td>
<td>Predicción sin modelo vigente.</td>
<td>El paso falla de forma controlada y los 7 indicadores se publican normalmente.</td>
</tr>
</tbody>
</table>

---

## IV. Propuesta de Solución (para ser llenado por el proveedor)

<img src="https://img.shields.io/badge/PROPUESTA_DE_SOLUCI%C3%93N-1B3139?style=for-the-badge" alt="Propuesta"/>

**Reporte de Performance Logístico y Riesgo de Entrega**

Entregar 1 archivo Excel con los 7 indicadores definidos en la sección anterior, distribuido en 4 pestañas, sobre una plataforma Data Lakehouse en Databricks que además incorpora validación de calidad, gobierno de datos y un modelo predictivo de riesgo de entrega.

---

### Arquitectura propuesta (Data Lakehouse en Databricks)

<table>
<thead>
<tr>
<th width="130">Capa</th>
<th width="200">Ubicación</th>
<th>Responsabilidad</th>
</tr>
</thead>
<tbody>
<tr>
<td><img src="https://img.shields.io/badge/Extracción-0078D4?style=flat-square" alt="ext"/></td>
<td>Volumen de Unity Catalog</td>
<td>Notebook en Python que se conecta a SharePoint Online con Microsoft Graph y descarga el CSV al volumen, con credenciales en Secret Scopes.</td>
</tr>
<tr>
<td><img src="https://img.shields.io/badge/Bronze-CD7F32?style=flat-square" alt="brz"/></td>
<td>Catálogo <code>brz_dataco</code></td>
<td>Carga cruda del CSV con todas las columnas como texto (sin transformar), más metadatos de trazabilidad: archivo, huella (hash), corte y ejecución. Reemplazo de la ventana de fechas para garantizar idempotencia.</td>
</tr>
<tr>
<td><img src="https://img.shields.io/badge/Silver-C0C0C0?style=flat-square" alt="slv"/></td>
<td>Catálogo <code>slv_dataco</code></td>
<td>Tipificación de fechas y montos, deduplicación por llave de negocio conservando el corte más reciente, validación de llaves y cuarentena de registros defectuosos. Separación del CSV de 53 columnas en entidades independientes: clientes, productos, ubicaciones, órdenes y detalle de órdenes.</td>
</tr>
<tr>
<td><img src="https://img.shields.io/badge/Gold-FFD700?style=flat-square" alt="gld"/></td>
<td>Catálogo <code>gld_dataco</code></td>
<td>Modelo dimensional tipo estrella (dimensiones y hechos), con historial SCD tipo 2 en clientes, productos y órdenes; resumen por orden como base única de los indicadores; tablas de indicadores con fotografía por corte.</td>
</tr>
<tr>
<td><img src="https://img.shields.io/badge/Control-1B3139?style=flat-square" alt="ctrl"/></td>
<td>Catálogo <code>metadata_dataco</code></td>
<td>Parámetros del corte, registro de ejecuciones, log por paso, auditoría de deduplicación y cuarentena, resultados de calidad y vistas de salud.</td>
</tr>
<tr>
<td><img src="https://img.shields.io/badge/Calidad-E8412C?style=flat-square" alt="dq"/></td>
<td>Entre Silver y Gold</td>
<td>Motor de reglas declarativas: catálogo de reglas e historial de resultados; ejecutado después de Silver y después de Gold.</td>
</tr>
<tr>
<td><img src="https://img.shields.io/badge/Predicción-6F42C1?style=flat-square" alt="ml"/></td>
<td>Gold + registro de modelos</td>
<td>Tabla de variables por orden, entrenamiento y registro del modelo con MLflow en Unity Catalog, y tabla de predicciones.</td>
</tr>
<tr>
<td><img src="https://img.shields.io/badge/Orquestación-0078D4?style=flat-square" alt="wf"/></td>
<td>Databricks Workflows</td>
<td>Un trabajo serverless con tareas en paralelo, tarea de manejo de error por cada tarea de negocio y alerta a Slack.</td>
</tr>
<tr>
<td><img src="https://img.shields.io/badge/Salida-28A745?style=flat-square" alt="out"/></td>
<td>Notebook de reporte</td>
<td>Genera el Excel de 4 pestañas con formato condicional y variación contra el corte anterior, y lo envía por correo con Microsoft Graph.</td>
</tr>
</tbody>
</table>

---

### Modelo de Datos (a diseñar en detalle)

| Tipo | Entidades |
|------|-----------|
| **Dimensiones** | Cliente (SCD2), producto (SCD2), ubicación, fecha y modo de envío. |
| **Hechos** | Orden (SCD2), detalle de orden y resumen por orden. |
| **Indicadores** | Resumen ejecutivo, detalle por región y alertas (fotografía por corte) y detalle por orden (SCD2). |
| **Convención de nombres** | Prefijos por tipo de tabla: `raw_`, `md_`, `hd_`, `desc_dim_`, `desc_ft_` para identificar su naturaleza y capa. |

---

### Estructura del Excel de Salida

| Pestaña | Granularidad | Contenido |
|---------|:------------:|-----------|
| **RESUMEN EJECUTIVO** | Mercado | 1 fila por mercado (market) y por agrupación (GLOBAL, AMERICAS) con los 7 KPIs y su variación vs. el corte anterior. |
| **DETALLE REGIÓN** | Región + Envío | 1 fila por región + modo de envío, con todos los KPIs. |
| **DETALLE ORDEN** | Orden | Granularidad máxima, para análisis puntual y reclamos. |
| **ALERTAS** | Orden | Órdenes con `late_delivery_risk = 1` y performance de región < 70%, con la probabilidad de retraso estimada por el modelo. |

---

### Frecuencia

> 📅 Semanal, todos los lunes, con corte al domingo anterior. Envío automático al grupo de distribución antes de las **8:00 am**.

---

### Prototipo

El área entregará un prototipo en Excel que muestra el formato visual esperado de las 4 pestañas. El equipo de TI replicará ese formato en el archivo final.

---

### Supuestos y Restricciones

- La plataforma es **Databricks Free Edition** con cómputo serverless y Unity Catalog; el diseño debe operar dentro de sus límites.
- El dataset es histórico (2015-2018); por ello la actualidad se mide contra la ventana definida en la tabla de control y no contra la fecha de hoy.
- El proyecto simula un entorno corporativo con datos públicos; la separación de ambientes se realiza por catálogo.
- Las capacidades de seguimiento de experimentos y registro de modelos disponibles en la plataforma se confirman en la etapa de diseño.

---

<div align="center">

<img src="https://img.shields.io/badge/DataCo-Performance_Log%C3%ADstico-1B3139?style=for-the-badge" alt="footer"/>
<br/>
<sub>Especificación No Técnica — Databricks Data Lakehouse</sub>

</div>
