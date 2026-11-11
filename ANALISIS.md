# Análisis de complejidad
Fuente: los `plan.md` de cada componente en `specs/`. Versión final de la entrega: están implementadas siete de las ocho estructuras declaradas, con todas las historias Must. La **lista simple** (conectados, HU-04) y las operaciones de las historias Should figuran «no implementada (Should)».

n = elementos de la estructura · k = resultados · g = grado · c = conectados · V, E = vértices y aristas.

| Estructura | Operación | Complejidad | Estado |
|---|---|---|---|
| Lista doble | insertar_al_frente | O(1) | implementada (`estructuras/lista_doble.py`) |
| Lista doble | inicio / pagina / avanzar / retroceder (página de 5) | O(1) | implementada |
| Búsqueda | buscar_palabra (recorre la plaza) | O(n·m) | implementada (`dominio/busqueda.py`) |
| Pila | apilar / desapilar / tope / esta_vacia / tamano | O(1) | implementada (`estructuras/pila.py`) |
| Navegación | ir_a / atras | O(1) | implementada (`dominio/navegacion.py`) |
| Cola | encolar / desencolar / frente / esta_vacia / tamano | O(1) | implementada (`estructuras/cola.py`) |
| Cola | contiene | O(k) | implementada |
| Notificaciones | notificar | O(1) amortizado | implementada (`dominio/notificaciones.py`) |
| Notificaciones | leer | O(k) | implementada |
| Amistades | enviar | O(log n + g + k) | implementada (`dominio/amistades.py`) |
| Amistades | primera / pendientes | O(1) | implementada |
| Amistades | atender / amigos | O(g) | implementada |
| Amistades | deshacer | O(log n + g) | implementada |
| Árbol general | abrir_hilo / tamano | O(1) | implementada (`estructuras/arbol_general.py`) |
| Árbol general | responder / buscar / recorrer / profundidad | O(n) | implementada |
| Hilos | publicar | O(1) amortizado | implementada (`dominio/hilos.py`) |
| Hilos | responder / mostrar | O(n) | implementada |
| Árbol general | aceptar | O(n) | no implementada (Should) |
| Árbol general | mejor_respuesta | O(k) | no implementada (Should) |
| AVL | insertar / buscar | O(log n) | implementada (`estructuras/avl.py`) |
| AVL | reemplazar | O(log n) | no implementada (Should: votos) |
| AVL | recorrer_en_orden | O(n) | implementada |
| AVL | altura / tamano | O(1) | implementada |
| AVL | buscar_por_prefijo | O(log n + k) | implementada |
| Usuarios | crear_perfil / entrar / buscar | O(log n) | implementada (`dominio/usuarios.py`) |
| Usuarios | buscar_por_prefijo | O(log n + k) | implementada |
| Usuarios | por_id | O(1) | implementada |
| Usuarios | generar_comunidad | O(n log n) | implementada |
| Grafo | agregar_vertice | O(1) amortizado | implementada (`estructuras/grafo.py`) |
| Grafo | agregar_amistad / eliminar_amistad / son_amigos / amigos | O(g) | implementada |
| Grafo | candidatos_dos_saltos | O(V + g + E′) | implementada |
| Montículo | insertar / extraer_maximo | O(log n) | implementada (`estructuras/monticulo.py`) |
| Montículo | actualizar | O(log n) | no implementada (Should: destacada) |
| Montículo | maximo | O(1) | implementada |
| Montículo | construir | O(m) | implementada |
| Recomendaciones | recomendar (5 mejores de m candidatos) | O(V + g + E′ + m + 5 log m) | implementada (`dominio/recomendaciones.py`) |
| Lista simple | conectar / registrar_actividad / salir / caducar / listar | O(c) | no implementada (Should) |

## Análisis por estructura implementada
**Lista doble (plaza).** Insertar al frente solo cambia dos punteros y el marcador de cada sesión se mueve de 5 en 5 siguiendo `siguiente`/`anterior`, así que todo el recorrido paginado es O(1) por página. Se descartó el arreglo de Python porque insertar al frente desplaza todos los elementos (O(n)). El costo está en la búsqueda por palabra, que recorre toda la plaza: O(n·m).

**Pila (historial).** Apilar y desapilar tocan solo la cima, O(1). Una lista con índices serviría igual, pero la pila enlazada no reserva espacio de más y deja claro que «atrás» solo mira la pantalla anterior.

**Cola (solicitudes y notificaciones).** Encolar por el final y desencolar por el frente son O(1) con referencia al último nodo; el orden de llegada sale gratis. `contiene` recorre la cola (O(k)), pero k es pequeña (solicitudes pendientes de una persona). Una pila entregaría primero lo más nuevo, contra la regla de «en orden de llegada».

**AVL (usuarios).** Con 120 perfiles sembrados que pueden llegar ya ordenados, un árbol sin equilibrar tendría altura cercana a n; el AVL la mantiene en O(log n) con las cuatro rotaciones, y buscar por prefijo cuesta O(log n + k) porque las claves con un prefijo son un tramo contiguo. El `dict` de Python daría O(1) exacto, pero no orden alfabético ni prefijo.

