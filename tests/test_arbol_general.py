"""Pruebas del árbol general y de los hilos (specs/04-arbol-general), escritas antes del código.

Criterios Must: CA-14, CA-15 y CA-16. Decisiones de Valentina: los rechazos lanzan
RespuestaInvalidaError con el motivo; en cada hilo la publicación es el 0 y las respuestas se
numeran 1, 2, 3...; una respuesta o un título vacíos se rechazan (el cuerpo puede ir vacío).
"""

import pytest

from dominio.feed import Plaza, PublicacionInvalidaError
from dominio.hilos import Hilos
from dominio.notificaciones import Notificaciones
from dominio.usuarios import Catalogo
from estructuras.arbol_general import ArbolGeneral, RespuestaInvalidaError


def _hilo():
    arbol = ArbolGeneral()
    arbol.abrir_hilo(0, "ana", "pregunta")
    return arbol


def _recorrido(arbol):
    return [(nivel, nodo.id) for nivel, nodo in arbol.recorrer()]


# ---------- CA-14: respuesta de primer nivel ----------

def test_abrir_hilo_deja_solo_la_publicacion():
    """CA-14: un hilo sin respuestas tiene tamaño 1 y solo la publicación."""
    arbol = _hilo()
    assert arbol.tamano() == 1
    assert _recorrido(arbol) == [(0, 0)]


def test_abrir_dos_veces_el_mismo_hilo_se_rechaza():
    """CA-14: extremo, hay un solo punto de partida por hilo."""
    arbol = _hilo()
    with pytest.raises(RespuestaInvalidaError):
        arbol.abrir_hilo(9, "luis", "otra")
    assert _recorrido(arbol) == [(0, 0)]


def test_responder_a_la_publicacion_queda_en_nivel_uno():
    """CA-14: una respuesta a la publicación queda en el nivel 1."""
    arbol = _hilo()
    nodo = arbol.responder(0, 1, "luis", "hola")
    assert (nodo.id, nodo.autor, nodo.texto) == (1, "luis", "hola")
    assert arbol.profundidad(1) == 1
    assert _recorrido(arbol) == [(0, 0), (1, 1)]


def test_respuestas_del_mismo_nivel_quedan_en_orden_de_llegada():
    """CA-14: varias respuestas de primer nivel salen en orden cronológico."""
    arbol = _hilo()
    for i in (1, 2, 3):
        arbol.responder(0, i, "luis", f"r{i}")
    assert _recorrido(arbol) == [(0, 0), (1, 1), (1, 2), (1, 3)]


def test_responder_aumenta_el_tamano():
    """CA-14: el tamaño cuenta la publicación y cada respuesta."""
    arbol = _hilo()
    arbol.responder(0, 1, "luis", "a")
    arbol.responder(0, 2, "luis", "b")
    assert arbol.tamano() == 3 and len(arbol) == 3


def test_respuesta_nueva_empieza_con_puntaje_cero():
    """CA-14: el puntaje neto nace en 0 (lo actualizan los votos, Should)."""
    assert _hilo().responder(0, 1, "luis", "a").puntaje == 0


# ---------- CA-15: anidar y mostrar con nivel ----------

def test_cadena_de_tres_niveles():
    """CA-15: se puede responder a una respuesta al menos 3 niveles."""
    arbol = _hilo()
    arbol.responder(0, 1, "a", "n1")
    arbol.responder(1, 2, "b", "n2")
    arbol.responder(2, 3, "c", "n3")
    assert _recorrido(arbol) == [(0, 0), (1, 1), (2, 2), (3, 3)]


def test_cada_respuesta_sale_debajo_de_su_padre():
    """CA-15: se termina una rama completa antes de seguir con el hermano."""
    arbol = _hilo()
    arbol.responder(0, 1, "a", "x")
    arbol.responder(0, 2, "a", "x")
    arbol.responder(1, 3, "a", "x")
    arbol.responder(1, 4, "a", "x")
    arbol.responder(3, 5, "a", "x")
    arbol.responder(2, 6, "a", "x")
    assert _recorrido(arbol) == [(0, 0), (1, 1), (2, 3), (3, 5), (2, 4), (1, 2), (2, 6)]


def test_hijos_de_una_respuesta_en_orden_de_llegada():
    """CA-15: dentro de cada nivel el orden es cronológico."""
    arbol = _hilo()
    arbol.responder(0, 1, "a", "x")
    for i in (2, 3, 4):
        arbol.responder(1, i, "a", "x")
    assert _recorrido(arbol) == [(0, 0), (1, 1), (2, 2), (2, 3), (2, 4)]


