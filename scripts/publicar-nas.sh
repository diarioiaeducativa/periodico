#!/usr/bin/env bash
# SPDX-License-Identifier: AGPL-3.0-or-later
# Publica el número preparado por noche.sh: regenera el sitio, lo sube a GitHub Pages, guarda
# en el repositorio de la redacción lo que han escrito los agentes y deja los avisos de los
# grupos donde los recoge el bot. Lo lanza reloj.sh a las 6:50, para que el sitio ya esté
# en línea cuando el bot avise a las 7:00.
#
#   scripts/publicar-nas.sh [AAAA-MM-DD]   (la fecha de las conversaciones; por defecto, ayer)
set -uo pipefail

RAIZ="$(cd "$(dirname "$(readlink -f "$0")")/.." && pwd)"
cd "$RAIZ"
FECHA="${1:-$(date -d yesterday +%F)}"
PUBLICA=$(date -d "$FECHA + 1 day" +%F)
SITIO="${SITIO_REPO:-/sitio}"
AVISOS_BOT="${AVISOS_BOT:-/avisos-bot}"
REG="registro/$FECHA.log"
NOTA="Modelo: Claude Sonnet 5.5 (claude-sonnet-5-5) y Claude Opus 5.5 (claude-opus-5-5) · Claude Code, redacción nocturna en el NAS"

log() { printf '%s  %s\n' "$(date '+%F %T')" "$*" | tee -a "$REG"; }

# La imagen de vista previa del número y la cabecera de los avisos (ADR 0010). Si fallan, el sitio
# sale con la imagen genérica y el bot publica los avisos sin cabecera.
python3 scripts/og-numero.py >> "$REG" 2>&1 || log "AVISO: no se pudo hacer la imagen del número; queda la genérica"
python3 scripts/avisos-cabecera.py "$FECHA" >> "$REG" 2>&1 || log "AVISO: los avisos salen sin la cabecera del número"
# Las imágenes del carrusel de Instagram (ADR 0015); las publica reloj.sh a las 7:05. Si fallan, ese día no hay carrusel.
python3 scripts/instagram.py imagenes "$FECHA" >> "$REG" 2>&1 || log "AVISO: no se pudieron hacer las imágenes de Instagram; hoy no habrá carrusel"
# Las cifras de los grupos que deja el Bot de IA Educativa una vez por semana (ADR 0029): las nuevas, al
# repositorio, para que el diagrama de «La redacción» y el pie salgan también desde GitHub.
mkdir -p comunidades
for f in /bot-datos/comunidades/????-??-??.json; do
  [ -f "$f" ] && [ ! -e "comunidades/${f##*/}" ] && cp "$f" comunidades/ && log "comunidades: cifras del ${f##*/}"
done
python3 generar.py >> "$REG" 2>&1 || { log "ERROR: el generador falla"; exit 1; }
# El índice del buscador (ADR 0007). Si falla, el sitio sale igual con el índice anterior.
python3 -m pagefind --site sitio >> "$REG" 2>&1 || log "AVISO: no se pudo rehacer el índice del buscador; queda el anterior"

# El sitio: lo generado, sin tocar lo que solo vive en su repositorio.
git -C "$SITIO" pull -q --ff-only >> "$REG" 2>&1 || { log "ERROR: no se pudo actualizar $SITIO"; exit 1; }
rsync -a --delete --exclude .git --exclude .github --exclude README.md --exclude LICENSE --exclude LICENSE-CODIGO \
  --exclude .nojekyll --exclude fuentes/OFL.txt sitio/ "$SITIO/"
git -C "$SITIO" add -A
if ! git -C "$SITIO" diff --cached --quiet; then
  git -C "$SITIO" commit -qm "Número del $PUBLICA" &&
  git -C "$SITIO" notes --ref=ia add -f -m "$NOTA" HEAD || { log "ERROR: no se pudo preparar el commit del sitio"; exit 1; }
fi
# Se sube también lo que un intento anterior dejó sin subir (reintentos de reloj.sh, ADR 0021)
if [ -n "$(git -C "$SITIO" rev-list '@{u}..HEAD' 2>/dev/null)" ]; then
  git -C "$SITIO" push -q && git -C "$SITIO" push -q origin refs/notes/ia ||
    { log "ERROR: no se pudo subir el sitio"; exit 1; }
  log "sitio publicado: $(git -C "$SITIO" log --oneline -1)"
fi

# Lo publicado, para que el bot busque en el diario (ADR 0017): solo con el sitio ya subido, para que
# no cite piezas que aún no están en línea. Se cambia de una vez, para que nunca lea un archivo a medias.
if [ -f indice/diario.json ] && [ -d "$AVISOS_BOT" ]; then
  cp indice/diario.json "$AVISOS_BOT/.hemeroteca.tmp" && mv "$AVISOS_BOT/.hemeroteca.tmp" "$AVISOS_BOT/hemeroteca.json" &&
    log "índice del diario entregado al bot" || log "AVISO: no se pudo entregar al bot el índice del diario"
fi

# Los avisos, solo cuando el sitio ya está subido: el bot los publica a las 7:00.
if [ -f "avisos/$PUBLICA.json" ] && [ -d "$AVISOS_BOT" ]; then
  cp "avisos/$PUBLICA.json" "$AVISOS_BOT/$PUBLICA.json" && log "avisos entregados al bot"
else
  log "sin avisos para el $PUBLICA: el bot no anunciará el número"
fi

# El número, a la Wayback Machine (ADR 0046): en segundo plano, para no retrasar nada; el script espera a
# que GitHub Pages lo despliegue y deja su registro en registro/archivo.log.
nohup python3 scripts/archivar.py "$FECHA" >> registro/archivo.log 2>&1 &

# Lo escrito por los agentes, al repositorio de la redacción (los mensajes de dias/ no se suben).
# Solo las carpetas que existen: si falta una, git add no añade nada y la redacción no se guarda.
# Las carpetas traducidas, una por idioma (ADR 0026); las de borradores no se suben (.gitignore).
TRAD=$(for c in $(python3 scripts/idiomas.py lista); do printf ' %s-%s' ediciones "$c" ilustraciones "$c" vinetas "$c" reportajes "$c" biblioteca "$c" repositorio "$c" comentario-semana "$c" hace-un-ano "$c"; done)
# shellcheck disable=SC2086
git add -A $(ls -d og/numeros videos reels multimedia ediciones ilustraciones vinetas avisos publicado.txt reportajes biblioteca repositorio reserva comunidades comentario-semana hace-un-ano $TRAD 2>/dev/null) >> "$REG" 2>&1 ||
  log "AVISO: no se pudo preparar lo escrito por la redacción para subirlo"
if ! git diff --cached --quiet; then
  git commit -qm "Número del $PUBLICA" || log "AVISO: no se pudo preparar el commit de la redacción"
fi
# Si desde el portátil se ha subido código mientras tanto, se coloca encima antes de subir. La nota
# va después del rebase, que cambia el identificador del commit. Sube también lo que un intento
# anterior dejó sin subir.
if [ -n "$(git rev-list '@{u}..HEAD' 2>/dev/null)" ]; then
  git pull -q --rebase && git notes --ref=ia add -f -m "$NOTA" HEAD && git push -q && git push -q origin refs/notes/ia ||
    log "AVISO: no se pudo subir la redacción a GitHub"
fi
touch "estado/$FECHA.publicado"
log "publicado el número del $PUBLICA"
