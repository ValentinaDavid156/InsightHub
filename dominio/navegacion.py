# Historial de pantallas («atrás») sobre la pila propia.
# Spec: specs/02-pila/spec.md (RF-06, CA-30, CA-31) · Plan: specs/02-pila/plan.md §5
# La regla «no apilar la pantalla repetida» vive aquí y no en la pila, para que
# la pila siga siendo genérica (también la usa el árbol general).

from estructuras.pila import PilaEnlazada, PilaVaciaError

MENSAJE_SIN_PANTALLA_PREVIA = "No hay pantalla previa."


class Navegacion:
    """Historial de una sesión: la pantalla actual y las anteriores en una pila.

    Complejidad: ir_a O(1), atras O(1). El historial no tiene tamaño máximo.
    """

    def __init__(self):
        self._historial = PilaEnlazada()
        self._actual = None

    @property
    def actual(self):
        """La pantalla en la que está la sesión (None si aún no entró a ninguna)."""
        return self._actual

    def ir_a(self, pantalla):
        """Abre `pantalla` guardando la actual en el historial.

        Devuelve False (y no apila nada) si `pantalla` es igual a la actual.
        """
        if pantalla == self._actual:
            return False
        if self._actual is not None:
            self._historial.apilar(self._actual)
        self._actual = pantalla
        return True

    def atras(self):
        """Vuelve a la pantalla guardada más reciente y la devuelve.

        Con el historial vacío devuelve None y deja la pantalla actual igual
        (la interfaz muestra MENSAJE_SIN_PANTALLA_PREVIA): CA-31.
        """
        try:
            anterior = self._historial.desapilar()
        except PilaVaciaError:
            return None
        self._actual = anterior
        return anterior
