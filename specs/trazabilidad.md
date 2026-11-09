# Trazabilidad criterio ↔ prueba ↔ código
Versión 1.2

Se recorre en los dos sentidos: de un criterio a la spec que lo define, su prueba y su código (primera tabla), y de una función a los criterios de los que nació (segunda tabla). Se actualiza con cada commit `test(...)`: el estado de la prueba pasa de «pendiente» a «pasa». Las historias están en [`00-producto/historias.md`](00-producto/historias.md) y las prioridades en [`00-producto/moscow.md`](00-producto/moscow.md).

## Criterio → historia → spec → prueba → código
| Criterio | Historia | Prioridad | Spec que lo define | Prueba esperada | Estado | Código esperado |
|---|---|---|---|---|---|---|
| CA-01 | HU-01 | Must | [`05-avl`](05-avl/spec.md) | `tests/test_avl.py` | pasa | `dominio/usuarios.py`, `estructuras/avl.py` |
| CA-02 | HU-01 | Must | [`05-avl`](05-avl/spec.md) | `tests/test_avl.py` | pasa | `dominio/usuarios.py` |
| CA-03 | HU-02 | Must | [`05-avl`](05-avl/spec.md) | `tests/test_avl.py` | pasa | `dominio/usuarios.py`, `estructuras/avl.py` |
| CA-04 | HU-02 | Must | [`05-avl`](05-avl/spec.md) | `tests/test_avl.py` | pasa | `dominio/usuarios.py` |
| CA-05 | HU-03 | Must | [`03-cola`](03-cola/spec.md) | `tests/test_cola.py` | parcial: `contiene` listo, falta `amistades.enviar` | `dominio/amistades.py`, `estructuras/cola.py` |
| CA-06 | HU-03 | Must | [`06-grafo`](06-grafo/spec.md) | `tests/test_grafo.py` | parcial (grafo hecho; falta aceptar/rechazar desde la cola) | `estructuras/grafo.py`, `dominio/amistades.py` |
| CA-07 | HU-03 | Must | [`03-cola`](03-cola/spec.md) | `tests/test_cola.py` | parcial: cola lista, falta `amistades.atender` | `estructuras/cola.py`, `dominio/amistades.py` |
| CA-08 | HU-03 | Must | [`06-grafo`](06-grafo/spec.md) | `tests/test_grafo.py` | pasa | `estructuras/grafo.py` |
| CA-09 | HU-04 | Should | [`08-lista-simple`](08-lista-simple/spec.md) | `tests/test_lista_simple.py` | pendiente | `estructuras/lista_simple.py`, `dominio/presencia.py` |
| CA-10 | HU-04 | Should | [`08-lista-simple`](08-lista-simple/spec.md) | `tests/test_lista_simple.py` | pendiente | `estructuras/lista_simple.py`, `dominio/presencia.py` |
| CA-11 | HU-04 | Should | [`08-lista-simple`](08-lista-simple/spec.md) | `tests/test_lista_simple.py` | pendiente | `estructuras/lista_simple.py`, `dominio/presencia.py` |
| CA-12 | HU-05 | Must | [`01-lista-doble`](01-lista-doble/spec.md) | `tests/test_lista_doble.py` | pasa | `estructuras/lista_doble.py`, `dominio/feed.py` |
| CA-13 | HU-05 | Must | [`01-lista-doble`](01-lista-doble/spec.md) | `tests/test_lista_doble.py` | pasa | `estructuras/lista_doble.py`, `dominio/feed.py` |
| CA-14 | HU-06 | Must | [`04-arbol-general`](04-arbol-general/spec.md) | `tests/test_arbol_general.py` | pendiente | `estructuras/arbol_general.py`, `dominio/hilos.py` |
| CA-15 | HU-06 | Must | [`04-arbol-general`](04-arbol-general/spec.md) | `tests/test_arbol_general.py` | pendiente | `estructuras/arbol_general.py`, `dominio/hilos.py` |
| CA-16 | HU-06 | Must | [`04-arbol-general`](04-arbol-general/spec.md) | `tests/test_arbol_general.py` | pendiente | `estructuras/arbol_general.py` |
| CA-17 | HU-07 | Should | [`05-avl`](05-avl/spec.md) | `tests/test_avl.py` | pendiente | `dominio/votos.py`, `estructuras/avl.py` |
| CA-18 | HU-07 | Should | [`05-avl`](05-avl/spec.md) | `tests/test_avl.py` | pendiente | `dominio/votos.py`, `estructuras/avl.py` |
| CA-19 | HU-07 | Should | [`05-avl`](05-avl/spec.md) | `tests/test_avl.py` | pendiente | `dominio/votos.py` |
| CA-20 | HU-07 | Should | [`05-avl`](05-avl/spec.md) | `tests/test_avl.py` | pendiente | `dominio/votos.py`, `estructuras/avl.py` |
| CA-21 | HU-07 | Should | [`05-avl`](05-avl/spec.md) | `tests/test_avl.py` | pendiente | `dominio/usuarios.py` |
| CA-22 | HU-08 | Should | [`04-arbol-general`](04-arbol-general/spec.md) | `tests/test_arbol_general.py` | pendiente | `estructuras/arbol_general.py`, `dominio/hilos.py` |
| CA-23 | HU-08 | Should | [`04-arbol-general`](04-arbol-general/spec.md) | `tests/test_arbol_general.py` | pendiente | `estructuras/arbol_general.py` |
| CA-24 | HU-09 | Should | [`07-monticulo`](07-monticulo/spec.md) | `tests/test_monticulo.py` | pendiente | `dominio/destacada.py`, `estructuras/monticulo.py` |
| CA-25 | HU-09 | Should | [`07-monticulo`](07-monticulo/spec.md) | `tests/test_monticulo.py` | pendiente | `estructuras/monticulo.py`, `dominio/destacada.py` |
| CA-26 | HU-09 | Should | [`07-monticulo`](07-monticulo/spec.md) | `tests/test_monticulo.py` | pendiente | `dominio/destacada.py` |
| CA-27 | HU-10 | Must | [`05-avl`](05-avl/spec.md) | `tests/test_avl.py` | pasa | `estructuras/avl.py`, `dominio/usuarios.py` |
| CA-28 | HU-10 | Must | [`05-avl`](05-avl/spec.md) | `tests/test_avl.py` | pasa | `estructuras/avl.py` |
| CA-29 | HU-10 | Must | [`01-lista-doble`](01-lista-doble/spec.md) | `tests/test_lista_doble.py` | pasa | `dominio/busqueda.py`, `estructuras/lista_doble.py` |
| CA-30 | HU-11 | Must | [`02-pila`](02-pila/spec.md) | `tests/test_pila.py` | pasa | `estructuras/pila.py`, `dominio/navegacion.py` |
| CA-31 | HU-11 | Must | [`02-pila`](02-pila/spec.md) | `tests/test_pila.py` | pasa | `estructuras/pila.py`, `dominio/navegacion.py` |
| CA-32 | HU-12 | Must | [`03-cola`](03-cola/spec.md) | `tests/test_cola.py` | pasa | `estructuras/cola.py`, `dominio/notificaciones.py` |
| CA-33 | HU-12 | Must | [`03-cola`](03-cola/spec.md) | `tests/test_cola.py` | pasa | `dominio/notificaciones.py` |
| CA-34 | HU-13 | Must | [`06-grafo`](06-grafo/spec.md) | `tests/test_grafo.py` | pasa | `estructuras/grafo.py`, `dominio/recomendaciones.py` |
| CA-35 | HU-13 | Must | [`07-monticulo`](07-monticulo/spec.md) | `tests/test_monticulo.py` | pendiente | `estructuras/monticulo.py`, `dominio/recomendaciones.py` |
| CA-36 | HU-13 | Must | [`06-grafo`](06-grafo/spec.md) | `tests/test_grafo.py` | pasa | `estructuras/grafo.py` |
| CA-37 | HU-14 | Must | [`99-sistema`](99-sistema/spec.md) | `tests/test_sistema.py` | pendiente | `main.py` |
| CA-38 | HU-14 | Should | [`99-sistema`](99-sistema/spec.md) | `tests/test_sistema.py` | pendiente | `web.py` |
| CA-39 | HU-10 | Should | [`05-avl`](05-avl/spec.md) | `tests/test_avl.py` | pendiente | `dominio/busqueda.py`, `estructuras/avl.py` |

