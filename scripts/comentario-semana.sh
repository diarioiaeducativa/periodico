#!/usr/bin/env bash
# SPDX-License-Identifier: AGPL-3.0-or-later
# El comentario de la semana (ADR 0038): lo más importante de lo que contó el diario, para la página
# semana/AAAA-WW/, debajo del pódcast y el vídeo. Lo lanza noche.sh la noche del domingo al lunes, cuando
# ya están las piezas con los mensajes del domingo, que cierran la semana; también a mano:
#
#   scripts/comentario-semana.sh AAAA-WW
#
# Tres pasos: el redactor (Opus) → comentario-semana-borrador/; el revisor (Sonnet, no ha escrito nada)
# → comentario-semana/; el traductor (Sonnet, uno por idioma) → comentario-semana-XX/ (ADR 0026). Después
# de cada uno, un programa comprueba la medida y los enlaces (scripts/comentario_semana.py). Si no sale,
# la página sale sin comentario: nunca impide el número. Sale con 0 si hay comentario y con 2 si no.
set -uo pipefail

RAIZ="$(cd "$(dirname "$(readlink -f "$0")")/.." && pwd)"
cd "$RAIZ"
SEMANA="$1"
FECHA="$SEMANA"   # los encargos y traducir() llaman FECHA a la clave del archivo: aquí, la semana
SONNET="${MODELO_SONNET:-claude-sonnet-5-5}"
OPUS="${MODELO_OPUS:-claude-opus-5-5}"
mkdir -p registro comentario-semana comentario-semana-borrador
REG="registro/semana-$SEMANA.log"

log() { printf '%s  %s\n' "$(date '+%F %T')" "$*" | tee -a "$REG"; }

agente() {   # el mismo de noche.sh: sin terminal y sin leer fuera de la redacción (ADR 0002)
  local modelo=$1 paso=$2 minutos=$3 salida
  log "empieza $paso ($modelo)"
  salida=$(sed -e "s/{FECHA}/$FECHA/g" "encargos/pasos/$paso.md" \
    | timeout "$((minutos * 60))" claude -p --model "$modelo" \
        --permission-mode acceptEdits --mcp-config scripts/buscar-mcp.json --allowedTools WebFetch WebSearch mcp__diario__buscar \
        --disallowedTools "Bash" "Read(//home/**)" "Read(//proc/**)" "Read(//sitio/**)" "Read(//etc/**)" \
        --output-format text 2>>"$REG")
  local codigo=$?
  printf '%s\n' "$salida" >> "$REG"
  log "acaba $paso (código $codigo)"
  return $codigo
}

json_ok() { python3 -c 'import json,sys; json.load(open(sys.argv[1]))' "$1" 2>/dev/null; }
. scripts/traducir.sh   # traducir y traducidos (ADR 0026)
sin() { log "sin comentario de la semana: $*"; rm -f "comentario-semana/$SEMANA.json" $(traducidos comentario-semana); exit 2; }
hay() { python3 -c 'import json,sys; sys.exit(0 if json.load(open(sys.argv[1])).get("hay_comentario") else 1)' "$1" 2>/dev/null; }

log "=== comentario de la semana $SEMANA"
python3 scripts/comentario_semana.py entrada "$SEMANA" >> "$REG" 2>&1 || sin "la semana no tiene piezas"

rm -f "comentario-semana-borrador/$SEMANA.json" "comentario-semana/$SEMANA.json" $(traducidos comentario-semana)
for intento in 1 2; do
  agente "$OPUS" 20-comentario-semana 20
  json_ok "comentario-semana-borrador/$SEMANA.json" && break
  log "el borrador no está o no es JSON válido (intento $intento)"
done
json_ok "comentario-semana-borrador/$SEMANA.json" || sin "no hay borrador"
hay "comentario-semana-borrador/$SEMANA.json" || sin "el redactor no lo ha escrito"

for intento in 1 2; do
  agente "$SONNET" 21-comentario-semana-repaso 20
  if json_ok "comentario-semana/$SEMANA.json"; then
    hay "comentario-semana/$SEMANA.json" || sin "el revisor no lo da por bueno"
    m=$(python3 scripts/comentario_semana.py comprobar "$SEMANA") && break
    log "$m (intento $intento)"
    rm -f "comentario-semana/$SEMANA.json"
  else
    log "el revisor no dejó un JSON válido (intento $intento)"
  fi
done
json_ok "comentario-semana/$SEMANA.json" || sin "no ha pasado el repaso"

traducir 22-comentario-semana-traduccion comentario-semana 15
log "comentario de la semana $SEMANA listo: $(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["titulo"])' "comentario-semana/$SEMANA.json")"
exit 0
