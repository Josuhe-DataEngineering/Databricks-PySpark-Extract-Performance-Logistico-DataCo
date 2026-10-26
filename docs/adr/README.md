# Registro de decisiones de arquitectura (ADR)

Cada ADR documenta una decisión de diseño: el contexto, las alternativas, lo
que se decidió y por qué. Sirven para entender el proyecto sin tener que
reconstruir el razonamiento a partir del código.

| ADR | Decisión | Estado |
|---|---|---|
| [001](001-abanico-vs-cadena.md) | Orquestar el Job en abanico (fan-out) en vez de en cadena | Aceptada |
| [002](002-cuarentena-en-silver.md) | Cuarentena en la misma tabla de Silver, sin descartar filas | Aceptada |
| [003](003-modulo-compartido-silver.md) | Módulo compartido para los helpers de Silver, con pruebas automáticas | Aceptada |
| [004](004-cd-solo-despliega.md) | El CD despliega la definición del Job pero no lo ejecuta | Aceptada |
| [005](005-bronze-en-string.md) | Bronze con todas las columnas de negocio en STRING | Aceptada |
| [006](006-conversion-segura-de-tipos.md) | Conversión segura de tipos: `NULL` y cuarentena en vez de cero | Aceptada |
| [007](007-prefijos-de-tablas.md) | Convención de prefijos en los nombres de tabla | Aceptada |
| [008](008-llaves-sustitutas.md) | Llaves sustitutas: hash donde la tabla se reconstruye, secuenciales en las tablas con historial | Aceptada, con limitación conocida |
| [009](009-parametros-de-calidad.md) | Umbrales y decisión por regla en el motor de calidad | Aceptada |
| [010](010-modo-de-prueba-por-parametro.md) | Un solo Job con modo de prueba por parámetro | Aceptada, reactivación pendiente |
| [011](011-serverless-sin-particionado.md) | Cómputo serverless, sin particionado ni Z-ORDER a esta escala | Aceptada |
| [012](012-lakehouse-para-volumen-moderado.md) | Usar un Lakehouse para un volumen moderado | Aceptada |
| [013](013-datos-sinteticos.md) | Datos sintéticos solo para pruebas y escala, nunca para ML | Aceptada |

## Cómo agregar un ADR nuevo

1. Crear `NNN-titulo-corto.md` con el siguiente número.
2. Incluir: estado, fecha, contexto, alternativas, decisión, motivos y consecuencias.
3. Añadir una fila a la tabla de este índice.
4. Si una decisión cambia, no se borra el ADR anterior: se marca como
   *Reemplazada por ADR-NNN* y se escribe uno nuevo.
