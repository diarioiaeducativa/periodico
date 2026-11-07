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
  la reserva (`reserva/`, que `reserva.sh` repone cada mañana; las piezas
  caducan a los 60 días y los reportajes a los 28) y reintentos cada 10
  minutos hasta las 9:00. El vigilante de GitHub Actions
  (`.github/workflows/vigilante.yml`) lo comprueba de 9:10 a 12:00.
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
  `GISCUS` en `generar.py`.
- **Buscador** (ADR 0007): Pagefind, tras `generar.py`, solo en los
  `<article>` con `data-pagefind-body`.
- **Vídeos** (ADR 0016 y 0027): «La semana en vídeo» la noche del sábado
  (`scripts/reel-semana.sh`), como mínimo una pieza de cada número y con
  música distinta cada vez; el dominical sale el domingo a las 9:00 en
  Instagram, X, Bluesky y LinkedIn desde el contenedor del boletín
  (`scripts/redes/dominical.sh`; probar con `--comprobar`).
- **Cinco idiomas** (ADR 0026): `/ca/`, `/gl/`, `/eu/` y `/en/`;
  traducción nocturna (`scripts/traducir.sh`) y de un día ya publicado
  (`scripts/traducir-dia.sh FECHA [idiomas]`, en una copia fuera de `/home`).
  Vídeos solo en castellano y catalán; avisos e Instagram, solo en castellano.

## Probar en local

En una copia en el directorio temporal, con `CLAUDE_CONFIG_DIR` apuntando a
una copia de las credenciales de Claude Code (borrarla al acabar), para no
usar el perfil de quien trabaja. Para el repositorio de VCE,
`REPOSITORIO_MODO=dia|semana|fondo`.
