"""Pruebas del AVL y de los usuarios (specs/05-avl): CA-01 a CA-04, CA-27 y CA-28.

Estilo de Semana6/Semana10: funciones sueltas de pytest; cada docstring nombra el criterio
CA que verifica. Los criterios de votos, insignias y fecha (CA-17 a CA-21, CA-39) son Should
y se prueban cuando se implementen.
"""

import math
import re

import pytest

from dominio.usuarios import (
    CANTIDAD_INICIAL,
    SEMILLA,
    Catalogo,
    UsuarioInvalidoError,
    generar_comunidad,
)
from estructuras.avl import AVL


def _arbol_con(*claves):
    arbol = AVL()
    for clave in claves:
        arbol.insertar(clave, clave.upper())
    return arbol


def _verificar_avl(arbol):
    """Comprueba orden de búsqueda, alturas guardadas y equilibrio en todos los nodos."""

    def revisar(nodo, minimo, maximo):
        if nodo is None:
            return -1
        if minimo is not None:
            assert nodo.clave > minimo
        if maximo is not None:
            assert nodo.clave < maximo
        h_izq = revisar(nodo.izquierdo, minimo, nodo.clave)
        h_der = revisar(nodo.derecho, nodo.clave, maximo)
        assert abs(h_izq - h_der) <= 1
        assert nodo.altura == 1 + max(h_izq, h_der)
        return nodo.altura

    revisar(arbol._raiz, None, None)


def _limite_altura(n):
    return 1.44 * math.log2(n + 2)


# ---------- AVL: insertar y rotaciones ----------
@pytest.mark.parametrize(
    "claves, raiz",
    [
        (["c", "b", "a"], "b"),   # izquierda-izquierda: rotación simple a la derecha
        (["a", "b", "c"], "b"),   # derecha-derecha: rotación simple a la izquierda
        (["c", "a", "b"], "b"),   # izquierda-derecha: rotación doble
        (["a", "c", "b"], "b"),   # derecha-izquierda: rotación doble
    ],
)
def test_las_cuatro_rotaciones_dejan_la_clave_del_medio_como_raiz(claves, raiz):
    """CA-01: tres claves en cualquier orden quedan con altura 1 y la del medio arriba."""
    arbol = _arbol_con(*claves)
    assert arbol._raiz.clave == raiz
    assert arbol.altura() == 1
    assert arbol.recorrer_en_orden() == ["a", "b", "c"]
    _verificar_avl(arbol)


def test_rotacion_doble_con_subarboles_no_pierde_ninguna_clave():
    """CA-01: con subárboles colgando, la rotación conserva todas las claves y el orden."""
    arbol = _arbol_con("e", "b", "g", "a", "c", "d")
    assert arbol.recorrer_en_orden() == ["a", "b", "c", "d", "e", "g"]
    assert arbol.tamano() == 6
    _verificar_avl(arbol)


def test_siete_claves_ascendentes_dejan_un_arbol_perfecto():
    """CA-01: 1..7 ya ordenadas quedan con raíz 4 y altura 2, rotando en varios niveles."""
    arbol = _arbol_con(*"1234567")
    assert arbol._raiz.clave == "4"
    assert arbol.altura() == 2
    _verificar_avl(arbol)


@pytest.mark.parametrize("orden", ["ascendente", "descendente"])
def test_cien_claves_ordenadas_mantienen_la_altura_logaritmica(orden):
    """CA-01: 100 claves ya ordenadas (el peor caso del BST) quedan con altura <= 1.44*log2(n+2)."""
    claves = [f"u{i:03d}" for i in range(100)]
    if orden == "descendente":
        claves.reverse()
    arbol = _arbol_con(*claves)
    assert arbol.altura() <= _limite_altura(100)
    assert arbol.tamano() == 100
    _verificar_avl(arbol)


def test_estres_mil_claves_siguen_siendo_un_avl():
    """CA-01: estrés, 1000 inserciones mantienen equilibrio, orden y altura logarítmica."""
    arbol = _arbol_con(*[f"k{i:04d}" for i in range(1000)])
    assert arbol.altura() <= _limite_altura(1000)
    assert arbol.recorrer_en_orden() == sorted(arbol.recorrer_en_orden())
    _verificar_avl(arbol)


def test_insertar_devuelve_true_y_deja_la_clave_encontrable():
    """CA-03: insertar una clave nueva devuelve True y ya se puede buscar."""
    arbol = AVL()
    assert arbol.insertar("ana", 1) is True
    assert arbol.buscar("ana") == 1


