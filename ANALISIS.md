# Análisis de complejidad
Fuente: los `plan.md` de cada componente en `specs/`. Se completa a medida que se implementa; hoy están implementadas la **pila**, la **cola** (con las notificaciones), la **lista doble** (con la plaza y la búsqueda por palabra) y el **AVL** (con los usuarios); las demás figuran «pendiente».

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
| Grafo | agregar_vertice | O(1) amortizado | pendiente |
| Grafo | agregar_amistad / eliminar_amistad / son_amigos / amigos | O(g) | pendiente |
| Grafo | candidatos_dos_saltos | O(V + g + E′) | pendiente |
| Montículo | insertar / extraer_maximo / actualizar | O(log n) | pendiente |
| Montículo | maximo | O(1) | pendiente |
| Montículo | construir | O(m) | pendiente |
| Lista simple | conectar / registrar_actividad / salir / caducar / listar | O(c) | pendiente |

## Comparaciones con la alternativa descartada
(Pendiente: al menos dos, con medición empírica si es posible. Una medición ya planeada: `specs/07-monticulo/tasks.md`, tarea T-07.17.)
