# 44. Las noticias, en columnas de periódico en el ordenador

Fecha: 2026-11-09 · Estado: aceptado

## Contexto

En el ordenador, la página de cada noticia era una columna de 44rem centrada: el dibujo, a todo ese ancho,
ocupaba unos 410 px de alto entre la entradilla y el texto, y la viñeta, en vertical (ADR 0035), más de
1.000 px. La noticia del 7 de noviembre sobre la memoria de los agentes medía 4.536 px a 1366 px de ancho,
y casi la mitad no era texto. Juanjo (09-11-2026): «sale estrecho, ocupa mucho en vertical y sin embargo
las imágenes son grandes». Se descartó poner el texto en dos columnas anchas: las líneas seguían teniendo
unos 80 caracteres, casi como antes, y Juanjo recordó que «lineas largas cuestan de leer, por eso se
inventaron las columnas».

## Decisión

- **Desde 60rem de ancho** (el corte de la portada), las noticias y el reportaje (`articulo()` y
  `articulo_reportaje()`, clase `en-columnas`) ocupan el ancho del diario, 76rem:
  - **la cabeza** (`cabeza_pieza()`): antetítulo, titular y entradilla a la izquierda y el dibujo a la
    derecha, a la mitad del ancho, como la principal de la portada; sin dibujo, el texto a 52rem como mucho;
  - **el texto en columnas de periódico** de 55 a 60 caracteres (`columns: 3 19rem`): tres en pantalla
    ancha y dos en la estrecha, justificado, con guiones y con filete entre columnas;
  - **los ladillos, las claves, las tablas, las figuras y los recursos cortan las columnas**
    (`column-span: all`): cada apartado se lee en su bloque, sin subir y bajar por toda la página;
  - en «La semana del repositorio», la captura y el texto de cada recurso fluyen en las mismas columnas,
    una detrás de otro, y las columnas quedan igualadas;
  - «Comprobado en», con la lista en columnas; la viñeta, con las tres viñetas en fila, como en la portada;
    «Más en…», en dos columnas; los comentarios, a 44rem.
- **Por defecto, en columnas.** Un botón, «Una columna» / «Columnas» (`boton_columnas()`, en los cinco
  idiomas, con los iconos `text-align-justify` y `columns-3` de Lucide), pasa al diseño anterior y vuelve.
  Va en la línea de la sección, entre su nombre y la fecha; en una pieza sin sección, con la fecha, en la
  línea del antetítulo. Juanjo prefería al principio un botón flotante abajo a la derecha; vio las dos
  posiciones en la prueba y se quedó con esta: está junto a lo que cambia y no tapa el texto.
- **La elección vale para todas las noticias y se recuerda en el dispositivo** (`diario.columnas` en
  `localStorage`, solo cuando se elige una columna), como el tema. La aplica un script de la cabeza antes
  de pintar (clase `una-columna` en `<html>`), sin salto al entrar. La política de privacidad
  (`redaccion.html#privacidad`) lo dice en los cinco idiomas.
- **En el móvil, la tableta en vertical y la impresión, nada cambia**: no hay botón y todo sigue en una
  columna. Los breves tampoco cambian.
- **Una columna es el diseño anterior tal cual**, con el texto a 44rem: más ancho, las líneas serían aún
  más largas.
- **De paso, en una columna y en la tableta**, la captura de cada recurso de «La semana del repositorio»
  flota a la derecha y el texto sigue por debajo de ella. Iba en una columna propia al lado del texto, y
  cuando el texto era más largo dejaba debajo de la captura un hueco de 230 a 290 px, que la revisión de
  maqueta encontró también en lo ya publicado (ADR 0041).

## Alternativas descartadas

- **Dos columnas anchas**: unos 80 caracteres por línea; no resolvía las líneas largas.
- **El dibujo en una de las tres columnas**, con la cabeza más baja: los rótulos de los dibujos se
  reducían a dos tercios, y la página no salía más corta (2.888 px frente a 2.915 en la noticia de la
  memoria, 3.582 frente a 3.567 en la de Debates y 9.318 frente a 8.750 en el reportaje).
- **El texto de cada recurso en dos columnas y la captura en la tercera**, como en la prueba: el texto
  quedaba más bajo que la captura y dejaba huecos de 100 a 300 px.
- **«Comprobado en» al lado de los botones de compartir**, como en la prueba: con muchas fuentes (el
  reportaje tiene decenas) dejaba un hueco a la izquierda (ADR 0041). Va debajo, a todo el ancho.
- **El botón flotante**: tapaba el final de la tercera columna; como la elección se recuerda, basta verlo
  al abrir la noticia.
- **Recordar la elección solo en la noticia que se lee**: quien prefiere una columna tendría que pulsarlo
  en cada una.

## Consecuencias

- La noticia del ejemplo pasa de 4.536 a 2.915 px de alto a 1366 px; la de Debates del 7 de noviembre, de
  5.486 a 3.567; la semana del repositorio, de 6.938 a 5.393; el reportaje del domingo, de 12.055 a 8.750.
- La viñeta bajo su noticia (ADR 0035) va en fila en columnas y en vertical en una columna.
- Las reglas viven al final de `estaticos/diario.css`, todas bajo `html:not(.una-columna) .en-columnas`
  y la media de 60rem: cualquier pieza nueva de la noticia que tenga que cortar las columnas se añade a la
  lista de `column-span: all`.

## Evidencia

Prueba con nueve piezas (corta, larga, sin dibujo, multimedia, la semana del repositorio, el reportaje, un
breve y una en catalán) servida en local, y medidas de altura con Playwright en Firefox, a 1366 y 412 px.

## Riesgos y limitaciones

- `column-span: all` es necesario para que un apartado no se reparta por toda la página: lo admiten
  Chromium, Firefox (desde la versión 71) y Safari.
- Una noticia muy larga sin ladillos haría columnas más altas que la pantalla; hoy la más larga sin
  ladillos (unas 620 palabras) queda en unos 750 px.

## Validación

Generado entero en local y probado con `probar-web` en Chromium y Firefox, en escritorio, tableta y móvil,
y además a 1000, 1280 y 1920 px de ancho, con `scripts/revisar-maqueta.js` (ADR 0041) en todas las noticias
en castellano y en una muestra de cada idioma, también en el modo de una columna y en WebKit: sin avisos de
maqueta ni desbordamientos. El botón, probado
al pulsarlo, al pasar a otra noticia y al volver; en el móvil y en los breves no aparece.
