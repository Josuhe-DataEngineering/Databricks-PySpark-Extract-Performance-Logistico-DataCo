# ADR-003: Módulo compartido para los helpers de Silver, con pruebas automáticas

- **Estado:** Aceptada
- **Fecha:** 2026-10-26

## Contexto

Los cinco notebooks de Silver (clientes, productos, ubicaciones, pedidos y
detalle de pedido) repetían las mismas funciones auxiliares: limpiar texto,
convertir a número, detectar tipos inválidos y quedarse con el registro más
reciente al deduplicar. Una corrección había que replicarla a mano en cada
notebook, con el riesgo de que alguno quedara distinto.

## Alternativas

1. **Mantener copias en cada notebook:** sin dependencias, pero las copias
   divergen con el tiempo.
2. **Módulo Python compartido en el repositorio:** una sola definición,
   versionada con el resto del código.
3. **Paquete instalable (.whl):** más formal, pero añade empaquetado y
   versionado desproporcionados para cuatro funciones.

## Decisión

Se crea `modulos_compartidos/transformaciones_silver.py` con las funciones
`clean_str`, `clean_num`, `tipo_invalido` y `dedup_reciente`. Los notebooks lo
importan agregando al `sys.path` la raíz del repositorio, calculada desde la
ubicación del notebook.

## Motivos

- Una sola definición: se corrige una vez y aplica a las cinco tablas.
- Es código de Python normal, por lo que se puede probar fuera de Databricks.
- Funciona igual con el Job original y con el desplegado por el bundle, porque
  ambos ejecutan los archivos del repositorio.

## Riesgo y mitigación

**Riesgo:** un error en el módulo afecta a las cinco tablas a la vez; antes, un
error se quedaba en un solo notebook.

**Mitigación:**
- 13 pruebas unitarias (pytest) cubren las cuatro funciones, con filas
  inventadas en memoria cuyo resultado correcto se conoce de antemano.
- Las pruebas corren en GitHub Actions en cada push y en cada pull request.
- Tras el cambio se validó con una ejecución completa del Job.

## Consecuencias

- Cualquier cambio al módulo debe pasar las pruebas antes de llegar a `main`.
- Las pruebas verifican la lógica de las funciones, no los datos reales: la
  calidad de los datos la siguen controlando las reglas de calidad (ADR-002).
- Si se agregan helpers nuevos, deben incluir sus pruebas.
