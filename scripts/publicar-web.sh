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
# Lo hace un programa, sin IA, salvo la traducción del resumen de cada vídeo: la nota lo dice para que nadie
# busque otro modelo
NOTA="scripts/publicar-web.sh, con el pódcast y el vídeo que deja el boletín semanal. Sin IA, salvo la traducción del resumen de cada vídeo: Claude Sonnet 5.5 (claude-sonnet-5-5) · Claude Code, en el NAS"
mkdir -p registro

log() { printf '%s  %s\n' "$(date '+%F %T')" "$*" | tee -a "$REG"; }

# El resumen de cada vídeo, a las otras lenguas (ADR 0057). Si alguna no sale, su edición lo enseña en
# castellano y lo dice: no impide publicar.
bash scripts/multimedia-traducir.sh > /dev/null 2>> "$REG" || log "AVISO: algún resumen de los vídeos de la semana sale en castellano en las ediciones traducidas"

python3 generar.py >> "$REG" 2>&1 || { log "ERROR: el generador falla"; exit 1; }
python3 -m pagefind --site sitio >> "$REG" 2>&1 || log "AVISO: no se pudo rehacer el índice del buscador; queda el anterior"

# --rebase: la copia de los comentarios (ADR 0030) sube sola al sitio y puede ir por delante de un intento
# anterior que no llegó a subir; la nota del modelo sigue a su commit
git -c notes.rewriteRef=refs/notes/ia -C "$SITIO" pull -q --rebase >> "$REG" 2>&1 || { log "ERROR: no se pudo actualizar $SITIO"; exit 1; }
rsync -a --delete --exclude .git --exclude .github --exclude /comentarios/ --exclude README.md --exclude LICENSE --exclude LICENSE-CODIGO \
  --exclude .nojekyll --exclude fuentes/OFL.txt sitio/ "$SITIO/"
git -C "$SITIO" add -A
if ! git -C "$SITIO" diff --cached --quiet; then
  git -C "$SITIO" commit -qm "La semana: pódcast y vídeo de cada grupo" &&
  git -C "$SITIO" notes --ref=ia add -f -m "$NOTA" HEAD || { log "ERROR: no se pudo preparar el commit del sitio"; exit 1; }
fi
if [ -n "$(git -C "$SITIO" rev-list '@{u}..HEAD' 2>/dev/null)" ]; then
  # Si entretanto ha subido la copia de los comentarios, se pone encima y se vuelve a intentar
  { git -C "$SITIO" push -q || { git -c notes.rewriteRef=refs/notes/ia -C "$SITIO" pull -q --rebase && git -C "$SITIO" push -q; }; } &&
    git -C "$SITIO" push -q origin refs/notes/ia || { log "ERROR: no se pudo subir el sitio"; exit 1; }
  log "sitio publicado: $(git -C "$SITIO" log --oneline -1)"
fi

# El archivo del boletín, al repositorio de la redacción, para que viaje con él
git add -A multimedia $(ls -d multimedia-?? comentario-semana comentario-semana-?? 2>/dev/null) >> "$REG" 2>&1
if ! git diff --cached --quiet; then
  git commit -qm "Pódcast y vídeo de la semana" || log "AVISO: no se pudo preparar el commit de la redacción"
fi
if [ -n "$(git rev-list '@{u}..HEAD' 2>/dev/null)" ]; then
  git pull -q --rebase --autostash && git notes --ref=ia add -f -m "$NOTA" HEAD && git push -q && git push -q origin refs/notes/ia ||
    log "AVISO: no se pudo subir la redacción a GitHub"
fi
log "web publicada con el pódcast y el vídeo de la semana"
