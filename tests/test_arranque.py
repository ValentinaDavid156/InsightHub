"""Pruebas de la consola (main.py): entrada con @usuario, menú, «atrás» y búsqueda de usuarios.

Integran CA-30, CA-31 (atrás), CA-03, CA-04 (entrar) y CA-27, CA-28 (buscar usuarios) en la
consola, como parte de CA-37. No sustituyen a las pruebas de cada estructura.
"""
import main
from dominio.usuarios import Catalogo


def _ejecutar(monkeypatch, capsys, respuestas, catalogo=None):
    entradas = iter(respuestas)
    monkeypatch.setattr("builtins.input", lambda _: next(entradas))
    main.menu(catalogo)
    return capsys.readouterr().out


def _catalogo_de_nombres():
    catalogo = Catalogo()
    for usuario in ("ana", "andres", "beatriz"):
        catalogo.crear_perfil(usuario)
    return catalogo


def test_arranque_pide_el_usuario_y_muestra_el_menu(monkeypatch, capsys):
    """CA-03: al arrancar pide el @usuario, abre la sesión y muestra el menú."""
    salida = _ejecutar(monkeypatch, capsys, ["tester", "0"])
    assert "Hola, @tester." in salida
    assert "=== InsightHub ===" in salida
    assert "Estás en: Inicio" in salida
    assert "Hasta pronto." in salida


def test_usuario_nuevo_se_crea_y_existente_solo_entra(monkeypatch, capsys):
    """CA-03: un @usuario nuevo crea el perfil; uno existente solo abre la sesión."""
    catalogo = _catalogo_de_nombres()
    salida = _ejecutar(monkeypatch, capsys, ["ana", "0"], catalogo)
    assert "Perfil creado" not in salida and len(catalogo) == 3
    salida = _ejecutar(monkeypatch, capsys, ["@Nuevo", "0"], catalogo)
    assert "Perfil creado" in salida and len(catalogo) == 4


def test_usuario_invalido_muestra_el_motivo_y_vuelve_a_pedir(monkeypatch, capsys):
    """CA-04: un @usuario inválido se rechaza con un mensaje claro y se vuelve a pedir."""
    salida = _ejecutar(monkeypatch, capsys, ["a", "ana maria", "tester", "0"])
    assert "corto" in salida
    assert "letras" in salida
    assert "Hola, @tester." in salida


def test_sin_entrada_el_arranque_sale_sin_error(monkeypatch, capsys):
    """CA-37: extremo, si la entrada se cierra (EOF) en el usuario, la consola sale sin fallar."""
    def sin_entrada(_):
        raise EOFError

    monkeypatch.setattr("builtins.input", sin_entrada)
    main.menu()
    assert "Hasta pronto." in capsys.readouterr().out


def test_el_menu_lista_las_opciones_en_orden_numerico(monkeypatch, capsys):
    """CA-37: las opciones salen de la 1 a la 8 y al final la 0, sin saltos."""
    salida = _ejecutar(monkeypatch, capsys, ["tester", "0"])
    numeros = [l.split(".")[0] for l in salida.splitlines() if l[:2] in {f"{n}." for n in range(9)}]
    assert numeros == ["1", "2", "3", "4", "5", "6", "7", "8", "0"]


def test_mi_perfil_muestra_usuario_y_puntos(monkeypatch, capsys):
    """CA-03: consultar mi perfil muestra mi @usuario y mis puntos."""
    salida = _ejecutar(monkeypatch, capsys, ["tester", "1", "0"])
    assert "@tester" in salida
    assert "0 puntos" in salida


def test_opcion_pendiente_avisa_y_vuelve_al_menu(monkeypatch, capsys):
    """CA-37: una opción aún sin implementar avisa y deja la pantalla en el historial."""
    salida = _ejecutar(monkeypatch, capsys, ["tester", "2", "0"])
    assert "aún no implementada" in salida
    assert "Estás en: Amigos y solicitudes" in salida


def test_opcion_inexistente_no_falla(monkeypatch, capsys):
    """CA-37: extremo, opciones inválidas avisan y el menú sigue."""
    salida = _ejecutar(monkeypatch, capsys, ["tester", "abc", "", "99", "0"])
    assert salida.count("Opción no válida.") == 3
    assert "Hasta pronto." in salida


def test_atras_en_inicio_informa_que_no_hay_pantalla_previa(monkeypatch, capsys):
    """CA-31 integrado: «atrás» sin historial informa y el menú sigue."""
    salida = _ejecutar(monkeypatch, capsys, ["tester", "6", "0"])
    assert "No hay pantalla previa." in salida


def test_atras_vuelve_a_la_pantalla_anterior(monkeypatch, capsys):
    """CA-30 integrado: abrir pantallas y volver atrás en orden inverso."""
    salida = _ejecutar(monkeypatch, capsys, ["tester", "3", "7", "6", "6", "0"])
    estados = [l for l in salida.splitlines() if l.startswith("Estás en:")]
    assert estados == [
        "Estás en: Inicio",
        "Estás en: Plaza: publicar y recorrer",
        "Estás en: Notificaciones",
        "Estás en: Plaza: publicar y recorrer",
        "Estás en: Inicio",
    ]


def test_buscar_usuarios_por_prefijo_lista_en_orden_alfabetico(monkeypatch, capsys):
    """CA-27 integrado: buscar «an» muestra ana y andres en orden y no a beatriz."""
    salida = _ejecutar(monkeypatch, capsys, ["tester", "5", "an", "0"], _catalogo_de_nombres())
    lineas = [l.strip() for l in salida.splitlines()]
    assert lineas.index("@ana") < lineas.index("@andres")
    assert "@beatriz" not in lineas


def test_buscar_usuarios_sin_coincidencias_informa(monkeypatch, capsys):
    """CA-28 integrado: sin coincidencias, y con prefijo vacío, informa sin error."""
    salida = _ejecutar(monkeypatch, capsys, ["tester", "5", "zzz", "5", "", "0"])
    assert salida.count("Sin coincidencias.") == 2
