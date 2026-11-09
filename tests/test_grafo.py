# Pruebas del grafo de amistades (escritas antes del código).
# Spec: specs/06-grafo/spec.md · CA-06, CA-08, CA-34, CA-36
# Decisiones de Valentina: agregar_amistad / eliminar_amistad devuelven True si
# cambiaron algo y False si se rechazan (sin tocar nada); candidatos_dos_saltos
# devuelve una lista de (id, comunes).

import pytest

from dominio.amistades import Amistades
from dominio.usuarios import Catalogo
from estructuras.grafo import Grafo


def _red(n, *amistades):
    """Grafo con n personas (ids 0..n-1) y las amistades dadas."""
    g = Grafo()
    for i in range(n):
        g.agregar_vertice(i)
    for a, b in amistades:
        assert g.agregar_amistad(a, b) is True
    return g


def _solo_ids(candidatos):
    return sorted(i for i, _ in candidatos)


# ---------- Base: agregar_vertice, amigos, grado (RF-01) ----------

def test_persona_nueva_no_tiene_amigos():
    g = _red(1)
    assert g.amigos(0) == []
    assert g.grado(0) == 0


def test_agregar_vertice_dos_veces_no_borra_amigos():
    g = _red(2, (0, 1))
    g.agregar_vertice(0)
    assert g.amigos(0) == [1]
    assert g.grado(0) == 1


def test_agregar_vertice_con_id_alto_deja_los_intermedios_validos():
    g = Grafo()
    g.agregar_vertice(5)
    assert g.amigos(3) == []
    assert g.grado(5) == 0


def test_cantidad_de_personas():
    g = _red(4)
    assert g.cantidad() == 4


def test_red_vacia_no_falla():
    g = Grafo()
    assert g.amigos(0) == []
    assert g.grado(0) == 0
    assert g.son_amigos(0, 1) is False
    assert g.candidatos_dos_saltos(0) == []
    assert g.agregar_amistad(0, 1) is False
    assert g.eliminar_amistad(0, 1) is False


@pytest.mark.parametrize("malo", [-1, "a", None, 1.5, True])
def test_id_invalido_se_trata_como_inexistente(malo):
    g = _red(2)
    assert g.amigos(malo) == []
    assert g.grado(malo) == 0
    assert g.agregar_amistad(0, malo) is False
    assert g.son_amigos(0, malo) is False
    assert g.candidatos_dos_saltos(malo) == []


@pytest.mark.parametrize("malo", [-1, "a", None, 1.5, True])
def test_agregar_vertice_con_id_invalido_lanza_value_error(malo):
    with pytest.raises(ValueError):
        Grafo().agregar_vertice(malo)


# ---------- CA-06: crear la amistad en ambos sentidos ----------

def test_amistad_queda_en_los_dos_sentidos():
    g = _red(2)
    assert g.agregar_amistad(0, 1) is True
    assert g.amigos(0) == [1]
    assert g.amigos(1) == [0]


def test_amistad_sube_el_grado_de_ambos():
    g = _red(3, (0, 1))
    assert g.grado(0) == 1 and g.grado(1) == 1 and g.grado(2) == 0


def test_la_amistad_mas_reciente_sale_primero():
    g = _red(4, (0, 1), (0, 2), (0, 3))
    assert g.amigos(0) == [3, 2, 1]


def test_son_amigos_da_lo_mismo_el_orden():
    g = _red(3, (0, 1))
    assert g.son_amigos(0, 1) is True
    assert g.son_amigos(1, 0) is True
    assert g.son_amigos(0, 2) is False


def test_amistad_consigo_mismo_se_rechaza():
    g = _red(2)
    assert g.agregar_amistad(0, 0) is False
    assert g.amigos(0) == [] and g.grado(0) == 0


def test_amistad_repetida_se_rechaza_y_conserva_una_entrada():
    g = _red(2, (0, 1))
    assert g.agregar_amistad(0, 1) is False
    assert g.amigos(0) == [1] and g.grado(0) == 1


