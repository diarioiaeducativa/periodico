#!/usr/bin/env bash
# SPDX-License-Identifier: AGPL-3.0-or-later
# Traduce un día ya publicado a los idiomas que se indiquen (por defecto, a todos los que les falte),
# con los mismos encargos y la misma comprobación que cada noche (ADR 0026): la edición con su viñeta y
# sus dibujos, y la Biblioteca, el Repositorio y el reportaje, si ese día los hay. Sirve para traducir
# lo publicado antes de añadir un idioma y para rehacer una traducción que se quitó. Después,
# publicar-nas.sh lo sube con el número siguiente (o generar.py y publicar a mano).
#
#   scripts/traducir-dia.sh AAAA-MM-DD [idioma ...]
set -uo pipefail

RAIZ="$(cd "$(dirname "$(readlink -f "$0")")/.." && pwd)"
cd "$RAIZ"
FECHA="$1"; shift
SONNET="${MODELO_SONNET:-claude-sonnet-5-5}"
mkdir -p registro
REG="registro/$FECHA-traducir.log"

log() { printf '%s  %s\n' "$(date '+%F %T')" "$*" | tee -a "$REG"; }

agente() {   # el mismo de noche.sh: sin terminal y sin leer fuera de la redacción (ADR 0002)
  local modelo=$1 paso=$2 minutos=$3 salida
  log "empieza $paso ($modelo)"
  salida=$(sed -e "s/{FECHA}/$FECHA/g" "encargos/pasos/$paso.md" \
    | timeout "$((minutos * 60))" claude -p --model "$modelo" \
        --permission-mode acceptEdits --allowedTools WebFetch WebSearch \
        --disallowedTools "Bash" "Read(//home/**)" "Read(//proc/**)" "Read(//sitio/**)" "Read(//etc/**)" \
        --output-format text 2>>"$REG")
  local codigo=$?
  printf '%s\n' "$salida" >> "$REG"
  log "acaba $paso (código $codigo)"
  return $codigo
}
. scripts/traducir.sh   # traducir y traducidos

hay_piezas() { python3 -c 'import json,sys; d=json.load(open(sys.argv[1])); sys.exit(0 if d.get("piezas") or d.get("apartados") else 1)' "$1" 2>/dev/null; }
# Solo lo que falta en cada idioma, salvo que se pidan idiomas concretos (entonces se rehace)
pendientes() {
  local carpeta=$1 c
  if [ -n "$PEDIDOS" ]; then echo "$PEDIDOS"; return; fi
  for c in $(python3 scripts/idiomas.py lista); do [ -e "$carpeta-$c/$FECHA.json" ] || printf '%s ' "$c"; done
}
PEDIDOS="$*"
for par in "ediciones 5-traduccion edicion" "biblioteca 15-biblioteca-traduccion biblioteca" \
           "repositorio 18-repositorio-traduccion repositorio" "reportajes 11-reportaje-traduccion reportaje"; do
  set -- $par
  hay_piezas "$1/$FECHA.json" || continue
  TRADUCCIONES=$(pendientes "$1")
  [ -n "${TRADUCCIONES// /}" ] || continue
  log "=== $1 del $FECHA → $TRADUCCIONES"
  traducir "$2" "$3" 40
done
log "traducciones del $FECHA hechas"
