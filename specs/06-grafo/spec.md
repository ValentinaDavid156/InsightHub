# Spec — Grafo dirigido (seguimientos)
Versión 1.0 · Estado: borrador de contrato

## Qué debe hacer (sin decir cómo)
Componente que sirve a: CA-03, CA-04, CA-17, CA-18, CA-19.

## Operaciones públicas
- `agregar_vertice(id)`
- `agregar_arista(origen, destino)`
- `eliminar_arista(origen, destino)`
- `existe_arista(origen, destino)`
- `vecinos(id)`
- `bfs_hasta_nivel(origen, niveles)`

## Criterios de aceptación
- **CA-03:** `agregar_arista` rechaza duplicados y autoaristas.
- **CA-04:** `eliminar_arista` de una arista inexistente no falla.
- **CA-17:** `bfs_hasta_nivel(u, 2)` entrega los vértices a 2 saltos sin repetir ni incluir a `u` ni a sus vecinos directos en la lista de candidatos.
- **CA-18:** Para cada candidato se puede obtener su número de contactos en común.
- **CA-19:** Un vértice sin vecinos produce candidatos vacíos.

## Casos extremos que debe cubrir
Estructura vacía · un solo elemento · elemento inexistente · duplicados (si aplica).

## Historial de cambios
| Versión | Fecha | Cambio | Motivo |
|---|---|---|---|
| 1.0 | 2026-11-07 | Versión inicial | Creación |
