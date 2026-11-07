# Plan — Lista doble
Versión 1.0

## Estructura elegida
Dos referencias (cabeza y cola) y un cursor `actual`; cada nodo guarda `anterior` y `siguiente`.

Decisión completa y alternativa descartada: ver `specs/00-producto/estructuras.md`.

## Módulo
`estructuras/lista_doble.py` · Pruebas: `tests/test_lista_doble.py`

## Complejidad de las operaciones
| Operación | Complejidad |
|---|---|
| `insertar_al_frente` | O(1) |
| `insertar_al_final` | O(1) |
| `actual` | O(1) |
| `avanzar` | O(1) |
| `retroceder` | O(1) |
| `ir_al_inicio` | O(1) |
| `esta_vacia` | O(1) |
| `tamano` | O(1) con contador |

## Soporte interno
Ninguno, salvo lo declarado en `estructuras.md`.

## Historial de cambios
| Versión | Fecha | Cambio | Motivo |
|---|---|---|---|
| 1.0 | 2026-11-07 | Versión inicial | Creación |
