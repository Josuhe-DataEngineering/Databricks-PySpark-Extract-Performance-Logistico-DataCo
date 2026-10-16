<div align="center">

&nbsp;

<img src="https://img.shields.io/badge/ESPECIFICACI%C3%93N%20NO%20T%C3%89CNICA-0A2540?style=for-the-badge&labelColor=0A2540" alt="Especificación No Técnica" height="32"/>

<br/>
<br/>

# 📦 Reporte de Performance Logístico

### *Riesgo de Entrega por Región · Data Lakehouse en Databricks*

<br/>

<img src="https://img.shields.io/badge/🏢_Supply_Chain-0D9488?style=flat-square&labelColor=0D9488" alt="Supply Chain" height="26"/>
&nbsp;
<img src="https://img.shields.io/badge/⚡_Prioridad_Alta-E11D48?style=flat-square&labelColor=E11D48" alt="Alta" height="26"/>
&nbsp;
<img src="https://img.shields.io/badge/🧠_Incluye_ML-7C3AED?style=flat-square&labelColor=7C3AED" alt="ML" height="26"/>
&nbsp;
<img src="https://img.shields.io/badge/📊_Databricks-FF3621?style=flat-square&logo=databricks&logoColor=white&labelColor=FF3621" alt="Databricks" height="26"/>

<br/>
<br/>

<a href="./Especificacion_No_Tecnica_DataCo_Databricks.docx"><img src="https://img.shields.io/badge/📥_Descargar_Word-0A2540?style=for-the-badge&labelColor=0A2540" alt="Download" height="34"/></a>

&nbsp;

</div>

---

<div align="center">

### 🎯 AT A GLANCE

<table>
<tr>
<td align="center" width="20%"><br/><strong>📊</strong><br/><br/><strong>180K+</strong><br/><sub>registros</sub><br/><br/></td>
<td align="center" width="20%"><br/><strong>🎯</strong><br/><br/><strong>7 KPIs</strong><br/><sub>indicadores</sub><br/><br/></td>
<td align="center" width="20%"><br/><strong>📑</strong><br/><br/><strong>4 Pestañas</strong><br/><sub>Excel final</sub><br/><br/></td>
<td align="center" width="20%"><br/><strong>🗓️</strong><br/><br/><strong>Semanal</strong><br/><sub>Lunes · 8:00 am</sub><br/><br/></td>
<td align="center" width="20%"><br/><strong>🌎</strong><br/><br/><strong>5 Mercados</strong><br/><sub>LATAM · EU · USCA · AP · AF</sub><br/><br/></td>
</tr>
</table>

</div>

---

<details open>
<summary><strong>📑 &nbsp; Tabla de Contenidos</strong></summary>

<br/>

