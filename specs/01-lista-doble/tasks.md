# Tareas — Lista doble

Desglose de [`plan.md`](plan.md). Orden prueba → código. Un commit por tarea. Cada tarea de criterio agrupa al menos 3 pruebas por operación.

## Parte A — Base
- [x] **T-01.1** Copiar `Nodo` y la lista de Semana7 a `estructuras/lista_doble.py`; quitar los `print`, sacar `actual` de la lista, agregar `tamano` y `esta_vacia`; docstrings con complejidad.
- **Entregable:** `estructuras/lista_doble.py`

## Parte B — CA-12: publicar al frente
- [x] **T-01.2** Prueba (rojo): la publicación nueva queda primera; dos seguidas; una con la plaza vacía; los enlaces `anterior` y `siguiente` coinciden en ambos sentidos.
- [x] **T-01.3** Código: `insertar_al_frente` y `inicio`.
- **Entregables:** `tests/test_lista_doble.py`, `estructuras/lista_doble.py`

## Parte C — CA-13: paginar
- [x] **T-01.4** Prueba (rojo): páginas de 5 en ambos sentidos; límites inicial y final informados sin mover; plaza vacía; 5 y 6 publicaciones; publicar mientras otra sesión está en la página 2; dos sesiones independientes.
- [x] **T-01.5** Código: `pagina`, `avanzar`, `retroceder` con marcador.
- [x] **T-01.6** Código: `dominio/feed.py` con una posición por sesión.
- **Entregables:** `tests/test_lista_doble.py`, `estructuras/lista_doble.py`, `dominio/feed.py`

## Parte D — CA-29: buscar por palabra
- [x] **T-01.7** Prueba (rojo): coincidencia en título, en cuerpo, con otras mayúsculas y dentro de otra palabra; sin coincidencias; palabra vacía; títulos repetidos; orden de la más nueva a la más antigua.
- [x] **T-01.8** Código: `dominio/busqueda.buscar_palabra` recorriendo la lista.
- **Entregables:** `tests/test_lista_doble.py`, `dominio/busqueda.py`

## Parte E — Integración
- [ ] **T-01.9** Opciones de consola: publicar, siguiente página, página anterior, buscar por palabra (CA-37).
- [x] **T-01.10** Marcar CA-12, CA-13 y CA-29 como «pasa» en [`trazabilidad.md`](../trazabilidad.md).
- **Entregables:** `main.py`, `specs/trazabilidad.md`

## Estado (2026-11-08)
Hechas T-01.1 a T-01.8 y T-01.10 (estructura, plaza, sesión y búsqueda; CA-12, CA-13 y CA-29). T-01.9 (opciones de consola) espera al AVL, porque la consola necesita una sesión de usuario (Avance 3).

## Verificación final
- [ ] `pytest tests/test_lista_doble.py -v` sin errores.

## Historial de cambios
| Versión | Fecha | Cambio | Motivo |
|---|---|---|---|
| 1.0 | 2026-11-07 | Versión inicial | Creación |
| 1.1 | 2026-11-07 | Tareas reales por criterio (CA-12, CA-13, CA-29) en orden prueba → código, con entregables | Las tareas citaban la numeración vieja (CA-05, CA-06) y no tenían entregables |