def test_buscar_y_profundidad():
    """CA-15: se sabe si una respuesta existe y a qué nivel está."""
    arbol = _hilo()
    arbol.responder(0, 1, "a", "x")
    arbol.responder(1, 2, "b", "y")
    assert arbol.buscar(2).autor == "b"
    assert arbol.profundidad(0) == 0
    assert arbol.profundidad(2) == 2
    assert arbol.buscar(9) is None
    assert arbol.profundidad(9) is None


def test_recorrer_no_modifica_el_hilo():
    """CA-15: mostrar dos veces da lo mismo."""
    arbol = _hilo()
    arbol.responder(0, 1, "a", "x")
    arbol.responder(1, 2, "a", "x")
    assert _recorrido(arbol) == _recorrido(arbol)
    assert arbol.tamano() == 3


def test_hilo_sin_abrir_no_falla():
    """CA-15: extremo, un árbol vacío no tiene nada que recorrer."""
    arbol = ArbolGeneral()
    assert arbol.recorrer() == []
    assert arbol.tamano() == 0
    assert arbol.buscar(0) is None
    assert arbol.profundidad(0) is None


def test_hilo_de_2000_niveles_no_agota_la_recursion():
    """CA-15: el recorrido usa la pila propia, no la recursión de Python."""
    arbol = _hilo()
    for i in range(1, 2001):
        arbol.responder(i - 1, i, "a", "x")
    recorrido = _recorrido(arbol)
    assert len(recorrido) == 2001
    assert recorrido[-1] == (2000, 2000)
    assert arbol.profundidad(2000) == 2000


# ---------- CA-16: padre inexistente e identificador repetido ----------

def test_responder_a_un_padre_inexistente_se_rechaza():
    """CA-16: el hilo no cambia."""
    arbol = _hilo()
    arbol.responder(0, 1, "a", "x")
    antes = _recorrido(arbol)
    with pytest.raises(RespuestaInvalidaError, match="no existe"):
        arbol.responder(9, 2, "a", "x")
    assert _recorrido(arbol) == antes and arbol.tamano() == 2


def test_responder_a_una_publicacion_de_otro_hilo_se_rechaza():
    """CA-16: el padre se busca solo en este hilo."""
    uno, otro = ArbolGeneral(), ArbolGeneral()
    uno.abrir_hilo(100, "ana", "p1")
    otro.abrir_hilo(200, "luis", "p2")
    with pytest.raises(RespuestaInvalidaError, match="no existe"):
        uno.responder(200, 1, "a", "x")
    assert uno.tamano() == 1 and otro.tamano() == 1


def test_responder_en_hilo_sin_abrir_se_rechaza():
    """CA-16: sin publicación no hay a quién responder."""
    with pytest.raises(RespuestaInvalidaError, match="no existe"):
        ArbolGeneral().responder(0, 1, "a", "x")


def test_identificador_repetido_se_rechaza():
    """RF-05: no se agrega y el hilo no cambia."""
    arbol = _hilo()
    arbol.responder(0, 1, "a", "x")
    with pytest.raises(RespuestaInvalidaError, match="ya existe"):
        arbol.responder(0, 1, "b", "y")
    with pytest.raises(RespuestaInvalidaError, match="ya existe"):
        arbol.responder(1, 0, "b", "y")
    assert arbol.tamano() == 2
    assert arbol.buscar(1).autor == "a"


# ---------- Dominio: publicar, responder y avisar ----------

def _foro():
    catalogo = Catalogo()
    for usuario in ("ana", "luis", "sara"):
        catalogo.crear_perfil(usuario)
    avisos = Notificaciones()
    return Hilos(Plaza(), catalogo, avisos), avisos


def test_publicar_abre_el_hilo_y_deja_la_publicacion_primera():
    """CA-14: al publicar existe su hilo, sin respuestas; aparece primera en la plaza (CA-12)."""
    foro, _ = _foro()
    foro.publicar("ana", "uno", "c")
    segunda = foro.publicar("luis", "dos", "c")
    assert next(iter(foro.plaza)) is segunda
    assert foro.existe(segunda.id)
    assert foro.tamano_de(segunda.id) == 1


def test_titulo_vacio_se_rechaza():
    """Decisión de Valentina: una publicación necesita título; la plaza no cambia."""
    foro, _ = _foro()
    for titulo in ("", "   "):
        with pytest.raises(PublicacionInvalidaError, match="título"):
            foro.publicar("ana", titulo, "c")
    assert foro.plaza.tamano() == 0


def test_cuerpo_vacio_se_permite():
    """Decisión de Valentina: el cuerpo puede ir vacío."""
    foro, _ = _foro()
    assert foro.publicar("ana", "solo título", "").cuerpo == ""


