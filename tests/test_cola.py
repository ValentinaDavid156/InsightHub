"""Pruebas de la cola y de las notificaciones (specs/03-cola).

Estilo de Semana10: funciones sueltas de pytest; cada docstring nombra el criterio CA
que verifica. CA-05 y CA-07 se completan con `dominio/amistades.py` (Avance 5, cuando
exista el grafo): aquí se prueba la parte de la cola que los sostiene.
"""

import pytest

from dominio.notificaciones import MENSAJE_SIN_NOTIFICACIONES, Notificaciones
from estructuras.cola import ColaEnlazada, ColaVaciaError


def _cola_con(*datos):
    cola = ColaEnlazada()
    for dato in datos:
        cola.encolar(dato)
    return cola


# ---------- encolar ----------
def test_encolar_xyz_y_desencolar_devuelve_xyz():
    """CA-07: encolar X, Y, Z y desencolar tres veces devuelve X, Y, Z."""
    cola = _cola_con("X", "Y", "Z")
    assert [cola.desencolar() for _ in range(3)] == ["X", "Y", "Z"]


def test_encolar_aumenta_el_tamano():
    """CA-07: cada encolar suma uno al tamaño."""
    cola = ColaEnlazada()
    for i in range(1, 4):
        cola.encolar(i)
        assert cola.tamano() == i


def test_encolar_en_vacia_deja_cabeza_y_cola_en_el_mismo_nodo():
    """CA-07: extremo, el primer elemento es cabeza y cola a la vez (IR-01)."""
    cola = ColaEnlazada()
    cola.encolar("solo")
    assert cola._cabeza is cola._cola
    assert cola.frente() == "solo"


def test_encolar_duplicados_se_conservan_en_orden():
    """CA-07: extremo, X, X, Y salen X, X, Y."""
    cola = _cola_con("X", "X", "Y")
    assert [cola.desencolar() for _ in range(3)] == ["X", "X", "Y"]


# ---------- desencolar ----------
def test_desencolar_un_solo_elemento_deja_la_cola_vacia():
    """CA-07: extremo, desencolar el único deja cabeza y cola en None."""
    cola = _cola_con("x")
    assert cola.desencolar() == "x"
    assert cola.esta_vacia()
    assert cola._cabeza is None
    assert cola._cola is None        # el error más común: olvidar esta línea


def test_vaciar_y_volver_a_encolar_respeta_el_orden():
    """CA-07: extremo, tras vaciar la cola, lo nuevo vuelve a quedar al frente."""
    cola = _cola_con(1, 2)
    cola.desencolar()
    cola.desencolar()
    cola.encolar(3)
    cola.encolar(4)
    assert [cola.desencolar() for _ in range(2)] == [3, 4]


def test_desencolar_reduce_el_tamano_y_devuelve_el_primero():
    """CA-07: desencolar devuelve el que llegó primero y resta uno."""
    cola = _cola_con(1, 2, 3)
    assert cola.desencolar() == 1
    assert cola.tamano() == 2
    assert cola.frente() == 2


def test_desencolar_en_vacia_lanza_error_controlado():
    """CA-07: sin solicitudes pendientes se avisa con ColaVaciaError, sin otro fallo."""
    with pytest.raises(ColaVaciaError):
        ColaEnlazada().desencolar()


def test_desencolar_en_vacia_no_modifica_la_cola():
    """CA-07: tras el error, la cola sigue vacía y se puede seguir usando."""
    cola = ColaEnlazada()
    with pytest.raises(ColaVaciaError):
        cola.desencolar()
    assert cola.tamano() == 0
    cola.encolar("a")
    assert cola.desencolar() == "a"


# ---------- frente ----------
def test_frente_no_quita_el_elemento():
    """CA-07: consultar el frente no cambia el tamaño."""
    cola = _cola_con("A", "B")
    assert cola.frente() == "A"
    assert cola.tamano() == 2


def test_frente_dos_veces_devuelve_lo_mismo():
    """CA-07: consultar dos veces seguidas da el mismo elemento."""
    cola = _cola_con("A", "B")
    assert cola.frente() == cola.frente() == "A"


def test_frente_avanza_al_desencolar():
    """CA-07: el frente pasa al siguiente que llegó."""
    cola = _cola_con("A", "B")
    cola.desencolar()
    assert cola.frente() == "B"


def test_frente_en_vacia_lanza_error_controlado():
    """CA-07: consultar el frente con la cola vacía avisa y no la modifica."""
    cola = ColaEnlazada()
    with pytest.raises(ColaVaciaError):
        cola.frente()
    assert cola.tamano() == 0


# ---------- contiene (sostiene CA-05: solicitud repetida) ----------
def test_contiene_un_elemento_presente():
    """CA-05: se puede saber si un elemento ya está pendiente."""
    cola = _cola_con("ana", "luis")
    assert cola.contiene("luis")
    assert cola.contiene("ana")


def test_contiene_un_elemento_ausente_o_en_cola_vacia():
    """CA-05: extremo, ausente y cola vacía devuelven False sin error."""
    assert not ColaEnlazada().contiene("x")
    assert not _cola_con("ana").contiene("luis")


