# Spec — Árbol general (hilos)
Versión 1.0 · Estado: borrador de contrato

## Qué debe hacer (sin decir cómo)
Componente que sirve a: CA-07, CA-08, CA-09.

## Operaciones públicas
- `agregar_hijo(id_padre, id_nuevo, dato)`
- `buscar(id)`
- `recorrer_preorden()`
- `profundidad(id)`
- `tamano()`

## Criterios de aceptación
- **CA-07:** Agregar un hijo a la raíz lo deja como respuesta de primer nivel.
- **CA-08:** Se pueden anidar al menos 3 niveles y `recorrer_preorden()` devuelve cada nodo con su nivel.
- **CA-09:** `agregar_hijo` con padre inexistente devuelve fallo y no altera el árbol.

## Casos extremos que debe cubrir
Estructura vacía · un solo elemento · elemento inexistente · duplicados (si aplica).

## Historial de cambios
| Versión | Fecha | Cambio | Motivo |
|---|---|---|---|
| 1.0 | 2026-11-07 | Versión inicial | Creación |
