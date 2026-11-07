# Base: Semana 05 (Nodo) — el mismo eslabón que usé en pila, cola y lista simple.


class Nodo:
    """Un eslabón de una cadena: un dato y una referencia al siguiente.

    `siguiente` es None cuando este nodo es el último de la cadena.
    """

    def __init__(self, dato, siguiente=None):
        self.dato = dato
        self.siguiente = siguiente

    def __repr__(self):
        return f"Nodo({self.dato!r})"
