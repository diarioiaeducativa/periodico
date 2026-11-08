# 34. La semana y el mes en la hemeroteca, con el pódcast y el vídeo de cada grupo, en lugar del boletín semanal

Fecha: 2026-11-08 · Estado: aceptado

## Contexto

Hasta ahora, ChatGPT-IA-edu y Vibe Coding Educativo tenían cada uno un boletín semanal (repositorio
`boletin-semanal`): un resumen escrito en una hoja de cálculo y su web, una infografía, un pódcast y un
vídeo de NotebookLM, y avisos en Telegram, X, Bluesky y LinkedIn cada lunes. EduMedia-IAG tenía el suyo,
que hacía Raül Torres. Desde que sale el diario, el resumen escrito repite lo que el diario ya cuenta cada
día, y la hemeroteca obligaba a recorrer los números uno a uno.

Raül Torres propuso (08-11-2026) agrupar la hemeroteca por semanas y por meses, porque «mirar día por día
es engorroso», quedarse del boletín con el pódcast y el vídeo de NotebookLM de cada comunidad, añadidos los
lunes a la semana, y dejar los boletines anteriores en la página como hemeroteca. Juanjo lo aprobó y decidió
que fueran solo pódcast y vídeo, sin infografía, que el proceso hiciera también los de EduMedia-IAG y que
desde el lunes 9 de noviembre de 2026 ya no saliera el boletín de siempre.

## Decisión

- **Página de cada semana** (`semana/AAAA-WW/`, en los cinco idiomas): todas las piezas de la semana por
  secciones, con el reportaje delante, solo con titular y fecha para que se abarque de un vistazo; el pódcast
  y el vídeo de NotebookLM de cada grupo; y los números de la semana con la pieza que abrió cada uno. Un
  selector filtra por grupo y lo deja en la dirección (`?grupo=chatgpt|vce|edumedia`), para enlazar desde
  cada grupo lo suyo. Lo que no nace de un grupo (el reportaje) solo sale en «Todos».
- **Enlace fijo a la última semana**: `semana/` a secas (también con `?grupo=`) lleva a la última semana
  que ya tiene el pódcast y el vídeo, o a la más reciente si aún no hay ninguna. Es el que dan las webs de
  los boletines antiguos, que no pueden saber cuál es la última.
- **La semana es la de los mensajes**, de lunes a domingo (ISO 8601): la misma que cubren el pódcast y el
  vídeo, que el boletín hace con la conversación completa de cada grupo. La cierra el número del lunes, que
  sale cuando llegan las piezas de NotebookLM. «La semana en vídeo» del diario no va en esta página: repasa
  los números de lunes a domingo, un día desplazada, y ya está en el número del domingo y en «Vídeos».
- **Página de cada mes** (`mes/AAAA-MM/`), con sus semanas y la pieza que abrió cada número. Una semana es
  del mes en que cae su jueves, como manda la ISO 8601, para que no salga en dos meses.
- **Hemeroteca** por meses y semanas, con los días de cada semana plegados (la más reciente, abierta) y, al
  final, los boletines semanales anteriores de los tres grupos en su web (`BOLETINES` en `generar.py`). Los
  enlaces a cada número no cambian.
- **El contrato con el boletín**: `multimedia/AAAA-WW.json` (formato en `multimedia/LEEME.md`). El vídeo
  no se carga hasta que se pulsa, desde youtube-nocookie, para que abrir la página no avise a YouTube; el
  audio, sin precarga. En los otros idiomas se dice que están en castellano.
- **Publicación**: cuando aparece o cambia ese archivo, con el número del día ya publicado, `nas/reloj.sh`
  vuelve a publicar solo la web (`scripts/publicar-web.sh`), sin avisos ni Instagram, y guarda el archivo en
  el repositorio; si falla, avisa una vez y lo reintenta cada media hora.
- En el pie, junto a la hemeroteca, «La semana, de un vistazo» lleva a la semana en curso.

## Alternativas descartadas

- **Tres páginas por semana, una por grupo**: repetirían el reportaje y lo común; el selector da a cada grupo
  su enlace sin duplicar nada.
- **Entradillas en la lista de la semana**: una semana tiene unas 45 piezas, y con ellas la página pasaba de
  14 000 píxeles de alto en el móvil (Firefox no podía ni capturarla); con titulares se queda en unos 9 500.
- **Importar al diario los boletines antiguos**: mucho trabajo para algo que ya se consulta en su web.
- **Incrustar el vídeo de entrada**: avisaría a YouTube de cada visita.

## Consecuencias

- El boletín deja de redactar el resumen escrito y de llenar las hojas de cálculo; sigue exportando la
  semana, generando y revisando el pódcast y el vídeo de los tres grupos, subiéndolos a YouTube e Internet
  Archive y avisando los lunes en Telegram y, con el vídeo de cada grupo y el enlace a su semana, en X,
  Bluesky y LinkedIn (ADR 0009 a 0011 del repositorio `boletin-semanal`).
- El contenedor del diario necesita reiniciarse para leer el bloque nuevo de `nas/reloj.sh`.

## Validación

Generado en una copia aparte con un `multimedia/2026-45.json` de prueba (los vídeos y pódcast reales de la
semana 44) y probado con `probar-web` en Chromium y Firefox, escritorio y móvil, claro y oscuro: sin errores
de la página, sin desbordamiento; el selector filtra, cambia la dirección y el vídeo se carga al pulsar
(Firefox anota en la consola una cookie que rechaza el propio reproductor de YouTube). El bloque del reloj,
simulado: no publica sin número del día, publica una vez por cambio y reintenta a la media hora.
`publicar-web.sh`, contra un repositorio de sitio local.
