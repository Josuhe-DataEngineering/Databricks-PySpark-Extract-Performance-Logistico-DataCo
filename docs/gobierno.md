# Gobierno de datos (Unity Catalog)

[← Volver al README](../README.md)

---

## Resumen

Se aplica con un notebook idempotente (`00_metadata/04_gobierno/aplicar_gobierno`), que se ejecuta cuando cambia el modelo. Cubre las tres capas del Lakehouse con un enfoque incremental: Gold tiene el gobierno más completo, Silver agrega permisos para analistas avanzados, y Bronze se limita a tags de clasificación para ingeniería.

---

## Comentarios

- **Por tabla:** cada tabla de Bronze, Silver y Gold lleva su descripción con el grano y el owner.
- **Por columna:** 262 columnas de Silver y Gold con su significado de negocio, a partir de un diccionario único por nombre de columna.

---

## Tags de clasificación

Todas las tablas llevan los tags `clasificacion` y `layer`:

| Capa | Tag `clasificacion` | Tag `layer` |
|---|---|---|
| Bronze | `confidencial` | `bronze` |
| Silver | `confidencial` | `silver` |
| Gold | `confidencial` | `gold` |

La columna `customer_email` lleva además el tag `DAC = YES` en Gold y Silver.

---

## Llaves informativas en Gold

Llaves primarias (verificadas como únicas y sin nulos antes de declararlas) y llaves foráneas entre hechos y dimensiones. Son **informativas** (no enforced por el motor), pero documentan las relaciones del modelo estrella en el catálogo.

---

## Enmascaramiento dinámico

El correo del cliente está enmascarado en:
- **Gold:** `desc_dim_customers.customer_email`
- **Silver:** `md_clientes.customer_email`

La función `mask_email` verifica si el usuario pertenece a `dac_lectores` o `dac_analistas_avanzados`; si pertenece, devuelve `***@***`.

Probado: al consultar la tabla, los miembros de esos grupos ven `XXXXXXXXX` en la columna de correo.

---

## Permisos por rol (GRANT)

| Grupo | Acceso |
|---|---|
| `dac_lectores` | `SELECT` sobre Gold |
| `dac_analistas_avanzados` | `SELECT` sobre Silver |
| *(sin grupo)* | Bronze: solo ingeniería accede |

Los grupos se nombran por rol, no por entorno.

---

## Diccionario de datos consultable

Tabla: `metadata_dataco.supply_chain.md_diccionario_datos`

Generada desde `information_schema` de las tres capas (Bronze, Silver y Gold). Contiene 536 columnas con:

| Campo | Descripción |
|---|---|
| `catalogo` | Catálogo de origen |
| `esquema` | Esquema de origen |
| `tabla` | Nombre de la tabla |
| `columna` | Nombre de la columna |
| `tipo` | Tipo de dato |
| `descripcion` | Comentario de la columna |
| `es_dato_personal` | `true` si lleva el tag `DAC = YES` |

Se regenera al ejecutar el notebook de gobierno.

---

## Probado, no aplicado

El **filtro de filas** funciona con el mismo mecanismo de grupo, pero falta definir el criterio de negocio que decide qué filas ve cada grupo.

---

## Límites de Free Edition y de Databricks

- Una máscara de columna no convive con restricciones `CHECK` en la misma tabla.
- Las restricciones `CHECK` solo van en Gold, porque las filas en cuarentena de Silver pueden traer llaves nulas o repetidas.
- Free Edition no permite service principals; el token de CI/CD es personal y de 90 días.

Detalle completo en el [ADR-014 · Gobierno de datos con Unity Catalog](adr/014-gobierno-en-gold.md).
