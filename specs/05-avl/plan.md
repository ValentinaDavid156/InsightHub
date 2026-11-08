# Plan — AVL
Versión 1.2

## 1. De qué implementación mía parto
**No tengo en el repositorio una implementación propia de árbol de búsqueda ni de AVL**: lo más cercano es **`Semana10/arbol_binario.py`** (`NodoArbol` con `izquierdo` y `derecho`, `inorden` y la convención de altura **vacío = −1, hoja = 0**). Qué cambia para InsightHub (casi todo es nuevo y lo escribo desde cero):
- `NodoArbol` gana `clave`, `valor` y `altura`; pasa de «árbol sin orden» a árbol de búsqueda (menores a la izquierda, mayores a la derecha).
- Se agregan la inserción ordenada y las **cuatro rotaciones** que mantienen el equilibrio. Eso no existe en mi código de Semana10.
- Se conserva el `inorden` de Semana10 como base de «en orden alfabético».
- Se mantiene la convención de altura (vacío = −1) para que el factor de equilibrio se calcule igual.

Por eso la estimación de horas de HU-01 en [`moscow.md`](../00-producto/moscow.md) es la más alta de las estructuras.

## 2. Estructura elegida y por qué
**Árbol AVL**: árbol binario de búsqueda donde, en cada nodo, la diferencia de alturas entre sus dos lados no pasa de 1. La clase es única y genérica (`clave` de texto, `valor` cualquiera); se instancia tres veces:
| Instancia | Clave | Valor |
|---|---|---|
| Usuarios | `@usuario` en minúsculas | perfil (identificador y puntos) |
| Votos de una respuesta | `@usuario` de quien votó | +1, −1 o 0 si retiró |
| Publicaciones por fecha | `AAAA-MM-DD\|` + id con ceros a la izquierda (6 dígitos) | la publicación |

Se necesita buscar por clave exacta y por prefijo, en orden, y la comunidad sembrada llega ya ordenada: un árbol sin equilibrar se volvería una lista. El AVL garantiza altura ≤ 1.44·log₂(n+2).

## 3. Complejidad por operación
n = claves del árbol; k = resultados.
| Operación | Complejidad | Por qué |
|---|---|---|
| `insertar(clave, valor)` | O(log n) | Baja por una rama y reequilibra al volver |
| `buscar(clave)` | O(log n) | Una comparación por nivel |
| `reemplazar(clave, valor)` | O(log n) | Busca y cambia el valor (votos) |
| `buscar_por_prefijo(prefijo)` | O(log n + k) | Solo entra a las ramas que pueden contener el prefijo |
| `recorrer_en_orden()` | O(n) | `inorden` |
| `altura()` | O(1) | Se lee del nodo raíz |
| `tamano()` | O(1) | Contador |

Memoria: O(n).

## 4. Alternativas descartadas
| Alternativa | Por qué no |
|---|---|
| Tabla hash (`dict`) | Da unicidad y búsqueda exacta en O(1), pero no orden alfabético ni prefijo; además es una estructura nativa |
| Árbol de búsqueda sin equilibrar | Con 120 claves sembradas ya ordenadas, la altura sería ~120 y la búsqueda O(n) |
| Lista ordenada | Insertar es O(n) |
| Árbol rojo-negro | También O(log n), pero sus casos de recoloreo son más difíciles de explicar línea por línea |
| Dos índices (nombre y `@usuario`) | El perfil no tiene otro nombre (decisión en la consulta); un índice basta |

## 5. Rotaciones y orden de punteros
Tras insertar, en cada nodo del camino de regreso: actualizar `altura` y calcular `factor = altura(izq) − altura(der)`.
| Caso | Condición | Arreglo |
|---|---|---|
| Izquierda-izquierda | factor > 1 y el hijo izquierdo no pesa hacia la derecha | rotación simple a la derecha |
| Derecha-derecha | factor < −1 y el hijo derecho no pesa hacia la izquierda | rotación simple a la izquierda |
| Izquierda-derecha | factor > 1 y el hijo izquierdo pesa hacia la derecha | rotar a la izquierda al hijo, luego a la derecha |
| Derecha-izquierda | factor < −1 y el hijo derecho pesa hacia la izquierda | rotar a la derecha al hijo, luego a la izquierda |

**Rotación a la derecha** sobre `y` (con `x = y.izquierdo`), cambia tres punteros en este orden:
1. `t2 = x.derecho` (guardar antes de pisarlo)
2. `x.derecho = y`
3. `y.izquierdo = t2`
y luego recalcular primero la altura de `y` (ahora es el hijo) y después la de `x`. Si se invierte, `y` queda con una altura calculada con datos viejos y el factor de equilibrio de los ancestros es incorrecto. Si se pisa `x.derecho` sin guardar `t2`, el subárbol `t2` se pierde (es la misma pérdida de referencias de mis notas de Semana6). La rotación a la izquierda es simétrica.

