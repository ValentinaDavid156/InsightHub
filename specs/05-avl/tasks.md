# Tareas — AVL

Desglose de [`plan.md`](plan.md). Orden prueba → código. Un commit por tarea. Cada tarea de criterio agrupa al menos 3 pruebas por operación. Las partes A a E son **Must**; las partes F a H son **Should** (HU-07 y búsqueda por fecha) y se hacen solo si sobra tiempo.

## Parte A — El árbol equilibrado
- [ ] **T-05.1** Adaptar `NodoArbol` de Semana10 a `estructuras/avl.py` con `clave`, `valor` y `altura`; `insertar` ordenado, `buscar`, `inorden`, `tamano`, `altura` (vacío = −1).
- [ ] **T-05.2** Prueba (rojo): las cuatro rotaciones (izquierda-izquierda, derecha-derecha, izquierda-derecha, derecha-izquierda) con tres claves; que ninguna rotación pierda un subárbol; que `inorden` siga ordenado después de cada una.
- [ ] **T-05.3** Código: rotaciones y reequilibrio al volver de la inserción, con el orden de punteros del plan.
- [ ] **T-05.4** Prueba (rojo): 100 claves en orden creciente y 100 en orden decreciente dejan altura ≤ 1.44·log₂(n+2); clave duplicada no cambia el árbol; árbol vacío y de un solo nodo.
- **Entregables:** `tests/test_avl.py`, `estructuras/avl.py`

## Parte B — CA-01 y CA-02: comunidad inicial
- [ ] **T-05.5** Prueba (rojo, CA-01): al generar hay 120 perfiles, todos con `@usuario` distinto y todos encontrables.
- [ ] **T-05.6** Prueba (rojo, CA-02): dos generaciones con la semilla 706132 dan los mismos perfiles en el mismo orden; con otra semilla, distintos.
- [ ] **T-05.7** Código: `dominio/usuarios.generar` con `random.Random(706132)`, lista fija de nombres y resorteo de repetidos.
- **Entregables:** `tests/test_avl.py`, `dominio/usuarios.py`

## Parte C — CA-03 y CA-04: entrar y validar
- [ ] **T-05.8** Prueba (rojo, CA-04): `@usuario` de 2, 3, 20 y 21 caracteres; con espacio, `@`, acento o `-`; ya existente; con mayúsculas distintas.
- [ ] **T-05.9** Código: validación y pase a minúsculas; `crear_perfil` rechaza con mensaje claro.
- [ ] **T-05.10** Prueba (rojo, CA-03): entrar con uno nuevo crea el perfil con 0 puntos y abre sesión; con uno existente solo abre sesión; entrar dos veces no duplica.
- [ ] **T-05.11** Código: `entrar` (buscar y, si no existe, crear).
- **Entregables:** `tests/test_avl.py`, `dominio/usuarios.py`

## Parte D — CA-27 y CA-28: buscar por prefijo
- [ ] **T-05.12** Prueba (rojo): prefijo con varias coincidencias en orden alfabético; `ana` y `ana_07` (el corto primero); otras mayúsculas; un solo usuario; árbol vacío; sin coincidencias; prefijo vacío.
- [ ] **T-05.13** Código: `buscar_por_prefijo` con las tres reglas de descarte del plan.
- **Entregables:** `tests/test_avl.py`, `estructuras/avl.py`

## Parte E — Integración Must
- [ ] **T-05.14** Opciones de consola: entrar, buscar usuarios por prefijo (CA-37).
- [ ] **T-05.15** Marcar CA-01 a CA-04, CA-27 y CA-28 como «pasa» en [`trazabilidad.md`](../trazabilidad.md).
- **Entregables:** `main.py`, `specs/trazabilidad.md`

## Parte F — CA-17 a CA-20: votos (Should)
- [ ] **T-05.16** Prueba (rojo): voto a favor +1 y en contra −1; dos votos iguales rechazados; propia respuesta rechazada; cambio de a favor a en contra −2 y al revés +2; retirar revierte y permite volver a votar; retirar sin votar informa; dos votantes se acumulan; dos respuestas no se mezclan.
- [ ] **T-05.17** Código: `dominio/votos.votar`, `cambiar`, `retirar` con un AVL por respuesta, usando `reemplazar`.
- **Entregables:** `tests/test_avl.py`, `dominio/votos.py`, `estructuras/avl.py`

## Parte G — CA-21: insignias (Should)
- [ ] **T-05.18** Prueba (rojo): 9 → Nuevo; 10 y 49 → Colaborador; 50 → Experto; negativos → Nuevo; bajar de 10 a 9 vuelve a Nuevo.
- [ ] **T-05.19** Código: `dominio/usuarios.insignia`.
- **Entregables:** `tests/test_avl.py`, `dominio/usuarios.py`

## Parte H — CA-39: publicaciones por fecha (Should)
- [ ] **T-05.20** Prueba (rojo): día sin publicaciones; varias en el mismo día de la más antigua a la más nueva; 23:59 y 00:00 de días vecinos no se mezclan; id con ceros a la izquierda ordena bien (9 antes que 10).
- [ ] **T-05.21** Código: `dominio/busqueda.por_fecha` con clave `AAAA-MM-DD|000123` y búsqueda por prefijo.
- **Entregables:** `tests/test_avl.py`, `dominio/busqueda.py`

## Parte I — Integración Should
- [ ] **T-05.22** Opciones de consola: votar, retirar voto, ver perfil con insignia, buscar por fecha.
- [ ] **T-05.23** Marcar CA-17 a CA-21 y CA-39 como «pasa» en [`trazabilidad.md`](../trazabilidad.md).
- **Entregables:** `main.py`, `specs/trazabilidad.md`

## Verificación final
- [ ] `pytest tests/test_avl.py -v` sin errores.

## Historial de cambios
| Versión | Fecha | Cambio | Motivo |
|---|---|---|---|
| 1.0 | 2026-11-07 | Versión inicial | Creación |
| 1.1 | 2026-11-07 | Tareas reales por criterio (CA-01 a CA-04, CA-27, CA-28 y, como Should, CA-17 a CA-21 y CA-39) en orden prueba → código, con entregables y las rotaciones como parte propia | Las tareas citaban la numeración vieja (CA-10 a CA-12) y no cubrían usuarios, votos ni fechas |
