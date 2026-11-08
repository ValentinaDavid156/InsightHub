# Spec — Lista doble (plaza pública)
Versión 1.2 · Estado: aprobada para implementar

## 1. Contexto y objetivo
La plaza es la lista de todas las publicaciones de InsightHub, la más nueva primero. Cada persona la recorre hacia adelante y hacia atrás sin perder su lugar (HU-05), y desde ella se buscan publicaciones por palabra (HU-10).

Historias: **HU-05, HU-10** (Must). Criterios: **CA-12, CA-13, CA-29**.
La búsqueda de usuarios (CA-27, CA-28) y por fecha (CA-39) pertenece al AVL ([`05-avl`](../05-avl/spec.md)).

## 2. Operaciones públicas y comportamiento

**RF-01 — Publicar.**
CUANDO se publique una pregunta, EL SISTEMA DEBE dejarla como la primera de la plaza y aumentar el tamaño en uno.

**RF-02 — Paginar hacia adelante.**
CUANDO una persona pida la página siguiente, EL SISTEMA DEBE mover su posición 5 publicaciones hacia las más antiguas y mostrar esa página (la última puede traer menos de 5).
SI ya está en la última página, ENTONCES EL SISTEMA DEBE conservar su posición e informar que llegó al final.

**RF-03 — Paginar hacia atrás.**
CUANDO una persona pida la página anterior, EL SISTEMA DEBE mover su posición 5 publicaciones hacia las más nuevas y mostrar esa página.
SI ya está en la primera página, ENTONCES EL SISTEMA DEBE conservar su posición e informar que llegó al principio.
SI faltan menos de 5 publicaciones para llegar al principio (por ejemplo, porque otra persona publicó y su posición quedó desalineada), ENTONCES EL SISTEMA DEBE llevar su posición hasta el principio.

**RF-04 — Posición propia.**
CUANDO varias sesiones recorran la plaza, EL SISTEMA DEBE recordar la posición de cada sesión por separado, de modo que paginar en una no mueva a las otras.

**RF-05 — Volver al principio.**
CUANDO una persona pida volver al inicio, EL SISTEMA DEBE colocar su posición en la publicación más nueva.

**RF-06 — Plaza vacía.**
SI la plaza está vacía, ENTONCES paginar, volver al inicio y consultar la posición DEBEN informar «no hay publicaciones» sin fallar.

**RF-07 — Publicar con una sesión en curso.**
CUANDO se publique mientras una sesión está en otra página, EL SISTEMA DEBE conservar la posición de esa sesión sobre la misma publicación que veía.

**RF-08 — Buscar por palabra.**
CUANDO se busque una palabra, EL SISTEMA DEBE devolver, de la más nueva a la más antigua, las publicaciones cuyo título o cuerpo la contienen, sin distinguir mayúsculas y aceptando coincidencias dentro de otra palabra (buscar «python» encuentra «Pythonista»).
SI ninguna coincide, ENTONCES EL SISTEMA DEBE devolver un resultado vacío sin error.

**RF-09 — Estado.**
CUANDO se pregunte si la plaza está vacía o por su tamaño, EL SISTEMA DEBE responder sin cambiar nada.

## 3. Criterios de aceptación
| ID | Criterio (de [`historias.md`](../00-producto/historias.md)) | Prueba esperada |
|---|---|---|
| CA-12 | Una publicación nueva aparece como la primera de la plaza. | `tests/test_lista_doble.py` |
| CA-13 | Se puede paginar hacia adelante y atrás; en el primer o último extremo la posición no cambia y se informa el límite; con la plaza vacía no falla. | `tests/test_lista_doble.py` |
| CA-29 | Buscar publicaciones por palabra devuelve las que la contienen en el título o el cuerpo. | `tests/test_lista_doble.py` |

## 4. Casos extremos
- Plaza vacía: paginar, volver al inicio y buscar no fallan (CA-13, CA-29).
- Una sola publicación: ambas direcciones informan límite; la posición no cambia.
- Exactamente 5 publicaciones: una sola página; avanzar informa el final.
- 6 publicaciones: la segunda página trae 1.
- Publicar dos veces seguidas: la última queda primera y la anterior segunda (CA-12).
- Dos sesiones en distintas páginas: avanzar en una no mueve a la otra.
- Publicar mientras una sesión está en la página 2: sigue viendo la misma publicación.
- Posición desalineada (a menos de 5 publicaciones del principio): retroceder la lleva al principio y no informa límite.
- Palabra que aparece solo en el cuerpo, solo en el título, con otras mayúsculas o dentro de otra palabra: se encuentra (CA-29).
- Palabra vacía o solo espacios: resultado vacío, no devuelve toda la plaza.
- Publicaciones con el mismo título: ambas aparecen, la más nueva primero.

## 5. Fuera de alcance
- Borrar o editar publicaciones.
- Búsqueda por palabra exacta o con varias palabras a la vez.
- Ordenar la plaza por otro criterio.

## Historial de cambios
| Versión | Fecha | Cambio | Motivo |
|---|---|---|---|
| 1.0 | 2026-11-07 | Versión inicial | Creación |
| 1.1 | 2026-11-07 | Se reescribe con requisitos CUANDO/EL SISTEMA DEBE; criterios CA-12, CA-13 (antes CA-05, CA-06) y se suma CA-29 (búsqueda por palabra, que era del AVL en el mapeo); páginas de 5, posición por sesión, búsqueda sin distinguir mayúsculas y casos extremos concretos | La numeración de las historias cambió; la búsqueda por palabra recorre la plaza, no el AVL; decisiones tomadas en la consulta del componente |
| 1.2 | 2026-11-08 | RF-03: si faltan menos de 5 publicaciones para el principio, retroceder lleva al principio; se agrega ese caso extremo | Al implementar apareció la posición desalineada cuando alguien publica durante la sesión; decisión de Valentina |
