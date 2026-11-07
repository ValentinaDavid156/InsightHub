# Spec — Pila
Versión 1.0 · Estado: borrador de contrato

## Qué debe hacer (sin decir cómo)
Componente que sirve a: CA-13, CA-14.

## Operaciones públicas
- `apilar(dato)`
- `desapilar()`
- `tope()`
- `esta_vacia()`
- `tamano()`

## Criterios de aceptación
- **CA-13:** Apilar A, B, C y desapilar tres veces devuelve C, B, A.
- **CA-14:** `desapilar()` en pila vacía informa la condición sin lanzar una excepción no controlada.

## Casos extremos que debe cubrir
Estructura vacía · un solo elemento · elemento inexistente · duplicados (si aplica).

## Historial de cambios
| Versión | Fecha | Cambio | Motivo |
|---|---|---|---|
| 1.0 | 2026-11-07 | Versión inicial | Creación |
