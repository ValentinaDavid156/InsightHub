# Constitución del proyecto InsightHub

Principios que rigen todas las decisiones. Versión 1.0.

## Principios
1. **La especificación va primero.** Ningún código se escribe sin un `spec.md` con criterios CA verificables. El historial de Git debe mostrarlo.
2. **Lo implemento yo, desde cero.** Cada estructura declarada es propia. No uso `list`, `dict`, `set`, `deque` ni `heapq` como sustituto de una estructura declarada. Solo como soporte interno, justificado en el `plan.md` del componente.
3. **Toda decisión se justifica con complejidad.** Operación dominante, alternativa descartada y lugar de uso.
4. **La spec dice qué, no cómo.** El `spec.md` describe comportamiento; el `plan.md` describe estructura y complejidad.
5. **Trazabilidad total.** Cada CA tiene identificador y una prueba que lo cita; cada función nace de un CA.
6. **Casos extremos explícitos.** Vacío, un elemento, elemento inexistente, duplicados.
7. **Integración continua con el dominio.** Cada estructura entra al sistema cuando se termina.
8. **Honestidad con la IA.** Uso de IA declarado en `BITACORA.md`. No integro código que no pueda explicar línea por línea.
9. **Reproducibilidad.** Datos sintéticos con semilla fija (`SEMILLA = 706132`).

## Restricciones técnicas
Python 3.11+, solo `pytest` (y opcionalmente `matplotlib`). Un módulo por estructura. Docstrings con la complejidad de cada operación pública. Mínimo 3 pruebas por operación pública.

## Convenciones
- Commits: `spec(...)`, `plan(...)`, `test(...)`, `feat(...)`, `fix(...)`.
- Un commit por tarea de `tasks.md`.
- Etiquetas: `entrega-1`, `entrega-2`, `entrega-final`.
- Cambios de spec/plan: línea en su historial de cambios, con motivo.

## Historial de cambios
| Versión | Fecha | Cambio | Motivo |
|---|---|---|---|
| 1.0 | 2026-11-07 | Versión inicial | Creación del proyecto |
