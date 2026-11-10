# Montículo máximo binario guardado en un arreglo (sin heapq).
# Base: de Semana 10 (cola_prioridad.py) solo la idea de que el orden lo decide una regla con
# desempate y que quien llama la aporta; el montículo es nuevo.
# Spec: specs/07-monticulo/spec.md · Plan: specs/07-monticulo/plan.md
# Soporte interno: un arreglo de Python con el árbol completo (declarado en estructuras.md).
# `actualizar` y el arreglo de posiciones llegan con la destacada (Should, T-07.12).


class MonticuloVacioError(IndexError):
    """Se intentó consultar o extraer en un montículo vacío."""


class Monticulo:
    """El elemento que va primero según `antes(a, b)` siempre está en la posición 0.

    Posiciones: hijo izquierdo de i en 2i+1, hijo derecho en 2i+2, padre en (i-1)//2.

    Invariante de representación:
        IR-01: para todo i > 0, el padre de i no va después de i: not antes(datos[i], datos[padre])

    n = elementos. Complejidad: insertar O(log n), maximo O(1), extraer_maximo O(log n),
    construir O(m) con m elementos, esta_vacio O(1), tamano O(1).
    """

    def __init__(self, antes):
        self._antes = antes     # antes(a, b) es True si a debe salir antes que b
        self._datos = []

    def esta_vacio(self):
        return len(self._datos) == 0

    def tamano(self):
        return len(self._datos)

    tamaño = tamano

    def __len__(self):
        return len(self._datos)

    def _intercambiar(self, i, j):
        temporal = self._datos[i]           # 1. guardar el de i
        self._datos[i] = self._datos[j]     # 2. copiar el de j a i
        self._datos[j] = temporal           # 3. poner el guardado en j

    def _subir(self, i):
        """Mientras el elemento vaya antes que su padre, cambia de lugar con él."""
        while i > 0:
            padre = (i - 1) // 2
            if not self._antes(self._datos[i], self._datos[padre]):
                return
            self._intercambiar(i, padre)
            i = padre

    def _bajar(self, i):
        """Cambia de lugar con el hijo que va antes, mientras ese hijo vaya antes que él."""
        n = len(self._datos)
        while True:
            izquierdo, derecho = 2 * i + 1, 2 * i + 2
            elegido = i
            if izquierdo < n and self._antes(self._datos[izquierdo], self._datos[elegido]):
                elegido = izquierdo
            if derecho < n and self._antes(self._datos[derecho], self._datos[elegido]):
                elegido = derecho
            if elegido == i:
                return
            self._intercambiar(i, elegido)
            i = elegido

    def insertar(self, elemento):
        """Agrega al final y lo sube hasta su lugar. O(log n)."""
        self._datos.append(elemento)
        self._subir(len(self._datos) - 1)

    def maximo(self):
        """El que va primero, sin sacarlo. O(1). MonticuloVacioError si está vacío."""
        if self.esta_vacio():
            raise MonticuloVacioError("maximo sobre montículo vacío")
        return self._datos[0]

    def extraer_maximo(self):
        """Saca y devuelve el que va primero. O(log n). MonticuloVacioError si está vacío.

        Guarda la raíz, mueve el último elemento a la posición 0 y lo baja.
        """
        if self.esta_vacio():
            raise MonticuloVacioError("extraer_maximo sobre montículo vacío")
        raiz = self._datos[0]
        ultimo = self._datos.pop()
        if self._datos:
            self._datos[0] = ultimo
            self._bajar(0)
        return raiz

    def construir(self, elementos):
        """Reemplaza el contenido por `elementos` (sin modificar la lista recibida). O(m).

        Baja cada padre desde el último hasta la raíz: las hojas ya son montículos de un elemento.
        """
        self._datos = list(elementos)
        for i in range(len(self._datos) // 2 - 1, -1, -1):
            self._bajar(i)
