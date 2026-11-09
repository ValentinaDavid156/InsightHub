# Base: Semana 5 (Nodo, cadena enlazada) para cada lista de adyacencia y
#       Semana 10 (ColaEnlazada) para el recorrido por niveles.
# Lo nuevo para InsightHub: grafo NO dirigido (la amistad vale en los dos sentidos),
# insertar al inicio de cada lista, desenlazar con nodo anterior y candidatos a 2 saltos.
# Spec: specs/06-grafo/spec.md · Plan: specs/06-grafo/plan.md

from estructuras.cola import ColaEnlazada
from estructuras.nodo import Nodo


def _id_valido(valor):
    return isinstance(valor, int) and not isinstance(valor, bool) and valor >= 0


class Grafo:
    """Red de amistades: grafo no dirigido con lista de adyacencia.

    Un arreglo indexado por el id de la persona guarda la cabeza de su lista de
    amigos (nodos propios, `dato` = id del amigo) y otro su grado.

    Invariantes de representación:
        IR-01: b está en la lista de a  <=>  a está en la lista de b
        IR-02: nadie está en su propia lista ni aparece dos veces en la misma lista
        IR-03: _grados[i] == cantidad de nodos de la lista de i
        IR-04: cada lista va de la amistad más reciente a la más antigua

    V = personas · g = grado · E' = suma de los grados de los amigos de la consultada.
    Complejidad: agregar_vertice O(1) amortizado, agregar_amistad O(g),
                 eliminar_amistad O(g_a + g_b), son_amigos O(g), amigos O(g),
                 grado O(1), candidatos_dos_saltos O(V + g + E').
    """

    def __init__(self):
        self._cabezas = []     # arreglo indexado por id: primer nodo de la lista de amigos
        self._grados = []      # arreglo indexado por id: cantidad de amigos

    # ---------- personas ----------

    def agregar_vertice(self, persona):
        """Registra a `persona` sin amigos. Si ya existía no cambia nada. O(1) amortizado.

        Lanza ValueError si el id no es un entero >= 0. Los ids intermedios que falten
        quedan registrados también, sin amigos.
        """
        if not _id_valido(persona):
            raise ValueError(f"id de persona inválido: {persona!r}")
        faltan = persona + 1 - len(self._cabezas)
        if faltan > 0:
            self._cabezas.extend([None] * faltan)
            self._grados.extend([0] * faltan)

    def cantidad(self):
        """Personas registradas. O(1)."""
        return len(self._cabezas)

    def _existe(self, persona):
        return _id_valido(persona) and persona < len(self._cabezas)

    # ---------- consultas ----------

    def amigos(self, persona):
        """Ids de los amigos, el de la amistad más reciente primero. O(g).

        Persona inexistente o sin amigos: lista vacía.
        """
        if not self._existe(persona):
            return []
        resultado = []
        actual = self._cabezas[persona]
        while actual is not None:
            resultado.append(actual.dato)
            actual = actual.siguiente
        return resultado

    def grado(self, persona):
        """Cantidad de amigos (0 si no existe). O(1)."""
        if not self._existe(persona):
            return 0
        return self._grados[persona]

    def _en_lista(self, dueño, buscado):
        actual = self._cabezas[dueño]
        while actual is not None:
            if actual.dato == buscado:
                return True
            actual = actual.siguiente
        return False

    def son_amigos(self, a, b):
        """True si son amigos; da lo mismo el orden. O(g) de la lista más corta."""
        if not (self._existe(a) and self._existe(b)) or a == b:
            return False
        if self._grados[a] <= self._grados[b]:
            return self._en_lista(a, b)
        return self._en_lista(b, a)

    # ---------- crear y deshacer amistades ----------

    def agregar_amistad(self, a, b):
        """Crea la amistad en los dos sentidos. O(g).

        Devuelve True si la creó; False si se rechaza (la misma persona, ya son
        amigas o alguna no existe) sin cambiar ninguna lista.
        """
        # 1. validar todo antes de tocar algo: la amistad nunca queda en un solo sentido
        if not (self._existe(a) and self._existe(b)) or a == b:
            return False
        if self._en_lista(a, b):
            return False
        # 2. insertar al inicio: primero nuevo.siguiente y después la cabeza
        #    (al revés se pierde el resto de la lista)
        self._cabezas[a] = Nodo(b, self._cabezas[a])
        self._cabezas[b] = Nodo(a, self._cabezas[b])
        # 3. subir el grado de ambos
        self._grados[a] += 1
        self._grados[b] += 1
        return True

    def _desenlazar(self, dueño, buscado):
        """Quita `buscado` de la lista de `dueño` usando el nodo anterior. True si estaba."""
        anterior = None
        actual = self._cabezas[dueño]
        while actual is not None and actual.dato != buscado:
            anterior = actual
            actual = actual.siguiente
        if actual is None:
            return False
        if anterior is None:                       # era el primero
            self._cabezas[dueño] = actual.siguiente
        else:                                      # intermedio o último
            anterior.siguiente = actual.siguiente
        self._grados[dueño] -= 1
        return True

    def eliminar_amistad(self, a, b):
        """Deshace la amistad en los dos sentidos. O(g_a + g_b).

        Devuelve True si existía y la quitó; False si no existía, una de las
        personas no existe o es la misma, sin cambiar nada.
        """
        if not (self._existe(a) and self._existe(b)) or a == b:
            return False
        if not self._en_lista(a, b):
            return False
        self._desenlazar(a, b)
        self._desenlazar(b, a)
        return True

    # ---------- recomendaciones ----------

    def candidatos_dos_saltos(self, persona):
        """Amigos de amigos de `persona`: lista de (id, amigos_en_comun). O(V + g + E').

        Sin repetir a nadie y sin incluir a `persona` ni a sus amigos. Salen en el
        orden en que se descubren (ordenarlos es trabajo del montículo, CA-35).
        Persona inexistente o sin amigos: lista vacía.
        """
        if not self._existe(persona) or self._grados[persona] == 0:
            return []                                   # CA-36: la cola nacería vacía
        total = len(self._cabezas)
        excluido = [False] * total                      # arreglos temporales por id
        comunes = [0] * total
        excluido[persona] = True
        nivel_uno = ColaEnlazada()
        actual = self._cabezas[persona]
        while actual is not None:                       # amigos directos: nivel 1
            excluido[actual.dato] = True
            nivel_uno.encolar(actual.dato)
            actual = actual.siguiente
        candidatos = []                                 # ids en orden de descubrimiento
        while not nivel_uno.esta_vacia():
            amigo = nivel_uno.desencolar()
            vecino = self._cabezas[amigo]
            while vecino is not None:
                w = vecino.dato
                if not excluido[w]:
                    if comunes[w] == 0:
                        candidatos.append(w)
                    comunes[w] += 1
                vecino = vecino.siguiente
        return [(w, comunes[w]) for w in candidatos]
