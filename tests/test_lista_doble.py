"""Pruebas de la lista doble, la plaza y la búsqueda por palabra (specs/01-lista-doble).

Estilo de Semana6/Semana10: funciones sueltas de pytest; cada docstring nombra el criterio
CA que verifica (CA-12, CA-13 o CA-29).
"""

from dominio.busqueda import buscar_palabra
from dominio.feed import (
    MENSAJE_FIN_PLAZA,
    MENSAJE_INICIO_PLAZA,
    MENSAJE_PLAZA_VACIA,
    Plaza,
)
from estructuras.lista_doble import ListaDoble


def _lista_con(n):
    """Lista con 0..n-1 insertados al frente: queda n-1 primero y 0 último."""
    lista = ListaDoble()
    for i in range(n):
        lista.insertar_al_frente(i)
    return lista


def _plaza_con(n):
    """Plaza con n publicaciones 'p0'..'p{n-1}'; la última publicada queda primera."""
    plaza = Plaza()
    for i in range(n):
        plaza.publicar("@ana", f"p{i}", f"cuerpo {i}", "2026-11-08")
    return plaza


def _titulos(pagina):
    return [p.titulo for p in pagina]


# ---------- estructura: insertar_al_frente ----------
def test_insertar_al_frente_deja_la_nueva_como_primera():
    """CA-12: tras insertar al frente, inicio() apunta al último dato insertado."""
    lista = ListaDoble()
    lista.insertar_al_frente("a")
    lista.insertar_al_frente("b")
    assert lista.inicio().dato == "b"


def test_insertar_al_frente_en_vacia_fija_cabeza_y_cola():
    """CA-12: extremo, el primer elemento es cabeza y cola a la vez."""
    lista = ListaDoble()
    lista.insertar_al_frente("unico")
    assert lista._cabeza is lista._cola
    assert lista.tamano() == 1


def test_insertar_al_frente_dos_seguidas_ultima_primero():
    """CA-12: extremo, dos publicaciones seguidas; la última queda primera y la anterior segunda."""
    lista = ListaDoble()
    lista.insertar_al_frente("vieja")
    lista.insertar_al_frente("nueva")
    assert list(lista) == ["nueva", "vieja"]


def test_enlaces_anterior_y_siguiente_son_coherentes_en_ambos_sentidos():
    """CA-12: recorrer hacia adelante y hacia atrás da los mismos datos al revés."""
    lista = _lista_con(10)
    adelante, nodo = [], lista._cabeza
    while nodo is not None:
        adelante.append(nodo.dato)
        nodo = nodo.siguiente
    atras, nodo = [], lista._cola
    while nodo is not None:
        atras.append(nodo.dato)
        nodo = nodo.anterior
    assert adelante == list(reversed(atras))
    assert lista._cabeza.anterior is None
    assert lista._cola.siguiente is None


def test_tamano_len_y_tamaño_coinciden():
    """CA-12: tamano(), tamaño() y len() devuelven lo mismo."""
    lista = _lista_con(4)
    assert lista.tamano() == lista.tamaño() == len(lista) == 4


def test_estres_muchas_inserciones_mantienen_el_orden():
    """CA-12: estrés, 1000 inserciones al frente quedan en orden inverso."""
    lista = _lista_con(1000)
    assert list(lista) == list(range(999, -1, -1))


# ---------- estructura: inicio, esta_vacia ----------
def test_inicio_y_esta_vacia_en_lista_vacia():
    """CA-13: extremo, con la plaza vacía no hay inicio y esta_vacia es True."""
    lista = ListaDoble()
    assert lista.esta_vacia()
    assert lista.inicio() is None
    assert lista.pagina(lista.inicio()) == []


def test_esta_vacia_es_falsa_con_elementos():
    """CA-13: con al menos un elemento, esta_vacia es False."""
    assert not _lista_con(1).esta_vacia()


# ---------- estructura: pagina, avanzar, retroceder ----------
def test_pagina_trae_cinco_y_la_ultima_puede_traer_menos():
    """CA-13: las páginas son de 5; la última trae el resto."""
    lista = _lista_con(12)
    marcador = lista.inicio()
    assert lista.pagina(marcador) == [11, 10, 9, 8, 7]
    marcador, _ = lista.avanzar(marcador)
    marcador, _ = lista.avanzar(marcador)
    assert lista.pagina(marcador) == [1, 0]


def test_avanzar_recorre_las_paginas_y_luego_informa_el_limite():
    """CA-13: avanzar mueve 5 hacia las más antiguas; en la última página no se mueve."""
    lista = _lista_con(12)
    m0 = lista.inicio()
    m1, se_movio1 = lista.avanzar(m0)
    m2, se_movio2 = lista.avanzar(m1)
    m3, se_movio3 = lista.avanzar(m2)
    assert (se_movio1, se_movio2, se_movio3) == (True, True, False)
    assert m3 is m2                      # la posición no cambia en el extremo


