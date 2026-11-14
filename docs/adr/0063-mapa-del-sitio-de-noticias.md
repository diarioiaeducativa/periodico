# 63. Mapa del sitio de noticias

Fecha: 2026-11-14 · Estado: aceptado

## Contexto

Juanjo preguntó el 14-11-2026 cómo conseguir que Google trate el diario como un medio de prensa y lo saque en
Google Noticias. Desde 2024 no se puede dar de alta una publicación a mano en Publisher Center, y desde 2025
Google crea solo la ficha de cada medio: entra lo que reconoce como noticia y cumple sus políticas de
contenido. No hay trámite; solo se le puede poner fácil. El diario ya tenía lo que piden esas políticas
(fechas y firma claras, «La redacción», página de contacto) y los datos estructurados de cada pieza (ADR 0039),
con la imagen en PNG de 1200 × 630 desde el ADR 0059. Faltaba el mapa del sitio para noticias, la señal más
directa de que un sitio publica noticias y de cuáles son las nuevas. Juanjo aprobó hacerlo.

## Decisión

- **`sitemap-news.xml`** en la raíz, con el formato de Google para noticias: las piezas, reportajes,
  presentaciones y breves que salieron en las últimas 48 horas, en los cinco idiomas. Cada entrada lleva el
  nombre del diario en su idioma (`L["titulo"]`, el mismo que firma la pieza en sus datos estructurados), el
  código de idioma, la hora de salida (las 7:00 de Madrid en UTC, `hora_de_salida()`) y el titular (el del
  breve, su primera frase, como en su página).
- La ventana se cuenta desde que se genera la web e incluye el número que sale ese día aunque se genere unos
  minutos antes de las 7:00 (`publicar-nas.sh`, a las 6:50). Como mucho, 1000 entradas, el tope de Google.
- Lo reúne `noticias_recientes()` en cada idioma y lo escribe `sitemap_noticias()` al final de `main()`.
  `robots.txt` lo anuncia junto a `sitemap.xml`.

## Alternativas descartadas

- **Meter las etiquetas de noticias en `sitemap.xml`**: Google pide que solo lleven etiquetas de noticias las
  piezas de los dos últimos días; mezclarlas en el mapa general obliga a rehacer cada entrada al caducar.
- **Solo el castellano**: las cinco ediciones son páginas propias e indexables (ADR 0026), y cada una puede
  salir en Google Noticias en su idioma.

## Consecuencias

- El mapa se renueva cada vez que se genera la web; si un día no se publica, se queda con lo de los últimos
  días, que ya habrá caducado para Google.
- Una página nueva que sea una noticia (un tipo de pieza nuevo) tiene que entrar en `noticias_recientes()`
  además de en `sitemap()`.
- Que el diario salga en Google Noticias sigue dependiendo de Google: el mapa solo le facilita encontrar lo
  nuevo. Cuando lo haga, Search Console enseñará el informe de rendimiento de Google News.

## Evidencia

- Google, [Crear un sitemap de Google News](https://developers.google.com/search/docs/crawling-indexing/sitemaps/news-sitemap):
  solo artículos de los dos últimos días; `news:name` igual al nombre con que firman las piezas;
  `news:language` en ISO 639; `news:publication_date` en formato W3C, la fecha original de publicación;
  `news:title` sin autor ni fecha; hasta 1000 entradas por mapa.
- Google, [Cómo aparecer en Google Noticias](https://support.google.com/news/publisher-center/answer/9607025?hl=es):
  la inclusión es automática para el contenido que cumple las políticas; no hay solicitud.
- Search Engine Land, [Google Publisher Center to stop allowing you to add publications](https://searchengineland.com/google-publisher-center-to-stop-allowing-you-to-add-publications-439978)
  (2024), y Search Engine Roundtable, [Google News fully transitioned to automatically generated publication pages](https://www.seroundtable.com/google-news-automatically-generated-publications-39149.html) (2025).

## Riesgos y limitaciones

- Hipótesis pendiente de validación: que Google lea el mapa. Se comprueba en Search Console (Indexación >
  Sitemaps) unos días después de enviarlo.

## Validación

- Web generada en una copia (14-11-2026): `sitemap-news.xml` válido como XML, con 100 entradas,
  20 por idioma (14 del número del 13-11 y 6 del 14-11, los dos que entran en las 48 horas), el nombre del
  diario en cada idioma, y las 100 direcciones existen en el sitio generado. `robots.txt` anuncia los dos
  mapas.
