# Priorización MoSCoW y capacidad
Versión 1.2

## Criterio de estimación
Cada estructura la escribo y la entiendo yo, línea por línea. Cuando ya tengo una implementación propia de una semana del curso (lista doble de Semana7, pila y cola de Semana10), la estimación baja un poco porque parto de mi propio código, pero igual lo reescribo y lo adapto. Las historias, criterios y estructuras están en [`historias.md`](historias.md) y [`estructuras.md`](estructuras.md).

## Cálculo de capacidad
| Concepto | Horas |
|---|---|
| Tiempo total disponible del 7 al 11 de nov (23:59), unas 7 h diarias | 29 |
| Escribir specs, plans y tasks de los 8 componentes, `99-sistema` y `trazabilidad.md` | −2.5 |
| Cierre: informe técnico de 6 a 10 páginas en APA (3), `ANALISIS.md` con mediciones (1.5), bitácora y README (0.5), preparar la sustentación (1) | −6 |
| Colchón para imprevistos | −2 |
| **Capacidad neta para implementar** | **18.5** |

## Must — 17.75 h (caben en las 18.5 h; sobran 0.75 h)
| Historia | Estructura | Horas |
|---|---|---|
| HU-01 Encontrar una comunidad ya poblada | AVL (inserción con rotaciones y generador con semilla) | 2 |
| HU-02 Acceder y crear perfil | AVL | 0.75 |
| HU-03 Hacer amigos con solicitud | Cola + Grafo | 3 |
| HU-05 Publicar y recorrer la plaza | Lista doble | 2 |
| HU-06 Debatir en hilos anidados | Árbol general + Pila | 3 |
| HU-10 (CA-27, CA-28, CA-29) Buscar usuarios por prefijo y publicaciones por palabra | AVL + recorrido de lista doble | 1.5 |
| HU-11 Volver a la pantalla anterior | Pila | 0.75 |
| HU-12 Recibir y leer notificaciones | Cola | 0.75 |
| HU-13 Recibir recomendaciones de contactos | Grafo + Montículo | 2.5 |
| HU-14 (CA-37) Participar desde la consola | (interfaz) | 1.5 |
| **Total Must** | | **17.75** |

### Dependencias resueltas
- **HU-12 → HU-08:** el aviso de «respuesta aceptada» salió de HU-12 y pasó a HU-08 (Should). HU-12 solo avisa de solicitudes, amistades aceptadas y respuestas, que vienen de historias Must (HU-03 y HU-06).
- **HU-14 → web:** CA-37 (consola) es Must; CA-38 (sitio web) es Should. Ningún Must depende de la web.
- **HU-10 → fecha:** CA-29 (palabra) es Must; CA-39 (fecha) es Should.

## Should — 9 h (solo si sobra tiempo; hoy sobran 0.75 h)
Orden sugerido de implementación:
| Historia | Estructura | Horas |
|---|---|---|
| HU-07 Votar y ganar reputación | AVL | 2 |
| HU-08 Destacar la mejor respuesta | Árbol general | 1 |
| HU-09 Ver la publicación destacada | Montículo | 1.75 |
| HU-04 Ver quién está conectado | Lista simple | 1 |
| HU-10 (CA-39) Buscar publicaciones por fecha | AVL | 0.75 |
| HU-14 (CA-38) Participar desde el sitio web | (interfaz) | 2.5 |

## Could
| Elemento | Horas |
|---|---|
| Categorías o etiquetas en las preguntas | 2 |

## Won't (esta vez)
| Elemento | Razón |
|---|---|
| Cadena de conexión más corta con A* | Es opcional en la temática y la capacidad se reserva a lo obligatorio |
| Guardar los datos en archivo o base de datos | Los datos viven en memoria (ver [Constitución](../CONSTITUTION.md)); la persistencia no aporta a la decisión de estructuras |
| Matriz dispersa para las relaciones | La lista de adyacencia ya resuelve la red dispersa; no hace falta una segunda representación |

## Historial de cambios
| Versión | Fecha | Cambio | Motivo |
|---|---|---|---|
| 1.0 | 2026-11-07 | Priorización inicial | Creación |
| 1.1 | 2026-11-07 | Capacidad de 20 h (13 h netas); 14 historias repartidas; el sitio web pasa a Should y la consola queda como Must; votos, mejor respuesta, destacada y conectados quedan como Should | Los Must con web sumaban 13.75 h y no cabían en 13 h; se decidió dejar la web para el final |
| 1.2 | 2026-11-07 | Se quita «se parte del código ya preparado» y se reestima escribiendo cada estructura (Must de 12.25 a 17.75 h, +5.5 h; Should de 6.25 a 9 h); se suman 2.5 h de specs; el cierre pasa de 5 a 6 h; el total sube de 20 a 29 h (18.5 h netas); se resuelven las dependencias HU-12→HU-08 y HU-14→web con CA-38 y CA-39 | Escribo y entiendo yo cada estructura; el tiempo de specs no estaba contado; 5 h no alcanzaban para informe, análisis, bitácora, README y sustentación; ningún Must debe depender de un Should |
