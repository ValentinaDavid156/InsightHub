"""Prueba del sistema (specs/99-sistema): CA-37 y RF-01 a RF-07.

CA-37: cada función implementada de las historias HU-02 a HU-13 se ejercita desde la consola,
de punta a punta, con la comunidad real de 120 perfiles (semilla 706132). Cada prueba recorre
una historia con varias personas que entran y salen con la opción 9 («Cambiar de @usuario»).
Las pruebas de cada estructura siguen en su propio archivo; aquí solo se mira la integración.
"""

import main
from dominio.usuarios import generar_comunidad


def _consola(monkeypatch, capsys, entradas):
    """Ejecuta main.menu() con la comunidad real y devuelve todo lo que imprimió."""
    respuestas = iter(entradas)
    monkeypatch.setattr("builtins.input", lambda _: next(respuestas))
    main.menu()
    return capsys.readouterr().out


def _cambiar(usuario):
    return ["9", usuario]


# Secuencias de una persona ya dentro del menú principal.
def _enviar(destino):
    return ["2", "2", destino, "0"]


ACEPTAR_PRIMERA = ["2", "3", "1", "0"]
RECHAZAR_PRIMERA = ["2", "3", "2", "0"]
VER_AMIGOS = ["2", "1", "0"]


def _publicar(titulo, cuerpo):
    return ["3", "1", titulo, cuerpo, "0"]


def _responder(publicacion, padre, texto):
    return ["4", str(publicacion), "1", str(padre), texto, "0"]


# ---------- RF-01: arranque con la comunidad sembrada y nada más ----------

def test_rf01_arranca_con_120_perfiles_y_sin_contenido(monkeypatch, capsys):
    """RF-01: los perfiles de la semilla existen; plaza, notificaciones, amigos y recomendaciones vacíos."""
    comunidad = generar_comunidad()
    primero = comunidad.por_id(0).usuario
    salida = _consola(
        monkeypatch, capsys,
        ["sistema_1", "5", primero, "3", "2", "0", "7", "8"] + VER_AMIGOS + ["2", "3", "0", "0"],
    )
    assert len(comunidad) == 120
    assert f"  @{primero}" in salida                 # un perfil de la semilla se encuentra
    assert "No hay publicaciones." in salida
    assert "Sin notificaciones." in salida
    assert "No hay recomendaciones por ahora." in salida
    assert "Aún no tienes amigos." in salida
    assert "No tienes solicitudes pendientes." in salida


def test_rf01_entrar_con_un_perfil_de_la_semilla_no_lo_crea(monkeypatch, capsys):
    """RF-01 y CA-03: un @usuario sembrado ya existe."""
    primero = generar_comunidad().por_id(0).usuario
    salida = _consola(monkeypatch, capsys, [primero.upper(), "1", "0"])
    assert "Perfil creado." not in salida
    assert f"Tu perfil: @{primero}, 0 puntos." in salida


# ---------- HU-02: acceder y crear perfil ----------

def test_hu02_entrar_validar_y_ver_perfil(monkeypatch, capsys):
    """CA-03 y CA-04 por consola."""
    salida = _consola(monkeypatch, capsys, ["", "ab", "con espacio", "Nueva_Persona", "1", "0"])
    assert "vacío" in salida and "corto" in salida and "letras" in salida
    assert "Perfil creado." in salida
    assert "Tu perfil: @nueva_persona, 0 puntos." in salida


# ---------- HU-03: amistades con solicitud ----------

def test_hu03_enviar_aceptar_rechazar_deshacer(monkeypatch, capsys):
    """CA-05 a CA-08 por consola, con tres personas."""
    entradas = (
        ["luis_s"] + _cambiar("sara_s") + _cambiar("ana_s")
        + _enviar("luis_s") + _enviar("sara_s")
        + ["2", "2", "luis_s", "2", "ana_s", "0"]            # repetida y a sí misma: rechazadas
        + _cambiar("luis_s") + ACEPTAR_PRIMERA + VER_AMIGOS
        + _cambiar("sara_s") + RECHAZAR_PRIMERA + VER_AMIGOS
        + _cambiar("ana_s") + VER_AMIGOS
        + ["2", "4", "luis_s", "4", "luis_s", "0"]            # deshacer y deshacer otra vez
        + VER_AMIGOS + ["0"]
    )
    salida = _consola(monkeypatch, capsys, entradas)
    assert salida.count("Solicitud enviada") == 2
    assert "Ya le enviaste una solicitud a @luis_s." in salida
    assert "No puedes enviarte una solicitud a ti mismo." in salida
    assert "Ahora eres amigo de @ana_s." in salida
    assert "Rechazaste la solicitud de @ana_s." in salida
    assert "  @luis_s" in salida                               # ana ve a luis antes de deshacer
    assert "Ya no eres amigo de @luis_s." in salida
    assert "No eres amigo de @luis_s." in salida


