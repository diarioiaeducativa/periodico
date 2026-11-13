# 54. Edición en papel: cada pieza y cada número, impresos desde el navegador

Fecha: 2026-11-13 · Estado: aceptado

## Contexto

Juanjo pidió (13-11-2026) una edición en papel del diario, y que también se pudiera imprimir cada noticia por
separado. Guardar un PDF de cada número ocuparía mucho: el de un número de once piezas pesaba unos 5 MB con la
maqueta de pantalla y unos 2 o 3 MB con una de papel; en los cinco idiomas, de 2 a 5 GB al año, más de lo que
admite GitHub Pages (1 GB por web).

## Decisión

- **Sin guardar ningún PDF**: lo hace el navegador de quien lo pide, con una maqueta de papel (`@media print` al
  final de `estaticos/diario.css`). El diálogo de imprimir deja elegir impresora o «Guardar como PDF».
- **Cada pieza** (también el reportaje del domingo) tiene el botón «Imprimir» junto a «Compartir».
- **Cada número** tiene su página `FECHA/papel.html`, en los cinco idiomas, con el sumario por secciones, todas sus
  piezas enteras (las mismas de su página, sin botones), la viñeta y los breves. Se llega desde el icono de
  impresora de la cabecera de la portada y de cada número, y desde «Edición en papel» en la hemeroteca; con
  `?imprimir=1` se abre el diálogo de imprimir al cargar. No se indexa (`noindex`, sin `data-pagefind-body`):
  repetiría cada pieza.
- **La maqueta de papel**: A4, papel blanco aunque la pantalla esté en tema oscuro, sin menú, botones, comentarios
  ni pie; arriba, el nombre del diario, el número y la fecha; el texto a dos columnas; la viñeta en fila; sin letra
  capitular (al final de una página se quedaba sola); los dibujos, de 52 mm de alto como mucho, para que el título,
  la entradilla y el dibujo quepan juntos.
- **Lo que en el papel no se puede pulsar**: al final del texto y dentro de sus columnas, el enlace a la
  conversación y las fuentes con su dirección escrita (fuera de las columnas se quedaban solas en una página casi
  vacía); arriba a la derecha de cada pieza, un QR con su dirección y la dirección debajo. El QR lo dibuja segno
  (BSD-3-Clause, sin dependencias, en el `Dockerfile`) al montar el sitio, en SVG escalable; sin segno, la pieza
  sale sin QR. Lo que es solo de papel (`.solo-papel`) no sale nunca en pantalla.
- **Lo que dice el pie de la web, también en el papel** (13-11-2026, ADR 0055): el pie no se imprime, así que
  la edición en papel no decía que el texto lo redacta una IA y lo revisa una persona, ni que una edición
  traducida es una traducción automática, ni de quién es ni su licencia. Ahora lo lleva al final (`creditos_papel()`):
  en una pieza suelta, tras sus fuentes; en el número entero, una sola vez, al final.
- **Los dibujos, con los colores del tema claro** aunque se esté leyendo en oscuro: con el tema oscuro elegido,
  las secciones y los rellenos de los dibujos se imprimían con sus colores oscuros sobre papel blanco. Un
  bloque `@media print` al final de `comun.css` repone los claros.

## Alternativas descartadas

- **Guardar los PDF** en la web o en Internet Archive: el espacio, y un paso más cada noche que puede fallar.
- **El QR al final de la pieza**: el reparto de las columnas lo mandaba a veces solo a una página nueva.
- **Una biblioteca de QR en JavaScript**: código de terceros en cada página; con segno, el QR llega hecho.

## Consecuencias

- El resultado depende algo del navegador: Chrome y Edge lo hacen mejor; Firefox, bien; Safari, algo peor con las
  columnas.
- Medido con 27 piezas de cuatro días: casi todas en una o dos páginas; alguna acaba con una última página corta
  cuando el texto llena de verdad la anterior. El número del 13-11-2026, con 11 piezas, ocupa 14 páginas.

## Validación

PDF de Chromium (la misma maqueta que imprime Chrome) de una pieza, de 27 piezas y de dos números enteros,
revisados página a página; la página de pantalla, con `revisar-maqueta.js` en Chromium, Firefox y WebKit, en
ordenador y móvil y en los cinco idiomas; lo solo de papel, oculto en pantalla y visible al imprimir en los tres
navegadores.
