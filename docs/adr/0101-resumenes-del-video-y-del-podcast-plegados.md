# 101. Los resúmenes del vídeo y del pódcast, plegados en su entradilla

Fecha: 2026-11-23 · Estado: aceptado

## Contexto

En la página de la semana, cada grupo tiene su vídeo y su pódcast de NotebookLM (ADR 0034). El vídeo llevaba debajo
su resumen de unas 72 palabras (ADR 0057), entero; el pódcast, ninguno, porque el boletín solo escribía la
descripción del vídeo para YouTube. Juanjo pidió el 23-11-2026 que el resumen se abriera al pulsarlo y que el pódcast
tuviera el suyo. La primera versión plegada ponía un rótulo «Resumen» bajo cada vídeo, y con el pódcast habrían
sido seis iguales en la misma pantalla: «resumen, resumen, resumen… y ahora pondrás más resumen».

## Decisión

- **Cada resumen, plegado en su propia entradilla**: cerrado enseña sus dos primeras líneas, cortadas con «…», y una
  flecha; al pulsarlo (o con Intro desde el teclado) se abre entero y la flecha se da la vuelta. Es un `<details>`
  cuyo `<summary>` es el propio texto (`resumen_plegado()` en `generar.py`): sin rótulos repetidos, cada ficha dice
  algo distinto y los lectores de pantalla lo anuncian como desplegable. El del vídeo va bajo el vídeo; el del
  pódcast, bajo el audio.
- **El resumen del pódcast lo escribe el boletín** (su ADR 0013) a partir de la transcripción del audio, sin empezar
  con la misma fórmula que el del vídeo, porque se leen juntos sus principios. Llega en `multimedia/AAAA-WW.json` como
  `resumen_podcast` y se traduce como el del vídeo (`scripts/multimedia.py`, `multimedia-traducir.sh` y el encargo
  `27-multimedia-traduccion.md`), con su origen en `origen_podcast`. Si falta, el pódcast sale sin resumen.
- **Fuera del ajuste de alturas** (`SCRIPT_FILAS`, ADR 0041): ya no hace falta recortar el resumen para igualar las
  fichas, y lo dejaba cortado al abrirlo.

## Alternativas descartadas

- **Un rótulo «Resumen» que despliega el texto**: la primera versión; se repetía en cada ficha.
- **Un solo desplegable por grupo con los dos resúmenes**: seguía repitiendo el rótulo tres veces y separaba cada
  resumen de lo que resume.

## Validación

Semana 2026-47 generada en una copia aparte, con los tres resúmenes del pódcast, y probada con `probar-web` en
Chromium, Firefox y WebKit, escritorio, móvil y tableta, claro y oscuro: cerrado ocupa dos líneas, se abre al pulsar
y se cierra con Intro.
