# Notificaciones pendientes de cada persona: una cola por persona.
# Spec: specs/03-cola/spec.md (RF-09, RF-10, CA-32, CA-33) · Plan: specs/03-cola/plan.md §6
# Soporte interno: un arreglo de Python indexado por el id de la persona guarda su cola
# (declarado en el plan); la cola de cada persona se crea la primera vez que recibe un aviso.

from estructuras.cola import ColaEnlazada

MENSAJE_SIN_NOTIFICACIONES = "Sin notificaciones."


class Notificaciones:
    """Colas de avisos por persona (solicitud, amistad aceptada, respuesta).

    Complejidad (k = avisos pendientes de la persona):
        notificar O(1) amortizado, pendientes O(1), leer O(k).
    """

    def __init__(self):
        self._colas = []      # arreglo indexado por id; None = nunca recibió avisos

    @staticmethod
    def _validar(persona):
        if isinstance(persona, bool) or not isinstance(persona, int) or persona < 0:
            raise ValueError(f"id de persona inválido: {persona!r}")

    def _cola_de(self, persona, crear):
        if persona >= len(self._colas):
            if not crear:
                return None
            self._colas.extend([None] * (persona + 1 - len(self._colas)))
        if self._colas[persona] is None and crear:
            self._colas[persona] = ColaEnlazada()
        return self._colas[persona]

    def notificar(self, persona, mensaje):
        """Encola `mensaje` al final de los avisos de `persona`."""
        self._validar(persona)
        self._cola_de(persona, crear=True).encolar(mensaje)

    def pendientes(self, persona):
        """Cuántos avisos tiene `persona` sin leer (0 si nunca recibió)."""
        self._validar(persona)
        cola = self._cola_de(persona, crear=False)
        return 0 if cola is None else cola.tamano()

    def leer(self, persona):
        """Devuelve todos los avisos en el orden en que llegaron y deja la cola vacía.

        Sin pendientes devuelve una lista vacía (la interfaz muestra
        MENSAJE_SIN_NOTIFICACIONES): CA-33.
        """
        self._validar(persona)
        cola = self._cola_de(persona, crear=False)
        leidos = []
        while cola is not None and not cola.esta_vacia():
            leidos.append(cola.desencolar())
        return leidos
