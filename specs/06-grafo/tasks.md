# Tareas — Grafo

Desglose de [`plan.md`](plan.md). Orden prueba → código. Un commit por tarea. Cada tarea de criterio agrupa al menos 3 pruebas por operación. Todas las partes son **Must**.

## Parte A — Base
- [x] **T-06.1** Crear `estructuras/grafo.py` con el arreglo de listas de adyacencia sobre `Nodo` (de Semana5), el grado por persona y `agregar_vertice`, `amigos`, `grado`; docstrings con complejidad.
- **Entregable:** `estructuras/grafo.py`

## Parte B — CA-06: crear la amistad en ambos sentidos
- [x] **T-06.2** Prueba (rojo): `agregar_amistad(a, b)` deja a `b` entre los amigos de `a` y a `a` entre los de `b`; los grados suben; la amistad más reciente sale primero; rechaza a uno mismo, repetida (también nombrando al revés) y persona inexistente sin cambiar ninguna lista; red vacía.
- [x] **T-06.3** Código: `agregar_amistad` validando primero y luego las dos inserciones al inicio; `son_amigos`.
- [ ] **T-06.4** Prueba (rojo): aceptar una solicitud (cola → grafo) crea la amistad y rechazarla deja la red igual.
- [ ] **T-06.5** Código: `dominio/amistades.atender` llama a `agregar_amistad` solo al aceptar.
- **Entregables:** `tests/test_grafo.py`, `estructuras/grafo.py`, `dominio/amistades.py`

## Parte C — CA-08: deshacer la amistad
- [x] **T-06.6** Prueba (rojo): deshacer elimina en ambos sentidos con la amistad en primer, intermedio y último lugar; las demás quedan; la inexistente, repetida o con persona inexistente informa y no cambia; volver a crear después de deshacer.
- [x] **T-06.7** Código: `eliminar_amistad` con nodo anterior, en el orden del plan.
- **Entregables:** `tests/test_grafo.py`, `estructuras/grafo.py`

## Parte D — CA-34: candidatos a 2 saltos
- [x] **T-06.8** Prueba (rojo): amigos de amigos sin repetir; excluye a la persona y a sus amigos (triángulo A–B–C); D con 3 amigos en común aparece una vez con 3; persona inexistente; solicitud pendiente no excluye.
- [x] **T-06.9** Código: `candidatos_dos_saltos(u)` con `ColaEnlazada`, `excluido` y `comunes`.
- **Entregables:** `tests/test_grafo.py`, `estructuras/grafo.py`

## Parte E — CA-36: persona sin amigos
- [x] **T-06.10** Prueba (rojo): sin amigos → vacío; con amigos que no tienen otros amigos → vacío; red de una sola persona; red vacía.
- [x] **T-06.11** Código: salida temprana cuando la cola nace vacía.
- **Entregables:** `tests/test_grafo.py`, `estructuras/grafo.py`

## Parte F — Integración
- [ ] **T-06.12** Opciones de consola: aceptar o rechazar solicitud, deshacer amistad, ver amigos (CA-37). Las recomendaciones se integran junto al montículo ([`07-monticulo`](../07-monticulo/tasks.md)).
- [ ] **T-06.13** Marcar CA-06, CA-08, CA-34 y CA-36 como «pasa» en [`trazabilidad.md`](../trazabilidad.md).
- **Entregables:** `main.py`, `specs/trazabilidad.md`

## Estado (2026-11-08)
Hechas T-06.1 a T-06.3 y T-06.6 a T-06.11 (grafo: CA-08, CA-34 y CA-36; y la parte del grafo de CA-06). T-06.4, T-06.5, T-06.12 y T-06.13 esperan a las amistades integradas con la cola (avance 5).

## Verificación final
- [x] `pytest tests/test_grafo.py -v` sin errores.

## Historial de cambios
| Versión | Fecha | Cambio | Motivo |
|---|---|---|---|
| 1.0 | 2026-11-07 | Versión inicial | Creación |
| 1.1 | 2026-11-07 | Tareas reales por criterio (CA-06, CA-08, CA-34, CA-36) en orden prueba → código, con entregables | Las tareas citaban la numeración vieja (CA-03, CA-04, CA-17 a CA-19) y eran del grafo dirigido |
| 1.2 | 2026-11-08 | Se marcan hechas las tareas del grafo y se anota qué espera al avance 5 | Avance 4 implementado |
