# 32. Para tu web: widget, canales RSS y piezas republicables

Fecha: 2026-11-08 · Estado: propuesto

## Contexto

Juanjo quiere que la gente pueda poner las noticias del diario en su blog, la web de su centro o su
aula virtual, de forma versátil (08-11-2026: «como se puede hacer para que sea algo versatil y util?»).
Ya había un RSS por idioma (`feed.xml`) con el titular, la entradilla y el enlace de cada pieza, pero
sin dibujo, sin forma de elegir una parte del diario y sin nada para quien no sabe qué es un RSS o usa
una plataforma que no lo lee (Google Sites, eXeLearning). Se le propusieron tres piezas (canales RSS
completos, un widget para incrustar y un botón para republicar una pieza entera) y pidió las tres
(«hazlo todo»).

## Decisión

- **Página «Para tu web»** (`para-tu-web.html`, en los cinco idiomas, enlazada desde el pie): el
  configurador del widget a la vista, con vista previa en vivo y el código para copiar; plegados debajo,
  la tarjeta de una pieza, los canales RSS y las condiciones para republicar.
- **Widget** (`insertar.html`, uno por idioma): una página sin cabecera ni pie, pensada para un
  `<iframe>`. Todo va en la dirección: `seccion` (una sección, `reportaje` o `breves`), `grupo`
  (`chatgpt`, `vce`, `edumedia`), `n` (1 a 20), `estilo` (`tarjetas` con dibujo, por defecto desde el 08-11-2026 a petición de Juanjo, o `lista`), `tema` (`claro`,
  `oscuro`; sin él, el del sistema de quien mira) y `pieza=AAAA-MM-DD/id` para la tarjeta de una sola
  pieza. Los enlaces se abren en otra pestaña. Lee `noticias.json` o `noticias-<filtro>.json` (las 50
  últimas) y, para una pieza, `datos/AAAA-MM.json` (todo lo de ese mes). Sin cookies ni contadores.
  El configurador calcula un alto según el número de piezas y el aspecto, y deja escribir otro; si el
  contenido no cabe, se desplaza dentro del marco, y en la tarjeta de una pieza el dibujo se encoge.
- **Botón «Para tu web» en cada pieza y reportaje**, junto a «Compartir»: despliega «Tarjeta para tu
  web» (copia el `<iframe>` de esa pieza), «Noticia completa» (copia la pieza entera con formato, para
  el editor de un blog, y como HTML, para un bloque de código) y el enlace a la página. El editorial no
  lo lleva: no entra en el widget ni en los canales.
- **La pieza republicable** lleva antetítulo, titular, entradilla, dibujo, cuerpo con los enlaces
  completos, fuentes, enlace a la conversación y, al final, «Publicado originalmente en el Diario de IA
  Educativa el…», el © de Juanjo y Raül, la licencia CC BY-SA 4.0 y cómo se redactó, en palabras que se
  entienden fuera del diario (nombra los tres grupos). En las otras lenguas, también el aviso de
  traducción automática. Va en un `<template>` fuera del `<article>`, para que Pagefind no la cuente
  dos veces.
- **Canales RSS**: el general (`feed.xml`, las 100 últimas) y uno por sección, reportaje, breves y
  grupo (`feed-<clave>.xml`, las 50 últimas), en cada idioma. Cada pieza lleva su dibujo
  (`media:content`), y el canal, la licencia (`copyright`) y el icono del diario (`image`).
- **Dibujos sueltos**: cada dibujo se publica también como archivo (`ilustraciones/AAAA-MM-DD-id.svg`
  en cada idioma) con un `<style>` dentro, sacado de las reglas `.ilu` de `comun.css`, en el que cada
  variable lleva como reserva el color claro de su sección. Con `<img>` (RSS, pieza republicada) se ve
  con sus colores; dentro del widget, que lo inserta en la página, mandan las variables del tema, también
  el oscuro.

## Alternativas descartadas

- **Pegado automático en WordPress (oEmbed)**: WordPress incrusta solo a los proveedores de su
  lista; para el resto exige permisos y es frágil.
- **Widget con JavaScript en lugar de iframe**: Google Sites, Moodle y muchos editores quitan los
  scripts; el iframe entra en todos y aísla los estilos.
- **Ajuste automático del alto** (el widget avisa a la página que lo contiene): necesita un script en la
  web ajena, que esas plataformas quitan. Se sustituye por un alto calculado y editable.

## Consecuencias

- El sitio crece por idioma en unos 13 canales, 13 JSON, un JSON por mes y un SVG por pieza (unos 4 KB).
- Quien republica guarda una copia que no cambia si la pieza se corrige o se retira; la página lo dice y
  pide hacer lo mismo, y el enlace al original lleva a la versión al día. El widget no tiene ese
  problema: lo que se retira del diario desaparece también de las webs que lo incrustan.
- El nombre de los parámetros y de los archivos (`insertar.html`, `noticias*.json`, `feed-*.xml`,
  `datos/`) queda fijo: cambiarlo rompería los widgets ya pegados en otras webs.

## Evidencia

- GitHub Pages no envía `X-Frame-Options`: sus páginas se pueden incrustar en cualquier web.
- Licencia de los textos y dibujos: CC BY-SA 4.0 (pie del diario), que permite republicar citando y con
  la misma licencia.

## Riesgos y limitaciones

- Sin HTTPS, el navegador no deja usar el portapapeles moderno: se copia con un campo oculto, sin
  formato. En el sitio publicado (HTTPS) se copia con formato.
- Un lector de RSS puede no mostrar un SVG; el texto llega igual.
- El tema «del sistema» del widget sigue el del dispositivo de quien mira, no el botón de tema de la web
  que lo incrusta, que el widget no puede conocer.

## Validación

- 08-11-2026, en una copia con los datos del día, servida en la red de casa: widget en lista, tarjetas y
  pieza, incrustado en una página de otro origen, en Chromium, Firefox y WebKit, escritorio y móvil,
  temas claro y oscuro, en castellano, catalán, gallego y euskera; sin errores de JavaScript ni
  desbordamiento.
- El configurador cambia la vista previa y el código al tocar cada control, y «Copiar el código» copia
  en los tres navegadores. El menú de la pieza se abre dentro de la pantalla del móvil.
- La pieza republicada, pegada en una página ajena: dibujo con sus colores y tabla del reportaje sin
  ensanchar la página en el móvil.
- axe-core (WCAG 2 A y AA y buenas prácticas) sin fallos en la página, el menú de la pieza y el widget,
  en claro y oscuro.
- Los canales, validados como XML.
