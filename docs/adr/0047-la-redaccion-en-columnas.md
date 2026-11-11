# 47. «La redacción», en columnas como las noticias

Fecha: 2026-11-11 · Estado: aceptado

## Contexto

Las noticias y el reportaje van en columnas de periódico en el ordenador desde el ADR 0044, pero «La
redacción» (`redaccion.html`) siguió en una columna de 44rem, con líneas de unos 90 caracteres y unos 8.750 px
de alto a 1366 px. Juanjo (11-11-2026): «La redacción se muestra en una columna, ¿no habría que hacer como el
resto de artículos, en columnas?». Es la página de texto más larga del diario después del reportaje.

## Decisión

- **Desde 60rem de ancho, como las noticias** (`en-columnas`, 76rem de ancho): la cabeza es la de una noticia
  sin dibujo (`cabeza_pieza()`), con el titular a lo ancho y la entradilla en dos columnas (ADR 0045), y lleva
  el mismo botón «Una columna» / «Columnas», con la misma elección recordada para todo el diario.
- **«Cómo se hace cada número», en dos columnas** (`.red-proceso`): la primera empieza por el organigrama y el
  texto sigue detrás y pasa a la segunda. El organigrama es vertical (716 × 1040): a media página queda a
  unos 590 px de ancho, casi como antes, y las dos columnas se igualan solas con el texto.
- **El resto, en bloques a lo ancho con el texto en tres columnas** (`.red-bloque`, `columns: 3 19rem`, de
  50 a 60 caracteres por línea): «El equipo», con el título a todo el ancho, y los apartados de `secciones`
  agrupados por tema en `BLOQUES_REDACCION`: cómo trabajan los agentes; las secciones del diario; quién lo
  lee y quién lo hace. En los bloques de varios apartados, cada título va en su columna, pegado a su texto.
- **El último bloque empieza por «Las comunidades»** (después, «Si participas en los grupos», «Las personas»,
  «El código», «Las visitas» y «Contacto»): el diagrama de los grupos no se puede partir y, en medio del
  bloque, dejaba unos 190 px vacíos al pie de la última columna; arriba de la primera, las columnas se
  igualan. Este orden vale también en una columna y en el móvil.
- **Sin mínimo de líneas a la cabeza o al pie de columna** (`orphans` y `widows` a 1) en estos bloques: con
  dos, Chromium no igualaba las columnas y dejaba huecos de 100 a 130 px en inglés y en euskera.
- **El título nunca se queda solo al pie de una columna**: `break-after: avoid` y, para Safari, que no lo
  respeta en columnas, un relleno inferior de 2,4em que no se puede partir y que no ocupa sitio (margen
  negativo). Con 3,4em volvía un hueco de 128 px en euskera a 1000 px.
- **En una columna, en el móvil, en la tableta en vertical y al imprimir**, la página es la de antes, salvo el
  nuevo orden del último bloque.

## Alternativas descartadas

- **El organigrama a la derecha y «Cómo se hace» a la izquierda**, como la cabeza de una noticia: el texto
  medía de 60 a 260 px más que el dibujo según el idioma, y al ensanchar el dibujo crecía también el texto.
- **Cada apartado con su título a todo el ancho**, como los ladillos de las noticias: los apartados cortos
  («Las personas», «Contacto») quedaban repartidos en tres columnas de una o dos líneas.
- **Todos los apartados seguidos en tres columnas**: cada columna mediría unos 1.500 px, más que una
  pantalla, y habría que subir y bajar por toda la página.

## Consecuencias

- A 1366 px, la página pasa de unos 8.750 px de alto a unos 5.350.
- Un apartado nuevo en `secciones` sale en un bloque propio al final mientras no se añada su posición a
  `BLOQUES_REDACCION`; el orden de `secciones` tiene que ser el mismo en los cinco idiomas.

## Validación

Medidas con Playwright, con un script que calcula dónde acaba cada columna de cada bloque y si algún título
queda separado de su texto, en Chromium, Firefox y WebKit, en los cinco idiomas, a 1000, 1280, 1366 y 1600 px:
sin diferencias de más de 90 px ni títulos sueltos. `scripts/revisar-maqueta.js` en escritorio, tableta y
móvil, y con una columna, y `scripts/revisar-anchos.js`, en los cinco idiomas. El modo de una columna,
comparado con la página anterior en captura.
