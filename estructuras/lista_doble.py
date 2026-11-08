# Base: Semana 07 (Nodos_enlazados_doblemente.py, ListadoblementeEnlazada; y carrusel.py).
# Cambios para InsightHub (ver specs/01-lista-doble/plan.md §1):
#   - se inserta AL FRENTE (lo nuevo primero); Semana7 insertaba al final
#   - el cursor `actual` sale de la lista: cada sesión guarda su propio marcador (un nodo)
#   - deshacer/rehacer pasan a avanzar/retroceder de 5 en 5, que informan el límite
#   - no es circular (el carrusel sí) y se quitan los print
# Spec: specs/01-lista-doble/spec.md

PAGINA = 5


class NodoDoble:
    """Un eslabón con dato, referencia al anterior y referencia al siguiente."""

    def __init__(self, dato=None, anterior=None, siguiente=None):
        self.dato = dato
        self.anterior = anterior
        self.siguiente = siguiente

    def __repr__(self):
        return f"NodoDoble({self.dato!r})"


class ListaDoble:
    """Lista doblemente enlazada: lo más nuevo al frente, se recorre en ambos sentidos.

    Un *marcador* es un NodoDoble: la posición de una sesión. Las operaciones de
    recorrido lo reciben y devuelven el marcador nuevo; la lista no guarda posición.

    Invariantes de representación:
        IR-01: _cabeza is None  <=>  _cola is None  <=>  _tamaño == 0
        IR-02: _cabeza.anterior is None  y  _cola.siguiente is None
        IR-03: para todo nodo n con n.siguiente: n.siguiente.anterior is n

    Complejidad: insertar_al_frente O(1), inicio O(1), pagina O(5)=O(1),
                 avanzar O(5)=O(1), retroceder O(5)=O(1),
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

    tamaño = tamano  # el nombre que ya usaba en Semana7

    def insertar_al_frente(self, dato):
        """Deja `dato` como el primero de la lista. O(1).

        Orden de punteros (si se cambia, se pierde un enlace):
            1. nuevo.siguiente = cabeza
            2. cabeza.anterior = nuevo (o, si estaba vacía, cola = nuevo)
            3. cabeza = nuevo
        """
        nuevo = NodoDoble(dato, None, self._cabeza)
        if self._cabeza is None:        # estaba vacía: es también la cola
            self._cola = nuevo
        else:
            self._cabeza.anterior = nuevo
        self._cabeza = nuevo
        self._tamaño += 1
        return nuevo

    def inicio(self):
        """Marcador del primer nodo (None si la lista está vacía). O(1)."""
        return self._cabeza

    def pagina(self, marcador):
        """Hasta 5 datos desde `marcador` hacia los más antiguos. O(5)."""
        datos = []
        actual = marcador
        while actual is not None and len(datos) < PAGINA:
            datos.append(actual.dato)
            actual = actual.siguiente
        return datos

    def avanzar(self, marcador):
        """Mueve el marcador 5 nodos hacia los más antiguos. O(5).

        Devuelve (marcador_nuevo, se_movio). Si no hay 5 nodos más adelante
        (última página) o la lista está vacía, devuelve (marcador, False).
        """
        if marcador is None:
            return None, False
        actual = marcador
        for _ in range(PAGINA):
            actual = actual.siguiente
            if actual is None:          # no caben 5 pasos: última página
                return marcador, False
        return actual, True

    def retroceder(self, marcador):
        """Mueve el marcador hasta 5 nodos hacia los más nuevos. O(5).

        Si faltan menos de 5 para el principio, llega al principio. Devuelve
        (marcador_nuevo, se_movio); si ya estaba en el principio, (marcador, False).
        """
        if marcador is None or marcador.anterior is None:
            return marcador, False
        actual = marcador
        pasos = 0
        while actual.anterior is not None and pasos < PAGINA:
            actual = actual.anterior
            pasos += 1
        return actual, True

    def __len__(self):
        return self._tamaño

    def __iter__(self):
        """Del frente (más nuevo) al final (más antiguo), sin modificar. O(n)."""
        actual = self._cabeza
        while actual is not None:
            yield actual.dato
            actual = actual.siguiente
