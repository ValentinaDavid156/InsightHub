"""Mediciones de ANALISIS.md: cada decisión contra la alternativa descartada, con n creciente.

Mismo método que Semana4/medicion.py: mediana de varias repeticiones.
Se ejecuta desde la raíz del repositorio:  python docs/evidencias/medir.py
Escribe docs/evidencias/mediciones.csv e imprime las tablas.
"""

import csv
import functools
import random
import statistics
import sys
import time
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ))

from estructuras.avl import AVL                     # noqa: E402
from estructuras.lista_doble import ListaDoble      # noqa: E402
from estructuras.monticulo import Monticulo         # noqa: E402

REPETICIONES = 7                    # como Semana4/medicion.py
SEMILLA = 706132


def mediana_ms(operacion):
    """Mediana, en milisegundos, de REPETICIONES ejecuciones de `operacion`."""
    tiempos = []
    for _ in range(REPETICIONES):
        inicio = time.perf_counter()
        operacion()
        tiempos.append((time.perf_counter() - inicio) * 1000)
    return statistics.median(tiempos)


# ---------- 1. AVL frente a árbol de búsqueda sin equilibrar (claves ya ordenadas) ----------

class _NodoSinEquilibrar:
    __slots__ = ("clave", "izquierdo", "derecho")

    def __init__(self, clave):
        self.clave = clave
        self.izquierdo = None
        self.derecho = None


class ArbolSinEquilibrar:
    """La alternativa descartada: inserta como el AVL pero sin rotaciones (sin recursión)."""

    def __init__(self):
        self.raiz = None

    def insertar(self, clave):
        nuevo = _NodoSinEquilibrar(clave)
        if self.raiz is None:
            self.raiz = nuevo
            return
        actual = self.raiz
        while True:
            if clave < actual.clave:
                if actual.izquierdo is None:
                    actual.izquierdo = nuevo
                    return
                actual = actual.izquierdo
            else:
                if actual.derecho is None:
                    actual.derecho = nuevo
                    return
                actual = actual.derecho

    def buscar(self, clave):
        actual = self.raiz
        while actual is not None and actual.clave != clave:
            actual = actual.izquierdo if clave < actual.clave else actual.derecho
        return actual

    def altura(self):
        altura, actual = -1, self.raiz
        while actual is not None:           # con claves ordenadas es una sola rama
            altura += 1
            actual = actual.derecho
        return altura


def comparar_arboles():
    filas = []
    for n in (1_000, 2_000, 4_000, 8_000):
        claves = [f"u{i:06d}" for i in range(n)]    # llegan ordenadas, como en el peor caso

        def llenar_avl():
            arbol = AVL()
            for clave in claves:
                arbol.insertar(clave, clave)
            return arbol

        def llenar_otro():
            arbol = ArbolSinEquilibrar()
            for clave in claves:
                arbol.insertar(clave)
            return arbol

        avl, otro = llenar_avl(), llenar_otro()
        ultima = claves[-1]

        def buscar_avl():
            for _ in range(1000):
                avl.buscar(ultima)

        def buscar_otro():
            for _ in range(1000):
                otro.buscar(ultima)

        filas.append({
            "comparacion": "arbol", "n": n,
            "avl_insertar_todo_ms": round(mediana_ms(llenar_avl), 2),
            "sin_equilibrar_insertar_todo_ms": round(mediana_ms(llenar_otro), 2),
            "avl_buscar_us": round(mediana_ms(buscar_avl), 3),
            "sin_equilibrar_buscar_us": round(mediana_ms(buscar_otro), 3),
            "avl_altura": avl.altura(),
            "sin_equilibrar_altura": otro.altura(),
        })
    return filas


# ---------- 2. Lista doble frente a arreglo de Python (publicar al frente) ----------

def comparar_plaza():
    filas = []
    publicaciones = 1_000
    for n in (1_000, 10_000, 100_000, 400_000):
        def en_lista_doble():
            lista = ListaDoble()
            for i in range(n):
                lista.insertar_al_frente(i)
            return lista

        def en_arreglo():
            return list(range(n))

        lista = en_lista_doble()
        arreglo = en_arreglo()

        def publicar_doble():
            for i in range(publicaciones):
                lista.insertar_al_frente(i)

        def publicar_arreglo():
            for i in range(publicaciones):
                arreglo.insert(0, i)

        filas.append({
            "comparacion": "plaza", "n": n,
            "lista_doble_por_publicacion_us": round(mediana_ms(publicar_doble) / publicaciones * 1000, 3),
            "arreglo_por_publicacion_us": round(mediana_ms(publicar_arreglo) / publicaciones * 1000, 3),
        })
    return filas


# ---------- 3. Montículo frente a ordenar todos los candidatos (5 mejores de m) ----------

def comparar_recomendaciones():
    filas = []
    azar = random.Random(SEMILLA)
    for m in (1_000, 10_000, 100_000):
        candidatos = [(azar.randint(1, 50), azar.randint(0, 10**9)) for _ in range(m)]
        cuenta = [0]

        def antes(a, b):
            cuenta[0] += 1
            return a[0] > b[0] or (a[0] == b[0] and a[1] < b[1])

        def con_monticulo():
            monticulo = Monticulo(antes)
            monticulo.construir(candidatos)
            return [monticulo.extraer_maximo() for _ in range(5)]

        def comparador(a, b):
            return -1 if antes(a, b) else 1

        def ordenando():
            return sorted(candidatos, key=functools.cmp_to_key(comparador))[:5]

        assert con_monticulo() == ordenando()       # las dos dan el mismo resultado
        cuenta[0] = 0
        con_monticulo()
        comparaciones_monticulo = cuenta[0]
        cuenta[0] = 0
        ordenando()
        comparaciones_ordenar = cuenta[0]
        filas.append({
            "comparacion": "recomendaciones", "n": m,
            "monticulo_ms": round(mediana_ms(con_monticulo), 2),
            "ordenar_ms": round(mediana_ms(ordenando), 2),
            "monticulo_comparaciones": comparaciones_monticulo,
            "ordenar_comparaciones": comparaciones_ordenar,
        })
    return filas


def main():
    grupos = [comparar_arboles(), comparar_plaza(), comparar_recomendaciones()]
    salida = RAIZ / "docs" / "evidencias" / "mediciones.csv"
    with open(salida, "w", newline="", encoding="utf-8") as archivo:
        escritor = csv.writer(archivo)
        for filas in grupos:
            escritor.writerow(filas[0].keys())
            for fila in filas:
                escritor.writerow(fila.values())
            escritor.writerow([])
    for filas in grupos:
        for fila in filas:
            print(fila)
    print("Python", sys.version.split()[0], "· repeticiones:", REPETICIONES, "· archivo:", salida.name)


if __name__ == "__main__":
    main()
