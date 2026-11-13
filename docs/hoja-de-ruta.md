# Hoja de ruta

[← Volver al README](../README.md)

Cada etapa se publica por separado y tiene un criterio de terminado. Las etapas marcadas con ✅ ya están hechas; el resto es 🚧 *en construcción*.

---

## Etapa A — Ingeniería de software, CI y CD ✅ Completa

- **Módulo compartido** (`clean_str`, `clean_num`, `tipo_invalido`, `dedup_reciente`) en `modulos_compartidos/`, importado por los cinco notebooks Silver.
- **13 pruebas unitarias con `pytest`** sobre esas funciones, en `tests/`.
- **GitHub Actions:** en cada push a `main` y en cada pull request se instalan Spark y Java y se ejecutan las pruebas.
- **Databricks Asset Bundles:** el Job, sus tasks, dependencias, parámetros y notificaciones descritos en YAML, con alerta si la ejecución supera los 35 minutos; validado desplegándolo y ejecutándolo de punta a punta desde el repositorio.
- **CD a `dev`:** un pull request valida el bundle y el merge a `main` despliega el Job `[dev jsosa]`; probado con ambos caminos. Las credenciales están en GitHub Secrets.
- **Decisiones documentadas:** catorce ADRs en `docs/adr/`.
- *El target `prod` y el despliegue automático hacia él pasan a la etapa D.*

Detalle en [ci-cd.md](ci-cd.md).

---

## Etapa B — Gobierno y metadatos ✅ Completa

- ✅ **Hecho:** comentario por tabla y por columna, tags de clasificación, llaves primarias y foráneas informativas en Gold, máscara del correo en Gold y Silver, GRANT por rol y diccionario de datos consultable (ADR-014).
- Pendiente menor: filtro de filas con un criterio de negocio definido, y bloque de trazabilidad estándar en la cabecera de cada notebook.
- ✅ **Cumplido:** cualquier tabla se explica sola desde el catálogo y `customer_email` se ve enmascarado para los grupos lectores.

Detalle en [gobierno.md](gobierno.md).

---

## Etapa C — Reprocesabilidad ✅ Completa

- SCD2 con fecha de negocio en lugar de la fecha del sistema; snapshots de KPIs regenerables para cortes pasados.
- Cierre en el SCD2 de los pedidos que pasan a cancelados.
- Backfill por rango de ventanas, notebook de reinicio y marca de ejecuciones interrumpidas en el log.
- Registro del mensaje de error también en las corridas de prueba (parametrizar los `log_error_*`).
- Reactivar el modo de prueba en el Job versionado (condición `es_modo_prueba`).
- **Terminado cuando:** se puede recargar cualquier rango de cortes sin tocar tablas a mano y el resultado es el mismo.

---

## Etapa D — Nube y escala 🚧

- **Despliegue automático a `prod`:** el CD a `dev` ya existe (etapa A); aquí se extiende a `prod`, con aprobación antes de desplegar.
- **Dos entornos con el mismo código:** Databricks Free Edition como `dev` y **Azure Databricks** como `prod`, con almacenamiento externo en **ADLS Gen2**, Unity Catalog con ubicación externa y presupuesto con alerta de costo.
- **Ingesta incremental con Auto Loader** sobre archivos que llegan al almacenamiento, en lugar de leer el archivo completo por ventana.
- **Prueba de escala:** datos sintéticos de decenas o cientos de millones de filas, en un esquema aparte y declarados como sintéticos, con tiempos y costos antes y después de `OPTIMIZE` y liquid clustering.
- **Infraestructura con Terraform** para el almacenamiento, las credenciales y los catálogos.
- **Terminado cuando:** el mismo bundle despliega a `dev` y a `prod` y existe un ADR con los tiempos y costos medidos.

---

## Etapa E — Nivel plataforma 🚧

- **Contratos de datos:** un archivo YAML por tabla con columnas, tipos, propietario y frescura exigida, validado automáticamente, y pruebas de qué pasa cuando la fuente agrega, quita o cambia el tipo de una columna.
- **SLOs:** metas de frescura, éxito y duración calculadas sobre `hd_etl_log`, con alerta si se incumplen.
- **Runbooks** para los fallos más comunes e **incidentes simulados con postmortem** publicados en el repositorio.
- **Segunda fuente:** una fuente pequeña adicional (por ejemplo, una API de tipo de cambio) que entra por la misma plataforma para mostrar que agregar un caso toma horas.
- **Terminado cuando:** un cambio de esquema en la fuente se detecta antes de llegar a Silver y hay al menos un postmortem escrito.

---

## Etapa F — Machine Learning ✅ Completa

Modelo de clasificación binaria que predice riesgo de retraso en entrega, construido y orquestado de punta a punta dentro del mismo Workflow de Databricks. Se entrena solo con datos reales, usando variables disponibles al momento de crear el pedido (sin fuga de datos), y el modelo queda versionado en Unity Catalog Model Registry.

**Lo que se construyó:**

- **`ml_feature_engineering`** — genera `desc_ml_features_orders` a partir de Gold (fact_orders + dim_fecha + dim_locations + dim_shipping_mode); 7 features sin fuga de datos, overwrite idempotente por corte.
- **`ml_train_register`** — pipeline Random Forest (StringIndexer x3 → OHE → VectorAssembler → RandomForestClassifier, 100 árboles, profundidad 10, seed 42); split 80/20 estratificado; registra accuracy, F1, precision, recall, AUC-ROC e importancias en experimento MLflow `dataco_late_delivery_risk`; modelo registrado en Unity Catalog (`gld_dataco.supply_chain.ml_late_delivery_risk`) con alias `champion`.
- **`ml_predict`** — carga el modelo por alias `champion` (sin hardcodear versión), aplica el pipeline sobre los pedidos vigentes y escribe `desc_ml_late_delivery_risk` con `late_delivery_risk_pred`, `prob_retraso`, `model_version` y trazabilidad de corte.
- **3 notebooks `log_error_*`** — mismo patrón Jobs API + DeltaTable + Slack que el resto del pipeline.
- **YAML del bundle actualizado** — 6 tasks ML (`ml_feature_engineering → ml_train_register → ml_predict` + sus 3 `log_error_*`) corriendo en paralelo con `dq_validaciones_gold` tras `gld_order_summary`; total del Workflow: 52 tasks.

**Lecciones técnicas registradas:**

- En clusters shared/serverless se requiere `dfs_tmpdir` apuntando a un UC Volume (`/Volumes/...`) tanto en `log_model()` como en `load_model()`.
- Unity Catalog exige `signature` e `input_example` al registrar; sin ellos el registro falla con error explícito.
- El alias `champion` permite promover una nueva versión del modelo sin modificar el notebook de predicción.

**Criterio cumplido:** el modelo corre automáticamente dentro del Workflow en cada corte, las predicciones están en una tabla Gold consultable, y el experimento MLflow permite comparar versiones entre ejecuciones.