def test_amistad_repetida_nombrando_al_reves_se_rechaza():
    g = _red(2, (0, 1))
    assert g.agregar_amistad(1, 0) is False
    assert g.amigos(0) == [1] and g.amigos(1) == [0]
    assert g.grado(0) == 1 and g.grado(1) == 1


def test_amistad_con_persona_inexistente_no_cambia_nada():
    g = _red(2, (0, 1))
    assert g.agregar_amistad(0, 9) is False
    assert g.agregar_amistad(9, 0) is False
    assert g.amigos(0) == [1] and g.amigos(1) == [0]
    assert g.grado(0) == 1


def test_el_invariante_a_en_lista_de_b_si_y_solo_si_b_en_lista_de_a():
    g = _red(6, (0, 1), (0, 2), (1, 2), (3, 4), (4, 5), (0, 5))
    for a in range(6):
        for b in range(6):
            assert (b in g.amigos(a)) == (a in g.amigos(b))
        assert a not in g.amigos(a)
        assert g.grado(a) == len(g.amigos(a))


def test_persona_con_cien_amigos():
    g = _red(101)
    for i in range(1, 101):
        assert g.agregar_amistad(0, i) is True
    assert g.grado(0) == 100
    assert g.amigos(0)[0] == 100 and g.amigos(0)[-1] == 1
    assert g.son_amigos(0, 50) is True
    assert g.agregar_amistad(0, 50) is False


# ---------- CA-08: deshacer la amistad ----------

def test_deshacer_elimina_en_ambos_sentidos():
    g = _red(2, (0, 1))
    assert g.eliminar_amistad(0, 1) is True
    assert g.amigos(0) == [] and g.amigos(1) == []
    assert g.grado(0) == 0 and g.grado(1) == 0
    assert g.son_amigos(0, 1) is False


def test_deshacer_nombrando_al_reves_tambien_funciona():
    g = _red(2, (0, 1))
    assert g.eliminar_amistad(1, 0) is True
    assert g.amigos(0) == []


def test_deshacer_la_primera_de_la_lista():
    g = _red(4, (0, 1), (0, 2), (0, 3))      # amigos(0) = [3, 2, 1]
    assert g.eliminar_amistad(0, 3) is True
    assert g.amigos(0) == [2, 1]
    assert g.amigos(3) == []


def test_deshacer_una_intermedia():
    g = _red(4, (0, 1), (0, 2), (0, 3))
    assert g.eliminar_amistad(0, 2) is True
    assert g.amigos(0) == [3, 1]
    assert g.grado(0) == 2


def test_deshacer_la_ultima_de_la_lista():
    g = _red(4, (0, 1), (0, 2), (0, 3))
    assert g.eliminar_amistad(0, 1) is True
    assert g.amigos(0) == [3, 2]
    # y todavía se puede agregar al final de la cadena sin romperla
    assert g.agregar_amistad(0, 1) is True
    assert g.amigos(0) == [1, 3, 2]


def test_deshacer_la_unica_amistad_deja_lista_vacia():
    g = _red(3, (0, 1), (1, 2))
    assert g.eliminar_amistad(1, 0) is True
    assert g.amigos(1) == [2]
    assert g.amigos(0) == []


def test_deshacer_las_demas_amistades_quedan_intactas():
    g = _red(5, (0, 1), (0, 2), (1, 2), (3, 4))
    g.eliminar_amistad(0, 1)
    assert g.amigos(2) == [1, 0]
    assert g.amigos(3) == [4] and g.amigos(4) == [3]
    assert g.son_amigos(1, 2) is True


def test_deshacer_una_inexistente_informa_y_no_cambia():
    g = _red(3, (0, 1))
    assert g.eliminar_amistad(0, 2) is False
    assert g.amigos(0) == [1] and g.grado(0) == 1 and g.grado(2) == 0


def test_deshacer_dos_veces_seguidas():
    g = _red(2, (0, 1))
    assert g.eliminar_amistad(0, 1) is True
    assert g.eliminar_amistad(0, 1) is False
    assert g.grado(0) == 0


