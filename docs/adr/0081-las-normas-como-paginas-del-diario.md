# 81. Las normas, como páginas del diario

Fecha: 2026-11-16 · Estado: aceptado

## Contexto

El ADR 0080 enlazó desde «La redacción» los tres documentos de normas (`docs/como-se-hace.md`,
`encargos/estilo.md` y `encargos/traduccion.md`) en GitHub. Allí se leen rodeados de los menús de GitHub,
que no son del diario. Se pidió una página propia, que siga al documento cuando este cambie.

## Decisión

- `generar.py` lee los tres `.md` cada vez que monta la web y escribe `normas.html`, `estilo.html` y
  `traduccion.html`, con la cabecera, el pie y la tipografía del diario (`pagina_documento`). Un cambio en
  un documento sale en la web con la siguiente publicación, sin tocar nada más.
- Un convertidor propio (`doc_html`, `doc_linea`) para lo que usan estos documentos: títulos, párrafos,
  listas, tablas (con el estilo de las del reportaje, en fichas en el móvil), citas, negritas, cursivas,
  código y enlaces. No se añade ninguna dependencia ni hay que reconstruir el contenedor.
- Maqueta de artículo largo: el primer párrafo de entradilla, el texto en columnas en el ordenador con el
  botón «Una columna» (ADR 0044) y el botón «Escuchar» (ADR 0073). Los títulos de los apartados van dentro
  de las columnas, como en «La redacción», sin partirse ni quedarse solos al pie de una, para que los
  apartados cortos no dejen huecos; solo las tablas cortan las columnas, y un texto muy corto entre dos
  tablas (menos de 400 caracteres) va a lo ancho.
- Los enlaces entre los tres documentos llevan a sus páginas; cada mención «ADR 0026» enlaza a ese
  registro en GitHub, y lo demás del código, también a GitHub.
- Solo en castellano, en la raíz. «La redacción» de cada idioma enlaza a ellas y dice que están en
  castellano; en estas páginas, el selector de idioma lleva a «La redacción» de cada lengua y no se
  anuncian versiones en otros idiomas.

## Consecuencias

- El lector no sale del diario para leer cómo se hace.
- Un documento que use algo que el convertidor no conoce (tablas con barras dentro de una celda, listas
  anidadas) se vería mal: hay que mirarlo en la web al cambiar su forma.
- Las páginas no entran en el buscador del diario ni en el mapa del sitio, que es por idiomas.

## Validación

Las tres páginas generadas y miradas en Chromium y Firefox, en escritorio y móvil (16-11-2026). En
Firefox móvil, la de normas es más larga de lo que admite la captura de la herramienta de prueba; la
página en sí carga bien.
