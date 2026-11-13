# Bitácora de interacción con la IA — InsightHub

> Registro exigido por el Principio 8 de la [Constitución](specs/CONSTITUTION.md): prompt textual, síntesis de la respuesta y decisión de la estudiante.
> Herramienta: Claude Code (Anthropic). Fechas de las sesiones: 2026-11-07 a 2026-11-10.
> Alcance de la IA: asistente bajo la dirección de la estudiante. La estudiante definió la temática, las historias de usuario, las estructuras y las reglas del dominio, y tomó cada decisión de diseño respondiendo preguntas con opciones y una recomendación. En las sesiones 1 a 15, con esas decisiones, la IA redactó y completó los documentos (`specs/`, `moscow.md`, esta bitácora). Desde la sesión 16, por decisión de la estudiante, la IA partió de su código del curso (`Estructura-datos/`, Semanas 4 a 10: nodo, pila, cola, lista doble y árbol), lo adaptó e integró, y escribió las estructuras sin antecedente en el curso (AVL, grafo y montículo) y las pruebas. La estudiante recibió el detalle de cada cambio y aprobó cada commit.

---

## Sesión 1 — Encargo y preparación del repositorio

**Prompt (textual):**
> trabaja en esta carpeta con base a lo pedido de C:\Users\Valentina\OneDrive\Desktop\Estructuras_datos
>
> [Se pegó el contenido de `PROMPT_ClaudeCode.md`: rol de asistente de Spec-Driven Development, carpeta de trabajo, ocho reglas, lista de tareas A a H, cinco commits propuestos y las verificaciones finales.]

Mensajes siguientes: «Instalo git y clono» · «continua».

**Síntesis de la respuesta:**
- Leyó `historias.md`, `moscow.md`, `CONSTITUTION.md` y el prompt; comprobó que `git` no estaba instalado y que `Desktop\InsightHub` no tenía `.git`.
- Tras la instalación, clonó `https://github.com/ValentinaDavid156/InsightHub` junto a `Estructura-datos/` (en `Estructuras_datos\InsightHub`) y comparó el contenido con la copia suelta: era idéntico salvo los finales de línea. Se trabajó en el clon, que conserva el historial.
- Renombró las carpetas con `git mv` (22 archivos conservados como renombres) y creó `07-monticulo/` y `08-lista-simple/`.

**Decisión de la estudiante:** instalar git y clonar. Aprobó el mensaje del commit 1 (`416fa9e`, «refactor(specs): carpetas 00-producto, 01..08 y 99-sistema»).

## Sesión 2 — `CONSTITUTION.md` v1.2

**Prompt (textual):** «Sí, haz el commit» (tras el commit 1; la Constitución se trabajó a continuación).

**Síntesis de la respuesta:** quitó `entrega-1` y `entrega-2` y propuso cuatro choques más.

**Decisiones de la estudiante:**
1. Mantener «3 pruebas por operación», agrupadas por criterio en `tasks.md`.
2. Agregar `refactor` y `docs` a los tipos de commit.
3. «Un commit por tarea» rige solo la implementación; los documentos de spec se pueden agrupar.
4. Presencia de 30 s en consola y web; el sondeo cada ~5 s solo si se hace la web.

## Sesión 3 — `historias.md` v1.2

**Síntesis de la respuesta:** separó CA-37 (consola) de CA-38 (web) y CA-29 (palabra) de CA-39 (fecha); reescribió HU-01 y HU-14 desde el valor para el miembro; quitó de HU-12 el aviso de respuestas aceptadas y lo pasó a HU-08. Total: 39 criterios, sin renumerar los existentes. Verificado por comando: 14 historias, todas con al menos 2 criterios.

**Decisiones de la estudiante:** agregar CA-38 y CA-39 al final (no renumerar); aviso de respuesta aceptada en HU-08; HU-01 y HU-14 redactadas desde el valor para el miembro.

## Sesión 4 — `moscow.md` v1.2 y `estructuras.md` v1.2

**Prompt (textual):** «Sí, haz el commit» (commit 2, `4c44ad7`, «spec(producto): historias, MoSCoW y estructuras v1.2»).