def test_deshacer_con_persona_inexistente():
    g = _red(2, (0, 1))
    assert g.eliminar_amistad(0, 9) is False
    assert g.eliminar_amistad(9, 0) is False
    assert g.eliminar_amistad(0, 0) is False
    assert g.amigos(0) == [1]


def test_deshacer_y_volver_a_crear():
    g = _red(2, (0, 1))
    g.eliminar_amistad(0, 1)
    assert g.agregar_amistad(0, 1) is True
    assert g.amigos(0) == [1] and g.amigos(1) == [0]


def test_invariante_tras_varias_altas_y_bajas():
    g = _red(6, (0, 1), (0, 2), (0, 3), (4, 5), (1, 5))
    g.eliminar_amistad(0, 2)
    g.eliminar_amistad(4, 5)
    g.agregar_amistad(2, 5)
    for a in range(6):
        for b in range(6):
            assert (b in g.amigos(a)) == (a in g.amigos(b))
        assert g.grado(a) == len(g.amigos(a))


# ---------- CA-34: candidatos a dos saltos ----------

def test_amigos_de_amigos_sin_repetir():
    # 0 - 1 - 2   y   0 - 3 - 4
    g = _red(5, (0, 1), (1, 2), (0, 3), (3, 4))
    assert sorted(g.candidatos_dos_saltos(0)) == [(2, 1), (4, 1)]


def test_excluye_a_la_persona_y_a_sus_amigos_triangulo():
    g = _red(3, (0, 1), (0, 2), (1, 2))      # A-B, A-C, B-C
    assert g.candidatos_dos_saltos(0) == []


def test_no_se_recomienda_a_si_mismo():
    g = _red(3, (0, 1), (1, 2))              # 2 ve a 0 como candidato; 0 ve a 2
    assert 0 not in _solo_ids(g.candidatos_dos_saltos(0))
    assert _solo_ids(g.candidatos_dos_saltos(0)) == [2]


def test_tres_amigos_en_comun_aparece_una_vez_con_tres():
    # 0 es amigo de 1, 2 y 3; los tres son amigos de 4
    g = _red(5, (0, 1), (0, 2), (0, 3), (1, 4), (2, 4), (3, 4))
    assert g.candidatos_dos_saltos(0) == [(4, 3)]


def test_amigos_en_comun_distintos_por_candidato():
    g = _red(6, (0, 1), (0, 2), (1, 3), (2, 3), (2, 4))
    assert sorted(g.candidatos_dos_saltos(0)) == [(3, 2), (4, 1)]


def test_no_cuenta_a_amigos_de_amigos_de_amigos():
    g = _red(4, (0, 1), (1, 2), (2, 3))      # 3 está a tres saltos
    assert _solo_ids(g.candidatos_dos_saltos(0)) == [2]


def test_persona_inexistente_devuelve_vacio():
    g = _red(3, (0, 1))
    assert g.candidatos_dos_saltos(9) == []


def test_solicitud_pendiente_no_cuenta_como_amistad():
    # El grafo solo conoce amistades: 0 y 2 no son amigos aunque haya solicitud.
    g = _red(3, (0, 1), (1, 2))
    assert 2 in _solo_ids(g.candidatos_dos_saltos(0))


def test_la_consulta_no_modifica_la_red():
    g = _red(5, (0, 1), (1, 2), (1, 3), (3, 4))
    antes = [g.amigos(i) for i in range(5)]
    g.candidatos_dos_saltos(0)
    g.candidatos_dos_saltos(0)
    assert [g.amigos(i) for i in range(5)] == antes


def test_consultas_seguidas_dan_lo_mismo():
    g = _red(5, (0, 1), (1, 2), (0, 3), (3, 2))
    assert g.candidatos_dos_saltos(0) == g.candidatos_dos_saltos(0) == [(2, 2)]


