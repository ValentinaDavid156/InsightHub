# «Personas que quizá conozcas»: el grafo da los candidatos y el montículo los ordena.
# Specs: specs/06-grafo/spec.md (CA-34, CA-36) · specs/07-monticulo/spec.md (CA-35)
# Plan: specs/07-monticulo/plan.md §6

from estructuras.monticulo import Monticulo

LIMITE = 5


def _antes(a, b):
    """a = (perfil, comunes). Más amigos en común primero; si empatan, @usuario menor."""
    if a[1] != b[1]:
        return a[1] > b[1]
    return a[0].usuario < b[0].usuario


def recomendar(amistades, persona, limite=LIMITE):
    """Hasta `limite` (perfil, amigos_en_comun), de más a menos amigos en común (CA-35).

    Sin amigos, o persona inexistente: lista vacía (CA-36). No modifica la red.
    Complejidad: O(V + g + E') para los candidatos, O(m) para construir y O(5 log m) para sacar.
    """
    candidatos = amistades.grafo.candidatos_dos_saltos(persona)
    monticulo = Monticulo(_antes)
    monticulo.construir([(amistades.catalogo.por_id(i), comunes) for i, comunes in candidatos])
    elegidos = []
    while not monticulo.esta_vacio() and len(elegidos) < limite:
        elegidos.append(monticulo.extraer_maximo())
    return elegidos
