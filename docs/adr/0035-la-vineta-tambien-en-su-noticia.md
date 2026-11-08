# 35. La viñeta, también debajo de la noticia de la que trata

Fecha: 2026-11-08 · Estado: aceptado

## Contexto

La viñeta de Tiza y Algoritmo salía en la portada del número y en la página de viñetas, con un enlace a su
noticia («A partir de…»), pero la noticia no la mostraba. Quien llega a una noticia desde un aviso, las
redes o el buscador no la veía. Juanjo preguntó si tendría sentido que saliera también al final del artículo
del que trata (08-11-2026) y lo aprobó, debajo de las fuentes y no antes: «las fuentes son del artículo, no
de la viñeta».

## Decisión

- La página de la noticia de la que trata la viñeta (`elegida.pieza` de `vinetas/FECHA.json`) la muestra
  justo después del artículo, tras «Comprobado en», y antes de «Más en…» y de los comentarios:
  `bloque_vineta(..., pieza=p["id"])` en `articulo()`.
- El mismo bloque que en la portada (rótulo que lleva a la página de viñetas, fecha y tira), sin la línea
  «A partir de…», que remitiría a la propia página.
- Fuera del `<article>`, así que el buscador no mezcla los diálogos de la tira con el texto de la noticia.
- En los cinco idiomas y en todo lo ya publicado, porque la web se rehace entera.
- Una viñeta que trata de un breve sin decir cuál (`"pieza": "breve"`, como la del 5 de noviembre) no sale
  en ninguna noticia: no hay forma segura de saber de cuál es.

## Validación

Generado en una copia aparte: la tira sale en las diez noticias de las que trata una viñeta (del 28 de
octubre al 7 de noviembre, salvo el 5, que era de un breve), en los cinco idiomas. Probado con `probar-web` en
Firefox y Chromium, escritorio y móvil, claro y oscuro: se ve igual que en la portada y sin errores propios
(los únicos, 404 de giscus en una noticia sin comentarios todavía, que es lo normal).
