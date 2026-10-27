# Ingeniería de software, CI y CD

[← Volver al README](../README.md)

---

## Módulo compartido

Las funciones `clean_str`, `clean_num`, `tipo_invalido` y `dedup_reciente` viven en un solo módulo: `modulos_compartidos/transformaciones_silver.py`. Los cinco notebooks Silver lo importan en lugar de repetir la lógica en cada uno.

Un error en el módulo afectaría a las cinco tablas Silver; por eso está probado.

**Decisión de diseño:** [ADR-003 · Módulo compartido](adr/003-modulo-compartido-silver.md)

---

## 13 pruebas con `pytest`

Pruebas con datos de ejemplo creados en memoria, sin tocar las tablas reales. Comprueban, por ejemplo:

- Que un valor vacío o no convertible da `NULL` y nunca `0`.
- Que de una llave repetida se conserva la fila del corte más reciente.
- Que los campos de texto se normalizan correctamente.

Ubicación: `tests/`

---

## CI con GitHub Actions

En cada push a `main` y en cada pull request se levanta una máquina limpia con Java, Spark y `pytest`, y se ejecutan las 13 pruebas.

Archivo: `.github/workflows/ci.yml`

---

## Job como código (Databricks Asset Bundles)

El Job se exportó del Workflow que ya funcionaba y se describe en YAML:

- 46 tasks con dependencias explícitas.
- Parámetros de catálogo y esquema (redirigen a producción o pruebas).
- Notificaciones por correo.
- Alerta si la ejecución supera los 35 minutos.

Se desplegó con Asset Bundles y se ejecutó de punta a punta desde el repositorio.

Archivos: `databricks.yml` y `resources/`

**Decisión de diseño:** [ADR-001 · Abanico vs cadena](adr/001-abanico-vs-cadena.md) · [ADR-011 · Serverless sin particionado](adr/011-serverless-sin-particionado.md)

---

## CD con GitHub Actions

| Evento | Acción |
|---|---|
| Pull request | `databricks bundle validate` (sin tocar Databricks) |
| Merge a `main` | `databricks bundle deploy` → despliega el Job `[dev jsosa]` |

El despliegue **no ejecuta** el Job: correrlo, con su correo real y sus escrituras de datos, es una decisión aparte.

**Seguridad:** la URL del workspace, el token y el correo de alertas viven solo en **GitHub Secrets**; ningún archivo del repositorio los contiene. El token es personal, de 90 días, porque Free Edition no permite service principals.

Archivos: `.github/workflows/cd.yml`

**Decisión de diseño:** [ADR-004 · El CD solo despliega](adr/004-cd-solo-despliega.md)