def test_hu03_solicitudes_en_orden_de_llegada(monkeypatch, capsys):
    """CA-07 por consola: luis y sara le escriben a ana; ana las ve en ese orden."""
    entradas = (
        ["ana_o"] + _cambiar("luis_o") + _enviar("ana_o") + _cambiar("sara_o") + _enviar("ana_o")
        + _cambiar("ana_o") + ACEPTAR_PRIMERA + ["2", "3", "0", "0", "0"]
    )
    salida = _consola(monkeypatch, capsys, entradas)
    primera = salida.index("Solicitud de @luis_o")
    segunda = salida.index("Solicitud de @sara_o")
    assert primera < segunda


# ---------- HU-05: publicar y recorrer la plaza ----------

def test_hu05_publicar_y_paginar(monkeypatch, capsys):
    """CA-12 y CA-13 por consola: 6 publicaciones, la última queda primera y hay 2 páginas."""
    entradas = ["autora_p", "3"]
    for i in range(1, 7):
        entradas += ["1", f"Pregunta {i}", "cuerpo"]
    entradas += ["2", "3", "3", "4", "4", "0", "0"]
    salida = _consola(monkeypatch, capsys, entradas)
    assert "Publicación #6 creada." in salida
    primera_linea = next(l for l in salida.splitlines() if l.startswith("  #"))
    assert "Pregunta 6" in primera_linea
    assert "Llegaste al final de la plaza." in salida
    assert "Estás en el principio de la plaza." in salida


# ---------- HU-06: hilos anidados ----------

def test_hu06_hilo_de_tres_niveles_y_padre_inexistente(monkeypatch, capsys):
    """CA-14 a CA-16 por consola, con dos personas."""
    entradas = (
        ["ana_h"] + _publicar("Duda de pilas", "LIFO?")
        + _cambiar("luis_h") + _responder(1, 0, "Sí, LIFO")
        + _cambiar("ana_h") + _responder(1, 1, "Gracias")
        + _cambiar("luis_h") + _responder(1, 2, "De nada")
        + _responder(1, 9, "huérfana")
        + ["0"]
    )
    salida = _consola(monkeypatch, capsys, entradas)
    assert "[0] @ana_h: Duda de pilas — LIFO?" in salida
    assert "\n  [1] @luis_h: Sí, LIFO" in salida
    assert "\n    [2] @ana_h: Gracias" in salida
    assert "\n      [3] @luis_h: De nada" in salida
    assert "no existe en el hilo" in salida
    assert "huérfana" not in salida.split("no existe en el hilo")[-1]


# ---------- HU-10: buscar usuarios y publicaciones ----------

def test_hu10_buscar_usuarios_y_publicaciones(monkeypatch, capsys):
    """CA-27 a CA-29 por consola, sobre la comunidad sembrada."""
    comunidad = generar_comunidad()
    prefijo = comunidad.por_id(0).usuario[:3]
    esperados = [f"  @{p.usuario}" for p in comunidad.buscar_por_prefijo(prefijo)]
    entradas = (
        ["lector_b", "5", prefijo, "5", "zzzz"]
        + ["3", "1", "Grafos en Python", "BFS con cola", "6", "python", "6", "BFS", "6", "árbol", "0", "0"]
    )
    salida = _consola(monkeypatch, capsys, entradas)
    lineas = salida.splitlines()
    posiciones = [lineas.index(e) for e in esperados]
    assert posiciones == sorted(posiciones)              # en orden alfabético
    assert salida.count("Sin coincidencias.") == 2       # zzzz y árbol
    assert salida.count("#1 @lector_b") == 2             # python (título) y BFS (cuerpo)


# ---------- HU-11: volver atrás ----------

def test_hu11_atras_en_orden_inverso_y_sin_historial(monkeypatch, capsys):
    """CA-30 y CA-31 por consola."""
    salida = _consola(monkeypatch, capsys, ["nav_a", "6", "1", "5", "x", "7", "6", "6", "6", "6", "0"])
    estados = [l for l in salida.splitlines() if l.startswith("Estás en:")]
    assert estados == [
        "Estás en: Inicio", "Estás en: Inicio", "Estás en: Mi perfil", "Estás en: Buscar usuarios",
        "Estás en: Notificaciones", "Estás en: Buscar usuarios", "Estás en: Mi perfil",
        "Estás en: Inicio", "Estás en: Inicio",
    ]
    assert salida.count("No hay pantalla previa.") == 2


# ---------- HU-12: notificaciones ----------