def test_insertar_clave_repetida_devuelve_false_y_no_cambia_nada():
    """CA-04: decisión de Valentina, un duplicado devuelve False, no cambia el valor ni el tamaño."""
    arbol = AVL()
    arbol.insertar("ana", 1)
    assert arbol.insertar("ana", 2) is False
    assert arbol.buscar("ana") == 1
    assert arbol.tamano() == 1


def test_insertar_en_vacio_y_un_solo_nodo():
    """CA-01: extremo, la primera clave es la raíz con altura 0."""
    arbol = AVL()
    arbol.insertar("solo", 0)
    assert arbol._raiz.clave == "solo"
    assert arbol.altura() == 0


# ---------- AVL: buscar ----------
def test_buscar_encuentra_cada_clave_insertada():
    """CA-03: buscar devuelve el valor de cada clave presente."""
    arbol = AVL()
    for i, clave in enumerate(["m", "c", "t", "a", "e", "p", "z"]):
        arbol.insertar(clave, i)
    assert [arbol.buscar(c) for c in ["m", "c", "t", "a", "e", "p", "z"]] == list(range(7))


def test_buscar_ausente_devuelve_none():
    """CA-03: decisión de Valentina, una clave ausente devuelve None."""
    arbol = _arbol_con("a", "c")
    assert arbol.buscar("b") is None
    assert arbol.buscar("zzz") is None


def test_buscar_en_arbol_vacio_devuelve_none():
    """CA-03: extremo, buscar en un árbol vacío no falla."""
    assert AVL().buscar("x") is None


def test_buscar_distingue_entre_prefijo_y_clave_completa():
    """CA-04: «ana» existe pero «an» y «ana_07» no si no se insertaron."""
    arbol = _arbol_con("ana")
    assert arbol.buscar("ana") == "ANA"
    assert arbol.buscar("an") is None
    assert arbol.buscar("ana_07") is None


# ---------- AVL: recorrer_en_orden, altura y tamaño ----------
def test_recorrer_en_orden_devuelve_las_claves_ordenadas():
    """CA-27: el recorrido en orden da las claves de menor a mayor."""
    arbol = _arbol_con("m", "c", "t", "a", "e")
    assert arbol.recorrer_en_orden() == ["a", "c", "e", "m", "t"]


def test_recorrer_en_orden_en_vacio_y_con_un_elemento():
    """CA-27: extremo, vacío da [] y un elemento da [clave]."""
    assert AVL().recorrer_en_orden() == []
    assert _arbol_con("x").recorrer_en_orden() == ["x"]


def test_recorrer_en_orden_no_repite_claves_duplicadas():
    """CA-27: insertar la misma clave dos veces no la duplica en el recorrido."""
    arbol = _arbol_con("b", "a")
    arbol.insertar("a", "otra")
    assert arbol.recorrer_en_orden() == ["a", "b"]


def test_altura_vacio_hoja_y_tres_claves():
    """CA-01: convención de Semana10: vacío = -1, un nodo = 0, tres claves = 1."""
    assert AVL().altura() == -1
    assert _arbol_con("a").altura() == 0
    assert _arbol_con("a", "b", "c").altura() == 1


def test_tamano_crece_y_no_cuenta_duplicados():
    """CA-01: el tamaño suma por cada clave nueva y no por las repetidas."""
    arbol = AVL()
    assert arbol.tamano() == 0
    arbol.insertar("a", 1)
    arbol.insertar("b", 2)
    arbol.insertar("a", 3)
    assert arbol.tamano() == 2


def test_tamano_len_y_tamaño_coinciden():
    """CA-01: tamano(), tamaño() y len() devuelven lo mismo."""
    arbol = _arbol_con("a", "b", "c")
    assert arbol.tamano() == arbol.tamaño() == len(arbol) == 3


# ---------- AVL: buscar_por_prefijo (CA-27, CA-28) ----------
def _arbol_de_nombres():
    arbol = AVL()
    for i, clave in enumerate(["ana", "andres", "ana_07", "beatriz", "camila", "carlos"]):
        arbol.insertar(clave, i)
    return arbol


def test_prefijo_devuelve_las_coincidencias_en_orden_alfabetico():
    """CA-27: el prefijo «an» devuelve ana, ana_07 y andres, en ese orden."""
    arbol = _arbol_de_nombres()
    assert arbol.buscar_por_prefijo("an") == [0, 2, 1]     # valores de ana, ana_07, andres