**Síntesis de la respuesta:** quitó «se parte del código ya preparado» y reestimó escribiendo cada estructura. Los Must pasan de 12.25 h a **17.75 h (+5.5 h)** y los Should de 6.25 h a 9 h. Sumó 2.5 h de specs, plans, tasks, `99-sistema` y trazabilidad, y subió el cierre de 5 h a 6 h (informe 3 h, `ANALISIS.md` 1.5 h, bitácora y README 0.5 h, sustentación 1 h). Con 20 h solo quedaban 9.5 h netas y no cabían los Must. Agregó la fila «representación de las relaciones» y las rutas nuevas en `estructuras.md`.

**Decisión de la estudiante:** subir el total a **29 h** (18.5 h netas; los Must caben con 0.75 h de margen).

## Sesión 5 — Pila (`02-pila`)

**Síntesis de la respuesta:** partió de `Semana10/pila.py` (`PilaEnlazada`). CA-30 y CA-31 quedan en la pila; la regla de pantallas repetidas queda en `dominio/navegacion.py`.

**Decisiones de la estudiante:** la pila avisa con un error y la navegación lo traduce; no apilar si la pantalla es igual a la actual; historial sin límite; el uso desde el árbol general se menciona sin criterio propio.

## Sesión 6 — Cola (`03-cola`)

**Síntesis de la respuesta:** partió de `ColaEnlazada` de `Semana10/cola.py` (no de la circular); agregó `contiene`.

**Decisiones de la estudiante:** CA-06 es del grafo (no de la cola); detectar solicitudes repetidas con `contiene`; solo se atiende la primera solicitud; leer notificaciones las lee todas y vacía la cola.

## Sesión 7 — Lista doble (`01-lista-doble`)

**Síntesis de la respuesta:** partió de `Semana7/Nodos_enlazados_doblemente.py` y `carrusel.py`; sacó el cursor de la lista (un marcador por sesión).

**Decisiones de la estudiante:** CA-29 (búsqueda por palabra) es de la lista doble y no del AVL; páginas de 5 publicaciones; una posición por sesión; búsqueda sin distinguir mayúsculas y como subcadena.

## Sesión 8 — Árbol general (`04-arbol-general`)

**Síntesis de la respuesta:** partió de `NodoArbol` de `Semana10/arbol_binario.py` (sus dos enlaces pasan a primer hijo y hermano derecho) y del recorrido con pila de `arbol_carpetas.py`/`recorridos.md`; recorrido sin recursión.

**Decisiones de la estudiante:** un árbol por publicación; respuestas del mismo nivel en orden cronológico; solo las de primer nivel pueden ser mejor respuesta; en un empate de puntaje queda la más antigua.

## Sesión 9 — AVL (`05-avl`)

**Síntesis de la respuesta:** señaló que el repositorio no tiene árbol de búsqueda ni AVL; solo se reutilizan `NodoArbol`, `inorden` y la altura con vacío = −1. Detectó que **CA-21 (insignias) no tenía dueño**.

**Decisiones de la estudiante:** CA-21 queda en el AVL con los votos; un solo índice por `@usuario` (se corrige la fila de `estructuras.md`); `@usuario` de 3 a 20 caracteres, letras, números y guión bajo, sin distinguir mayúsculas; 120 perfiles de ejemplo con nombres de una lista fija más un número.

## Sesión 10 — Grafo (`06-grafo`)

**Síntesis de la respuesta:** el grafo pasa de dirigido («seguimientos») a no dirigido; partió de `Nodo` de Semana5 y `ColaEnlazada` de Semana10; recorrido por niveles con la cola para llegar a 2 saltos.

**Decisiones de la estudiante:** contadores de amigos en común en un arreglo temporal por id; la amistad más reciente sale primero.

## Sesión 11 — Montículo (`07-monticulo`)

**Síntesis de la respuesta:** señaló que no hay montículo en el repositorio; de `cola_prioridad.py` solo toma la clave compuesta para desempatar.

**Decisiones de la estudiante:** actividad = respuestas + votos vigentes del hilo, 1 a 1; empate a favor de la publicación más reciente; actualización en sitio con arreglo de posiciones; 5 recomendaciones con desempate por `@usuario` alfabético.

## Sesión 12 — Lista simple (`08-lista-simple`)

**Síntesis de la respuesta:** partió de `ListaEnlazada` de `Semana6/lista_reproduccion/lista_enlazada.py` y de la idea de tiempo por parámetro de `cola_prioridad.py`; quitó `_cola`.

**Decisiones de la estudiante:** cualquier acción cuenta como actividad; la caducidad se aplica al consultar con la hora dada por quien llama; la verdad del estado de conexión vive solo en la lista.

## Sesión 13 — `99-sistema` y `trazabilidad.md`

