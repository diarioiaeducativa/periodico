#!/usr/bin/env bash
# SPDX-License-Identifier: AGPL-3.0-or-later
# Dibuja las piezas de un número que se quedaron sin dibujo (o las que se indiquen), con la
# misma revisión que cada noche (ADR 0005), y las traduce al catalán. Sirve para los números
# anteriores al 03-11-2026, cuando solo se dibujaban las piezas de importancia 1 y 2, y para
# volver a intentar un dibujo retirado. Después, publicar-nas.sh lo sube con el número siguiente.
#
#   scripts/dibujar.sh AAAA-MM-DD [id ...]
set -uo pipefail

RAIZ="$(cd "$(dirname "$(readlink -f "$0")")/.." && pwd)"
cd "$RAIZ"
FECHA="$1"; shift
SONNET="${MODELO_SONNET:-claude-sonnet-5-5}"
mkdir -p registro
REG="registro/$FECHA-dibujos.log"

log() { printf '%s  %s\n' "$(date '+%F %T')" "$*" | tee -a "$REG"; }

agente() {   # el mismo de noche.sh, con {IDS}: sin terminal y sin leer fuera de la redacción (ADR 0002)
  local modelo=$1 paso=$2 minutos=$3 salida
  log "empieza $paso ($modelo)"
  salida=$(sed -e "s/{FECHA}/$FECHA/g" -e "s/{IDS}/$IDS/g" "encargos/pasos/$paso.md" \
    | timeout "$((minutos * 60))" claude -p --model "$modelo" \
        --permission-mode acceptEdits --allowedTools WebFetch WebSearch \
        --disallowedTools "Bash" "Read(//home/**)" "Read(//proc/**)" "Read(//sitio/**)" "Read(//etc/**)" \
        --output-format text 2>>"$REG")
  local codigo=$?
  printf '%s\n' "$salida" >> "$REG"
  log "acaba $paso (código $codigo)"
  return $codigo
}
. scripts/dibujos.sh   # revisar_dibujos y revisar_dibujos_ca

if [ $# -gt 0 ]; then
  ids="$*"
else
  ids=$(python3 -c '
import json, pathlib, sys
f = sys.argv[1]
d = json.load(open(f"ediciones/{f}.json"))
ids = [p["id"] for p in d.get("piezas", [])]
print(" ".join(i for i in ids if not pathlib.Path("ilustraciones/%s-%s.svg" % (f, i)).exists()))
' "$FECHA")
fi
[ -n "$ids" ] || { log "dibujos del $FECHA: no falta ninguno"; exit 0; }
IDS=$(echo "$ids" | sed 's/ /, /g')
log "=== dibujos que faltan del $FECHA: $ids"
cp "ediciones/$FECHA.json" "registro/$FECHA-antes.json"
agente "$SONNET" 2d-ilustraciones-faltan 30
python3 -c 'import json,sys; json.load(open(sys.argv[1]))' "ediciones/$FECHA.json" 2>/dev/null \
  || { log "ERROR: el ilustrador estropeó la edición: se deja como estaba"; cp "registro/$FECHA-antes.json" "ediciones/$FECHA.json"; exit 1; }
# shellcheck disable=SC2086
revisar_dibujos $ids
hechos=$(for id in $ids; do [ -e "ilustraciones/$FECHA-$id.svg" ] && printf '%s ' "$id"; done)
[ -n "$hechos" ] || { log "ningún dibujo ha pasado la revisión"; exit 0; }
IDS=$(echo "$hechos" | sed 's/ *$//; s/ /, /g')
if [ -e "ediciones-ca/$FECHA.json" ]; then
  cp "ediciones-ca/$FECHA.json" "registro/$FECHA-antes-ca.json"
  agente "$SONNET" 2e-ilustraciones-traduccion 20
  python3 -c 'import json,sys; json.load(open(sys.argv[1]))' "ediciones-ca/$FECHA.json" 2>/dev/null \
    || { log "la traducción estropeó ediciones-ca: se deja como estaba"; cp "registro/$FECHA-antes-ca.json" "ediciones-ca/$FECHA.json"; }
  revisar_dibujos_ca
fi
log "dibujos del $FECHA hechos: $hechos"
