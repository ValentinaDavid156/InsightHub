# InsightHub
> Red social - Plataforma interactiva de preguntas y respuestas comunitarias orientada a la discusión pública.
>
> ## 1. Temática del proyecto
> **InsightHub** es una red social orientada al intercambio de conocimientos, preguntas y respuestas en un entorno público y estructurado. El sistema permite a los usuarios plantear interrogantes, debatir sobre temas de interés común y calificar la relevancia de las intervenciones.
>
> ## 2. Contexto Narrativo
> Inspirada en el concepto histórico del *Ágora* (el centro de la vida pública y del debate ciudadano), esta plataforma busca recrear un espacio virtual donde cualquier usuario pueda plantear dudas y recibir respuestas fundamentadas de la comunidad, cada publicación funciona como un hilo de discusión interactivo en el que los participantes pueden interactuar, categorizar consultas por temáticas y destacar los aportes más valiosos mediante un sistema de calificación.

## 3. Cómo instalar y ejecutar
Requiere Python 3.11 o superior. Sin dependencias externas salvo `pytest` (y, opcionalmente, `matplotlib`).

```bash
git clone https://github.com/ValentinaDavid156/InsightHub
cd InsightHub
python -m pip install pytest
python main.py
python -m pytest
```

Estado: el repositorio contiene las especificaciones (`specs/`) y el esqueleto; las estructuras se implementan a partir de `specs/*/tasks.md`.

## 4. Estructura
- `specs/`: constitución, producto (historias, MoSCoW, estructuras), un componente por carpeta y `99-sistema/`.
- `estructuras/`: un módulo por estructura.
- `dominio/`: la lógica de la temática.
- `tests/`: pruebas con pytest.
- `docs/`: informe final y evidencias.