def test_hu12_avisos_en_orden_y_sin_pendientes(monkeypatch, capsys):
    """CA-32 y CA-33 por consola: solicitud, aceptada y respuesta, en orden de llegada."""
    entradas = (
        ["ana_n"] + _publicar("Pregunta", "")
        + _cambiar("luis_n") + _enviar("ana_n") + _responder(1, 0, "Respuesta")
        + _cambiar("ana_n") + ["7", "7"] + ACEPTAR_PRIMERA
        + _cambiar("luis_n") + ["7", "0"]
    )
    salida = _consola(monkeypatch, capsys, entradas)
    solicitud = salida.index("@luis_n te envió una solicitud de amistad.")
    respuesta = salida.index("@luis_n respondió a tu publicación «Pregunta».")
    assert solicitud < respuesta
    assert "@ana_n aceptó tu solicitud de amistad." in salida
    assert "Sin notificaciones." in salida


# ---------- HU-13: recomendaciones ----------

def test_hu13_recomendaciones_ordenadas(monkeypatch, capsys):
    """CA-34 a CA-36 por consola: meta tiene 2 amigos en común con ana y beto 1."""
    entradas = ["ana_r"]
    for usuario in ("luis_r", "sara_r", "meta_r", "beto_r"):
        entradas += _cambiar(usuario)
    entradas += _cambiar("ana_r") + ["8"] + _enviar("luis_r") + _enviar("sara_r")
    entradas += _cambiar("luis_r") + ACEPTAR_PRIMERA + _enviar("meta_r") + _enviar("beto_r")
    entradas += _cambiar("sara_r") + ACEPTAR_PRIMERA + _enviar("meta_r")
    entradas += _cambiar("meta_r") + ACEPTAR_PRIMERA + ACEPTAR_PRIMERA
    entradas += _cambiar("beto_r") + ACEPTAR_PRIMERA
    entradas += _cambiar("ana_r") + ["8", "0"]
    salida = _consola(monkeypatch, capsys, entradas)
    assert "No hay recomendaciones por ahora." in salida      # CA-36, antes de tener amigos
    meta = salida.index("@meta_r (2 amigos en común)")
    beto = salida.index("@beto_r (1 amigo en común)")
    assert meta < beto                                       # CA-35
    final = salida[meta:]
    assert "@luis_r (" not in final and "@sara_r (" not in final   # CA-34: sus amigos no


# ---------- RF-02, RF-03, RF-04 y RF-07 ----------

def test_rf02_y_rf07_menu_sin_privados_ni_opciones_should(monkeypatch, capsys):
    """RF-02: no hay mensajes privados. RF-07: no aparecen las opciones Should no implementadas."""
    salida = _consola(monkeypatch, capsys, ["menu_m", "0"]).lower()
    for palabra in ("chat", "mensaje privado", "votar", "destacada", "conectad", "mejor respuesta", "fecha"):
        assert palabra not in salida


def test_rf03_un_rechazo_no_cambia_el_estado(monkeypatch, capsys):
    """RF-03: tras cada rechazo la consola sigue y el estado es el mismo."""
    entradas = (
        ["ana_e"] + ["3", "1", "", "cuerpo", "2", "0"]          # título vacío: plaza sigue vacía
        + _enviar("nadie_e")                                     # destinatario inexistente
        + ["2", "3", "0"]                                        # sigue sin solicitudes
        + ["4", "1", "4", "x"]                                   # hilo inexistente y no número
        + ["1", "0"]
    )
    salida = _consola(monkeypatch, capsys, entradas)
    assert "La publicación necesita un título." in salida
    assert "No hay publicaciones." in salida
    assert "Ese @usuario no existe." in salida
    assert "No tienes solicitudes pendientes." in salida
    assert "Esa publicación no existe." in salida
    assert "Número no válido." in salida
    assert "Tu perfil: @ana_e, 0 puntos." in salida
    assert "Hasta pronto." in salida


def test_rf04_opciones_invalidas_en_todas_las_pantallas(monkeypatch, capsys):
    """RF-04: opción inexistente, texto o línea vacía avisan y repiten el menú."""
    entradas = (
        ["ana_i", "99", "", "texto"]
        + ["2", "9", "0"] + ["3", "9", "0"]
        + _publicar("Una", "") + ["4", "1", "9", "0"]
        + ["0"]
    )
    salida = _consola(monkeypatch, capsys, entradas)
    assert salida.count("Opción no válida.") == 6
    assert "Hasta pronto." in salida


def test_rf04_el_menu_tiene_atras_y_salir(monkeypatch, capsys):
    """RF-04: menú numerado del 1 al 9 y 0, con «Volver atrás»."""
    salida = _consola(monkeypatch, capsys, ["menu_n", "0"])
    for numero, texto in main.OPCIONES_ACTIVAS.items():
        assert f"{numero}. {texto}" in salida
    assert "6. Volver atrás" in salida and "0. Salir" in salida