def test_prefijo_igual_a_una_clave_la_incluye_primero():
    """CA-27: «ana» devuelve ana (la más corta) y ana_07."""
    arbol = _arbol_de_nombres()
    assert arbol.buscar_por_prefijo("ana") == [0, 2]


def test_prefijo_de_una_letra_y_con_un_solo_elemento():
    """CA-27: extremo, una letra trae a todos los que empiezan así; con un solo nodo lo encuentra."""
    assert _arbol_de_nombres().buscar_por_prefijo("c") == [4, 5]
    assert _arbol_con("ana").buscar_por_prefijo("a") == ["ANA"]


def test_prefijo_sobre_muchas_claves_coincide_con_filtrar_a_mano():
    """CA-27: 120 claves ordenadas, el resultado coincide con filtrar la lista a mano."""
    claves = [f"{n}_{i:02d}" for n in ("luis", "mara", "mario") for i in range(1, 41)]
    arbol = AVL()
    for clave in claves:
        arbol.insertar(clave, clave)
    esperado = sorted(c for c in claves if c.startswith("mar"))
    assert arbol.buscar_por_prefijo("mar") == esperado
    assert len(esperado) == 80


def test_prefijo_sin_coincidencias_devuelve_vacio():
    """CA-28: un prefijo que nadie cumple devuelve [] sin error."""
    assert _arbol_de_nombres().buscar_por_prefijo("zz") == []


def test_prefijo_vacio_o_en_arbol_vacio_devuelve_vacio():
    """CA-28: extremo, prefijo vacío y árbol vacío devuelven [] (decisión del spec)."""
    assert _arbol_de_nombres().buscar_por_prefijo("") == []
    assert AVL().buscar_por_prefijo("a") == []


def test_prefijo_mas_largo_que_cualquier_clave_devuelve_vacio():
    """CA-28: extremo, un prefijo más largo que todas las claves no encuentra nada."""
    assert _arbol_de_nombres().buscar_por_prefijo("beatrizzzzzzzzzz") == []


# ---------- usuarios: comunidad inicial (CA-01, CA-02) ----------
def test_generar_crea_120_perfiles_con_usuarios_distintos():
    """CA-01: al iniciar hay al menos 100 perfiles, todos con @usuario único."""
    comunidad = generar_comunidad()
    usuarios = [p.usuario for p in comunidad.perfiles()]
    assert CANTIDAD_INICIAL == 120
    assert len(comunidad) == 120 >= 100
    assert len(set(usuarios)) == 120
    assert all(re.fullmatch(r"[a-z0-9_]{3,20}", u) for u in usuarios)


def test_cada_perfil_generado_se_encuentra_por_su_usuario_y_por_su_id():
    """CA-01: todos los perfiles son encontrables y los ids van de 0 a 119 en orden."""
    comunidad = generar_comunidad()
    for i, perfil in enumerate(comunidad.perfiles()):
        assert perfil.id == i
        assert comunidad.buscar(perfil.usuario) is perfil
        assert comunidad.por_id(i) is perfil
    assert comunidad.por_id(120) is None
    assert comunidad.por_id(-1) is None


def test_los_perfiles_generados_empiezan_con_cero_puntos():
    """CA-01: ningún perfil de ejemplo trae puntos."""
    assert all(p.puntos == 0 for p in generar_comunidad().perfiles())


def test_cantidad_personalizada_y_cantidad_imposible():
    """CA-01: extremo, 5 perfiles se generan; pedir más de los posibles lanza ValueError."""
    assert len(generar_comunidad(cantidad=5)) == 5
    with pytest.raises(ValueError):
        generar_comunidad(cantidad=10_000)


def test_120_perfiles_insertados_ya_ordenados_mantienen_el_indice_equilibrado():
    """CA-01: 120 @usuario en orden alfabético dejan el índice con altura logarítmica."""
    catalogo = Catalogo()
    for i in range(120):
        catalogo.crear_perfil(f"user{i:03d}")
    assert catalogo._indice.altura() <= _limite_altura(120)
    _verificar_avl(catalogo._indice)


def test_misma_semilla_da_los_mismos_perfiles_en_el_mismo_orden():
    """CA-02: dos generaciones con la semilla 706132 coinciden en usuarios y orden."""
    a = [p.usuario for p in generar_comunidad(SEMILLA).perfiles()]
    b = [p.usuario for p in generar_comunidad(SEMILLA).perfiles()]
    assert a == b
    assert SEMILLA == 706132


