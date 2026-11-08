# 21. Ningún día sin número: reserva, vigilante, recuperación y reintentos de publicación

Fecha: 2026-11-05 · Estado: aceptado · Revisado: 2026-11-08 (el vigilante, todo el día y lanzado desde IONOS)

## Contexto

Juanjo, 05-11-2026: «no puede haber dia sin numero, la gente lo espera. para esos casos hay que
tener un plan b». Hasta entonces, un día se quedaba sin número si:

- no había nada que contar y tampoco salía nada de la Biblioteca ni del repositorio (`sin-numero`);
- la redacción o el repaso fallaban dos veces (error de un agente, Claude caído, cuota agotada):
  aviso a las 6:30 y nada más;
- el NAS o el contenedor estaban caídos: ni número ni aviso, porque el aviso sale del propio NAS;
- GitHub fallaba al publicar más allá de los reintentos de la conexión (ADR 0012, unos 100 s): un
  solo intento y el resto, a mano.

Aprobado ese mismo día («sí a todo, hazlo»), junto con el resumen semanal día a día (ADR 0016).

## Decisión

- **Piezas de reserva, siempre tres listas** (`reserva/`, `scripts/reserva.sh` y
  `scripts/reserva.py`). Son artículos del fondo del Repositorio de VCE («Del fondo del
  repositorio»), que no caducan, escritos con el mismo proceso de siempre (`repositorio.sh` en
  modo fondo: documentalista, revisor y traductor) con una clave de fecha provisional
  (`2099-01-NN`) y guardados con su captura y su traducción. Cada mañana, con el número ya
  publicado, `reloj.sh` escribe una más si faltan (una por día) y la sube a GitHub. Lo que está en
  la reserva cuenta como ya contado en `repositorio.py`, para que no salga dos veces.
- **Usar la reserva no necesita IA**: `reserva.py usar FECHA fallo|relleno` cambia la clave por la
  fecha en el JSON y en el nombre de la captura, la pasa a `repositorio/` y marca la edición con
  `"reserva"`. Si faltan los avisos de los grupos, los escribe sin IA con los titulares del número.
  Si el día ya tenía piezas (la redacción terminó y se atascó después), no añade nada y el número
  sale con lo que había.
- **Cuándo se usa**:
  - en `noche.sh`, un día sin nada que contar en el que tampoco sale nada de la Biblioteca ni del
    repositorio («relleno»: no hay nada que recuperar ni que avisar en la web);
  - en `reloj.sh`, si los dos intentos de la noche han fallado o a las 6:30 si aún no está
    («fallo»): para la redacción (se lanza con `setsid`, así que se para entera, con sus agentes),
    usa la reserva y avisa a Juanjo;
  - en el **vigilante de fuera de casa** (`.github/workflows/vigilante.yml` y
    `scripts/vigilante.sh`, en GitHub Actions, gratis en un repositorio público): desde las 9:10
    de Madrid y hasta el final del día mira si el número de hoy está en la web; si no está, lo saca con la reserva, lo
    publica con su propia clave de despliegue del sitio y avisa a Juanjo por Telegram. Los grupos
    no reciben aviso ese día: el bot está en el NAS. Si el número ya está en el repositorio
    (`ediciones/FECHA.json`) pero GitHub Pages aún no lo sirve, no hace nada: el sitio se sube
    antes que la redacción, así que eso solo pasa si alguien acaba de publicarlo.
  - **quién lanza el vigilante** (revisado el 08-11-2026): GitHub Actions retrasa horas, o se
    salta, las pasadas programadas. Del horario original (tres pasadas, a las 9:10, 10:10 y 11:10)
    solo hizo una al día, a las 15:57 el 06-11 y a las 14:56 el 07-11, fuera de la ventana de
    entonces (9:10-12:00), así que con el NAS caído no habría salido número ni aviso. Por eso lo
    lanza a su hora el hosting de IONOS (`ionos/lanzar-vigilante.sh`, con el cron del hosting a las
    9:12, 10:12, 12:12 y 16:12): mira la web y, si falta el número, pide a GitHub la ejecución
    (`workflow_dispatch` con `simular=false`) con un token de grano fino que solo puede lanzar
    flujos de este repositorio; si GitHub no la acepta, avisa a Juanjo. El token no caduca (la
    organización lo permite desde el 08-11-2026, por decisión de Juanjo: con un permiso tan pequeño,
    la caducidad solo añade el riesgo de que el lanzador se pare por una renovación olvidada). Cada
    mañana a las 8:40 comprueba que el token sirve, y si un día tuviera fecha, avisaría a 30, 14, 7,
    3 y 1 días de que caduque. El horario de
    GitHub se queda de respaldo, cada hora de las 7:23 a las 21:23 UTC, en un minuto poco
    concurrido.
- **Nada se pierde**: el número de reserva por fallo lo dice en la portada y en la página del día
  («Hoy no han podido salir las noticias de los grupos de ayer por un fallo de la redacción…»), y
  la noche siguiente `noche.sh` ve la marca y pide a `preparar.py` (`RECUPERA=1`) los mensajes de
  ese día como noticia, no como contexto; el encargo de la redacción lo explica. Así el resumen
  de la semana tiene también su pieza ese día.
