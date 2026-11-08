# Base: Semana 10 (cola.py, ColaEnlazada). Cambios para InsightHub:
#   - se usa solo la versión enlazada (no la ColaCircular del mismo archivo)
#   - se agrega tamano() (sin ñ, como pide el spec) y se conserva tamaño()
#   - se agregan contiene() (para detectar solicitudes repetidas, CA-05) e __iter__
# Spec: specs/03-cola/spec.md · Plan: specs/03-cola/plan.md

from estructuras.nodo import Nodo


class ColaVaciaError(IndexError):
    """Se intentó operar sobre una cola vacía."""


class ColaEnlazada:
    """Cola FIFO sobre nodos. Desencola por la cabeza, encola por la cola.

    Invariantes de representación:
        IR-01: _cabeza is None  <=>  _cola is None  <=>  _tamaño == 0
        IR-02: _cola.siguiente is None siempre

    Complejidad: encolar O(1), desencolar O(1), frente O(1),
                 contiene O(k) con k elementos pendientes,
                 esta_vacia O(1), tamano O(1) (contador).
    """

    def __init__(self):
        self._cabeza = None
        self._cola = None
        self._tamaño = 0

    def esta_vacia(self):
        """True si no hay elementos. O(1)."""
        return self._cabeza is None

    def tamano(self):
        """Cantidad de elementos. O(1)."""
        return self._tamaño

    tamaño = tamano  # el nombre que ya usaba en Semana10

    def encolar(self, elemento):
        """Deja `elemento` al final, detrás de todos los que esperaban. O(1)."""
        nuevo = Nodo(elemento)
        if self._cola is None:
            self._cabeza = nuevo
        else:
            self._cola.siguiente = nuevo
        self._cola = nuevo
        self._tamaño += 1

    def desencolar(self):
        """Devuelve y quita el que llegó primero. O(1).

        Lanza ColaVaciaError si la cola está vacía (no modifica nada).
        """
        if self.esta_vacia():
            raise ColaVaciaError("desencolar sobre cola vacía")
        nodo = self._cabeza
        self._cabeza = nodo.siguiente
        if self._cabeza is None:        # era el último
            self._cola = None           # ¡no olvides esta línea!
        self._tamaño -= 1
        return nodo.dato

    def frente(self):
        """Devuelve el que llegó primero sin quitarlo. O(1).

        Lanza ColaVaciaError si la cola está vacía.
        """
        if self.esta_vacia():
            raise ColaVaciaError("frente sobre cola vacía")
        return self._cabeza.dato

    def contiene(self, elemento):
        """True si `elemento` está pendiente (comparación con ==). O(k).

        Recorre la cadena sin modificarla; sirve para no encolar dos veces
        la misma solicitud de amistad (CA-05).
        """
        actual = self._cabeza
        while actual is not None:
            if actual.dato == elemento:
                return True
            actual = actual.siguiente
        return False

    def __len__(self):
        return self._tamaño

    def __iter__(self):
        """Del frente al final, sin sacar nada. O(k)."""
        actual = self._cabeza
        while actual is not None:
            yield actual.dato
            actual = actual.siguiente