def test_candidatos_en_red_grande_encadenada():
    g = _red(200)
    for i in range(199):
        g.agregar_amistad(i, i + 1)
    assert sorted(g.candidatos_dos_saltos(100)) == [(98, 1), (102, 1)]


# ---------- CA-36: persona sin amigos ----------

def test_sin_amigos_candidatos_vacio():
    g = _red(3, (1, 2))
    assert g.candidatos_dos_saltos(0) == []


def test_amigos_que_no_tienen_otros_amigos_candidatos_vacio():
    g = _red(4, (0, 1), (0, 2), (0, 3))
    assert g.candidatos_dos_saltos(0) == []


def test_red_de_una_sola_persona():
    g = _red(1)
    assert g.candidatos_dos_saltos(0) == []
    assert g.amigos(0) == []


def test_candidatos_tras_deshacer_todas_las_amistades():
    g = _red(3, (0, 1), (1, 2))
    g.eliminar_amistad(0, 1)
    assert g.candidatos_dos_saltos(0) == []


# ---------- CA-06 integrado: de la cola al grafo (dominio/amistades.py) ----------

def _comunidad():
    catalogo = Catalogo()
    for usuario in ("ana", "luis", "sara"):
        catalogo.crear_perfil(usuario)
    return Amistades(catalogo)


def _usuarios(perfiles):
    return [p.usuario for p in perfiles]


def test_aceptar_crea_la_amistad_en_ambos_sentidos():
    """CA-06: aceptar la solicitud deja a cada uno entre los amigos del otro."""
    amistades = _comunidad()
    amistades.enviar(0, "luis")
    remitente = amistades.atender(1, aceptar=True)
    assert remitente.usuario == "ana"
    assert _usuarios(amistades.amigos(0)) == ["luis"]
    assert _usuarios(amistades.amigos(1)) == ["ana"]
    assert amistades.pendientes(1) == 0


def test_rechazar_descarta_la_solicitud_sin_crear_amistad():
    """CA-06: rechazar la saca de la cola y la red queda igual."""
    amistades = _comunidad()
    amistades.enviar(0, "luis")
    assert amistades.atender(1, aceptar=False).usuario == "ana"
    assert amistades.amigos(0) == [] and amistades.amigos(1) == []
    assert amistades.pendientes(1) == 0


def test_aceptar_avisa_a_quien_envio_la_solicitud():
    """CA-06 y CA-32: aceptar genera el aviso para quien la envió."""
    amistades = _comunidad()
    amistades.enviar(0, "luis")
    amistades.atender(1, aceptar=True)
    assert amistades.notificaciones.leer(0) == ["@luis aceptó tu solicitud de amistad."]


def test_rechazar_no_genera_aviso():
    """CA-06: quien la envió no recibe aviso si se la rechazan."""
    amistades = _comunidad()
    amistades.enviar(0, "luis")
    amistades.atender(1, aceptar=False)
    assert amistades.notificaciones.leer(0) == []


def test_amigos_salen_del_mas_reciente_al_mas_antiguo():
    """CA-06: `amigos` entrega perfiles en el orden del grafo."""
    amistades = _comunidad()
    amistades.enviar(1, "ana")
    amistades.atender(0, aceptar=True)
    amistades.enviar(2, "ana")
    amistades.atender(0, aceptar=True)
    assert _usuarios(amistades.amigos(0)) == ["sara", "luis"]


def test_deshacer_desde_el_dominio_en_ambos_sentidos():
    """CA-08: deshacer por @usuario quita la amistad a los dos."""
    amistades = _comunidad()
    amistades.enviar(0, "luis")
    amistades.atender(1, aceptar=True)
    assert amistades.deshacer(1, "@ANA") is True
    assert amistades.amigos(0) == [] and amistades.amigos(1) == []


@pytest.mark.parametrize("otro", ["sara", "nadie", "", None])
def test_deshacer_inexistente_no_produce_error(otro):
    """CA-08: una amistad que no existe, o un @usuario que no existe, da False."""
    amistades = _comunidad()
    assert amistades.deshacer(0, otro) is False
