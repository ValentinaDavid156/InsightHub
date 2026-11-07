# Tareas — Pila

Desglose de [`plan.md`](plan.md). Orden prueba → código. Un commit por tarea. Cada tarea de criterio agrupa al menos 3 pruebas por operación (caso normal, extremo y error).

## Parte A — Base
- [x] **T-02.1** Copiar `Nodo` y `PilaEnlazada` de Semana10 a `estructuras/pila.py` y adaptar nombres (`tamano`) y docstrings con complejidad.
- **Entregable:** `estructuras/pila.py`

## Parte B — CA-30: «atrás» en orden inverso
- [x] **T-02.2** Prueba (rojo): apilar A, B, C → desapilar devuelve C, B, A; un elemento; `tope` no quita; repetidos no consecutivos.
- [x] **T-02.3** Código: `apilar`, `desapilar`, `tope` hasta que pase.
- [x] **T-02.4** Prueba (rojo): `navegacion.ir_a(p)` no apila si `p` es la pantalla actual; `atras()` vuelve a la anterior.
- [x] **T-02.5** Código: `dominio/navegacion.py` con `ir_a` y `atras`.
- **Entregables:** `tests/test_pila.py`, `estructuras/pila.py`, `dominio/navegacion.py`

## Parte C — CA-31: historial vacío
- [x] **T-02.6** Prueba (rojo): `desapilar` y `tope` en pila vacía lanzan `PilaVaciaError` sin cambiar el tamaño; `atras()` sin historial devuelve «no hay pantalla previa».
- [x] **T-02.7** Código: lanzar el error en la pila y capturarlo en la navegación.
- **Entregables:** `tests/test_pila.py`, `dominio/navegacion.py`

## Parte D — Integración
- [x] **T-02.8** Cada pantalla de la consola llama a `ir_a`; la opción «atrás» llama a `atras` (CA-37).
- [x] **T-02.9** Marcar CA-30 y CA-31 como «pasa» en [`trazabilidad.md`](../trazabilidad.md).
- **Entregables:** `main.py`, `specs/trazabilidad.md`

## Verificación final
- [x] `pytest tests/test_pila.py -v` sin errores.

## Historial de cambios
| Versión | Fecha | Cambio | Motivo |
|---|---|---|---|
| 1.0 | 2026-11-07 | Versión inicial | Creación |
| 1.1 | 2026-11-07 | Tareas reales por criterio (CA-30, CA-31) en orden prueba → código, con entregables y la capa de navegación | Las tareas citaban la numeración vieja (CA-13, CA-14) y no tenían entregables |
