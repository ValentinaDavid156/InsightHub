# Base: Semana 10 (arbol_binario.py): NodoArbol con izquierdo/derecho, inorden recursivo y la
# convención de altura «vacío = -1, hoja = 0». No tengo un árbol de búsqueda ni un AVL propio
# en el curso: la inserción ordenada, las rotaciones y la búsqueda por prefijo son nuevas.
# Spec: specs/05-avl/spec.md · Plan: specs/05-avl/plan.md


class NodoAVL:
    """Un nodo con clave, valor, altura y hasta dos hijos (como el NodoArbol de Semana10)."""

    def __init__(self, clave, valor, izquierdo=None, derecho=None):
        self.clave = clave
        self.valor = valor
        self.izquierdo = izquierdo
        self.derecho = derecho
        self.altura = 0

    def __repr__(self):
        return f"NodoAVL({self.clave!r})"


def _altura(nodo):
    return -1 if nodo is None else nodo.altura      # ¡NO 0! Igual que en Semana10


def _actualizar_altura(nodo):
    nodo.altura = 1 + max(_altura(nodo.izquierdo), _altura(nodo.derecho))


def _factor(nodo):
    """Altura izquierda menos altura derecha: en un AVL siempre está en [-1, 1]."""
    return _altura(nodo.izquierdo) - _altura(nodo.derecho)


def _rotar_derecha(y):
    """Sube el hijo izquierdo `x` y baja `y` a su derecha. Devuelve la nueva raíz `x`.

    Orden de punteros (si se cambia, se pierde un subárbol):
        1. t2 = x.derecho         (guardar antes de pisarlo)
        2. x.derecho = y
        3. y.izquierdo = t2
    y luego las alturas: primero `y` (ahora es el hijo) y después `x`.
    """
    x = y.izquierdo
    t2 = x.derecho
    x.derecho = y
    y.izquierdo = t2
    _actualizar_altura(y)
    _actualizar_altura(x)
    return x


def _rotar_izquierda(x):
    """Simétrica a _rotar_derecha: sube el hijo derecho `y` y baja `x` a su izquierda."""
    y = x.derecho
    t2 = y.izquierdo
    y.izquierdo = x
    x.derecho = t2
    _actualizar_altura(x)
    _actualizar_altura(y)
    return y


def _equilibrar(nodo):
    """Recalcula la altura de `nodo` y, si el factor sale de [-1, 1], rota. Devuelve la raíz del subárbol."""
    _actualizar_altura(nodo)
    factor = _factor(nodo)
    if factor > 1:                                   # pesa a la izquierda
        if _factor(nodo.izquierdo) < 0:              # izquierda-derecha: primero se endereza el hijo
            nodo.izquierdo = _rotar_izquierda(nodo.izquierdo)
        return _rotar_derecha(nodo)
    if factor < -1:                                  # pesa a la derecha
        if _factor(nodo.derecho) > 0:                # derecha-izquierda
            nodo.derecho = _rotar_derecha(nodo.derecho)
        return _rotar_izquierda(nodo)
    return nodo


class AVL:
    """Árbol binario de búsqueda equilibrado: la diferencia de alturas de los dos lados de
    cada nodo no pasa de 1, así que la altura es siempre <= 1.44*log2(n+2).

    Las claves se comparan con < y == (aquí son texto en minúsculas). Un valor None no se
    distingue de «no encontrado» en buscar().

    Invariantes de representación:
        IR-01: orden de búsqueda: izquierda < nodo < derecha en todo nodo
        IR-02: nodo.altura == 1 + max(altura de sus hijos) y |factor| <= 1 en todo nodo
        IR-03: _tamaño == cantidad de nodos

    Complejidad (n = claves, k = resultados):
        insertar O(log n), buscar O(log n), buscar_por_prefijo O(log n + k),
        recorrer_en_orden O(n), altura O(1), tamano O(1) (contador).
    """

    def __init__(self):
        self._raiz = None
        self._tamaño = 0

    def tamano(self):
        """Cantidad de claves. O(1)."""
        return self._tamaño

    tamaño = tamano  # el nombre que ya usaba en Semana4 a Semana10

    def altura(self):
        """Altura del árbol: vacío = -1, un solo nodo = 0. O(1) (se lee de la raíz)."""
        return _altura(self._raiz)

    def insertar(self, clave, valor):
        """Inserta (clave, valor) y reequilibra. Devuelve True si la clave era nueva.

        Si la clave ya existe devuelve False y no cambia nada (ni el valor ni el tamaño). O(log n).
        """
        self._raiz, insertado = self._insertar(self._raiz, clave, valor)
        if insertado:
            self._tamaño += 1
        return insertado

    def _insertar(self, nodo, clave, valor):
        """Baja por una rama y reequilibra al volver. Devuelve (raíz del subárbol, insertado)."""
        if nodo is None:
            return NodoAVL(clave, valor), True
        if clave == nodo.clave:
            return nodo, False
        if clave < nodo.clave:
            nodo.izquierdo, insertado = self._insertar(nodo.izquierdo, clave, valor)
        else:
            nodo.derecho, insertado = self._insertar(nodo.derecho, clave, valor)
        if not insertado:
            return nodo, False
        return _equilibrar(nodo), True

    def buscar(self, clave):
        """Valor de `clave`, o None si no está. O(log n): una comparación por nivel."""
        actual = self._raiz
        while actual is not None:
            if clave == actual.clave:
                return actual.valor
            actual = actual.izquierdo if clave < actual.clave else actual.derecho
        return None

    def recorrer_en_orden(self):
        """Lista de claves de menor a mayor (inorden de Semana10). O(n)."""
        resultado = []
        self._en_orden(self._raiz, resultado)
        return resultado

    def _en_orden(self, nodo, acumulador):
        if nodo is None:                             # CASO BASE — nunca lo omitas
            return
        self._en_orden(nodo.izquierdo, acumulador)
        acumulador.append(nodo.clave)
        self._en_orden(nodo.derecho, acumulador)

    def buscar_por_prefijo(self, prefijo):
        """Valores de todas las claves que empiezan por `prefijo`, en orden alfabético.

        Con prefijo vacío devuelve [] (decisión del spec). O(log n + k).

        En cada nodo: si la clave empieza por el prefijo se visitan los dos lados (izquierdo,
        la clave, derecho: orden alfabético); si la clave es menor que el prefijo, solo el
        derecho; si es mayor y no empieza por él, solo el izquierdo. Las claves con un prefijo
        forman un tramo contiguo, así que se descarta toda rama fuera del tramo.
        """
        resultado = []
        if prefijo:
            self._por_prefijo(self._raiz, prefijo, resultado)
        return resultado

    def _por_prefijo(self, nodo, prefijo, acumulador):
        if nodo is None:
            return
        if nodo.clave.startswith(prefijo):
            self._por_prefijo(nodo.izquierdo, prefijo, acumulador)
            acumulador.append(nodo.valor)
            self._por_prefijo(nodo.derecho, prefijo, acumulador)
        elif nodo.clave < prefijo:
            self._por_prefijo(nodo.derecho, prefijo, acumulador)
        else:
            self._por_prefijo(nodo.izquierdo, prefijo, acumulador)

    def __len__(self):
        return self._tamaño
