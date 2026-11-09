# Instrucciones para agentes

Este repositorio escribe y publica cada día el Diario de IA Educativa
(<https://diarioiaeducativa.github.io/>), a partir de lo que se habla en los
grupos ChatGPT-IA-edu, Vibe Coding Educativo y EduMedia-IAG. El porqué de cada
pieza está en `docs/adr/`; aquí, lo que hay que saber para trabajar en él.

## Dónde corre

- **En el NAS**, en el contenedor `diario-ia-educativa`
  (`/volume1/docker/diario-ia-educativa`; `compose.yml` y `Dockerfile` se
  copian de `nas/`). Cambiar el `Dockerfile` exige `docker compose build &&
  docker compose up -d`; cambiar `nas/reloj.sh`, reiniciar el contenedor. Lo
  demás lo trae `noche.sh` con `git pull`.
- **El NAS sube cada mañana a este repositorio**: `git pull` antes de tocar
  nada.
- **Horario** (`nas/reloj.sh`): a la 1:00, `noche.sh` con las conversaciones
  del día anterior; a las 5:00, vista previa en la red de casa (ADR 0025); a
  las 6:30, aviso si no está; a las 6:50, `publicar-nas.sh` (sitio,
  repositorio y avisos al bot, que los publica a las 7:00); a las 7:05, el
  carrusel de Instagram (ADR 0015).
- **Estado y registro**: `estado/<fecha>.{listo,publicado,sin-numero,intentos,avisado}`
  y `registro/<fecha>.log`.

## Lo que no se puede olvidar

- **Siempre sale un número** (ADR 0021 y 0028): si fallan los dos intentos,
  la reserva (`reserva/`, del fondo del repositorio y de la biblioteca, alternados; que `reserva.sh` repone cada mañana; las piezas
  caducan a los 60 días y los reportajes a los 28) y reintentos cada 10
  minutos hasta las 9:00. El vigilante de GitHub Actions
  (`.github/workflows/vigilante.yml`) lo comprueba desde las 9:10 hasta el final del día; lo lanza
  a su hora el hosting de IONOS (`ionos/lanzar-vigilante.sh`, en `~/.diario-vigilante/`), porque
  el horario de GitHub se retrasa horas. Cambiar ese script exige copiarlo allí.
- **Publicar la web a mano sin repetir avisos**: en el contenedor,
  `generar.py`, Pagefind, `rsync` a `/sitio` y commit con push. Nunca
  `publicar-nas.sh`, que copia los avisos al bot.
- **Cambiar un número antes de que salga**: editar
  `ediciones|vinetas(-ca)/FECHA.json` en el NAS y `docker exec
  diario-ia-educativa python3 /proyecto/generar.py`.
- **Reportaje de reserva a propósito**: crear `estado/<sábado>.reportaje-reserva`
  (ADR 0028).
- **La rama `instagram` del sitio se rehace cada día con push forzado**:
  GitHub ofrece «Compare & pull request»; no se fusiona nunca.
- **Sin huecos** (ADR 0041): ninguna composición puede dejar espacios vacíos con ninguna cantidad de
  piezas; se comprueba con pocas y con muchas. En la portada, cada sección enseña sus tres más recientes.
  Antes de enseñar o publicar un cambio de maqueta, `scripts/revisar-maqueta.js` con `probar-web -s` en
  todas las páginas, idiomas y anchuras (cómo, en su cabecera): tiene que salir sin avisos.
- **Lectura automática bloqueada a propósito** (UNESCO en la Biblioteca): no
  se salta.

## Piezas

- **Reportaje del domingo** (ADR 0004): `scripts/reportaje.sh`, que lanza
  `noche.sh` los sábados (o con `REPORTAJE=1`).
- **Revisión de dibujos** (ADR 0005): `scripts/revisar-dibujos.py`; lo que
  sigue mal va a `revision/FECHA/retirados/` y avisa.
- **Biblioteca** (ADR 0006): `scripts/biblioteca.sh FECHA [ids]`.
- **Repositorio de VCE** (ADR 0008 y 0018): `scripts/repositorio.sh FECHA
  [urls]`; la cola se calcula cada noche; los viernes, «La semana del
  repositorio», con la lista de lo ya contado en la semana; con la cola vacía, el fondo. El umbral (`UMBRAL=4`) es
  provisional.
- **Dibujos** (ADR 0009 y 0014): `scripts/dibujar.sh FECHA [ids]`, en el NAS
  con `docker exec`. Los iconos de Lucide son un recurso, no una plantilla:
  vigilar que los dibujos no se uniformicen. Al probar un redibujo, quitar
  antes `ilustracion_alt`, o el ilustrador calca lo que describe.
- **Comentarios** (ADR 0030): giscus, en las Discussions del repositorio del
  sitio (categoría «Comentarios»); un hilo por pieza, el mismo en los cinco
  idiomas. Se moderan desde GitHub. Si se renombra la categoría, cambiar
  `GISCUS` en `generar.py`. El aviso de cada comentario (a Juanjo y a Raül,
  por el Bot de IA Educativa) es una acción del repositorio del sitio: por eso
  la publicación no toca `.github/`.
- **Enlaces en el texto** (ADR 0011 y 0031): lo ya publicado y cada fuente
  nombrada, en su primera mención (`encargos/enlaces.md`). Para enlazar las
  fuentes de piezas ya escritas, `scripts/enlazar-fuentes.py`, que no deja
  cambiar ni un carácter del texto.
- **Noticias en columnas** (ADR 0044): en el ordenador, las noticias y el reportaje (`en-columnas`) van en
  columnas de periódico, con el botón «Una columna» en la línea de la sección; las reglas, al final de
  `estaticos/diario.css`. Lo que tenga que cortar las columnas (un bloque nuevo dentro de `.cuerpo`) se
  añade a su lista de `column-span: all`.
- **Buscador** (ADR 0007): Pagefind, tras `generar.py`, solo en los
  `<article>` con `data-pagefind-body`.
- **Vídeos** (ADR 0016 y 0027): «La semana en vídeo» la noche del sábado
  (`scripts/reel-semana.sh`), como mínimo una pieza de cada número y con
  música distinta cada vez; el dominical sale el domingo a las 9:00 en
  Instagram, X, Bluesky y LinkedIn desde el contenedor del boletín
  (`scripts/redes/dominical.sh`; probar con `--comprobar`). Los `.mp4` van a Internet Archive
  (`diarioiaeducativa_<año>`, ADR 0037) con `scripts/subir-videos.py`, que marca `archive` en su JSON
  tras comprobar la descarga; no se suben a los repositorios.
- **Para tu web** (ADR 0032): `para-tu-web.html` (configurador), `insertar.html` (el widget, para un
  iframe), `noticias*.json`, `datos/AAAA-MM.json`, `feed-*.xml` e `ilustraciones/*.svg` en cada idioma,
  y el botón de cada pieza con su `<template id="republicar">`. Los nombres de archivos y parámetros no
  se cambian: hay widgets pegados en otras webs.
- **Contador de visitas** (ADR 0033): `CONTADOR` en `generar.py` y `ionos/estadisticas/`, desplegado
  a mano en `app/diario-ia-educativa/` del hosting (`config.php`, con las contraseñas, solo allí; no
  sobrescribirlo). Panel privado en <https://bilateria.org/app/diario-ia-educativa/>. Para probar sin
  contar, Playwright ya no cuenta; a mano, `?nocontar=1`. El panel marca solo los navegadores de los autores
  (salto con `volver=1`): publicar el sitio antes que un cambio del panel que dependa de él.
- **Buscadores** (ADR 0039): `robots.txt`, la dirección canónica de cada página y los datos
  estructurados de cada pieza salen de `generar.py` (`cabeza()`, `datos_noticia()`). El diario está en
  Google Search Console, con la cuenta de Juanjo: `estaticos/google0f64171555c8a8ac.html` lo verifica y no
  se borra; de esa verificación depende también la de Bing Webmaster Tools. Una página nueva que deba indexarse pasa por `cabeza()` y entra en `sitemap()`.
- **La semana y el mes** (ADR 0034): `semana/AAAA-WW/` (semana de los mensajes, selector `?grupo=`),
  `mes/AAAA-MM/` y la hemeroteca por semanas. El boletín deja el pódcast y el vídeo de cada grupo en
  `multimedia/AAAA-WW.json` (formato en su `LEEME.md`) y `reloj.sh` vuelve a publicar solo la web con
  `scripts/publicar-web.sh`, con el número del día ya publicado.
- **Hace un año** (ADR 0040): `scripts/hace-un-ano.sh FECHA`, cada noche: los mensajes del mismo día
  del año anterior al de publicación (±1 día), una pieza en `hace-un-ano/` de 150 a 250 palabras, sin
  repetir tema del último mes, con un díptico «Entonces / Ahora»; en la portada, un recuadro a todo el
  ancho con lo de hoy; sección sin entrada en el menú (`SECCIONES_FUERA`), con enlace en el pie.
- **Comentario de la semana** (ADR 0038): `scripts/comentario-semana.sh AAAA-WW`, que lanza `noche.sh`
  la noche del domingo (o con `COMENTARIO=1`): uno general y uno por grupo en `comentario-semana/`,
  de 150 a 250 palabras; `scripts/comentario_semana.py comprobar` dice si vale.
- **App de Android y lectura sin conexión** (ADR 0042): `estaticos/sw.js` (primero la red; sin ella,
  lo guardado y `sin-conexion.html`); si cambia lo que guarda, subir `CACHE`. La app es una TWA en
  `android/` (`construeix.sh`, con la clave en `~/.config/diario-ia-educativa/android/`), vinculada por
  `estaticos/.well-known/assetlinks.json`, que no se borra. La política de privacidad de la ficha es
  `redaccion.html#privacidad`: si se cambia ese apartado, que siga diciendo lo que guarda el dispositivo.
- **Avisos del número** (ADR 0043): la app mira `ultimo.json` (no se renombra: hay apps que lo leen) hacia
  las 7:00 y cada 15 minutos hasta las 9:30. Su código está en `android/avisos/` y lo engancha `aplicar.py`
  (lo lanza `construeix.sh`), porque `bubblewrap update` lo borra del manifiesto. Para probar, el emulador
  `prueba-twa` (`ANDROID_AVD_HOME=~/.config/.android/avd`), sin ventana; el registro, `adb logcat -s Avisos`.
- **Cinco idiomas** (ADR 0026): `/ca/`, `/gl/`, `/eu/` y `/en/`;
  traducción nocturna (`scripts/traducir.sh`) y de un día ya publicado
  (`scripts/traducir-dia.sh FECHA [idiomas]`, en una copia fuera de `/home`).
  Vídeos solo en castellano y catalán; avisos e Instagram, solo en castellano.

## Probar en local

En una copia en el directorio temporal, con `CLAUDE_CONFIG_DIR` apuntando a
una copia de las credenciales de Claude Code (borrarla al acabar), para no
usar el perfil de quien trabaja. Para el repositorio de VCE,
`REPOSITORIO_MODO=dia|semana|fondo`.