def test_semilla_por_defecto_es_la_706132():
    """CA-02: sin indicar semilla se usa SEMILLA y da lo mismo que pasarla."""
    por_defecto = [p.usuario for p in generar_comunidad().perfiles()]
    explicita = [p.usuario for p in generar_comunidad(706132).perfiles()]
    assert por_defecto == explicita


def test_otra_semilla_da_perfiles_distintos():
    """CA-02: una semilla distinta cambia la comunidad."""
    a = [p.usuario for p in generar_comunidad(706132).perfiles()]
    b = [p.usuario for p in generar_comunidad(1).perfiles()]
    assert a != b


def test_dos_comunidades_no_comparten_estado():
    """CA-02: crear un perfil en una comunidad no aparece en otra generada igual."""
    a, b = generar_comunidad(), generar_comunidad()
    a.crear_perfil("solo_en_a")
    assert a.buscar("solo_en_a") is not None
    assert b.buscar("solo_en_a") is None
    assert len(b) == 120


# ---------- usuarios: entrar (CA-03) ----------
def test_entrar_con_usuario_nuevo_crea_el_perfil_con_cero_puntos():
    """CA-03: entrar con un @usuario nuevo crea el perfil y abre la sesión."""
    catalogo = Catalogo()
    perfil, creado = catalogo.entrar("ana")
    assert creado is True
    assert perfil.usuario == "ana"
    assert perfil.puntos == 0
    assert len(catalogo) == 1


def test_entrar_con_usuario_existente_solo_abre_la_sesion():
    """CA-03: con un @usuario que ya existe no se crea otro perfil ni se tocan sus puntos."""
    catalogo = Catalogo()
    original, _ = catalogo.entrar("ana")
    original.puntos = 7
    perfil, creado = catalogo.entrar("ana")
    assert creado is False
    assert perfil is original
    assert perfil.puntos == 7
    assert len(catalogo) == 1


def test_entrar_dos_veces_seguidas_no_duplica():
    """CA-03: extremo, el segundo entrar con el mismo nombre no agrega nada."""
    catalogo = Catalogo()
    catalogo.entrar("ana")
    catalogo.entrar("ana")
    assert len(catalogo) == 1


def test_ana_Ana_ANA_y_arroba_ana_son_la_misma_persona():
    """CA-03: sin distinguir mayúsculas y con o sin @ inicial, es un único perfil guardado en minúsculas."""
    catalogo = Catalogo()
    primero, _ = catalogo.entrar("Ana")
    for variante in ("ANA", "@ana", "@Ana"):
        perfil, creado = catalogo.entrar(variante)
        assert perfil is primero
        assert creado is False
    assert primero.usuario == "ana"
    assert len(catalogo) == 1


def test_entrar_con_usuario_invalido_se_rechaza_y_no_crea_nada():
    """CA-03: entrar con un @usuario inválido lanza el error y el catálogo queda igual."""
    catalogo = Catalogo()
    with pytest.raises(UsuarioInvalidoError):
        catalogo.entrar("a")
    assert len(catalogo) == 0


# ---------- usuarios: validación (CA-04) ----------
def test_longitud_valida_de_3_a_20_caracteres():
    """CA-04: extremo, 3 y 20 caracteres se aceptan."""
    catalogo = Catalogo()
    assert catalogo.crear_perfil("abc").usuario == "abc"
    assert catalogo.crear_perfil("a" * 20).usuario == "a" * 20


def test_longitud_2_y_21_se_rechazan_con_el_motivo():
    """CA-04: extremo, 2 es muy corto y 21 es muy largo, y el mensaje lo dice."""
    catalogo = Catalogo()
    with pytest.raises(UsuarioInvalidoError, match="corto"):
        catalogo.crear_perfil("ab")
    with pytest.raises(UsuarioInvalidoError, match="largo"):
        catalogo.crear_perfil("a" * 21)
    assert len(catalogo) == 0


@pytest.mark.parametrize("usuario", ["ana maria", "ana-maria", "anáa", "ana@x", "ana!", "añb"])
def test_caracteres_no_permitidos_se_rechazan_con_el_motivo(usuario):
    """CA-04: espacio, guion, acento, @ en medio, signos y ñ no son letras, números ni guión bajo."""
    with pytest.raises(UsuarioInvalidoError, match="letras"):
        Catalogo().crear_perfil(usuario)


def test_guion_bajo_y_numeros_se_aceptan():
    """CA-04: el guión bajo y los dígitos sí están permitidos."""
    assert Catalogo().crear_perfil("ana_07").usuario == "ana_07"


