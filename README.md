<div align="center">

# 🏗️ DataCo Supply Chain — Data Lakehouse

### Plataforma de datos **ELT de punta a punta** sobre Databricks Lakehouse
#### De un reporte logístico armado a mano en Excel a un Lakehouse cloud gobernado, con calidad declarativa probada, observabilidad, infraestructura como código y Machine Learning

<br>

![Databricks](https://img.shields.io/badge/Databricks-FF3621?style=for-the-badge&logo=databricks&logoColor=white)
![Delta Lake](https://img.shields.io/badge/Delta_Lake-00ADD4?style=for-the-badge&logo=delta&logoColor=white)
![PySpark](https://img.shields.io/badge/PySpark-E25A1C?style=for-the-badge&logo=apachespark&logoColor=white)
![Unity Catalog](https://img.shields.io/badge/Unity_Catalog-FF3621?style=for-the-badge&logo=databricks&logoColor=white)
![GitHub Actions](https://img.shields.io/badge/CI%2FCD-GitHub_Actions-2088FF?style=for-the-badge&logo=githubactions&logoColor=white)
![Microsoft Graph](https://img.shields.io/badge/Microsoft_Graph-0078D4?style=for-the-badge&logo=microsoft&logoColor=white)

<br>

![Calidad](https://img.shields.io/badge/Reglas_de_calidad-24-3E6D9C?style=flat-square&labelColor=24384C)
![Pruebas](https://img.shields.io/badge/Pruebas_pytest-13-3E6D9C?style=flat-square&labelColor=24384C)
![Columnas](https://img.shields.io/badge/Columnas_documentadas-536-3E6D9C?style=flat-square&labelColor=24384C)
![Duplicados](https://img.shields.io/badge/Duplicados_·_cuarentena-0-3E6D9C?style=flat-square&labelColor=24384C)
![ADRs](https://img.shields.io/badge/Decisiones_de_arquitectura-14-3E6D9C?style=flat-square&labelColor=24384C)

</div>

<br>

> **Qué es:** tomé un reporte logístico que se armaba a mano cada semana cruzando exports en Excel (2–3 h de un analista, con cifras distintas entre áreas) y lo convertí en una **plataforma de datos gobernada de punta a punta** sobre Databricks Lakehouse: ingesta desde SharePoint, procesamiento en capas con **24 reglas de calidad probadas con datos defectuosos**, modelo dimensional con historial, gobierno con Unity Catalog, un Excel ejecutivo que se envía solo, trazabilidad y alertas — todo descrito como código y con CI/CD.
>
> 🚧 marca lo diseñado pero aún no implementado. Lo demás **ya corre de punta a punta**.

<br>

## El salto

<table>
<tr>
<th width="50%">❌ Antes — proceso manual</th>
<th width="50%">✅ Ahora — plataforma gobernada</th>
</tr>
<tr>
<td valign="top">
<ul>
<li>2–3 horas de un analista cada semana</li>
<li>Exports de Excel cruzados a mano</li>
<li>Cifras distintas entre áreas según el corte</li>
<li>Sin historial, sin trazabilidad</li>
<li>Reglas de negocio en la cabeza de alguien</li>
</ul>
</td>
<td valign="top">
<ul>
<li><b>Una corrida reproducible</b> de ~19 min</li>
<li>Reglas de negocio <b>centralizadas y versionadas</b></li>
<li>Calidad <b>validada antes de publicar</b> (24 reglas)</li>
<li><b>Historial de cambios</b> (SCD2) y linaje en el catálogo</li>
<li><b>Entrega automática</b> del Excel al área por correo</li>
</ul>
</td>
</tr>
</table>

<br>

## 🧭 Estado del proyecto

| Fase | Alcance | Estado |
|---|---|:---:|
| **1 · Pipeline de datos** | Bronze → Silver → Gold, modelo estrella con SCD2, Excel ejecutivo por correo | ✅ |
| **2 · Calidad de datos** | 24 reglas declarativas, cuarentena, pruebas con datos defectuosos | ✅ |
| **3 · Ingeniería, CI y CD** | Módulo compartido, 13 pruebas `pytest` en GitHub Actions, Asset Bundles, deploy a `dev` | ✅ |
| **4 · Gobierno** | Comentarios, tags, máscara PII, GRANT por rol, diccionario de datos | ✅ |
| **5 · Reprocesabilidad** | SCD2 con fecha de negocio, backfill, reinicio | 🚧 |
| **6 · Nube y escala** | Azure Databricks, ADLS Gen2, Auto Loader, prueba de escala | 🚧 |
| **7 · Nivel plataforma** | Contratos de datos, SLOs, runbooks, incidentes simulados | 🚧 |
| **8 · Machine Learning** | Modelo de riesgo de retraso con MLflow en Unity Catalog | 🚧 |

<br>

## 🏛️ Arquitectura

```
SharePoint ──▶ 🥉 Bronze ──▶ 🥈 Silver ──▶ ✅ Calidad ──▶ 🥇 Gold ──▶ ✅ Calidad ──▶ 📊 Excel + 📧 Correo
             (crudo,         (tipado,       (21 reglas    (modelo      (3 reglas
              STRING +        dedupe,        + cuarentena)  estrella +   de consistencia)
              metadatos)      cuarentena)                   KPIs)
                     └──── 📋 etl_log + 🚨 alertas Slack + 📈 dashboard de salud en cada task ────┘
```

Pipeline orquestado como **un único Databricks Workflow en abanico** (46 tasks), descrito como código con **Asset Bundles**. Entre capas, dos **compuertas de calidad** detienen el flujo si una regla crítica falla; cada task tiene su `log_error` que registra la excepción y avisa a Slack. Una alerta salta si la ejecución supera los 35 min.

<p align="center">
  <img src="docs/workflow.png" alt="Workflow DataCo de punta a punta" width="100%">
</p>

> ⏱️ **Medido** sobre el mismo código en Free Edition: la cadena lineal tardó **16 min 34 s** y el abanico **19 min**. El abanico no gana tiempo porque el cómputo serverless es compartido; se versiona así porque deja el grafo listo para un entorno con más capacidad ([ADR-001](docs/adr/001-abanico-vs-cadena.md)).

<br>

## 🧱 Los tres pilares de ingeniería

<table>
<tr>
<td width="33%" valign="top">
<h4>🔄 Pipeline confiable</h4>
Idempotencia por corte, hash SHA-256 del archivo, <b>conversión segura</b> (nunca un cero por un nulo) y deduplicación determinista por llave de negocio.
</td>
<td width="33%" valign="top">
<h4>🛡️ Calidad probada</h4>
<b>24 reglas</b> en 6 dimensiones. El dato malo va a <b>cuarentena</b> sin frenar el pipeline; los 3 comportamientos se prueban con el <b>Workflow real</b> y datos defectuosos.
</td>
<td width="33%" valign="top">
<h4>⚙️ Como código</h4>
Job en <b>YAML</b> (Asset Bundles), <b>13 pruebas</b> en GitHub Actions, <b>CD a <code>dev</code></b> al fusionar a <code>main</code> y <b>14 ADRs</b> que documentan cada decisión.
</td>
</tr>
</table>

<br>

## 📚 Documentación

Esta portada da la visión general. El detalle vive en `docs/`, un archivo por tema:

| 📄 Documento | Qué encontrarás |
|---|---|
| **[🧱 Capas del Lakehouse](docs/capas.md)** | Qué hace Bronze, Silver y Gold: grano, cuarentena, SCD2, KPIs y entrega |
| **[🛡️ Calidad de datos](docs/calidad-de-datos.md)** | Las 24 reglas, el motor declarativo y las pruebas con datos defectuosos |
| **[🔐 Gobierno](docs/gobierno.md)** | Comentarios, tags, máscara PII, permisos por rol y diccionario de datos |
| **[⚙️ CI y CD](docs/ci-cd.md)** | Módulo compartido, pruebas, Asset Bundles y despliegue a `dev` |
| **[🗺️ Hoja de ruta](docs/hoja-de-ruta.md)** | Etapas A–F con su criterio de terminado |
| **[📐 Decisiones (ADRs)](docs/adr/)** | 14 decisiones de arquitectura con contexto y consecuencias |

<br>

<details>
<summary><b>🗂️ Modelo dimensional &amp; los 7 indicadores</b></summary>

<br>

```
        dim_customers        dim_products
              │                    │
              ▼                    ▼
  dim_fecha ─▶ fact_orders ◀─ fact_order_details ◀─ dim_products
              ▲       ▲
        dim_locations  dim_shipping_mode
```

5 dimensiones (clientes y productos con **SCD2**) · 2 tablas de hechos · 1 resumen por pedido como base única de los KPIs. Las tablas de Gold declaran llaves primarias y foráneas informativas; no llevan `CHECK` porque Databricks no lo permite junto a una máscara de columna ([ADR-014](docs/adr/014-gobierno-en-gold.md)).

**Los 7 indicadores:** On-Time Delivery % · Late Delivery Risk % · Shipping Variance · Profit Margin % · Revenue por Cliente · Beneficio por Orden · Lead Time Promedio — con agrupaciones **GLOBAL** y **AMERICAS**, excluyendo cancelados y marcando los sospechosos de fraude.

</details>

<details>
<summary><b>🛠️ Stack completo</b></summary>

<br>

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
| Pruebas | pytest |
| IaC, CI y CD | Databricks Asset Bundles · Databricks CLI · GitHub Actions |
| Nube 🚧 | Azure Databricks · ADLS Gen2 · Auto Loader |
| Machine Learning 🚧 | MLflow · Unity Catalog Models |

</details>

<details>
<summary><b>📁 Organización del repositorio</b></summary>

<br>

```
00_metadata/                  # control del pipeline, logs, observabilidad y gobierno
01_ingest_sharepoint_bronze/  # ingesta a Bronze
02_silver_dimensiones/        # clientes, productos, ubicaciones
02_silver_hechos/             # pedidos, detalle de pedido
03_gold_dimensiones/          # 5 dimensiones
03_gold_hechos/               # hechos y resumen por pedido
03_gold_kpis/                 # 4 KPIs
04_reporte_excel_correo/      # Excel + correo
05_pruebas_calidad/           # pruebas con datos defectuosos
06_calidad_datos/             # motor de validaciones (24 reglas)
modulos_compartidos/          # funciones comunes de Silver
tests/                        # 13 pruebas con pytest
resources/ · databricks.yml   # Asset Bundle (YAML del Job)
.github/workflows/            # CI y CD
docs/                         # documentación detallada y ADRs
```

Cada carpeta separa el notebook de negocio (`01_negocio/`) de su notebook de manejo de errores (`02_logs/`).

</details>

<br>

## 🧩 Contexto

Proyecto que **migra un proceso tradicional** (SQL Server Integration Services sobre Data Warehouse on-premise) a una **arquitectura Lakehouse en la nube**, conservando las reglas de negocio del reporte original. El dataset es público (*DataCo Smart Supply Chain*, Kaggle) y la infraestructura es real.

<br>

<div align="center">

**Josuhe Sosa Lara** · Data Engineering · Lima, Perú

<sub>Dataset público · infraestructura real · construido de punta a punta sobre Databricks Lakehouse.</sub>

</div> 
