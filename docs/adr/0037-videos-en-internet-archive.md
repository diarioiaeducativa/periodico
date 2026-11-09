# 37. Los vídeos, en Internet Archive

Fecha: 2026-11-09 · Estado: aceptado

## Contexto

Cada domingo «La semana en vídeo» (ADR 0016) sale en cinco idiomas, unos 2,3 MB cada uno: unos 12 MB
por semana, más de 500 MB al año. Hasta ahora `generar.py` los copiaba al sitio, y los dos repositorios
(este y el del sitio) los guardaban para siempre en su historial, aunque luego se borraran. GitHub Pages
admite como mucho 1 GB por sitio publicado. El boletín semanal ya guarda sus pódcast en Internet Archive,
un elemento por grupo y año (`boletinia_2026`, `vce_2026`). El 6 de noviembre se acordó hacer lo mismo con
los vídeos después del primer dominical.

## Decisión

- **Un elemento por año, `diarioiaeducativa_<año>`** (el año en que se publica el vídeo), «Diario de IA
  Educativa · Vídeos <año>», con autoría del diario, © de quienes lo firman y CC BY-SA 4.0, como el sitio.
  Se crea solo con el primer vídeo del año.
- **`scripts/subir-videos.py`** sube el vídeo y la portada de cada idioma con la librería oficial
  (`internetarchive`), espera a que se indexen, **descarga cada archivo desde archive.org y lo compara con
  el local** (tamaño y MD5) y solo entonces escribe `"archive": "<elemento>"` en `videos/<id>.json`.
- **La web enlaza el vídeo a `https://archive.org/download/<elemento>/<archivo>`** cuando el JSON lleva
  `archive`, y ya no lo copia al sitio. **La portada sigue en el sitio**: pesa unos 70 KB, se carga en
  cada visita a la página de vídeos (los vídeos no, `preload="none"`) y servirla desde archive.org la
  haría más lenta, porque cada descarga pasa por una redirección. En Archive queda también como copia.
- **Cuándo**: `reel-semana.sh` lo sube la noche del sábado, justo después de montarlo y antes de generar
  el número (el número suele estar listo hacia la 1:45, así que hay margen; tope de 90 minutos). Si
  archive.org falla, el JSON no cambia y la web sirve la copia local, como antes: el vídeo nunca falta.
  `noche.sh` lo vuelve a probar cada noche (tope de 15 minutos; sin pendientes, no hace nada), y en
  cuanto sube, la siguiente publicación lo quita del sitio. Es un fallo que se arregla solo: no se avisa
  a Juanjo, queda en el registro.
- **Los `.mp4` dejan de ir en los dos repositorios** (`.gitignore` de este). El historial conserva los
  anteriores. El NAS guarda el del domingo en local, porque el dominical de X, Bluesky y LinkedIn
  (`scripts/redes/dominical.sh`) lo sube desde allí; los de semanas anteriores están en Archive.
- **El contenedor**: `internetarchive` va en `nas/Dockerfile` (la misma versión que el boletín) y las
  claves del boletín se montan solo para leer (`nas/compose.yml`). El user-agent identifica el cliente
  con la dirección del repositorio, como pide Internet Archive, sin datos personales.

## Validación

El 9 de noviembre se subieron los dos vídeos publicados hasta entonces (el de la comunidad del 5 de
noviembre y «La semana en vídeo» del 8, en cinco idiomas) con sus portadas. Cada archivo se descargó desde
archive.org y coincidió con el local. La web generada se comprobó con `probar-web` en Chromium, Firefox
y WebKit, escritorio y móvil: los vídeos cargan y se reproducen desde archive.org.

## Riesgos

- Si archive.org está caído cuando alguien visita la web, el vídeo no se ve (la portada, sí). Es la
  misma dependencia que tienen los pódcast del boletín.
- Si cae varias noches seguidas, el vídeo de esa semana entra en el historial del sitio, como antes.
