# Spec — Montículo máximo (destacada y recomendaciones)
Versión 1.0 · Estado: aprobada para implementar

## 1. Contexto y objetivo
Dos cosas de InsightHub necesitan «el mayor primero» sin ordenar todo cada vez:
- la **publicación destacada**, la de mayor actividad de la plaza (HU-09, Should);
- las **recomendaciones de contactos**, ordenadas por amigos en común (HU-13, Must).

Historias: **HU-13** (Must) y **HU-09** (Should). Criterios Must: **CA-35**. Criterios Should: **CA-24, CA-25, CA-26**.
Los candidatos a recomendar y su número de amigos en común los entrega el grafo ([`06-grafo`](../06-grafo/spec.md)); este componente solo los ordena.

## 2. Operaciones públicas y comportamiento

### Recomendaciones (Must)
**RF-01 — Ordenar recomendaciones.**
CUANDO se pidan recomendaciones, EL SISTEMA DEBE entregar hasta 5 personas, de las que tienen más amigos en común a las que tienen menos; si dos empatan, primero la de `@usuario` alfabéticamente menor.
SI hay menos de 5 candidatos, ENTONCES EL SISTEMA DEBE entregar todos; SI no hay ninguno, ENTONCES EL SISTEMA DEBE entregar una lista vacía sin error.

**RF-02 — Consultar sin alterar.**
CUANDO se pidan recomendaciones, EL SISTEMA NO DEBE modificar a los candidatos ni a la red de amistades.

### Publicación destacada (Should)
**RF-03 — Medir la actividad.**
CUANDO se publique una pregunta, EL SISTEMA DEBE registrarla con actividad 0.
CUANDO alguien responda a una publicación, EL SISTEMA DEBE sumar 1 a su actividad.
CUANDO alguien vote una respuesta de su hilo, EL SISTEMA DEBE sumar 1; CUANDO retire ese voto, restar 1. Cambiar un voto no cambia la actividad.

**RF-04 — Consultar la destacada.**
CUANDO se pida la destacada, EL SISTEMA DEBE devolver la publicación de mayor actividad; si dos empatan, la más reciente.
SI no hay publicaciones, ENTONCES EL SISTEMA DEBE informar que no hay destacada sin error.

**RF-05 — Reacomodar al cambiar la actividad.**
CUANDO cambie la actividad de cualquier publicación, EL SISTEMA DEBE dejar como destacada a la que corresponda según RF-04: si otra supera (o empata siendo más reciente) a la destacada, pasa a ser la destacada; si la destacada pierde actividad, puede dejar de serlo.

**RF-06 — Consultar sin alterar.**
CUANDO se pida la destacada, EL SISTEMA NO DEBE modificar la actividad de ninguna publicación.

## 3. Criterios de aceptación
| ID | Criterio (de [`historias.md`](../00-producto/historias.md)) | Prioridad | Prueba esperada |
|---|---|---|---|
| CA-35 | Las recomendaciones se ordenan por número de amigos en común, de mayor a menor. | Must | `tests/test_monticulo.py` |
| CA-24 | La publicación destacada es la de mayor actividad (respuestas y votos). | Should | `tests/test_monticulo.py` |
| CA-25 | Cuando cambia la actividad de otra publicación y supera a la destacada, la destacada se actualiza. | Should | `tests/test_monticulo.py` |
| CA-26 | Sin publicaciones, no hay destacada y no se produce error. | Should | `tests/test_monticulo.py` |

## 4. Casos extremos
**Recomendaciones (CA-35)**
- Sin candidatos: lista vacía.
- Un solo candidato: se entrega.
- Exactamente 5 candidatos: se entregan los 5; con 6 se entregan solo los 5 mejores.
- Todos con los mismos amigos en común: salen en orden alfabético de `@usuario`.
- Candidato con muchos amigos en común (por ejemplo 50) frente a otros con 1: va primero.
- Los candidatos no cambian después de pedir las recomendaciones, y pedirlas dos veces da lo mismo.

**Destacada (CA-24, CA-25, CA-26)**
- Sin publicaciones: no hay destacada, sin error (CA-26).
- Una sola publicación, aun con actividad 0: es la destacada.
- Todas con la misma actividad: la más reciente es la destacada.
- Otra publicación supera a la destacada: pasa a ser la destacada (CA-25).
- Otra publicación empata con la destacada y es más reciente: pasa a ser la destacada; si es más antigua, no (CA-24).
- La destacada pierde actividad por un voto retirado y otra queda por encima: cambia (CA-25).
- Cambiar un voto de a favor a en contra: la actividad no cambia (CA-24).
- Una publicación sin respuestas nunca supera a una con respuestas (CA-24).
- Consultar la destacada varias veces seguidas: siempre la misma y sin cambios (RF-06).

## 5. Fuera de alcance
- Destacada por tiempo (que la actividad «caduque» con los días).
- Lista de las N publicaciones más activas (solo la primera).
- Más de 5 recomendaciones.
- Cálculo de los amigos en común (grafo).

## Historial de cambios
| Versión | Fecha | Cambio | Motivo |
|---|---|---|---|
| 1.0 | 2026-11-07 | Versión inicial (la carpeta estaba vacía) | Faltaban spec, plan y tasks del montículo; criterios CA-35, CA-24, CA-25, CA-26; actividad = respuestas + votos vigentes; empate a favor de la más reciente; 5 recomendaciones con desempate alfabético; decisiones tomadas en la consulta del componente |
