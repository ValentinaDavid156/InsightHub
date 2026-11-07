# Historias de usuario — InsightHub

Formato: *Como [rol], quiero [acción], para [valor].* Cada historia se mapea a una funcionalidad F-xx del enunciado.

## HU-01 · Generar usuarios sintéticos (F-01)
Como **administrador de la comunidad**, quiero generar usuarios de prueba de forma reproducible, para poder demostrar y probar el sistema con datos estables.
- **CA-01:** Al generar, el sistema crea al menos 100 usuarios con id y nombre únicos.
- **CA-02:** Con la misma semilla se obtienen exactamente los mismos usuarios en el mismo orden.

## HU-02 · Seguir y dejar de seguir (F-02)
Como **miembro**, quiero seguir a otros usuarios y dejar de seguirlos, para ver sus aportes y construir mi red.
- **CA-03:** Al seguir a un usuario, la relación existe; seguir dos veces o seguirse a sí mismo se rechaza sin duplicar.
- **CA-04:** Al dejar de seguir, la relación desaparece; dejar de seguir a quien no sigo no produce error.

## HU-03 · Publicar preguntas y navegar el feed (F-03)
Como **miembro**, quiero publicar una pregunta y recorrer mi feed hacia adelante y atrás, para revisar discusiones sin perder mi lugar.
- **CA-05:** Una pregunta nueva aparece como la primera del feed del autor.
- **CA-06:** Avanzar en la última o retroceder en la primera pregunta no mueve la posición e informa el límite; en un feed vacío no falla.

## HU-04 · Responder en hilos anidados (F-04)
Como **miembro**, quiero responder a una pregunta o a otra respuesta, para profundizar el debate en el punto exacto.
- **CA-07:** Responder a una pregunta agrega una respuesta de primer nivel a su hilo.
- **CA-08:** Se puede responder a una respuesta hasta una profundidad de al menos 3 niveles, y el hilo se muestra completo con sangría por nivel.
- **CA-09:** Responder a un comentario inexistente se rechaza sin alterar el hilo.

## HU-05 · Buscar usuarios y preguntas (F-05)
Como **miembro**, quiero buscar usuarios por nombre y preguntas por palabra o fecha, para encontrar a quién seguir y qué ya se discutió.
- **CA-10:** Buscar usuarios por prefijo devuelve las coincidencias en orden alfabético.
- **CA-11:** Una búsqueda sin coincidencias devuelve resultado vacío, sin error.
- **CA-12:** Buscar preguntas por palabra devuelve solo las que la contienen en el título.

## HU-06 · Volver a la pantalla anterior (F-06)
Como **miembro**, quiero un botón «atrás», para regresar a la pantalla que visité antes.
- **CA-13:** «Atrás» regresa a la pantalla visitada inmediatamente antes, y repetirlo retrocede en orden inverso.
- **CA-14:** «Atrás» con historial vacío informa que no hay pantalla previa y no falla.

## HU-07 · Recibir y leer notificaciones (F-07)
Como **miembro**, quiero recibir avisos de nuevos seguidores, comentarios y respuestas, para enterarme de lo que me concierne.
- **CA-15:** Las notificaciones se leen en el mismo orden en que llegaron.
- **CA-16:** Leer con la cola vacía informa «sin notificaciones» y no falla.

## HU-08 · Recomendaciones de contactos (F-08)
Como **miembro**, quiero sugerencias de «personas que quizá conozcas», para ampliar mi red con gente afín.
- **CA-17:** Se recomiendan usuarios a 2 saltos (seguidos de mis seguidos), excluyéndome a mí y a quienes ya sigo.
- **CA-18:** Las recomendaciones se ordenan por número de contactos en común, de mayor a menor.
- **CA-19:** Un usuario que no sigue a nadie recibe una lista vacía.

## HU-09 · Calificar aportes (Should)
Como **miembro**, quiero votar las respuestas útiles, para destacar los mejores aportes.
- **CA-20:** Votar una respuesta incrementa su puntaje en 1.
- **CA-21:** Un mismo usuario no puede votar dos veces la misma respuesta.
