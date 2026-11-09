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


def _catalogo_de_nombres_con_luis():
    catalogo = _catalogo_de_nombres()
    catalogo.crear_perfil("luis")
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
    """CA-37: las opciones salen de la 1 a la 9 y al final la 0, sin saltos."""
    salida = _ejecutar(monkeypatch, capsys, ["tester", "0"])
    numeros = [l.split(".")[0] for l in salida.splitlines() if l[:2] in {f"{n}." for n in range(10)}]
    assert numeros == ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]


def test_mi_perfil_muestra_usuario_y_puntos(monkeypatch, capsys):
    """CA-03: consultar mi perfil muestra mi @usuario y mis puntos."""
    salida = _ejecutar(monkeypatch, capsys, ["tester", "1", "0"])
    assert "@tester" in salida
    assert "0 puntos" in salida


def test_opcion_pendiente_avisa_y_vuelve_al_menu(monkeypatch, capsys):
    """CA-37: una opción aún sin implementar avisa y deja la pantalla en el historial."""
    salida = _ejecutar(monkeypatch, capsys, ["tester", "3", "0"])
    assert "aún no implementada" in salida
    assert "Estás en: Plaza: publicar y recorrer" in salida


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


# ---------- Amigos, solicitudes y notificaciones en la consola (CA-05 a CA-08, CA-32, CA-33) ----------
# Secuencias: «2» abre Amigos; dentro: 1 ver, 2 enviar, 3 revisar, 4 deshacer, 0 volver.
# «9» cambia de @usuario.

ANA_ENVIA_A_LUIS = ["ana", "2", "2", "luis", "0"]
LUIS_ACEPTA = ["9", "luis", "2", "3", "1", "0"]


def test_enviar_y_aceptar_entre_dos_personas(monkeypatch, capsys):
    """CA-05, CA-06 integrados: ana envía, se cambia a luis, acepta y son amigos."""
    salida = _ejecutar(
        monkeypatch, capsys,
        ANA_ENVIA_A_LUIS + LUIS_ACEPTA + ["2", "1", "0", "0"],
        _catalogo_de_nombres_con_luis(),
    )
    assert "Solicitud enviada a @luis." in salida
    assert "Hola, @luis." in salida
    assert "Solicitud de @ana" in salida
    assert "Ahora eres amigo de @ana." in salida
    assert "  @ana" in salida


def test_rechazar_no_crea_amistad_en_consola(monkeypatch, capsys):
    """CA-06 integrado: rechazar informa y la lista de amigos sigue vacía."""
    salida = _ejecutar(
        monkeypatch, capsys,
        ANA_ENVIA_A_LUIS + ["9", "luis", "2", "3", "2", "1", "0", "0"],
        _catalogo_de_nombres_con_luis(),
    )
    assert "Rechazaste la solicitud de @ana." in salida
    assert "Aún no tienes amigos." in salida


def test_dejar_la_solicitud_para_despues_no_la_saca(monkeypatch, capsys):
    """CA-07 integrado: sin decidir, la solicitud sigue siendo la primera."""
    salida = _ejecutar(
        monkeypatch, capsys,
        ANA_ENVIA_A_LUIS + ["9", "luis", "2", "3", "0", "3", "9", "1", "0", "0"],
        _catalogo_de_nombres_con_luis(),
    )
    assert salida.count("Solicitud de @ana") == 2
    assert "Opción no válida." in salida
    assert "Ahora eres amigo de @ana." in salida


def test_enviar_rechazada_muestra_el_motivo_y_sigue(monkeypatch, capsys):
    """CA-05 integrado: a uno mismo y a alguien inexistente muestran el motivo."""
    salida = _ejecutar(
        monkeypatch, capsys,
        ["ana", "2", "2", "ana", "2", "nadie", "0", "0"],
        _catalogo_de_nombres_con_luis(),
    )
    assert "ti mismo" in salida
    assert "no existe" in salida
    assert "Hasta pronto." in salida


def test_revisar_sin_solicitudes_informa(monkeypatch, capsys):
    """CA-07 integrado: sin pendientes informa sin error."""
    salida = _ejecutar(monkeypatch, capsys, ["tester", "2", "3", "0", "0"])
    assert "No tienes solicitudes pendientes." in salida


