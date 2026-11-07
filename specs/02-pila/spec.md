# Spec — Pila
Versión 1.1 · Estado: aprobada para implementar

## 1. Contexto y objetivo
InsightHub necesita un botón «atrás» que regrese a la última pantalla visitada (HU-11). La pila guarda el historial de pantallas y entrega siempre la más reciente. El mismo componente lo usa también el árbol general para mostrar un hilo ([`04-arbol-general`](../04-arbol-general/spec.md)); ese uso no tiene criterio propio aquí.

Historia que atiende: **HU-11** (Must). Criterios: **CA-30, CA-31**.

## 2. Operaciones públicas y comportamiento

**RF-01 — Apilar.**
CUANDO se apile un elemento, EL SISTEMA DEBE dejarlo como el más reciente y aumentar el tamaño en uno.

**RF-02 — Desapilar.**
CUANDO se desapile y haya elementos, EL SISTEMA DEBE devolver el más reciente, quitarlo y disminuir el tamaño en uno.

**RF-03 — Consultar el tope.**
CUANDO se consulte el tope y haya elementos, EL SISTEMA DEBE devolver el más reciente sin quitarlo.

**RF-04 — Pila vacía.**
SI se desapila o se consulta el tope con la pila vacía, ENTONCES EL SISTEMA DEBE avisar la condición de pila vacía de forma controlada, sin modificar la pila.

**RF-05 — Estado.**
CUANDO se pregunte si está vacía o por su tamaño, EL SISTEMA DEBE responder sin modificar la pila.

**RF-06 — Navegación «atrás».**
CUANDO la persona abra una pantalla distinta de la actual, EL SISTEMA DEBE guardar la actual en el historial; SI la pantalla nueva es igual a la actual, ENTONCES EL SISTEMA NO DEBE guardarla otra vez.
CUANDO la persona pulse «atrás», EL SISTEMA DEBE llevarla a la pantalla guardada más reciente.

El historial no tiene tamaño máximo.

## 3. Criterios de aceptación
| ID | Criterio (de [`historias.md`](../00-producto/historias.md)) | Prueba esperada |
|---|---|---|
| CA-30 | «Atrás» regresa a la pantalla visitada inmediatamente antes; repetirlo retrocede en orden inverso. | `tests/test_pila.py` |
| CA-31 | «Atrás» con historial vacío informa que no hay pantalla previa y no falla. | `tests/test_pila.py` |

## 4. Casos extremos
- Pila vacía: desapilar y consultar el tope avisan sin fallar; el tamaño sigue en 0 (CA-31).
- Un solo elemento: desapilarlo deja la pila vacía; un segundo «atrás» informa que no hay pantalla previa.
- Apilar A, B, C y desapilar tres veces devuelve C, B, A (CA-30).
- Elementos repetidos no consecutivos (A, B, A): se guardan los tres y «atrás» los devuelve en orden inverso.
- Misma pantalla dos veces seguidas: el historial no crece.
- Consultar el tope dos veces seguidas devuelve lo mismo y no cambia el tamaño.

## 5. Fuera de alcance
- Botón «adelante».
- Guardar el historial entre sesiones.

## Historial de cambios
| Versión | Fecha | Cambio | Motivo |
|---|---|---|---|
| 1.0 | 2026-11-07 | Versión inicial | Creación |
| 1.1 | 2026-11-07 | Se reescribe con requisitos CUANDO/EL SISTEMA DEBE; se corrige la numeración a CA-30 y CA-31 (antes CA-13 y CA-14); se agregan casos extremos concretos, la regla de pantallas repetidas, historial sin límite y el uso desde el árbol general | La numeración v1.1 de las historias cambió y la spec no tenía comportamiento ni extremos concretos; decisiones tomadas en la consulta del componente |
