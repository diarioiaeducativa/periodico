#!/usr/bin/env bash
# SPDX-License-Identifier: AGPL-3.0-or-later
# «La semana en vídeo» (ADR 0016). Lo lanza noche.sh la noche del sábado, después de la traducción;
# también a mano:
#
#   scripts/reel-semana.sh AAAA-MM-DD      (la fecha del sábado)
#
# 19. guionista del reel (Sonnet) → reels/FECHA.json; después scripts/reel-semana.py monta el
# vídeo sin IA (web: videos/, y el vídeo a Internet Archive, ADR 0037; Instagram: instagram/reel-FECHA/). Si el guion no vale o un texto no
# cabe, el agente lo rehace una vez. Nunca impide el número. Sale con 0 si hay vídeo y con 2 si no.
set -uo pipefail

RAIZ="$(cd "$(dirname "$(readlink -f "$0")")/.." && pwd)"
cd "$RAIZ"
FECHA="$1"
DESDE=$(date -d "$FECHA - 6 days" +%F)
SONNET="${MODELO_SONNET:-claude-sonnet-5-5}"
mkdir -p registro reels videos
REG="registro/$FECHA.log"

log() { printf '%s  %s\n' "$(date '+%F %T')" "$*" | tee -a "$REG"; }

agente() {   # el mismo de noche.sh: sin terminal y sin leer fuera de la redacción (ADR 0002)
  local modelo=$1 paso=$2 minutos=$3 nota=${4:-} salida
  log "empieza $paso ($modelo)"
  salida=$( { sed -e "s/{FECHA}/$FECHA/g" -e "s/{DESDE}/$DESDE/g" "encargos/pasos/$paso.md"; [ -n "$nota" ] && printf '\n%s\n' "$nota"; } \
    | timeout "$((minutos * 60))" claude -p --model "$modelo" \
        --permission-mode acceptEdits --allowedTools WebFetch WebSearch \
        --disallowedTools "Bash" "Read(//home/**)" "Read(//proc/**)" "Read(//sitio/**)" "Read(//etc/**)" \
        --output-format text 2>>"$REG")
  local codigo=$?
  printf '%s\n' "$salida" >> "$REG"
  log "acaba $paso (código $codigo)"
  return $codigo
}

agente "$SONNET" 19-reel-guion 20
for intento in 1 2; do
  error=$(python3 scripts/reel-semana.py "$FECHA" 2>&1 >>"$REG")
  codigo=$?
  if [ $codigo = 0 ]; then
    log "reel de la semana hecho"
    # A Internet Archive antes de generar el número, para que el vídeo no entre en el repositorio del
    # sitio (ADR 0037). Si archive.org falla, la web sirve la copia local y se reintenta cada noche.
    python3 scripts/subir-videos.py --minutos 90 >> "$REG" 2>&1 || log "AVISO: el vídeo no ha llegado a Internet Archive; esta semana va en el sitio"
    exit 0
  fi
  printf '%s\n' "$error" >> "$REG"
  [ $intento = 2 ] && break
  log "el reel no sale ($error): el guionista lo rehace una vez"
  agente "$SONNET" 19-reel-guion 20 "El guion anterior no ha servido: $error. Corrígelo (textos más cortos si no caben) y vuelve a escribir reels/$FECHA.json."
done
log "AVISO: esta semana no hay reel"
rm -f "reels/$FECHA.json"
exit 2
