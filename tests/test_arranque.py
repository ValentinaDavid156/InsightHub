"""Prueba de arranque del esqueleto.

No verifica un criterio CA: solo comprueba que main.py arranca y sale,
para que `pytest` corra desde la primera entrega. Las pruebas de cada
criterio llegan con sus tareas (ver specs/trazabilidad.md).
"""
import main


def test_menu_muestra_opciones_y_sale(monkeypatch, capsys):
    monkeypatch.setattr("builtins.input", lambda _: "0")
    main.menu()
    salida = capsys.readouterr().out
    assert "=== InsightHub ===" in salida
    assert "Hasta pronto." in salida


def test_opcion_pendiente_avisa_y_vuelve_al_menu(monkeypatch, capsys):
    respuestas = iter(["1", "0"])
    monkeypatch.setattr("builtins.input", lambda _: next(respuestas))
    main.menu()
    assert "aún no implementada" in capsys.readouterr().out


def test_opcion_inexistente_no_falla(monkeypatch, capsys):
    respuestas = iter(["abc", "", "99", "0"])
    monkeypatch.setattr("builtins.input", lambda _: next(respuestas))
    main.menu()
    assert "Hasta pronto." in capsys.readouterr().out
