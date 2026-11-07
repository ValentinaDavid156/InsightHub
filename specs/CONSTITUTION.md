# Constitución del proyecto InsightHub

Reglas que rigen todas las decisiones del proyecto. Versión 1.2.

## Alcance
InsightHub es una plataforma **100 % pública y colaborativa** de preguntas y respuestas: debate transparente e intercambio de conocimiento. **No hay chats ni mensajes privados.**
Se usa desde **consola** (prioridad Must) y desde un **sitio web** servido con la librería estándar de Python (prioridad Should; ver [`00-producto/moscow.md`](00-producto/moscow.md)).

## Principios
1. **La especificación va primero.** Ningún código se escribe sin un `spec.md` con criterios CA verificables. El historial de Git debe mostrarlo.
2. **Lo implemento yo, desde cero.** Cada estructura declarada es propia. No uso `list`, `dict`, `set`, `deque` ni `heapq` como sustituto de una estructura declarada; solo como soporte interno, justificado en el `plan.md` del componente.
3. **Toda decisión se justifica con complejidad:** operación dominante, alternativa descartada y lugar de uso.
4. **La spec dice qué, no cómo.** El `spec.md` describe comportamiento; el `plan.md` describe estructura y complejidad.
5. **Trazabilidad total.** Cada CA tiene identificador y una prueba que lo cita; cada función nace de un CA (ver [`trazabilidad.md`](trazabilidad.md)).
6. **Casos extremos explícitos:** vacío, un elemento, elemento inexistente, duplicados.
7. **Integración continua con el dominio.** Cada estructura entra al sistema cuando se termina.
8. **Honestidad con la IA.** El uso de IA se declara en `BITACORA.md`. No integro código que no pueda explicar línea por línea.
9. **Reproducibilidad.** Los datos sintéticos usan semilla fija (`SEMILLA = 706132`).
10. **Todo es público.** Ninguna función crea conversaciones privadas.

## Decisiones técnicas
| Tema | Decisión | Motivo |
|---|---|---|
| Lenguaje y librerías | Python 3.11+; solo `pytest` (y opcionalmente `matplotlib`) | Lo exige el enunciado |
| Interfaz | Consola (Must) + sitio web con `http.server` de la librería estándar (Should) | Permite ver la plataforma sin dependencias externas; la consola basta para cumplir |
| Acceso | Con `@usuario`, sin contraseña | Registro simplificado; el proyecto evalúa estructuras, no seguridad |
| Datos | Solo en memoria; datos de demostración con semilla fija | Es lo más simple; evita trabajo de persistencia fuera del objetivo del curso |
| Presencia | Tras 30 s sin actividad la persona figura desconectada, en consola y en web | Una sola regla para ambas interfaces |
| Sondeo del navegador (solo si se hace la web) | El navegador consulta al servidor cada ~5 s presencia y notificaciones | Es la opción más simple y no necesita conexiones abiertas |

## Restricciones técnicas
Un módulo por estructura. Docstrings con la complejidad de cada operación pública. Mínimo 3 pruebas por operación pública, incluidos los extremos; en `tasks.md` cada tarea de criterio agrupa esas pruebas.

## Convenciones
- Commits: `spec(...)`, `plan(...)`, `test(...)`, `feat(...)`, `fix(...)`, `refactor(...)`, `docs(...)`.
- Un commit por tarea de implementación de `tasks.md` (prueba o código). Los documentos de spec, plan y tasks pueden agruparse en un mismo commit.
- Etiqueta: `entrega-final` (antes del 11 de nov de 2026, 23:59).
- Todo cambio de spec o plan deja una línea en su historial de cambios, con el motivo.

## Historial de cambios
| Versión | Fecha | Cambio | Motivo |
|---|---|---|---|
| 1.0 | 2026-11-07 | Versión inicial | Creación del proyecto |
| 1.1 | 2026-11-07 | Agrega alcance, principio 10 y tabla de decisiones técnicas (interfaz consola + web, datos en memoria, sondeo cada ~5 s) | La idea del proyecto pasó a incluir interfaz web y presencia |
| 1.2 | 2026-11-07 | Quita las etiquetas `entrega-1` y `entrega-2`; separa la regla de presencia (30 s, ambas interfaces) del sondeo (solo web); agrega `refactor` y `docs` a los commits; aclara que «un commit por tarea» rige la implementación y que las 3 pruebas por operación se agrupan por criterio; corrige la ruta a `00-producto/` | Las entregas 1 y 2 vencieron; la web pasó a Should; las carpetas se renombraron; había choques con el plan de commits y con las tareas por criterio |
