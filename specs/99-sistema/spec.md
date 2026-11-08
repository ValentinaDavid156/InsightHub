# Spec del sistema — InsightHub
Versión 1.1 · Estado: aprobada para implementar

## 1. Qué hace el sistema
InsightHub es una red social **100 % pública** de preguntas y respuestas. Los miembros entran con su `@usuario`, hacen amigos con solicitud y aceptación, publican preguntas en una plaza común, responden en hilos anidados, votan, buscan, navegan con «atrás», reciben notificaciones y obtienen recomendaciones de contactos. **No hay chats ni mensajes privados** ([`CONSTITUTION.md`](../CONSTITUTION.md)).

Se usa desde la **consola** (prioridad Must) y, si sobra tiempo, desde un **sitio web** (prioridad Should). Los datos viven solo en memoria. Este documento dice qué hace el sistema como conjunto y cómo se conectan sus ocho componentes; el detalle de cada uno está en su propia carpeta.

Historia: **HU-14**. Criterios: **CA-37** (consola, Must) y **CA-38** (sitio web, Should).

## 2. Componentes y lo que expone cada uno
| Componente | Estructura | Operaciones que expone | Spec |
|---|---|---|---|
| Plaza | Lista doble | `insertar_al_frente`, `inicio`, `pagina`, `avanzar`, `retroceder`, `buscar_palabra`, `esta_vacia`, `tamano` | [`01-lista-doble`](../01-lista-doble/spec.md) |
| Historial | Pila | `apilar`, `desapilar`, `tope`, `esta_vacia`, `tamano` | [`02-pila`](../02-pila/spec.md) |
| Solicitudes y notificaciones | Cola | `encolar`, `desencolar`, `frente`, `contiene`, `esta_vacia`, `tamano` | [`03-cola`](../03-cola/spec.md) |
| Hilos | Árbol general | `abrir_hilo`, `responder`, `buscar`, `recorrer`, `profundidad`, `tamano`, `aceptar`, `mejor_respuesta` | [`04-arbol-general`](../04-arbol-general/spec.md) |
| Usuarios, votos y fechas | AVL | `insertar`, `buscar`, `reemplazar`, `buscar_por_prefijo`, `recorrer_en_orden`, `altura`, `tamano` | [`05-avl`](../05-avl/spec.md) |
| Amistades | Grafo | `agregar_vertice`, `agregar_amistad`, `eliminar_amistad`, `son_amigos`, `amigos`, `grado`, `candidatos_dos_saltos` | [`06-grafo`](../06-grafo/spec.md) |
| Destacada y recomendaciones | Montículo máximo | `insertar`, `maximo`, `extraer_maximo`, `actualizar`, `construir`, `esta_vacio`, `tamano` | [`07-monticulo`](../07-monticulo/spec.md) |
| Conectados | Lista simple | `conectar`, `registrar_actividad`, `salir`, `caducar`, `listar`, `esta_conectado`, `estado_amigos`, `cantidad` | [`08-lista-simple`](../08-lista-simple/spec.md) |

Las partes marcadas Should en cada componente (votos, mejor respuesta, destacada, búsqueda por fecha, conectados) solo se conectan si se implementan.

