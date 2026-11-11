# 13. El diario se puede instalar como app, sin avisos

Fecha: 2026-11-04 · Estado: aceptado; el service worker y la app de Google Play, sustituidos por el ADR 0042

## Contexto

Juanjo preguntó si el diario podía ser una app para el móvil que avisara cuando sale cada
número. Puso dos condiciones: sin servidores y sin cargar más el NAS ni el hosting de IONOS.

Un aviso de la web (Web Push) necesita que alguien guarde la lista de suscripciones y envíe
cada aviso, es decir, un servidor. Lo que queda sin servidor es que el propio dispositivo
mire si hay número nuevo:

- una app nativa de Android que lea cada mañana un archivo del sitio y avise (sin servidor,
  pero solo Android y con ficha y revisión en Google Play);
- la sincronización periódica en segundo plano de la web instalada (Periodic Background
  Sync), que solo existe en los navegadores Chromium, exige la app instalada y deja la
  frecuencia en manos del navegador según lo mucho que se use la web: el aviso puede llegar
  horas tarde, y deja de llegar a quien deja de abrirla, que es a quien más falta hace.

Juanjo descartó también el canal de Telegram y la app de Google Play, y decidió la web
instalable **sin aviso** («sin aviso entonces»): el número ya se anuncia cada mañana a las
7:00 en los grupos.

## Decisión

- **Una ficha de aplicación por idioma** (`manifest.webmanifest` en la raíz y en `ca/`), que
  genera `generar.py` (`manifiesto()`): nombre, nombre corto («Diario IA», «Diari IA»), lema,
  pantalla completa (`standalone`), los colores de la cabecera e iconos de 192 y 512 px,
  además de uno adaptable (`maskable`) con el dibujo dentro de la zona segura. La instalada
  desde `/ca/` abre la edición catalana; la de la raíz, la castellana, que ya salta al catalán
  si así lo eligió quien la usa o si su sistema está en catalán.
- Los iconos salen de `estaticos/favicon.svg` (Tiza y Algoritmo) con `rsvg-convert`; el
  adaptable, del mismo dibujo al 78 % sobre fondo entero.
  *Desde el 11-11-2026, los de la app salen de `scripts/iconos.py`, con el dibujo de la imagen de vista
  previa (ADR 0048), y `favicon.svg` es una versión simplificada del mismo dibujo.*
- **Un enlace «Instalar la app» en el pie**, junto a «La redacción» y «RSS», que solo
  aparece donde el navegador deja instalar con un toque (evento `beforeinstallprompt`:
  Chrome y Edge, en el móvil y el ordenador). Se evita así la barra que Chrome pondría sola
  al entrar: nada interrumpe a quien llega a leer. En iPhone y iPad, donde no hay ese botón,
  una línea explica que se puede añadir a la pantalla de inicio desde el botón de compartir
  del navegador. Con la app ya instalada no sale nada.
- **Sin service worker**: Chrome ya no lo exige para instalar, y sin él la app siempre
  enseña lo publicado, sin copias guardadas que haya que invalidar.
  *Desde el 09-11-2026 hay service worker (ADR 0042), para leer sin conexión y para la app de
  Google Play; con conexión sigue enseñando siempre lo publicado.*
- **Sin avisos**: ni Web Push ni sincronización periódica.

## Alternativas descartadas

- **Web Push** (como en Temps a Montflorit, ADR 0048 de meteo-local): necesita servidor para
  las suscripciones; descartado por las condiciones.
- **App nativa de Android que comprueba el RSS** y **app de Google Play** en general:
  descartadas por Juanjo.
- **Canal de Telegram del diario**: descartado por Juanjo.
- **ntfy.sh, Firebase Cloud Messaging u OneSignal**: dependen de un servidor ajeno; los dos
  últimos, además, de Google o de una empresa que rastrea a quien se suscribe.
- **Sincronización periódica en segundo plano**: poco fiable (véase el contexto).
- **Lector de RSS con avisos** (Feeder): sigue disponible para quien quiera, con el
  `feed.xml` de siempre, pero avisa de cada pieza y no enseña el diario tal como es.

## Consecuencias

- No se toca el NAS ni IONOS: los archivos nuevos se publican en GitHub Pages con el resto
  del sitio, cada mañana.
- Quien instala la app sigue enterándose del número por los grupos; la app solo le ahorra
  buscar la dirección.

## Evidencia

- Criterios de instalación y `beforeinstallprompt`: documentación de Chrome
  (https://web.dev/learn/pwa/installation-prompt, https://web.dev/articles/install-criteria).
- Sincronización periódica: https://developer.chrome.com/docs/capabilities/periodic-background-sync (solo instalada,
  frecuencia según el uso de la web).

## Riesgos y limitaciones

- Firefox para Android y Safari no tienen `beforeinstallprompt`: en Firefox no sale el enlace,
  aunque se puede instalar desde su menú.
- Sin service worker, la app no funciona sin conexión.
- La línea de iPhone e iPad se decide por el agente de usuario: un navegador que se haga
  pasar por otro puede ver la línea que no le toca.

## Validación

04-11-2026, con el sitio generado en local y servido en `127.0.0.1`:

- Chromium de Playwright con perfil propio y `--bypass-app-banner-engagement-checks`:
  `Page.getInstallabilityErrors` sin errores y `Page.getAppManifest` sin errores en `/`,
  `/ca/` y una pieza; `beforeinstallprompt` llega y el enlace del pie aparece. Sin errores de
  JavaScript.
- Con agente de usuario de iPhone: sale la línea de la pantalla de inicio y no el enlace.
- Firefox y WebKit de Playwright: sin enlace y sin errores de JavaScript.
- No probado en un móvil real: queda por ver la instalación con el dedo en Android y el
  icono adaptable en el lanzador.