## Dirección inversa (función → criterio)
Cada función pública nombrada en un `plan.md` nace de al menos un criterio. Las funciones auxiliares sin criterio propio están en la última sección.

### Plaza ([`01-lista-doble`](01-lista-doble/plan.md))
| Función | Nació del criterio |
|---|---|
| `ListaDoble.insertar_al_frente` | CA-12 |
| `ListaDoble.inicio` | CA-12, CA-13 |
| `ListaDoble.pagina` | CA-13 |
| `ListaDoble.avanzar` | CA-13 |
| `ListaDoble.retroceder` | CA-13 |
| `ListaDoble.esta_vacia` | CA-13 |
| `ListaDoble.tamano` | CA-12 |
| `ListaDoble.__iter__` | CA-29 |
| `busqueda.buscar_palabra` | CA-29 |
| `Plaza.publicar` | CA-12 |
| `Plaza.sesion` y `SesionPlaza.ver` / `siguiente` / `anterior` / `inicio` | CA-13 |

### Historial ([`02-pila`](02-pila/plan.md))
| Función | Nació del criterio |
|---|---|
| `PilaEnlazada.apilar` | CA-30 |
| `PilaEnlazada.desapilar` | CA-30, CA-31 |
| `PilaEnlazada.tope` | CA-30, CA-31 |
| `PilaEnlazada.esta_vacia` | CA-31 |
| `PilaEnlazada.tamano` | CA-30 |
| `navegacion.ir_a` | CA-30 |
| `navegacion.atras` | CA-30, CA-31 |

