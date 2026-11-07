# Tareas — Lista simple (conectados)

Desglose de [`plan.md`](plan.md). Orden prueba → código. Un commit por tarea. Cada tarea de criterio agrupa al menos 3 pruebas por operación. Todas las partes son **Should** (HU-04): se hacen solo si sobra tiempo después de los Must.

## Parte A — Base
- [ ] **T-08.1** Adaptar `ListaEnlazada` de Semana6 a `estructuras/lista_simple.py`: solo `_cabeza` y contador, insertar al inicio, eliminar con nodo anterior (primero y cualquier otro); entradas con `usuario` y `ultima_actividad`; `UMBRAL = 30`; docstrings con complejidad.
- **Entregable:** `estructuras/lista_simple.py`

## Parte B — CA-09: al entrar figura conectada
- [ ] **T-08.2** Prueba (rojo): conectar deja a la persona en la lista; entrar dos veces no la repite y renueva la hora; varias personas con la última primero; lista vacía; hora que retrocede rechazada sin cambios.
- [ ] **T-08.3** Código: `conectar`, `esta_conectado` y la validación de `ahora` (`ValueError`).
- **Entregables:** `tests/test_lista_simple.py`, `estructuras/lista_simple.py`

## Parte C — CA-10: salir y caducar
- [ ] **T-08.4** Prueba (rojo, salir): salir siendo la primera, una intermedia y la última; salir sin haber entrado; salir dos veces; salir de la única persona.
- [ ] **T-08.5** Código: `salir` con nodo anterior y orden de punteros del plan.
- [ ] **T-08.6** Prueba (rojo, inactividad): a los 29 s sigue conectada y a los 30 no; una acción a los 29 s renueva el plazo (58 conectada, 59 no); varias vencen a la vez incluyendo la primera y la última; una desconectada que actúa vuelve a figurar conectada.
- [ ] **T-08.7** Código: `registrar_actividad` y `caducar` en un solo recorrido sin mover `anterior` tras desenlazar.
- **Entregables:** `tests/test_lista_simple.py`, `estructuras/lista_simple.py`

## Parte D — CA-11: lista y estado de los amigos
- [ ] **T-08.8** Prueba (rojo): `listar` con la última conectada primero; vacía devuelve vacío; `estado_amigos` con amigos conectados, desconectados y que nunca entraron mezclados; persona inexistente → «no conectada»; `cantidad` coincide con la lista.
- [ ] **T-08.9** Código: `listar`, `estado_amigos`, `cantidad`; `dominio/presencia.py` pide los amigos al grafo.
- **Entregables:** `tests/test_lista_simple.py`, `estructuras/lista_simple.py`, `dominio/presencia.py`

## Parte E — Integración
- [ ] **T-08.10** Consola: cada comando llama a `registrar_actividad`; opciones «ver conectados» y «ver estado de mis amigos» (CA-37).
- [ ] **T-08.11** Marcar CA-09, CA-10 y CA-11 como «pasa» en [`trazabilidad.md`](../trazabilidad.md).
- **Entregables:** `main.py`, `specs/trazabilidad.md`

## Verificación final
- [ ] `pytest tests/test_lista_simple.py -v` sin errores.

## Historial de cambios
| Versión | Fecha | Cambio | Motivo |
|---|---|---|---|
| 1.0 | 2026-11-07 | Versión inicial (la carpeta estaba vacía) | Faltaban las tareas de la lista simple: CA-09, CA-10 y CA-11 en orden prueba → código, con entregables |