def test_deshacer_amistad_en_consola(monkeypatch, capsys):
    """CA-08 integrado: deshacer informa, y repetirlo avisa que no son amigos."""
    salida = _ejecutar(
        monkeypatch, capsys,
        ANA_ENVIA_A_LUIS + LUIS_ACEPTA + ["2", "4", "ana", "4", "ana", "1", "0", "0"],
        _catalogo_de_nombres_con_luis(),
    )
    assert "Ya no eres amigo de @ana." in salida
    assert "No eres amigo de @ana." in salida
    assert "Aún no tienes amigos." in salida


def test_el_submenu_rechaza_opciones_invalidas(monkeypatch, capsys):
    """CA-37: extremo, opción inexistente en el submenú avisa y lo repite."""
    salida = _ejecutar(monkeypatch, capsys, ["tester", "2", "x", "", "0", "0"])
    assert salida.count("Opción no válida.") == 2
    assert "Hasta pronto." in salida


def test_volver_del_submenu_regresa_a_la_pantalla_anterior(monkeypatch, capsys):
    """CA-30 integrado: el 0 del submenú es «atrás»."""
    salida = _ejecutar(monkeypatch, capsys, ["tester", "2", "0", "0"])
    assert [l for l in salida.splitlines() if l.startswith("Estás en:")] == [
        "Estás en: Inicio",
        "Estás en: Inicio",
    ]


def test_notificaciones_en_consola_en_orden_y_se_vacian(monkeypatch, capsys):
    """CA-32 integrado: luis lee sus avisos en orden; ana recibe el de aceptada; leer vacía."""
    salida = _ejecutar(
        monkeypatch, capsys,
        ANA_ENVIA_A_LUIS + ["9", "luis", "7", "7", "2", "3", "1", "0", "9", "ana", "7", "0"],
        _catalogo_de_nombres_con_luis(),
    )
    assert "@ana te envió una solicitud de amistad." in salida
    assert "Sin notificaciones." in salida
    assert "@luis aceptó tu solicitud de amistad." in salida


def test_sin_notificaciones_en_consola(monkeypatch, capsys):
    """CA-33 integrado: sin pendientes informa «sin notificaciones»."""
    salida = _ejecutar(monkeypatch, capsys, ["tester", "7", "0"])
    assert "Sin notificaciones." in salida


def test_cambiar_de_usuario_conserva_los_datos_y_reinicia_el_historial(monkeypatch, capsys):
    """CA-37: cambiar @usuario no borra nada; el «atrás» de la nueva sesión empieza en Inicio."""
    salida = _ejecutar(
        monkeypatch, capsys,
        ["ana", "5", "an", "9", "nueva", "6", "9", "ana", "0"],
        _catalogo_de_nombres_con_luis(),
    )
    assert "Perfil creado." in salida
    assert "No hay pantalla previa." in salida
    assert salida.count("Hola, @ana.") == 2


def test_cambiar_usuario_invalido_vuelve_a_pedir(monkeypatch, capsys):
    """CA-04 integrado: al cambiar también se valida el @usuario."""
    salida = _ejecutar(monkeypatch, capsys, ["ana", "9", "x", "luis", "0"], _catalogo_de_nombres_con_luis())
    assert "corto" in salida
    assert "Hola, @luis." in salida


def test_entrada_cerrada_dentro_del_submenu_sale_sin_error(monkeypatch, capsys):
    """CA-37: extremo, EOF dentro de un submenú o de un prompt termina sin fallar."""
    entradas = iter(["tester", "2", "2"])

    def responder(_):
        try:
            return next(entradas)
        except StopIteration:
            raise EOFError

    monkeypatch.setattr("builtins.input", responder)
    main.menu()
    assert "Hasta pronto." in capsys.readouterr().out


def test_entrada_cerrada_al_cambiar_de_usuario_sale_sin_error(monkeypatch, capsys):
    """CA-37: extremo, EOF al pedir el nuevo @usuario termina sin fallar."""
    entradas = iter(["tester", "9"])

    def responder(_):
        try:
            return next(entradas)
        except StopIteration:
            raise EOFError

    monkeypatch.setattr("builtins.input", responder)
    main.menu()
    assert "Hasta pronto." in capsys.readouterr().out