**Grafo (amistades).** La red es dispersa: cada persona tiene pocos amigos entre todas las posibles. La lista de adyacencia usa memoria O(V + E) y listar amigos cuesta O(g); la matriz gastaría O(V²) casi vacía y listar costaría O(V). Comprobar si dos personas son amigas cuesta O(g) en vez de O(1), que es lo que se cede, aceptable con grados pequeños. Los candidatos a 2 saltos salen de un recorrido por niveles con la cola propia, y cada candidato se encuentra una vez por cada amigo en común, así que contar es gratis.

**Árbol general (hilos).** Una respuesta puede tener cualquier cantidad de respuestas. Con los dos enlaces primer hijo y hermano derecho no hace falta una `list` por nodo. `responder` cuesta O(n) porque busca al padre recorriendo el hilo; se acepta porque un hilo tiene decenas de nodos, y un índice AVL por id bajaría a O(log n) a cambio de otra estructura. El recorrido usa la pila propia y no la recursión de Python: un hilo de 2000 niveles se recorre sin agotarla (prueba `test_hilo_de_2000_niveles_no_agota_la_recursion`).

**Montículo (recomendaciones).** Solo se necesitan los 5 mejores de m candidatos: `construir` cuesta O(m) y sacar 5 cuesta O(5 log m), frente a O(m log m) de ordenarlos todos. No se usa `heapq`.

**Lista simple (conectados).** Diseñada en `specs/08-lista-simple/`, pero no implementada: HU-04 es Should y no alcanzó la capacidad.

## Comparaciones con la alternativa descartada
Medición propia con `docs/evidencias/medir.py` (mediana de 7 repeticiones, Python 3.13, Windows 11). Datos en `docs/evidencias/mediciones.csv`. Los tiempos dependen de la máquina y del momento: dos corridas previas dieron la misma tendencia con ruido visible en algunos puntos. Lo determinista son la altura y el número de comparaciones.

### 1. AVL frente a árbol de búsqueda sin equilibrar
Claves que llegan ya ordenadas, el peor caso del árbol sin equilibrar.

| n | Altura AVL | Altura sin equilibrar | Insertar todo AVL (ms) | Insertar todo sin equilibrar (ms) | Buscar AVL (µs) | Buscar sin equilibrar (µs) |
|---|---|---|---|---|---|---|
| 1 000 | 9 | 999 | 3.88 | 18.95 | 0.559 | 53.86 |
| 2 000 | 10 | 1 999 | 8.68 | 75.17 | 0.638 | 108.28 |
| 4 000 | 11 | 3 999 | 19.05 | 300.68 | 0.671 | 213.68 |
| 8 000 | 12 | 7 999 | 40.59 | 1 199.12 | 0.954 | 454.39 |

Al duplicar n, insertar todo sin equilibrar se multiplica por 4 (O(n²) en total) y buscar por 2 (O(n)); en el AVL insertar todo apenas se duplica (O(n log n)) y buscar casi no cambia (O(log n)). Con 8 000 claves la búsqueda es unas 470 veces más lenta sin equilibrar. El precio del AVL es el código de las rotaciones.

### 2. Lista doble frente a arreglo de Python (publicar al frente)
Costo de una publicación sobre una plaza de tamaño n.

| n | Lista doble (µs) | Arreglo con `insert(0, x)` (µs) |
|---|---|---|
| 1 000 | 0.204 | 1.304 |
| 10 000 | 0.192 | 3.257 |
| 100 000 | 0.187 | 27.991 |
| 400 000 | 0.547 | 667.491 |

La lista doble se mantiene plana (O(1)) y el arreglo crece con n (O(n)). El punto de 400 000 es el más ruidoso: en otra corrida el arreglo dio 129 µs y la lista 0.216 µs. El desplazamiento del arreglo lo hace código en C, por eso con pocos miles de publicaciones la diferencia es de microsegundos: la ventaja de la lista doble es de escala, y además da avanzar y retroceder por página sin índices.

### 3. Montículo frente a ordenar todos los candidatos (5 mejores)
Las dos versiones usan la misma función de comparación escrita en Python y devuelven el mismo resultado (se comprueba en el script).

| m | Comparaciones montículo | Comparaciones ordenar | Montículo (ms) | Ordenar (ms) |
|---|---|---|---|---|
| 1 000 | 1 978 | 8 631 | 1.96 | 6.98 |
| 10 000 | 18 929 | 120 252 | 22.63 | 112.78 |
| 100 000 | 188 347 | 1 531 684 | 234.52 | 1 609.52 |

El montículo hace cerca de 2 comparaciones por candidato (lineal) y ordenar crece como m log m: con 100 000 candidatos son unas 8 veces menos comparaciones. Con los 120 perfiles de la demostración la diferencia no se nota; la decisión se justifica por el crecimiento. No se comparó contra `sorted` sin función de comparación, que corre en C y sería más rápido en la práctica para claves simples.
