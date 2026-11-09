"""Pruebas de la cola y de las notificaciones (specs/03-cola).

Estilo de Semana10: funciones sueltas de pytest; cada docstring nombra el criterio CA
que verifica. CA-05 y CA-07 se prueban al final con `dominio/amistades.py`.
"""

import pytest

from dominio.amistades import Amistades, MENSAJE_SIN_SOLICITUDES, SolicitudInvalidaError
from dominio.notificaciones import MENSAJE_SIN_NOTIFICACIONES, Notificaciones
from dominio.usuarios import Catalogo
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


# ---------- CA-05: enviar solicitud (dominio/amistades.py) ----------

def _comunidad():
    """Catálogo con ana (0), luis (1), sara (2) y tomas (3), más sus amistades."""
    catalogo = Catalogo()
    for usuario in ("ana", "luis", "sara", "tomas"):
        catalogo.crear_perfil(usuario)
    return catalogo, Amistades(catalogo)


ANA, LUIS, SARA, TOMAS = 0, 1, 2, 3


def test_enviar_deja_la_solicitud_pendiente_en_la_cola_del_destinatario():
    """CA-05: la solicitud queda en la cola de quien la recibe, no en la de quien la envía."""
    _, amistades = _comunidad()
    destino = amistades.enviar(ANA, "luis")
    assert destino.usuario == "luis"
    assert amistades.pendientes(LUIS) == 1
    assert amistades.pendientes(ANA) == 0
    assert amistades.primera(LUIS).usuario == "ana"


def test_enviar_acepta_arroba_y_mayusculas():
    """CA-05: el destinatario se busca sin distinguir mayúsculas y con o sin arroba."""
    _, amistades = _comunidad()
    assert amistades.enviar(ANA, "@LUIS").usuario == "luis"


def test_enviar_no_crea_la_amistad():
    """CA-05: mientras esté pendiente no son amigos."""
    _, amistades = _comunidad()
    amistades.enviar(ANA, "luis")
    assert amistades.amigos(ANA) == []
    assert amistades.amigos(LUIS) == []


def test_enviar_avisa_al_destinatario():
    """CA-32 integrado: enviar genera un aviso para quien la recibe."""
    _, amistades = _comunidad()
    amistades.enviar(ANA, "luis")
    assert amistades.notificaciones.leer(LUIS) == ["@ana te envió una solicitud de amistad."]
    assert amistades.notificaciones.leer(ANA) == []


def test_enviar_a_uno_mismo_se_rechaza_sin_cambiar_la_cola():
    """CA-05: no se permite enviarla a uno mismo."""
    _, amistades = _comunidad()
    with pytest.raises(SolicitudInvalidaError, match="ti mismo"):
        amistades.enviar(ANA, "@Ana")
    assert amistades.pendientes(ANA) == 0
    assert amistades.notificaciones.pendientes(ANA) == 0


def test_enviar_a_un_amigo_se_rechaza():
    """CA-05: no se permite enviarla a quien ya es amigo."""
    _, amistades = _comunidad()
    amistades.enviar(ANA, "luis")
    amistades.atender(LUIS, aceptar=True)
    with pytest.raises(SolicitudInvalidaError, match="amigo"):
        amistades.enviar(ANA, "luis")
    with pytest.raises(SolicitudInvalidaError, match="amigo"):
        amistades.enviar(LUIS, "ana")
    assert amistades.pendientes(LUIS) == 0
    assert amistades.pendientes(ANA) == 0


def test_enviar_repetida_se_rechaza_y_la_cola_no_cambia():
    """CA-05: no se permite repetirla mientras esté pendiente."""
    _, amistades = _comunidad()
    amistades.enviar(ANA, "luis")
    with pytest.raises(SolicitudInvalidaError, match="Ya le enviaste"):
        amistades.enviar(ANA, "luis")
    assert amistades.pendientes(LUIS) == 1
    assert amistades.notificaciones.pendientes(LUIS) == 1


def test_solicitud_cruzada_se_rechaza_con_aviso():
    """CA-05: decisión de Valentina, si el otro ya te la envió, se te remite a tus solicitudes."""
    _, amistades = _comunidad()
    amistades.enviar(ANA, "luis")
    with pytest.raises(SolicitudInvalidaError, match="ya te envió"):
        amistades.enviar(LUIS, "ana")
    assert amistades.pendientes(ANA) == 0
    assert amistades.pendientes(LUIS) == 1


