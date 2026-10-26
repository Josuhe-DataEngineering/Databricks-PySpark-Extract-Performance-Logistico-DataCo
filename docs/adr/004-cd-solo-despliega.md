# ADR-004: El CD despliega la definición del Job pero no lo ejecuta

- **Estado:** Aceptada
- **Fecha:** 2026-10-26

## Contexto

El repositorio tiene dos flujos automáticos en GitHub Actions:

- **Tests:** corre pytest en cada push a `main` y en cada pull request.
- **Deploy:** en un pull request valida el bundle (`databricks bundle validate`);
  al hacer merge a `main` lo despliega (`databricks bundle deploy`) en el target
  `dev`, que crea o actualiza el Job `[dev jsosa] databricks_extract_performance_logistico`.

Hay que decidir si, tras desplegar, el flujo también debe **ejecutar** el Job.

## Alternativas

1. **Desplegar y ejecutar en cada merge:** verifica de inmediato que el Job
   funciona de punta a punta.
2. **Solo desplegar:** el Job queda actualizado y la ejecución se lanza aparte.

## Decisión

Se aplica la opción 2: el CD **solo despliega**. La ejecución del Job es una
acción separada (desde la interfaz de Databricks o con `databricks bundle run`).

## Motivos

- Una ejecución completa dura entre 16 y 19 minutos y consume cómputo serverless
  limitado en Free Edition; hacerlo en cada merge, incluso uno que solo cambia
  documentación, es un gasto innecesario.
- El pipeline incluye el envío de un correo real con el reporte de Excel
  (`gld_reporte_excel_correo`); ejecutarlo automáticamente enviaría correos en
  cada merge.
- La ejecución modifica tablas con datos; conviene que sea una decisión
  deliberada y no un efecto secundario de cambiar un archivo.
- El despliegue es rápido (unos 20 s) y deja el feedback inmediato donde
  importa: el bundle es válido y el Job quedó actualizado.

## Seguridad del despliegue

- Las credenciales viven solo en GitHub Secrets: `DATABRICKS_HOST`,
  `DATABRICKS_TOKEN` y `BUNDLE_VAR_alert_email`. Ningún archivo del repositorio
  contiene URL del workspace, token ni correo.
- El token es un token personal dedicado al CD (`github-actions`), con
  vigencia de 90 días; debe renovarse antes de que venza y actualizarse en
  GitHub Secrets.
- Un grupo de concurrencia evita dos despliegues simultáneos sobre el mismo
  entorno.

## Consecuencias

- Un cambio mergeado puede dejar el Job desplegado sin haber sido ejecutado;
  la verificación real requiere una corrida manual.
- Limitación de Free Edition: no se pueden crear service principals (requieren
  APIs de cuenta), por lo que el CD usa un token personal. En un entorno
  empresarial se usaría un service principal con permisos mínimos.
- Evolución prevista: una corrida de verificación (smoke test) en modo de
  prueba tras el despliegue, cuando el modo de prueba se reactive en el Job
  versionado.
