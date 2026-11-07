# Spec — Grafo (amistades y recomendaciones)
Versión 1.1 · Estado: aprobada para implementar

## 1. Contexto y objetivo
Las amistades de InsightHub forman una red: cada persona tiene unos pocos amigos entre todos los usuarios, y la amistad vale en los dos sentidos. Este componente guarda esa red, crea y deshace amistades (HU-03) y encuentra a las personas «a 2 saltos» para recomendar (HU-13).

Historias: **HU-03** y **HU-13** (Must). Criterios: **CA-06, CA-08, CA-34, CA-36**.
Las solicitudes pendientes (CA-05, CA-07) son de la cola ([`03-cola`](../03-cola/spec.md)). El orden de las recomendaciones por amigos en común (CA-35) es del montículo ([`07-monticulo`](../07-monticulo/spec.md)); este componente solo entrega los candidatos con su número de amigos en común.

## 2. Operaciones públicas y comportamiento

**RF-01 — Registrar una persona.**
CUANDO se cree un perfil, EL SISTEMA DEBE registrar a la persona en la red sin amigos.

**RF-02 — Crear una amistad.**
CUANDO una solicitud sea aceptada, EL SISTEMA DEBE crear la amistad entre las dos personas en ambos sentidos: cada una figura entre los amigos de la otra.
SI son la misma persona, ya son amigas, o alguna de las dos no existe, ENTONCES EL SISTEMA DEBE rechazarlo sin cambiar ninguna lista de amigos.

**RF-03 — Rechazar una solicitud.**
CUANDO una solicitud sea rechazada, EL SISTEMA NO DEBE crear amistad entre las dos personas.

**RF-04 — Deshacer una amistad.**
CUANDO una persona deshaga una amistad, EL SISTEMA DEBE eliminarla en ambos sentidos: ninguna figura ya entre los amigos de la otra.
SI la amistad no existe, o una de las personas no existe, ENTONCES EL SISTEMA DEBE informarlo sin error y sin cambiar nada.

**RF-05 — Consultar amistades.**
CUANDO se pregunte si dos personas son amigas, EL SISTEMA DEBE responder sí o no con el mismo resultado sin importar el orden en que se nombren.
CUANDO se pida la lista de amigos de una persona, EL SISTEMA DEBE devolverlos con la amistad más reciente primero; si no tiene, una lista vacía.
CUANDO se pregunte cuántos amigos tiene, EL SISTEMA DEBE devolver el número.

**RF-06 — Candidatos a recomendar.**
CUANDO se pidan los candidatos de una persona, EL SISTEMA DEBE devolver a quienes son amigos de sus amigos, sin repetir a nadie, sin incluirla a ella ni a quienes ya son sus amigos, y con el número de amigos que tienen en común con ella.
SI la persona no tiene amigos, o no existe, ENTONCES EL SISTEMA DEBE devolver una lista vacía sin error.

## 3. Criterios de aceptación
| ID | Criterio (de [`historias.md`](../00-producto/historias.md)) | Prioridad | Prueba esperada |
|---|---|---|---|
| CA-06 | Aceptar una solicitud crea la amistad en ambos sentidos; rechazarla la descarta sin crear amistad. | Must | `tests/test_grafo.py` |
| CA-08 | Deshacer una amistad la elimina en ambos sentidos; deshacer una que no existe no produce error. | Must | `tests/test_grafo.py` |
| CA-34 | Se recomiendan personas a 2 saltos (amigos de mis amigos), excluyéndome a mí y a quienes ya son mis amigos. | Must | `tests/test_grafo.py` |
| CA-36 | Una persona sin amigos recibe una lista vacía. | Must | `tests/test_grafo.py` |

## 4. Casos extremos
- Red sin personas: consultar amigos, preguntar si son amigos y pedir candidatos no fallan.
- Una sola persona sin amigos: lista de amigos vacía; candidatos vacíos (CA-36).
- Amistad de una persona consigo misma: rechazada (CA-06).
- Amistad repetida, nombrando a las dos personas en orden inverso: rechazada, y cada lista conserva una sola entrada (CA-06).
- Amistad con una persona que no existe: rechazada sin cambios.
- Deshacer una amistad inexistente, deshacerla dos veces seguidas, o con una persona inexistente: informa y no cambia nada (CA-08).
- Deshacer la única amistad, la primera y la última de una lista: las demás quedan intactas (CA-08).
- Deshacer una amistad y volver a crearla: se permite (CA-08, CA-06).
- Rechazar una solicitud: no existe amistad después (CA-06).
- Amigos de amigos que también son mis amigos (por ejemplo A–B, A–C, B–C): no se recomiendan (CA-34).
- Tres amigos de A que son amigos de D: D aparece una sola vez con 3 amigos en común (CA-34).
- A tiene amigos pero ninguno tiene otros amigos: candidatos vacíos (CA-34).
- Una solicitud pendiente no cuenta como amistad: esa persona sigue pudiendo recomendarse (CA-34).
- Persona con muchos amigos (por ejemplo 100): las operaciones siguen respondiendo.

## 5. Fuera de alcance
- Solicitudes pendientes y su orden (cola).
- Ordenar o limitar las recomendaciones (montículo).
- Camino más corto entre dos personas (A*, Won't).
- Amistades dirigidas o seguir sin aceptación.
- Guardar la red entre ejecuciones.

## Historial de cambios
| Versión | Fecha | Cambio | Motivo |
|---|---|---|---|
| 1.0 | 2026-11-07 | Versión inicial | Creación |
| 1.1 | 2026-11-07 | Se reescribe con requisitos CUANDO/EL SISTEMA DEBE; pasa de grafo dirigido de «seguimientos» a red de amistades no dirigida; criterios CA-06, CA-08, CA-34, CA-36 (antes CA-03, CA-04, CA-17 a CA-19); la amistad más reciente sale primero; el orden de recomendaciones (CA-35) queda en el montículo | La numeración y las reglas de las historias cambiaron (amistad con solicitud y aceptación); cada CA debe tener un solo dueño; decisiones tomadas en la consulta del componente |
