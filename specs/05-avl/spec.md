# Spec — AVL (usuarios, votos y fechas)
Versión 1.1 · Estado: aprobada para implementar

## 1. Contexto y objetivo
Tres cosas de InsightHub necesitan encontrarse rápido y en orden:
- los **usuarios**, por su `@usuario` (acceso, perfil y búsqueda por prefijo);
- los **votos** de cada respuesta, para saber si una persona ya votó;
- las **publicaciones por fecha**, para listar las de un día.

Historias: **HU-01, HU-02, HU-10** (Must) y **HU-07, HU-10** (Should). Criterios Must: **CA-01, CA-02, CA-03, CA-04, CA-27, CA-28**. Criterios Should: **CA-17, CA-18, CA-19, CA-20, CA-21, CA-39**.
La búsqueda de publicaciones por palabra (CA-29) pertenece a la lista doble ([`01-lista-doble`](../01-lista-doble/spec.md)). En este componente «buscar usuarios por nombre» es buscar por `@usuario`.

## 2. Operaciones públicas y comportamiento

### Usuarios (Must)
**RF-01 — Comunidad inicial.**
CUANDO el sistema inicie, EL SISTEMA DEBE crear 120 perfiles de ejemplo, cada uno con un `@usuario` distinto.
CUANDO se use la misma semilla, EL SISTEMA DEBE producir los mismos perfiles en el mismo orden.

**RF-02 — Reglas del `@usuario`.**
CUANDO se cree un perfil, EL SISTEMA DEBE aceptar un `@usuario` de 3 a 20 caracteres formado por letras, números y guión bajo, sin distinguir mayúsculas de minúsculas (`@Ana` y `@ana` son la misma persona).
SI el `@usuario` tiene menos de 3 o más de 20 caracteres, o un carácter no permitido, o ya existe, ENTONCES EL SISTEMA DEBE rechazarlo con un mensaje claro que diga el motivo, sin crear nada.

**RF-03 — Entrar.**
CUANDO alguien entre con un `@usuario` que no existe y es válido, EL SISTEMA DEBE crear su perfil con 0 puntos y abrir su sesión.
CUANDO entre con uno que ya existe, EL SISTEMA DEBE abrir su sesión sin tocar el perfil.
SI el `@usuario` no es válido, ENTONCES EL SISTEMA DEBE rechazarlo como en RF-02.

**RF-04 — Buscar usuarios por prefijo.**
CUANDO se busque un prefijo, EL SISTEMA DEBE devolver todos los usuarios cuyo `@usuario` empieza por él, sin distinguir mayúsculas, en orden alfabético.
SI nadie coincide, o el prefijo está vacío, ENTONCES EL SISTEMA DEBE devolver un resultado vacío sin error.

**RF-05 — Consultar un perfil.**
CUANDO se pida un `@usuario`, EL SISTEMA DEBE devolver su perfil (con sus puntos e insignia) o decir que no existe.

### Votos (Should)
**RF-06 — Votar.**
CUANDO una persona vote a favor una respuesta, EL SISTEMA DEBE sumar 1 punto al autor de la respuesta; si vota en contra, restarle 1.
SI la persona ya votó esa respuesta en el mismo sentido, o es la autora de la respuesta, ENTONCES EL SISTEMA DEBE rechazar el voto sin cambiar puntos. Cada persona tiene como máximo un voto por respuesta.

**RF-07 — Cambiar o retirar el voto.**
CUANDO una persona cambie su voto, EL SISTEMA DEBE corregir los puntos del autor (de a favor a en contra, resta 2; de en contra a a favor, suma 2).
CUANDO retire su voto, EL SISTEMA DEBE revertir sus efectos, y la persona puede volver a votar después.
SI intenta retirar un voto que no dio, ENTONCES EL SISTEMA DEBE informarlo sin cambiar puntos.

**RF-08 — Insignia.**
CUANDO se muestre un perfil, EL SISTEMA DEBE mostrar la insignia según sus puntos: Nuevo con menos de 10, Colaborador desde 10 hasta 49, Experto desde 50. Los puntos negativos también son Nuevo.

### Fechas (Should)
**RF-09 — Publicaciones por fecha.**
CUANDO se busque una fecha, EL SISTEMA DEBE devolver las publicaciones hechas ese día, de la más antigua a la más nueva.
SI ese día no hubo publicaciones, ENTONCES EL SISTEMA DEBE devolver un resultado vacío sin error.

