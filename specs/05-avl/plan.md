# Plan — Árbol AVL (índice de usuarios)
Versión 1.0

## Estructura elegida
Nodos con altura y rotaciones simples y dobles tras cada inserción; las claves se comparan como texto en minúsculas.

Decisión completa y alternativa descartada: ver `specs/00-producto/estructuras.md`.

## Módulo
`estructuras/avl.py` · Pruebas: `tests/test_avl.py`

## Complejidad de las operaciones
| Operación | Complejidad |
|---|---|
| `insertar` | O(log n) |
| `buscar` | O(log n) |
| `buscar_por_prefijo` | O(log n + k), k = coincidencias |
| `recorrer_en_orden` | O(n) |
| `altura` | O(1) |
| `tamano` | O(1) con contador |

## Soporte interno
Ninguno, salvo lo declarado en `estructuras.md`.

## Historial de cambios
| Versión | Fecha | Cambio | Motivo |
|---|---|---|---|
| 1.0 | 2026-11-07 | Versión inicial | Creación |
