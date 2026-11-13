"""InsightHub — interfaz de consola.

Al arrancar crea los 120 perfiles de ejemplo (semilla 706132), pide el @usuario y muestra el
menú por pantallas (specs/99-sistema/spec.md). Hoy funcionan: entrar, cambiar de @usuario, mi
perfil, amigos y solicitudes, plaza, hilos, buscar usuarios, notificaciones, «Volver atrás» y
recomendaciones; ya no queda ninguna pantalla Must pendiente.
"""

from dominio.amistades import Amistades, MENSAJE_SIN_SOLICITUDES, SolicitudInvalidaError
from dominio.busqueda import buscar_palabra
from dominio.feed import Plaza, PublicacionInvalidaError
from dominio.hilos import Hilos
from dominio.navegacion import MENSAJE_SIN_PANTALLA_PREVIA, Navegacion
from dominio.notificaciones import MENSAJE_SIN_NOTIFICACIONES
from dominio.recomendaciones import recomendar
from dominio.usuarios import UsuarioInvalidoError, generar_comunidad
from estructuras.arbol_general import RespuestaInvalidaError

OPCIONES_ACTIVAS = {
    "1": "Mi perfil",
    "2": "Amigos y solicitudes",
    "3": "Plaza: publicar y recorrer",
    "4": "Responder en hilos",
    "5": "Buscar usuarios",
    "6": "Volver atrás",
    "7": "Notificaciones",
    "8": "Personas que quizá conozcas",
    "9": "Cambiar de @usuario",
}


def pedir_usuario(catalogo):
    """Pide el @usuario hasta que sea válido. Devuelve el perfil, o None si se cierra la entrada."""
    while True:
        try:
            texto = input("@usuario: ").strip()
        except EOFError:
            return None
        try:
            perfil, creado = catalogo.entrar(texto)
        except UsuarioInvalidoError as error:
            print(error)
            continue
        if creado:
            print("Perfil creado.")
        print(f"Hola, @{perfil.usuario}.")
        return perfil


def mostrar_menu(nav) -> None:
    print("\n=== InsightHub ===")
    print(f"Estás en: {nav.actual}")
    for numero in "123456789":               # siempre en orden numérico
        print(f"{numero}. {OPCIONES_ACTIVAS[numero]}")
    print("0. Salir")


def buscar_usuarios(catalogo) -> None:
    prefijo = input("Prefijo del @usuario: ").strip()
    encontrados = catalogo.buscar_por_prefijo(prefijo)
    if not encontrados:
        print("Sin coincidencias.")
    for perfil in encontrados:
        print(f"  @{perfil.usuario}")
    exacto = catalogo.buscar(prefijo)
    if exacto is not None:
        print(f"Perfil de @{exacto.usuario}: {exacto.puntos} puntos.")


def ver_amigos(amistades, perfil) -> None:
    amigos = amistades.amigos(perfil.id)
    if not amigos:
        print("Aún no tienes amigos.")
    for amigo in amigos:
        print(f"  @{amigo.usuario}")


def enviar_solicitud(amistades, perfil) -> None:
    usuario = input("Enviar solicitud a @usuario: ").strip()
    try:
        destino = amistades.enviar(perfil.id, usuario)
    except SolicitudInvalidaError as error:
        print(error)
        return
    print(f"Solicitud enviada a @{destino.usuario}.")


def revisar_solicitudes(amistades, perfil) -> None:
    """Muestra solo la primera solicitud pendiente y espera la decisión (CA-07)."""
    remitente = amistades.primera(perfil.id)
    if remitente is None:
        print(MENSAJE_SIN_SOLICITUDES)
        return
    print(f"Solicitud de @{remitente.usuario}")
    print("1. Aceptar")
    print("2. Rechazar")
    print("0. Dejarla pendiente")
    while True:
        decision = input("Opción: ").strip()
        if decision == "0":
            return
        if decision == "1":
            amistades.atender(perfil.id, aceptar=True)
            print(f"Ahora eres amigo de @{remitente.usuario}.")
            return
        if decision == "2":
            amistades.atender(perfil.id, aceptar=False)
            print(f"Rechazaste la solicitud de @{remitente.usuario}.")
            return
        print("Opción no válida.")


