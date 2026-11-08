# Usuarios de InsightHub: índice por @usuario sobre el AVL, ids por arreglo y comunidad inicial.
# Spec: specs/05-avl/spec.md (RF-01 a RF-05, CA-01 a CA-04, CA-27, CA-28) · Plan: specs/05-avl/plan.md §7
# Soporte interno: un arreglo de Python indexado por id (declarado en estructuras.md) para
# llegar a un perfil por su id en O(1); `random.Random` y los nombres no son estructuras declaradas.

import random
import re

from estructuras.avl import AVL

SEMILLA = 706132            # Constitución, principio 9
CANTIDAD_INICIAL = 120      # CA-01: al menos 100 perfiles
MINIMO = 3
MAXIMO = 20

# 40 nombres sin tildes ni ñ (así cumplen las reglas del @usuario); lista aprobada por Valentina.
NOMBRES = (
    "ana", "luis", "maria", "carlos", "sofia", "andres", "camila", "juan", "valentina", "daniel",
    "laura", "felipe", "paula", "diego", "natalia", "sebastian", "daniela", "mateo", "isabella",
    "santiago", "mariana", "julian", "catalina", "david", "juliana", "nicolas", "carolina",
    "miguel", "alejandra", "samuel", "lucia", "tomas", "gabriela", "esteban", "sara", "jorge",
    "manuela", "camilo", "andrea", "simon",
)


class UsuarioInvalidoError(ValueError):
    """El @usuario no cumple las reglas (vacío, longitud, caracteres) o ya existe."""


class Perfil:
    """Una persona de la comunidad: id (posición en el catálogo), @usuario en minúsculas y puntos."""

    def __init__(self, id, usuario, puntos=0):
        self.id = id
        self.usuario = usuario
        self.puntos = puntos

    def __repr__(self):
        return f"Perfil({self.id}, @{self.usuario})"


def normalizar_usuario(texto):
    """Devuelve el @usuario válido en minúsculas y sin la arroba inicial, o lanza UsuarioInvalidoError.

    Reglas (CA-04): de 3 a 20 caracteres; letras a-z, números y guión bajo; sin distinguir
    mayúsculas; la @ inicial es opcional (una @ en medio es un carácter no permitido).
    """
    if not isinstance(texto, str):
        raise UsuarioInvalidoError("El @usuario debe ser texto")
    usuario = texto.lower()
    if usuario.startswith("@"):
        usuario = usuario[1:]
    if not usuario.strip():
        raise UsuarioInvalidoError("El @usuario está vacío")
    if len(usuario) < MINIMO:
        raise UsuarioInvalidoError(f"El @usuario es muy corto (mínimo {MINIMO} caracteres)")
    if len(usuario) > MAXIMO:
        raise UsuarioInvalidoError(f"El @usuario es muy largo (máximo {MAXIMO} caracteres)")
    if not re.fullmatch(r"[a-z0-9_]+", usuario):
        raise UsuarioInvalidoError(
            "El @usuario solo puede tener letras, números y guión bajo (sin espacios, tildes ni otros signos)"
        )
    return usuario


def _clave_de_busqueda(texto):
    """Clave para consultar (minúsculas, sin @ inicial) o None si no hay nada que buscar."""
    if not isinstance(texto, str):
        return None
    clave = texto.lower()
    if clave.startswith("@"):
        clave = clave[1:]
    return clave if clave.strip() else None


class Catalogo:
    """Todos los perfiles: el AVL (clave @usuario) para buscar y un arreglo por id.

    Complejidad (n = perfiles, k = coincidencias): crear_perfil O(log n), entrar O(log n),
    buscar O(log n), buscar_por_prefijo O(log n + k), por_id O(1), tamano O(1).
    """

    def __init__(self):
        self._indice = AVL()      # @usuario -> Perfil
        self._por_id = []         # arreglo indexado por id

    def tamano(self):
        return len(self._por_id)

    def __len__(self):
        return len(self._por_id)

    def perfiles(self):
        """Los perfiles en orden de creación (id 0, 1, 2...)."""
        return list(self._por_id)

    def por_id(self, id):
        """El perfil con ese id, o None si no existe. O(1)."""
        if isinstance(id, int) and not isinstance(id, bool) and 0 <= id < len(self._por_id):
            return self._por_id[id]
        return None

    def buscar(self, usuario):
        """El perfil de ese @usuario (sin distinguir mayúsculas), o None."""
        clave = _clave_de_busqueda(usuario)
        return None if clave is None else self._indice.buscar(clave)

    def buscar_por_prefijo(self, prefijo):
        """Perfiles cuyo @usuario empieza por `prefijo`, en orden alfabético (CA-27).

        Sin coincidencias, o con prefijo vacío o que no es texto, devuelve [] (CA-28).
        """
        clave = _clave_de_busqueda(prefijo)
        return [] if clave is None else self._indice.buscar_por_prefijo(clave)

    def crear_perfil(self, usuario):
        """Crea el perfil con 0 puntos. Lanza UsuarioInvalidoError si es inválido o ya existe (CA-04)."""
        clave = normalizar_usuario(usuario)
        if self._indice.buscar(clave) is not None:
            raise UsuarioInvalidoError("El @usuario ya existe")
        perfil = Perfil(len(self._por_id), clave)
        self._indice.insertar(clave, perfil)
        self._por_id.append(perfil)
        return perfil

    def entrar(self, usuario):
        """Abre la sesión: devuelve (perfil, creado).

        Con un @usuario nuevo y válido crea el perfil; con uno existente solo lo devuelve
        sin tocarlo (CA-03). Con uno inválido lanza UsuarioInvalidoError.
        """
        clave = normalizar_usuario(usuario)
        perfil = self._indice.buscar(clave)
        if perfil is not None:
            return perfil, False
        return self.crear_perfil(clave), True


def generar_comunidad(semilla=SEMILLA, cantidad=CANTIDAD_INICIAL):
    """Catálogo con `cantidad` perfiles de ejemplo, siempre iguales para la misma semilla (CA-01, CA-02).

    Cada @usuario es un nombre de NOMBRES y un número del 01 al 99 (por ejemplo mariana_07);
    si sale repetido se vuelve a sortear. Lanza ValueError si no hay tantas combinaciones.
    """
    if cantidad > len(NOMBRES) * 99:
        raise ValueError(f"no hay {cantidad} combinaciones distintas de nombre y número")
    azar = random.Random(semilla)
    catalogo = Catalogo()
    while len(catalogo) < cantidad:
        usuario = f"{azar.choice(NOMBRES)}_{azar.randint(1, 99):02d}"
        if catalogo.buscar(usuario) is None:
            catalogo.crear_perfil(usuario)
    return catalogo
