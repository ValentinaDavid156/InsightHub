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


def test_ya_no_quedan_opciones_pendientes(monkeypatch, capsys):
    """CA-37: todas las opciones Must del menú funcionan."""
    salida = _ejecutar(monkeypatch, capsys, ["tester", "0"])
    assert "(pendiente)" not in salida


def test_recomendaciones_sin_amigos_informa(monkeypatch, capsys):
    """CA-36 integrado: sin amigos no hay recomendaciones y no falla."""
    salida = _ejecutar(monkeypatch, capsys, ["tester", "8", "0"])
    assert "No hay recomendaciones por ahora." in salida
    assert "Estás en: Personas que quizá conozcas" in salida


def test_recomendaciones_en_consola_con_amigos_en_comun(monkeypatch, capsys):
    """CA-34 y CA-35 integrados: ana-luis y luis-beatriz son amigos; ana ve a beatriz."""
    salida = _ejecutar(
        monkeypatch, capsys,
        ["ana", "2", "2", "luis", "0", "9", "luis", "2", "3", "1", "2", "beatriz", "0",
         "9", "beatriz", "2", "3", "1", "0", "9", "ana", "8", "0"],
        _catalogo_de_nombres_con_luis(),
    )
    assert "@beatriz (1 amigo en común)" in salida