Cada `insertar` devuelve la nueva raíz del subárbol para que el padre se enlace con ella; así no queda un enlace apuntando a un nodo que dejó de ser raíz.

## 6. Búsqueda por prefijo
En cada nodo: si la clave empieza por el prefijo, se visitan los dos lados (primero el izquierdo, luego la clave, luego el derecho, lo que da orden alfabético); si la clave es menor que el prefijo, solo el derecho; si es mayor y no empieza por el prefijo, solo el izquierdo. Las claves con un prefijo dado forman un tramo contiguo, así que se descarta toda rama fuera del tramo. Con el prefijo vacío el método devuelve vacío (decisión de la spec).

## 7. Reglas de negocio en el dominio
- `dominio/usuarios.py`: valida `@usuario` (3 a 20; letras, números y guión bajo), pasa a minúsculas, genera los 120 perfiles, calcula la insignia, `entrar`.
- Generación: `random.Random(706132)` (librería estándar) elige nombres de una lista fija y un número; si un nombre resulta repetido se vuelve a sortear. Mismo generador y mismo orden → mismos perfiles (CA-02).
- `dominio/votos.py` (Should): un AVL de votos por respuesta; `votar` busca la clave y aplica la diferencia de valor × puntos (nuevo − anterior). Un voto retirado queda en 0, no se borra; así «cambiar» y «retirar» son el mismo reemplazo.
- `dominio/busqueda.py` (Should): clave de fecha `AAAA-MM-DD|000123`; buscar un día es buscar el prefijo `AAAA-MM-DD|`.

## 8. Soporte interno
- Arreglo de Python indexado por id para acceder a un usuario por su id (catálogo), declarado en [`estructuras.md`](../00-producto/estructuras.md).
- `random.Random` y los textos de la lista de nombres: no son estructuras declaradas.
- El resultado de una búsqueda se entrega en una `list` de Python: es la salida, no la estructura de datos.

## 9. Módulos
`estructuras/avl.py` · `dominio/usuarios.py` · `dominio/votos.py` · `dominio/busqueda.py` · pruebas en `tests/test_avl.py`.

## 10. Decisiones tomadas al implementar (todas de Valentina)
- **`AVL.insertar`:** devuelve `True` si la clave era nueva y `False` si ya existía, sin cambiar nada (ni el valor ni el tamaño).
- **`AVL.buscar`:** devuelve `None` si la clave no está; por eso un valor `None` no se distingue de «ausente».
- **`AVL.buscar_por_prefijo`:** devuelve los **valores** en orden alfabético de clave, y `[]` con prefijo vacío. **`recorrer_en_orden`** devuelve las claves.
- **`reemplazar`** no se implementó todavía: llega con los votos (Should, T-05.17).
- **Errores del @usuario:** el dominio lanza `UsuarioInvalidoError` (hereda de `ValueError`) con el motivo («muy corto», «muy largo», «solo puede tener letras…», «está vacío», «ya existe»).
- **Arroba inicial:** opcional; se guarda sin ella y en minúsculas.
- **Catálogo:** `Catalogo` junta el AVL (`@usuario` → `Perfil`) y un arreglo indexado por id; los ids van de 0 en el orden de creación y no se reutilizan.
- **`entrar`:** devuelve `(perfil, creado)`. La consulta de perfiles (`buscar`, `buscar_por_prefijo`) nunca lanza error: texto vacío o inválido da `None` o `[]`.
- **Comunidad inicial:** 40 nombres fijos (sin tildes ni ñ) con número del 01 al 99, sorteados con `random.Random(706132)`; los repetidos se vuelven a sortear. La lista la aprobó Valentina.

## Historial de cambios
| Versión | Fecha | Cambio | Motivo |
|---|---|---|---|
| 1.0 | 2026-11-07 | Versión inicial | Creación |
| 1.1 | 2026-11-07 | Se aclara que no hay implementación previa y qué se toma de Semana10; tres instancias del mismo árbol; rotaciones con su orden de punteros; búsqueda por prefijo; reglas de votos e insignia; generación con semilla; alternativas descartadas | El plan no justificaba la elección ni explicaba las rotaciones; decisiones tomadas en la consulta del componente |
| 1.2 | 2026-11-08 | Se agrega la sección 10 con las decisiones de implementación: duplicado, ausente, errores, arroba opcional, ids y nombres de ejemplo | Al implementar hubo que cerrar detalles que el plan no fijaba; decisiones de Valentina |
