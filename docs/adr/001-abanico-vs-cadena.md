# ADR-001: Orquestar el Job en abanico (fan-out) en vez de en cadena

- **Estado:** Aceptada
- **Fecha:** 2026-10-26

## Contexto

El Job tiene 23 tareas de negocio (más 23 de log de errores). Pueden orquestarse
de dos formas:

- **Cadena:** cada tarea espera a la anterior, aunque no dependa de ella.
- **Abanico (fan-out):** cada tarea depende solo de lo que realmente necesita,
  de modo que las independientes (por ejemplo las 5 dimensiones de Silver o de
  Gold) pueden correr en paralelo.

Se midieron ambas versiones con el mismo código en Databricks Free Edition:

| Versión | Duración |
|---|---|
| Cadena | 16 min 34 s |
| Abanico | 19 min |

## Restricciones del entorno

Free Edition solo ofrece cómputo serverless y permite **máximo 5 tareas
simultáneas por cuenta**, por lo que el paralelismo no se aprovecha del todo.

## Decisión

Se versiona el Job **en abanico**, aunque en este entorno resulte ~2,5 min más
lento que la cadena.

## Motivos

- Las dependencias del abanico reflejan las dependencias reales de los datos;
  la cadena las oculta con un orden artificial.
- Con más cómputo (otro workspace de pago) el abanico escala y la cadena no.
- Un fallo en una rama no bloquea innecesariamente las ramas independientes.
- Se documenta el resultado medido, sin afirmar una ventaja que no se observó.

## Consecuencias

- Se añade una alerta: si el Job supera **35 min** (`RUN_DURATION_SECONDS > 2100`)
  se envía un correo (`on_duration_warning_threshold_exceeded`).
- Si en producción real se mantiene la restricción de concurrencia, conviene
  volver a medir antes de elegir.
