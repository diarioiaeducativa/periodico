# 100. El lunes, la portada anuncia el resumen semanal

Fecha: 2026-11-23 · Estado: aceptado

## Contexto

El número del lunes cierra la semana: esa noche se escribe el comentario de la semana (ADR 0038) y la página de la
semana reúne todo lo publicado, con el pódcast y el vídeo de cada grupo (ADR 0034). Pero la portada no lo decía: el
único enlace estaba en el pie («Resumen semanal»). Juanjo pidió (23-11-2026) que la portada de los lunes enlazara los
resúmenes semanales.

## Decisión

- **El número que cuenta el domingo** (el que sale el lunes) lleva, a la derecha de la apertura, un anuncio del resumen
  de su semana: el mismo hueco que ocupa la columna de opinión el día que sale (ADR 0092), que los lunes está libre.
  En la tableta y el móvil, debajo de la apertura, como el de la columna.
- **Qué dice**: el rótulo «Resumen semanal» con el número de la semana; el titular del comentario general; una
  línea que explica qué hay en la página, y «Leer el resumen de la semana». Si la semana no tiene comentario, el
  titular es el nombre de la semana y la línea dice solo que están todos los artículos por secciones.
- **Dónde**: en la portada y en la página de ese número, que se compone igual (ADR 0045). Los colores, los del
  comentario de la semana (fondo de papel y filete azul), para no confundirlo con la columna.
- **Código**: `anuncio_semana()` en `generar.py`; `apertura_portada()` recibe ya el anuncio hecho, sea de la columna
  o de la semana. Textos nuevos en las cinco lenguas: `leer_semana`, `sem_anuncio` y `sem_anuncio_sin`.

## Alternativas descartadas

- **Una franja a todo el ancho encima de la apertura**: empujaba hacia abajo las noticias del día.
- **Un enlace al resumen de cada grupo en el anuncio**: estuvo en la primera versión, pero sobraba (Juanjo,
  23-11-2026): la página de la semana ya tiene el selector de grupo.
- **Poner la fecha completa de la semana en el rótulo**: en escritorio partía el rótulo en dos líneas; la fecha
  queda en el título emergente y en la propia página de la semana.

## Validación

Generado en una copia aparte con el número del 23-11-2026 (semana 47) y probado con `probar-web` en Chromium,
Firefox y WebKit, escritorio, móvil y tableta, claro y oscuro: el anuncio no se sale de la pantalla. Comprobado también un lunes sin comentario (semana 44).
