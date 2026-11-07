# Base: Semana 10 (pila.py, PilaEnlazada). Cambios para InsightHub:
#   - se agrega tamano() (sin ñ, como pide el spec) y se conserva tamaño()
#   - docstrings con invariantes y complejidad (Constitución, restricciones técnicas)
# Spec: specs/02-pila/spec.md · Plan: specs/02-pila/plan.md

from estructuras.nodo import Nodo


class PilaVaciaError(IndexError):
    """Se intentó operar sobre una pila vacía."""


class PilaEnlazada:
    """Pila LIFO sobre nodos: apila y desapila por la cabeza.

    Invariantes de representación:
        IR-01: _cabeza is None  <=>  _tamaño == 0
        IR-02: recorrer desde _cabeza llega al final en exactamente _tamaño pasos

    Complejidad: apilar O(1), desapilar O(1), tope O(1),
                 esta_vacia O(1), tamano O(1) (contador).
    """

    def __init__(self):
        self._cabeza = None
        self._tamaño = 0

    def esta_vacia(self):
        """True si no hay elementos. O(1)."""
        return self._cabeza is None

    def tamano(self):
        """Cantidad de elementos. O(1)."""
        return self._tamaño

    tamaño = tamano  # el nombre que ya usaba en Semana10

    def apilar(self, elemento):
        """Deja `elemento` como el más reciente. O(1).

        Primero el nodo nuevo apunta a la cabeza actual y solo después pasa a
        ser la cabeza: al revés se pierde el resto de la pila.
        """
        self._cabeza = Nodo(elemento, self._cabeza)
        self._tamaño += 1

    def desapilar(self):
        """Devuelve y quita el elemento más reciente. O(1).

        Lanza PilaVaciaError si la pila está vacía (no modifica nada).
        """
        if self.esta_vacia():
            raise PilaVaciaError("desapilar sobre pila vacía")
        nodo = self._cabeza
        self._cabeza = nodo.siguiente
        self._tamaño -= 1
        return nodo.dato

    def tope(self):
        """Devuelve el elemento más reciente sin quitarlo. O(1).

        Lanza PilaVaciaError si la pila está vacía.
        """
        if self.esta_vacia():
            raise PilaVaciaError("tope sobre pila vacía")
        return self._cabeza.dato

    def __len__(self):
        return self._tamaño
