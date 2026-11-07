"""Pruebas de la pila y de la navegación «atrás» (specs/02-pila).

Estilo de Semana10: funciones sueltas de pytest; cada docstring nombra el criterio CA
que verifica (CA-30 o CA-31) o la operación que cubre con sus casos extremos.
"""

import pytest

from dominio.navegacion import MENSAJE_SIN_PANTALLA_PREVIA, Navegacion
from estructuras.pila import PilaEnlazada, PilaVaciaError


def _pila_con(*datos):
    pila = PilaEnlazada()
    for dato in datos:
        pila.apilar(dato)
    return pila


# ---------- apilar ----------
def test_apilar_abc_y_desapilar_devuelve_cba():
    """CA-30: apilar A, B, C y desapilar tres veces devuelve C, B, A."""
    pila = _pila_con("A", "B", "C")
    assert [pila.desapilar() for _ in range(3)] == ["C", "B", "A"]


def test_apilar_aumenta_el_tamano():
    """CA-30: cada apilar suma uno al tamaño."""
    pila = PilaEnlazada()
    for i in range(1, 4):
        pila.apilar(i)
        assert pila.tamano() == i


def test_apilar_sobre_vacia_fija_el_tope():
    """CA-30: extremo, apilar en una pila vacía deja ese elemento como tope."""
    pila = PilaEnlazada()
    pila.apilar("solo")
    assert pila.tope() == "solo"
    assert not pila.esta_vacia()


def test_apilar_duplicados_no_consecutivos_se_conservan():
    """CA-30: extremo, A, B, A se guardan los tres y salen A, B, A."""
    pila = _pila_con("A", "B", "A")
    assert [pila.desapilar() for _ in range(3)] == ["A", "B", "A"]


def test_apilar_none_no_se_confunde_con_pila_vacia():
    """CA-31: extremo, un None apilado es un dato; vacía es otra cosa."""
    pila = _pila_con(None)
    assert not pila.esta_vacia()
    assert pila.desapilar() is None
    assert pila.esta_vacia()


# ---------- desapilar ----------
def test_desapilar_un_solo_elemento_deja_la_pila_vacia():
    """CA-30: extremo, desapilar el único elemento deja la pila vacía."""
    pila = _pila_con("x")
    assert pila.desapilar() == "x"
    assert pila.esta_vacia()
    assert pila.tamano() == 0


def test_desapilar_reduce_el_tamano_y_devuelve_el_tope():
    """CA-30: desapilar devuelve el último apilado y resta uno."""
    pila = _pila_con(1, 2, 3)
    assert pila.desapilar() == 3
    assert pila.tamano() == 2
    assert pila.tope() == 2


def test_desapilar_en_vacia_lanza_error_controlado():
    """CA-31: desapilar en pila vacía avisa con PilaVaciaError."""
    pila = PilaEnlazada()
    with pytest.raises(PilaVaciaError):
        pila.desapilar()


def test_desapilar_en_vacia_no_modifica_la_pila():
    """CA-31: tras el error, la pila sigue vacía y se puede seguir usando."""
    pila = PilaEnlazada()
    with pytest.raises(PilaVaciaError):
        pila.desapilar()
    assert pila.tamano() == 0
    pila.apilar("a")
    assert pila.desapilar() == "a"


def test_vaciar_y_volver_a_apilar():
    """CA-30: extremo, tras quedar vacía la pila vuelve a funcionar (cabeza en None)."""
    pila = _pila_con(1, 2)
    pila.desapilar()
    pila.desapilar()
    pila.apilar(9)
    assert pila.tope() == 9
    assert pila.tamano() == 1


# ---------- tope ----------
def test_tope_no_quita_el_elemento():
    """CA-30: consultar el tope no cambia el tamaño."""
    pila = _pila_con("A", "B")
    assert pila.tope() == "B"
    assert pila.tamano() == 2


def test_tope_dos_veces_devuelve_lo_mismo():
    """CA-30: consultar dos veces seguidas da el mismo elemento."""
    pila = _pila_con("A", "B")
    assert pila.tope() == pila.tope() == "B"


