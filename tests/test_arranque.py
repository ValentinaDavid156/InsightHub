"""Pruebas de arranque de la consola.

No verifican un criterio CA propio: comprueban que main.py arranca, sale y
conecta «atrás» con la pila (integración de CA-30 y CA-31 en la consola).
"""
import main


def _ejecutar(monkeypatch, capsys, respuestas):
    entradas = iter(respuestas)
    monkeypatch.setattr("builtins.input", lambda _: next(entradas))
    main.menu()
    return capsys.readouterr().out


def test_menu_muestra_opciones_y_sale(monkeypatch, capsys):
    salida = _ejecutar(monkeypatch, capsys, ["0"])
    assert "=== InsightHub ===" in salida
    assert "Estás en: Inicio" in salida
    assert "Hasta pronto." in salida


def test_opcion_pendiente_avisa_y_vuelve_al_menu(monkeypatch, capsys):
    salida = _ejecutar(monkeypatch, capsys, ["1", "0"])
    assert "aún no implementada" in salida
    assert "Estás en: Entrar con mi @usuario" in salida


def test_opcion_inexistente_no_falla(monkeypatch, capsys):
    salida = _ejecutar(monkeypatch, capsys, ["abc", "", "99", "0"])
    assert salida.count("Opción no válida.") == 3
    assert "Hasta pronto." in salida


def test_atras_en_inicio_informa_que_no_hay_pantalla_previa(monkeypatch, capsys):
    """CA-31 integrado: «atrás» sin historial informa y el menú sigue."""
    salida = _ejecutar(monkeypatch, capsys, ["6", "0"])
    assert "No hay pantalla previa." in salida


def test_atras_vuelve_a_la_pantalla_anterior(monkeypatch, capsys):
    """CA-30 integrado: abrir pantallas y volver atrás en orden inverso."""
    salida = _ejecutar(monkeypatch, capsys, ["3", "5", "6", "6", "0"])
    estados = [l for l in salida.splitlines() if l.startswith("Estás en:")]
    assert estados == [
        "Estás en: Inicio",
        "Estás en: Plaza: publicar y recorrer",
        "Estás en: Buscar usuarios y publicaciones",
        "Estás en: Plaza: publicar y recorrer",
        "Estás en: Inicio",
    ]
