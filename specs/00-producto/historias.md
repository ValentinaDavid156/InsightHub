# Historias de usuario — InsightHub
Versión 1.1

Formato: *Como [rol], quiero [acción], para [valor].* Cada historia indica la funcionalidad F-xx del enunciado a la que responde.

## HU-01 · Generar usuarios sintéticos (F-01)
Como **administrador de la comunidad**, quiero generar usuarios de prueba de forma reproducible, para demostrar y probar la plataforma con datos estables.
- **CA-01:** Al generar, el sistema crea al menos 100 usuarios con `@usuario` único.
- **CA-02:** Con la misma semilla se obtienen los mismos usuarios en el mismo orden.

## HU-02 · Acceder y crear perfil
Como **visitante**, quiero entrar con mi `@usuario`, para integrarme de inmediato a la comunidad.
- **CA-03:** Entrar con un `@usuario` nuevo crea el perfil y abre la sesión; con uno existente solo abre la sesión.
- **CA-04:** Un `@usuario` inválido (longitud o caracteres) o ya existente al registrarse se rechaza con un mensaje claro.

## HU-03 · Hacer amigos con solicitud (F-02)
Como **miembro**, quiero enviar solicitudes de amistad y aceptarlas o rechazarlas, para construir mi red de contactos.
- **CA-05:** Enviar una solicitud la deja pendiente en la cola del destinatario; no se permite enviarla a uno mismo, a un amigo ni repetida.
- **CA-06:** Aceptar una solicitud crea la amistad en ambos sentidos; rechazarla la descarta sin crear amistad.
- **CA-07:** Las solicitudes se atienden en el orden en que llegaron; sin solicitudes pendientes se informa sin error.
- **CA-08:** Deshacer una amistad la elimina en ambos sentidos; deshacer una que no existe no produce error.

## HU-04 · Ver quién está conectado
Como **miembro**, quiero saber quién está conectado, para interactuar con quien está activo.
- **CA-09:** Al entrar, la persona figura como conectada.
- **CA-10:** Al salir, o tras 30 segundos sin actividad, figura como desconectada.
- **CA-11:** Se puede ver la lista de personas conectadas y el estado (conectado o no) de cada amigo.

## HU-05 · Publicar y recorrer la plaza (F-03)
Como **miembro**, quiero publicar una pregunta en la plaza pública y recorrerla hacia adelante y atrás, para participar sin perder mi lugar.
- **CA-12:** Una publicación nueva aparece como la primera de la plaza.
- **CA-13:** Se puede paginar hacia adelante y atrás; en el primer o último extremo la posición no cambia y se informa el límite; con la plaza vacía no falla.

## HU-06 · Debatir en hilos anidados (F-04)
Como **miembro**, quiero responder a una publicación o a otra respuesta, para profundizar el debate en el punto exacto.
- **CA-14:** Responder a una publicación agrega una respuesta de primer nivel.
- **CA-15:** Se puede responder a una respuesta hasta una profundidad de al menos 3 niveles, y el hilo se muestra completo con sangría por nivel.
- **CA-16:** Responder a un comentario inexistente se rechaza sin alterar el hilo.

## HU-07 · Votar y ganar reputación
Como **miembro**, quiero votar las respuestas a favor o en contra, para señalar cuáles son valiosas y reconocer a quienes aportan.
- **CA-17:** Un voto positivo suma 1 punto de reputación al autor de la respuesta.
- **CA-18:** Un voto negativo resta 1 punto de reputación al autor de la respuesta.
- **CA-19:** Cada persona tiene como máximo un voto por respuesta y no puede votar su propia respuesta.
- **CA-20:** Cambiar o retirar el voto corrige el puntaje (de positivo a negativo el autor pierde 2 puntos; retirar revierte el voto).
- **CA-21:** La insignia visible en el perfil depende de los puntos: Nuevo (menos de 10), Colaborador (desde 10), Experto (desde 50).

## HU-08 · Destacar la mejor respuesta
Como **miembro que pregunta**, quiero marcar la respuesta que resolvió mi duda, para que todos la encuentren primero.
- **CA-22:** La respuesta que acepta quien hizo la pregunta queda fijada arriba del hilo y suma 15 puntos a su autor; solo quien preguntó puede aceptar, y una sola vez.
- **CA-23:** Si no hay respuesta aceptada, queda fijada la de mayor puntaje neto, siempre que sea positivo; sin respuestas, no hay ninguna fijada.

## HU-09 · Ver la publicación destacada
Como **miembro**, quiero ver arriba de la plaza la publicación con más actividad, para sumarme al debate del momento.
- **CA-24:** La publicación destacada es la de mayor actividad (respuestas y votos).
- **CA-25:** Cuando cambia la actividad de otra publicación y supera a la destacada, la destacada se actualiza.
- **CA-26:** Sin publicaciones, no hay destacada y no se produce error.

## HU-10 · Buscar usuarios y publicaciones (F-05)
Como **miembro**, quiero buscar personas por nombre y publicaciones por palabra o fecha, para encontrar con quién conectar y qué ya se discutió.
- **CA-27:** Buscar usuarios por prefijo devuelve las coincidencias en orden alfabético.
- **CA-28:** Una búsqueda sin coincidencias devuelve resultado vacío, sin error.
- **CA-29:** Buscar publicaciones por palabra devuelve las que la contienen en el título o el cuerpo; por fecha, las de ese día.

## HU-11 · Volver a la pantalla anterior (F-06)
Como **miembro**, quiero un botón «atrás», para regresar a lo que visité antes sin perder el hilo de la exploración.
- **CA-30:** «Atrás» regresa a la pantalla visitada inmediatamente antes; repetirlo retrocede en orden inverso.
- **CA-31:** «Atrás» con historial vacío informa que no hay pantalla previa y no falla.

## HU-12 · Recibir y leer notificaciones (F-07)
Como **miembro**, quiero recibir avisos de solicitudes de amistad, amistades aceptadas, respuestas y respuestas aceptadas, para enterarme de lo que me concierne.
- **CA-32:** Las notificaciones se leen en el mismo orden en que llegaron.
- **CA-33:** Leer notificaciones sin pendientes informa «sin notificaciones» y no falla.

## HU-13 · Recibir recomendaciones de contactos (F-08)
Como **miembro**, quiero sugerencias de «personas que quizá conozcas», para ampliar mi red.
- **CA-34:** Se recomiendan personas a 2 saltos (amigos de mis amigos), excluyéndome a mí y a quienes ya son mis amigos.
- **CA-35:** Las recomendaciones se ordenan por número de amigos en común, de mayor a menor.
- **CA-36:** Una persona sin amigos recibe una lista vacía.

## HU-14 · Usar la plataforma desde la consola y el navegador
Como **miembro**, quiero usar todas las funciones tanto desde la consola como desde un sitio web, para participar desde donde me resulte cómodo.
- **CA-37:** Cada función de las historias HU-02 a HU-13 puede ejercitarse desde la consola y desde el sitio web.

## Historial de cambios
| Versión | Fecha | Cambio | Motivo |
|---|---|---|---|
| 1.0 | 2026-11-07 | Versión inicial | Creación |
| 1.1 | 2026-11-07 | Se reescribe todo: amistad con solicitud y aceptación (antes «seguir»), votos positivos y negativos con cambio o retiro, presencia, mejor respuesta, publicación destacada, acceso y uso web. De 9 a 14 historias y de 21 a 37 criterios | La idea del proyecto se amplió y se decidieron las reglas de amistad y votos |
