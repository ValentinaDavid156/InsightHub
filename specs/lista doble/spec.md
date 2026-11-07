# Spec — Lista doble
Versión 1.0 · Estado: borrador de contrato

## Qué debe hacer (sin decir cómo)
Componente que sirve a: CA-05, CA-06.

## Operaciones públicas
- `insertar_al_frente(dato)`
- `insertar_al_final(dato)`
- `actual()`
- `avanzar()`
- `retroceder()`
- `ir_al_inicio()`
- `esta_vacia()`
- `tamano()`

## Criterios de aceptación
- **CA-05:** Tras insertar al frente, `actual()` tras `ir_al_inicio()` devuelve el último dato insertado.
- **CA-06:** `avanzar()` en el último nodo y `retroceder()` en el primero devuelven que no hubo movimiento y no cambian la posición; en lista vacía no fallan.

## Casos extremos que debe cubrir
Estructura vacía · un solo elemento · elemento inexistente · duplicados (si aplica).

## Historial de cambios
| Versión | Fecha | Cambio | Motivo |
|---|---|---|---|
| 1.0 | 2026-11-07 | Versión inicial | Creación |
