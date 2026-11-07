# Decisión de estructuras
Versión 1.2

Ocho estructuras, todas implementadas desde cero: lista simple, lista doble, pila, cola, árbol general, AVL, grafo y montículo.

## Carpeta de cada componente
| Estructura | Spec, plan y tasks |
|---|---|
| Lista doble | [`01-lista-doble/`](../01-lista-doble/spec.md) |
| Pila | [`02-pila/`](../02-pila/spec.md) |
| Cola | [`03-cola/`](../03-cola/spec.md) |
| Árbol general | [`04-arbol-general/`](../04-arbol-general/spec.md) |
| AVL | [`05-avl/`](../05-avl/spec.md) |
| Grafo | [`06-grafo/`](../06-grafo/spec.md) |
| Montículo | [`07-monticulo/`](../07-monticulo/spec.md) |
| Lista simple | [`08-lista-simple/`](../08-lista-simple/spec.md) |
| Sistema (cómo encajan) | [`99-sistema/`](../99-sistema/spec.md) |

## Decisión por capacidad

| Capacidad | HU | Estructura | Por qué esta | Alternativa descartada | Complejidad clave | Dónde se usa |
|---|---|---|---|---|---|---|
| Índice de usuarios y acceso por `@usuario` | HU-01, HU-02 | **AVL** | Garantiza unicidad y búsqueda con altura O(log n) aunque los usuarios lleguen ordenados | Tabla hash: no da orden alfabético ni búsqueda por prefijo | insertar y buscar O(log n) | `dominio/usuarios.py` |
| Amistades | HU-03 | **Grafo no dirigido con lista de adyacencia** | La red es dispersa: cada persona tiene pocos amigos entre los n posibles | Matriz de adyacencia: n² celdas casi vacías, O(n²) de memoria | agregar y quitar arista O(grado) · vecinos O(grado) | `dominio/red.py` |
| Representación de las relaciones | HU-03, HU-13 | **Lista de adyacencia** (frente a matriz de adyacencia) | Con n usuarios y pocos amigos cada uno, la lista guarda solo las aristas que existen: memoria O(n + m). Recorrer los amigos de alguien cuesta O(grado), que es lo que hace la búsqueda a 2 saltos | Matriz de adyacencia: memoria O(n²) casi toda vacía y listar amigos cuesta O(n); solo gana en «¿son amigos?» O(1) frente a O(grado), una consulta poco frecuente con grados pequeños | memoria O(n + m) · vecinos O(grado) · ¿son amigos? O(grado) | `estructuras/grafo.py` |
| Solicitudes de amistad pendientes | HU-03 | **Cola enlazada** (una por persona) | Se atienden en orden de llegada: encolar al final y desencolar al frente en O(1) | Arreglo dinámico: desencolar del inicio desplaza elementos, O(n) | encolar O(1) · desencolar O(1) | `dominio/amistades.py` |
| Personas conectadas | HU-04 | **Lista enlazada simple** | Entrar es insertar al inicio en O(1); listar cuesta O(conectados) y no O(todos los usuarios) | Recorrer todo el AVL en cada consulta: O(n) | insertar O(1) · listar O(c) · quitar O(c) | `dominio/presencia.py` |
| Plaza pública (feed) | HU-05 | **Lista doble** | Lo nuevo entra al frente y desde cualquier nodo se avanza o retrocede en ambos sentidos | Lista simple: retroceder exige recorrer desde el inicio, O(n) | insertar al frente O(1) · avanzar y retroceder O(1) | `dominio/feed.py` |
| Hilos de respuestas anidadas | HU-06 | **Árbol general** (hijo-izquierdo, hermano-derecho) + **Pila** para recorrerlo sin recursión | Una respuesta puede tener varias respuestas, y estas a su vez otras: es una jerarquía | Lista plana con id de padre: armar el hilo cuesta O(n) por consulta | responder O(n) por buscar al padre · recorrido completo O(n) | `dominio/hilos.py` |
| Votos de cada respuesta | HU-07 | **AVL** (clave `@usuario`, valor +1, −1 o 0 si retiró) | Comprobar si ya votó cuesta O(log n); cambiar o retirar es reemplazar el valor | Lista simple de votantes: O(n) por voto | buscar e insertar O(log n) | `dominio/votos.py` |
| Mejor respuesta de un hilo | HU-08 | **Árbol general** (recorrido del hilo) | Un hilo tiene pocas respuestas y ya están en el árbol: no hace falta otra estructura | Montículo por hilo: complejidad extra sin ganancia real | recorrido O(n) | `dominio/hilos.py` |
| Publicación destacada | HU-09 | **Montículo máximo** | La más activa es la cima: consultar O(1), actualizar O(log n) | Reordenar toda la plaza en cada cambio: O(n log n) | insertar y extraer O(log n) · máximo O(1) | `dominio/destacada.py` |
| Búsqueda de usuarios por nombre | HU-10 | **AVL** (por nombre y por `@usuario`) | Prefijo y orden alfabético en O(log n + k) | Recorrer todos los usuarios: O(n) | prefijo O(log n + k) | `dominio/usuarios.py` |
| Búsqueda de publicaciones por fecha | HU-10 | **AVL** (clave `AAAA-MM-DD\|id`) | Todas las de un día se obtienen sin recorrer la plaza, O(log n + k) | Recorrer la lista doble: O(n) | prefijo de fecha O(log n + k) | `dominio/busqueda.py` |
| Búsqueda de publicaciones por palabra | HU-10 | **Recorrido de la lista doble** | Hay que leer el texto de cada publicación; un índice por palabra excede el alcance | Índice invertido por palabra: demasiado para este proyecto | recorrido O(n) | `dominio/busqueda.py` |
| Historial de pantallas («atrás») | HU-11 | **Pila** | «Atrás» vuelve a lo último visitado: LIFO | Lista doble con cursor: no se necesita «adelante» | apilar y desapilar O(1) | `dominio/navegacion.py` |
| Notificaciones pendientes | HU-12 | **Cola enlazada** (frente y final) | Se leen en orden de llegada: O(1) con dos referencias | Arreglo dinámico: desencolar del inicio es O(n) | encolar y desencolar O(1) | `dominio/notificaciones.py` |
| Recomendaciones («quizá conozcas») | HU-13 | **Grafo** (BFS a 2 saltos) + **Montículo máximo** para los k mejores | Amigos de amigos es el nivel 2 del BFS; el montículo extrae los k con más amigos en común | DFS: no respeta la cercanía. Ordenar todos los candidatos: O(m log m) | BFS acotado O(V + E) de la vecindad · extraer k, O(k log m) | `dominio/recomendaciones.py` |

