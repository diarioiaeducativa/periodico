# 39. Preparado para los buscadores

Fecha: 2026-11-09 · Estado: aceptado

## Contexto

Juanjo preguntó el 09-11-2026 si el diario estaba preparado para que los buscadores lo indexaran bien.
Mirada la web publicada, las páginas lo estaban (HTML completo sin JavaScript, un título y un titular por
página, `hreflang` a los cinco idiomas, `sitemap.xml` con 495 direcciones y la portada sin salto de idioma
para los robots, ADR 0026), pero faltaban tres cosas: nadie decía a los buscadores dónde estaba el mapa del
sitio (no había `robots.txt` ni alta en Google Search Console), ninguna página declaraba su dirección
canónica y no había datos estructurados. Con el sitio recién nacido (01-11-2026) y pocos enlaces desde
otras webs, lo primero era lo que más pesaba. Juanjo aprobó hacer las tres.

## Decisión

- **`robots.txt`** en la raíz, sin vetos: solo anuncia `sitemap.xml`. Lo escribe `generar.py` junto al
  mapa, con la misma dirección base.
- **Dirección canónica** (`rel="canonical"`) en todas las páginas que pasan por `cabeza()`, salvo la 404:
  absoluta y la de su propio idioma. Así las direcciones con parámetros (`?grupo=` de la semana,
  `?nocontar=1` del contador) no cuentan como páginas distintas.
- **Datos estructurados** (JSON-LD de schema.org, `datos_noticia()`): cada pieza, reportaje y breve es
  un `NewsArticle` con su titular, la hora de salida (las 7:00 de Madrid, en UTC, la misma del RSS:
  `hora_de_salida()`), el idioma, su dirección y su dibujo si lo tiene. La firma y el editor son la
  redacción, como organización, con la dirección de «La redacción», donde se cuenta cómo se hace el
  diario y quién lo dirige. No se pone fecha de modificación, porque no se lleva. La portada de la raíz
  lleva además un `WebSite` con el nombre del diario.
- **La página de cada día se describe con lo que trae** (`descripcion_dia()`): los titulares de sus
  piezas principales, con el reportaje delante si lo tiene; hasta tres, enteros y sin pasar de 300
  caracteres. Antes las 60 repetían el lema de la portada, y en un buscador no se distinguía un número
  de otro. Es también el texto de la vista previa al compartir el número. La portada sigue con el lema.
- **Google Search Console**: el diario está dado de alta como propiedad de prefijo de URL, verificada
  con el archivo `estaticos/google0f64171555c8a8ac.html`, que tiene que seguir publicado (si se borra,
  se pierde la verificación), y con `sitemap.xml` enviado. La cuenta es la de Juanjo. Search Console no
  añade nada a las páginas ni recoge datos de quien lee: enseña lo que Google ya sabe de sus búsquedas.

## Alternativas descartadas

- **Una canónica común al castellano para todos los idiomas**: Google pide que la canónica esté en el
  mismo idioma de la página; con una sola, las otras cuatro ediciones dejarían de indexarse.
- **Firmar las piezas con nombres de persona**: la redacción es un conjunto de agentes dirigidos por dos
  personas, y eso se explica en «La redacción»; una firma personal en cada pieza diría otra cosa.
- **Fecha sin hora en `datePublished`**: Google la leería en su propia zona horaria y podría caer en el
  día anterior.
- **La imagen genérica del diario en las piezas sin dibujo**: Google pide imágenes de la pieza, no
  logotipos; las que no tienen dibujo van sin imagen.

## Consecuencias

- Los buscadores encuentran el mapa del sitio por dos vías (`robots.txt` y Search Console), pero el mapa
  es una sugerencia: Google decide qué indexa y cuándo.
- Una página nueva que deba indexarse tiene que pasar por `cabeza()` y entrar en `sitemap()`.
- El alta en Bing no se ha hecho: exige otra cuenta.

## Evidencia

- Google, [Crear y enviar un sitemap](https://developers.google.com/search/docs/crawling-indexing/sitemaps/build-sitemap?hl=es):
  el mapa se da a conocer desde Search Console o con una línea `Sitemap:` en `robots.txt`, y enviarlo
  es solo una sugerencia.
- Google, [Cómo especificar una URL canónica](https://developers.google.com/search/docs/crawling-indexing/consolidate-duplicate-urls?hl=es):
  rutas absolutas, y con `hreflang`, una canónica en el mismo idioma.
- Google, [Datos estructurados de artículo](https://developers.google.com/search/docs/appearance/structured-data/article?hl=es):
  ninguna propiedad es obligatoria; se recomiendan titular, fecha con zona horaria, imagen de la pieza
  y autor, que puede ser una organización con su dirección.

## Riesgos y limitaciones

- No se ha podido comprobar desde fuera cuántas páginas tenía ya indexadas Google: se verá en Search
  Console pasados unos días.
- Nada más enviar el mapa, Search Console lo daba como «No se ha podido obtener», sin fecha de lectura:
  Google aún no lo había leído. Queda por comprobar que lo acepta.
- Que el nombre del sitio salga en los resultados como «Diario de IA Educativa» depende de Google; el
  `WebSite` de la portada solo lo propone.

## Validación

- Web generada en local (09-11-2026): 508 páginas con una sola canónica, igual a su dirección; sin
  canónica, solo la 404 y `insertar.html` (que lleva `noindex`); 345 `NewsArticle` con JSON válido,
  fecha en UTC y la misma dirección que su canónica (260 con dibujo); un `WebSite` en la portada.
- Descripción de cada día: 12 días por idioma, las 12 distintas en los cinco idiomas, de 79 a 299
  caracteres, y ninguna con el lema.
- En la web publicada, una pieza y la portada en Chromium, Firefox y WebKit, en escritorio y en móvil:
  sin errores propios ni desbordamiento. En Chromium, la pieza anota un 404 de giscus, que es lo que
  responde su servicio cuando la pieza aún no tiene hilo de comentarios (ADR 0030).
- En la web publicada: `robots.txt` y el archivo de verificación responden, las piezas llevan su
  canónica y su `NewsArticle`, y `sitemap.xml` se descarga como XML válido con sus 495 direcciones.
  Search Console dio la propiedad por verificada y el mapa por enviado.
