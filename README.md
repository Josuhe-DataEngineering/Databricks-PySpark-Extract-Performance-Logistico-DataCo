<div align="center">

# DataCo Supply Chain · Data Lakehouse

### Plataforma de datos **ELT end-to-end** sobre Databricks Lakehouse — de SSIS on-premise a un Lakehouse cloud gobernado, con calidad declarativa probada, observabilidad, infraestructura como código y Machine Learning

![Databricks](https://img.shields.io/badge/Databricks-FF3621?style=for-the-badge&logo=databricks&logoColor=white)
![Delta Lake](https://img.shields.io/badge/Delta_Lake-00ADD4?style=for-the-badge&logo=delta&logoColor=white)
![PySpark](https://img.shields.io/badge/PySpark-E25A1C?style=for-the-badge&logo=apachespark&logoColor=white)
![Unity Catalog](https://img.shields.io/badge/Unity_Catalog-FF3621?style=for-the-badge&logo=databricks&logoColor=white)
![GitHub Actions](https://img.shields.io/badge/CI/CD-GitHub_Actions-2088FF?style=for-the-badge&logo=githubactions&logoColor=white)

</div>

Tomé un reporte logístico que se armaba a mano cada semana (2-3 h de un analista) y lo convertí en una **plataforma de datos gobernada de punta a punta**: ingesta desde SharePoint, procesamiento en capas con **24 reglas de calidad probadas con datos defectuosos**, modelo dimensional con SCD2, gobierno con Unity Catalog, un Excel ejecutivo enviado por correo, trazabilidad y alertas — todo descrito como código y con CI/CD.

> **En construcción** marca lo que está diseñado pero todavía no está implementado. Lo demás ya corre de punta a punta. El detalle de lo que sigue está en la [hoja de ruta](docs/hoja-de-ruta.md).

---

## Estado del proyecto

| Fase | Alcance | Estado |
|---|---|---|
| **1. Pipeline de datos** | Bronze → Silver → Gold, modelo estrella con SCD2, Excel ejecutivo por correo | ✅ Completa |
| **2. Calidad de datos** | 24 reglas declarativas, cuarentena, pruebas con datos defectuosos | ✅ Completa |
| **3. CI y CD** | Módulo compartido, 13 pruebas `pytest` en GitHub Actions, Asset Bundles, deploy a `dev` | ✅ Completa |
| **4. Gobierno** | Comentarios, tags, máscara PII, GRANT por rol, diccionario de datos | ✅ Completa |
| **5. Reprocesabilidad** | SCD2 con fecha de negocio, backfill por ventana, snapshots regenerables | ✅ Completa |
| **6. Nube y escala** | Azure Databricks, ADLS Gen2, Auto Loader, prueba de escala | 🚧 En construcción |
| **7. Nivel plataforma** | Contratos de datos, SLOs, runbooks, incidentes simulados | 🚧 En construcción |
| **8. Machine Learning** | Modelo de riesgo de retraso con MLflow en Unity Catalog | 🚧 En construcción |

---

## Pipeline de un vistazo

```
SharePoint ──▶ Bronze ──▶ Silver ──▶ ✅ Calidad ──▶ Gold ──▶ ✅ Calidad ──▶ Excel + Correo
            (crudo,     (tipado,    (21 reglas    (modelo     (3 reglas
             STRING)     dedupe,     + cuarentena)  estrella)   consistencia)
                         cuarentena)
```

Pipeline orquestado como un único Databricks Workflow en **abanico** (46 tasks), descrito como código con Asset Bundles. Entre capas, dos **compuertas de calidad** validan los datos y detienen el flujo si una regla crítica falla. Cada task tiene su `log_error` que registra la excepción y notifica a Slack.

<p align="center">
  <img src="docs/workflow.png" alt="Workflow DataCo" width="100%">
</p>

---

## Resultados medidos

| Métrica | Valor |
|---|---|
| Ejecución completa (abanico) | 19 min |
| Ejecución completa (cadena) | 16 min 34 s |
| Reglas de calidad | 24 (21 Silver + 3 Gold) |
| Pruebas unitarias | 13 con `pytest` en CI |
| Columnas documentadas | 536 (diccionario consultable) |
| Comentarios por columna | 262 en Silver y Gold |
| Datos de última corrida | 65,752 pedidos · 0 duplicados · 0 cuarentena |

> El abanico no gana tiempo en Free Edition (cómputo compartido); se versiona así porque deja el grafo listo para un entorno con más capacidad ([ADR-001](docs/adr/001-abanico-vs-cadena.md)).

---

## Documentación detallada

| Documento | Qué contiene |
|---|---|
| **[Capas del Lakehouse](docs/capas.md)** | Qué hace Bronze, Silver, Gold: grano, cuarentena, SCD2, KPIs, entrega |
| **[Calidad de datos](docs/calidad-de-datos.md)** | Las 24 reglas, el motor declarativo, la cuarentena con trazabilidad y las pruebas con datos defectuosos |
| **[Gobierno](docs/gobierno.md)** | Comentarios, tags, máscara PII, permisos por rol, diccionario de datos, límites de Free Edition |
| **[CI y CD](docs/ci-cd.md)** | Módulo compartido, pruebas, Asset Bundles, GitHub Actions, despliegue a `dev` |
| **[Hoja de ruta](docs/hoja-de-ruta.md)** | Etapas A–F con criterio de terminado y estado |
| **[ADRs](docs/adr/)** | 14 decisiones de arquitectura documentadas |
| **[Pruebas manuales](docs/tests_manuales.md)** | Procedimiento paso a paso de las pruebas con datos defectuosos |

---

## Modelo dimensional

```
        dim_customers        dim_products
              │                    │
              ▼                    ▼
  dim_fecha ─▶ fact_orders ◀─ fact_order_details ◀─ dim_products
              ▲       ▲
        dim_locations  dim_shipping_mode
```

5 dimensiones (clientes y productos con SCD2) · 2 tablas de hechos · 7 indicadores de negocio (On-Time Delivery %, Late Delivery Risk %, Shipping Variance, Profit Margin %, Revenue por Cliente, Beneficio por Orden, Lead Time Promedio). Detalle en [capas.md](docs/capas.md).

---

## Stack

| Área | Tecnología |
|---|---|
| Plataforma | Databricks · Serverless |
| Procesamiento | PySpark · Spark SQL |
| Almacenamiento | Delta Lake |
| Catálogo y gobierno | Unity Catalog |
| Ingesta y correo | Microsoft Graph API |
| Alertas | Webhook de Slack |
| Pruebas | pytest |
| IaC, CI y CD | Asset Bundles · GitHub Actions |
| Nube 🚧 | Azure Databricks · ADLS Gen2 · Auto Loader |
| ML 🚧 | MLflow · Unity Catalog Models |

---

## Organización del repositorio

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
07_backfill/                  # orquestador de backfill por ventana de cortes
modulos_compartidos/          # funciones comunes de Silver
tests/                        # 13 pruebas con pytest
resources/                    # Asset Bundle (YAML del Job)
.github/workflows/            # CI y CD
docs/                         # documentación detallada y ADRs
```

---

## Contexto

Proyecto que **migra un proceso tradicional** (SSIS sobre Data Warehouse on-premise) a una **arquitectura Lakehouse en la nube**. El dataset es público (*DataCo Smart Supply Chain*, Kaggle) y la infraestructura es real.

---

<div align="center">

**Josuhe Sosa Lara** · Data Engineering · Lima, Perú

*Dataset público · infraestructura real · construido de punta a punta sobre Databricks Lakehouse.*

</div>