def deshacer_amistad(amistades, perfil) -> None:
    usuario = input("Deshacer amistad con @usuario: ").strip().lstrip("@").lower()
    if amistades.deshacer(perfil.id, usuario):
        print(f"Ya no eres amigo de @{usuario}.")
    else:
        print(f"No eres amigo de @{usuario}.")


def pantalla_amigos(amistades, perfil, nav) -> None:
    """Submenú de amigos y solicitudes; su 0 es «atrás»."""
    acciones = {
        "1": ver_amigos,
        "2": enviar_solicitud,
        "3": revisar_solicitudes,
        "4": deshacer_amistad,
    }
    while True:
        print("\n--- Amigos y solicitudes ---")
        print(f"Solicitudes pendientes: {amistades.pendientes(perfil.id)}")
        print("1. Ver amigos")
        print("2. Enviar solicitud")
        print("3. Revisar solicitudes")
        print("4. Deshacer amistad")
        print("0. Volver atrás")
        eleccion = input("Opción: ").strip()
        if eleccion == "0":
            nav.atras()
            return
        if eleccion in acciones:
            acciones[eleccion](amistades, perfil)
        else:
            print("Opción no válida.")


def leer_notificaciones(amistades, perfil) -> None:
    avisos = amistades.notificaciones.leer(perfil.id)
    if not avisos:
        print(MENSAJE_SIN_NOTIFICACIONES)
    for aviso in avisos:
        print(f"  {aviso}")


def _mostrar_publicaciones(publicaciones) -> None:
    for publicacion in publicaciones:
        print(f"  #{publicacion.id} @{publicacion.autor} ({publicacion.fecha}): {publicacion.titulo}")


def _mostrar_pagina(resultado) -> None:
    pagina, aviso = resultado
    _mostrar_publicaciones(pagina)
    if aviso:
        print(aviso)


def publicar(hilos, perfil) -> None:
    titulo = input("Título: ").strip()
    cuerpo = input("Cuerpo: ").strip()
    try:
        publicacion = hilos.publicar(perfil.usuario, titulo, cuerpo)
    except PublicacionInvalidaError as error:
        print(error)
        return
    print(f"Publicación #{publicacion.id} creada.")


def buscar_en_plaza(hilos) -> None:
    encontradas = buscar_palabra(hilos.plaza, input("Palabra: "))
    if not encontradas:
        print("Sin coincidencias.")
    _mostrar_publicaciones(encontradas)


def pantalla_plaza(hilos, perfil, nav) -> None:
    """Submenú de la plaza, con la posición propia de cada persona; su 0 es «atrás»."""
    sesion = hilos.sesion_de(perfil.id)
    while True:
        print("\n--- Plaza ---")
        print("1. Publicar")
        print("2. Ver página actual")
        print("3. Página siguiente")
        print("4. Página anterior")
        print("5. Volver al inicio de la plaza")
        print("6. Buscar por palabra")
        print("0. Volver atrás")
        eleccion = input("Opción: ").strip()
        if eleccion == "0":
            nav.atras()
            return
        if eleccion == "1":
            publicar(hilos, perfil)
        elif eleccion == "2":
            _mostrar_pagina(sesion.ver())
        elif eleccion == "3":
            _mostrar_pagina(sesion.siguiente())
        elif eleccion == "4":
            _mostrar_pagina(sesion.anterior())
        elif eleccion == "5":
            _mostrar_pagina(sesion.inicio())
        elif eleccion == "6":
            buscar_en_plaza(hilos)
        else:
            print("Opción no válida.")


def _leer_numero(mensaje):
    """Pide un número entero; devuelve None, avisando, si lo escrito no lo es."""
    texto = input(mensaje).strip()
    if texto.isascii() and texto.isdigit():
        return int(texto)
    print("Número no válido.")
    return None


