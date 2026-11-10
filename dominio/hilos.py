# Publicar, responder y mostrar: une la plaza, un árbol por publicación y los avisos.
# Spec: specs/04-arbol-general/spec.md (CA-14, CA-15, CA-16) · Plan: specs/04-arbol-general/plan.md
# Soporte interno: arreglos de Python indexados por id (la publicación y su árbol; la sesión de
# plaza de cada persona), con acceso O(1); declarados en el plan.

from estructuras.arbol_general import ArbolGeneral, RespuestaInvalidaError

ID_PUBLICACION = 0          # en cada hilo la publicación es el 0 (decisión de Valentina)


class Hilos:
    """Un hilo por publicación; las respuestas se numeran 1, 2, 3... dentro de cada hilo.

    Complejidad (n = elementos del hilo): publicar O(1) amortizado, existe O(1),
    tamano_de O(1), responder O(n), mostrar O(n), sesion_de O(1) amortizado.
    """

    def __init__(self, plaza, catalogo, notificaciones):
        self.plaza = plaza
        self._catalogo = catalogo
        self._notificaciones = notificaciones
        self._entradas = []     # arreglo por id de publicación: (publicacion, arbol) o None
        self._sesiones = []     # arreglo por id de persona: su SesionPlaza o None

    def publicar(self, autor, titulo, cuerpo, fecha=None):
        """Publica en la plaza y abre su hilo. Lanza PublicacionInvalidaError sin título."""
        publicacion = self.plaza.publicar(autor, titulo, cuerpo, fecha)
        arbol = ArbolGeneral()
        arbol.abrir_hilo(ID_PUBLICACION, autor, titulo)
        faltan = publicacion.id + 1 - len(self._entradas)
        self._entradas.extend([None] * faltan)
        self._entradas[publicacion.id] = (publicacion, arbol)
        return publicacion

    def existe(self, id_publicacion):
        """True si hay una publicación con ese número."""
        return (
            isinstance(id_publicacion, int)
            and not isinstance(id_publicacion, bool)
            and 0 <= id_publicacion < len(self._entradas)
            and self._entradas[id_publicacion] is not None
        )

    def tamano_de(self, id_publicacion):
        """Elementos del hilo, contando la publicación (0 si no existe)."""
        if not self.existe(id_publicacion):
            return 0
        return self._entradas[id_publicacion][1].tamano()

    def responder(self, id_publicacion, id_padre, autor, texto):
        """Agrega una respuesta y avisa al autor de la publicación, salvo que sea él mismo.

        Lanza RespuestaInvalidaError, sin cambiar nada, si la publicación o el padre no
        existen o si el texto está vacío (CA-16).
        """
        if not self.existe(id_publicacion):
            raise RespuestaInvalidaError("Esa publicación no existe.")
        if not isinstance(texto, str) or not texto.strip():
            raise RespuestaInvalidaError("La respuesta está vacía.")
        publicacion, arbol = self._entradas[id_publicacion]
        # no hay borrado: el tamaño actual siempre es un número libre (la publicación es el 0)
        nodo = arbol.responder(id_padre, arbol.tamano(), autor, texto)
        if autor != publicacion.autor:
            destinatario = self._catalogo.buscar(publicacion.autor)
            self._notificaciones.notificar(
                destinatario.id, f"@{autor} respondió a tu publicación «{publicacion.titulo}»."
            )
        return nodo

    def mostrar(self, id_publicacion):
        """El hilo como líneas con dos espacios por nivel (CA-15); [] si no existe."""
        if not self.existe(id_publicacion):
            return []
        publicacion, arbol = self._entradas[id_publicacion]
        lineas = []
        for nivel, nodo in arbol.recorrer():
            texto = nodo.texto
            if nivel == 0 and publicacion.cuerpo:
                texto = f"{texto} — {publicacion.cuerpo}"
            lineas.append(f"{'  ' * nivel}[{nodo.id}] @{nodo.autor}: {texto}")
        return lineas

    def sesion_de(self, persona):
        """La posición en la plaza de `persona`; se crea la primera vez y se conserva."""
        if persona >= len(self._sesiones):
            self._sesiones.extend([None] * (persona + 1 - len(self._sesiones)))
        if self._sesiones[persona] is None:
            self._sesiones[persona] = self.plaza.sesion()
        return self._sesiones[persona]
