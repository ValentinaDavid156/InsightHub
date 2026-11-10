# Amistades con solicitud y aceptación: une el catálogo (AVL), la cola y el grafo.
# Specs: specs/03-cola/spec.md (RF-07, RF-08, CA-05, CA-07) · specs/06-grafo/spec.md (CA-06, CA-08)
# Plan: specs/03-cola/plan.md §6
# Soporte interno: un arreglo de Python indexado por el id de la persona guarda su cola de
# solicitudes (la misma idea de notificaciones.py); la cola se crea con la primera solicitud.

from dominio.notificaciones import Notificaciones
from estructuras.cola import ColaEnlazada
from estructuras.grafo import Grafo

MENSAJE_SIN_SOLICITUDES = "No tienes solicitudes pendientes."


class SolicitudInvalidaError(ValueError):
    """La solicitud se rechaza; el mensaje dice el motivo (CA-05)."""


class Amistades:
    """Solicitudes pendientes (una cola por persona) y red de amistades (grafo).

    Complejidad (k = solicitudes pendientes de una persona, g = grado, n = perfiles):
        enviar O(log n + g + k), primera O(1), pendientes O(1),
        atender O(g), deshacer O(log n + g), amigos O(g).
    """

    def __init__(self, catalogo, grafo=None, notificaciones=None):
        self.catalogo = catalogo
        self.grafo = Grafo() if grafo is None else grafo
        self.notificaciones = Notificaciones() if notificaciones is None else notificaciones
        self._solicitudes = []      # arreglo indexado por id; None = nunca recibió solicitudes
        for perfil in catalogo.perfiles():
            self.grafo.agregar_vertice(perfil.id)

    def registrar(self, persona):
        """Registra en la red a un perfil creado después de arrancar. Si ya estaba, no cambia nada."""
        self.grafo.agregar_vertice(persona)

    def _cola_de(self, persona, crear=False):
        """La cola de solicitudes de `persona`, o None si no tiene (y no se pidió crearla)."""
        if self.catalogo.por_id(persona) is None:
            return None
        if persona >= len(self._solicitudes):
            if not crear:
                return None
            self._solicitudes.extend([None] * (persona + 1 - len(self._solicitudes)))
        if self._solicitudes[persona] is None and crear:
            self._solicitudes[persona] = ColaEnlazada()
        return self._solicitudes[persona]

    # ---------- solicitudes ----------

    def enviar(self, de, usuario_para):
        """Deja la solicitud de `de` (id) al final de la cola de `usuario_para` y lo avisa (CA-05).

        Devuelve el perfil del destinatario. Lanza SolicitudInvalidaError, sin cambiar nada, si
        alguno no existe, es uno mismo, ya son amigos, está repetida o el otro ya te la envió.
        """
        remitente = self.catalogo.por_id(de)
        if remitente is None:
            raise SolicitudInvalidaError("Quien envía la solicitud no existe.")
        destino = self.catalogo.buscar(usuario_para)
        if destino is None:
            raise SolicitudInvalidaError("Ese @usuario no existe.")
        if destino.id == remitente.id:
            raise SolicitudInvalidaError("No puedes enviarte una solicitud a ti mismo.")
        # un perfil recién creado también debe estar en la red; agregar_vertice es idempotente
        self.grafo.agregar_vertice(remitente.id)
        self.grafo.agregar_vertice(destino.id)
        if self.grafo.son_amigos(remitente.id, destino.id):
            raise SolicitudInvalidaError(f"Ya eres amigo de @{destino.usuario}.")
        cola_destino = self._cola_de(destino.id)
        if cola_destino is not None and cola_destino.contiene(remitente.id):
            raise SolicitudInvalidaError(f"Ya le enviaste una solicitud a @{destino.usuario}.")
        cola_propia = self._cola_de(remitente.id)
        if cola_propia is not None and cola_propia.contiene(destino.id):
            raise SolicitudInvalidaError(
                f"@{destino.usuario} ya te envió una solicitud: revísala en tus solicitudes."
            )
        self._cola_de(destino.id, crear=True).encolar(remitente.id)
        self.notificaciones.notificar(
            destino.id, f"@{remitente.usuario} te envió una solicitud de amistad."
        )
        return destino

    def pendientes(self, persona):
        """Cuántas solicitudes esperan a `persona` (0 si no existe). O(1)."""
        cola = self._cola_de(persona)
        return 0 if cola is None else cola.tamano()

    def primera(self, persona):
        """El perfil de quien envió la primera solicitud, sin sacarla; None si no hay (CA-07)."""
        cola = self._cola_de(persona)
        if cola is None or cola.esta_vacia():
            return None
        return self.catalogo.por_id(cola.frente())

    def atender(self, persona, aceptar):
        """Saca la primera solicitud y, si se acepta, crea la amistad y avisa (CA-06, CA-07).

        Devuelve el perfil de quien la envió, o None si no había pendientes.
        """
        cola = self._cola_de(persona)
        if cola is None or cola.esta_vacia():
            return None
        remitente = self.catalogo.por_id(cola.desencolar())
        if aceptar:
            self.grafo.agregar_amistad(persona, remitente.id)
            quien_acepta = self.catalogo.por_id(persona)
            self.notificaciones.notificar(
                remitente.id, f"@{quien_acepta.usuario} aceptó tu solicitud de amistad."
            )
        return remitente

    # ---------- amistades ----------

    def deshacer(self, persona, usuario_otro):
        """Deshace la amistad en ambos sentidos. False si no existe, sin error (CA-08)."""
        otro = self.catalogo.buscar(usuario_otro)
        if otro is None:
            return False
        return self.grafo.eliminar_amistad(persona, otro.id)

    def amigos(self, persona):
        """Los perfiles de sus amigos, el de la amistad más reciente primero."""
        return [self.catalogo.por_id(i) for i in self.grafo.amigos(persona)]
