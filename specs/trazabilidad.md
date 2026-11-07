# Trazabilidad criterio ↔ prueba ↔ código

Actualiza esta tabla con cada commit `test(...)`. «—» significa que aún no existe la prueba.

| Criterio | Historia | Prueba | Código |
|---|---|---|---|
| CA-01 | HU-01 | — | dominio/usuarios.py |
| CA-02 | HU-01 | — | dominio/usuarios.py |
| CA-03 | HU-02 | tests/test_grafo.py | estructuras/grafo.py |
| CA-04 | HU-02 | tests/test_grafo.py | estructuras/grafo.py |
| CA-05 | HU-03 | tests/test_lista_doble.py | estructuras/lista_doble.py |
| CA-06 | HU-03 | tests/test_lista_doble.py | estructuras/lista_doble.py |
| CA-07 | HU-04 | — | estructuras/arbol_general.py |
| CA-08 | HU-04 | — | estructuras/arbol_general.py |
| CA-09 | HU-04 | — | estructuras/arbol_general.py |
| CA-10 | HU-05 | — | estructuras/avl.py |
| CA-11 | HU-05 | — | estructuras/avl.py |
| CA-12 | HU-05 | — | dominio/usuarios.py |
| CA-13 | HU-06 | — | estructuras/pila.py |
| CA-14 | HU-06 | — | estructuras/pila.py |
| CA-15 | HU-07 | — | estructuras/cola.py |
| CA-16 | HU-07 | — | estructuras/cola.py |
| CA-17 | HU-08 | — | dominio/recomendaciones.py |
| CA-18 | HU-08 | — | dominio/recomendaciones.py |
| CA-19 | HU-08 | — | dominio/recomendaciones.py |
| CA-20 | HU-09 | — | (Should) |
| CA-21 | HU-09 | — | (Should) |

## Dirección inversa (código → criterio)
| Función | Nació del criterio |
|---|---|
| `ListaDoble.insertar_al_frente` | CA-05 |
| `ListaDoble.avanzar` / `retroceder` | CA-06 |
