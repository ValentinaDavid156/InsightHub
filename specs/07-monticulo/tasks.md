# Tareas — Montículo máximo

Desglose de [`plan.md`](plan.md). Orden prueba → código. Un commit por tarea. Cada tarea de criterio agrupa al menos 3 pruebas por operación. Las partes A a C son **Must** (HU-13); las partes D a H son **Should** (HU-09) y se hacen solo si sobra tiempo.

## Parte A — El montículo
- [x] **T-07.1** Prueba (rojo): `insertar` y `extraer_maximo` devuelven siempre el mayor según `antes`; vacío, un elemento, repetidos con la misma clave, 100 elementos en orden creciente y decreciente; el arreglo cumple la propiedad del montículo después de cada operación.
- [x] **T-07.2** Código: `estructuras/monticulo.py` con `antes(a, b)` recibida, `insertar`, `maximo`, `extraer_maximo`, `subir`, `bajar`; docstrings con complejidad.
- [x] **T-07.3** Prueba (rojo): `construir` con m candidatos deja el mismo resultado que insertarlos de uno en uno; lista vacía y un elemento.
- [x] **T-07.4** Código: `construir` bajando desde el último padre hasta la raíz.
- **Entregables:** `tests/test_monticulo.py`, `estructuras/monticulo.py`

## Parte B — CA-35: recomendaciones ordenadas (Must)
- [x] **T-07.5** Prueba (rojo): sin candidatos → vacío; uno; exactamente 5; 6 → solo los 5 mejores; todos empatados → alfabético por `@usuario`; 50 amigos en común frente a 1; pedirlas dos veces da lo mismo y no cambia los candidatos.
- [x] **T-07.6** Código: `dominio/recomendaciones.py` con la función de orden (más amigos en común; empate por `@usuario`), `construir` y 5 `extraer_maximo`.
- **Entregables:** `tests/test_monticulo.py`, `dominio/recomendaciones.py`

## Parte C — Integración Must
- [x] **T-07.7** Opción de consola: «personas que quizá conozcas» (CA-37), usando el grafo ([`06-grafo`](../06-grafo/tasks.md)) y este componente.
- [x] **T-07.8** Marcar CA-35 como «pasa» en [`trazabilidad.md`](../trazabilidad.md).
- **Entregables:** `main.py`, `specs/trazabilidad.md`

## Parte D — CA-24: la destacada es la de mayor actividad (Should)
- [ ] **T-07.9** Prueba (rojo): actividad = respuestas + votos vigentes; una sin respuestas no supera a una con respuestas; todas empatadas → la más reciente; cambiar un voto no cambia la actividad; consultar varias veces no altera nada.
- [ ] **T-07.10** Código: `dominio/destacada.py` con `publicar`, `responder`, `votar`, `retirar_voto`, `destacada`, y la función de orden (mayor actividad; empate por id).
- **Entregables:** `tests/test_monticulo.py`, `dominio/destacada.py`

## Parte E — CA-25: reacomodar al cambiar (Should)
- [ ] **T-07.11** Prueba (rojo): otra publicación supera a la destacada → cambia; empata y es más reciente → cambia; empata y es más antigua → no; la destacada pierde un voto y otra queda arriba → cambia; las posiciones coinciden con el arreglo después de cada intercambio.
- [ ] **T-07.12** Código: `actualizar` con arreglo de posiciones y el orden de intercambios del plan.
- **Entregables:** `tests/test_monticulo.py`, `estructuras/monticulo.py`

## Parte F — CA-26: sin publicaciones (Should)
- [ ] **T-07.13** Prueba (rojo): sin publicaciones → «no hay destacada»; una sola con actividad 0 → es la destacada; extraer hasta vaciar y volver a consultar.
- [ ] **T-07.14** Código: manejar el montículo vacío sin lanzar error al consultar la destacada.
- **Entregables:** `tests/test_monticulo.py`, `dominio/destacada.py`

## Parte G — Integración Should
- [ ] **T-07.15** Consola: mostrar la publicación destacada arriba de la plaza; actualizarla con cada respuesta y voto.
- [ ] **T-07.16** Marcar CA-24, CA-25 y CA-26 como «pasa» en [`trazabilidad.md`](../trazabilidad.md).
- **Entregables:** `main.py`, `specs/trazabilidad.md`

## Parte H — Medición para `ANALISIS.md` (Should)
- [ ] **T-07.17** Medir con 1 000 y 10 000 publicaciones: `actualizar` en el montículo frente a recorrer todas para hallar la mayor; registrar los tiempos como en `Semana4/decision.md`.
- **Entregable:** tabla de tiempos en `ANALISIS.md`

## Estado (2026-11-10)
Hechas T-07.1 a T-07.8 (montículo, recomendaciones y consola: CA-35). Las partes D a H (destacada y medición, CA-24 a CA-26) son Should y siguen pendientes. En la práctica las pruebas de las partes A y B se escribieron juntas antes del código.

## Verificación final
- [x] `pytest tests/test_monticulo.py -v` sin errores.

## Historial de cambios
| Versión | Fecha | Cambio | Motivo |
|---|---|---|---|
| 1.0 | 2026-11-07 | Versión inicial (la carpeta estaba vacía) | Faltaban las tareas del montículo: CA-35 (Must) y CA-24, CA-25, CA-26 (Should) en orden prueba → código, con entregables y una medición para el análisis |
| 1.1 | 2026-11-10 | Se marcan hechas las tareas Must con su estado | Avance 7 implementado |
