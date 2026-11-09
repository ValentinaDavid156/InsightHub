# Plan — Grafo
Versión 1.2

## 1. De qué implementación mía parto
No tengo un grafo propio en el repositorio. Parto de dos piezas mías:
- **`Semana5/nodo.py`** (`Nodo` con `dato` y `siguiente`): cada arista es un nodo de la lista de adyacencia de una persona, con `dato` = id del amigo.
- **`Semana10/cola.py`** (`ColaEnlazada`): el recorrido por niveles para llegar a los amigos de los amigos.

Qué cambia para InsightHub: el grafo es nuevo y lo escribo desde cero. Es **no dirigido**: la amistad se guarda en las dos listas a la vez, de modo que `a ∈ lista(b) ⇔ b ∈ lista(a)`, nunca hay una persona consigo misma ni repetida (la versión anterior era dirigida, de «seguimientos»).

## 2. Estructura elegida y por qué
**Grafo no dirigido con lista de adyacencia**: un arreglo indexado por el id de la persona guarda la cabeza de su lista de amigos (nodos propios) y su grado. Justificación de la representación (frente a la matriz) en [`estructuras.md`](../00-producto/estructuras.md): la red es dispersa, la lista usa memoria O(V + E) y listar amigos cuesta O(grado).

## 3. Complejidad por operación
V = personas; g = grado de la persona; E′ = suma de los grados de los amigos de la persona consultada.
| Operación | Complejidad | Por qué |
|---|---|---|
| `agregar_vertice(id)` | O(1) amortizado | Agrega una posición al arreglo |
| `agregar_amistad(a, b)` | O(g) | Comprobar duplicado recorriendo la lista de `a`; luego dos inserciones al inicio, O(1) |
| `eliminar_amistad(a, b)` | O(g_a + g_b) | Busca con su predecesor en cada lista y la desenlaza |
| `son_amigos(a, b)` | O(g) | Recorre la lista más corta de las dos |
| `amigos(id)` | O(g) | Recorre la lista (ya está de la más reciente a la más antigua) |
| `grado(id)` | O(1) | Contador por persona |
| `candidatos_dos_saltos(u)` | O(V + g + E′) | Crear los arreglos temporales cuesta O(V); luego se recorre solo la vecindad |

## 4. Alternativas descartadas
| Alternativa | Por qué no |
|---|---|
| Matriz de adyacencia | O(V²) de memoria casi vacía; listar amigos cuesta O(V) |
| Lista de aristas sueltas | Listar los amigos de una persona recorre todas las aristas, O(E) |
| DFS para llegar a 2 saltos | No respeta la cercanía; el nivel 2 es exactamente lo que da el recorrido por niveles |
| AVL de candidatos para contar amigos en común | O(log m) por visita, pero otra dependencia entre componentes sin ganancia con redes pequeñas (decisión en la consulta) |
| Guardar la lista ordenada alfabéticamente | Obliga a insertar en el medio o a ordenar al consultar; la amistad más reciente primero es inserción al inicio (decisión en la consulta) |

## 5. Orden de punteros
**Crear amistad** (todo se valida antes de tocar algo):
1. Comprobar que `a` y `b` existen, que `a ≠ b` y que `b` no está ya en la lista de `a`.
2. Insertar `b` al inicio de la lista de `a`: `nuevo.siguiente = cabeza_a`, luego `cabeza_a = nuevo`.
3. Insertar `a` al inicio de la lista de `b` del mismo modo.
4. Subir el grado de ambos.
Se valida primero para que nunca quede la amistad en un solo sentido; si la primera inserción pudiera fallar, el invariante `a ∈ lista(b) ⇔ b ∈ lista(a)` se rompería. Dentro de cada inserción se asigna primero `nuevo.siguiente` y después la cabeza: al revés se pierde el resto de la lista (la misma pérdida de referencias de mis notas de Semana5).

**Deshacer amistad:** recorrer la lista de `a` con el nodo anterior; si `b` no está, terminar sin tocar nada. Si está: `anterior.siguiente = actual.siguiente` (o `cabeza = actual.siguiente` si era el primero); y repetir en la lista de `b`. Se desenlaza antes de soltar la referencia del nodo para no perder lo que sigue. Los casos son: primero, intermedio y último.

## 6. Candidatos a 2 saltos
Uso dos arreglos temporales del tamaño de V, indexados por id (soporte interno, declarado abajo): `excluido` y `comunes`.
1. Marcar `excluido[u]` y el de cada amigo de `u`.
2. Encolar los amigos de `u` en la `ColaEnlazada` (nivel 1).
3. Mientras la cola no esté vacía: desencolar un amigo `f`; para cada vecino `w` de `f`, si `w` no está excluido: si `comunes[w]` era 0, agregar `w` a la lista de candidatos; sumar 1 a `comunes[w]`.
4. Devolver los candidatos, cada uno con `comunes[w]`.
El número de amigos en común sale gratis: `w` se encuentra una vez por cada amigo de `u` que lo conoce. Si `u` no tiene amigos, la cola nace vacía y el resultado es vacío (CA-36).

## 7. Soporte interno
- Arreglo de Python indexado por id con la cabeza de cada lista de adyacencia y el grado, declarado en [`estructuras.md`](../00-producto/estructuras.md). Las aristas son nodos enlazados propios.
- Dos arreglos temporales por consulta (`excluido`, `comunes`), tamaño V, justificados porque dan acceso O(1) por id y se descartan al terminar.
- Lista de Python como contenedor del **resultado** (candidatos y amigos), no como estructura de datos del grafo.

## 8. Módulos
`estructuras/grafo.py` · `dominio/amistades.py` · `dominio/recomendaciones.py` (usa también [`07-monticulo`](../07-monticulo/plan.md)) · pruebas en `tests/test_grafo.py`.

## 9. Decisiones tomadas al implementar (todas de Valentina)
- **Rechazos:** `agregar_amistad` y `eliminar_amistad` devuelven `True` si cambiaron algo y `False` si se rechazan (la misma persona, repetida, persona inexistente, amistad que no existe), sin tocar nada; el mensaje claro lo pone el dominio. Igual que `AVL.insertar`.
- **Candidatos:** `candidatos_dos_saltos` devuelve una lista de `(id, comunes)` en el orden en que se descubren; ordenarlos es del montículo.
- **Ids:** `agregar_vertice(id)` acepta un entero >= 0 (si no, `ValueError`), es idempotente y registra también los ids intermedios que falten. Una consulta con un id inválido o inexistente da `[]`, `0` o `False`, sin error.
- **Extra:** `cantidad()` devuelve las personas registradas.

## Historial de cambios
| Versión | Fecha | Cambio | Motivo |
|---|---|---|---|
| 1.0 | 2026-11-07 | Versión inicial | Creación |
| 1.1 | 2026-11-07 | Pasa de dirigido a no dirigido; se declara el punto de partida (`Nodo` de Semana5 y `ColaEnlazada` de Semana10); orden de punteros al crear y deshacer; candidatos a 2 saltos con arreglos temporales; alternativas descartadas | El plan seguía siendo del grafo dirigido de «seguimientos»; decisiones tomadas en la consulta del componente |
| 1.2 | 2026-11-08 | Sección 9 con las decisiones de implementación: rechazos con True/False, candidatos como (id, comunes) e ids | Al implementar hubo que cerrar detalles que el plan no fijaba; decisiones de Valentina |
