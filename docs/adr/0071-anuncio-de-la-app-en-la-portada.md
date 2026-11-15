# 71. Anuncio de la app en la portada

Fecha: 2026-11-15 · Estado: aceptado

## Contexto

La app de Android salió en Google Play el 14-11-2026 (ADR 0042) y se anunció en las redes. Juanjo propuso
poner en la portada la imagen del anuncio, arriba a la derecha, unos días y con enlace a Google Play.

## Decisión

- Una franja bajo la barra de secciones, solo en la portada de cada idioma (`franja_app()` en `generar.py`;
  estilos `.promo-app` en `estaticos/diario.css`): Algoritmo con los brazos en alto, «Nueva app para
  Android», una frase y el botón a la ficha de Play en el idioma de la página (`&hl=`). Textos en `PROMO_APP`.
- Sale oculta y la enseña el navegador si tiene sentido: no dentro de la propia app (la marca de sesión
  `diario.app`, ADR 0043), ni en iPhone o iPad, que no pueden instalarla, ni si se ha cerrado con la X
  (`localStorage` `diario.promo-app`), ni pasada la fecha.
- Caduca sola: `PROMO_APP_HASTA` (22-11-2026). El generador deja de ponerla en el número que sale después, y el
  navegador la esconde desde el día siguiente aunque la página esté guardada.
- No sale al imprimir.

## Alternativas descartadas

- **La imagen de las redes tal cual**: vertical y con mucho texto; en el móvil ocupaba una pantalla entera
  antes de las noticias.
- **Un recuadro solo a la derecha**: la portada no tiene columna derecha (cada bloque va a todo el ancho) y
  habría dejado un hueco a su lado (ADR 0041).

## Consecuencias

- Pasado el 22-11-2026 el código no hace nada; se puede quitar o reutilizar cambiando la fecha y los textos.

## Validación

- Generado en una copia y servido en local: `scripts/revisar-maqueta.js` con `probar-web` en Chromium y
  Firefox, escritorio y móvil, tema claro y oscuro, sin avisos nuevos (los dos huecos que avisa ya estaban en la
  portada publicada). Juanjo lo vio en local antes de publicarlo (15-11-2026).