## 3. Cómo encajan
| Acción del miembro | Qué hace cada componente | Prioridad |
|---|---|---|
| Entrar con `@usuario` | AVL busca o crea el perfil; si es nuevo, el grafo lo registra sin amigos | Must |
| Enviar solicitud de amistad | AVL comprueba que existe; el grafo, que no son amigos; la cola del destinatario, que no está repetida; si todo cumple se encola la solicitud y se avisa al destinatario (cola de notificaciones) | Must |
| Revisar solicitudes | La cola entrega solo la primera pendiente | Must |
| Aceptar la solicitud | La cola la saca; el grafo crea la amistad en ambos sentidos; se avisa a quien la envió (cola) | Must |
| Rechazar la solicitud | La cola la saca; el grafo no cambia | Must |
| Deshacer una amistad | El grafo la elimina en ambos sentidos | Must |
| Publicar una pregunta | La plaza la inserta al frente; el árbol abre su hilo; (Should) el montículo la registra con actividad 0 y el AVL de fechas la indexa | Must |
| Recorrer la plaza | La plaza pagina de 5 en 5 desde la posición propia de la sesión | Must |
| Buscar usuarios | El AVL busca por prefijo en orden alfabético | Must |
| Buscar publicaciones por palabra | La plaza recorre sus publicaciones | Must |
| Buscar publicaciones por fecha | El AVL de fechas devuelve las de ese día | Should |
| Responder | El árbol agrega la respuesta; se avisa al autor de la publicación (cola), salvo que responda él mismo; (Should) el montículo suma 1 a la actividad | Must |
| Ver un hilo | El árbol lo recorre mostrando el nivel de cada respuesta | Must |
| Votar, cambiar o retirar un voto | El AVL de votos de la respuesta registra el voto; el AVL de usuarios ajusta los puntos del autor y su insignia; el montículo ajusta la actividad | Should |
| Aceptar la mejor respuesta | El árbol la fija; el AVL de usuarios suma 15 puntos; se avisa a su autor (cola) | Should |
| Ver notificaciones | La cola entrega todas en orden de llegada y queda vacía | Must |
| Recomendaciones | El grafo entrega los candidatos a 2 saltos; el montículo los ordena y se muestran hasta 5 | Must |
| Ver la destacada | El montículo entrega la de mayor actividad | Should |
| Ver quién está conectado | La lista simple entrega los conectados y el estado de cada amigo (los amigos los da el grafo) | Should |
| Cada pantalla visitada | La pila guarda la anterior; «atrás» la recupera | Must |
| Cada acción de la persona | (Should) La lista simple renueva su actividad | Should |

## 4. Requisitos del sistema

**RF-01 — Una sola aplicación.**
CUANDO se inicie InsightHub, EL SISTEMA DEBE crear los 120 perfiles de ejemplo con la semilla `706132` y empezar sin amistades, publicaciones ni notificaciones: el contenido de la demostración lo crean los miembros.

**RF-02 — Todo es público.**
EL SISTEMA NO DEBE ofrecer ninguna función que cree conversaciones privadas.

**RF-03 — Errores controlados.**
SI una operación se rechaza (usuario inválido, solicitud repetida, respuesta a un comentario inexistente, etc.), ENTONCES EL SISTEMA DEBE mostrar un mensaje claro y seguir funcionando con el mismo estado que tenía.

**RF-04 — Consola con menús (Must).**
CUANDO una persona use la consola, EL SISTEMA DEBE pedirle su `@usuario` al arrancar, repitiendo la pregunta con el motivo mientras sea inválido, y después mostrarle menús numerados por pantalla (inicio, plaza, hilo, perfil, búsqueda, amigos, solicitudes, notificaciones, recomendaciones y, si se implementan, conectados y destacada), con una opción «atrás» en toda pantalla excepto la de inicio.
CUANDO elija una opción que no existe o escriba algo que no es un número, EL SISTEMA DEBE avisarlo y volver a mostrar el menú sin cambiar nada.

**RF-05 — Todas las funciones por consola (CA-37).**
EL SISTEMA DEBE permitir ejercitar desde la consola cada función implementada de las historias HU-02 a HU-13.

**RF-06 — Sitio web (Should).**
CUANDO se inicie el sitio web, EL SISTEMA DEBE ofrecer en el navegador las mismas funciones que la consola, sobre los mismos datos, con una sesión independiente por persona (cada una con su posición en la plaza y su historial de «atrás»).
CUANDO una persona tenga la página abierta, EL SISTEMA DEBE actualizar cada ~5 segundos sus notificaciones y la lista de conectados, y la hora de actividad de ese navegador cuenta como actividad.

