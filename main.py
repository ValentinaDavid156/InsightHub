"""InsightHub — interfaz de consola (versión inicial)."""


def menu() -> None:
    opciones = [
        "1. Generar usuarios (pendiente)",
        "2. Seguir / dejar de seguir (pendiente)",
        "3. Publicar y ver feed (pendiente)",
        "4. Responder en hilos (pendiente)",
        "5. Buscar (pendiente)",
        "6. Volver atrás (pendiente)",
        "7. Notificaciones (pendiente)",
        "8. Recomendaciones (pendiente)",
        "0. Salir",
    ]
    while True:
        print("\n=== InsightHub ===")
        print("\n".join(opciones))
        eleccion = input("Opción: ").strip()
        if eleccion == "0":
            print("Hasta pronto.")
            return
        print("Funcionalidad aún no implementada.")


if __name__ == "__main__":
    menu()