def test_contiene_deja_de_ser_cierto_al_desencolar():
    """CA-05: un elemento ya atendido no cuenta como pendiente."""
    cola = _cola_con("ana", "luis")
    cola.desencolar()
    assert not cola.contiene("ana")
    assert cola.contiene("luis")


def test_contiene_no_modifica_la_cola():
    """CA-05: preguntar no cambia el tamaño ni el orden."""
    cola = _cola_con(1, 2, 3)
    cola.contiene(2)
    assert cola.tamano() == 3
    assert list(cola) == [1, 2, 3]


# ---------- esta_vacia, tamaño e iteración ----------
def test_esta_vacia_en_cola_nueva_con_elementos_y_al_vaciar():
    """CA-33: esta_vacia es True al inicio, False con datos y True al vaciar."""
    cola = ColaEnlazada()
    assert cola.esta_vacia()
    cola.encolar(1)
    assert not cola.esta_vacia()
    cola.desencolar()
    assert cola.esta_vacia()


def test_tamano_len_y_tamaño_coinciden():
    """CA-07: tamano(), tamaño() y len() devuelven lo mismo (tu nombre de Semana10 sigue vivo)."""
    cola = _cola_con(1, 2, 3)
    assert cola.tamano() == cola.tamaño() == len(cola) == 3


def test_iterar_recorre_del_frente_al_final_sin_sacar():
    """CA-07: iterar muestra el orden de llegada y deja la cola intacta."""
    cola = _cola_con("a", "b", "c")
    assert list(cola) == ["a", "b", "c"]
    assert cola.tamano() == 3


def test_estres_muchos_encolar_y_desencolar_mantienen_el_orden():
    """CA-07: estrés, 1000 encolar y 1000 desencolar salen en orden de llegada."""
    cola = ColaEnlazada()
    for i in range(1000):
        cola.encolar(i)
    assert [cola.desencolar() for _ in range(1000)] == list(range(1000))
    assert cola.esta_vacia()


# ---------- notificaciones ----------
def test_notificaciones_se_leen_en_orden_de_llegada():
    """CA-32: solicitud, amistad aceptada y respuesta se leen como llegaron."""
    avisos = Notificaciones()
    avisos.notificar(7, "solicitud de @ana")
    avisos.notificar(7, "@ana aceptó tu solicitud")
    avisos.notificar(7, "respuesta a tu publicación")
    assert avisos.leer(7) == [
        "solicitud de @ana",
        "@ana aceptó tu solicitud",
        "respuesta a tu publicación",
    ]


def test_leer_vacia_la_cola_de_notificaciones():
    """CA-32: tras leer, no quedan pendientes y la segunda lectura no repite nada."""
    avisos = Notificaciones()
    avisos.notificar(1, "a")
    avisos.leer(1)
    assert avisos.pendientes(1) == 0
    assert avisos.leer(1) == []


def test_cada_persona_tiene_su_propia_cola_de_avisos():
    """CA-32: los avisos de una persona no aparecen en otra."""
    avisos = Notificaciones()
    avisos.notificar(1, "para uno")
    avisos.notificar(2, "para dos")
    assert avisos.leer(2) == ["para dos"]
    assert avisos.leer(1) == ["para uno"]


def test_notificar_a_un_id_alto_y_leer_otro_vacio_no_falla():
    """CA-32: extremo, el arreglo de colas crece con el id y los huecos están vacíos."""
    avisos = Notificaciones()
    avisos.notificar(50, "lejos")
    assert avisos.pendientes(3) == 0
    assert avisos.leer(50) == ["lejos"]


def test_leer_sin_pendientes_informa_sin_notificaciones_y_no_falla():
    """CA-33: leer sin pendientes devuelve vacío y existe el mensaje «Sin notificaciones.»."""
    avisos = Notificaciones()
    assert avisos.leer(5) == []
    assert MENSAJE_SIN_NOTIFICACIONES == "Sin notificaciones."


def test_leer_persona_que_nunca_recibio_nada_no_crea_pendientes():
    """CA-33: extremo, preguntar por quien nunca tuvo avisos no cambia nada."""
    avisos = Notificaciones()
    assert avisos.pendientes(9) == 0
    assert avisos.leer(9) == []
    assert avisos.pendientes(9) == 0


def test_leer_dos_veces_seguidas_la_segunda_informa_vacio():
    """CA-33: la segunda lectura seguida no tiene pendientes."""
    avisos = Notificaciones()
    avisos.notificar(2, "x")
    assert avisos.leer(2) == ["x"]
    assert avisos.leer(2) == []


@pytest.mark.parametrize("persona", [-1, "ana", None, 1.5, True])
def test_persona_invalida_se_rechaza(persona):
    """CA-32: extremo, solo se aceptan ids enteros de cero en adelante."""
    avisos = Notificaciones()
    with pytest.raises(ValueError):
        avisos.notificar(persona, "x")
    with pytest.raises(ValueError):
        avisos.leer(persona)