def test_las_respuestas_se_numeran_por_hilo():
    """Decisión de Valentina: cada hilo numera desde 1; la publicación es el 0."""
    foro, _ = _foro()
    p1 = foro.publicar("ana", "uno", "c")
    p2 = foro.publicar("ana", "dos", "c")
    assert foro.responder(p1.id, 0, "luis", "a").id == 1
    assert foro.responder(p1.id, 1, "sara", "b").id == 2
    assert foro.responder(p2.id, 0, "luis", "c").id == 1


def test_responder_a_una_respuesta_inexistente_no_altera_el_hilo():
    """CA-16 integrado."""
    foro, avisos = _foro()
    p = foro.publicar("ana", "uno", "c")
    with pytest.raises(RespuestaInvalidaError, match="no existe"):
        foro.responder(p.id, 7, "luis", "a")
    assert foro.tamano_de(p.id) == 1
    assert avisos.pendientes(0) == 0


@pytest.mark.parametrize("id_publicacion", [99, 0, -1, "x", None])
def test_responder_a_una_publicacion_inexistente_se_rechaza(id_publicacion):
    """CA-16: la publicación debe existir."""
    foro, _ = _foro()
    foro.publicar("ana", "uno", "c")
    assert not foro.existe(id_publicacion)
    with pytest.raises(RespuestaInvalidaError, match="no existe"):
        foro.responder(id_publicacion, 0, "luis", "a")


@pytest.mark.parametrize("texto", ["", "   "])
def test_respuesta_vacia_se_rechaza(texto):
    """Decisión de Valentina: no hay respuestas en blanco."""
    foro, avisos = _foro()
    p = foro.publicar("ana", "uno", "c")
    with pytest.raises(RespuestaInvalidaError, match="vacía"):
        foro.responder(p.id, 0, "luis", texto)
    assert foro.tamano_de(p.id) == 1
    assert avisos.pendientes(0) == 0


def test_responder_avisa_al_autor_de_la_publicacion():
    """RF-09 de la cola: el aviso va al autor de la publicación."""
    foro, avisos = _foro()
    p = foro.publicar("ana", "uno", "c")
    foro.responder(p.id, 0, "luis", "a")
    assert avisos.leer(0) == ["@luis respondió a tu publicación «uno»."]


def test_responder_a_una_respuesta_avisa_al_autor_de_la_publicacion_y_no_al_de_la_respuesta():
    """RF-09 de la cola: extremo del hilo."""
    foro, avisos = _foro()
    p = foro.publicar("ana", "uno", "c")
    foro.responder(p.id, 0, "luis", "a")
    avisos.leer(0)
    foro.responder(p.id, 1, "sara", "b")
    assert avisos.pendientes(0) == 1
    assert avisos.pendientes(1) == 0


def test_el_autor_que_responde_no_se_avisa_a_si_mismo():
    """RF-09 de la cola: sin aviso si responde el propio autor."""
    foro, avisos = _foro()
    p = foro.publicar("ana", "uno", "c")
    foro.responder(p.id, 0, "ana", "a")
    assert avisos.pendientes(0) == 0


def test_mostrar_con_sangria_por_nivel():
    """CA-15: el hilo completo, con dos espacios por nivel."""
    foro, _ = _foro()
    p = foro.publicar("ana", "uno", "cuerpo")
    foro.responder(p.id, 0, "luis", "a")
    foro.responder(p.id, 1, "sara", "b")
    foro.responder(p.id, 2, "luis", "c")
    foro.responder(p.id, 0, "sara", "d")
    assert foro.mostrar(p.id) == [
        "[0] @ana: uno — cuerpo",
        "  [1] @luis: a",
        "    [2] @sara: b",
        "      [3] @luis: c",
        "  [4] @sara: d",
    ]


def test_mostrar_sin_cuerpo_ni_respuestas():
    """CA-15: extremo, solo la publicación."""
    foro, _ = _foro()
    p = foro.publicar("ana", "uno", "")
    assert foro.mostrar(p.id) == ["[0] @ana: uno"]


def test_mostrar_publicacion_inexistente_da_vacio():
    """CA-16: extremo, sin error."""
    foro, _ = _foro()
    assert foro.mostrar(5) == []
    assert foro.tamano_de(5) == 0


def test_cada_persona_conserva_su_posicion_en_la_plaza():
    """CA-13 integrado: la sesión de cada persona es propia y se conserva."""
    foro, _ = _foro()
    for i in range(7):
        foro.publicar("ana", f"p{i}", "c")
    sesion_ana = foro.sesion_de(0)
    sesion_ana.ver()
    sesion_ana.siguiente()
    assert foro.sesion_de(0) is sesion_ana
    pagina_luis, _ = foro.sesion_de(1).ver()
    pagina_ana, _ = foro.sesion_de(0).ver()
    assert pagina_luis[0].titulo == "p6"
    assert pagina_ana[0].titulo == "p1"