def test_recomendaciones_dicen_amigos_en_plural(capsys):
    """La consola concuerda «amigos» con el número."""
    from dominio.amistades import Amistades
    catalogo = Catalogo()
    for usuario in ("yoli", "aaa", "bbb", "meta"):
        catalogo.crear_perfil(usuario)
    amistades = Amistades(catalogo)
    for x, y in ((0, 1), (0, 2), (1, 3), (2, 3)):
        amistades.grafo.agregar_amistad(x, y)
    main.ver_recomendaciones(amistades, catalogo.buscar("yoli"))
    assert "@meta (2 amigos en común)" in capsys.readouterr().out


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
    salida = _ejecutar(monkeypatch, capsys, ["tester", "5", "zzz", "7", "6", "6", "0"])
    estados = [l for l in salida.splitlines() if l.startswith("Estás en:")]
    assert estados == [
        "Estás en: Inicio",
        "Estás en: Buscar usuarios",
        "Estás en: Notificaciones",
        "Estás en: Buscar usuarios",
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


def test_buscar_el_usuario_exacto_muestra_su_perfil(monkeypatch, capsys):
    """RF-05 (AVL): escribir un @usuario completo muestra el perfil de esa persona con sus puntos."""
    salida = _ejecutar(monkeypatch, capsys, ["tester", "5", "andres", "0"], _catalogo_de_nombres())
    assert "Perfil de @andres: 0 puntos." in salida


def test_buscar_el_usuario_exacto_con_arroba_y_mayusculas(monkeypatch, capsys):
    """RF-05 (AVL): la consulta del perfil no distingue mayúsculas y acepta la @ inicial."""
    salida = _ejecutar(monkeypatch, capsys, ["tester", "5", "@ANA", "0"], _catalogo_de_nombres())
    assert "Perfil de @ana: 0 puntos." in salida


def test_buscar_solo_un_prefijo_no_muestra_ningun_perfil(monkeypatch, capsys):
    """RF-05 (AVL): «an» no es un @usuario completo, así que solo se listan coincidencias."""
    salida = _ejecutar(monkeypatch, capsys, ["tester", "5", "an", "0"], _catalogo_de_nombres())
    assert "Perfil de @" not in salida


def test_buscar_un_usuario_que_no_existe_lo_dice(monkeypatch, capsys):
    """RF-05 (AVL): si el @usuario no existe, la consola lo dice sin fallar."""
    salida = _ejecutar(monkeypatch, capsys, ["tester", "5", "zzz", "0"], _catalogo_de_nombres())
    assert "Sin coincidencias." in salida
    assert "Perfil de @" not in salida


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


# ---------- Plaza e hilos en la consola (CA-12, CA-13, CA-14 a CA-16, CA-29) ----------
# Plaza («3»): 1 publicar, 2 ver, 3 siguiente, 4 anterior, 5 inicio, 6 buscar, 0 volver.
# Hilos («4»): se escribe el número de la publicación; dentro: 1 responder, 0 volver.

PUBLICA_ANA = ["ana", "3", "1", "Mi pregunta", "Mi cuerpo", "0"]


def test_publicar_y_ver_la_plaza(monkeypatch, capsys):
    """CA-12 integrado: lo publicado aparece en la página."""
    salida = _ejecutar(
        monkeypatch, capsys, ["ana", "3", "1", "Mi pregunta", "c", "2", "0", "0"], _catalogo_de_nombres_con_luis()
    )
    assert "Publicación #1 creada." in salida
    assert "#1 @ana" in salida and "Mi pregunta" in salida


def test_titulo_vacio_muestra_el_motivo(monkeypatch, capsys):
    """Título vacío se rechaza y la plaza sigue vacía."""
    salida = _ejecutar(monkeypatch, capsys, ["ana", "3", "1", "   ", "c", "2", "0", "0"], _catalogo_de_nombres_con_luis())
    assert "título" in salida
    assert "No hay publicaciones." in salida


def test_plaza_vacia_informa_al_paginar(monkeypatch, capsys):
    """CA-13 integrado: con la plaza vacía no falla."""
    salida = _ejecutar(monkeypatch, capsys, ["tester", "3", "2", "3", "4", "5", "0", "0"])
    assert salida.count("No hay publicaciones.") == 4


def test_paginar_y_avisar_los_limites(monkeypatch, capsys):
    """CA-13 integrado: 7 publicaciones son 2 páginas; en los extremos se avisa."""
    publicar = []
    for i in range(7):
        publicar += ["1", f"p{i}", "c"]
    salida = _ejecutar(
        monkeypatch, capsys,
        ["ana", "3"] + publicar + ["2", "4", "3", "3", "5", "0", "0"],
        _catalogo_de_nombres_con_luis(),
    )
    assert "Estás en el principio de la plaza." in salida
    assert "Llegaste al final de la plaza." in salida


def test_buscar_por_palabra_en_consola(monkeypatch, capsys):
    """CA-29 integrado: busca en título y cuerpo; sin coincidencias informa."""
    salida = _ejecutar(
        monkeypatch, capsys,
        ["ana", "3", "1", "Aprender Python", "c", "6", "python", "6", "zzz", "6", "", "0", "0"],
        _catalogo_de_nombres_con_luis(),
    )
    assert "#1 @ana" in salida
    assert salida.count("Sin coincidencias.") == 2


def test_responder_y_ver_el_hilo_con_sangria(monkeypatch, capsys):
    """CA-14 y CA-15 integrados: el hilo se muestra con sangría por nivel."""
    salida = _ejecutar(
        monkeypatch, capsys,
        PUBLICA_ANA + ["4", "1", "1", "0", "uno", "1", "1", "dos", "1", "2", "tres", "0", "0"],
        _catalogo_de_nombres_con_luis(),
    )
    assert "[0] @ana: Mi pregunta — Mi cuerpo" in salida
    assert "\n  [1] @ana: uno" in salida
    assert "\n    [2] @ana: dos" in salida
    assert "\n      [3] @ana: tres" in salida


def test_responder_a_padre_inexistente_informa_y_no_cambia(monkeypatch, capsys):
    """CA-16 integrado: se muestra el motivo y el menú sigue."""
    salida = _ejecutar(
        monkeypatch, capsys,
        PUBLICA_ANA + ["4", "1", "1", "9", "hola", "1", "abc", "0", "0"],
        _catalogo_de_nombres_con_luis(),
    )
    assert "no existe" in salida
    assert "Número no válido." in salida
    assert "hola" not in salida.replace("Hola", "")


def test_respuesta_vacia_muestra_el_motivo(monkeypatch, capsys):
    """La respuesta vacía se rechaza en la consola."""
    salida = _ejecutar(
        monkeypatch, capsys, PUBLICA_ANA + ["4", "1", "1", "0", "  ", "0", "0"], _catalogo_de_nombres_con_luis()
    )
    assert "vacía" in salida


def test_abrir_hilo_inexistente_informa(monkeypatch, capsys):
    """CA-16 integrado: publicación inexistente o texto en vez de número."""
    salida = _ejecutar(monkeypatch, capsys, ["tester", "4", "7", "4", "abc", "0"])
    assert "Esa publicación no existe." in salida
    assert "Número no válido." in salida
    assert "Hasta pronto." in salida


def test_responder_avisa_en_consola(monkeypatch, capsys):
    """RF-09 de la cola integrado: luis responde y ana lee el aviso."""
    salida = _ejecutar(
        monkeypatch, capsys,
        PUBLICA_ANA + ["9", "luis", "4", "1", "1", "0", "hola", "0", "9", "ana", "7", "0"],
        _catalogo_de_nombres_con_luis(),
    )
    assert "@luis respondió a tu publicación «Mi pregunta»." in salida


def test_volver_de_plaza_e_hilos_regresa_a_inicio(monkeypatch, capsys):
    """CA-30 integrado: el 0 de esos submenús es «atrás»."""
    salida = _ejecutar(monkeypatch, capsys, PUBLICA_ANA + ["4", "1", "0", "0"], _catalogo_de_nombres_con_luis())
    assert [l for l in salida.splitlines() if l.startswith("Estás en:")] == ["Estás en: Inicio"] * 3


def test_submenu_de_plaza_e_hilo_rechazan_opciones(monkeypatch, capsys):
    """CA-37: extremo, opción inexistente en los submenús."""
    salida = _ejecutar(
        monkeypatch, capsys, PUBLICA_ANA + ["3", "x", "0", "4", "1", "x", "0", "0"], _catalogo_de_nombres_con_luis()
    )
    assert salida.count("Opción no válida.") == 2


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
