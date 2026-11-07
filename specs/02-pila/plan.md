# Plan — Pila
Versión 1.0

## Estructura elegida
Lista enlazada simple con referencia al tope; apilar y desapilar operan sobre la cabeza.

Decisión completa y alternativa descartada: ver `specs/00-producto/estructuras.md`.

## Módulo
`estructuras/pila.py` · Pruebas: `tests/test_pila.py`

## Complejidad de las operaciones
| Operación | Complejidad |
|---|---|
| `apilar` | O(1) |
| `desapilar` | O(1) |
| `tope` | O(1) |
| `esta_vacia` | O(1) |
| `tamano` | O(1) con contador |

## Soporte interno
Ninguno, salvo lo declarado en `estructuras.md`.

## Historial de cambios
| Versión | Fecha | Cambio | Motivo |
|---|---|---|---|
| 1.0 | 2026-11-07 | Versión inicial | Creación |
