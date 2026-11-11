# 46. Cada número, en la Wayback Machine

Fecha: 2026-11-11 · Estado: aceptado

## Contexto

El 11-11-2026, al cambiar el titular de una pieza ya publicada, Juanjo preguntó si el diario estaba en
Internet Archive. No lo estaba: la Wayback Machine no tenía ninguna captura del sitio. El diario vive en
GitHub Pages y su historial en un repositorio, pero una copia en un archivo público e independiente deja
constancia de lo que se publicó cada día y sigue a mano si el sitio desaparece. Juanjo pidió las dos
cosas: archivar ya el número del día y que se archive solo cada mañana.

## Decisión

- **`scripts/archivar.py FECHA`** pide a Internet Archive, con Save Page Now y sin cuenta, que guarde la
  portada de cada idioma, la página del día y cada pieza del número en los cinco idiomas (unas 50
  páginas). La lista sale del mapa del sitio publicado (`sitemap.xml`): así solo se piden páginas que
  existen, y mientras el mapa no lleve el día, GitHub Pages aún no ha desplegado y el script espera
  (como mucho 30 minutos).
- **Una captura cada vez y 20 s entre una y otra.** Si Internet Archive contesta que va demasiado deprisa
  (429) o falla su servidor, espera 5 minutos y prueba otra vez; a la segunda seguida, lo deja, para no
  acabar bloqueado. Sin IA, sin coste y sin datos de nadie: solo las direcciones públicas del diario.
- **Lo lanza `publicar-nas.sh` en segundo plano**, con el sitio ya subido, para no retrasar los avisos ni
  el carrusel. El registro va a `registro/archivo.log`. Un día ya publicado o un cambio posterior (un
  titular corregido) se archiva a mano con la misma orden.
- **El contador de visitas (ADR 0033) solo cuenta en `diarioiaeducativa.github.io`.** La copia de la
  Wayback Machine ejecuta el JavaScript de la página: sin esta comprobación, una visita a la copia podría
  sumar en el panel una visita que no ha llegado al diario. Deja fuera también la vista previa de casa.

## Alternativas descartadas

- **La API de Save Page Now con cuenta**, que guarda también los enlaces de cada página: exige una cuenta y
  sus claves en el NAS, y con la lista del mapa del sitio no hace falta.
- **Archivar solo la portada**: la portada cambia cada día y las piezas quedarían fuera.

## Consecuencias

Cada número queda en la Wayback Machine en sus cinco idiomas hacia las 7:30. Un titular o un texto
corregido después de publicar queda archivado con la versión de la mañana hasta que se vuelva a lanzar el
script para ese día.

## Evidencia

- 11-11-2026: el índice de capturas (`web.archive.org/cdx/search/cdx?url=diarioiaeducativa.github.io*`)
  y la consulta de disponibilidad no devolvían nada.
- La primera captura de prueba, de la pieza del 10-11-2026 sobre la animación de la fotosíntesis, contestó
  con una redirección a `/web/20261111064412/…` y la copia guardada lleva el titular corregido.
- `robots.txt` deja pasar a todos los robots.

## Riesgos y limitaciones

- Los límites de Save Page Now sin cuenta no están publicados con cifras: el ritmo de 20 s es una
  hipótesis prudente. Si el registro muestra 429 a menudo, se alarga la pausa.
- Si Internet Archive está caído, ese día no se archiva; no se reintenta otro día.
- Que la reproducción de la copia no llegue al contador se garantiza por la comprobación de la dirección,
  no por cómo reescribe Internet Archive las peticiones.

## Validación

El número del 10-11-2026 (Núm. 10, publicado el 11-11-2026) se archivó a mano con el script; el resultado,
en `registro/archivo.log`.
