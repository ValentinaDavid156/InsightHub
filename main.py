"""InsightHub — interfaz de consola.

Al arrancar crea los 120 perfiles de ejemplo (semilla 706132), pide el @usuario y muestra el
menú por pantallas (specs/99-sistema/spec.md). Hoy funcionan: entrar, cambiar de @usuario, mi
perfil, amigos y solicitudes, buscar usuarios, notificaciones y «Volver atrás»; las demás
pantallas se abren, quedan en el historial y avisan que están pendientes.
"""

from dominio.amistades import Amistades, MENSAJE_SIN_SOLICITUDES, SolicitudInvalidaError
from dominio.navegacion import MENSAJE_SIN_PANTALLA_PREVIA, Navegacion
from dominio.notificaciones import MENSAJE_SIN_NOTIFICACIONES
from dominio.usuarios import UsuarioInvalidoError, generar_comunidad

PANTALLAS = {
    "3": "Plaza: publicar y recorrer",
    "4": "Responder en hilos",
    "8": "Personas que quizá conozcas",
}

OPCIONES_ACTIVAS = {
    "1": "Mi perfil",
    "2": "Amigos y solicitudes",
    "5": "Buscar usuarios",
    "6": "Volver atrás",
    "7": "Notificaciones",
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
        if numero in PANTALLAS:
            print(f"{numero}. {PANTALLAS[numero]} (pendiente)")
        else:
            print(f"{numero}. {OPCIONES_ACTIVAS[numero]}")
    print("0. Salir")


def buscar_usuarios(catalogo) -> None:
    prefijo = input("Prefijo del @usuario: ").strip()
    encontrados = catalogo.buscar_por_prefijo(prefijo)
    if not encontrados:
        print("Sin coincidencias.")
    for perfil in encontrados:
        print(f"  @{perfil.usuario}")


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


def _abrir_sesion(catalogo, amistades):
    """Pide el @usuario y prepara su historial. Devuelve (perfil, nav), o (None, None) con EOF."""
    perfil = pedir_usuario(catalogo)
    if perfil is None:
        return None, None
    amistades.registrar(perfil.id)
    nav = Navegacion()                       # cada sesión tiene su propio «atrás»
    nav.ir_a("Inicio")
    return perfil, nav


def _ciclo(catalogo, amistades) -> None:
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
        elif eleccion == "5":
            nav.ir_a("Buscar usuarios")
            buscar_usuarios(catalogo)
        elif eleccion == "6":
            if nav.atras() is None:
                print(MENSAJE_SIN_PANTALLA_PREVIA)
        elif eleccion == "7":
            nav.ir_a("Notificaciones")
            leer_notificaciones(amistades, perfil)
        elif eleccion == "9":
            perfil, nav = _abrir_sesion(catalogo, amistades)
            if perfil is None:
                return
        elif eleccion in PANTALLAS:
            nav.ir_a(PANTALLAS[eleccion])
            print("Funcionalidad aún no implementada.")
        else:
            print("Opción no válida.")


def menu(catalogo=None) -> None:
    if catalogo is None:
        catalogo = generar_comunidad()
    try:
        _ciclo(catalogo, Amistades(catalogo))
    except EOFError:                         # se cerró la entrada en cualquier pantalla
        pass
    print("Hasta pronto.")


if __name__ == "__main__":
    menu()
