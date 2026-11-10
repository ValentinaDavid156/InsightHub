# Base: Semana 10 (arbol_binario.py, NodoArbol con dos enlaces; arbol_carpetas.py, recorrido
# con contenedor propio). Cambios para InsightHub:
#   - `izquierdo` significa PRIMER HIJO y `derecho` HERMANO DERECHO: con dos enlaces un nodo
#     puede tener cualquier cantidad de respuestas, sin la `list` de hijos de arbol_carpetas
#   - el recorrido usa la PilaEnlazada propia, sin recursión, para hilos muy profundos
# Spec: specs/04-arbol-general/spec.md · Plan: specs/04-arbol-general/plan.md

from estructuras.pila import PilaEnlazada


class RespuestaInvalidaError(ValueError):
    """La respuesta se rechaza; el mensaje dice el motivo. El hilo no cambia."""


class NodoHilo:
    """La publicación o una respuesta. Puntaje neto en 0 hasta que existan los votos (Should)."""

    def __init__(self, id, autor, texto):
        self.id = id
        self.autor = autor
        self.texto = texto
        self.puntaje = 0
        self.izquierdo = None       # primer hijo: su primera respuesta
        self.derecho = None         # hermano derecho: la siguiente respuesta del mismo padre

    def __repr__(self):
        return f"NodoHilo({self.id!r})"


class ArbolGeneral:
    """Un hilo: la publicación es la raíz y las respuestas cuelgan de ella.

    Invariantes de representación:
        IR-01: _raiz is None  <=>  _tamaño == 0
        IR-02: la raíz no tiene hermano derecho
        IR-03: los identificadores del hilo son distintos entre sí
        IR-04: una cadena de hermanos va de la respuesta más antigua a la más nueva

    n = nodos del hilo.
    Complejidad: abrir_hilo O(1), tamano O(1), responder O(n), buscar O(n),
                 recorrer O(n), profundidad O(n).
    """

    def __init__(self):
        self._raiz = None
        self._tamaño = 0

    def tamano(self):
        """Elementos del hilo, contando la publicación. O(1)."""
        return self._tamaño

    tamaño = tamano

    def __len__(self):
        return self._tamaño

    def abrir_hilo(self, id, autor, texto):
        """Crea la raíz. O(1). Lanza RespuestaInvalidaError si el hilo ya estaba abierto."""
        if self._raiz is not None:
            raise RespuestaInvalidaError("Este hilo ya está abierto.")
        self._raiz = NodoHilo(id, autor, texto)
        self._tamaño = 1
        return self._raiz

    def _nodos(self):
        """Genera (nivel, nodo) en orden de hilo, con la pila propia. O(n).

        Apila primero el hermano y después el hijo: la pila saca lo último que entró, así
        se baja por una rama completa antes de seguir con la respuesta siguiente.
        """
        if self._raiz is None:
            return
        pila = PilaEnlazada()
        pila.apilar((0, self._raiz))
        while not pila.esta_vacia():
            nivel, nodo = pila.desapilar()
            yield nivel, nodo
            if nodo.derecho is not None:
                pila.apilar((nivel, nodo.derecho))
            if nodo.izquierdo is not None:
                pila.apilar((nivel + 1, nodo.izquierdo))

    def recorrer(self):
        """Lista de (nivel, nodo): cada respuesta debajo de su padre, en orden cronológico. O(n)."""
        return list(self._nodos())

    def buscar(self, id):
        """El nodo con ese identificador, o None. O(n)."""
        for _, nodo in self._nodos():
            if nodo.id == id:
                return nodo
        return None

    def profundidad(self, id):
        """Nivel del nodo (la publicación es 0), o None si no existe. O(n)."""
        for nivel, nodo in self._nodos():
            if nodo.id == id:
                return nivel
        return None

    def responder(self, id_padre, id_nuevo, autor, texto):
        """Agrega una respuesta después de las que ya tenía el padre y la devuelve. O(n).

        Lanza RespuestaInvalidaError, sin alterar el hilo, si el padre no existe o si
        `id_nuevo` ya está en el hilo. Todo se valida antes de enlazar.
        """
        padre = None
        for _, nodo in self._nodos():       # una sola pasada para las dos comprobaciones
            if nodo.id == id_nuevo:
                raise RespuestaInvalidaError("Ese identificador ya existe en el hilo.")
            if nodo.id == id_padre:
                padre = nodo
        if padre is None:
            raise RespuestaInvalidaError("Eso a lo que quieres responder no existe en el hilo.")
        nuevo = NodoHilo(id_nuevo, autor, texto)
        if padre.izquierdo is None:
            padre.izquierdo = nuevo
        else:
            ultimo = padre.izquierdo
            while ultimo.derecho is not None:
                ultimo = ultimo.derecho
            ultimo.derecho = nuevo
        self._tamaño += 1                   # solo después de enlazar
        return nuevo
