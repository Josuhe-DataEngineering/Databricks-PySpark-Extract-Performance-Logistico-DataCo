# ADR-013: Datos sintéticos solo para pruebas y escala, nunca para Machine Learning

- **Estado:** Aceptada
- **Fecha:** 2026-10-26

## Contexto

El proyecto usa datos reales (el dataset público de DataCo), pero hay dos
necesidades que los datos reales no cubren: probar el comportamiento ante datos
defectuosos y medir el rendimiento a una escala mayor.

## Decisión

Los datos sintéticos se permiten solo en dos usos, siempre en un esquema aparte
y declarados como sintéticos:

1. **Pruebas de calidad:** un Bronze defectuoso (10,500 filas), generado por
   código a partir de filas reales, en el esquema `pruebas_calidad`. Las
   cantidades esperadas se calculan a partir de los datos inyectados, no se
   escriben a mano.
2. **Prueba de escala (etapa D):** decenas o cientos de millones de filas para
   medir tiempos y costos.

El **entrenamiento y la evaluación del modelo de Machine Learning usan solo
datos reales**, con separación temporal (entrenar con el pasado, probar con el
futuro).

## Motivos

- Un dato sintético refleja la distribución que se programó, no la del negocio.
  Un modelo entrenado con él aprendería el generador y las métricas serían
  engañosas.
- Para pruebas de calidad y de escala lo que importa es la forma del dato
  (defectos, volumen), no su significado de negocio.

## Consecuencias

- Los resultados de escala se declaran como medidos sobre datos sintéticos.
- Ninguna tabla sintética alimenta a Gold de producción ni al modelo.
