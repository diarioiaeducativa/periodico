# 42. App de Android en Google Play y lectura sin conexión

Fecha: 2026-11-09 · Estado: aceptado

## Contexto

Desde el ADR 0013 el diario se puede instalar desde el navegador, sin avisos. Entonces se descartó la
app de Google Play, porque se hablaba de avisar de cada número y eso exigía un servidor. El 09-11-2026
Juanjo pidió hacer del diario una app de Android y preguntó si era el mismo proceso que con PageKeeper
(su ADR 9) y Temps a Montflorit (ADR 0082 de meteo-local). Lo que aporta, sin avisos, es estar en la
tienda: «búscalo en Google Play» lo entiende todo el mundo, y no todo el mundo sabe instalar una web.

Lo que lo condicionaba:

- Google Play rechaza a menudo una app que solo enseña una web («funcionalidad mínima»), y el diario,
  sin service worker, no funcionaba sin conexión.
- Un diario entra de lleno en la política de apps de noticias de Play, que pide una declaración en
  Play Console y cubre también las noticias escritas con IA.
- Sin gastos nuevos, sin servidores y sin cargar el NAS ni el hosting.

Juanjo aprobó la propuesta: la misma TWA de PageKeeper, más un service worker que deje leer el último
número sin conexión («sí, hazlo con el service worker»).

## Decisión

- **Lectura sin conexión con un service worker** (`estaticos/sw.js`, en la raíz del sitio para que
  cubra los cinco idiomas; lo registra `SCRIPT_TEMA` en `generar.py`):
  - **Primero la red.** Con conexión se lee siempre lo publicado, igual que antes. Así se mantiene lo
    que quería el ADR 0013 al dejarlo sin service worker: no hay copias que invalidar. Solo si la red
    no responde se sirve lo guardado.
  - **Se guarda lo que se abre** y, cada vez que llega una portada, las piezas que enlaza y sus
    imágenes. El último número se puede leer entero sin haberlo abierto pieza a pieza.
  - **Lo que no está guardado** lleva a `sin-conexion.html`, en el idioma de la página pedida. Esa
    página no lleva fecha ni número, porque se guarda al instalar y puede tener semanas; no cuenta
    visitas ni se indexa.
  - Solo se guarda lo del propio sitio, sin la consulta de la dirección (`?v=`, `?grupo=`), y hasta 400
    archivos; se quitan primero los más antiguos. No se guardan el buscador (Pagefind) ni los vídeos,
    que pesan, ni nada de otros sitios: ni el contador (ADR 0033) ni los comentarios (ADR 0030). Lo
    que el service worker descarga por su cuenta no ejecuta la página, así que no suma visitas.
  - Dentro del marco de otra web (el widget de «Para tu web», ADR 0032) no se registra.
