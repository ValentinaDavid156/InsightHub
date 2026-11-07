# Plan — Lista simple (conectados)
Versión 1.0

## 1. De qué implementación mía parto
De **`Semana6/lista_reproduccion/lista_enlazada.py`** (`ListaEnlazada`, con `_cabeza`, `_cola`, los cinco casos de inserción y eliminación y sus invariantes IR-01 a IR-03) y de **`Semana5/nodo.py`** (`Nodo` con `dato` y `siguiente`). De **`Semana10/cola_prioridad.py`** tomo la idea de que el tiempo lo entrega quien llama y de rechazar un tiempo que retrocede. Qué cambia para InsightHub:
- Me quedo con **tres** de los cinco casos de Semana6: insertar al inicio, eliminar el primero y eliminar cualquier otro. Los otros dos (insertar al final y en el medio) no se usan.
- **Se quita `_cola`**: como solo se inserta al inicio, mantener la referencia al último nodo es trabajo extra y un invariante más que se puede romper al eliminar (IR-02 de Semana6).
- Los datos son entradas con `usuario` y `ultima_actividad`, no valores sueltos; la búsqueda es por `usuario`, no por igualdad de valor.
- Se agrega un recorrido que **retira durante el paso** a los vencidos (caducidad), que Semana6 no tiene.

## 2. Estructura elegida y por qué
**Lista enlazada simple** con referencia a la cabeza y un contador. Cada nodo guarda la entrada (`usuario`, `ultima_actividad`).

Conectar es insertar al inicio en O(1). Listar cuesta O(c) con c = personas conectadas, y no O(n) con n = todos los usuarios, que es lo que costaría recorrer el AVL en cada consulta. Como c es pequeño frente a n, las demás operaciones, que recorren la lista, son baratas.

## 3. Complejidad por operación
c = personas conectadas; g = amigos de la persona consultada.
| Operación | Complejidad | Por qué |
|---|---|---|
| `conectar(usuario, ahora)` | O(c) | Buscar si ya está para no repetirla; insertar al inicio es O(1) |
| `registrar_actividad(usuario, ahora)` | O(c) | Buscar su nodo y cambiar la hora; si no está, insertar |
| `salir(usuario)` | O(c) | Buscar con el nodo anterior y desenlazar |
| `caducar(ahora)` | O(c) | Un solo recorrido que retira a los vencidos |
| `listar(ahora)` | O(c) | `caducar` y recorrido |
| `esta_conectado(usuario, ahora)` | O(c) | `caducar` y búsqueda |
| `estado_amigos(amigos, ahora)` | O(c + g·c) | `caducar` una vez y una búsqueda por amigo |
| `cantidad()` | O(1) | Contador (después de `caducar`) |

## 4. Alternativas descartadas
| Alternativa | Por qué no |
|---|---|
| Recorrer todo el AVL de usuarios con un campo `conectado` | Listar cuesta O(n) en cada consulta |
| `list` de Python | Los costos serían los mismos, pero sustituye una estructura declarada (Constitución, principio 2) |
| Marca de conexión también en el perfil | Estado en O(1), pero dos fuentes de verdad que mantener iguales al entrar, salir y caducar (decisión en la consulta) |
| Hilo temporizador que barre la lista | Agrega concurrencia y pruebas con tiempo real (decisión en la consulta) |
| Lista doble | No se necesita ir hacia atrás; el nodo anterior se lleva mientras se recorre |
| Insertar al final con `_cola` | Mismo costo, pero un invariante más |

## 5. Orden de punteros
**Insertar al inicio:** `nuevo.siguiente = cabeza`, luego `cabeza = nuevo`, luego `tamano += 1`. Al revés se pierde el resto de la lista.

**Eliminar con nodo anterior** (casos de Semana6): se recorre con `anterior` y `actual`.
- Si `actual` es la cabeza: `cabeza = actual.siguiente`.
- Si no: `anterior.siguiente = actual.siguiente`.
En ambos casos se desenlaza **antes** de soltar `actual`, y se resta 1 al contador.

**Caducar en un solo paso:** mientras `actual` no sea `None`: si `ahora − actual.ultima_actividad ≥ 30`, desenlazarlo como arriba y **avanzar `actual` sin mover `anterior`**; si no, avanzar los dos. Si se movía `anterior` después de eliminar, quedaba apuntando a un nodo ya desenlazado y el siguiente desenlace dejaba el nodo muerto dentro de la lista. Si se eliminaba la cabeza y no se actualizaba `cabeza`, la lista seguía empezando por un vencido.

## 6. Tiempo
Toda operación recibe `ahora` (segundos) y la lista guarda `ultimo_tiempo`; si `ahora < ultimo_tiempo` lanza `ValueError` sin tocar nada (RF-07), como `_avanzar_reloj` de Semana10. El umbral es la constante `UMBRAL = 30`; una persona con `ahora − ultima_actividad ≥ 30` está desconectada. Así las pruebas no necesitan esperar 30 segundos.

## 7. Uso desde el dominio
- Cada comando de la consola (y cada petición del navegador) llama a `presencia.registrar_actividad(usuario, ahora)` antes de ejecutarse.
- `presencia.estado_amigos(usuario, ahora)` pide los amigos al grafo ([`06-grafo`](../06-grafo/plan.md)) y los pasa a `estado_amigos`.

## 8. Soporte interno
Ninguno. Solo nodos propios. El resultado de `listar` y `estado_amigos` se entrega en una `list` de Python (salida, no estructura).

## 9. Módulos
`estructuras/lista_simple.py` · `dominio/presencia.py` · pruebas en `tests/test_lista_simple.py`.

## Historial de cambios
| Versión | Fecha | Cambio | Motivo |
|---|---|---|---|
| 1.0 | 2026-11-07 | Versión inicial (la carpeta estaba vacía) | Faltaban spec, plan y tasks de la lista simple; se declara el punto de partida (`ListaEnlazada` de Semana6 y `Nodo` de Semana5) y qué cambia (se quita `_cola`); caducidad en un solo paso con orden de punteros; tiempo por parámetro; alternativas descartadas |
