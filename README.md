# InsightHub
> Red social - Plataforma interactiva de preguntas y respuestas comunitarias orientada a la discusión pública.
>
> ## 1. Temática del proyecto
> **InsightHub** es una red social orientada al intercambio de conocimientos, preguntas y respuestas en un entorno público y estructurado. El sistema permite a los usuarios plantear interrogantes, debatir sobre temas de interés común y calificar la relevancia de las intervenciones.
>
> ## 2. Contexto Narrativo
> Inspirada en el concepto histórico del *Ágora* (el centro de la vida pública y del debate ciudadano), esta plataforma busca recrear un espacio virtual donde cualquier usuario pueda plantear dudas y recibir respuestas fundamentadas de la comunidad, cada publicación funciona como un hilo de discusión interactivo en el que los participantes pueden interactuar, categorizar consultas por temáticas y destacar los aportes más valiosos mediante un sistema de calificación.

## 3. Cómo instalar y ejecutar
Requiere Python 3.11 o superior y Git. La aplicación usa solo la biblioteca estándar de Python; las pruebas necesitan `pytest`.

```bash
git clone https://github.com/ValentinaDavid156/InsightHub
cd InsightHub
python -m pip install pytest
python main.py
```

Para correr las pruebas, desde la carpeta `InsightHub`:

```bash
python -m pytest
```

Para repetir las mediciones de `ANALISIS.md` (tarda unos minutos y reescribe `docs/evidencias/mediciones.csv`):

```bash
python docs/evidencias/medir.py
```

## 4. Cómo usar la consola
Al arrancar, la comunidad tiene 120 perfiles de ejemplo (semilla `706132`). Escribe un `@usuario` de 3 a 20 caracteres (letras, números y guión bajo): si no existe, se crea. Los datos viven en memoria y se pierden al salir.

| Opción | Qué hace |
|---|---|
| 1 | Ver mi perfil |
| 2 | Amigos y solicitudes: ver amigos, enviar, revisar y deshacer |
| 3 | Plaza: publicar, recorrer de 5 en 5 y buscar por palabra |
| 4 | Hilos: escribir el número de una publicación, ver el hilo y responder (0 = la publicación) |
| 5 | Buscar usuarios por prefijo |
| 6 | Volver atrás |
| 7 | Leer notificaciones |
| 8 | Personas que quizá conozcas |
| 9 | Cambiar de `@usuario` sin borrar los datos |
| 0 | Salir |

Para probar una amistad: entra con una persona, cambia con la opción 9 a otra, envía la solicitud, vuelve con la 9 a la primera y acéptala en la opción 2.

## 5. Estado
Están implementadas todas las historias Must, con siete de las ocho estructuras declaradas: lista doble, pila, cola, árbol general, AVL, grafo y montículo. No se implementaron las historias Should: votos, mejor respuesta, publicación destacada, conectados (y con ella la lista simple), búsqueda por fecha y sitio web. Ver [`moscow.md`](specs/00-producto/moscow.md) y [`trazabilidad.md`](specs/trazabilidad.md).

## 6. Estructura
- `specs/`: constitución, producto (historias, MoSCoW, estructuras), un componente por carpeta y `99-sistema/`.
- `estructuras/`: un módulo por estructura.
- `dominio/`: la lógica de la temática.
- `main.py`: la consola.
- `tests/`: pruebas con pytest.
- `docs/`: informe final y evidencias (mediciones).
- `ANALISIS.md`: complejidad y comparaciones. `BITACORA.md`: uso de IA, prompt por prompt.
