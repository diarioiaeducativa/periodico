# La redacción del Diario de IA Educativa

El código y la redacción del [Diario de IA Educativa](https://diarioiaeducativa.github.io/):
cada noche, ocho agentes de IA leen lo que se ha hablado en tres comunidades docentes de
Telegram y preparan el número que sale a las 7:00 en castellano, traducido al catalán, gallego,
euskera e inglés ([ADR 0026](docs/adr/0026-cinco-idiomas.md)), con su
viñeta de Tiza y Algoritmo. La noche del sábado, cinco agentes más preparan el
reportaje del domingo ([ADR 0004](docs/adr/0004-reportaje-del-domingo.md)). El sitio generado se publica en
[diarioiaeducativa.github.io](https://github.com/diarioiaeducativa/diarioiaeducativa.github.io).

- `encargos/`: lo que se pide a cada agente; `encargos/pasos/`, el encargo de cada paso de la noche.
- `scripts/noche.sh`: la redacción nocturna; `scripts/reportaje.sh`: el reportaje del domingo; `scripts/biblioteca.sh`: los artículos de la Biblioteca digital ([ADR 0006](docs/adr/0006-biblioteca-digital.md)); `scripts/repositorio.sh` y `scripts/repositorio.py`: los recursos del Repositorio de VCE en la sección Vibe coding ([ADR 0008](docs/adr/0008-recursos-del-repositorio-de-vce.md)); `scripts/revisar-dibujos.py` y `scripts/dibujos.sh`: la revisión de los dibujos en su página ([ADR 0005](docs/adr/0005-revision-de-dibujos.md)); `scripts/publicar-nas.sh`: la publicación.
- `nas/`: el contenedor del NAS y su reloj ([ADR 0001](docs/adr/0001-redaccion-nocturna-en-el-nas.md)).
- `generar.py` y `vineta.py`: el sitio y la tira, sin IA; el índice del buscador lo hace Pagefind al publicar ([ADR 0007](docs/adr/0007-buscador.md)); `estaticos/`, los estilos, fuentes e iconos que copia al sitio; el diario se puede instalar como app desde el navegador, sin avisos ([ADR 0013](docs/adr/0013-instalable-como-app-sin-avisos.md)).
- `scripts/reel-semana.sh` y `scripts/reel-semana.py`: «La semana en vídeo», el reel del domingo, con música de `scripts/musica.py` distinta cada vez; los vídeos de la web, en `videos/` ([ADR 0016](docs/adr/0016-videos-y-la-semana-en-video.md)).
- `scripts/instagram.py`: el carrusel diario en Instagram (@comunidad.iaeducativa): imágenes, publicación y renovación del permiso ([ADR 0015](docs/adr/0015-el-numero-en-instagram.md)).
- `lucide/iconos.txt`: los iconos de Lucide que el ilustrador puede usar en sus dibujos, preparados por `scripts/lucide.py` ([ADR 0014](docs/adr/0014-iconos-de-lucide-rotulos-en-la-descripcion-y-dibujos-ampliables.md)).
- `ediciones/`, `ilustraciones/`, `vinetas/` (y sus versiones `-ca`, `-gl`, `-eu` y `-en`) y `avisos/`: lo que ha escrito la redacción.
- `idiomas_web.py`: los textos de la web en gallego, euskera e inglés; `scripts/idiomas.py`, `scripts/traducir.sh` y `scripts/traducir-dia.sh`: las traducciones de cada noche, su comprobación y la de un día ya publicado ([ADR 0026](docs/adr/0026-cinco-idiomas.md)).
- `publicar.sh`: publicar a mano desde el portátil.
- `reserva/`, `scripts/reserva.sh` y `scripts/reserva.py`: las piezas de reserva para que no haya ningún día sin número, y `scripts/vigilante.sh` con `.github/workflows/vigilante.yml`, el vigilante que saca el número desde GitHub si el NAS no lo ha publicado ([ADR 0021](docs/adr/0021-ningun-dia-sin-numero.md)).

Código con licencia [AGPL v3](LICENSE); textos e ilustraciones, CC BY-SA 4.0, © 2026 Juan José de
Haro y Raül Torres. Letra [Newsreader](https://github.com/productiontype/Newsreader) (OFL,
`estaticos/fuentes/OFL.txt`) e iconos de [Lucide](https://lucide.dev) (ISC, `lucide/LICENSE`).
El porqué de cada decisión está en los [ADR](docs/adr/README.md), y la última evaluación con la
rúbrica VCER, en [evaluacion-vcer.md](evaluacion-vcer.md).

Los mensajes de los grupos (`dias/`), los registros de cada noche y las credenciales no están en
el repositorio: los mensajes los recoge cada noche `scripts/preparar.py` de lo que guarda el Bot de
IA Educativa.

## Modificarlo

- **El aspecto**: `generar.py` monta todo el sitio en `sitio/` a partir de los JSON de
  `ediciones/`, `biblioteca/`, `repositorio/`, `reportajes/` y `vinetas/`, sin IA ni conexión.
  Con Python 3 basta `python3 generar.py` y abrir `sitio/index.html` en el navegador. Los
  estilos están en `estaticos/comun.css` y `estaticos/diario.css`; los textos fijos de la web,
  en los dos idiomas, en el diccionario del principio de `generar.py`.
- **Lo que escriben los agentes**: cada paso de la noche tiene su encargo en
  `encargos/pasos/`, y los criterios comunes (estilo, enlaces, ilustraciones, viñeta) están en
  `encargos/`. Cambiar un encargo cambia el número siguiente, sin tocar el código.
- **Probar una noche sin publicar**: en una copia del repositorio, con
  [Claude Code](https://code.claude.com/docs/es/overview) identificado y
  `DATOS_BOT` apuntando a una carpeta con los mensajes en el formato que guarda el Bot de IA
  Educativa (lo que lee `scripts/preparar.py`), `scripts/noche.sh AAAA-MM-DD` prepara el número y
  `python3 generar.py` lo monta. Sin `scripts/publicar-nas.sh` no sale nada a la web ni a los
  grupos.
- **Adaptarlo a otra comunidad**: los grupos están en `GRUPOS` (`generar.py`) y en `NOMBRES`
  (`scripts/preparar.py`); el nombre y el lema, en el diccionario de textos.

## Recuperar en otra máquina

Todo lo necesario está en este repositorio y en el del sitio, salvo las dos claves de
despliegue, que son secretas y se crean de nuevo. En una máquina con Docker:

1. Construir antes la imagen `boletin-semanal:local` (repositorio `jjdeharo/boletin-semanal`),
   de la que parte la del diario.
2. Crear la carpeta del diario, con `home/.ssh` dentro, y copiar en ella `nas/compose.yml` y
   `nas/Dockerfile`. En `compose.yml`, ajustar las rutas de fuera de la carpeta (el token de
   Claude, los datos del Bot de IA Educativa, el avisador y las claves de Internet Archive del
   boletín, ADR 0037) si no están en el mismo sitio.
3. Generar las dos claves (`ssh-keygen -t ed25519 -N "" -f home/.ssh/periodico` y lo mismo con
   `sitio`) y darlas de alta con permiso de escritura, como *deploy keys*, en
   `diarioiaeducativa/periodico` y `diarioiaeducativa/diarioiaeducativa.github.io`. Quitar las
   antiguas. Guardar la huella de GitHub en `home/.ssh/known_hosts`
   (`ssh-keyscan -t ed25519 github.com`, comparándola con `api.github.com/meta`).
4. `docker compose build`, y clonar los dos repositorios en `repo/` y `sitio/` desde un
   contenedor de esa imagen, poniendo en cada uno `core.sshCommand` con su clave
   (`/proyecto/scripts/ssh-reintenta.sh -i ~/.ssh/<clave> -o IdentitiesOnly=yes
   -o UserKnownHostsFile=~/.ssh/known_hosts`, que reintenta si GitHub rechaza la conexión,
   ADR 0012) y
   `remote.origin.fetch` también para `+refs/notes/*:refs/notes/*`.
5. `docker compose up -d`. No hace falta copiar `estado/`: un número cuya edición ya está en
   GitHub no se vuelve a preparar ni a publicar.

El lanzador del vigilante (ADR 0021) no corre en el NAS sino en un hosting con cron:
`ionos/lanzar-vigilante.sh` explica en su cabecera la carpeta, el token de GitHub de grano fino
(solo «Actions: Read and write» en este repositorio) y las líneas del crontab.

Para preparar o rehacer un día a mano:
`docker exec diario-ia-educativa /proyecto/scripts/noche.sh AAAA-MM-DD` (con `-e REHACER=1`
si ese número ya se publicó) y después `scripts/publicar-nas.sh AAAA-MM-DD`.