**Síntesis de la respuesta:** escribió la spec del sistema (tabla de ocho componentes con sus operaciones, flujos de integración, consola Must y web Should) y la trazabilidad de CA-01 a CA-39 con su tabla inversa. Detectó una incoherencia propia en el aviso de respuesta.

**Decisiones de la estudiante:** consola con menús numerados por pantalla; la semilla crea solo los perfiles (la demo crea amistades y publicaciones desde la consola); el aviso de respuesta va solo al autor de la publicación y no se avisa si responde el propio autor.

## Sesión 14 — Verificación

**Síntesis de la respuesta:** corrió un script que comprobó: 39 criterios, cada uno con exactamente una spec dueña y una fila en `trazabilidad.md`; todas las historias con al menos 2 criterios; Must 17.75 h ≤ 18.5 h netas; 3 Won't con razón; 135 enlaces entre `.md` sin ninguno roto; 58 filas de historial, todas con motivo y fecha 2026-11-07; ningún término de implementación en las specs (se corrigió «sin recursión» en la pila).

**Decisión de la estudiante:** aprobó la verificación y pidió hacer un commit por componente.

## Sesión 15 — Esqueleto del repositorio

**Prompt (textual):**
> ya esta lo necesario de la entrega 1?  (con el enunciado `Proyecto-Integrador-Tematica-B.pdf`)
>
> completalo y subelo con un commit llamado, cambios pequeños

**Síntesis de la respuesta:** cruzó el checklist de la Entrega 1 del PDF con el repositorio: los documentos estaban completos, pero faltaban `estructuras/`, `dominio/`, `tests/`, `docs/` y `pytest` no corría. Creó las carpetas, una prueba de arranque (`tests/test_arranque.py`, sin criterio CA, solo para que pytest corra), actualizó el menú de `main.py` a las specs v1.2, corrigió `ANALISIS.md` (decía «implementada» para la lista doble sin código) y agregó instrucciones al `README.md`. No escribió código de estructuras.

**Decisión de la estudiante:** completar el esqueleto y subirlo con el commit «cambios pequeños».

## Sesión 16 — Avance funcional: pila y navegación «atrás»

**Prompt (textual):**
> empecemos con el avance funcional
>
> no, lo que queria decir es que TÚ claude, escribas todo y yo Valentina Reviso
>
> Para los archivos de python revisa primero esta carpeta, lo que se puede reciclar de aqui, quiero que todos los .py los hagas con base a lo que yo ya he visto/usado que esta aqui

**Síntesis de la respuesta:**
- Se revisó el código del curso (`Semana5/nodo.py`, `Semana10/pila.py`, `cola.py`, `cola_prioridad.py`, `Semana6/lista_enlazada.py`, `Semana4/lista_arreglo.py`, `Semana7/*`, y sus pruebas) para imitar su estilo: invariantes y complejidad en el docstring, errores propios que heredan de `IndexError`, `tamaño()` además de `tamano()`, pruebas con `pytest` como funciones sueltas.
- Se escribieron primero las pruebas (rojo: `ModuleNotFoundError`) y después `estructuras/nodo.py`, `estructuras/pila.py` (de `PilaEnlazada`, Semana10) y `dominio/navegacion.py`. Resultado: 24 pruebas de pila y navegación pasan (29 en total con las de arranque de la consola).
- Se integró «Volver atrás» en `main.py` y se marcaron CA-30 y CA-31 como «pasa» en la trazabilidad.

**Decisión de la estudiante:** la IA escribe pruebas y código y la estudiante los revisa. Pendiente: leer línea por línea lo escrito antes de la sustentación (Principio 8 de la Constitución).

## Sesión 17 — Avance 1: cola y notificaciones

**Prompt (textual):**
> analiza nuevamente el documento del proyecto integrador B, y realiza un plan con commits, nombres propuestos donde este dividido cada avance para la entrega final, y analiza que mas hace falta de la entrega 2
>
> si   (aprobó empezar por el avance 1, la cola)

