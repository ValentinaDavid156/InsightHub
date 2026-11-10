# Tareas — Árbol general

Desglose de [`plan.md`](plan.md). Orden prueba → código. Un commit por tarea. Cada tarea de criterio agrupa al menos 3 pruebas por operación. Las partes B a D son **Must**; las partes E y F son **Should** (HU-08) y se hacen solo si sobra tiempo.

## Parte A — Base
- [x] **T-04.1** Adaptar `NodoArbol` de Semana10 a `estructuras/arbol_general.py` (primer hijo y hermano derecho, con autor, texto y puntaje); crear la clase del hilo con raíz y contador; docstrings con complejidad.
- **Entregable:** `estructuras/arbol_general.py`

## Parte B — CA-14: respuesta de primer nivel
- [x] **T-04.2** Prueba (rojo): abrir un hilo; responder a la publicación deja la respuesta en el nivel 1; varias respuestas quedan en orden de llegada; el tamaño aumenta.
- [x] **T-04.3** Código: `abrir_hilo` y `responder` con la cadena de hermanos.
- **Entregables:** `tests/test_arbol_general.py`, `estructuras/arbol_general.py`

## Parte C — CA-15: anidar y mostrar con sangría
- [x] **T-04.4** Prueba (rojo): cadena de 3 niveles o más; el hilo se muestra con el nivel de cada respuesta y debajo de su padre; hilo sin respuestas; hilo profundo (por ejemplo 2 000 niveles) que no agota la recursión.
- [x] **T-04.5** Código: `recorrer` con la pila propia, apilando primero el hermano y luego el hijo; `buscar` y `profundidad`.
- [x] **T-04.6** Código: `dominio/hilos.py` con el texto sangrado por nivel.
- **Entregables:** `tests/test_arbol_general.py`, `estructuras/arbol_general.py`, `dominio/hilos.py`

## Parte D — CA-16: padre inexistente
- [x] **T-04.7** Prueba (rojo): responder a un id inexistente o de otro hilo se rechaza y el hilo queda igual (tamaño y recorrido); identificador repetido rechazado.
- [x] **T-04.8** Código: validar padre e identificador antes de enlazar.
- **Entregables:** `tests/test_arbol_general.py`, `estructuras/arbol_general.py`

## Parte E — CA-22: aceptar la mejor respuesta (Should)
- [ ] **T-04.9** Prueba (rojo): acepta quien preguntó, una respuesta de primer nivel → queda fijada primero y el autor suma 15; rechazo si acepta otra persona, si es de segundo nivel, inexistente o ya hay aceptada.
- [ ] **T-04.10** Código: `aceptar` y mostrar con la fijada primero; `dominio/hilos.py` suma los 15 puntos.
- **Entregables:** `tests/test_arbol_general.py`, `estructuras/arbol_general.py`, `dominio/hilos.py`

## Parte F — CA-23: fijada por puntaje (Should)
- [ ] **T-04.11** Prueba (rojo): sin aceptada gana la de mayor puntaje positivo; empate → la más antigua; todas en cero o negativas → ninguna; sin respuestas → ninguna; la aceptada gana a la de mayor puntaje.
- [ ] **T-04.12** Código: `mejor_respuesta` sobre las de primer nivel con comparación estricta.
- **Entregables:** `tests/test_arbol_general.py`, `estructuras/arbol_general.py`

## Parte G — Integración
- [x] **T-04.13** Opciones de consola: publicar, ver hilo, responder a publicación o a respuesta (CA-37); si se hace HU-08, aceptar respuesta.
- [x] **T-04.14** Responder genera el aviso al autor de la publicación ([`03-cola`](../03-cola/tasks.md)).
- [x] **T-04.15** Marcar CA-14, CA-15 y CA-16 (y CA-22 y CA-23 si se hicieron) como «pasa» en [`trazabilidad.md`](../trazabilidad.md).
- **Entregables:** `main.py`, `specs/trazabilidad.md`

## Estado (2026-11-09)
Hechas T-04.1 a T-04.8 y T-04.13 a T-04.15 (CA-14, CA-15 y CA-16, con consola y avisos). Las partes E y F (mejor respuesta, CA-22 y CA-23) son Should y siguen pendientes. En la práctica las pruebas de las partes B a D se escribieron juntas antes del código.

## Verificación final
- [x] `pytest tests/test_arbol_general.py -v` sin errores.

## Historial de cambios
| Versión | Fecha | Cambio | Motivo |
|---|---|---|---|
| 1.0 | 2026-11-07 | Versión inicial | Creación |
| 1.1 | 2026-11-07 | Tareas reales por criterio (CA-14, CA-15, CA-16 y, como Should, CA-22 y CA-23) en orden prueba → código, con entregables | Las tareas citaban la numeración vieja (CA-07 a CA-09) y no cubrían la mejor respuesta |
| 1.2 | 2026-11-09 | Se marcan hechas las tareas Must con su estado | Avance 6 implementado |
