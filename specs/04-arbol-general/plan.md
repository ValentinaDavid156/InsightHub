# Plan — Árbol general (hilos)
Versión 1.0

## Estructura elegida
Representación hijo-izquierdo / hermano-derecho: cada nodo guarda `primer_hijo` y `siguiente_hermano`.

Decisión completa y alternativa descartada: ver `specs/00-producto/estructuras.md`.

## Módulo
`estructuras/arbol_general.py` · Pruebas: `tests/test_arbol_general.py`

## Complejidad de las operaciones
| Operación | Complejidad |
|---|---|
| `agregar_hijo` | O(n) por la búsqueda del padre |
| `buscar` | O(n) |
| `recorrer_preorden` | O(n) |
| `profundidad` | O(n) |
| `tamano` | O(1) con contador |

## Soporte interno
Ninguno, salvo lo declarado en `estructuras.md`.

## Historial de cambios
| Versión | Fecha | Cambio | Motivo |
|---|---|---|---|
| 1.0 | 2026-11-07 | Versión inicial | Creación |
