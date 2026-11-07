# Plan — Árbol general (hilos)
Versión 1.1

## 1. De qué implementación mía parto
De **`Semana10/arbol_binario.py`** (`NodoArbol` con dos enlaces) y de **`Semana10/arbol_carpetas.py`** (recorrido con contenedor propio, versión con pila de `recorridos.md`). Qué cambia para InsightHub:
- El `NodoArbol` binario tiene `izquierdo` y `derecho`. Aquí esos dos enlaces pasan a significar **primer hijo** y **hermano derecho**: con solo dos enlaces se representa un árbol con cualquier cantidad de hijos.
- `arbol_carpetas.py` guarda los hijos en una `list` de Python (permitido allí como soporte). Aquí **no**: la lista de hijos se reemplaza por la cadena de hermanos, para no depender de una estructura nativa.
- Mis recorridos de Semana10 son recursivos. Aquí el recorrido usa la pila propia ([`02-pila`](../02-pila/plan.md)), sin recursión, de modo que un hilo muy profundo no agote la recursión de Python.
- Cada nodo guarda: identificador, autor, texto, puntaje neto (lo actualizan los votos) y los dos enlaces. El hilo guarda su raíz, su tamaño y cuál es la respuesta aceptada.

## 2. Estructura elegida y por qué
**Árbol general en representación primer-hijo / hermano-derecho**, un árbol por publicación (la raíz es la publicación), con la pila propia para recorrerlo.

Una respuesta puede tener varias respuestas, y estas a su vez otras: es una jerarquía de ancho variable. Con un árbol por publicación, buscar al padre solo mira ese hilo (decenas de nodos) y no toda la plaza. La mejor respuesta se calcula sobre ese mismo árbol, sin otra estructura.

## 3. Complejidad por operación
n = nodos del hilo; k = respuestas de primer nivel.
| Operación | Complejidad | Por qué |
|---|---|---|
| `abrir_hilo(dato)` | O(1) | Crea la raíz |
| `buscar(id)` | O(n) | Recorrido con pila hasta hallar el id |
| `responder(id_padre, id_nuevo, dato)` | O(n) | Buscar al padre O(n) + llegar al final de sus hijos, que es como máximo O(n) |
| `recorrer()` (hilo con niveles) | O(n) | Cada nodo entra y sale una vez de la pila |
| `profundidad(id)` | O(n) | Se recorre llevando el nivel de cada nodo |
| `tamano()` | O(1) | Contador |
| `aceptar(id, quien)` | O(n) | Buscar la respuesta y comprobar que es de primer nivel |
| `mejor_respuesta()` | O(k) | Recorre solo las de primer nivel |

Memoria: O(n).

## 4. Alternativas descartadas
| Alternativa | Por qué no |
|---|---|
| Lista plana con id del padre | Armar el hilo con sangría cuesta O(n) por consulta y exige ordenar |
| Árbol con `list` de hijos (Semana10 `arbol_carpetas`) | Es una estructura nativa como soporte de la declarada; hijo-izquierdo/hermano-derecho usa solo nodos propios |
| Un único árbol con todas las publicaciones | Buscar al padre recorrería toda la plaza |
| Recorrido recursivo | Un hilo muy profundo podría pasar el límite de recursión |
| Índice AVL de id → nodo | `responder` bajaría a O(log n), pero agrega otra estructura y horas sin ganancia con hilos de decenas de nodos |
| Guardar el último hijo en cada nodo | Evitaría recorrer los hermanos, pero el costo está dominado por buscar al padre; no se justifica |

## 5. Recorrido con pila y orden de punteros
Para recorrer: apilar la raíz con nivel 0. Mientras la pila no esté vacía: desapilar, visitar, **apilar primero el hermano derecho** (con el mismo nivel) y **después el primer hijo** (con nivel + 1).

Se apila en ese orden porque la pila saca lo último que entró: el primer hijo sale antes que el hermano, así se baja por una rama completa y luego se sigue con los hermanos. Si se apilara al revés, saldría primero el hermano y las respuestas quedarían fuera de su padre. Es el mismo razonamiento que en `recorridos.md` (con la pila, el último que entra sale primero).

**Agregar un hijo:** se recorre la cadena de hermanos del padre hasta el último y se enlaza ahí (`ultimo.derecho = nuevo`); si el padre no tiene hijos, `padre.izquierdo = nuevo`. Se incrementa el tamaño solo después de enlazar, así un fallo antes no deja el contador desfasado.

**Mostrar con la fijada:** primero se muestra la publicación; luego el subárbol de la respuesta fijada con sus niveles; luego el resto de las de primer nivel en orden cronológico, saltándose la fijada.

## 6. Mejor respuesta (Should)
- Si hay aceptada, es la fijada. `aceptar` comprueba, en este orden: que quien acepta es el autor de la publicación, que la respuesta existe, que es de primer nivel y que no hay otra aceptada. Si todo se cumple guarda la aceptada y el dominio suma 15 puntos al autor (`dominio/hilos.py` llama a `dominio/usuarios.py`).
- Si no hay aceptada, `mejor_respuesta` recorre las respuestas de primer nivel y se queda con la de mayor puntaje neto; compara con `>` estricto, así en un empate gana la primera encontrada, que es la más antigua. Si el mayor puntaje no es positivo, no hay fijada.

## 7. Soporte interno
Ninguno. Solo nodos propios y la pila del proyecto.

## 8. Módulos
`estructuras/arbol_general.py` · `dominio/hilos.py` · pruebas en `tests/test_arbol_general.py`.

## Historial de cambios
| Versión | Fecha | Cambio | Motivo |
|---|---|---|---|
| 1.0 | 2026-11-07 | Versión inicial | Creación |
| 1.1 | 2026-11-07 | Se declara el punto de partida (`NodoArbol` y `arbol_carpetas` de Semana10) y qué cambia; un árbol por publicación; recorrido con pila y su orden de punteros; mejor respuesta; alternativas descartadas | El plan no decía de qué implementación partía ni justificaba las decisiones; decisiones tomadas en la consulta del componente |
