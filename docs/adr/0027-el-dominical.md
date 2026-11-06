# 27. El dominical: la semana en vídeo con el reportaje, en todas las redes

Fecha: 2026-11-06 · Estado: aceptado

## Contexto

Juanjo quiere que el vídeo de la semana y el reportaje del domingo salgan en todas sus redes
(06-11-2026: «el video y el anuncio del articulo especial»), y propuso juntarlos: «el reportaje + video
no se podria indicar como dominical y ponerlo todo junto?». Instagram ya publicaba el vídeo el domingo a
las 12:00 (ADR 0016). Bluesky no admite imagen y vídeo en la misma publicación; X y LinkedIn, tampoco
mezclados.

## Decisión

- **Un vídeo, «el dominical»**: «La semana en vídeo» termina con una escena del reportaje (rótulo
  «Reportaje», su titular, su conclusión y su infografía). El guionista del vídeo escribe esos textos en
  los cinco idiomas (`encargos/reel.md`); el reportaje ya está hecho cuando se monta el vídeo, la misma
  madrugada del domingo. Si no hay reportaje o faltan sus textos, el vídeo sale sin esa escena.
- **Una publicación por red, el domingo a las 12:00**, con el vídeo en castellano y un solo enlace, al
  número del domingo, que reúne el reportaje y el vídeo:
  - Instagram: el reel, como hasta ahora (`scripts/instagram.py reel`), titulado «El dominical» cuando
    lleva reportaje.
  - X y Bluesky: el texto corto del guionista («El dominical del Diario de IA Educativa: …», hasta 220
    caracteres) con «👉 El número del domingo: URL»; se acorta por frases si pasa de 300 con el enlace.
  - LinkedIn: el texto largo (el de Instagram) con el mismo enlace.
- **Quién publica en X, Bluesky y LinkedIn**: el contenedor del boletín semanal, que tiene las sesiones
  y los programas (los mismos del boletín de los lunes). `reel-semana.py` deja `dominical/<sábado>.json`
  con los textos y la ruta del vídeo; `scripts/redes/dominical.sh` (de este repositorio, montado allí en
  `/diario` solo para leer) lo publica desde las 12:00, con dos intentos por red y aviso si una falla
  (ADR 0007 del boletín). LinkedIn reutiliza `7-linkedin.py` del boletín por medio de
  `scripts/redes/dominical_linkedin.py`.
- **Revisión**: el aviso de las 5:00 del domingo (ADR 0025) trae también el texto de las redes.

## Alternativas descartadas

- Dos publicaciones (reportaje a las 9:00 con su infografía y vídeo a las 12:00): más ruido; Juanjo
  prefirió una sola.
- Un carrusel del reportaje en Instagram: queda dentro del vídeo.

## Validación

`dominical.sh --comprobar` en el contenedor del boletín, el 06-11-2026: Bluesky (sesión y longitud),
X (sesión, longitud y duplicados) y LinkedIn (navegador, editor y vídeo) dan por buena la publicación
sin publicar nada. La escena del reportaje, montada en una copia con el reportaje del 31-10 en
castellano, euskera e inglés. La primera publicación de verdad, el domingo 08-11-2026: vigilarla.

## Riesgos

- Es lo único que no se puede ensayar sin publicar. Si una sesión ha caducado, esa red falla y se avisa;
  las demás salen.
- Si el vídeo no se ha montado (por ejemplo, con el plan B de las 6:30), ese domingo no hay dominical en
  las redes.