- **Publicar, hasta las 9:00**: si `publicar-nas.sh` falla a las 6:50, `reloj.sh` lo repite cada
  10 minutos hasta las 9:00 y avisa una vez al primer fallo y otra al final. `publicar-nas.sh`
  sube también lo que un intento anterior dejó sin subir (antes, un commit hecho y no subido se
  quedaba así). El bot publica los avisos de los grupos en cuanto llegan, hasta las 12:00
  (ADR 0025 del bot).
- **El vigilante entra a las 9:10, después de que el NAS deje de reintentar**, para que nunca
  publiquen los dos a la vez.

## Alternativas descartadas

- **Un número hecho por programa con los mensajes del día, sin IA**: rompería lo que promete el
  diario (cada dato comprobado en su fuente, las opiniones sin nombre).
- **El vigilante entero en el hosting de IONOS**: la web y el código ya están en GitHub, y así no
  gasta espacio del hosting. Funciona igual cuando falla la casa. IONOS solo lo lanza: un script de
  pocas líneas, sin copia de la redacción.
- **Solo el horario de GitHub, con más pasadas**: sigue dependiendo de una cola que GitHub no
  garantiza; se queda como respaldo del lanzador de IONOS.
- **El vigilante solo hasta las 12:00**: un número a media tarde es mejor que ninguno, y después de
  las 9:00 el NAS ya no intenta publicar, así que no pueden chocar.
- **El vigilante antes de las 9:10**: llegaría antes los días de NAS caído, pero podría publicar a
  la vez que el NAS cuando este solo está reintentando.

## Consecuencias

- El NAS escribe una pieza de reserva más al día mientras falten: unos 3 minutos de agentes.
- Un día con el NAS caído, el número sale hacia las 9:15, lanzado desde IONOS (si IONOS también
  falla, cuando pase el horario de GitHub, que puede ser por la tarde), y sin aviso en los grupos.
- El token de IONOS no caduca. Si hay que rehacerlo, se crea en GitHub (Settings › Developer
  settings › Fine-grained tokens), con dueño `diarioiaeducativa`, solo el repositorio `periodico`,
  solo «Actions: Read and write» y sin caducidad, y se deja en `~/.diario-vigilante/token` del
  hosting.
- La reserva vive en el repositorio público: su artículo se puede leer en GitHub antes de salir.

## Evidencia

- Prueba del 05-11-2026 en una copia de la redacción: `reserva.sh` escribió «La recta numèrica»
  (documentalista, revisor y traductor, 2 min 20 s) y la guardó en `reserva/2099-01-01/`;
  `reserva.py usar 2026-11-05 fallo` la pasó al número, con los avisos y la marca; la portada,
  en Chromium a 1280 px en claro y a 390 px en oscuro, con el aviso y sin avisos de axe-core.
- Bot: `scripts/diario_grupos.py`, `VENTANA = timedelta(hours=5)` desde las 7:00.

## Riesgos y limitaciones

- Si el NAS deja de publicar por algo que no es GitHub y el vigilante saca la reserva, la redacción
  del NAS puede tener ese día archivos sin subir que choquen con los del vigilante: lo avisa el NAS
  a las 9:00 y se arregla a mano.
- Si se agotan las reservas (tres fallos seguidos sin poder escribir otra), no hay número: avisa
  el NAS o el vigilante.
- El vigilante necesita tres secretos en GitHub (la clave del sitio y el bot de avisos de Juanjo), y
  el lanzador de IONOS, el token y una copia del `config.json` del bot de avisos, en una carpeta
  que su `.htaccess` no deja servir (comprobado: HTTP 403).
- Si IONOS y GitHub fallan a la vez el mismo día, no sale número.

## Validación

- 05-11-2026, en el NAS: `reserva.sh` tres veces; tres reservas listas y subidas
  (`reserva/2099-01-01` a `03`), unos 3 minutos cada una.
- `preparar.py` con `RECUPERA=1` en el NAS sobre los mensajes reales del 04-11: el día anterior
  entra como «RECUPERADO» y cuenta como noticia (156 mensajes en lugar de 68).
- `setsid` en el contenedor: parar el grupo de procesos para `timeout` y lo que lanza, sin restos.
- El vigilante en GitHub Actions, lanzado a mano en simulación (`simular`, y `fecha` para dar por
  perdido un número): monta el número con la reserva, genera el sitio y el buscador, descarga el
  repositorio del sitio con su clave, `push --dry-run` sin error y el bot de avisos responde
  (`getMe`), sin subir ni enviar nada (ejecución 42084398936).
- 08-11-2026: historial de ejecuciones del vigilante (`gh run list`): solo una pasada programada al
  día, a las 15:57 y a las 14:56, que terminaron con «solo actúa de 9:10 a 12:00». En IONOS,
  `lanzar-vigilante.sh --probar` con el número en la web y con `HOY_PRUEBA` (el camino de cuando
  falta), y `--comprobar` sin token avisa. Con el token, `--comprobar` lo da por válido (primero con
  caducidad de un año y después, regenerado, «sin caducidad»), y dos lanzamientos desde IONOS por `workflow_dispatch` (HTTP 204): con `simular=true`
  monta el número con la reserva sin subir nada (ejecución 42472300877), y con `simular=false` y
  el número ya en la web termina en «ya está en la web», sin tocar nada (también con el token
  regenerado). Cron del hosting
  instalado ese día.