def test_tope_cambia_al_apilar_y_al_desapilar():
    """CA-30: el tope sigue al último apilado."""
    pila = _pila_con("A")
    pila.apilar("B")
    assert pila.tope() == "B"
    pila.desapilar()
    assert pila.tope() == "A"


def test_tope_en_vacia_lanza_error_controlado():
    """CA-31: consultar el tope con la pila vacía avisa y no la modifica."""
    pila = PilaEnlazada()
    with pytest.raises(PilaVaciaError):
        pila.tope()
    assert pila.tamano() == 0


# ---------- esta_vacia y tamaño ----------
def test_esta_vacia_en_pila_nueva_con_elementos_y_al_vaciar():
    """CA-31: esta_vacia es True al inicio, False con datos y True al vaciar."""
    pila = PilaEnlazada()
    assert pila.esta_vacia()
    pila.apilar(1)
    assert not pila.esta_vacia()
    pila.desapilar()
    assert pila.esta_vacia()


def test_tamano_len_y_tamaño_coinciden():
    """CA-30: tamano(), tamaño() y len() devuelven lo mismo (tu nombre de Semana10 sigue vivo)."""
    pila = _pila_con(1, 2, 3)
    assert pila.tamano() == pila.tamaño() == len(pila) == 3


def test_estres_muchos_apilar_y_desapilar_mantienen_el_orden():
    """CA-30: estrés, 1000 apilar y 1000 desapilar salen en orden inverso."""
    pila = PilaEnlazada()
    for i in range(1000):
        pila.apilar(i)
    assert pila.tamano() == 1000
    assert [pila.desapilar() for _ in range(1000)] == list(range(999, -1, -1))
    assert pila.esta_vacia()


# ---------- navegación «atrás» ----------
def test_atras_retrocede_en_orden_inverso():
    """CA-30: «atrás» vuelve a la pantalla visitada justo antes, y repetirlo retrocede en orden inverso."""
    nav = Navegacion()
    for pantalla in ["inicio", "plaza", "hilo"]:
        nav.ir_a(pantalla)
    assert nav.atras() == "plaza"
    assert nav.atras() == "inicio"
    assert nav.actual == "inicio"


def test_ir_a_la_misma_pantalla_no_la_apila_dos_veces():
    """CA-30: abrir dos veces seguidas la misma pantalla no hace crecer el historial."""
    nav = Navegacion()
    nav.ir_a("inicio")
    assert nav.ir_a("plaza") is True
    assert nav.ir_a("plaza") is False
    assert nav.atras() == "inicio"      # no se queda en «plaza»


def test_pantallas_repetidas_no_consecutivas_se_conservan():
    """CA-30: extremo, A, B, A guarda las tres y «atrás» las devuelve al revés."""
    nav = Navegacion()
    for pantalla in ["A", "B", "A"]:
        nav.ir_a(pantalla)
    assert nav.atras() == "B"
    assert nav.atras() == "A"
    assert nav.atras() is None


def test_atras_con_historial_vacio_informa_y_no_falla():
    """CA-31: «atrás» sin historial devuelve None y deja la pantalla actual igual."""
    nav = Navegacion()
    nav.ir_a("inicio")
    assert nav.atras() is None
    assert nav.actual == "inicio"
    assert MENSAJE_SIN_PANTALLA_PREVIA == "No hay pantalla previa."


def test_atras_en_navegacion_recien_creada_no_falla():
    """CA-31: extremo, ni siquiera hay pantalla actual."""
    nav = Navegacion()
    assert nav.atras() is None
    assert nav.actual is None


def test_atras_hasta_agotar_el_historial_y_seguir_navegando():
    """CA-31: tras agotar el historial, un segundo «atrás» informa; luego se puede seguir."""
    nav = Navegacion()
    nav.ir_a("inicio")
    nav.ir_a("plaza")
    assert nav.atras() == "inicio"
    assert nav.atras() is None
    assert nav.atras() is None
    nav.ir_a("perfil")
    assert nav.atras() == "inicio"


def test_cada_sesion_tiene_su_propio_historial():
    """CA-30: dos navegaciones no comparten historial."""
    a, b = Navegacion(), Navegacion()
    a.ir_a("inicio")
    a.ir_a("plaza")
    b.ir_a("inicio")
    assert b.atras() is None
    assert a.atras() == "inicio"