**Síntesis de la respuesta:**
- Releyó el PDF y propuso un plan de 10 avances con commits para llegar a `entrega-final` (11 de nov); señaló lo que falta de la entrega 2: 3 estructuras más (de las 4 mínimas), el párrafo por estructura en `ANALISIS.md`, «Qué se dificultó» en la bitácora y una nota de prioridades en `moscow.md`.
- Avance 1: escribió primero 33 pruebas (`tests/test_cola.py`, en rojo) y luego `estructuras/cola.py` (de `ColaEnlazada`, Semana10, más `contiene` e iterador) y `dominio/notificaciones.py` (una cola por persona en un arreglo indexado por id). Resultado: 62 pruebas pasan en total.
- CA-32 y CA-33 quedan «pasa»; CA-05 y CA-07 quedan «parcial» hasta que existan el grafo y el AVL (`amistades.enviar` y `amistades.atender`, Avance 5). Se agregó el arreglo indexado como soporte interno en el plan de la cola (v1.2).

**Decisión de la estudiante:** aprobar el plan por avances y empezar por la cola; la IA escribe pruebas y código y la estudiante los revisa.

## Sesión 18 — Avance 2: lista doble (plaza)

**Prompt (textual):**
> Sí, haz los 4  /  pero no aparecen los commits en insighthub  /  no, continua, y recuerda, cada cambio me lo indicas, yo tomo la decision

**Síntesis de la respuesta:**
- Subió los 4 commits de la cola a GitHub y retomó con la lista doble. Antes de escribir código consultó 3 decisiones de diseño que el spec no cerraba.
- Escribió primero 36 pruebas (`tests/test_lista_doble.py`, en rojo) y luego `estructuras/lista_doble.py` (de `ListadoblementeEnlazada`, Semana7: inserta al frente, marcador por sesión, avanzar y retroceder de 5 en 5), `dominio/feed.py` (`Publicacion`, `Plaza`, `SesionPlaza`) y `dominio/busqueda.py`. Resultado: 98 pruebas pasan en total.
- CA-12, CA-13 y CA-29 quedan «pasa». Spec de la lista doble v1.2 (retroceder llega al principio) y plan v1.2 (búsqueda en el dominio, `Publicacion` en `feed.py`).

**Decisión de la estudiante:** retroceder hasta el inicio si faltan menos de 5; la búsqueda por palabra va en `dominio/busqueda.py`; la `Publicacion` va en `dominio/feed.py`; cada cambio se le indica y ella decide.

## Sesión 19 — Avance 3: AVL y usuarios

**Prompt (textual):**
> necesito entregar todo asi no cuente, asi que continuemos con el avl, ya sabes la tematica, yo tomo las decisiones
>
> esperate, no hicimos cada entrega, los commits son con entrega 1 entrega 2 y entrega final :c  /  pero se pueden cambiar los commits sin alterar la fecha? el nombre ps  /  renombralos por fa, si  /  haz el push de la entrega 1  /  continua con AVL

**Síntesis de la respuesta:**
- Reorganizó las entregas: renombró el commit `cambios pequeños` a `Entrega 1: especificación y diseño` (fechas y contenido intactos), creó y subió la etiqueta `entrega-1`; acordó los commits en 3 por avance (`test`, `feat`, `docs`) y una etiqueta por entrega.
- Consultó 3 decisiones antes de programar y escribió primero las pruebas (rojo): `tests/test_avl.py` (73 pruebas del AVL y los usuarios: CA-01 a CA-04, CA-27 y CA-28) y las 12 de la consola actualizada.
- Escribió `estructuras/avl.py` (desde el `NodoArbol` de Semana10: inserción ordenada, cuatro rotaciones, prefijo), `dominio/usuarios.py` (`Catalogo`, `Perfil`, `UsuarioInvalidoError`, `generar_comunidad` con la semilla 706132) y la entrada por consola. Resultado: 178 pruebas pasan. Al probar la consola a mano se corrigió el orden del menú, que salía desordenado.
- CA-01 a CA-04, CA-27 y CA-28 quedan «pasa». Spec del AVL v1.2, plan v1.2 (decisiones de implementación) y spec de `99-sistema` v1.1.

**Decisión de la estudiante:** `insertar` devuelve False si existe; `buscar` devuelve None si no está; el dominio lanza `UsuarioInvalidoError`; la `@` inicial es opcional; la consola pide el `@usuario` al arrancar; la lista de 40 nombres; commits agrupados por avance.

## Sesión 20 — Cierre de la entrega 2 y avance 4: grafo

**Prompt (textual):**
> Sí, prepárala  /  Sí, al grafo

