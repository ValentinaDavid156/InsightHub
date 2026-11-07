# Decisión de estructuras

| Capacidad | Estructura | Por qué esta | Alternativa descartada | Complejidad clave | Dónde se usa |
|---|---|---|---|---|---|
| Feed de preguntas de un usuario | **Lista doble** | Lo nuevo entra al frente y se navega en ambos sentidos desde cualquier pregunta; con cursor, avanzar/retroceder es O(1). | Lista simple: retroceder exige recorrer desde el inicio, O(n). | insertar al frente O(1) · avanzar/retroceder O(1) | `dominio/feed.py` |
| Historial de pantallas | **Pila** | «Atrás» regresa a lo último visitado: LIFO. | Lista doble con cursor: más compleja de lo que se necesita; no requiere «adelante». | apilar O(1) · desapilar O(1) | `dominio/navegacion.py` |
| Notificaciones pendientes | **Cola enlazada** (frente y final) | Se leen en orden de llegada: encolar al final y desencolar al frente O(1) con dos referencias. | Arreglo dinámico: desencolar del inicio desplaza elementos, O(n). | encolar O(1) · desencolar O(1) | `dominio/notificaciones.py` |
| Hilos de comentarios anidados | **Árbol general (n-ario)** | Cada comentario tiene cualquier número de respuestas, y estas a su vez otras: es una jerarquía. | Lista plana con id de padre: reconstruir el hilo exige recorrer todo, O(n) por consulta anidada. | responder O(h) buscando el padre · recorrido completo O(n) | `dominio/hilos.py` |
| Índice de usuarios y búsqueda por nombre | **Árbol AVL** | Búsqueda por prefijo y recorrido alfabético, con O(log n) garantizado. | BST simple: con inserciones ordenadas degenera a O(n). Tabla hash: no da orden alfabético ni prefijo. | insertar/buscar O(log n) · recorrido en orden O(n) | `dominio/usuarios.py` |
| Red de seguimiento | **Grafo dirigido con lista de adyacencia** | La red es dispersa (cada usuario sigue a pocos de los n posibles). | Matriz de adyacencia densa: n² celdas casi vacías, O(n²) memoria. | agregar arista O(1)* · vecinos O(grado) | `dominio/red.py` |
| Recomendaciones («quizá conozcas») | **BFS limitado a 2 saltos** sobre el grafo | Amigos de amigos = nivel 2 de BFS; recorre solo lo cercano. | DFS: no respeta la cercanía por saltos. | O(V + E) acotado a la vecindad de 2 saltos | `dominio/recomendaciones.py` |

\* O(1) amortizado si se evita el duplicado con control de pertenencia; si se verifica recorriendo la lista del origen, O(grado).

## Soporte interno permitido (justificado)
Para el índice del grafo (usuario → su lista de adyacencia) se usa un arreglo base de Python indexado por id de usuario (ids 0..n−1). Es soporte interno, no sustituye ninguna estructura declarada. Documentar en `specs/06-grafo/plan.md`.

## Historial de cambios
| Versión | Fecha | Cambio | Motivo |
|---|---|---|---|
| 1.0 | 2026-11-07 | Tabla inicial | Creación |