La búsqueda por palabra es CA-29 (Must) y la búsqueda por fecha es CA-39 (Should).

HU-14 (consola y web) no tiene estructura propia: es la interfaz que usa todas las anteriores y se explica en [`99-sistema/spec.md`](../99-sistema/spec.md).

## Fuera de alcance (Won't)
A* (opcional en la temática), persistencia en archivo o base de datos y matriz dispersa. Ver [`moscow.md`](moscow.md).

## Soporte interno permitido (justificado)
- **Grafo:** un arreglo de Python indexado por id guarda la cabeza de cada lista de adyacencia. Las aristas son nodos enlazados propios.
- **Montículo:** un arreglo de Python guarda el árbol completo; no se usa `heapq`.
- **Acceso a usuarios por id:** un arreglo de Python indexado por id (arreglo dinámico del catálogo).
Ninguno sustituye una estructura declarada; cada uno se detalla en el `plan.md` del componente.

## Historial de cambios
| Versión | Fecha | Cambio | Motivo |
|---|---|---|---|
| 1.0 | 2026-11-07 | Tabla inicial (6 estructuras) | Creación |
| 1.1 | 2026-11-07 | Se asigna una estructura a cada historia aprobada (HU-01 a HU-13). Se suman lista simple y montículo; la red pasa de dirigida a no dirigida; se agregan solicitudes, votos, destacada y búsquedas por fecha y palabra | Las historias v1.1 agregaron amistad con solicitud, presencia, votos y destacada |
| 1.2 | 2026-11-07 | Agrega la fila «representación de las relaciones» (lista de adyacencia frente a matriz), la tabla de carpetas de cada componente con enlaces a `01-…` a `08-…` y `99-sistema`, la ruta corregida de HU-14 y la separación palabra (CA-29) / fecha (CA-39) | Faltaba justificar la representación del grafo; las carpetas se renombraron; las historias v1.2 separaron CA-29 y CA-39 |
