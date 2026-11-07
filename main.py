"""InsightHub — interfaz de consola (versión inicial).

Los menús se completan a medida que se implementa cada componente
(ver specs/99-sistema/spec.md). Hoy solo funciona «Volver atrás» (pila);
las demás pantallas se abren, quedan en el historial y avisan que están pendientes.
"""

from dominio.navegacion import MENSAJE_SIN_PANTALLA_PREVIA, Navegacion

PANTALLAS = {
    "1": "Entrar con mi @usuario",
    "2": "Amigos y solicitudes",
    "3": "Plaza: publicar y recorrer",
    "4": "Responder en hilos",
    "5": "Buscar usuarios y publicaciones",
    "7": "Notificaciones",
    "8": "Personas que quizá conozcas",
}


def mostrar_menu(nav: Navegacion) -> None:
    print("\n=== InsightHub ===")
    print(f"Estás en: {nav.actual}")
    for numero, nombre in PANTALLAS.items():
        print(f"{numero}. {nombre} (pendiente)")
    print("6. Volver atrás")
    print("0. Salir")


def menu() -> None:
    nav = Navegacion()
    nav.ir_a("Inicio")
    while True:
        mostrar_menu(nav)
        eleccion = input("Opción: ").strip()
        if eleccion == "0":
            print("Hasta pronto.")
            return
        if eleccion == "6":
            if nav.atras() is None:
                print(MENSAJE_SIN_PANTALLA_PREVIA)
        elif eleccion in PANTALLAS:
            nav.ir_a(PANTALLAS[eleccion])
            print("Funcionalidad aún no implementada.")
        else:
            print("Opción no válida.")


if __name__ == "__main__":
    menu()
