# ADR-011: Cómputo serverless, sin particionado ni Z-ORDER a esta escala

- **Estado:** Aceptada
- **Fecha:** 2026-10-26

## Contexto

El proyecto corre en Databricks Free Edition, que solo ofrece cómputo
serverless, sobre un volumen de 180,519 filas. Hay que decidir cómo se configura
el cómputo y cómo se organizan físicamente las tablas Delta.

## Decisión

- **Cómputo:** serverless. No se configura autoscale ni auto-terminación,
  porque no hay un clúster propio que dimensionar: Databricks asigna los
  recursos cuando el Workflow los pide y los libera al terminar.
- **Almacenamiento:** tablas Delta sin particionado ni `OPTIMIZE ... ZORDER`.

## Motivos

- A este volumen, particionar genera archivos muy pequeños y más metadatos sin
  ganar velocidad de lectura; el particionado y Z-ORDER rinden cuando las
  tablas son grandes.
- No hay parámetros de clúster que tunear; el esfuerzo se dedica a lo que sí
  importa aquí: calidad, trazabilidad y reproducibilidad (ADR-012).
- El límite real del entorno es la concurrencia (máximo 5 tareas simultáneas
  por cuenta), y eso se midió (ADR-001).

## Consecuencias

- Estas decisiones valen solo para esta escala.
- La etapa D de la hoja de ruta incluye una prueba con datos sintéticos de
  decenas o cientos de millones de filas, con tiempos y costos antes y después
  de `OPTIMIZE` y liquid clustering. Ese resultado permitirá revisar este ADR
  con datos medidos.