### Solicitudes y notificaciones ([`03-cola`](03-cola/plan.md))
| Función | Nació del criterio |
|---|---|
| `ColaEnlazada.encolar` | CA-05, CA-32 |
| `ColaEnlazada.desencolar` | CA-07, CA-32 |
| `ColaEnlazada.frente` | CA-07 |
| `ColaEnlazada.contiene` | CA-05 |
| `ColaEnlazada.esta_vacia` | CA-07, CA-33 |
| `ColaEnlazada.tamano` | CA-05 |
| `amistades.enviar` | CA-05 |
| `amistades.atender` | CA-07 (y CA-06 en el grafo) |
| `notificaciones.notificar` | CA-32 |
| `notificaciones.leer` | CA-32, CA-33 |

### Hilos ([`04-arbol-general`](04-arbol-general/plan.md))
| Función | Nació del criterio |
|---|---|
| `ArbolGeneral.abrir_hilo` | CA-14 |
| `ArbolGeneral.responder` | CA-14, CA-15, CA-16 |
| `ArbolGeneral.buscar` | CA-16 |
| `ArbolGeneral.recorrer` | CA-15 |
| `ArbolGeneral.profundidad` | CA-15 |
| `ArbolGeneral.tamano` | CA-14 |
| `ArbolGeneral.aceptar` | CA-22 |
| `ArbolGeneral.mejor_respuesta` | CA-23 |
| `hilos.mostrar` (sangría por nivel) | CA-15 |
| `hilos.aceptar` (suma 15 puntos) | CA-22 |

