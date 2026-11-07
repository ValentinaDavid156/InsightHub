# Spec — Árbol AVL (índice de usuarios)
Versión 1.0 · Estado: borrador de contrato

## Qué debe hacer (sin decir cómo)
Componente que sirve a: CA-10, CA-11, CA-12.

## Operaciones públicas
- `insertar(clave, valor)`
- `buscar(clave)`
- `buscar_por_prefijo(prefijo)`
- `recorrer_en_orden()`
- `altura()`
- `tamano()`

## Criterios de aceptación
- **CA-10:** `buscar_por_prefijo` devuelve las coincidencias en orden alfabético.
- **CA-11:** Un prefijo sin coincidencias devuelve vacío.
- **CA-12:** Insertar claves en orden creciente mantiene altura ≤ 1.44·log2(n+2).

## Casos extremos que debe cubrir
Estructura vacía · un solo elemento · elemento inexistente · duplicados (si aplica).

## Historial de cambios
| Versión | Fecha | Cambio | Motivo |
|---|---|---|---|
| 1.0 | 2026-11-07 | Versión inicial | Creación |
