# Plan — Montículo máximo
Versión 1.1

## 1. De qué implementación mía parto
**No tengo un montículo en el repositorio.** De **`Semana10/cola_prioridad.py`** (`ColaPrioridad`) tomo solo la idea de desempatar con una **clave compuesta** (`nivel efectivo, llegada, orden`) y de que el tiempo o el orden los aporte quien llama para que sea determinista y probable. Qué cambia para InsightHub:
- Mi `ColaPrioridad` es de tres niveles fijos con una cola FIFO por nivel; un montículo es un árbol completo guardado por posiciones, con prioridades arbitrarias. Es nuevo y lo escribo desde cero.
- La comparación no está fija: el montículo recibe una función `antes(a, b)` que dice cuál va primero, y así sirve para las dos tareas (actividad y amigos en común).
- No uso `heapq`.

## 2. Estructura elegida y por qué
**Montículo máximo binario** guardado en un arreglo: el hijo izquierdo de la posición `i` está en `2i+1`, el derecho en `2i+2`, el padre en `(i−1)//2`; el mayor siempre está en la posición 0.

| Uso | Elemento | `antes(a, b)` |
|---|---|---|
| Destacada | id de publicación y su actividad | mayor actividad; si empata, mayor id (más reciente) |
| Recomendaciones | id de persona y sus amigos en común | más amigos en común; si empata, `@usuario` alfabéticamente menor |

La destacada cambia con cada respuesta o voto: leer el mayor tiene que ser O(1) y reacomodar O(log n); reordenar toda la plaza costaría O(n log n). Para las recomendaciones solo se necesitan los 5 mejores de m candidatos: construir el montículo cuesta O(m) y sacar 5 cuesta O(5 log m), mejor que ordenar los m candidatos en O(m log m).

## 3. Complejidad por operación
n = elementos del montículo.
| Operación | Complejidad | Por qué |
|---|---|---|
| `insertar(id, valor)` | O(log n) | Se agrega al final y se sube |
| `maximo()` | O(1) | Posición 0 |
| `extraer_maximo()` | O(log n) | Se mueve el último a la raíz y se baja |
| `actualizar(id, valor)` | O(log n) | Con la posición guardada, se sube o se baja desde ahí |
| `construir(candidatos)` | O(m) | Bajar desde el último padre hasta la raíz |
| `esta_vacio()`, `tamano()` | O(1) | Contador |
| Destacada tras un cambio | O(log n) | Una `actualizar` |
| 5 mejores recomendaciones | O(m + 5 log m) | `construir` y 5 `extraer_maximo` |

## 4. Alternativas descartadas
| Alternativa | Por qué no |
|---|---|
| Recorrer todas las publicaciones para hallar la mayor | O(n) por consulta o cambio |
| Reordenar la plaza en cada cambio | O(n log n) por cambio |
| Insertar de nuevo y descartar la entrada vieja al consultar | El montículo crece con cada cambio y `maximo` deja de ser O(1) (decisión en la consulta) |
| Lista ordenada | Insertar es O(n) |
| AVL por actividad | Mantener la clave cambiando exige borrar e insertar; consultar el mayor es O(log n) y no O(1) |
| Ordenar los m candidatos para sacar 5 | O(m log m), más que construir el montículo y extraer 5 |

## 5. Orden de intercambios y posiciones
Cada intercambio de dos posiciones mueve **tres** cosas que deben cambiar juntas: los dos elementos en el arreglo y las posiciones guardadas de los dos ids. El orden es:
1. Guardar el elemento de la posición `i` en una variable temporal.
2. Copiar el de `j` a `i` y actualizar `pos[id_j] = i`.
3. Poner el temporal en `j` y actualizar `pos[id_i] = j`.
Si se actualizan las posiciones antes de mover los elementos, o se olvida una de las dos, `actualizar` sube o baja desde una posición equivocada y la destacada queda mal sin fallar (el error más difícil de ver).

**`subir(i)`:** mientras `i > 0` y el elemento va `antes` que su padre, intercambiar con el padre.
**`bajar(i)`:** elegir el hijo que va `antes` entre los dos y, si va `antes` que el elemento, intercambiar; repetir hasta que ningún hijo gane.
**`extraer_maximo`:** guardar la raíz, mover el último elemento a la posición 0, poner `pos` de la raíz extraída en −1, reducir el tamaño y bajar desde 0.
**`actualizar`:** cambiar el valor, y después `subir` y `bajar` desde su posición (solo uno de los dos se mueve).

## 6. Uso desde el dominio
- `dominio/destacada.py`: `publicar` inserta con actividad 0; `responder` suma 1; `votar` suma 1; `retirar_voto` resta 1; todas llaman a `actualizar`. `destacada()` devuelve `maximo()`.
- `dominio/recomendaciones.py`: pide los candidatos al grafo ([`06-grafo`](../06-grafo/plan.md)), `construir` el montículo con la función de orden de recomendaciones y extrae hasta 5.

## 7. Soporte interno
- Arreglo de Python con el árbol completo (declarado en [`estructuras.md`](../00-producto/estructuras.md); no se usa `heapq`).
- Arreglo de posiciones indexado por id de publicación, solo en la instancia de la destacada (en recomendaciones se construye sin posiciones, porque no hay `actualizar`). Se justifica porque sin él `actualizar` costaría O(n) para encontrar el elemento.

## 8. Módulos
`estructuras/monticulo.py` · `dominio/destacada.py` · `dominio/recomendaciones.py` · pruebas en `tests/test_monticulo.py`.

## 9. Decisiones tomadas al implementar (todas de Valentina)
- **Montículo vacío:** `maximo` y `extraer_maximo` lanzan `MonticuloVacioError` (hereda de `IndexError`), igual que la pila y la cola; el dominio revisa `esta_vacio` antes de pedir.
- **Elementos:** el montículo guarda elementos cualesquiera y solo los compara con `antes(a, b)`. Las recomendaciones usan `(perfil, amigos_en_comun)`.
- **Consola:** la opción 8 muestra cada recomendación como `@usuario (N amigos en común)`, en singular si es 1; no envía solicitudes (eso sigue en la opción 2).
- **Acceso al grafo:** `Amistades` expone `grafo` y `catalogo` para que `recomendaciones.recomendar(amistades, persona)` pida los candidatos sin duplicar la red.
- **`actualizar` y el arreglo de posiciones** no se implementaron todavía: llegan con la destacada (Should, T-07.12).

## Historial de cambios
| Versión | Fecha | Cambio | Motivo |
|---|---|---|---|
| 1.0 | 2026-11-07 | Versión inicial (la carpeta estaba vacía) | Faltaban spec, plan y tasks del montículo; se declara que no hay montículo previo y qué se toma de `cola_prioridad.py`; actualización en sitio con arreglo de posiciones; construcción en O(m); orden de intercambios; alternativas descartadas |
| 1.1 | 2026-11-10 | Sección 9 con las decisiones de implementación: montículo vacío, elementos genéricos, salida de consola y acceso al grafo | Al implementar hubo que cerrar detalles que el plan no fijaba; decisiones de Valentina |