### Usuarios, votos y fechas ([`05-avl`](05-avl/plan.md))
| Función | Nació del criterio |
|---|---|
| `AVL.insertar` | CA-01, CA-03, CA-04 |
| `AVL.buscar` | CA-03, CA-04 |
| `AVL.reemplazar` | CA-17, CA-18, CA-20 |
| `AVL.buscar_por_prefijo` | CA-27, CA-28, CA-39 |
| `AVL.recorrer_en_orden` | CA-27 |
| `AVL.altura` | CA-01 (prueba de equilibrio con perfiles ordenados) |
| `AVL.tamano` | CA-01 |
| `usuarios.generar_comunidad` | CA-01, CA-02 |
| `Catalogo.entrar` | CA-03 |
| `Catalogo.crear_perfil` | CA-03, CA-04 |
| `usuarios.normalizar_usuario` | CA-04 |
| `Catalogo.buscar` | CA-03 |
| `Catalogo.buscar_por_prefijo` | CA-27, CA-28 |
| `Catalogo.por_id` | CA-01 |
| `Catalogo.perfiles` | CA-01 |
| `Catalogo.tamano` | CA-01 |
| `usuarios.insignia` | CA-21 |
| `votos.votar` | CA-17, CA-18, CA-19 |
| `votos.cambiar` | CA-20 |
| `votos.retirar` | CA-20 |
| `busqueda.por_fecha` | CA-39 |

### Amistades ([`06-grafo`](06-grafo/plan.md))
| Función | Nació del criterio |
|---|---|
| `Grafo.agregar_vertice` / `Grafo.cantidad` | CA-06 |
| `Grafo.agregar_amistad` | CA-06 |
| `Grafo.eliminar_amistad` | CA-08 |
| `Grafo.son_amigos` | CA-05, CA-06 |
| `Grafo.amigos` | CA-11, CA-34 |
| `Grafo.grado` | CA-36 |
| `Grafo.candidatos_dos_saltos` | CA-34, CA-36 |

### Destacada y recomendaciones ([`07-monticulo`](07-monticulo/plan.md))
| Función | Nació del criterio |
|---|---|
| `Monticulo.insertar` | CA-24 |
| `Monticulo.maximo` | CA-24, CA-26 |
| `Monticulo.extraer_maximo` | CA-35 |
| `Monticulo.actualizar` | CA-25 |
| `Monticulo.construir` | CA-35 |
| `Monticulo.esta_vacio` | CA-26 |
| `Monticulo.tamano` | CA-35 |
| `destacada.publicar` / `responder` / `votar` / `retirar_voto` | CA-24, CA-25 |
| `destacada.destacada` | CA-24, CA-26 |
| `recomendaciones.recomendar` | CA-34, CA-35, CA-36 |

### Conectados ([`08-lista-simple`](08-lista-simple/plan.md))
| Función | Nació del criterio |
|---|---|
| `ListaSimple.conectar` | CA-09 |
| `ListaSimple.registrar_actividad` | CA-10 |
| `ListaSimple.salir` | CA-10 |
| `ListaSimple.caducar` | CA-10 |
| `ListaSimple.listar` | CA-11 |
| `ListaSimple.esta_conectado` | CA-09, CA-11 |
| `ListaSimple.estado_amigos` | CA-11 |
| `ListaSimple.cantidad` | CA-11 |
| `presencia.estado_amigos` | CA-11 |

### Sistema ([`99-sistema`](99-sistema/spec.md))
| Función | Nació del criterio |
|---|---|
| Menús de la consola en `main.py` | CA-37 |
| Servidor y páginas en `web.py` | CA-38 |

## Funciones auxiliares sin criterio propio
Se prueban dentro de la tarea del criterio que las usa: `subir` y `bajar` del montículo (CA-24, CA-25, CA-35), rotaciones del AVL (CA-01), `_avanzar_reloj` de la lista simple (CA-10), `Nodo` de cada estructura.

## Historial de cambios
| Versión | Fecha | Cambio | Motivo |
|---|---|---|---|
| 1.0 | 2026-11-07 | Tabla inicial con 21 criterios | Creación |
| 1.1 | 2026-11-07 | Se reescribe con los 39 criterios de las historias v1.2 (historia, prioridad, spec, prueba, estado y código) y una tabla inversa función → criterio por componente | La tabla anterior usaba la numeración v1.0 de los criterios y solo llegaba a CA-21; la traza debe poder recorrerse en ambos sentidos |
| 1.2 | 2026-11-08 | CA-08, CA-34 y CA-36 pasan a «pasa»; CA-06 queda «parcial»; se anota `Grafo.cantidad` | Se implementó el grafo (avance 4); aceptar y rechazar desde la cola llegan con las amistades integradas |