def test_avanzar_con_exactamente_cinco_es_una_sola_pagina():
    """CA-13: extremo, con 5 publicaciones avanzar informa el final y no se mueve."""
    lista = _lista_con(5)
    marcador = lista.inicio()
    nuevo, se_movio = lista.avanzar(marcador)
    assert not se_movio
    assert nuevo is marcador


def test_avanzar_con_seis_la_segunda_pagina_trae_una():
    """CA-13: extremo, con 6 publicaciones la segunda página trae 1."""
    lista = _lista_con(6)
    marcador, se_movio = lista.avanzar(lista.inicio())
    assert se_movio
    assert lista.pagina(marcador) == [0]


def test_avanzar_con_un_solo_elemento_y_con_lista_vacia_no_falla():
    """CA-13: extremo, uno y cero elementos informan límite sin fallar."""
    assert _lista_con(1).avanzar(_lista_con(1).inicio())[1] is False
    assert ListaDoble().avanzar(None) == (None, False)


def test_retroceder_vuelve_a_la_pagina_anterior():
    """CA-13: ida y vuelta, retroceder deshace un avanzar."""
    lista = _lista_con(12)
    m0 = lista.inicio()
    m1, _ = lista.avanzar(m0)
    atras, se_movio = lista.retroceder(m1)
    assert se_movio
    assert atras is m0


def test_retroceder_en_el_inicio_no_se_mueve():
    """CA-13: en el primer extremo la posición no cambia y se informa."""
    lista = _lista_con(12)
    m0 = lista.inicio()
    nuevo, se_movio = lista.retroceder(m0)
    assert not se_movio
    assert nuevo is m0


def test_retroceder_con_menos_de_cinco_para_el_inicio_llega_al_inicio():
    """CA-13: decisión de Valentina, posición desalineada: retrocede hasta el inicio."""
    lista = _lista_con(12)
    marcador = lista.inicio()
    for _ in range(3):                   # avanza 3 nodos a mano: queda desalineada
        marcador = marcador.siguiente
    nuevo, se_movio = lista.retroceder(marcador)
    assert se_movio
    assert nuevo is lista.inicio()


def test_retroceder_con_lista_vacia_y_con_un_elemento_no_falla():
    """CA-13: extremo, cero y un elemento informan límite sin fallar."""
    assert ListaDoble().retroceder(None) == (None, False)
    uno = _lista_con(1)
    assert uno.retroceder(uno.inicio())[1] is False


# ---------- dominio: publicar (CA-12) ----------
def test_publicar_deja_la_publicacion_como_primera_de_la_plaza():
    """CA-12: una publicación nueva aparece como la primera de la plaza."""
    plaza = _plaza_con(3)
    plaza.publicar("@luis", "nueva", "cuerpo", "2026-11-08")
    pagina, _ = plaza.sesion().ver()
    assert pagina[0].titulo == "nueva"


def test_publicar_asigna_ids_distintos_y_crece_el_tamano():
    """CA-12: cada publicación recibe su identificador y suma uno al tamaño."""
    plaza = Plaza()
    a = plaza.publicar("@ana", "a", "x", "2026-11-08")
    b = plaza.publicar("@ana", "b", "y", "2026-11-08")
    assert a.id != b.id
    assert plaza.tamano() == 2


def test_publicar_en_plaza_vacia_la_hace_visible():
    """CA-12: extremo, la primera publicación de una plaza vacía se ve en la página."""
    plaza = Plaza()
    plaza.publicar("@ana", "primera", "x", "2026-11-08")
    pagina, aviso = plaza.sesion().ver()
    assert _titulos(pagina) == ["primera"]
    assert aviso is None


# ---------- dominio: paginar con sesión (CA-13) ----------
def test_sesion_pagina_hacia_adelante_y_atras():
    """CA-13: se puede paginar hacia adelante y atrás."""
    sesion = _plaza_con(12).sesion()
    p1, _ = sesion.ver()
    p2, _ = sesion.siguiente()
    atras, _ = sesion.anterior()
    assert _titulos(p1) == ["p11", "p10", "p9", "p8", "p7"]
    assert _titulos(p2) == ["p6", "p5", "p4", "p3", "p2"]
    assert _titulos(atras) == _titulos(p1)


def test_sesion_informa_el_limite_al_final_y_conserva_la_posicion():
    """CA-13: en el último extremo la posición no cambia y se informa el límite."""
    sesion = _plaza_con(7).sesion()
    sesion.siguiente()
    pagina, aviso = sesion.siguiente()
    assert aviso == MENSAJE_FIN_PLAZA
    assert _titulos(pagina) == ["p1", "p0"]


def test_sesion_informa_el_limite_al_principio_y_conserva_la_posicion():
    """CA-13: en el primer extremo la posición no cambia y se informa el límite."""
    sesion = _plaza_con(7).sesion()
    pagina, aviso = sesion.anterior()
    assert aviso == MENSAJE_INICIO_PLAZA
    assert _titulos(pagina) == ["p6", "p5", "p4", "p3", "p2"]