**RF-07 — Las partes Should no bloquean las Must.**
EL SISTEMA DEBE funcionar completo en sus partes Must aunque ninguna parte Should esté implementada: en ese caso el menú no ofrece las opciones Should, y ninguna pantalla Must depende de ellas.

## 5. Criterios de aceptación
| ID | Criterio (de [`historias.md`](../00-producto/historias.md)) | Prioridad | Prueba esperada |
|---|---|---|---|
| CA-37 | Cada función implementada de las historias HU-02 a HU-13 puede ejercitarse desde la consola. | Must | `tests/test_sistema.py` |
| CA-38 | Cada función implementada de las historias HU-02 a HU-13 puede ejercitarse desde el sitio web. | Should | `tests/test_sistema.py` |

## 6. Mapa de criterios por componente
| Criterios | Dueño |
|---|---|
| CA-30, CA-31 | [`02-pila`](../02-pila/spec.md) |
| CA-05, CA-07, CA-32, CA-33 | [`03-cola`](../03-cola/spec.md) |
| CA-12, CA-13, CA-29 | [`01-lista-doble`](../01-lista-doble/spec.md) |
| CA-14, CA-15, CA-16, CA-22, CA-23 | [`04-arbol-general`](../04-arbol-general/spec.md) |
| CA-01, CA-02, CA-03, CA-04, CA-17, CA-18, CA-19, CA-20, CA-21, CA-27, CA-28, CA-39 | [`05-avl`](../05-avl/spec.md) |
| CA-06, CA-08, CA-34, CA-36 | [`06-grafo`](../06-grafo/spec.md) |
| CA-24, CA-25, CA-26, CA-35 | [`07-monticulo`](../07-monticulo/spec.md) |
| CA-09, CA-10, CA-11 | [`08-lista-simple`](../08-lista-simple/spec.md) |
| CA-37, CA-38 | este documento |

## 7. Casos extremos
- Recién iniciado: hay 120 perfiles y nada más; la plaza está vacía, no hay amistades, solicitudes ni notificaciones, y cada pantalla lo dice sin fallar.
- Entrar con un `@usuario` vacío o solo con espacios: se rechaza con mensaje claro.
- Opción de menú inexistente, texto en lugar de número o línea vacía: se avisa y se repite el menú.
- «Atrás» en la pantalla de inicio: se informa que no hay pantalla previa (CA-31).
- Una acción Should no implementada: su opción no aparece en el menú.
- Dos sesiones web a la vez: cada una conserva su propia posición en la plaza y su propio historial; los datos de la comunidad son los mismos para ambas.
- Una persona entra por la consola y otra por la web (si ambas están activas): ven la misma comunidad.
- Salir de la aplicación: se pierde todo el contenido, y al volver a entrar empieza de nuevo con los 120 perfiles de la semilla.

## 8. Fuera de alcance
- Chats o mensajes privados.
- Contraseñas.
- Guardar datos en archivo o base de datos (Won't).
- Camino más corto entre personas con A* (Won't).
- Datos de demostración más allá de los perfiles: amistades y publicaciones de ejemplo (decisión en la consulta del sistema).

## Historial de cambios
| Versión | Fecha | Cambio | Motivo |
|---|---|---|---|
| 0.1 | 2026-11-07 | Versión inicial | Entrega 1 |
| 1.0 | 2026-11-07 | Se reescribe: tabla de ocho componentes con las operaciones que expone cada uno; flujos de integración (solicitud → cola, aceptar → grafo y aviso, responder → árbol y aviso, cada pantalla → pila); consola Must (menús numerados) y web Should; criterios CA-37 y CA-38; mapa de criterios por componente | La spec 0.1 tenía seis componentes con las historias viejas (seguir en vez de amistad) y no describía las interfaces; decisiones tomadas en la consulta del sistema |
| 1.1 | 2026-11-08 | RF-04: la consola pide el `@usuario` al arrancar y luego muestra los menús | Decisión de Valentina al implementar la entrada (el AVL de usuarios) |
