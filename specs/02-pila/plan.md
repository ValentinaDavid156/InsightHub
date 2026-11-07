# Plan — Pila
Versión 1.1

## 1. De qué implementación mía parto
De **`Semana10/pila.py`** (`PilaEnlazada` sobre `Nodo`, con `PilaVaciaError(IndexError)`). Qué cambia para InsightHub:
- Se mueve a `estructuras/pila.py` y usa el `Nodo` del proyecto.
- `tamaño()` pasa a `tamano()` para evitar la ñ en nombres de métodos (se conserva `__len__`).
- Se agregan docstrings con la complejidad de cada operación (Constitución, restricciones técnicas).
- La regla de «no apilar la pantalla repetida» **no** va en la pila: va en `dominio/navegacion.py`, que es quien conoce las pantallas. Así la pila sigue siendo genérica y la puede reutilizar el árbol general.

## 2. Estructura elegida y por qué
**Pila enlazada**: lista enlazada simple con referencia al tope y un contador de tamaño. Apilar y desapilar operan sobre la cabeza.

«Atrás» siempre necesita la última pantalla visitada: es exactamente LIFO. Con la cabeza como tope, ninguna operación recorre la cadena.

## 3. Complejidad por operación
| Operación | Complejidad | Por qué |
|---|---|---|
| `apilar(dato)` | O(1) | Crea un nodo que apunta a la cabeza actual |
| `desapilar()` | O(1) | Mueve la cabeza al siguiente |
| `tope()` | O(1) | Lee la cabeza |
| `esta_vacia()` | O(1) | Compara la cabeza con `None` |
| `tamano()` / `len()` | O(1) | Contador que se actualiza al apilar y desapilar |

Memoria: O(n) con n = pantallas visitadas en la sesión. Sin límite, porque una sesión de consola o web no visita miles de pantallas.

## 4. Alternativa descartada
| Alternativa | Por qué no |
|---|---|
| `list` de Python con `append`/`pop` | También O(1) amortizado, pero sería usar una estructura nativa como sustituto de la declarada (Constitución, principio 2) |
| Lista doble con cursor | Solo se justificaría con «adelante», que está fuera de alcance; duplica punteros sin ganancia |
| Historial con tope de 50 | Borrar el más viejo exige llegar al fondo de la pila, O(n), o una segunda estructura; no hace falta con datos en memoria |

## 5. Pila vacía
`desapilar()` y `tope()` lanzan `PilaVaciaError` y no modifican nada (igual que en Semana10). `dominio/navegacion.py` captura el error y muestra «no hay pantalla previa» (CA-31). Así se distingue «no hay nada» de «se apiló un `None`».

## 6. Soporte interno
Ninguno. Solo nodos propios.

## 7. Módulos
`estructuras/pila.py` · `dominio/navegacion.py` · pruebas en `tests/test_pila.py`.

## Historial de cambios
| Versión | Fecha | Cambio | Motivo |
|---|---|---|---|
| 1.0 | 2026-11-07 | Versión inicial | Creación |
| 1.1 | 2026-11-07 | Se declara el punto de partida (Semana10), el porqué de cada decisión, alternativas descartadas, el manejo de pila vacía y la separación pila / navegación | El plan no decía de qué implementación partía ni justificaba las decisiones; decisiones tomadas en la consulta del componente |