def test_sesion_con_plaza_vacia_no_falla():
    """CA-13: con la plaza vacía, ver, avanzar, retroceder e inicio avisan sin fallar."""
    sesion = Plaza().sesion()
    for operacion in (sesion.ver, sesion.siguiente, sesion.anterior, sesion.inicio):
        assert operacion() == ([], MENSAJE_PLAZA_VACIA)


def test_sesion_creada_con_plaza_vacia_funciona_al_publicar_despues():
    """CA-13: extremo, una sesión abierta antes de la primera publicación la ve después."""
    plaza = Plaza()
    sesion = plaza.sesion()
    plaza.publicar("@ana", "tarde", "x", "2026-11-08")
    pagina, _ = sesion.ver()
    assert _titulos(pagina) == ["tarde"]


def test_dos_sesiones_en_distintas_paginas_son_independientes():
    """CA-13: avanzar en una sesión no mueve a la otra."""
    plaza = _plaza_con(12)
    a, b = plaza.sesion(), plaza.sesion()
    a.siguiente()
    pagina_b, _ = b.ver()
    assert _titulos(pagina_b)[0] == "p11"


def test_publicar_mientras_otra_sesion_esta_en_la_pagina_2_no_la_mueve():
    """CA-13: la sesión sigue viendo la misma publicación aunque llegue una nueva."""
    plaza = _plaza_con(12)
    sesion = plaza.sesion()
    antes, _ = sesion.siguiente()
    plaza.publicar("@luis", "nueva", "x", "2026-11-08")
    despues, _ = sesion.ver()
    assert _titulos(despues) == _titulos(antes)


def test_inicio_vuelve_a_la_publicacion_mas_nueva():
    """CA-13: volver al inicio coloca la sesión en la publicación más nueva."""
    plaza = _plaza_con(12)
    sesion = plaza.sesion()
    sesion.siguiente()
    plaza.publicar("@luis", "nueva", "x", "2026-11-08")
    pagina, _ = sesion.inicio()
    assert pagina[0].titulo == "nueva"


# ---------- dominio: buscar por palabra (CA-29) ----------
def _plaza_para_buscar():
    plaza = Plaza()
    plaza.publicar("@ana", "Aprendiendo Python", "listas y pilas", "2026-11-01")
    plaza.publicar("@luis", "Una duda", "¿Alguien usa pythonista?", "2026-11-02")
    plaza.publicar("@eva", "Grafos", "BFS y DFS", "2026-11-03")
    return plaza


def test_buscar_encuentra_en_el_titulo():
    """CA-29: devuelve las publicaciones que contienen la palabra en el título."""
    assert [p.titulo for p in buscar_palabra(_plaza_para_buscar(), "grafos")] == ["Grafos"]


def test_buscar_encuentra_en_el_cuerpo():
    """CA-29: devuelve las que la contienen solo en el cuerpo."""
    assert [p.titulo for p in buscar_palabra(_plaza_para_buscar(), "pilas")] == ["Aprendiendo Python"]


def test_buscar_ignora_mayusculas_y_acepta_subcadenas():
    """CA-29: «python» encuentra «Python» y «pythonista», la más nueva primero."""
    titulos = [p.titulo for p in buscar_palabra(_plaza_para_buscar(), "PYTHON")]
    assert titulos == ["Una duda", "Aprendiendo Python"]


def test_buscar_sin_coincidencias_devuelve_vacio():
    """CA-29: extremo, sin coincidencias el resultado es vacío y no falla."""
    assert buscar_palabra(_plaza_para_buscar(), "java") == []


def test_buscar_en_plaza_vacia_devuelve_vacio():
    """CA-29: extremo, con la plaza vacía no falla."""
    assert buscar_palabra(Plaza(), "algo") == []


def test_buscar_palabra_vacia_o_solo_espacios_no_devuelve_toda_la_plaza():
    """CA-29: extremo, palabra vacía o de espacios da resultado vacío."""
    plaza = _plaza_para_buscar()
    assert buscar_palabra(plaza, "") == []
    assert buscar_palabra(plaza, "   ") == []


def test_buscar_con_titulos_repetidos_devuelve_ambos_la_mas_nueva_primero():
    """CA-29: extremo, dos publicaciones con el mismo título aparecen las dos."""
    plaza = Plaza()
    primera = plaza.publicar("@ana", "Duda", "uno", "2026-11-01")
    segunda = plaza.publicar("@luis", "Duda", "dos", "2026-11-02")
    assert [p.id for p in buscar_palabra(plaza, "duda")] == [segunda.id, primera.id]


def test_buscar_no_modifica_la_plaza():
    """CA-29: buscar no cambia el tamaño ni el orden."""
    plaza = _plaza_para_buscar()
    antes = [p.titulo for p in plaza]
    buscar_palabra(plaza, "python")
    assert [p.titulo for p in plaza] == antes
    assert plaza.tamano() == 3
