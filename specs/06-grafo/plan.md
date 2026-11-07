# Plan — Grafo dirigido (seguimientos)
Versión 1.0

## Estructura elegida
Lista de adyacencia con nodos enlazados por vértice; BFS con la cola del curso y marcado de visitados.

Decisión completa y alternativa descartada: ver `specs/00-producto/estructuras.md`.

## Módulo
`estructuras/grafo.py` · Pruebas: `tests/test_grafo.py`

## Complejidad de las operaciones
| Operación | Complejidad |
|---|---|
| `agregar_vertice` | O(1) |
| `agregar_arista` | O(grado) por verificación de duplicado |
| `eliminar_arista` | O(grado) |
| `existe_arista` | O(grado) |
| `vecinos` | O(grado) |
| `bfs_hasta_nivel` | O(V + E) acotado a la vecindad |

## Soporte interno
Ninguno, salvo lo declarado en `estructuras.md`.

## Historial de cambios
| Versión | Fecha | Cambio | Motivo |
|---|---|---|---|
| 1.0 | 2026-11-07 | Versión inicial | Creación |
