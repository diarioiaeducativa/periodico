Rúbrica VCER: Recomendable (100 %)
Versión evaluada: la web publicada el 05-11-2026 (sitio en el commit `03a4665` de
`diarioiaeducativa/diarioiaeducativa.github.io`, redacción en el `7be4fbf` de
`diarioiaeducativa/periodico`). El diario no tiene número de versión.

Cumple lo esencial de la guía y puede utilizarse o publicarse; las mejoras propuestas lo completan.

Rúbrica: la de la versión 3.0 de la guía *Vibe coding responsable* (De Haro, 2026,
<https://doi.org/10.5281/zenodo.24073199>). El punto 2 se puso al día el 09-11-2026, con el contador
de visitas del 08-11 y la caducidad de la cuenta de la visita en el navegador; el resto es la evaluación del
05-11-2026. Los 13 meses son la duración que pone de ejemplo la AEPD y los 25 meses, su plazo máximo de
conservación: Agencia Española de Protección de Datos (2024), *Uso de cookies para herramientas de
medición de audiencia* (versión de enero de 2024), apartado III.A «Garantías mínimas», garantías 2 y 3,
p. 4, <https://www.aepd.es/guias/guia-cookies-analiticas-externas.pdf>.

Es la segunda evaluación del día. La primera, sobre el sitio `4fd8423` y la redacción `da8b513`,
dio un 90 %, con un 1 en los puntos 1 y 10; lo que se corrigió está en el ADR 0019 y en la
sección «Cambios desde la primera evaluación».

## Puntuación

| # | Punto | Nota | Justificación |
|---|---|---|---|
| 1 | Contenido | 2 | Se comprobaron unas 80 afirmaciones de las 6 piezas del número del 5 de noviembre contra sus fuentes, abriendo cada enlace. Los dos errores y las imprecisiones que salieron en la primera evaluación están corregidos en la web, en los dos idiomas, y no se ha detectado ninguno más. Conviene que una persona compruebe, de vez en cuando, que las fechas con que una pieza remite a otra son las de publicación: era un fallo sistemático, ya corregido en el encargo (ADR 0011). |
| 2 | Datos personales | 2 | No pide datos. Desde el 08-11-2026 lleva un contador de visitas (ADR 0033) que la rúbrica admite: en el propio servidor de quien publica, sumado por página y por hora, sin cookies, IP, navegador ni procedencia, explicado en «La redacción» y con los datos borrados a los 25 meses. En el navegador guarda el tema, el idioma y la cuenta de la visita en curso (hora de la última página y páginas ya contadas), nada que distinga a quien lee; la cuenta de la visita caduca a los 13 meses, y el tema y el idioma, preferencias de quien lee, se recuerdan sin caducar. El buscador (Pagefind) funciona dentro del sitio. Nombra solo a quien publica un recurso propio (ADR 0018) y no atribuye opiniones. No maneja datos del alumnado. |
| 3 | Entender qué hace | 2 | Cada noche, unos agentes de IA leen las conversaciones de ayer de tres grupos de Telegram y redactan, revisan, dibujan y traducen el número. Después, unos programas sin IA montan una web estática y la publican a las 7:00. Solo se comunica con GitHub (para publicar) y con el Bot de IA Educativa (para los avisos). «La redacción» y el README lo describen así, y coincide con el código: modelos por paso, horarios y umbral de 4 piezas. |
| 4 | Dependencias | 2 | No carga nada de fuera: la letra, los iconos, los dibujos, las capturas y el vídeo están dentro del sitio. Las direcciones externas son solo enlaces: las fuentes de cada pieza, los mensajes de Telegram (t.me), Instagram, Lucide, Newsreader, Creative Commons, bilateria.org, el portafolio de Raül Torres, el repositorio del código y la página de la evaluación VCER. Descargado y abierto sin internet, se lee entero, con sus dibujos, capturas y vídeo; lo que no funciona son esos enlaces externos. El buscador abierto como archivo local no se ha probado. |
| 5 | Accesibilidad | 2 | Ver «Pruebas de accesibilidad» debajo de la tabla. |
| 6 | Material ajeno | 2 | Hay tres elementos ajenos. **Letra:** Newsreader (Production Type), con licencia OFL; el pie enlaza `fuentes/OFL.txt`. **Iconos:** los de Lucide (ISC), acreditados en el pie con su licencia en `LICENSE-LUCIDE.txt` y con una nota en cada SVG. **Capturas:** las de los recursos del repositorio de VCE, cada una con su ficha de nombre, autoría y licencia. La música de los vídeos se compone por programa. |
| 7 | Rastro | 2 | Hay 20 ADR, con el contexto, las alternativas y la evidencia de cada decisión, y ahora son públicos. |
| 8 | Uso de IA | 2 | El pie y «La redacción» dicen qué hace la IA y qué hacen programas corrientes. También dicen qué se comprueba y quién lo comprueba (agentes revisores que no han escrito lo que revisan), que unas personas lo idean, lo diseñan y lo supervisan, y que aun así puede haber errores. La traducción al catalán se declara automática. |
| 9 | Licencia | 2 | El pie lleva «© 2026 Juan José de Haro y Raül Torres» y CC BY-SA 4.0 enlazada. Los dos repositorios tienen sus archivos de licencia y el README del sitio ya coincide con el pie. |
| 10 | Reutilización | 2 | El código está completo y es público: el generador, los scripts de la noche y los encargos de los agentes en `diarioiaeducativa/periodico`, y el sitio en `diarioiaeducativa/diarioiaeducativa.github.io`, con AGPL v3. Es legible y está comentado, sin comprimir, y el README explica cómo cambiar el aspecto y los encargos, probar una noche sin publicar y adaptarlo a otra comunidad. |

### Pruebas de accesibilidad (punto 5)

- **axe-core 4.13** en 15 páginas publicadas, en tema claro y oscuro, con el buscador lleno y el visor abierto: ningún aviso.
- **Teclado:** recorrido con el tabulador de una pieza, con 49 elementos, todos con el foco visible. El visor se abre con Intro y lleva el foco a la X. El tabulador ya no lo saca del visor, y Esc lo cierra y devuelve el foco a la imagen.
- **Pantalla estrecha:** a 320 px no hay desbordamiento ni errores de JavaScript, en Chromium, Firefox y WebKit.
- **Imágenes:** todas tienen texto alternativo, y el de los dibujos recoge sus rótulos.
- **Color:** las secciones se distinguen también por su nombre e icono, no solo por el color.

## Cambios desde la primera evaluación

- **Contenido de las piezas:**
  - **Seedance 2.5:** la pieza de la cámara virtual decía que no se había podido confirmar en una fuente oficial que el modelo admite un vídeo de referencia para la cámara. La página de ByteDance sí lo confirma, y ahora es una de sus fuentes.
  - **Fechas de remisión:** dos remisiones citaban la fecha de la carpeta y no la de publicación («31 de octubre» por 1 de noviembre y «2 de noviembre» por 3 de noviembre). Están corregidas, y `publicado.txt` y el encargo de enlaces dan ya la fecha de publicación.
  - **Raül Torres:** se le presenta como administrador de EduMedia-IAG y coautor del diario, y la serie que cita es la suya.
  - **Imprecisiones menores:** corregidas las de Jigsaw (los pasos y el temporizador salen tras formar los grupos, y los niveles son los de la ficha), EduTicTac Blocs (al abrirlo sale el reproductor con «Ver dentro», no el editor) y Tongjiang (secundaria superior, no Bachillerato), además de una errata.
- **Accesibilidad:** la mancheta es el `h1` de la página de cada número, sin ningún cambio visible (384 capturas comparadas píxel a píxel), y el visor retiene el foco.
- **Licencias:** licencia de Lucide en el sitio y enlace a la de la letra en el pie; el © del README del sitio coincide con el pie.
- **Código:** el repositorio de la redacción es público, con historial nuevo y sin menciones a cuentas personales (ADR 0019), y tiene indicaciones para modificarlo en el README.

## Mejoras propuestas

Ninguna sube ya la puntuación; estas la consolidan:

1. **Remisiones a piezas anteriores:** comprobar en los próximos números que citan la fecha de publicación.
2. **Buscador sin internet:** probar Pagefind abriendo una copia descargada; si no funciona como archivo local, decirlo en el README.
3. **Siguiente evaluación:** repetirla cuando cambie algo de fondo (un servicio nuevo, otra forma de publicar), sobre el número de ese día.
