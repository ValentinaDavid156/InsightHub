# La plaza pública (feed) y la posición de cada sesión sobre ella.
# Spec: specs/01-lista-doble/spec.md (RF-01 a RF-07, CA-12, CA-13)
# Plan: specs/01-lista-doble/plan.md §5 (marcador por sesión)
# La Publicacion vive aquí (decisión de Valentina): el árbol y el montículo la importan de este módulo.

import datetime

from estructuras.lista_doble import ListaDoble

MENSAJE_FIN_PLAZA = "Llegaste al final de la plaza."
MENSAJE_INICIO_PLAZA = "Estás en el principio de la plaza."
MENSAJE_PLAZA_VACIA = "No hay publicaciones."


class PublicacionInvalidaError(ValueError):
    """La publicación se rechaza; el mensaje dice el motivo. La plaza no cambia."""


class Publicacion:
    """Una pregunta publicada: identificador, autor, título, cuerpo y fecha (AAAA-MM-DD)."""

    def __init__(self, id, autor, titulo, cuerpo, fecha):
        self.id = id
        self.autor = autor
        self.titulo = titulo
        self.cuerpo = cuerpo
        self.fecha = fecha

    def __repr__(self):
        return f"Publicacion({self.id}, {self.titulo!r})"


class Plaza:
    """Todas las publicaciones, la más nueva primero, sobre una ListaDoble.

    Complejidad: publicar O(1), tamano O(1), recorrer O(n).
    """

    def __init__(self):
        self._lista = ListaDoble()
        self._siguiente_id = 1

    def publicar(self, autor, titulo, cuerpo, fecha=None):
        """Crea la publicación y la deja como la primera de la plaza (CA-12).

        Lanza PublicacionInvalidaError si el título está vacío; el cuerpo puede ir vacío.
        """
        if not isinstance(titulo, str) or not titulo.strip():
            raise PublicacionInvalidaError("La publicación necesita un título.")
        if fecha is None:
            fecha = datetime.date.today().isoformat()
        publicacion = Publicacion(self._siguiente_id, autor, titulo, cuerpo, fecha)
        self._siguiente_id += 1
        self._lista.insertar_al_frente(publicacion)
        return publicacion

    def tamano(self):
        return self._lista.tamano()

    def esta_vacia(self):
        return self._lista.esta_vacia()

    def sesion(self):
        """Una posición propia sobre la plaza, para una persona (RF-04)."""
        return SesionPlaza(self._lista)

    def __iter__(self):
        """De la más nueva a la más antigua, sin modificar."""
        return iter(self._lista)


class SesionPlaza:
    """La posición de una sesión: un marcador sobre la lista, independiente de otras sesiones.

    Cada operación devuelve (pagina, aviso): `pagina` es la lista de hasta 5 publicaciones
    y `aviso` es None o el mensaje del límite (CA-13) o de plaza vacía.
    """

    def __init__(self, lista):
        self._lista = lista
        self._marcador = None

    def _asegurar_marcador(self):
        # La sesión pudo abrirse con la plaza vacía: se coloca en la primera publicación al llegar.
        if self._marcador is None:
            self._marcador = self._lista.inicio()

    def _devolver(self, aviso=None):
        if self._marcador is None:
            return [], MENSAJE_PLAZA_VACIA
        return self._lista.pagina(self._marcador), aviso

    def ver(self):
        """Muestra la página actual."""
        self._asegurar_marcador()
        return self._devolver()

    def siguiente(self):
        """Página siguiente (hacia las más antiguas); en la última conserva la posición y avisa."""
        self._asegurar_marcador()
        if self._marcador is None:
            return self._devolver()
        self._marcador, se_movio = self._lista.avanzar(self._marcador)
        return self._devolver(None if se_movio else MENSAJE_FIN_PLAZA)

    def anterior(self):
        """Página anterior (hacia las más nuevas); en la primera conserva la posición y avisa."""
        self._asegurar_marcador()
        if self._marcador is None:
            return self._devolver()
        self._marcador, se_movio = self._lista.retroceder(self._marcador)
        return self._devolver(None if se_movio else MENSAJE_INICIO_PLAZA)

    def inicio(self):
        """Vuelve a la publicación más nueva."""
        self._marcador = self._lista.inicio()
        return self._devolver()
