"""InsightHub — interfaz de consola.

Al arrancar crea los 120 perfiles de ejemplo (semilla 706132), pide el @usuario y muestra el
menú por pantallas (specs/99-sistema/spec.md). Hoy funcionan: entrar, mi perfil, buscar usuarios
y «Volver atrás»; las demás pantallas se abren, quedan en el historial y avisan que están pendientes.
"""

from dominio.navegacion import MENSAJE_SIN_PANTALLA_PREVIA, Navegacion
from dominio.usuarios import UsuarioInvalidoError, generar_comunidad

PANTALLAS = {
    "2": "Amigos y solicitudes",
    "3": "Plaza: publicar y recorrer",
    "4": "Responder en hilos",
    "7": "Notificaciones",
    "8": "Personas que quizá conozcas",
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


OPCIONES_ACTIVAS = {"1": "Mi perfil", "5": "Buscar usuarios", "6": "Volver atrás"}


def mostrar_menu(nav) -> None:
    print("\n=== InsightHub ===")
    print(f"Estás en: {nav.actual}")
    for numero in "12345678":                # siempre en orden numérico
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


def menu(catalogo=None) -> None:
    if catalogo is None:
        catalogo = generar_comunidad()
    perfil = pedir_usuario(catalogo)
    if perfil is None:
        print("Hasta pronto.")
        return
    nav = Navegacion()
    nav.ir_a("Inicio")
    while True:
        mostrar_menu(nav)
        try:
            eleccion = input("Opción: ").strip()
        except EOFError:
            print("Hasta pronto.")
            return
        if eleccion == "0":
            print("Hasta pronto.")
            return
        if eleccion == "1":
            nav.ir_a("Mi perfil")
            print(f"Tu perfil: @{perfil.usuario}, {perfil.puntos} puntos.")
        elif eleccion == "5":
            nav.ir_a("Buscar usuarios")
            buscar_usuarios(catalogo)
        elif eleccion == "6":
            if nav.atras() is None:
                print(MENSAJE_SIN_PANTALLA_PREVIA)
        elif eleccion in PANTALLAS:
            nav.ir_a(PANTALLAS[eleccion])
            print("Funcionalidad aún no implementada.")
        else:
            print("Opción no válida.")


if __name__ == "__main__":
    menu()
