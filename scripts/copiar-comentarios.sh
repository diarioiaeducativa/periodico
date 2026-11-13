#!/usr/bin/env bash
# SPDX-License-Identifier: AGPL-3.0-or-later
# La copia de los comentarios en el sitio (ADR 0030), desde el NAS: la lanza nas/reloj.sh cada dos minutos.
# Trabaja en un clon propio y parcial del sitio (solo comentarios/), para no cruzarse con /sitio, que es de la
# publicación del número. Sube solo si algo ha cambiado. Las subidas del NAS despliegan GitHub Pages; las de una
# acción con GITHUB_TOKEN no lo harían, y las claves de despliegue no pueden subir flujos (por eso no es una acción).
#
#   scripts/copiar-comentarios.sh
# Lee el token de ~/.config/diario-comentarios/github (de grano fino de Juanjo: con él basta para leer las
# Discussions, que son públicas). Si falla, avisa una vez y otra cuando vuelve a funcionar.
set -uo pipefail
RAIZ="$(cd "$(dirname "$(readlink -f "$0")")/.." && pwd)"
CLON="${COMENTARIOS_CLON:-$HOME/comentarios-sitio}"
TOKEN_ARCHIVO="$HOME/.config/diario-comentarios/github"
FALLO="$RAIZ/estado/comentarios.fallo"
LOG="$RAIZ/registro/comentarios.log"
SSH="$RAIZ/scripts/ssh-reintenta.sh -i $HOME/.ssh/sitio -o IdentitiesOnly=yes -o UserKnownHostsFile=$HOME/.ssh/known_hosts"

avisar() { avisar-juanjo --de "Diario de IA Educativa" "$1" >/dev/null 2>&1 || true; }
log() { printf '%s  %s\n' "$(date '+%F %T')" "$*" >> "$LOG"; }
fallar() {
  log "ERROR: $1"
  if [ ! -e "$FALLO" ]; then
    echo "$1" > "$FALLO"
    avisar "Los comentarios del diario no se están copiando a la web: $1. En giscus (botón «Comentar») se siguen viendo. Registro: /volume1/docker/diario-ia-educativa/repo/registro/comentarios.log"
  fi
  exit 1
}

[ -s "$TOKEN_ARCHIVO" ] || fallar "falta el token de GitHub ($TOKEN_ARCHIVO)"
export GITHUB_TOKEN="$(cat "$TOKEN_ARCHIVO")"

if [ ! -d "$CLON/.git" ]; then
  rm -rf "$CLON"
  git -c core.sshCommand="$SSH" clone -q --depth 1 --filter=blob:none --no-checkout \
    git@github.com:diarioiaeducativa/diarioiaeducativa.github.io.git "$CLON" || fallar "no se puede descargar el repositorio del sitio"
  git -C "$CLON" config core.sshCommand "$SSH"
  git -C "$CLON" sparse-checkout set --no-cone /comentarios/
  git -C "$CLON" config user.name "Diario de IA Educativa (comentarios)"
  git -C "$CLON" config user.email "diarioiaeducativa@users.noreply.github.com"
fi
cd "$CLON"
TMP=$(mktemp -d); trap 'rm -rf "$TMP"' EXIT
python3 "$RAIZ/scripts/copiar-comentarios.py" "$TMP/comentarios" > "$TMP/salida" 2>&1 || fallar "GitHub no da los comentarios ($(tail -1 "$TMP/salida"))"
# Si entretanto ha salido el número, se vuelve a poner encima de lo nuevo (cinco intentos)
for intento in 1 2 3 4 5; do
  git fetch -q --depth 1 origin main && git reset -q --hard origin/main || { sleep 10; continue; }
  rm -rf comentarios && { [ ! -d "$TMP/comentarios" ] || cp -r "$TMP/comentarios" comentarios; }
  git add -A --sparse comentarios 2>/dev/null || git add -A --sparse .
  if git diff --cached --quiet; then
    [ -e "$FALLO" ] && { rm -f "$FALLO"; log "vuelve a funcionar"; avisar "Los comentarios del diario vuelven a copiarse a la web."; }
    exit 0
  fi
  git commit -qm "Copia de los comentarios ($(cat "$TMP/salida"))"
  if git push -q origin HEAD:main 2>> "$LOG"; then
    log "subida: $(cat "$TMP/salida")"
    [ -e "$FALLO" ] && { rm -f "$FALLO"; avisar "Los comentarios del diario vuelven a copiarse a la web."; }
    exit 0
  fi
  sleep $((intento * 10))
done
fallar "no se puede subir la copia al sitio"
