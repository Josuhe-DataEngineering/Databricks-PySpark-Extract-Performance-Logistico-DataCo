# ADR-007: Convención de prefijos en los nombres de tabla

- **Estado:** Aceptada
- **Fecha:** 2026-10-26

## Contexto

El proyecto tiene tablas en tres capas y en un catálogo de metadatos. Sin una
convención, el nombre de una tabla no dice qué es ni en qué capa vive.

## Decisión

Cada tabla lleva un prefijo que indica su rol y su capa:

| Prefijo | Significado | Capa |
|---|---|---|
| `raw_` | Dato crudo | Bronze |
| `md_` | Maestro de datos | Silver |
| `hd_` | Histórico o transaccional | Silver y control |
| `desc_dim_` | Descriptor dimensional (dimensión) | Gold |
| `desc_ft_` | Descriptor de hechos | Gold |
| `desc_ft_kpi_` | Indicador | Gold |
| `vw_salud_` | Vista de salud del pipeline | Control |

Ejemplos: `md_clientes`, `hd_pedidos`, `desc_dim_customers`,
`desc_ft_orders`, `desc_ft_kpi_alertas`.

## Excepciones documentadas

- `hd_` se usa también para tablas de control que registran ejecuciones
  (`hd_etl_log`, `hd_deduplicacion_log`, `hd_cuarentena_resumen`,
  `hd_dq_resultados`), porque son históricos aunque no sean datos de negocio.
- El catálogo de reglas de calidad se llama `md_dq_reglas`: es un maestro, y
  vive en el catálogo de metadatos.

## Motivos

- El nombre responde de inmediato "¿es dato crudo, maestro, histórico o
  indicador?" sin abrir la tabla.
- Facilita permisos y revisión por capa.

## Consecuencias

- Toda tabla nueva debe elegir un prefijo de la lista; si ninguno encaja, se
  documenta aquí la excepción.