def responder_en_hilo(hilos, perfil, id_publicacion) -> None:
    id_padre = _leer_numero("Responder al número (0 = la publicación): ")
    if id_padre is None:
        return
    texto = input("Respuesta: ").strip()
    try:
        hilos.responder(id_publicacion, id_padre, perfil.usuario, texto)
    except RespuestaInvalidaError as error:
        print(error)


def pantalla_hilo(hilos, perfil, nav) -> None:
    """Abre el hilo de una publicación y permite responder; su 0 es «atrás»."""
    id_publicacion = _leer_numero("Número de la publicación: ")
    if id_publicacion is None:
        nav.atras()
        return
    if not hilos.existe(id_publicacion):
        print("Esa publicación no existe.")
        nav.atras()
        return
    while True:
        print(f"\n--- Hilo #{id_publicacion} ---")
        for linea in hilos.mostrar(id_publicacion):
            print(linea)
        print("1. Responder")
        print("0. Volver atrás")
        eleccion = input("Opción: ").strip()
        if eleccion == "0":
            nav.atras()
            return
        if eleccion == "1":
            responder_en_hilo(hilos, perfil, id_publicacion)
        else:
            print("Opción no válida.")


def ver_recomendaciones(amistades, perfil) -> None:
    """Hasta 5 personas, de más a menos amigos en común (CA-35)."""
    recomendaciones = recomendar(amistades, perfil.id)
    if not recomendaciones:
        print("No hay recomendaciones por ahora.")
    for recomendado, comunes in recomendaciones:
        palabra = "amigo" if comunes == 1 else "amigos"
        print(f"  @{recomendado.usuario} ({comunes} {palabra} en común)")


def _abrir_sesion(catalogo, amistades):
    """Pide el @usuario y prepara su historial. Devuelve (perfil, nav), o (None, None) con EOF."""
    perfil = pedir_usuario(catalogo)
    if perfil is None:
        return None, None
    amistades.registrar(perfil.id)
    nav = Navegacion()                       # cada sesión tiene su propio «atrás»
    nav.ir_a("Inicio")
    return perfil, nav


def _ciclo(catalogo, amistades, hilos) -> None:
    perfil, nav = _abrir_sesion(catalogo, amistades)
    if perfil is None:
        return
    while True:
        mostrar_menu(nav)
        eleccion = input("Opción: ").strip()
        if eleccion == "0":
            return
        if eleccion == "1":
            nav.ir_a("Mi perfil")
            print(f"Tu perfil: @{perfil.usuario}, {perfil.puntos} puntos.")
        elif eleccion == "2":
            nav.ir_a("Amigos y solicitudes")
            pantalla_amigos(amistades, perfil, nav)
        elif eleccion == "3":
            nav.ir_a("Plaza: publicar y recorrer")
            pantalla_plaza(hilos, perfil, nav)
        elif eleccion == "4":
            nav.ir_a("Responder en hilos")
            pantalla_hilo(hilos, perfil, nav)
        elif eleccion == "5":
            nav.ir_a("Buscar usuarios")
            buscar_usuarios(catalogo)
        elif eleccion == "6":
            if nav.atras() is None:
                print(MENSAJE_SIN_PANTALLA_PREVIA)
        elif eleccion == "7":
            nav.ir_a("Notificaciones")
            leer_notificaciones(amistades, perfil)
        elif eleccion == "8":
            nav.ir_a("Personas que quizá conozcas")
            ver_recomendaciones(amistades, perfil)
        elif eleccion == "9":
            perfil, nav = _abrir_sesion(catalogo, amistades)
            if perfil is None:
                return
        else:
            print("Opción no válida.")


def menu(catalogo=None) -> None:
    if catalogo is None:
        catalogo = generar_comunidad()
    amistades = Amistades(catalogo)
    hilos = Hilos(Plaza(), catalogo, amistades.notificaciones)
    try:
        _ciclo(catalogo, amistades, hilos)
    except EOFError:                        # se cerró la entrada en cualquier pantalla
        pass
    print("Hasta pronto.")


if __name__ == "__main__":
    menu()
