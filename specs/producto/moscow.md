# Priorización MoSCoW y capacidad

## Cálculo de capacidad (AJUSTA estas cifras a tu tiempo real)
- Horas disponibles estimadas para implementar: **35 h**
- Colchón para imprevistos, informe y sustentación (20 %): **−7 h**
- **Capacidad neta: 28 h**

## Must (obligatorios del enunciado) — 22 h
| Historia | Estructura | Estimación |
|---|---|---|
| HU-01 Usuarios sintéticos | AVL (índice) | 2 h |
| HU-02 Seguir / dejar de seguir | Grafo | 3 h |
| HU-03 Publicar y feed | Lista doble | 3 h |
| HU-04 Hilos anidados | Árbol general | 4 h |
| HU-05 Búsqueda | AVL | 4 h |
| HU-06 Atrás | Pila | 1.5 h |
| HU-07 Notificaciones | Cola | 1.5 h |
| HU-08 Recomendaciones | Grafo + BFS | 3 h |
**Total Must: 22 h ≤ 28 h → caben.**

## Should — 6 h (entran si sobra capacidad)
- HU-09 Calificar aportes (votos y ranking de respuestas).

## Could — 3 h
- Categorías/etiquetas de preguntas.

## Won't (esta vez)
| Elemento | Razón |
|---|---|
| Cadena de conexión con A* | Opcional en la temática y la capacidad restante se reserva a pruebas y análisis. |
| Interfaz gráfica / web | El enunciado pide consola; la interfaz no aporta a la decisión de estructuras. |
| Persistencia en base de datos | Fuera del alcance del curso; los datos viven en memoria. |

## Historial de cambios
| Versión | Fecha | Cambio | Motivo |
|---|---|---|---|
| 1.0 | 2026-11-07 | Priorización inicial | Creación |
