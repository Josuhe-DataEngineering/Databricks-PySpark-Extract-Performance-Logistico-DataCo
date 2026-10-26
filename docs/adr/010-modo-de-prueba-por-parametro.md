# ADR-010: Un solo Job con modo de prueba por parámetro

- **Estado:** Aceptada. La condición de modo de prueba está pendiente de reactivar en el Job versionado (etapa C)
- **Fecha:** 2026-10-26

## Contexto

El motor de calidad debe probarse con datos defectuosos sin tocar producción.
Hay que decidir cómo ejecutar esas pruebas.

## Alternativas

1. **Un Job de pruebas aparte:** una copia del Workflow apuntando a tablas de
   prueba. Con el tiempo las dos copias divergen y la prueba deja de representar
   a producción.
2. **El mismo Job, con parámetros:** los catálogos y esquemas son parámetros;
   las pruebas redirigen los mismos notebooks a un esquema aislado.

## Decisión

Un solo Job. Sus parámetros tienen por defecto los valores de producción
(`modo_prueba=false`, catálogos y esquemas de producción). Una corrida de
prueba sobrescribe esos parámetros para apuntar al esquema `pruebas_calidad` y
a un Bronze defectuoso generado por código a partir de filas reales.

Durante las pruebas, una condición `es_modo_prueba` omitía el envío del correo y
la actualización de la tabla de control, para no afectar a producción.

## Motivos

- Se prueba el Workflow real, no copias: lo que pasa en la prueba es lo que
  pasaría en producción.
- Sin segundo Job que mantener.
- Los datos y los logs de producción no se tocan: las tablas y los esquemas de
  prueba son otros.

## Consecuencias

- Antes de cada escenario hay que reiniciar las tablas Silver y Gold de prueba,
  porque la dimensión de pedidos Gold es SCD2 y conserva historial.
- **Estado actual:** la condición `es_modo_prueba` no está en el Job versionado
  en `resources/`. Reactivarla está en la etapa C de la hoja de ruta; hasta
  entonces una corrida de prueba desde el bundle enviaría el correo real.
