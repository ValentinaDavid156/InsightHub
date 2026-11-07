# Plan — Cola enlazada
Versión 1.0

## Estructura elegida
Lista enlazada con referencias a frente y final.

Decisión completa y alternativa descartada: ver `specs/00-producto/estructuras.md`.

## Módulo
`estructuras/cola.py` · Pruebas: `tests/test_cola.py`

## Complejidad de las operaciones
| Operación | Complejidad |
|---|---|
| `encolar` | O(1) |
| `desencolar` | O(1) |
| `frente` | O(1) |
| `esta_vacia` | O(1) |
| `tamano` | O(1) con contador |

## Soporte interno
Ninguno, salvo lo declarado en `estructuras.md`.

## Historial de cambios
| Versión | Fecha | Cambio | Motivo |
|---|---|---|---|
| 1.0 | 2026-11-07 | Versión inicial | Creación |
