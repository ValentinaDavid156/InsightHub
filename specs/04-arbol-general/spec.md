# Spec — Árbol general (hilos de respuestas)
Versión 1.1 · Estado: aprobada para implementar

## 1. Contexto y objetivo
Cada publicación abre un hilo: las personas responden a la publicación o a otra respuesta, y cada respuesta puede tener a su vez más respuestas (HU-06). Hay un hilo por publicación. En el hilo también se fija la mejor respuesta (HU-08, Should).

Historias: **HU-06** (Must) y **HU-08** (Should). Criterios: **CA-14, CA-15, CA-16** (Must) y **CA-22, CA-23** (Should).

## 2. Operaciones públicas y comportamiento

**RF-01 — Abrir un hilo.**
CUANDO se publique una pregunta, EL SISTEMA DEBE abrir un hilo cuyo punto de partida es esa publicación, sin respuestas.

**RF-02 — Responder a la publicación.**
CUANDO alguien responda a la publicación, EL SISTEMA DEBE agregar su respuesta como respuesta de primer nivel, después de las que ya existían en ese nivel.

**RF-03 — Responder a una respuesta.**
CUANDO alguien responda a una respuesta existente, EL SISTEMA DEBE agregarla un nivel más abajo de aquella a la que responde, después de las respuestas que esa ya tenía. La profundidad no tiene un máximo.

**RF-04 — Padre inexistente.**
SI se responde a una publicación o respuesta que no existe en el hilo, ENTONCES EL SISTEMA DEBE rechazar la respuesta con un mensaje claro, sin alterar el hilo.

**RF-05 — Identificador repetido.**
SI se intenta agregar una respuesta con un identificador que ya existe en el hilo, ENTONCES EL SISTEMA DEBE rechazarla sin alterar el hilo.

**RF-06 — Mostrar el hilo.**
CUANDO se pida ver el hilo, EL SISTEMA DEBE mostrar la publicación y todas sus respuestas, cada una debajo de aquella a la que responde, con su nivel (para la sangría) y en orden cronológico dentro de cada nivel.

**RF-07 — Buscar y medir.**
CUANDO se pregunte por una respuesta por su identificador, EL SISTEMA DEBE decir si existe y a qué nivel está.
CUANDO se pregunte por el tamaño, EL SISTEMA DEBE devolver el número de elementos del hilo, contando la publicación.

**RF-08 — Aceptar la mejor respuesta (Should).**
CUANDO quien hizo la pregunta acepte una respuesta de primer nivel, EL SISTEMA DEBE fijarla arriba del hilo y sumar 15 puntos a su autor.
SI quien acepta no es quien preguntó, la respuesta no es de primer nivel, no existe, o ya hay una aceptada, ENTONCES EL SISTEMA DEBE rechazarlo con un mensaje claro, sin cambiar el hilo ni los puntos.

**RF-09 — Mejor respuesta por puntaje (Should).**
CUANDO no haya respuesta aceptada, EL SISTEMA DEBE fijar arriba del hilo la respuesta de primer nivel con mayor puntaje neto, siempre que ese puntaje sea positivo; si dos empatan, la más antigua.
SI no hay respuestas, o ninguna tiene puntaje positivo, ENTONCES EL SISTEMA NO DEBE fijar ninguna.

**RF-10 — Mostrar con la fijada.**
CUANDO el hilo tenga una respuesta fijada, EL SISTEMA DEBE mostrarla primero entre las de su nivel, con sus respuestas debajo.

## 3. Criterios de aceptación
| ID | Criterio (de [`historias.md`](../00-producto/historias.md)) | Prioridad | Prueba esperada |
|---|---|---|---|
| CA-14 | Responder a una publicación agrega una respuesta de primer nivel. | Must | `tests/test_arbol_general.py` |
| CA-15 | Se puede responder a una respuesta hasta una profundidad de al menos 3 niveles, y el hilo se muestra completo con sangría por nivel. | Must | `tests/test_arbol_general.py` |
| CA-16 | Responder a un comentario inexistente se rechaza sin alterar el hilo. | Must | `tests/test_arbol_general.py` |
| CA-22 | La respuesta que acepta quien hizo la pregunta queda fijada arriba del hilo y suma 15 puntos a su autor; solo quien preguntó puede aceptar, y una sola vez. | Should | `tests/test_arbol_general.py` |
| CA-23 | Si no hay respuesta aceptada, queda fijada la de mayor puntaje neto, siempre que sea positivo; sin respuestas, no hay ninguna fijada. | Should | `tests/test_arbol_general.py` |

## 4. Casos extremos
- Hilo sin respuestas: se muestra solo la publicación; el tamaño es 1; no hay fijada (CA-23).
- Una sola respuesta: aparece en el nivel 1 (CA-14).
- Cadena de 3 niveles o más: cada una aparece con su nivel y debajo de su padre (CA-15).
- Varias respuestas en el mismo nivel: se muestran en orden de llegada.
- Responder a una respuesta que no existe, o a una publicación de otro hilo: rechazado, el hilo no cambia (CA-16).
- Identificador repetido: rechazado (RF-05).
- Aceptar una respuesta de segundo nivel, una inexistente, o aceptar dos veces: rechazado (CA-22).
- Aceptar siendo otra persona distinta de quien preguntó: rechazado (CA-22).
- Empate en puntaje positivo entre dos respuestas: queda la más antigua (CA-23).
- Todas con puntaje cero o negativo: ninguna fijada (CA-23).
- Respuesta aceptada con puntaje menor que otra: la aceptada manda sobre la de mayor puntaje (CA-22 frente a CA-23).

## 5. Fuera de alcance
- Borrar o editar respuestas.
- Mover una respuesta a otro padre.
- Un límite de profundidad.
- Que una réplica profunda sea mejor respuesta.
- Los avisos de «respuesta» y de «respuesta aceptada»: los entrega la cola ([`03-cola`](../03-cola/spec.md)).
- El cálculo del puntaje neto y las insignias: pertenecen a los votos ([`05-avl`](../05-avl/spec.md)).

## Historial de cambios
| Versión | Fecha | Cambio | Motivo |
|---|---|---|---|
| 1.0 | 2026-11-07 | Versión inicial | Creación |
| 1.1 | 2026-11-07 | Se reescribe con requisitos CUANDO/EL SISTEMA DEBE; criterios CA-14, CA-15, CA-16 (antes CA-07 a CA-09) y se suman CA-22 y CA-23 (mejor respuesta); un hilo por publicación, orden cronológico, solo las de primer nivel pueden ser mejor respuesta, empate a favor de la más antigua, casos extremos concretos | La numeración de las historias cambió y la mejor respuesta no estaba cubierta; decisiones tomadas en la consulta del componente |