**Síntesis de la respuesta:**
- Cerró la entrega 2 en local: párrafo por estructura en `ANALISIS.md`, `moscow.md` v1.3 sin cambios de prioridad, commit y etiqueta `entrega-2`, sin push.
- Escribió primero `tests/test_grafo.py` (52 pruebas) y luego `estructuras/grafo.py`, desde el `Nodo` de Semana5 y la `ColaEnlazada` de Semana10. Resultado: 230 pruebas pasan.
- CA-08, CA-34 y CA-36 quedan «pasa» y CA-06 «parcial». Plan del grafo v1.2.

**Decisión de la estudiante:** `agregar_amistad` y `eliminar_amistad` devuelven True o False; `candidatos_dos_saltos` devuelve una lista de `(id, comunes)`.

## Sesión 21 — Avance 5: amistades integradas

**Prompt (textual):**
> Sí, al avance 5

**Síntesis de la respuesta:**
- Consultó 4 decisiones antes de programar. Señaló que con una sola sesión nadie podía aceptar una solicitud desde la consola.
- Escribió primero las pruebas (rojo): 47 nuevas en `tests/test_cola.py`, `tests/test_grafo.py` y `tests/test_arranque.py`; cambió 2 pruebas de consola porque la opción 2 ya no está pendiente y el menú llega a 9.
- Escribió `dominio/amistades.py` (`enviar`, `primera`, `pendientes`, `atender`, `deshacer`, `amigos`) y en `main.py` el submenú de amigos, las notificaciones y «Cambiar de @usuario». Resultado: 277 pruebas pasan; también se probó la consola real entre dos personas.
- CA-05, CA-06 y CA-07 quedan «pasa». Spec de la cola v1.2, plan v1.3 y spec de `99-sistema` v1.2.

**Decisión de la estudiante:** la solicitud cruzada se rechaza con aviso; el dominio lanza `SolicitudInvalidaError`; submenú de amigos y notificaciones activas; opción 9 para cambiar de `@usuario`.

## Sesión 22 — Avance 6: árbol general e hilos

**Prompt (textual):**
> bueno, eso es mejor comprobarlo despues, sigamos con lo que hace falta en orden
>
> 1. error, 2. hilo, 3 rechazar la respuesta, 4. recomendado

**Síntesis de la respuesta:**
- Consultó 4 decisiones antes de programar y escribió primero las pruebas (rojo): `tests/test_arbol_general.py` y las de consola, 48 nuevas; cambió 2 pruebas de consola que usaban la opción 3, que ya no está pendiente.
- Escribió `estructuras/arbol_general.py` (primer hijo y hermano derecho sobre la idea del `NodoArbol` de Semana10, recorrido con la pila propia), `dominio/hilos.py` y en `main.py` las pantallas de plaza e hilos. Resultado: 325 pruebas pasan, incluido un hilo de 2000 niveles; también se probó la consola real.
- CA-14, CA-15 y CA-16 quedan «pasa». Spec del árbol v1.2, plan v1.2, spec de la lista doble v1.3 y `estructuras.md` v1.3.

**Decisión de la estudiante:** los rechazos lanzan `RespuestaInvalidaError`; las respuestas se numeran por hilo (la publicación es el 0); se rechazan la respuesta y el título vacíos, y el cuerpo puede ir vacío; opción 3 para la plaza y 4 para los hilos.

## Sesión 23 — Avance 7: montículo y recomendaciones

**Prompt (textual):**
> Sí, al avance 7

**Síntesis de la respuesta:**
- Consultó 3 decisiones antes de programar y escribió primero las pruebas (rojo): `tests/test_monticulo.py` y las de consola, 28 nuevas; reemplazó la prueba de «opción pendiente» porque ya no queda ninguna.
- Escribió `estructuras/monticulo.py` (arreglo con `antes(a, b)` recibida, `subir`, `bajar`, `construir` en O(m)), `dominio/recomendaciones.py` y la opción 8 de la consola. Resultado: 353 pruebas pasan; también se probó la consola real (`@meta_x (2 amigos en común)`).
- CA-35 queda «pasa»: los 24 criterios Must tienen código salvo CA-37, que se cierra con la prueba del sistema. Plan del montículo v1.1.

**Decisión de la estudiante:** con el montículo vacío se lanza `MonticuloVacioError`; cada recomendación se muestra con su número de amigos en común; la opción 8 solo muestra, sin enviar solicitudes.

## Sesión 24 — Avance 8: consola completa (CA-37)

**Prompt (textual):**
> Sí, al avance 8