| # | Sección | Descripción |
|:-:|---------|-------------|
| **I** | [📜 Historia de Cambios](#-i--historia-de-los-cambios) | Control de versiones del documento |
| **II** | [📩 Origen de la Solicitud](#-ii--origen-de-la-solicitud) | Datos del solicitante y clasificación |
| **III** | [🔍 Detalle de la Solicitud](#-iii--detalle-de-la-solicitud) | Alcance, indicadores, reglas, calidad, ML |
| **IV** | [🏗️ Propuesta de Solución](#-iv--propuesta-de-solución) | Arquitectura Lakehouse, modelo de datos |

</details>

---

## 📜 I · Historia de los Cambios

<table>
<thead>
<tr>
<th align="center" width="12%">Versión</th>
<th align="center" width="15%">Fecha</th>
<th width="25%">Responsable</th>
<th width="48%">Breve descripción del cambio</th>
</tr>
</thead>
<tbody>
<tr>
<td align="center"><img src="https://img.shields.io/badge/v1-0D9488?style=flat-square&labelColor=0D9488" alt="v1"/></td>
<td align="center"><code>01/10/2026</code></td>
<td>🧑‍💻 Ingeniería de Datos</td>
<td>Versión inicial del requerimiento sobre Databricks Data Lakehouse, incluye el requerimiento de modelo predictivo de riesgo de entrega.</td>
</tr>
<tr>
<td align="center"><img src="https://img.shields.io/badge/v2-94A3B8?style=flat-square&labelColor=94A3B8" alt="v2"/></td>
<td align="center">—</td>
<td>—</td>
<td>—</td>
</tr>
<tr>
<td align="center"><img src="https://img.shields.io/badge/v3-94A3B8?style=flat-square&labelColor=94A3B8" alt="v3"/></td>
<td align="center">—</td>
<td>—</td>
<td>—</td>
</tr>
</tbody>
</table>

---

## 📩 II · Origen de la Solicitud

<table>
<tbody>
<tr>
<td width="22%"><strong>📋 Asunto</strong></td>
<td colspan="3">Reporte de Performance Logístico y Riesgo de Entrega por Región</td>
</tr>
<tr>
<td><strong>📅 Fecha de la Solicitud</strong></td>
<td width="28%"><code>01/10/2026</code></td>
<td width="22%"><strong>🏷️ Tipo de solicitud</strong></td>
<td width="28%">Nuevo reporte y modelo predictivo</td>
</tr>
<tr>
<td><strong>🧑 Nombre del Solicitante</strong></td>
<td>[Nombre del KU]</td>
<td><strong>✍️ Firma</strong></td>
<td>—</td>
</tr>
<tr>
<td><strong>🏢 Área</strong></td>
<td>Operaciones / Logística</td>
<td><strong>📦 Módulo</strong></td>
<td>Supply Chain</td>
</tr>
<tr>
<td><strong>⚡ Prioridad</strong></td>
<td colspan="3">
<img src="https://img.shields.io/badge/Alta-E11D48?style=flat-square" alt="Alta"/> &nbsp; <code>(X)</code>
&nbsp;&nbsp;&nbsp;
<img src="https://img.shields.io/badge/Media-F59E0B?style=flat-square" alt="Media"/> &nbsp; <code>( )</code>
&nbsp;&nbsp;&nbsp;
<img src="https://img.shields.io/badge/Baja-059669?style=flat-square" alt="Baja"/> &nbsp; <code>( )</code>
</td>
</tr>
</tbody>
</table>

---

## 🔍 III · Detalle de la Solicitud

### 📝 Descripción del Cambio Propuesto

> <sub>👤 **Responsable: KU**</sub>
>
> Actualmente el área de Operaciones no cuenta con una vista consolidada que permita medir, con periodicidad semanal, el performance de entrega de la cadena logística ni el nivel de riesgo de entregas tardías que se produce a nivel de orden y región. Esta información se arma manualmente en Excel cruzando exportaciones del ERP, proceso que toma entre **2 y 3 horas por semana** a un analista de BI y que genera diferencias entre áreas que trabajan con cortes distintos.
>
> Se requiere consolidar esta información en una plataforma de datos con arquitectura **Data Lakehouse sobre Databricks**, que alimente un reporte automático semanal para el equipo de Supply Chain y las gerencias regionales (LATAM, Europe, USCA, Pacific Asia, Africa), de modo que puedan decidir con oportunidad sobre la priorización de envíos, la selección de modos de transporte y la gestión de reclamos por entregas tardías.
>
> Adicionalmente, se requiere pasar de **medir** el retraso a **anticiparlo**: un modelo predictivo que estime, para cada orden, la probabilidad de entrega tardía con la información disponible al momento de crearla.

<br/>

### 🎯 Alcance de la Solicitud

<table>
<thead>
<tr>
<th width="25%">Componente</th>
<th width="40%">Descripción</th>
<th width="35%">Resultado esperado</th>
</tr>
</thead>
<tbody>
<tr>
<td align="center">
<img src="https://img.shields.io/badge/01-Reporte-0891B2?style=for-the-badge&labelColor=0A2540" alt="C1" height="40"/>
</td>
<td>Ingesta, limpieza, modelado y cálculo de los 7 indicadores logísticos.</td>
<td>📊 Excel de 4 pestañas enviado por correo cada semana.</td>
</tr>
<tr>
<td align="center">
<img src="https://img.shields.io/badge/02-Calidad_y_Gobierno-0D9488?style=for-the-badge&labelColor=0A2540" alt="C2" height="40"/>
</td>
<td>Validación de datos entre capas, trazabilidad, clasificación y protección de datos personales.</td>
<td>🔒 Cifras confiables, auditables y con acceso controlado por rol.</td>
</tr>
<tr>
<td align="center">
<img src="https://img.shields.io/badge/03-Predicci%C3%B3n_ML-7C3AED?style=for-the-badge&labelColor=0A2540" alt="C3" height="40"/>
</td>
<td>Modelo de clasificación del riesgo de entrega tardía por orden.</td>
<td>🧠 Probabilidad de retraso por orden en el reporte y las alertas.</td>
</tr>
</tbody>
</table>

<br/>

### 📑 Presentación

<table>
<tr>
<td align="center" width="25%"><br/>
<img src="https://img.shields.io/badge/📈-RESUMEN_EJECUTIVO-0A2540?style=for-the-badge" height="34"/>
<br/><br/>
<sub>KPIs totalizados por mercado con variación contra el corte anterior</sub>
<br/><br/>
</td>
<td align="center" width="25%"><br/>
<img src="https://img.shields.io/badge/🌍-DETALLE_REGI%C3%93N-1E40AF?style=for-the-badge" height="34"/>
<br/><br/>
<sub>Grano región + modo de envío con sus 7 indicadores</sub>
<br/><br/>
</td>
<td align="center" width="25%"><br/>
<img src="https://img.shields.io/badge/📦-DETALLE_ORDEN-0891B2?style=for-the-badge" height="34"/>
<br/><br/>
<sub>Máximo grano para decisiones puntuales y reclamos</sub>
<br/><br/>
</td>
<td align="center" width="25%"><br/>
<img src="https://img.shields.io/badge/🚨-ALERTAS-E11D48?style=for-the-badge" height="34"/>
<br/><br/>
<sub>Órdenes con riesgo crítico + probabilidad de retraso ML</sub>
<br/><br/>
</td>
</tr>
</table>

> 🖥️ Adicionalmente, el equipo de Ingeniería de Datos dispone de un **tablero de salud** de la plataforma (estado de cada ejecución, duración, filas procesadas y errores) para uso interno.

<br/>

### ⚠️ Particularidades de la Fuente

- 🔤 El dataset principal viene en formato CSV separado por coma, con codificación **Latin-1**. Se debe cuidar el tratamiento de acentos en nombres de ciudades y países.
- 📅 Las fechas de orden y envío vienen en formato `mm/dd/yyyy HH:MM` y deben convertirse a fecha y hora.
- 🔁 La fuente se entrega por **cortes de fechas**, y los cortes consecutivos pueden traslaparse. Reprocesar una ventana no debe duplicar registros.
- 🚫 Existen registros con `customer_id` nulo o con `order_status = 'SUSPECTED_FRAUD'` que deben tratarse con criterio (ver reglas de negocio).
- 🔑 Pueden existir filas duplicadas. La llave natural de la línea de orden es `order_id + order_item_id`.
- 🔎 El campo `late_delivery_risk` viene precalculado en el CSV. Se debe validar si coincide con el cálculo propio (`days_real > days_scheduled`).
- 🔐 El archivo contiene datos personales de clientes (nombre, correo, dirección) y un campo de contraseña (`customer_password`). **Este último no debe ingresar a las capas de análisis**; los datos personales deben quedar protegidos según su clasificación.

<br/>

### 📊 Desarrollo del Reporte · 7 Indicadores Logísticos

<div align="center">
<img src="https://img.shields.io/badge/🎯_KPIs_LOG%C3%8DSTICOS_A_CALCULAR-0A2540?style=for-the-badge&labelColor=0A2540" alt="KPIs" height="30"/>
</div>

<br/>

El analista actualmente descarga el CSV principal manualmente, lo pega en un libro maestro de Excel y aplica tablas dinámicas con fórmulas para obtener los indicadores. Se solicita automatizar este cálculo de modo que el resultado sea **idéntico** al del trabajo manual.

<table>
<thead>
<tr>
<th align="center" width="8%">N°</th>
<th width="22%">Indicador</th>
<th width="36%">Fórmula</th>
<th width="34%">Consideración / Granularidad</th>
</tr>
</thead>
<tbody>
<tr>
<td align="center"><img src="https://img.shields.io/badge/1-059669?style=flat-square" alt="1"/></td>
<td>⏱️ <strong>On-Time Delivery %</strong></td>
<td><code>Σ (days_real ≤ days_scheduled) / Σ (total órdenes)</code></td>
<td>Por región y por modo de envío. Granularidad más fina: la orden individual.</td>
</tr>
<tr>
<td align="center"><img src="https://img.shields.io/badge/2-E11D48?style=flat-square" alt="2"/></td>
<td>🚨 <strong>Late Delivery Risk %</strong></td>
<td><code>Σ (late_delivery_risk = 1) / Σ (total órdenes)</code></td>
<td>Campo precalculado en el CSV. Comparar contra el cálculo propio como validación cruzada.</td>
</tr>
<tr>
<td align="center"><img src="https://img.shields.io/badge/3-F59E0B?style=flat-square" alt="3"/></td>
<td>📏 <strong>Shipping Variance</strong></td>
<td><code>days_for_shipping_real – days_for_shipment_scheduled</code></td>
<td>Si el resultado es positivo, la entrega se retrasó. Promediar a nivel región.</td>
</tr>
<tr>
<td align="center"><img src="https://img.shields.io/badge/4-7C3AED?style=flat-square" alt="4"/></td>
<td>💰 <strong>Profit Margin %</strong></td>
<td><code>(order_profit_per_order / sales) × 100</code></td>
<td>Hay órdenes con margen negativo (pérdida). No filtrar, solo resaltar.</td>
</tr>
<tr>
<td align="center"><img src="https://img.shields.io/badge/5-0891B2?style=flat-square" alt="5"/></td>
<td>🧑‍💼 <strong>Revenue por Cliente</strong></td>
<td><code>Σ (sales) / COUNT(DISTINCT customer_id)</code></td>
<td>Segmentar por customer_segment. Un cliente puede tener múltiples órdenes.</td>
</tr>
<tr>
<td align="center"><img src="https://img.shields.io/badge/6-0D9488?style=flat-square" alt="6"/></td>
<td>📈 <strong>Beneficio por Orden</strong></td>
<td><code>sales – (product_price × order_item_quantity – order_profit_per_order)</code></td>
<td>Validar con 5 órdenes de muestra que el cálculo cierre.</td>
</tr>
<tr>
<td align="center"><img src="https://img.shields.io/badge/7-1E40AF?style=flat-square" alt="7"/></td>
<td>⏳ <strong>Lead Time Promedio</strong></td>
<td><code>AVG(days_for_shipping_real) agrupado por shipping_mode</code></td>
<td>Solo órdenes con delivery_status distinto de 'Shipping canceled'.</td>
</tr>
</tbody>
</table>

<br/>

### 📏 Reglas de Negocio

<table>
<thead>
<tr>
<th width="30%">🏷️ Regla</th>
<th width="70%">Detalle</th>
</tr>
</thead>
<tbody>
<tr>
<td>🌍 <strong>Agrupaciones</strong></td>
<td><code>GLOBAL</code> = LATAM + Europe + USCA + Pacific Asia + Africa &nbsp; · &nbsp; <code>AMERICAS</code> = LATAM + USCA. Cada indicador se publica por mercado y en ambas agrupaciones.</td>
</tr>
<tr>
<td>🚫 <strong>Alcance por order_status</strong></td>
<td>Excluir las órdenes con <code>order_status = 'CANCELED'</code>. Las órdenes <code>'SUSPECTED_FRAUD'</code> se incluyen y se marcan visualmente.</td>
</tr>
<tr>
<td>📦 <strong>Shipping canceled</strong></td>
<td>Las órdenes con <code>delivery_status = 'Shipping canceled'</code> se muestran en el detalle, pero <strong>no</strong> entran al cálculo de On-Time Delivery % ni de Lead Time.</td>
</tr>
<tr>
<td>📆 <strong>Fecha de corte</strong></td>
<td>Siempre el <strong>domingo anterior</strong> a la ejecución. Los indicadores se calculan acumulados hasta el corte.</td>
</tr>
<tr>
<td>🗂️ <strong>Historial</strong></td>
<td>Cada corte conserva su propia fotografía de indicadores para poder comparar contra el corte anterior y reconstruir cualquier reporte pasado.</td>
</tr>
<tr>
<td>⏰ <strong>Historia de cambios</strong></td>
<td>Si cambia un atributo relevante de un cliente, producto u orden, debe conservarse la versión anterior con su vigencia.</td>
</tr>
<tr>
<td>🚨 <strong>Alerta de riesgo crítico</strong></td>
<td>Orden con <code>late_delivery_risk = 1</code> cuya región tiene On-Time Delivery % menor a <strong>70%</strong>.</td>
</tr>
</tbody>
</table>

<br/>

#### 🎨 Formato condicional esperado en el Excel final

<table>
<thead>
<tr>
<th width="55%">Condición</th>
<th width="45%" align="center">Formato</th>
</tr>
</thead>
<tbody>
<tr><td>On-Time Delivery % <code>&lt; 70%</code></td><td align="center"><img src="https://img.shields.io/badge/🔴_Celda_en_Rojo-DC2626?style=flat-square&labelColor=DC2626" alt="rojo"/></td></tr>
<tr><td>On-Time Delivery % entre <code>70%</code> y <code>89.9%</code></td><td align="center"><img src="https://img.shields.io/badge/🟡_Celda_en_Amarillo-F59E0B?style=flat-square&labelColor=F59E0B" alt="amarillo"/></td></tr>
<tr><td>Late Delivery Risk % <code>&gt; 55%</code></td><td align="center"><img src="https://img.shields.io/badge/🔴_Celda_en_Rojo-DC2626?style=flat-square&labelColor=DC2626" alt="rojo"/></td></tr>
<tr><td>Profit Margin % <code>&lt; 0</code> (pérdida)</td><td align="center"><img src="https://img.shields.io/badge/🩸_Fila_Rojo_Claro-FB7185?style=flat-square&labelColor=FB7185" alt="rosa"/></td></tr>
<tr><td>Shipping Variance <code>&gt; 5 días</code></td><td align="center"><img src="https://img.shields.io/badge/❗_Texto_Rojo-DC2626?style=flat-square&labelColor=DC2626" alt="texto rojo"/></td></tr>
</tbody>
</table>

<br/>

### 🗓️ Frecuencia de Actualización

> 📅 **Semanal** · todos los lunes · con corte al domingo anterior
>
> 📧 Envío al grupo de distribución **`BI_Rpt_PerformanceLogistico_DataCo`** antes de las **8:00 am**

<br/>

### 🛡️ Requerimientos de Calidad de Datos

<div align="center">
<img src="https://img.shields.io/badge/CALIDAD_DE_DATOS-0D9488?style=for-the-badge&labelColor=0D9488" alt="DQ" height="30"/>
</div>

<br/>

Los datos deben validarse entre capas antes de publicarse en el reporte. Principios solicitados:

- ✅ Ningún registro defectuoso se elimina: se **aísla en cuarentena** con su motivo, para su revisión posterior.
- ⚠️ La ejecución **se detiene únicamente por errores propios del proceso** (por ejemplo, un duplicado que sobrevivió a la deduplicación o un hecho sin su dimensión). Un dato defectuoso de la fuente no detiene el reporte.
- 📣 Cuando una regla supera su umbral de tolerancia, se **notifica** al equipo, sin detener la ejecución.
- 📝 Cada validación deja evidencia histórica: regla, ejecución, filas evaluadas, filas que incumplen, porcentaje y decisión.

<br/>

<table>
<thead>
<tr>
<th width="22%">Dimensión</th>
<th width="56%">Regla de negocio</th>
<th width="22%" align="center">Si no se cumple</th>
</tr>
</thead>
<tbody>
<tr>
<td>🔑 <strong>Unicidad</strong></td>
<td>Cada orden, línea de orden, cliente y producto aparece una sola vez.</td>
<td align="center"><img src="https://img.shields.io/badge/⛔_Detener-DC2626?style=flat-square&labelColor=DC2626" alt="detener"/></td>
</tr>
<tr>
<td>📋 <strong>Completitud</strong></td>
<td>Toda orden tiene fecha de orden y cliente informado; toda orden tiene fecha de envío.</td>
<td align="center"><img src="https://img.shields.io/badge/⚠️_Cuarentena-F59E0B?style=flat-square&labelColor=F59E0B" alt="cuarentena"/></td>
</tr>
<tr>
<td>✔️ <strong>Validez</strong></td>
<td><code>late_delivery_risk</code> solo toma valor 0 o 1; la cantidad de cada línea &gt; 0; <code>order_status</code> pertenece a valores conocidos.</td>
<td align="center"><img src="https://img.shields.io/badge/⚠️_Cuarentena-F59E0B?style=flat-square&labelColor=F59E0B" alt="cuarentena"/></td>
</tr>
<tr>
<td>🔗 <strong>Integridad referencial</strong></td>
<td>Toda línea apunta a una orden y a un producto existentes; toda orden apunta a un cliente existente (tolerancia mínima <strong>99.5%</strong>); todo hecho apunta a sus dimensiones.</td>
<td align="center"><img src="https://img.shields.io/badge/⚠️_Cuar._/_⛔-E11D48?style=flat-square&labelColor=E11D48" alt="mixto"/></td>
</tr>
<tr>
<td>🧮 <strong>Consistencia</strong></td>
<td>Órdenes vigentes del reporte iguales a órdenes válidas no canceladas de capa limpia; un solo resumen por orden; fecha envío no anterior a fecha orden.</td>
<td align="center"><img src="https://img.shields.io/badge/⛔_/_⚠️-DC2626?style=flat-square&labelColor=DC2626" alt="mixto"/></td>
</tr>
<tr>
<td>⏱️ <strong>Actualidad</strong></td>
<td>El último corte cargado corresponde al corte esperado según la tabla de control.</td>
<td align="center"><img src="https://img.shields.io/badge/⚠️_Advertencia-F59E0B?style=flat-square&labelColor=F59E0B" alt="warn"/></td>
</tr>
</tbody>
</table>

<br/>

### 🏛️ Requerimientos de Gobierno y Seguridad

<div align="center">
<img src="https://img.shields.io/badge/GOBIERNO_Y_SEGURIDAD-1E40AF?style=for-the-badge&labelColor=1E40AF" alt="GOV" height="30"/>
</div>

<br/>

<table>
<tbody>
<tr>
<td width="4%" align="center">🏷️</td>
<td><strong>Clasificación</strong> de cada atributo en cuatro niveles (<em>Público · Interno · Confidencial · Restringido</em>), alineada con la <strong>Ley N.° 29733</strong> de Protección de Datos Personales del Perú.</td>
</tr>
<tr>
<td align="center">🎭</td>
<td><strong>Protección de datos personales:</strong> el correo del cliente se enmascara para usuarios sin autorización y el acceso a filas se restringe según el grupo del usuario.</td>
</tr>
<tr>
<td align="center">🔐</td>
<td><strong>Acceso por rol:</strong> capa cruda solo para Ingeniería de Datos · capa limpia para analistas avanzados · capa de consumo para usuarios del reporte.</td>
</tr>
<tr>
<td align="center">🗝️</td>
<td><strong>Credenciales</strong> (SharePoint, correo, alertas) fuera del código, en un <em>almacén de secretos</em>.</td>
</tr>
<tr>
<td align="center">📚</td>
<td><strong>Propiedad y documentación:</strong> cada tabla tiene un responsable (owner), un steward, su grano y su descripción de negocio. El linaje de datos debe ser consultable de la fuente al reporte.</td>
</tr>
</tbody>
</table>

<br/>

### 🧠 Requerimiento de Modelo Predictivo (Machine Learning)

<div align="center">
<img src="https://img.shields.io/badge/MACHINE_LEARNING-7C3AED?style=for-the-badge&logo=mlflow&logoColor=white&labelColor=7C3AED" alt="ML" height="30"/>
</div>

<br/>

El área requiere anticipar cuáles órdenes tienen mayor probabilidad de llegar tarde, para actuar antes del retraso (cambiar el modo de envío, priorizar el despacho o avisar al cliente).

<br/>

<table>
<thead>
<tr>
<th width="25%">Aspecto</th>
<th width="75%">Detalle</th>
</tr>
</thead>
<tbody>
<tr>
<td>🎯 <strong>Problema</strong></td>
<td>Clasificación binaria: ¿la orden llegará tarde? (variable objetivo: <code>late_delivery_risk</code>, 0 o 1).</td>
</tr>
<tr>
<td>📍 <strong>Unidad de predicción</strong></td>
<td>Una orden.</td>
</tr>
<tr>
<td>✅ <strong>Información permitida</strong></td>
<td>Solo atributos conocidos <strong>al crear la orden</strong>: modo de envío, días programados, mercado, región, país, cantidad de líneas y unidades, monto, descuento, categoría y departamento del producto, segmento del cliente, mes y día de la semana.</td>
</tr>
<tr>
<td>⛔ <strong>Información prohibida</strong></td>
<td>Días reales de envío y estado de entrega: son resultados que se conocen después y producirían una predicción engañosa (<em>fuga de datos</em>).</td>
</tr>
<tr>
<td>🧪 <strong>Validación</strong></td>
<td>Partición <strong>temporal</strong>: se entrena con las órdenes más antiguas y se valida con las más recientes, nunca de forma aleatoria.</td>
</tr>
<tr>
<td>📏 <strong>Comparación</strong></td>
<td>El modelo debe superar a una regla simple de referencia (por ejemplo, el promedio de retraso por modo de envío).</td>
</tr>
<tr>
<td>📊 <strong>Métricas</strong></td>
<td>AUC-ROC y AUC-PR, junto con precisión y recuperación al umbral elegido, e informe del desbalance de clases.</td>
</tr>
<tr>
<td>🔍 <strong>Trazabilidad</strong></td>
<td>Cada experimento registra parámetros, métricas, variables y versión de los datos. El modelo se versiona y queda gobernado en el catálogo de datos.</td>
</tr>
<tr>
<td>📦 <strong>Resultado</strong></td>
<td>Tabla de predicciones con la probabilidad por orden, el modelo y la versión que la generó, incorporada a la pestaña <strong>ALERTAS</strong>.</td>
</tr>
<tr>
<td>⚙️ <strong>Operación</strong></td>
<td>La predicción se ejecuta como un paso más del proceso semanal. Si no hay un modelo vigente, el paso falla de forma controlada sin afectar los 7 indicadores.</td>
</tr>
</tbody>
</table>

<br/>

### ⚙️ Requerimientos No Funcionales

<table>
<thead>
<tr>
<th width="22%">Requerimiento</th>
<th width="78%">Descripción</th>
</tr>
</thead>
<tbody>
<tr><td>🔁 <strong>Idempotencia</strong></td><td>Ejecutar el mismo corte más de una vez deja el resultado idéntico, sin duplicados ni versiones espurias del historial.</td></tr>
<tr><td>🔍 <strong>Trazabilidad</strong></td><td>De cada cifra se debe poder llegar al archivo, corte y ejecución de origen.</td></tr>
<tr><td>👁️ <strong>Observabilidad</strong></td><td>Cada paso registra inicio, fin, filas procesadas y estado. Ante cualquier fallo se alerta al equipo.</td></tr>
<tr><td>🧪 <strong>Reproducibilidad</strong></td><td>La misma entrada produce el mismo resultado (reglas deterministas y llaves estables).</td></tr>
<tr><td>🛡️ <strong>Seguridad</strong></td><td>Sin secretos en el código ni contraseñas de clientes en el análisis; acceso por rol.</td></tr>
<tr><td>🗃️ <strong>Retención</strong></td><td>Historial de cambios de las tablas durante <strong>365 días</strong>, para auditoría y reconstrucción de cortes anteriores.</td></tr>
<tr><td>🔧 <strong>Mantenibilidad</strong></td><td>Lógica común reutilizable, convención de nombres uniforme y documentación de decisiones de arquitectura.</td></tr>
<tr><td>🚀 <strong>Despliegue repetible</strong></td><td>La definición del proceso y su despliegue entre ambientes (desarrollo y producción) es versionada como código.</td></tr>
</tbody>
</table>

<br/>

### 🛠️ Consideraciones Técnicas Sugeridas · Stack

<div align="center">

<img src="https://img.shields.io/badge/Databricks-FF3621?style=for-the-badge&logo=databricks&logoColor=white" alt="Databricks"/>
&nbsp;
<img src="https://img.shields.io/badge/Delta_Lake-00ADD4?style=for-the-badge&logo=delta&logoColor=white" alt="Delta"/>
&nbsp;
<img src="https://img.shields.io/badge/Unity_Catalog-0A2540?style=for-the-badge" alt="UC"/>
&nbsp;
<img src="https://img.shields.io/badge/PySpark-E25A1C?style=for-the-badge&logo=apachespark&logoColor=white" alt="PySpark"/>
<br/><br/>
<img src="https://img.shields.io/badge/Microsoft_Graph-0078D4?style=for-the-badge&logo=microsoft&logoColor=white" alt="Graph"/>
&nbsp;
<img src="https://img.shields.io/badge/MLflow-0194E2?style=for-the-badge&logo=mlflow&logoColor=white" alt="MLflow"/>
&nbsp;
<img src="https://img.shields.io/badge/Slack-4A154B?style=for-the-badge&logo=slack&logoColor=white" alt="Slack"/>
&nbsp;
<img src="https://img.shields.io/badge/GitHub_Actions-2088FF?style=for-the-badge&logo=githubactions&logoColor=white" alt="GHA"/>

</div>

<br/>

<table>
<thead>
<tr>
<th width="30%">Capacidad</th>
<th width="70%">Tecnología</th>
</tr>
</thead>
<tbody>
<tr><td>🏗️ <strong>Arquitectura</strong></td><td><strong>Data Lakehouse en Databricks</strong> con patrón medallón de 3 capas: Bronze → Silver → Gold.</td></tr>
<tr><td>🏛️ <strong>Gobierno</strong></td><td><strong>Unity Catalog</strong>: un catálogo por capa más un catálogo de metadatos de control.</td></tr>
<tr><td>💾 <strong>Almacenamiento</strong></td><td><strong>Delta Lake</strong> (transacciones, historial y time-travel).</td></tr>
<tr><td>📥 <strong>Extracción</strong></td><td><strong>Microsoft Graph</strong> para SharePoint Online, credenciales en <strong>Secret Scopes</strong>.</td></tr>
<tr><td>🎼 <strong>Orquestación</strong></td><td><strong>Databricks Workflows</strong> sobre cómputo <strong>serverless</strong> con tareas en paralelo.</td></tr>
<tr><td>⚡ <strong>Transformaciones</strong></td><td><strong>PySpark y Spark SQL</strong>; dimensiones SCD tipo 2 donde se requiera historial.</td></tr>
<tr><td>🔁 <strong>Idempotencia</strong></td><td>Reemplazo de la ventana de fechas (<code>replaceWhere</code>) en lugar de agregar filas.</td></tr>
<tr><td>📊 <strong>Auditoría</strong></td><td>Tablas de control + tablero <strong>AI/BI</strong> de salud del proceso.</td></tr>
<tr><td>🔔 <strong>Alertas</strong></td><td><strong>Slack</strong> y correo ante cualquier fallo; envío del reporte con Microsoft Graph.</td></tr>
<tr><td>🧠 <strong>Machine Learning</strong></td><td><strong>MLflow</strong> (experimentos) y registro de modelos en <strong>Unity Catalog</strong>.</td></tr>
<tr><td>🚀 <strong>CI/CD</strong></td><td><strong>Databricks Asset Bundles</strong> y <strong>GitHub Actions</strong>; código versionado en GitHub.</td></tr>
</tbody>
</table>

<br/>

### 💡 Justificación

> <sub>👤 **Responsable: KU**</sub>

- ⏱️ **Reducir** las 2-3 horas semanales que el analista invierte armando el reporte a mano, liberando tiempo para análisis de valor.
- 🎯 **Eliminar** las diferencias de cifras entre áreas que hoy trabajan con cortes distintos del mismo dato.
- 🔍 **Detectar** órdenes con riesgo de entrega tardía el mismo día en que ocurren, y no 2-3 días después como ocurre hoy.
- 🧠 **Anticipar** el retraso con un modelo predictivo, para pasar de una gestión reactiva a una preventiva.
- 🏛️ **Contar** con datos gobernados y trazables, con protección de los datos personales de clientes.

<br/>

### ⚠️ Impacto si el cambio no se implementa

> <sub>👤 **Responsable: KU**</sub>

- 🐢 El tiempo de reacción ante alertas de entrega sigue siendo de **48-72 horas**.
- 💸 El cálculo de la venta afectada por entregas tardías continúa haciéndose a destiempo, impactando las decisiones de la semana siguiente.
- 📝 Se mantiene el riesgo de errores por copy/paste manual.
- 🔓 Los datos personales de clientes continúan circulando en archivos sin control de acceso.

<br/>

### 🔀 Alternativas de Solución

> <sub>👤 **Responsable: KU**</sub>

<table>
<thead>
<tr>
<th width="15%" align="center">Plan</th>
<th width="40%">Descripción</th>
<th width="45%">⚠️ Limitación</th>
</tr>
</thead>
<tbody>
<tr>
<td align="center"><img src="https://img.shields.io/badge/Plan_B1-F59E0B?style=for-the-badge&labelColor=F59E0B" alt="B1"/></td>
<td>Construir el reporte conectando <strong>Power BI</strong> directamente al CSV.</td>
<td>No pasa por el Lakehouse, no cumple con la política de consolidar datos en la plataforma corporativa, y no ofrece historial ni trazabilidad.</td>
</tr>
<tr>
<td align="center"><img src="https://img.shields.io/badge/Plan_B2-F59E0B?style=for-the-badge&labelColor=F59E0B" alt="B2"/></td>
<td>Mantener el proceso manual con <strong>macros de Excel</strong> mejoradas.</td>
<td>No resuelve las diferencias de corte entre áreas.</td>
</tr>
<tr>
<td align="center"><img src="https://img.shields.io/badge/Plan_B3-F59E0B?style=for-the-badge&labelColor=F59E0B" alt="B3"/></td>
<td>Una <strong>base de datos relacional</strong> con paquetes de integración en servidor propio.</td>
<td>Requiere infraestructura y mantenimiento, y no cubre de forma nativa el modelo predictivo ni el gobierno de datos.</td>
</tr>
</tbody>
</table>

<br/>

### ✅ Casos de Prueba

> <sub>👤 **Responsable: KU** — Propuesta de periodo de prueba</sub>

<table>
<thead>
<tr>
<th align="center" width="6%">N°</th>
<th width="38%">Caso de prueba</th>
<th width="56%">Criterio de aceptación</th>
</tr>
</thead>
<tbody>
<tr><td align="center"><strong>01</strong></td><td>Ejecución en paralelo con el proceso manual durante 2 semanas.</td><td>Los 7 indicadores coinciden con el Excel manual; se acepta diferencia ≤ 0.5% por redondeos.</td></tr>
<tr><td align="center"><strong>02</strong></td><td>Reprocesamiento: correr dos veces el mismo corte.</td><td>Las tablas finales quedan idénticas; sin filas duplicadas ni versiones nuevas del historial.</td></tr>
<tr><td align="center"><strong>03</strong></td><td>Traslape de cortes: cargar una ventana con días ya cargados.</td><td>Los días repetidos se reemplazan, no se duplican; el conteo por orden y línea se mantiene.</td></tr>
<tr><td align="center"><strong>04</strong></td><td>Manejo de errores: provocar que el CSV no esté en SharePoint.</td><td>El proceso falla de forma controlada, se registra el error y se avisa por Slack.</td></tr>
<tr><td align="center"><strong>05</strong></td><td>Muestreo: tomar 5 órdenes al azar del detalle.</td><td>Cada uno de los 7 indicadores coincide con el cálculo manual sobre el CSV original.</td></tr>
<tr><td align="center"><strong>06</strong></td><td>Registros defectuosos: introducir una orden sin fecha o sin cliente.</td><td>La orden queda en cuarentena con su motivo y no aparece en el reporte; el proceso continúa.</td></tr>
<tr><td align="center"><strong>07</strong></td><td>Duplicado propio: forzar duplicado después de la deduplicación.</td><td>La validación de unicidad detiene la ejecución y deja evidencia.</td></tr>
<tr><td align="center"><strong>08</strong></td><td>Cambio de un atributo de cliente entre cortes.</td><td>Se crea una nueva versión vigente y se conserva la anterior con su vigencia.</td></tr>
<tr><td align="center"><strong>09</strong></td><td>Datos personales: consulta con usuario sin autorización.</td><td>El correo aparece enmascarado; no existe campo de contraseña en capas de análisis.</td></tr>
<tr><td align="center"><strong>10</strong></td><td>Modelo predictivo: evaluación sobre el periodo más reciente.</td><td>Supera a la regla de referencia; no usa variables posteriores a la creación de la orden; versionado.</td></tr>
<tr><td align="center"><strong>11</strong></td><td>Predicción sin modelo vigente.</td><td>El paso falla de forma controlada y los 7 indicadores se publican normalmente.</td></tr>
</tbody>
</table>

---

## 🏗️ IV · Propuesta de Solución

<div align="center">
<em>(para ser llenado por el proveedor)</em>
<br/><br/>
<img src="https://img.shields.io/badge/ARQUITECTURA_DATA_LAKEHOUSE-0A2540?style=for-the-badge&labelColor=0A2540" alt="Arq" height="30"/>
</div>

<br/>

**Reporte de Performance Logístico y Riesgo de Entrega**

Entregar **1 archivo Excel** con los 7 indicadores definidos en la sección anterior, distribuido en 4 pestañas, sobre una plataforma Data Lakehouse en Databricks que además incorpora validación de calidad, gobierno de datos y un modelo predictivo de riesgo de entrega.

<br/>

### 🧱 Arquitectura Propuesta · Capas del Lakehouse

<table>
<thead>
<tr>
<th width="18%" align="center">Capa</th>
<th width="22%">Ubicación</th>
<th width="60%">Responsabilidad</th>
</tr>
</thead>
<tbody>
<tr>
<td align="center"><img src="https://img.shields.io/badge/🔌-EXTRACCI%C3%93N-0891B2?style=for-the-badge&labelColor=0A2540" alt="EXT" height="34"/></td>
<td><code>Volumen UC</code></td>
<td>Notebook en Python que se conecta a SharePoint Online con <strong>Microsoft Graph</strong> y descarga el CSV al volumen, con credenciales en Secret Scopes.</td>
</tr>
<tr>
<td align="center"><img src="https://img.shields.io/badge/🥉-BRONZE-CD7F32?style=for-the-badge&labelColor=0A2540" alt="BRZ" height="34"/></td>
<td><code>brz_dataco</code></td>
<td>Carga cruda del CSV con todas las columnas como texto, más metadatos de trazabilidad: archivo, hash, corte y ejecución. Reemplazo de la ventana de fechas para garantizar idempotencia.</td>
</tr>
<tr>
<td align="center"><img src="https://img.shields.io/badge/🥈-SILVER-94A3B8?style=for-the-badge&labelColor=0A2540" alt="SLV" height="34"/></td>
<td><code>slv_dataco</code></td>
<td>Tipificación de fechas y montos, deduplicación por llave de negocio, validación de llaves y cuarentena. Separación del CSV de 53 columnas en entidades independientes: clientes, productos, ubicaciones, órdenes y detalle.</td>
</tr>
<tr>
<td align="center"><img src="https://img.shields.io/badge/🥇-GOLD-D4AF37?style=for-the-badge&labelColor=0A2540" alt="GLD" height="34"/></td>
<td><code>gld_dataco</code></td>
<td>Modelo dimensional tipo estrella con historial <strong>SCD tipo 2</strong> en clientes, productos y órdenes; resumen por orden como base única de los indicadores; tablas de indicadores con fotografía por corte.</td>
</tr>
<tr>
<td align="center"><img src="https://img.shields.io/badge/⚙️-CONTROL-475569?style=for-the-badge&labelColor=0A2540" alt="CTL" height="34"/></td>
<td><code>metadata_dataco</code></td>
<td>Parámetros del corte, registro de ejecuciones, log por paso, auditoría de deduplicación y cuarentena, resultados de calidad y vistas de salud.</td>
</tr>
<tr>
<td align="center"><img src="https://img.shields.io/badge/🛡️-CALIDAD-0D9488?style=for-the-badge&labelColor=0A2540" alt="DQ" height="34"/></td>
<td><code>Entre Silver y Gold</code></td>
<td>Motor de reglas declarativas: catálogo de reglas e historial de resultados; ejecutado después de Silver y después de Gold.</td>
</tr>
<tr>
<td align="center"><img src="https://img.shields.io/badge/🧠-PREDICCI%C3%93N-7C3AED?style=for-the-badge&labelColor=0A2540" alt="ML" height="34"/></td>
<td><code>Gold + MLflow</code></td>
<td>Tabla de variables por orden, entrenamiento y registro del modelo con MLflow en Unity Catalog, y tabla de predicciones.</td>
</tr>
<tr>
<td align="center"><img src="https://img.shields.io/badge/🎼-ORQUESTACI%C3%93N-1E40AF?style=for-the-badge&labelColor=0A2540" alt="ORQ" height="34"/></td>
<td><code>Workflows</code></td>
<td>Un trabajo serverless con tareas en paralelo, tarea de manejo de error por cada tarea de negocio y alerta a Slack.</td>
</tr>
<tr>
<td align="center"><img src="https://img.shields.io/badge/📤-SALIDA-059669?style=for-the-badge&labelColor=0A2540" alt="OUT" height="34"/></td>
<td><code>Notebook reporte</code></td>
<td>Genera el Excel de 4 pestañas con formato condicional y variación contra el corte anterior, y lo envía por correo con Microsoft Graph.</td>
</tr>
</tbody>
</table>

<br/>

### 🧩 Modelo de Datos (a diseñar en detalle)

<table>
<thead>
<tr>
<th width="30%">Tipo</th>
<th width="70%">Entidades</th>
</tr>
</thead>
<tbody>
<tr><td>📐 <strong>Dimensiones</strong></td><td>Cliente (SCD2), producto (SCD2), ubicación, fecha y modo de envío.</td></tr>
<tr><td>📊 <strong>Hechos</strong></td><td>Orden (SCD2), detalle de orden y resumen por orden.</td></tr>
<tr><td>🎯 <strong>Indicadores</strong></td><td>Resumen ejecutivo, detalle por región y alertas (fotografía por corte) y detalle por orden (SCD2).</td></tr>
<tr><td>🏷️ <strong>Convención de nombres</strong></td><td>Prefijos por tipo de tabla: <code>raw_</code>, <code>md_</code>, <code>hd_</code>, <code>desc_dim_</code>, <code>desc_ft_</code>.</td></tr>
</tbody>
</table>

<br/>

### 📑 Estructura del Excel de Salida

<table>
<thead>
<tr>
<th width="25%">Pestaña</th>
<th width="20%" align="center">Granularidad</th>
<th width="55%">Contenido</th>
</tr>
</thead>
<tbody>
<tr><td><img src="https://img.shields.io/badge/📈-RESUMEN_EJECUTIVO-0A2540?style=flat-square" alt="RE"/></td><td align="center">Mercado</td><td>1 fila por mercado (market) y por agrupación (GLOBAL, AMERICAS) con los 7 KPIs y su variación vs. el corte anterior.</td></tr>
<tr><td><img src="https://img.shields.io/badge/🌍-DETALLE_REGI%C3%93N-1E40AF?style=flat-square" alt="DR"/></td><td align="center">Región + Envío</td><td>1 fila por región + modo de envío, con todos los KPIs.</td></tr>
<tr><td><img src="https://img.shields.io/badge/📦-DETALLE_ORDEN-0891B2?style=flat-square" alt="DO"/></td><td align="center">Orden</td><td>Granularidad máxima, para análisis puntual y reclamos.</td></tr>
<tr><td><img src="https://img.shields.io/badge/🚨-ALERTAS-E11D48?style=flat-square" alt="AL"/></td><td align="center">Orden</td><td>Órdenes con <code>late_delivery_risk = 1</code> y performance de región &lt; 70%, con la probabilidad de retraso estimada por el modelo.</td></tr>
</tbody>
</table>

<br/>

### 🗓️ Frecuencia

> 📅 Semanal · todos los lunes · con corte al domingo anterior
>
> 📧 Envío automático al grupo de distribución antes de las **8:00 am**

<br/>

### 🎨 Prototipo

El área entregará un prototipo en Excel que muestra el formato visual esperado de las 4 pestañas. El equipo de TI replicará ese formato en el archivo final.

<br/>

### 📌 Supuestos y Restricciones

- 🆓 La plataforma es **Databricks Free Edition** con cómputo serverless y Unity Catalog; el diseño debe operar dentro de sus límites.
- 📆 El dataset es histórico (**2015-2018**); por ello la actualidad se mide contra la ventana definida en la tabla de control y no contra la fecha de hoy.
- 🧪 El proyecto simula un entorno corporativo con datos públicos; la separación de ambientes se realiza por catálogo.
- 🔎 Las capacidades de seguimiento de experimentos y registro de modelos disponibles en la plataforma se confirman en la etapa de diseño.

---

<div align="center">

&nbsp;

<img src="https://img.shields.io/badge/🚀_DataCo_·_Performance_Log%C3%ADstico-0A2540?style=for-the-badge&labelColor=0A2540" alt="footer" height="32"/>

<sub>Especificación No Técnica · Databricks Data Lakehouse · Versión 1.0 · Octubre 2026</sub>

&nbsp;

</div>
