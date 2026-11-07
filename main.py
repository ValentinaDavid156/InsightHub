"""InsightHub — interfaz de consola (versión inicial).

Los menús se completan a medida que se implementa cada componente
(ver specs/99-sistema/spec.md). Hoy ninguna opción está implementada.
"""

OPCIONES = [
    "1. Entrar con mi @usuario (pendiente)",
    "2. Amigos y solicitudes (pendiente)",
    "3. Plaza: publicar y recorrer (pendiente)",
    "4. Responder en hilos (pendiente)",
    "5. Buscar usuarios y publicaciones (pendiente)",
    "6. Volver atrás (pendiente)",
    "7. Notificaciones (pendiente)",
    "8. Personas que quizá conozcas (pendiente)",
    "0. Salir",
]


def menu() -> None:
    while True:
        print("\n=== InsightHub ===")
        print("\n".join(OPCIONES))
        eleccion = input("Opción: ").strip()
        if eleccion == "0":
            print("Hasta pronto.")
            return
        print("Funcionalidad aún no implementada.")


if __name__ == "__main__":
    menu()
