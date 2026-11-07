# Plan — Lista doble
Versión 1.1

## 1. De qué implementación mía parto
De **`Semana7/Nodos_enlazados_doblemente.py`** (`ListadoblementeEnlazada` con `cabeza`, `cola`, `actual`, `deshacer` y `rehacer`) y de **`Semana7/carrusel.py`** para la idea de moverse en ambos sentidos. Qué cambia para InsightHub:
- Se mueve a `estructuras/lista_doble.py`.
- Semana7 inserta **al final** y mueve `actual` hacia atrás con `deshacer`; la plaza inserta **al frente** (lo nuevo primero), así que se agrega `insertar_al_frente`.
- El cursor `actual` **sale de la lista**: Semana7 guarda uno solo, pero en la web varias sesiones recorren la misma plaza. Cada sesión guarda su propia referencia a un nodo (un *marcador*).
- `deshacer` y `rehacer` se reemplazan por `avanzar` y `retroceder` con paso de 5, que informan el límite en vez de imprimir.
- No es circular (el carrusel sí): en los extremos hay que informar el límite (CA-13).
- Se quitan los `print`: la lista devuelve resultados y la interfaz los muestra.

## 2. Estructura elegida y por qué
**Lista doblemente enlazada** con referencias a `cabeza` y `cola`, nodos con `anterior` y `siguiente`, y un contador.

La plaza recibe publicaciones al frente y se recorre en ambos sentidos desde una posición cualquiera. Con doble enlace, avanzar y retroceder desde un nodo cuestan O(1); con lista simple retroceder obligaría a recorrer desde el inicio, O(n).

## 3. Complejidad por operación
| Operación | Complejidad | Por qué |
|---|---|---|
| `insertar_al_frente(dato)` | O(1) | Enlaza antes de la cabeza |
| `inicio()` (marcador al primer nodo) | O(1) | Devuelve `cabeza` |
| `pagina(marcador)` | O(5) = O(1) | Lee 5 nodos desde el marcador |
| `avanzar(marcador)` | O(5) = O(1) | Sigue `siguiente` hasta 5 veces o hasta el final |
| `retroceder(marcador)` | O(5) = O(1) | Sigue `anterior` hasta 5 veces o hasta el inicio |
| `buscar_palabra(texto)` | O(n·m) | Recorre los n nodos y busca la subcadena en título y cuerpo (m = largo del texto) |
| `esta_vacia()`, `tamano()` | O(1) | Cabeza y contador |

## 4. Alternativas descartadas
| Alternativa | Por qué no |
|---|---|
| Lista simple | Retroceder es O(n) |
| Arreglo dinámico | Insertar al frente desplaza todo, O(n) |
| Cursor único dentro de la lista (Semana7) | Las sesiones web se pisarían entre sí |
| Índice invertido por palabra | Fuera de alcance; el recorrido basta para el volumen del proyecto (decisión en [`estructuras.md`](../00-producto/estructuras.md)) |

## 5. Orden de punteros
**Insertar al frente** (cuatro cambios, en este orden):
1. `nuevo.siguiente = cabeza`
2. Si hay cabeza, `cabeza.anterior = nuevo`; si no, `cola = nuevo`
3. `cabeza = nuevo`
4. `tamano += 1`

Si se mueve `cabeza` antes del paso 2, se pierde la referencia al nodo viejo y el enlace `anterior` queda sin actualizar: retroceder desde el segundo nodo saltaría a `None`.

**Marcador y nuevas publicaciones:** como la inserción es al frente y el marcador apunta a un nodo concreto, publicar no mueve el marcador de nadie (RF-07). Solo cambia «inicio».

## 6. Soporte interno
Ninguno. Solo nodos propios. La comparación de subcadenas usa los operadores de texto de Python sobre el contenido de una publicación, no como sustituto de la lista.

## 7. Módulos
`estructuras/lista_doble.py` · `dominio/feed.py` (sesión y marcador) · `dominio/busqueda.py` (palabra) · pruebas en `tests/test_lista_doble.py`.

## Historial de cambios
| Versión | Fecha | Cambio | Motivo |
|---|---|---|---|
| 1.0 | 2026-11-07 | Versión inicial | Creación |
| 1.1 | 2026-11-07 | Se declara el punto de partida (Semana7: lista doble y carrusel) y qué cambia, el marcador por sesión, páginas de 5, búsqueda por palabra O(n·m), orden de punteros y alternativas descartadas | El plan no decía de qué implementación partía ni justificaba las decisiones; decisiones tomadas en la consulta del componente |