- **Una Trusted Web Activity** generada con
  [Bubblewrap](https://github.com/GoogleChromeLabs/bubblewrap) 1.27 (Google Chrome Labs, Apache-2.0)
  en `android/`. La app abre https://diarioiaeducativa.github.io/ a pantalla completa con Chrome por
  debajo y no lleva copia de la web, así que cada número le llega sin tocarla. La portada de la raíz
  ya salta al idioma elegido o al del sistema. Identificador `io.github.diarioiaeducativa`, nombre
  «Diario de IA Educativa» y, en el lanzador, «Diario IA»; Android 7 (API 24) como mínimo y Android 16
  (API 36) como objetivo; sin notificaciones.
- **La web dice que la app es suya** con `estaticos/.well-known/assetlinks.json`, que se publica con
  el resto del sitio (`.nojekyll` ya estaba). Lleva la huella SHA-256 de la clave de subida, con la que
  se firma el APK de pruebas, y llevará la de la clave de firma de Google cuando Play la dé. Sin ese
  archivo, la app enseñaría la barra de dirección.
- **Clave de subida fuera del repositorio**, que es público: `~/.config/diario-ia-educativa/android/`
  (`upload.jks` y su contraseña en `clau.env`), con una copia en la carpeta de credenciales de Juanjo.
  `android/construeix.sh` la enlaza y compila. Con la firma de apps de Play, si se pierde, Google deja
  cambiarla.
- **La política de privacidad es el apartado de las visitas de «La redacción»**
  (`redaccion.html#privacidad`, en los cinco idiomas). Ahora dice también que el navegador guarda en el
  propio dispositivo una copia de lo leído para leerlo sin conexión, que esa copia no sale de él y que
  la app es la misma web y no recoge nada más.
- **La versión de la app va aparte de la del diario**: cambia solo con el envoltorio (icono, nombre,
  versión de Android que exige Play). Cada año, cuando Play suba la versión exigida:
  `bubblewrap update` en `android/`, subir `appVersionCode` y publicar el paquete nuevo.

## Alternativas descartadas

- **Seguir solo con la web instalable** (ADR 0013): funciona, pero hay que saber hacerlo.
- **La TWA sin service worker**: es la que más riesgo corre de que Play la rechace por ser solo una web,
  y no deja leer nada sin conexión.
- **Guardar primero y actualizar después** («stale-while-revalidate»): abre más rápido, pero enseñaría
  el número de ayer a quien abre la app por la mañana.
- **App nativa o con Capacitor**: dos programas que mantener; la TWA es la misma web.
- **PWABuilder**: usa Bubblewrap por debajo, pero desde una web de Microsoft; con la herramienta en el
  equipo todo queda en el repositorio, como en PageKeeper.
- **Avisos de número nuevo**: siguen descartados (ADR 0013): necesitan servidor.

## Consecuencias

- El diario se lee sin conexión también en el navegador, instalado o no, y en Firefox y Safari.
- La app guarda sus datos en el almacenamiento de Chrome para diarioiaeducativa.github.io: lo
  guardado es lo mismo que en Chrome, y borrar los datos de ese sitio en Chrome lo borra.
- Hay que mantener `assetlinks.json` y rehacer el paquete cuando Play suba la versión de Android
  exigida.
- Cambiar la forma de guardar exige cambiar `CACHE` en `sw.js` (`diario-v1`, `diario-v2`…): al activarse,
  el service worker nuevo borra las cachés anteriores.

## Evidencia

- Política de Play para apps de noticias: [Requirements for news and magazine
  apps](https://support.google.com/googleplay/android-developer/answer/10523915) y [How to declare a news
  and magazine app](https://support.google.com/googleplay/android-developer/answer/16189314) (consultadas
  el 09-11-2026): la declaración se hace en «Contenido de la aplicación», pide una página de contacto que
  también se pueda abrir desde la app y cubre las noticias generadas con IA; sin ella, Google retira la
  app.
- Bubblewrap genera el proyecto a partir de `twa-manifest.json` (`bubblewrap update`) y de la ficha de
  aplicación publicada.

## Riesgos y limitaciones

- Play puede rechazarla igualmente por «funcionalidad mínima»; la lectura sin conexión lo hace menos
  probable, no imposible.
- Lo que se guarda depende de lo que el navegador deje: si el dispositivo va justo de espacio, puede
  borrarlo.
- Sin Chrome (u otro navegador compatible con TWA) en el móvil, la app abre la web en una pestaña
  personalizada, con barra de dirección.
- Solo Android; en iPhone y iPad, la web instalable del ADR 0013, que ahora también funciona sin
  conexión.

## Validación

09-11-2026, con el sitio generado en local y servido en `127.0.0.1`, en Chromium, Firefox y WebKit de
Playwright, apagando el servidor para quitar la red:

- Con red, un cambio en la portada se ve al recargar: no se sirve lo guardado.
- Al cargar la portada catalana se guardaron sus 24 piezas (37-38 archivos en total). Sin red se
  abrieron la primera y la última sin haberlas abierto antes, y la portada; una página no guardada
  enseña «Sense connexió» y una inglesa, «You are offline».
- Sin errores de JavaScript, salvo en WebKit sin red, que avisa de que no puede leer la ficha de
  aplicación inglesa, no guardada (inofensivo).
- `probar-web` en los tres motores, móvil, tableta y escritorio, claro y oscuro: sin errores.
- APK firmado con la clave de subida compilado con `android/construeix.sh`. Queda probarlo en un móvil
  real con el sitio ya publicado.
