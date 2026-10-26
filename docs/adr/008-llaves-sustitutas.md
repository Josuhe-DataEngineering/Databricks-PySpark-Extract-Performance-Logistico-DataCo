# ADR-008: Llaves sustitutas, por hash donde la tabla se reconstruye y secuenciales en las tablas con historial

- **Estado:** Aceptada, con una limitación conocida
- **Fecha:** 2026-10-26

## Contexto

Las tablas de Gold necesitan una llave sustituta estable para relacionar hechos
y dimensiones. La estabilidad importa: si una tabla se reconstruye y sus llaves
cambian, los hechos que las referencian quedan desalineados.

## Alternativas

1. **Hash de la llave natural (`xxhash64`):** el mismo dato produce siempre la
   misma llave, sin importar cuántas veces se reconstruya la tabla.
2. **Número secuencial** (máxima llave existente más un contador): sirve cuando
   una misma llave natural tiene varias filas, pero no es reproducible.

## Decisión

- **Hash estable (`xxhash64` de la llave natural)** en las dimensiones que se
  reconstruyen completas y tienen una fila por llave natural:
  `desc_dim_locations` y `desc_dim_shipping_mode`.
- **Llave secuencial** (`max_key` más un contador) en las tablas con **SCD2**:
  `desc_dim_customers`, `desc_dim_products` y `desc_ft_orders`. En ellas cada
  llave natural tiene una fila por versión, así que la llave sustituta debe ser
  distinta en cada versión y no puede derivarse solo de la llave natural.

## Motivos

- Donde la llave natural identifica una fila, el hash garantiza reproducibilidad.
- Donde hay historial, la llave debe distinguir versiones; la secuencial lo
  logra, y las versiones ya emitidas conservan su llave porque no se reescriben.

## Limitación conocida

La llave secuencial usa `monotonically_increasing_id()`, que no es contigua ni
reproducible si la tabla se reconstruye desde cero. Mientras las tablas SCD2 no
se reconstruyan, las llaves no cambian. Una mejora prevista es usar
`row_number()` o incorporar la fecha de vigencia al hash. Esto se retomará con
la etapa C (reprocesabilidad).

## Consecuencias

- Reconstruir `desc_dim_locations` o `desc_dim_shipping_mode` es seguro.
- Reconstruir las tablas SCD2 requiere recargar también los hechos que las
  referencian.
