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

## Etapa C — Reprocesabilidad 🚧

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
- **Infraestructura con Terraform** (opcional) para el almacenamiento, las credenciales y los catálogos.
- **Terminado cuando:** el mismo bundle despliega a `dev` y a `prod` y existe un ADR con los tiempos y costos medidos.

---

## Etapa E — Nivel plataforma 🚧

- **Contratos de datos:** un archivo YAML por tabla con columnas, tipos, propietario y frescura exigida, validado automáticamente, y pruebas de qué pasa cuando la fuente agrega, quita o cambia el tipo de una columna.
- **SLOs:** metas de frescura, éxito y duración calculadas sobre `hd_etl_log`, con alerta si se incumplen.
- **Runbooks** para los fallos más comunes e **incidentes simulados con postmortem** publicados en el repositorio.
- **Segunda fuente (opcional):** una fuente pequeña adicional (por ejemplo, una API de tipo de cambio) que entra por la misma plataforma para mostrar que agregar un caso toma horas.
- **Terminado cuando:** un cambio de esquema en la fuente se detecta antes de llegar a Silver y hay al menos un postmortem escrito.

---

## Etapa F — Machine Learning 🚧

Modelo de riesgo de retraso con variables sin fuga de datos, MLflow, modelo versionado en Unity Catalog y tabla de predicciones. Se entrena solo con datos reales.