@pytest.mark.parametrize("usuario", ["", "   ", "@"])
def test_usuario_vacio_se_rechaza_con_el_motivo(usuario):
    """CA-04: extremo, vacío, solo espacios o solo la arroba se rechazan como vacío."""
    with pytest.raises(UsuarioInvalidoError, match="vacío"):
        Catalogo().crear_perfil(usuario)


def test_usuario_que_no_es_texto_se_rechaza():
    """CA-04: extremo, None no es un @usuario y se rechaza con el mismo error."""
    with pytest.raises(UsuarioInvalidoError):
        Catalogo().crear_perfil(None)


def test_usuario_ya_existente_al_registrarse_se_rechaza_sin_importar_mayusculas():
    """CA-04: crear «ana» y luego «ANA» o «@ana» se rechaza como ya existente."""
    catalogo = Catalogo()
    catalogo.crear_perfil("ana")
    for repetido in ("ana", "ANA", "@ana"):
        with pytest.raises(UsuarioInvalidoError, match="ya existe"):
            catalogo.crear_perfil(repetido)
    assert len(catalogo) == 1


def test_el_error_es_un_value_error_con_mensaje_claro():
    """CA-04: UsuarioInvalidoError hereda de ValueError y su texto explica el motivo."""
    with pytest.raises(ValueError) as info:
        Catalogo().crear_perfil("ab")
    assert isinstance(info.value, UsuarioInvalidoError)
    assert "3" in str(info.value)


# ---------- usuarios: buscar por prefijo (CA-27, CA-28) ----------
def _catalogo_de_nombres():
    catalogo = Catalogo()
    for usuario in ("ana", "andres", "ana_07", "beatriz"):
        catalogo.crear_perfil(usuario)
    return catalogo


def test_buscar_usuarios_por_prefijo_devuelve_perfiles_en_orden_alfabetico():
    """CA-27: el prefijo «an» devuelve ana, ana_07 y andres, en orden alfabético."""
    encontrados = _catalogo_de_nombres().buscar_por_prefijo("an")
    assert [p.usuario for p in encontrados] == ["ana", "ana_07", "andres"]


@pytest.mark.parametrize("prefijo", ["AN", "An", "@an", "@AN"])
def test_el_prefijo_no_distingue_mayusculas_ni_arroba_inicial(prefijo):
    """CA-27: «AN», «An», «@an» y «@AN» encuentran lo mismo que «an»."""
    encontrados = _catalogo_de_nombres().buscar_por_prefijo(prefijo)
    assert [p.usuario for p in encontrados] == ["ana", "ana_07", "andres"]


def test_prefijo_sobre_la_comunidad_generada_coincide_con_filtrar_a_mano():
    """CA-27: sobre los 120 perfiles, cada resultado empieza por el prefijo y están todos."""
    comunidad = generar_comunidad()
    esperado = sorted(p.usuario for p in comunidad.perfiles() if p.usuario.startswith("ma"))
    encontrados = [p.usuario for p in comunidad.buscar_por_prefijo("ma")]
    assert encontrados == esperado
    assert len(esperado) > 0


def test_prefijo_sin_coincidencias_devuelve_lista_vacia():
    """CA-28: una búsqueda sin coincidencias devuelve [] y no falla."""
    assert _catalogo_de_nombres().buscar_por_prefijo("zzz") == []


@pytest.mark.parametrize("prefijo", ["", "   ", "@", "ñ", "an a", None])
def test_prefijos_vacios_o_raros_devuelven_lista_vacia(prefijo):
    """CA-28: extremo, vacío, solo @, caracteres no permitidos o None devuelven [] sin error."""
    assert _catalogo_de_nombres().buscar_por_prefijo(prefijo) == []


def test_buscar_en_catalogo_vacio_devuelve_vacio():
    """CA-28: extremo, sin usuarios la búsqueda y la consulta no fallan."""
    catalogo = Catalogo()
    assert catalogo.buscar_por_prefijo("a") == []
    assert catalogo.buscar("ana") is None


def test_buscar_un_perfil_por_su_usuario():
    """CA-03: consultar un perfil devuelve el perfil o None si no existe."""
    catalogo = _catalogo_de_nombres()
    assert catalogo.buscar("ANA").usuario == "ana"
    assert catalogo.buscar("@beatriz").usuario == "beatriz"
    assert catalogo.buscar("nadie") is None
    assert catalogo.buscar("a b") is None
