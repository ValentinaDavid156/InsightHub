# Análisis de complejidad
Fuente: los `plan.md` de cada componente en `specs/`. Se completa a medida que se implementa; hoy están implementadas la **pila**, la **cola** (con las notificaciones), la **lista doble** (con la plaza y la búsqueda por palabra), el **AVL** (con los usuarios), el **grafo** y las **amistades** que unen cola y grafo; las demás figuran «pendiente».

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
| Árbol general | abrir_hilo / tamano | O(1) | pendiente |
| Árbol general | responder / buscar / recorrer / profundidad / aceptar | O(n) | pendiente |
| Árbol general | mejor_respuesta | O(k) | pendiente |
| AVL | insertar / buscar | O(log n) | implementada (`estructuras/avl.py`) |
| AVL | reemplazar | O(log n) | pendiente (Should: votos) |
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
| Montículo | insertar / extraer_maximo / actualizar | O(log n) | pendiente |
| Montículo | maximo | O(1) | pendiente |
| Montículo | construir | O(m) | pendiente |
| Lista simple | conectar / registrar_actividad / salir / caducar / listar | O(c) | pendiente |

## Análisis por estructura implementada (entrega 2)
**Lista doble (plaza).** Insertar al frente solo cambia dos punteros y el marcador de cada sesión se mueve de 5 en 5 siguiendo `siguiente`/`anterior`, así que todo el recorrido paginado es O(1) por página. Se descartó el arreglo de Python porque insertar al frente desplaza todos los elementos (O(n)). El costo está en la búsqueda por palabra, que recorre toda la plaza: O(n·m).

**Pila (historial).** Apilar y desapilar tocan solo la cima, O(1). Una lista con índices serviría igual, pero la pila enlazada no reserva espacio de más y deja claro que «atrás» solo mira la pantalla anterior.

**Cola (solicitudes y notificaciones).** Encolar por el final y desencolar por el frente son O(1) con referencia al último nodo; el orden de llegada sale gratis. `contiene` recorre la cola (O(k)), pero k es pequeña (solicitudes pendientes de una persona). Una pila entregaría primero lo más nuevo, contra la regla de «en orden de llegada».

**AVL (usuarios).** Con 120 perfiles sembrados que pueden llegar ya ordenados, un árbol sin equilibrar tendría altura cercana a n; el AVL la mantiene en O(log n) con las cuatro rotaciones, y buscar por prefijo cuesta O(log n + k) porque las claves con un prefijo son un tramo contiguo. El `dict` de Python daría O(1) exacto, pero no orden alfabético ni prefijo.

## Comparaciones con la alternativa descartada
(Pendiente: al menos dos, con medición empírica si es posible. Una medición ya planeada: `specs/07-monticulo/tasks.md`, tarea T-07.17.)
