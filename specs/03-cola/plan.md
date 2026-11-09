# Plan — Cola
Versión 1.3

## 1. De qué implementación mía parto
De **`Semana10/cola.py`**, clase `ColaEnlazada` (no la `ColaCircular` del mismo archivo), con `ColaVaciaError(IndexError)` y sus invariantes IR-01 e IR-02. Qué cambia para InsightHub:
- Se mueve a `estructuras/cola.py` y usa el `Nodo` del proyecto.
- `tamaño()` pasa a `tamano()`.
- Se agrega `contiene(dato)` (recorrido) y `__iter__` (para listar sin sacar).
- La lógica de solicitudes y notificaciones no va en la cola: va en `dominio/amistades.py` y `dominio/notificaciones.py`.

## 2. Estructura elegida y por qué
**Cola enlazada** con referencias a la cabeza (frente) y a la cola (final), más un contador.

Solicitudes y avisos se atienden en orden de llegada (FIFO). Con dos referencias, encolar y desencolar no recorren nada. Se descarta la `ColaCircular` porque cada persona tiene dos colas y casi todas están vacías o con pocos elementos: un arreglo de capacidad 8 por cola desperdicia memoria con miles de usuarios, y la enlazada no necesita redimensionar.

## 3. Complejidad por operación
| Operación | Complejidad | Por qué |
|---|---|---|
| `encolar(dato)` | O(1) | Enlaza al final con la referencia `_cola` |
| `desencolar()` | O(1) | Mueve la cabeza; si queda vacía, `_cola = None` (IR-01) |
| `frente()` | O(1) | Lee la cabeza |
| `contiene(dato)` | O(k) | Recorre las k pendientes; k es pequeño por persona |
| `esta_vacia()`, `tamano()` | O(1) | Cabeza y contador |
| Leer todas las notificaciones | O(k) | Desencola las k pendientes |

## 4. Alternativas descartadas
| Alternativa | Por qué no |
|---|---|
| `list` con `pop(0)` | Desencolar desplaza todo, O(n); además sustituye la estructura declarada |
| `ColaCircular` (Semana10) | O(1) amortizado también, pero reserva memoria fija por persona aunque esté vacía |
| Índice aparte (AVL) para detectar solicitudes repetidas | O(log n) frente a O(k) con k pequeño; agrega otra estructura y horas sin ganancia real |
| Aceptar cualquier solicitud de la lista | Exige quitar del medio, O(k), y rompe CA-07 |

## 5. Orden de punteros al desencolar
1. Guardar la cabeza actual.
2. Mover la cabeza a su siguiente.
3. Si la cabeza quedó en `None`, poner `_cola = None`.

Si se omite el paso 3, `_cola` sigue apuntando a un nodo que ya salió y el siguiente `encolar` lo enlaza ahí: el elemento nuevo se pierde. Es el error marcado en Semana10 («¡no olvides esta línea!»).

## 6. Uso desde el dominio
- `amistades.enviar(de, para)`: valida uno mismo (comparación), amigo (consulta al grafo) y repetida (`contiene`), y encola.
- `amistades.atender(persona, aceptar)`: desencola la primera; si acepta, llama al grafo (CA-06) y notifica.
- `notificaciones.leer(persona)`: desencola todo; si estaba vacía, devuelve «sin notificaciones».

## 7. Soporte interno
- La cola es de nodos propios, sin soporte.
- `dominio/notificaciones.py` guarda la cola de cada persona en un **arreglo de Python indexado por el id de la persona** (las colas se crean al recibir el primer aviso). Se justifica porque da acceso O(1) por id y el id viene del catálogo de usuarios (el mismo soporte declarado en [`estructuras.md`](../00-producto/estructuras.md)); no sustituye a la cola.

## 8. Módulos
`estructuras/cola.py` · `dominio/amistades.py` · `dominio/notificaciones.py` · pruebas en `tests/test_cola.py`.

## 9. Decisiones tomadas al implementar (todas de Valentina)
- **Rechazos:** `amistades.enviar` lanza `SolicitudInvalidaError` (hereda de `ValueError`) con el motivo; la consola lo imprime. Igual que `UsuarioInvalidoError`.
- **Solicitud cruzada:** se rechaza con aviso, consultando `contiene` en la cola de quien envía. Así nunca quedan dos solicitudes cruzadas ni una sobrante.
- **Interfaz:** `enviar(de, usuario_para)` recibe el id de quien envía y el `@usuario` de destino, y devuelve el perfil destino. `primera` consulta sin sacar; `atender(persona, aceptar)` devuelve el perfil de quien la envió o `None`.
- **Soporte:** las colas de solicitudes se guardan en un arreglo indexado por id, como las de notificaciones.

## Historial de cambios
| Versión | Fecha | Cambio | Motivo |
|---|---|---|---|
| 1.0 | 2026-11-07 | Versión inicial | Creación |
| 1.1 | 2026-11-07 | Se declara el punto de partida (`ColaEnlazada` de Semana10), por qué no la circular, `contiene`, orden de punteros al desencolar y el uso desde amistades y notificaciones | El plan no justificaba la elección ni decía de qué implementación partía; decisiones tomadas en la consulta del componente |
| 1.2 | 2026-11-07 | Se declara el arreglo indexado por id como soporte interno de `notificaciones.py` | Al implementar apareció dónde guardar la cola de cada persona; antes el plan decía «ninguno» |
| 1.3 | 2026-11-08 | Sección 9 con las decisiones de implementación de `amistades.py`; la cabecera pasa a 1.3 (seguía en 1.1 aunque el historial ya tenía la 1.2) | Al integrar las amistades hubo que cerrar detalles que el plan no fijaba; decisiones de Valentina |