@pytest.mark.parametrize("texto", ["nadie", "", "   ", None])
def test_enviar_a_alguien_que_no_existe_se_rechaza(texto):
    """CA-05: el destinatario debe existir; nunca se encola nada."""
    _, amistades = _comunidad()
    with pytest.raises(SolicitudInvalidaError, match="no existe"):
        amistades.enviar(ANA, texto)
    assert amistades.pendientes(ANA) == 0


def test_remitente_inexistente_se_rechaza():
    """CA-05: extremo, quien envía también debe existir."""
    _, amistades = _comunidad()
    with pytest.raises(SolicitudInvalidaError, match="no existe"):
        amistades.enviar(99, "luis")
    assert amistades.pendientes(LUIS) == 0


def test_se_puede_volver_a_enviar_despues_de_un_rechazo():
    """CA-05: al rechazarla sale de la cola, así que ya no está repetida."""
    _, amistades = _comunidad()
    amistades.enviar(ANA, "luis")
    amistades.atender(LUIS, aceptar=False)
    amistades.enviar(ANA, "luis")
    assert amistades.pendientes(LUIS) == 1


def test_se_puede_volver_a_enviar_despues_de_deshacer_la_amistad():
    """CA-05: al deshacer ya no son amigos."""
    _, amistades = _comunidad()
    amistades.enviar(ANA, "luis")
    amistades.atender(LUIS, aceptar=True)
    amistades.deshacer(ANA, "luis")
    amistades.enviar(LUIS, "ana")
    assert amistades.pendientes(ANA) == 1


def test_persona_creada_despues_tambien_puede_recibir_solicitudes():
    """CA-05: un perfil creado después de arrancar funciona igual (RF-01 del grafo)."""
    catalogo, amistades = _comunidad()
    nueva = catalogo.crear_perfil("nueva")
    amistades.registrar(nueva.id)
    amistades.enviar(ANA, "nueva")
    amistades.atender(nueva.id, aceptar=True)
    assert [p.usuario for p in amistades.amigos(ANA)] == ["nueva"]


# ---------- CA-07: atender en orden de llegada ----------

def test_solicitudes_se_atienden_en_orden_de_llegada():
    """CA-07: X, Y, Z salen en ese orden."""
    _, amistades = _comunidad()
    for origen in (LUIS, SARA, TOMAS):
        amistades.enviar(origen, "ana")
    atendidas = [amistades.atender(ANA, aceptar=False).usuario for _ in range(3)]
    assert atendidas == ["luis", "sara", "tomas"]


def test_primera_muestra_solo_la_primera_sin_sacarla():
    """CA-07: revisar no cambia la cola."""
    _, amistades = _comunidad()
    amistades.enviar(LUIS, "ana")
    amistades.enviar(SARA, "ana")
    assert amistades.primera(ANA).usuario == "luis"
    assert amistades.primera(ANA).usuario == "luis"
    assert amistades.pendientes(ANA) == 2


def test_sin_solicitudes_informa_sin_error():
    """CA-07: sin pendientes no falla."""
    _, amistades = _comunidad()
    assert amistades.primera(ANA) is None
    assert amistades.atender(ANA, aceptar=True) is None
    assert amistades.pendientes(ANA) == 0
    assert MENSAJE_SIN_SOLICITUDES == "No tienes solicitudes pendientes."


def test_vaciar_y_volver_a_recibir_respeta_el_orden():
    """CA-07: la cola se puede vaciar y volver a usar."""
    _, amistades = _comunidad()
    amistades.enviar(LUIS, "ana")
    amistades.atender(ANA, aceptar=False)
    amistades.enviar(SARA, "ana")
    amistades.enviar(LUIS, "ana")
    assert amistades.primera(ANA).usuario == "sara"


def test_atender_la_ultima_deja_la_cola_lista():
    """CA-07: el último en salir deja la cola vacía (IR-01)."""
    _, amistades = _comunidad()
    amistades.enviar(LUIS, "ana")
    amistades.atender(ANA, aceptar=False)
    assert amistades.pendientes(ANA) == 0
    assert amistades.primera(ANA) is None


def test_dos_personas_tienen_colas_separadas():
    """CA-07: las solicitudes de una persona no se mezclan con las de otra."""
    _, amistades = _comunidad()
    amistades.enviar(LUIS, "ana")
    amistades.enviar(SARA, "tomas")
    assert amistades.primera(ANA).usuario == "luis"
    assert amistades.primera(TOMAS).usuario == "sara"


def test_persona_sin_id_valido_no_falla_al_consultar():
    """CA-07: extremo, consultar con un id que no existe informa vacío."""
    _, amistades = _comunidad()
    assert amistades.pendientes(99) == 0
    assert amistades.primera(99) is None
    assert amistades.atender(99, aceptar=True) is None
