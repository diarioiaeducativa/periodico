#!/usr/bin/env bash
# SPDX-License-Identifier: AGPL-3.0-or-later
# Vuelve a publicar solo la web, sin avisos al bot ni Instagram, cuando el proceso del boletín deja en
# multimedia/AAAA-WW.json el pódcast y el vídeo de NotebookLM de la semana (ADR 0034). Lo lanza reloj.sh,
# siempre con el número del día ya publicado. Guarda además ese archivo en el repositorio de la redacción.
#
#   scripts/publicar-web.sh
set -uo pipefail

RAIZ="$(cd "$(dirname "$(readlink -f "$0")")/.." && pwd)"
cd "$RAIZ"
SITIO="${SITIO_REPO:-/sitio}"
REG="registro/multimedia.log"
# Lo hace un programa, sin IA: la nota lo dice para que nadie busque un modelo
NOTA="Sin IA: scripts/publicar-web.sh, con el pódcast y el vídeo que deja el boletín semanal"
mkdir -p registro

log() { printf '%s  %s\n' "$(date '+%F %T')" "$*" | tee -a "$REG"; }

python3 generar.py >> "$REG" 2>&1 || { log "ERROR: el generador falla"; exit 1; }
python3 -m pagefind --site sitio >> "$REG" 2>&1 || log "AVISO: no se pudo rehacer el índice del buscador; queda el anterior"

git -C "$SITIO" pull -q --ff-only >> "$REG" 2>&1 || { log "ERROR: no se pudo actualizar $SITIO"; exit 1; }
rsync -a --delete --exclude .git --exclude .github --exclude README.md --exclude LICENSE --exclude LICENSE-CODIGO \
  --exclude .nojekyll --exclude fuentes/OFL.txt sitio/ "$SITIO/"
git -C "$SITIO" add -A
if ! git -C "$SITIO" diff --cached --quiet; then
  git -C "$SITIO" commit -qm "La semana: pódcast y vídeo de cada grupo" &&
  git -C "$SITIO" notes --ref=ia add -f -m "$NOTA" HEAD || { log "ERROR: no se pudo preparar el commit del sitio"; exit 1; }
fi
if [ -n "$(git -C "$SITIO" rev-list '@{u}..HEAD' 2>/dev/null)" ]; then
  git -C "$SITIO" push -q && git -C "$SITIO" push -q origin refs/notes/ia || { log "ERROR: no se pudo subir el sitio"; exit 1; }
  log "sitio publicado: $(git -C "$SITIO" log --oneline -1)"
fi

# El archivo del boletín, al repositorio de la redacción, para que viaje con él
git add multimedia >> "$REG" 2>&1
if ! git diff --cached --quiet; then
  git commit -qm "Pódcast y vídeo de la semana" || log "AVISO: no se pudo preparar el commit de la redacción"
fi
if [ -n "$(git rev-list '@{u}..HEAD' 2>/dev/null)" ]; then
  git pull -q --rebase && git notes --ref=ia add -f -m "$NOTA" HEAD && git push -q && git push -q origin refs/notes/ia ||
    log "AVISO: no se pudo subir la redacción a GitHub"
fi
log "web publicada con el pódcast y el vídeo de la semana"
