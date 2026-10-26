# ADR-009: Umbrales y decisión por regla en el motor de calidad

- **Estado:** Aceptada
- **Fecha:** 2026-10-26

## Contexto

El motor de calidad tiene 24 reglas (21 en Silver y 3 en Gold). Para cada una
hay que decidir qué porcentaje de cumplimiento se exige (umbral) y qué hacer si
no se alcanza.

## Decisión

Cada regla se define en una tabla (`md_dq_reglas`) con dimensión, criticidad,
umbral, decisión y justificación. Las decisiones posibles son tres:

| Decisión | Efecto | Reglas |
|---|---|---|
| **Detener** | La task falla y el Workflow se detiene | 7: unicidad en Silver (DQ-001 a DQ-004) y consistencia en Gold (DQ-014 a DQ-016) |
| **Cuarentena** | La fila se aísla con su motivo y el pipeline sigue | 9: DQ-005, 006, 008, 009, 011, 012, 013, 023 y 024 |
| **Advertir** | Se registra y se avisa, sin aislar ni detener | 8: DQ-007, DQ-010 y DQ-017 a DQ-022 |

Criterio general:
- Un **dato defectuoso** va a cuarentena con alerta, sin detener el pipeline.
- Un **exceso sobre el umbral** solo advierte.
- El pipeline **se detiene** únicamente ante errores propios: duplicados después
  de deduplicar, llaves rotas en Gold o Silver que no cuadra con Gold.

## Umbrales

- **100 %** en unicidad, completitud y validez de criticidad alta: no se tolera
  ninguna excepción.
- **99,5 %** en integridad referencial y en la fecha de envío: se tolera hasta
  0,5 % por desfases de carga y las filas afectadas se aíslan.
- **99 %** en validez de criticidad baja (por ejemplo, precio y descuento de
  cada línea): son señales de alerta, no errores del dato.

## Motivos

- Detener todo por un dato sucio paraliza el negocio; aislar y avisar mantiene
  el flujo y deja evidencia.
- Un duplicado después de deduplicar indica un fallo del propio pipeline, por
  eso sí detiene.
- Cada umbral lleva su justificación escrita junto a la regla.

## Consecuencias

- Cambiar un umbral o una decisión es modificar una fila del catálogo, sin
  tocar código.
- Cada regla se prueba con datos defectuosos (ADR-010).
