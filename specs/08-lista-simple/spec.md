# Spec — Lista simple (personas conectadas)
Versión 1.0 · Estado: aprobada para implementar

## 1. Contexto y objetivo
Para interactuar con quien está activo, cada miembro necesita saber quién está conectado (HU-04): al entrar, una persona figura conectada; al salir, o si pasan 30 segundos sin que haga nada, deja de figurar. También se ve el estado de cada amigo.

Historia: **HU-04** (Should). Criterios: **CA-09, CA-10, CA-11**.
Quiénes son los amigos de una persona lo da el grafo ([`06-grafo`](../06-grafo/spec.md)); este componente solo responde si cada una está conectada.

## 2. Operaciones públicas y comportamiento
La hora la entrega quien llama (en segundos), de modo que el comportamiento se puede probar sin esperar tiempo real.

**RF-01 — Conectar.**
CUANDO una persona entre, EL SISTEMA DEBE hacerla figurar como conectada con la hora de entrada.
SI ya figuraba conectada, ENTONCES EL SISTEMA NO DEBE repetirla; solo renueva su hora de actividad.

**RF-02 — Actividad.**
CUANDO una persona realice cualquier acción (cada comando en la consola, cada petición del navegador), EL SISTEMA DEBE renovar su hora de actividad.
SI la persona ya figuraba desconectada por inactividad, ENTONCES EL SISTEMA DEBE hacerla figurar conectada de nuevo.

**RF-03 — Salir.**
CUANDO una persona salga, EL SISTEMA DEBE dejar de mostrarla como conectada.
SI no figuraba conectada, ENTONCES EL SISTEMA DEBE informarlo sin error y sin cambiar nada.

**RF-04 — Inactividad.**
CUANDO se consulte quién está conectado o el estado de alguien, EL SISTEMA DEBE dejar de mostrar como conectada a toda persona con 30 segundos o más sin actividad.

**RF-05 — Listar conectados.**
CUANDO se pida la lista de personas conectadas, EL SISTEMA DEBE devolver a todas las que figuran conectadas, la que se conectó más recientemente primero; renovar la actividad no cambia ese orden.
SI nadie está conectado, ENTONCES EL SISTEMA DEBE devolver una lista vacía sin error.

**RF-06 — Estado de una persona y de sus amigos.**
CUANDO se pregunte por una persona, EL SISTEMA DEBE responder si figura conectada o no.
CUANDO se pida el estado de los amigos de una persona, EL SISTEMA DEBE devolver cada amigo con su estado, en el mismo orden en que se entregaron.

**RF-07 — Hora que retrocede.**
SI la hora recibida es anterior a la última hora conocida, ENTONCES EL SISTEMA DEBE rechazar la operación sin cambiar nada.

**RF-08 — Estado.**
CUANDO se pregunte cuántas personas figuran conectadas, EL SISTEMA DEBE devolver el número sin cambiar nada más que la caducidad de RF-04.

## 3. Criterios de aceptación
| ID | Criterio (de [`historias.md`](../00-producto/historias.md)) | Prioridad | Prueba esperada |
|---|---|---|---|
| CA-09 | Al entrar, la persona figura como conectada. | Should | `tests/test_lista_simple.py` |
| CA-10 | Al salir, o tras 30 segundos sin actividad, figura como desconectada. | Should | `tests/test_lista_simple.py` |
| CA-11 | Se puede ver la lista de personas conectadas y el estado (conectado o no) de cada amigo. | Should | `tests/test_lista_simple.py` |

## 4. Casos extremos
- Nadie conectado: listar devuelve vacío y el estado de cualquiera es «no conectada» (CA-11).
- Una sola persona conectada: aparece, y al salir la lista queda vacía (CA-09, CA-10).
- Entrar dos veces seguidas: aparece una sola vez (CA-09).
- Salir sin haber entrado, o salir dos veces: informa sin error (CA-10).
- Salir siendo la primera, una intermedia o la última de la lista: las demás siguen figurando (CA-10).
- A los 29 segundos sin actividad sigue conectada; a los 30 ya figura desconectada (CA-10).
- Una acción a los 29 segundos renueva el plazo: a los 58 sigue conectada y a los 59 ya no (CA-10).
- Varias personas vencen a la vez, entre ellas la primera y la última: todas se retiran en una sola consulta y las demás quedan (CA-10).
- Una persona desconectada por inactividad hace una acción: vuelve a figurar conectada (CA-10).
- Varias personas conectadas: la última en entrar sale primero en la lista (CA-11).
- Estado de un amigo que nunca entró, de un amigo desconectado y de uno conectado, mezclados (CA-11).
- Estado de una persona que no existe: «no conectada», sin error (CA-11).
- Hora anterior a la última conocida: se rechaza y la lista queda igual (RF-07).

## 5. Fuera de alcance
- Mostrar desde cuándo está conectada una persona.
- Estados intermedios («ausente», «ocupado»).
- Mantener la lista al día con un temporizador en segundo plano.
- Guardar quién estuvo conectado entre ejecuciones.

## Historial de cambios
| Versión | Fecha | Cambio | Motivo |
|---|---|---|---|
| 1.0 | 2026-11-07 | Versión inicial (la carpeta estaba vacía) | Faltaban spec, plan y tasks de la lista simple; criterios CA-09, CA-10, CA-11; cualquier acción cuenta como actividad; la caducidad se aplica al consultar con la hora dada por quien llama; 30 segundos o más es desconectada; decisiones tomadas en la consulta del componente |
