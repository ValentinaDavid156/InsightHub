# Spec — Cola enlazada
Versión 1.0 · Estado: borrador de contrato

## Qué debe hacer (sin decir cómo)
Componente que sirve a: CA-15, CA-16.

## Operaciones públicas
- `encolar(dato)`
- `desencolar()`
- `frente()`
- `esta_vacia()`
- `tamano()`

## Criterios de aceptación
- **CA-15:** Encolar X, Y, Z y desencolar tres veces devuelve X, Y, Z.
- **CA-16:** `desencolar()` en cola vacía informa la condición sin fallar.

## Casos extremos que debe cubrir
Estructura vacía · un solo elemento · elemento inexistente · duplicados (si aplica).

## Historial de cambios
| Versión | Fecha | Cambio | Motivo |
|---|---|---|---|
| 1.0 | 2026-11-07 | Versión inicial | Creación |
