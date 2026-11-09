# Spec — Cola
Versión 1.2 · Estado: aprobada para implementar

## 1. Contexto y objetivo
Dos cosas en InsightHub se atienden en orden de llegada: las **solicitudes de amistad** pendientes de cada persona (HU-03) y sus **notificaciones** (HU-12). Cada persona tiene una cola de solicitudes y una cola de notificaciones.

Historias: **HU-03, HU-12** (Must). Criterios: **CA-05, CA-07, CA-32, CA-33**.
CA-06 (la amistad se crea en ambos sentidos) y CA-08 (deshacer amistad) pertenecen al grafo ([`06-grafo`](../06-grafo/spec.md)); la cola solo entrega la solicitud que se acepta o se rechaza.

## 2. Operaciones públicas y comportamiento

**RF-01 — Encolar.**
CUANDO se encole un elemento, EL SISTEMA DEBE dejarlo al final, detrás de todos los que ya esperaban, y aumentar el tamaño en uno.

**RF-02 — Desencolar.**
CUANDO se desencole y haya elementos, EL SISTEMA DEBE devolver el que llegó primero, quitarlo y disminuir el tamaño en uno.

**RF-03 — Consultar el frente.**
CUANDO se consulte el frente y haya elementos, EL SISTEMA DEBE devolver el que llegó primero sin quitarlo.

**RF-04 — Cola vacía.**
SI se desencola o se consulta el frente con la cola vacía, ENTONCES EL SISTEMA DEBE avisar la condición de cola vacía de forma controlada, sin modificar la cola.

**RF-05 — Contiene.**
CUANDO se pregunte si un elemento está en la cola, EL SISTEMA DEBE responder sí o no sin modificar la cola.

**RF-06 — Estado.**
CUANDO se pregunte si está vacía o por su tamaño, EL SISTEMA DEBE responder sin modificar la cola.

**RF-07 — Enviar solicitud.**
CUANDO una persona envíe una solicitud de amistad, EL SISTEMA DEBE dejarla pendiente al final de la cola de solicitudes del destinatario.
SI el destinatario es la misma persona, ya es su amigo ya tiene una solicitud pendiente de esa persona, o esa persona ya le envió una a quien la intenta, ENTONCES EL SISTEMA DEBE rechazarla con un mensaje claro que diga el motivo y sin encolarla.

**RF-08 — Atender solicitudes.**
CUANDO la persona revise sus solicitudes, EL SISTEMA DEBE mostrarle solo la primera pendiente para aceptarla o rechazarla; al decidir, esa solicitud sale de la cola.
SI no tiene solicitudes pendientes, ENTONCES EL SISTEMA DEBE informarlo sin error.

**RF-09 — Notificar.**
CUANDO alguien envíe una solicitud, acepte una amistad o responda a una publicación, EL SISTEMA DEBE encolar un aviso para la persona afectada: el destinatario de la solicitud, quien envió la solicitud aceptada, o el autor de la publicación (también cuando la respuesta es a una respuesta de ese hilo).
SI quien responde es el autor de la publicación, ENTONCES EL SISTEMA NO DEBE generar aviso.

**RF-10 — Leer notificaciones.**
CUANDO la persona lea sus notificaciones, EL SISTEMA DEBE mostrar todas las pendientes en el orden en que llegaron y dejar la cola vacía.
SI no hay pendientes, ENTONCES EL SISTEMA DEBE informar «sin notificaciones».

## 3. Criterios de aceptación
| ID | Criterio (de [`historias.md`](../00-producto/historias.md)) | Prueba esperada |
|---|---|---|
| CA-05 | Enviar una solicitud la deja pendiente en la cola del destinatario; no se permite enviarla a uno mismo, a un amigo ni repetida. | `tests/test_cola.py` |
| CA-07 | Las solicitudes se atienden en el orden en que llegaron; sin solicitudes pendientes se informa sin error. | `tests/test_cola.py` |
| CA-32 | Las notificaciones se leen en el mismo orden en que llegaron. | `tests/test_cola.py` |
| CA-33 | Leer notificaciones sin pendientes informa «sin notificaciones» y no falla. | `tests/test_cola.py` |

## 4. Casos extremos
- Cola vacía: desencolar y consultar el frente avisan sin fallar; el tamaño sigue en 0 (CA-07, CA-33).
- Un solo elemento: desencolarlo deja la cola vacía y una nueva inserción vuelve a quedar al frente.
- Encolar X, Y, Z y desencolar tres veces devuelve X, Y, Z (CA-07, CA-32).
- Vaciar la cola y volver a encolar: el orden se respeta.
- Solicitud a uno mismo, a un amigo o repetida: se rechaza y la cola no cambia (CA-05).
- A le envió solicitud a B y, con esa pendiente, B intenta enviársela a A: se rechaza y se le indica que revise sus solicitudes (CA-05).
- Solicitud a un `@usuario` que no existe: se rechaza y ninguna cola cambia (CA-05).
- Dos personas distintas envían solicitud al mismo destinatario: ambas quedan, en orden de llegada.
- Leer notificaciones dos veces seguidas: la segunda vez informa «sin notificaciones».
- El autor responde en su propia publicación: no recibe aviso.
- Otra persona responde a una respuesta dentro del hilo: el aviso va al autor de la publicación, no al de la respuesta.
- Aceptar la solicitud genera un aviso para quien la envió; rechazarla no genera ninguno.

## 5. Fuera de alcance
- Aceptar o rechazar una solicitud que no esté al frente.
- Aviso de respuesta aceptada (pertenece a HU-08, Should; si se implementa, usa la misma cola).

## Historial de cambios
| Versión | Fecha | Cambio | Motivo |
|---|---|---|---|
| 1.0 | 2026-11-07 | Versión inicial | Creación |
| 1.1 | 2026-11-07 | Se reescribe con requisitos CUANDO/EL SISTEMA DEBE; criterios CA-05, CA-07, CA-32, CA-33 (antes CA-15, CA-16); CA-06 pasa al grafo; se agregan «contiene», atender solo la primera solicitud, leer todas las notificaciones y a quién se avisa (solo al autor de la publicación; sin aviso si responde el propio autor) | La numeración de las historias cambió; cada CA debe tener un solo dueño; decisiones tomadas en la consulta del componente y en la del sistema |
| 1.2 | 2026-11-08 | RF-07: se rechaza también la solicitud cruzada; casos extremos de solicitud cruzada y destinatario inexistente | La spec no decía qué pasa si los dos se envían solicitud; decisión de Valentina al integrar las amistades |
