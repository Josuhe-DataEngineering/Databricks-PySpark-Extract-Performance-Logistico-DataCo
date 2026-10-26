# ADR-012: Usar un Lakehouse para un volumen moderado

- **Estado:** Aceptada
- **Fecha:** 2026-10-26

## Contexto

El dataset (DataCo Smart Supply Chain) tiene 180,519 filas. Ese volumen cabe en
una base de datos tradicional; usar un Lakehouse podría parecer excesivo.

## Decisión

Se construye el proyecto sobre una arquitectura Lakehouse (Databricks, Delta
Lake y Unity Catalog) aunque el volumen sea moderado.

## Motivos

El objetivo del proyecto **no es la escala**. Es demostrar las razones por las
que una empresa adopta este patrón:

- **Gobierno:** catálogo, permisos, clasificación y tags en Unity Catalog.
- **Trazabilidad:** cada fila se rastrea hasta el archivo y la ejecución que la
  cargó, y el linaje cubre Bronze, Silver y Gold.
- **Reproducibilidad:** misma entrada, mismo resultado (deduplicación
  determinista, historial Delta, idempotencia por ventana).

Además, el proyecto migra un proceso real de SSIS sobre un Data Warehouse
on-premise; llevarlo a un Lakehouse es parte del caso.

## Consecuencias

- El proyecto no afirma rendimiento a gran escala. Cualquier afirmación de
  escala debe salir de una prueba medida (etapa D) con datos sintéticos
  declarados como tales (ADR-013).
- Para este volumen exacto, una base de datos relacional también funcionaría;
  la elección se justifica por lo que el patrón enseña y gobierna, no por el
  tamaño.