**Síntesis de la respuesta:**
- Revisó las historias HU-02 a HU-13 contra el menú: todas las funciones Must ya tenían opción en la consola desde los avances 5 a 7.
- Escribió `tests/test_sistema.py` (15 pruebas) con la comunidad real de 120 perfiles: un recorrido por historia (HU-02, HU-03, HU-05, HU-06, HU-10 a HU-13) con varias personas que se turnan con la opción 9, más RF-01 a RF-04 y RF-07. Pasaron sin cambiar código, salvo una aserción mal planteada en la prueba de la plaza que se quitó: aquí no hubo fase en rojo porque el código ya existía. Resultado: 368 pruebas pasan.
- CA-37 queda «pasa»: los 24 criterios Must pasan.

**Decisión de la estudiante:** seguir con el avance 8 en orden.

## Sesión 25 — Cierre de la entrega final

**Prompt (textual):**
> Sí, al cierre
>
> continuemos

**Síntesis de la respuesta:**
- Releyó el enunciado de la entrega final y escribió `docs/evidencias/medir.py`, que mide AVL frente a árbol sin equilibrar, lista doble frente a arreglo y montículo frente a ordenar; resultados en `docs/evidencias/mediciones.csv`.
- Completó `ANALISIS.md`, `README.md`, `moscow.md` v1.4 y `estructuras.md` v1.4, y redactó `docs/informe_final.pdf` (fuente en `docs/informe_final.html`).
- Corrigió el encabezado de esta bitácora, que todavía decía que la IA solo escribió documentos.

**Decisión de la estudiante:** cerrar sin los Should.

## Sesión 26 — Correcciones después de la entrega

**Prompt (textual):**
> puedes revisar nuevamente el repositorio y me confirmas si si lo puedo subir?
>
> Sí, corrígelos

**Síntesis de la respuesta:** revisó el repositorio desde un clon nuevo de GitHub y señaló tres detalles. Corrigió los planes del AVL, el grafo y el montículo, que decían «lo escribo desde cero», y la tabla de `99-sistema`, que ponía `buscar_palabra` en la lista doble. Para RF-05 del AVL escribió primero 4 pruebas en `tests/test_arranque.py` (una falló en rojo) y luego el código: en «Buscar usuarios», si se escribe un `@usuario` completo se muestra su perfil con sus puntos. Resultado: 372 pruebas pasan. Actualizó la spec y el plan del AVL, la trazabilidad, el README y las cifras del informe.

**Decisión de la estudiante:** corregir los tres detalles en commits nuevos, sin mover la etiqueta `entrega-final`.

## Supuestos de la IA pendientes de tu revisión
- Una persona con **30 s o más** sin actividad figura desconectada (CA-10 dice «tras 30 segundos»).
- Prefijo vacío y palabra vacía devuelven resultado vacío (no la comunidad ni la plaza completas).
- Una sola publicación, aun con actividad 0, es la destacada.
- Se agregó a la spec de la cola el caso extremo «sin aviso si responde el propio autor».
- Nombre sugerido para el sitio web: `web.py` (aparece en la trazabilidad como código esperado de CA-38).
- `99-sistema` no tiene `plan.md` ni `tasks.md` (el encargo pedía solo `spec.md`).

## Qué hice
- 2026-11-07: creé la estructura del repositorio, la constitución, las historias, MoSCoW, la decisión de estructuras y spec/plan/tasks de cada componente; ese mismo día los reescribí con la numeración v1.2.

## Qué se dificultó
- **Grafos (autodidacta):** no lo vimos en clase, así que investigamos cómo hacerlo. Usamos una lista de adyacencia. Lo difícil fue validar: que nadie se agregue a sí mismo, no duplicar amistades y que la amistad quede en ambos sentidos. Con un recorrido por niveles sugerimos amigos de amigos.
- **AVL:** no habíamos visto árboles equilibrados. Lo más difícil fue programar bien las cuatro rotaciones al insertar, porque un error en los enlaces o en la altura desbalanceaba el árbol.
- **Pilas, colas y lista doble:** las colas atienden solicitudes y notificaciones en orden de llegada. La pila guarda el historial para «volver atrás» y recorre los hilos sin recursión. La lista doble muestra la plaza de 5 en 5, con lo más nuevo arriba.
- **Conectar las estructuras:** el perfil se guarda una sola vez en el AVL, y las demás estructuras solo usan su id, para no duplicar datos.
- **Consola:** los datos viven en memoria, porque guardar en archivos quedó como Won't. Para probar con varias personas agregamos «cambiar de `@usuario`». También validamos que el programa no se caiga si se escriben letras donde van números u opciones que no existen.
