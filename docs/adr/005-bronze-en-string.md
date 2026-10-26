# ADR-005: Bronze con todas las columnas de negocio en STRING

- **Estado:** Aceptada
- **Fecha:** 2026-10-26

## Contexto

La fuente es un archivo CSV en SharePoint (180,519 filas, de 2015-01-01 a
2018-01-31). Al cargarlo hay que decidir si Bronze infiere los tipos o guarda
el dato tal como llega.

## Alternativas

1. **Inferir tipos al cargar:** cómodo, pero un valor inesperado (texto en una
   columna numérica, fecha en otro formato) puede fallar la carga o convertirse
   en un valor distinto al original sin que nadie lo note.
2. **Todo en STRING:** Bronze es una copia fiel de la fuente; el tipado ocurre
   después, en Silver.

## Decisión

Todas las columnas de negocio de Bronze se almacenan como **STRING**, sin
inferencia de tipos, sin limpieza, sin deduplicación y sin reglas de negocio.
Solo las columnas técnicas están tipadas (fechas de corte y de carga,
identificador de ejecución, filas del archivo).

Cada fila lleva sus metadatos: fecha de carga, ejecución, origen, archivo,
hash SHA-256 del archivo, filas del archivo y el esquema original en JSON.

## Motivos

- Nunca se pierde información del origen: lo que llegó es lo que quedó.
- Un dato mal formado no rompe la ingesta; se detecta y se aísla en Silver,
  donde existe la cuarentena (ADR-002 y ADR-006).
- Los metadatos permiten rastrear cada fila hasta el archivo y la ejecución.

## Retención e idempotencia

- Historial Delta de **365 días** (`delta.logRetentionDuration` y
  `delta.deletedFileRetentionDuration`).
- La carga es idempotente: `replaceWhere` por fecha de pedido, de modo que una
  ventana que se traslapa reemplaza sus días y no duplica filas.

## Consecuencias

- Bronze no es para consumo: ninguna consulta de negocio debe leerlo
  directamente (sus columnas son texto).
- Bronze conserva los duplicados; la deduplicación ocurre en Silver.
