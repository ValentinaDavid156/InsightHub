# Búsquedas de publicaciones.
# Spec: specs/01-lista-doble/spec.md (RF-08, CA-29) · Plan: specs/01-lista-doble/plan.md
# La búsqueda por palabra vive aquí y recorre la plaza (decisión de Valentina): la lista doble
# queda genérica y no sabe qué es un título o un cuerpo. La búsqueda por fecha (CA-39) llega con el AVL.


def buscar_palabra(plaza, texto):
    """Publicaciones cuyo título o cuerpo contienen `texto`, de la más nueva a la más antigua.

    Sin distinguir mayúsculas y aceptando coincidencias dentro de otra palabra
    («python» encuentra «Pythonista»). Un texto vacío o solo de espacios devuelve [].
    Complejidad: O(n·m), con n publicaciones y m el largo del texto. No modifica la plaza.
    """
    buscado = texto.strip().lower()
    if not buscado:
        return []
    encontradas = []
    for publicacion in plaza:
        if buscado in publicacion.titulo.lower() or buscado in publicacion.cuerpo.lower():
            encontradas.append(publicacion)
    return encontradas
