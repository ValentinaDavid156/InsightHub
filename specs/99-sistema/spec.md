# Spec del sistema — InsightHub
Versión inicial 0.1

## Qué hace el sistema
InsightHub es el núcleo lógico, usado desde consola, de una red social de preguntas y respuestas. Los miembros se siguen, publican preguntas, responden en hilos anidados, buscan, navegan con «atrás», reciben notificaciones y obtienen recomendaciones de contactos.

## Componentes y contratos
| Componente | Estructura | Sirve a | Lo consume |
|---|---|---|---|
| Feed | Lista doble | HU-03 | `dominio/feed.py` |
| Historial | Pila | HU-06 | `dominio/navegacion.py` |
| Notificaciones | Cola | HU-07 | `dominio/notificaciones.py` |
| Hilos | Árbol general | HU-04 | `dominio/hilos.py` |
| Índice de usuarios | AVL | HU-01, HU-05 | `dominio/usuarios.py` |
| Red | Grafo | HU-02, HU-08 | `dominio/red.py`, `dominio/recomendaciones.py` |

## Cómo encajan
- Seguir a alguien (grafo) genera una notificación (cola).
- Responder en un hilo (árbol) genera una notificación al autor del comentario padre (cola).
- Cada pantalla visitada en la consola se apila (pila).
- Las recomendaciones leen el grafo; la búsqueda lee el AVL.

## Historial de cambios
| Versión | Fecha | Cambio | Motivo |
|---|---|---|---|
| 0.1 | 2026-11-07 | Versión inicial | Entrega 1 |
