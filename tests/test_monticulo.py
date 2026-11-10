"""Pruebas del montículo máximo y de las recomendaciones (specs/07-monticulo), antes del código.

Criterio Must: CA-35. Decisiones de Valentina: con el montículo vacío, `maximo` y
`extraer_maximo` lanzan MonticuloVacioError (como la pila y la cola); la consola muestra
cada recomendación con su número de amigos en común.
"""

import random

import pytest

from dominio.amistades import Amistades
from dominio.recomendaciones import LIMITE, recomendar
from dominio.usuarios import Catalogo
from estructuras.monticulo import Monticulo, MonticuloVacioError


def mayor(a, b):
    return a > b


def _es_monticulo(m):
    datos = m._datos
    for i in range(1, len(datos)):
        if m._antes(datos[i], datos[(i - 1) // 2]):
            return False
    return True


def _vaciar(m):
    salida = []
    while not m.esta_vacio():
        salida.append(m.extraer_maximo())
        assert _es_monticulo(m)
    return salida


# ---------- Parte A: insertar, maximo, extraer_maximo ----------

def test_monticulo_nuevo_esta_vacio():
    m = Monticulo(mayor)
    assert m.esta_vacio() and m.tamano() == 0 and len(m) == 0


def test_vacio_lanza_error_controlado_sin_cambiar_nada():
    """Decisión de Valentina: igual que PilaVaciaError y ColaVaciaError."""
    m = Monticulo(mayor)
    with pytest.raises(MonticuloVacioError):
        m.maximo()
    with pytest.raises(MonticuloVacioError):
        m.extraer_maximo()
    assert m.tamano() == 0
    assert issubclass(MonticuloVacioError, IndexError)


def test_un_elemento():
    m = Monticulo(mayor)
    m.insertar(7)
    assert m.maximo() == 7 and m.tamano() == 1
    assert m.extraer_maximo() == 7
    assert m.esta_vacio()


def test_maximo_no_saca_nada():
    m = Monticulo(mayor)
    for x in (3, 9, 1):
        m.insertar(x)
    assert m.maximo() == 9 and m.maximo() == 9
    assert m.tamano() == 3


def test_extraer_siempre_da_el_mayor():
    m = Monticulo(mayor)
    for x in (5, 1, 9, 3, 7, 2, 8):
        m.insertar(x)
        assert _es_monticulo(m)
    assert _vaciar(m) == [9, 8, 7, 5, 3, 2, 1]


def test_cien_en_orden_creciente_y_decreciente():
    for orden in (range(100), range(99, -1, -1)):
        m = Monticulo(mayor)
        for x in orden:
            m.insertar(x)
            assert _es_monticulo(m)
        assert _vaciar(m) == list(range(99, -1, -1))


def test_repetidos_con_la_misma_clave():
    m = Monticulo(mayor)
    for x in (4, 4, 2, 4, 2):
        m.insertar(x)
    assert _vaciar(m) == [4, 4, 4, 2, 2]


def test_la_funcion_antes_decide_el_orden():
    """El mismo montículo sirve como mínimo si `antes` lo pide."""
    m = Monticulo(lambda a, b: a < b)
    for x in (5, 1, 9):
        m.insertar(x)
    assert _vaciar(m) == [1, 5, 9]


def test_vaciar_y_volver_a_usar():
    m = Monticulo(mayor)
    m.insertar(1)
    m.extraer_maximo()
    m.insertar(3)
    m.insertar(2)
    assert m.maximo() == 3


def test_aleatorio_coincide_con_ordenar():
    azar = random.Random(706132)
    datos = [azar.randint(0, 50) for _ in range(300)]
    m = Monticulo(mayor)
    for x in datos:
        m.insertar(x)
    assert _vaciar(m) == sorted(datos, reverse=True)


# ---------- Parte A: construir ----------

def test_construir_da_lo_mismo_que_insertar_de_uno_en_uno():
    datos = [5, 1, 9, 3, 7, 2, 8, 6, 4, 0]
    uno = Monticulo(mayor)
    for x in datos:
        uno.insertar(x)
    otro = Monticulo(mayor)
    otro.construir(datos)
    assert _es_monticulo(otro) and otro.tamano() == 10
    assert _vaciar(otro) == _vaciar(uno)


def test_construir_vacio_y_un_elemento():
    m = Monticulo(mayor)
    m.construir([])
    assert m.esta_vacio()
    m.construir([4])
    assert m.maximo() == 4 and m.tamano() == 1


def test_construir_no_modifica_la_lista_recibida():
    datos = [1, 5, 3]
    m = Monticulo(mayor)
    m.construir(datos)
    m.extraer_maximo()
    assert datos == [1, 5, 3]


def test_construir_reemplaza_lo_que_habia():
    m = Monticulo(mayor)
    m.insertar(100)
    m.construir([1, 2])
    assert _vaciar(m) == [2, 1]


def test_construir_mil_aleatorios():
    azar = random.Random(706132)
    datos = [azar.randint(0, 10_000) for _ in range(1000)]
    m = Monticulo(mayor)
    m.construir(datos)
    assert _es_monticulo(m)
    assert _vaciar(m)[:5] == sorted(datos, reverse=True)[:5]


# ---------- Parte B: CA-35, recomendaciones ordenadas ----------

def _red(usuarios, amistades_por_nombre):
    catalogo = Catalogo()
    for usuario in usuarios:
        catalogo.crear_perfil(usuario)
    amistades = Amistades(catalogo)
    for a, b in amistades_por_nombre:
        amistades.grafo.agregar_amistad(catalogo.buscar(a).id, catalogo.buscar(b).id)
    return catalogo, amistades


def _nombres(recomendaciones):
    return [(perfil.usuario, comunes) for perfil, comunes in recomendaciones]


def test_sin_candidatos_lista_vacia():
    """CA-35 y CA-36: sin amigos no hay recomendaciones."""
    catalogo, amistades = _red(["yoli", "ana"], [])
    assert recomendar(amistades, catalogo.buscar("yoli").id) == []


def test_persona_inexistente_lista_vacia():
    catalogo, amistades = _red(["yoli"], [])
    assert recomendar(amistades, 99) == []


def test_un_solo_candidato():
    catalogo, amistades = _red(["yoli", "ana", "luis"], [("yoli", "ana"), ("ana", "luis")])
    assert _nombres(recomendar(amistades, 0)) == [("luis", 1)]


def test_ordena_por_amigos_en_comun_de_mayor_a_menor():
    """CA-35."""
    catalogo, amistades = _red(
        ["yoli", "am1", "am2", "am3", "uno", "dos", "tres"],
        [("yoli", "am1"), ("yoli", "am2"), ("yoli", "am3"),
         ("am1", "tres"), ("am2", "tres"), ("am3", "tres"),
         ("am1", "uno"),
         ("am1", "dos"), ("am2", "dos")],
    )
    assert _nombres(recomendar(amistades, 0)) == [("tres", 3), ("dos", 2), ("uno", 1)]


def test_empate_en_orden_alfabetico():
    """CA-35: si empatan, primero el @usuario alfabéticamente menor."""
    catalogo, amistades = _red(
        ["yoli", "ana", "zoe", "beto", "carla"],
        [("yoli", "ana"), ("ana", "zoe"), ("ana", "carla"), ("ana", "beto")],
    )
    assert _nombres(recomendar(amistades, 0)) == [("beto", 1), ("carla", 1), ("zoe", 1)]


def _estrella(cuantos):
    """yoli es amiga de «puente», y puente de `cuantos` personas c00, c01..."""
    otros = [f"c{i:02d}" for i in range(cuantos)]
    return _red(["yoli", "puente"] + otros, [("yoli", "puente")] + [("puente", c) for c in otros])


def test_exactamente_cinco_se_entregan_los_cinco():
    catalogo, amistades = _estrella(5)
    assert LIMITE == 5
    assert len(recomendar(amistades, 0)) == 5


def test_con_seis_solo_los_cinco_mejores():
    """CA-35: con empate total, los 5 primeros alfabéticamente."""
    catalogo, amistades = _estrella(6)
    assert [u for u, _ in _nombres(recomendar(amistades, 0))] == ["c00", "c01", "c02", "c03", "c04"]


def test_cincuenta_en_comun_va_antes_que_uno():
    usuarios = ["yoli", "zz_popular", "aa_solo"] + [f"am{i:02d}" for i in range(50)]
    pares = []
    for i in range(50):
        pares += [("yoli", f"am{i:02d}"), (f"am{i:02d}", "zz_popular")]
    pares.append(("am00", "aa_solo"))
    catalogo, amistades = _red(usuarios, pares)
    assert _nombres(recomendar(amistades, 0)) == [("zz_popular", 50), ("aa_solo", 1)]


def test_pedirlas_dos_veces_da_lo_mismo_y_no_cambia_la_red():
    """RF-02: consultar no altera candidatos ni amistades."""
    catalogo, amistades = _estrella(7)
    antes = [amistades.grafo.amigos(i) for i in range(catalogo.tamano())]
    candidatos = amistades.grafo.candidatos_dos_saltos(0)
    primera = _nombres(recomendar(amistades, 0))
    assert _nombres(recomendar(amistades, 0)) == primera
    assert amistades.grafo.candidatos_dos_saltos(0) == candidatos
    assert [amistades.grafo.amigos(i) for i in range(catalogo.tamano())] == antes


def test_no_recomienda_a_quien_ya_es_amigo_ni_a_si_misma():
    """CA-34 integrado."""
    catalogo, amistades = _red(
        ["yoli", "ana", "luis", "sara"],
        [("yoli", "ana"), ("yoli", "luis"), ("ana", "luis"), ("luis", "sara")],
    )
    assert _nombres(recomendar(amistades, 0)) == [("sara", 1)]