## 3. Criterios de aceptación
| ID | Criterio (de [`historias.md`](../00-producto/historias.md)) | Prioridad | Prueba esperada |
|---|---|---|---|
| CA-01 | Al iniciar, la comunidad tiene al menos 100 perfiles, cada uno con `@usuario` único. | Must | `tests/test_avl.py` |
| CA-02 | Con la misma semilla se obtienen los mismos perfiles en el mismo orden. | Must | `tests/test_avl.py` |
| CA-03 | Entrar con un `@usuario` nuevo crea el perfil y abre la sesión; con uno existente solo abre la sesión. | Must | `tests/test_avl.py` |
| CA-04 | Un `@usuario` inválido (longitud o caracteres) o ya existente al registrarse se rechaza con un mensaje claro. | Must | `tests/test_avl.py` |
| CA-27 | Buscar usuarios por prefijo devuelve las coincidencias en orden alfabético. | Must | `tests/test_avl.py` |
| CA-28 | Una búsqueda sin coincidencias devuelve resultado vacío, sin error. | Must | `tests/test_avl.py` |
| CA-17 | Un voto positivo suma 1 punto de reputación al autor de la respuesta. | Should | `tests/test_avl.py` |
| CA-18 | Un voto negativo resta 1 punto de reputación al autor de la respuesta. | Should | `tests/test_avl.py` |
| CA-19 | Cada persona tiene como máximo un voto por respuesta y no puede votar su propia respuesta. | Should | `tests/test_avl.py` |
| CA-20 | Cambiar o retirar el voto corrige el puntaje (de positivo a negativo el autor pierde 2 puntos; retirar revierte el voto). | Should | `tests/test_avl.py` |
| CA-21 | La insignia visible en el perfil depende de los puntos: Nuevo (menos de 10), Colaborador (desde 10), Experto (desde 50). | Should | `tests/test_avl.py` |
| CA-39 | Buscar publicaciones por fecha devuelve las publicadas ese día. | Should | `tests/test_avl.py` |

## 4. Casos extremos
**Usuarios**
- Sin usuarios (antes de generar): buscar y consultar devuelven vacío o «no existe» sin fallar.
- Un solo usuario: se encuentra por su nombre exacto y por cualquier prefijo suyo.
- `@usuario` de 2, 3, 20 y 21 caracteres: rechaza 2 y 21; acepta 3 y 20 (CA-04).
- Caracteres no permitidos (espacio, `@` dentro del nombre, acentos, `-`): rechazado (CA-04).
- `@Ana` frente a `@ana` frente a `@ANA`: es un único usuario (CA-03, CA-04).
- Entrar dos veces con el mismo nombre: el segundo solo abre sesión y no duplica (CA-03).
- Generar con la misma semilla dos veces: mismos 120 perfiles en el mismo orden; con otra semilla, distintos (CA-01, CA-02).
- 100 o más usuarios insertados ya en orden alfabético: las búsquedas siguen siendo rápidas; el índice se mantiene equilibrado.
- Prefijo que coincide con un usuario completo y con otros más largos (`ana`, `ana_07`): devuelve ambos, el más corto primero (CA-27).
- Prefijo en otras mayúsculas: encuentra lo mismo (CA-27).
- Prefijo sin coincidencias, o vacío: resultado vacío (CA-28).

**Votos (Should)**
- Primer voto a favor y primer voto en contra: ±1 punto (CA-17, CA-18).
- Votar dos veces igual: rechazado (CA-19). Votar la propia respuesta: rechazado (CA-19).
- Cambiar de a favor a en contra: el autor pierde 2; de en contra a a favor: gana 2 (CA-20).
- Retirar y volver a votar: se permite (CA-20).
- Retirar sin haber votado: se informa, sin cambios (CA-20).
- Dos personas votan la misma respuesta: los puntos se acumulan; dos respuestas distintas no se mezclan.

**Insignias (Should)**
- 9 puntos Nuevo, 10 Colaborador, 49 Colaborador, 50 Experto (CA-21).
- Puntos negativos: Nuevo. Un autor baja de 10 a 9 por un voto retirado: vuelve a Nuevo (CA-21).

**Fechas (Should)**
- Día sin publicaciones: vacío (CA-39).
- Varias publicaciones el mismo día: todas, de la más antigua a la más nueva (CA-39).
- Publicaciones de días vecinos (23:59 y 00:00): no se mezclan (CA-39).

## 5. Fuera de alcance
- Contraseñas y cuentas privadas.
- Borrar o renombrar un usuario.
- Buscar por parte intermedia del `@usuario` (solo por inicio).
- Votar publicaciones (solo respuestas).
- Persistir usuarios entre ejecuciones.

## Historial de cambios
| Versión | Fecha | Cambio | Motivo |
|---|---|---|---|
| 1.0 | 2026-11-07 | Versión inicial | Creación |
| 1.1 | 2026-11-07 | Se reescribe con requisitos CUANDO/EL SISTEMA DEBE; criterios CA-01 a CA-04, CA-27, CA-28 (Must) y CA-17 a CA-21, CA-39 (Should) en vez de los CA-10 a CA-12 viejos; CA-21 (insignias) queda aquí; CA-29 pasa a la lista doble; un solo índice por `@usuario`; reglas del `@usuario` (3 a 20, sin distinguir mayúsculas); 120 perfiles de ejemplo | La numeración de las historias cambió; CA-21 no tenía dueño; la búsqueda por palabra recorre la plaza; decisiones tomadas en la consulta del componente |
