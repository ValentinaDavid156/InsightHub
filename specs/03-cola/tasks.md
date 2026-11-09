# Tareas — Cola

Desglose de [`plan.md`](plan.md). Orden prueba → código. Un commit por tarea. Cada tarea de criterio agrupa al menos 3 pruebas por operación.

## Parte A — Base
- [x] **T-03.1** Copiar `ColaEnlazada` de Semana10 a `estructuras/cola.py`; renombrar `tamano`; agregar `contiene` y `__iter__`; docstrings con complejidad.
- **Entregable:** `estructuras/cola.py`

## Parte B — CA-05: enviar solicitud
- [x] **T-03.2** Prueba (rojo): la solicitud queda en la cola del destinatario; se rechazan a uno mismo, a un amigo y repetida sin cambiar la cola.
- [x] **T-03.3** Código: `dominio/amistades.enviar` con las tres validaciones y `contiene`.
- **Entregables:** `tests/test_cola.py`, `dominio/amistades.py`

## Parte C — CA-07: atender en orden
- [x] **T-03.4** Prueba (rojo): X, Y, Z salen en ese orden; vaciar y volver a encolar; sin pendientes informa sin error; el último en salir deja `_cola` en `None`.
- [x] **T-03.5** Código: `desencolar`, `frente` y `amistades.atender` (solo la primera).
- **Entregables:** `tests/test_cola.py`, `dominio/amistades.py`

## Parte D — CA-32: notificaciones en orden
- [x] **T-03.6** Prueba (rojo): solicitud, amistad aceptada y respuesta generan avisos que se leen en orden de llegada y vacían la cola.
- [x] **T-03.7** Código: `dominio/notificaciones.py` (`notificar`, `leer`).
- **Entregables:** `tests/test_cola.py`, `dominio/notificaciones.py`

## Parte E — CA-33: sin notificaciones
- [x] **T-03.8** Prueba (rojo): leer sin pendientes devuelve «sin notificaciones»; leer dos veces seguidas igual.
- [x] **T-03.9** Código: capturar `ColaVaciaError` o comprobar `esta_vacia` en `leer`.
- **Entregables:** `tests/test_cola.py`, `dominio/notificaciones.py`

## Parte F — Integración
- [x] **T-03.10** Opciones de consola: enviar solicitud, revisar solicitudes, ver notificaciones (CA-37).
- [x] **T-03.11** Marcar CA-05, CA-07, CA-32 y CA-33 como «pasa» en [`trazabilidad.md`](../trazabilidad.md).
- **Entregables:** `main.py`, `specs/trazabilidad.md`

## Estado (2026-11-08)
Hechas todas (T-03.1 a T-03.11): CA-05, CA-07, CA-32 y CA-33.

## Verificación final
- [x] `pytest tests/test_cola.py -v` sin errores.

## Historial de cambios
| Versión | Fecha | Cambio | Motivo |
|---|---|---|---|
| 1.0 | 2026-11-07 | Versión inicial | Creación |
| 1.1 | 2026-11-07 | Tareas reales por criterio (CA-05, CA-07, CA-32, CA-33) en orden prueba → código, con entregables | Las tareas citaban la numeración vieja (CA-15, CA-16) y no tenían entregables |
| 1.2 | 2026-11-08 | Se marcan hechas las tareas de amistades y de consola | Avance 5 implementado |
