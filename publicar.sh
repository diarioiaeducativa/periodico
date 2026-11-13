#!/bin/sh
# SPDX-License-Identifier: AGPL-3.0-or-later
# Regenera el sitio y lo sube al repositorio de GitHub Pages (diarioiaeducativa.github.io).
# Las licencias, el README y .nojekyll viven solo en el repositorio del sitio y no se tocan.
set -e
AQUI=$(cd "$(dirname "$0")" && pwd)
SITIO_REPO=${SITIO_REPO:-$HOME/Documentos/github/diarioiaeducativa.github.io}
python3 "$AQUI/generar.py"
python3 -m pagefind --site "$AQUI/sitio" >/dev/null   # el índice del buscador (ADR 0007)
git -C "$SITIO_REPO" -c notes.rewriteRef=refs/notes/ia pull -q --rebase   # la copia de los comentarios (ADR 0030) sube sola
rsync -a --delete --exclude .git --exclude .github --exclude /comentarios/ --exclude README.md --exclude LICENSE --exclude LICENSE-CODIGO \
  --exclude .nojekyll --exclude fuentes/OFL.txt "$AQUI/sitio/" "$SITIO_REPO/"
cd "$SITIO_REPO"
git add -A
if git diff --cached --quiet; then echo "Sin cambios que publicar."; exit 0; fi
git commit -qm "${1:-Actualización del diario}"
git notes --ref=ia add -f -m "Modelo: Claude Opus 5.5 (claude-opus-5-5) · Claude Code" HEAD
git push -q && git push -q origin refs/notes/ia
echo "Publicado: $(git log --oneline -1)"
