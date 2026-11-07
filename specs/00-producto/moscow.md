# Priorización MoSCoW y capacidad
Versión 1.1

## Cálculo de capacidad
Se parte del código ya preparado: el trabajo es estudiarlo, adaptarlo a las decisiones del proyecto y poder explicarlo línea por línea. Las horas estimadas son aproximadamente la mitad de escribirlo todo desde cero.

| Concepto | Horas |
|---|---|
| Tiempo total disponible hasta el 11 de nov (23:59) | 20 |
| Informe técnico, `ANALISIS.md` y preparación de la sustentación | −5 |
| Colchón para imprevistos | −2 |
| **Capacidad neta para implementar** | **13** |

## Must — 12.25 h (caben en las 13 h; sobran 0.75 h)
| Historia | Estructura | Horas |
|---|---|---|
| HU-01 Generar usuarios sintéticos | AVL | 1 |
| HU-02 Acceder y crear perfil | AVL | 0.5 |
| HU-03 Hacer amigos con solicitud | Cola + Grafo | 2 |
| HU-05 Publicar y recorrer la plaza | Lista doble | 1.5 |
| HU-06 Debatir en hilos anidados | Árbol general + Pila | 2 |
| HU-10 Buscar usuarios por prefijo y publicaciones por palabra | AVL + recorrido de lista doble | 1.25 |
| HU-11 Volver a la pantalla anterior | Pila | 0.75 |
| HU-12 Recibir y leer notificaciones | Cola | 0.75 |
| HU-13 Recibir recomendaciones de contactos | Grafo + Montículo | 1.5 |
| HU-14 Usar la plataforma desde la consola | (interfaz) | 1 |
| **Total Must** | | **12.25** |

## Should — 6.25 h (solo si sobra tiempo; hoy sobran 0.75 h)
Orden sugerido de implementación:
| Historia | Estructura | Horas |
|---|---|---|
| HU-07 Votar y ganar reputación | AVL | 1.5 |
| HU-08 Destacar la mejor respuesta | Árbol general | 0.75 |
| HU-09 Ver la publicación destacada | Montículo | 1.25 |
| HU-04 Ver quién está conectado | Lista simple | 0.75 |
| HU-10 (parte) Buscar publicaciones por fecha | AVL | 0.5 |
| HU-14 (parte) Usar la plataforma desde el sitio web | (interfaz) | 1.5 |

## Could
| Elemento | Horas |
|---|---|
| Categorías o etiquetas en las preguntas | 2 |

## Won't (esta vez)
| Elemento | Razón |
|---|---|
| Cadena de conexión más corta con A* | Es opcional en la temática y la capacidad se reserva a lo obligatorio |
| Guardar los datos en archivo o base de datos | Los datos viven en memoria (ver Constitución); la persistencia no aporta a la decisión de estructuras |
| Matriz dispersa para las relaciones | La lista de adyacencia ya resuelve la red dispersa; no hace falta una segunda representación |

## Historial de cambios
| Versión | Fecha | Cambio | Motivo |
|---|---|---|---|
| 1.0 | 2026-11-07 | Priorización inicial | Creación |
| 1.1 | 2026-11-07 | Capacidad de 20 h (13 h netas); 14 historias repartidas; el sitio web pasa a Should y la consola queda como Must; votos, mejor respuesta, destacada y conectados quedan como Should | Los Must con web sumaban 13.75 h y no cabían en 13 h; se decidió dejar la web para el final |
