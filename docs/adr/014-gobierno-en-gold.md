# ADR-014: Gobierno de datos con Unity Catalog, y sus límites en Free Edition

- **Estado:** Aceptada
- **Fecha:** 2026-10-27

## Contexto

Las tablas de Gold son las que consume el negocio, y `desc_dim_customers` contiene
datos personales (nombre, correo y calle). Hay que decidir qué controles de
gobierno se aplican, dónde y cómo, dentro de las capacidades de Databricks Free
Edition.

## Decisión

El gobierno se aplica con un notebook idempotente
(`00_metadata/04_gobierno/aplicar_gobierno`). Las llaves y las restricciones se
aplican solo en Gold (`gld_dataco.supply_chain`); el resto, en las tres capas:

- **Comentario** en cada tabla, con el grano y el owner.
- **Tags** `clasificacion` (`interno` o `confidencial`) y `layer`.
- **Llaves primarias informativas**, declaradas solo si la llave es única y sin
  nulos (se verifica antes de aplicarlas), y **llaves foráneas informativas**
  entre hechos y dimensiones.
- **Máscara de columna** en `customer_email`, con el tag `DAC = YES`: los
  miembros del grupo `dac_lectores` ven `***@***` y el resto ve el valor real.
- **Permisos de lectura** (`USE CATALOG`, `USE SCHEMA` y `SELECT`) sobre Gold
  para `dac_lectores`.
- **Comentario por columna** en Silver y Gold, desde un diccionario único por
  nombre de columna; el notebook lista las columnas sin descripción.
- **Diccionario de datos** como tabla (`metadata_dataco.supply_chain.md_diccionario_datos`),
  generada desde `information_schema` y regenerada en cada ejecución.
- **Silver:** comentario, tags, la misma máscara de correo en `md_clientes` y
  `SELECT` para `dac_analistas_avanzados`.
- **Bronze:** tags `clasificacion = confidencial` y `layer`, sin permisos para
  grupos de lectura: solo ingeniería de datos accede.

## Límites encontrados y decisiones derivadas

1. **Máscara y `CHECK` no conviven.** Databricks rechaza una máscara de columna
   en una tabla con restricciones `CHECK` (`SQLSTATE 0A000`). Por eso Gold no
   lleva `CHECK`: la validez de los valores la verifica el motor de calidad
   (ADR-009), y la máscara es más importante en la dimensión de clientes.
2. **Restricciones solo en Gold.** En Silver, las filas en cuarentena pueden
   traer llaves nulas o repetidas (ADR-002), y una restricción las rechazaría.
   Gold solo lee filas válidas, así que ahí sí aplican.
3. **Las llaves son informativas.** Unity Catalog no las hace cumplir al
   escribir; documentan el modelo y alimentan el linaje.
4. **La máscara se aplica directamente** con `SET MASK`, no mediante políticas
   dirigidas por tags. El tag `DAC = YES` marca la columna sensible y documenta
   la intención.
5. **El filtro de filas funciona** (se probó con una tabla de prueba y el mismo
   grupo), pero no se aplica a Gold porque aún no hay un criterio de negocio
   que defina qué filas ve cada grupo.

## Por qué se aplica una vez

Se probó que los comentarios, los tags y las llaves de una tabla sobreviven a
las reescrituras (`overwrite`) del pipeline, y que el pipeline puede seguir
escribiendo en una tabla con máscara. Por eso el notebook no forma parte del
Job: se ejecuta cuando cambia el modelo, y es idempotente.

## Consecuencias

- Una tabla nueva de Gold debe añadirse al notebook para recibir su comentario,
  sus tags y sus llaves.
- Una columna nueva debe añadirse al diccionario del notebook; si falta, aparece
  en la lista de columnas sin descripción.
- Pendiente: captura del linaje y filtro de filas con criterio de negocio.
