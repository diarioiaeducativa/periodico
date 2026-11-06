#!/usr/bin/env bash
# SPDX-License-Identifier: AGPL-3.0-or-later
# El reportaje del domingo: un tema de la semana, a fondo (ADR 0004). Lo lanza noche.sh la
# noche del sábado al domingo, cuando el número del día ya está preparado; también a mano:
#
#   scripts/reportaje.sh AAAA-MM-DD      (el sábado: la semana son los siete días que acaban en él)
#
# Cinco agentes, uno detrás de otro:
#   7. jefe de reportajes (Opus) → elige el tema: reportajes-borrador/FECHA-tema.json
#   8. reportero (Opus) → investiga y escribe: reportajes-borrador/FECHA.json
#   9. verificador (Sonnet, no ha escrito nada) → reportajes/FECHA.json
#  10. ilustrador (Sonnet) → la infografía;  11. traductor (Sonnet, uno por idioma) → reportajes-XX/ (ADR 0026)
# Sin verificación no hay reportaje, y el número del domingo sale igual: este guion nunca
# impide que salga. Sale con 0 si hay reportaje y con 2 si no (noche.sh lo apunta y avisa).
set -uo pipefail

RAIZ="$(cd "$(dirname "$(readlink -f "$0")")/.." && pwd)"
cd "$RAIZ"
FECHA="$1"
PUBLICA=$(date -d "$FECHA + 1 day" +%F)
DATOS="${DATOS_BOT:-/bot-datos}"
SONNET="${MODELO_SONNET:-claude-sonnet-5-5}"
OPUS="${MODELO_OPUS:-claude-opus-5-5}"
mkdir -p registro reportajes reportajes-borrador semanas
REG="registro/$FECHA.log"

log() { printf '%s  %s\n' "$(date '+%F %T')" "$*" | tee -a "$REG"; }

agente() {   # el mismo de noche.sh: sin terminal y sin leer fuera de la redacción (ADR 0002)
  local modelo=$1 paso=$2 minutos=$3 salida
  log "empieza $paso ($modelo)"
  salida=$(sed -e "s/{FECHA}/$FECHA/g" -e "s/{PUBLICA}/$PUBLICA/g" "encargos/pasos/$paso.md" \
    | timeout "$((minutos * 60))" claude -p --model "$modelo" \
        --permission-mode acceptEdits --allowedTools WebFetch WebSearch \
        --disallowedTools "Bash" "Read(//home/**)" "Read(//proc/**)" "Read(//sitio/**)" "Read(//etc/**)" \
        --output-format text 2>>"$REG")
  local codigo=$?
  printf '%s\n' "$salida" >> "$REG"
  log "acaba $paso (código $codigo)"
  return $codigo
}

json_ok() { python3 -c 'import json,sys; json.load(open(sys.argv[1]))' "$1" 2>/dev/null; }
. scripts/dibujos.sh   # revisar_dibujos (ADR 0005)
. scripts/traducir.sh   # traducir y traducidos (ADR 0026)
hay() { python3 -c 'import json,sys; sys.exit(0 if json.load(open(sys.argv[1])).get("hay_reportaje") else 1)' "$1" 2>/dev/null; }
sin() { log "sin reportaje: $*"; rm -f reportajes/"$FECHA".json $(traducidos reportajes); exit 2; }

log "=== reportaje del domingo $PUBLICA, con la semana que acaba el $FECHA"
python3 scripts/semana.py "$DATOS" semanas "$FECHA" >> "$REG" 2>&1 || sin "la semana no tiene mensajes o no se pudieron leer"
rm -f "reportajes-borrador/$FECHA-tema.json" "reportajes-borrador/$FECHA.json" "reportajes/$FECHA.json" $(traducidos reportajes)

agente "$OPUS" 7-reportaje-tema 20
json_ok "reportajes-borrador/$FECHA-tema.json" || sin "el jefe de reportajes no dejó el tema"
hay "reportajes-borrador/$FECHA-tema.json" || sin "la semana no da para un reportaje"

for intento in 1 2; do
  agente "$OPUS" 8-reportaje-redaccion 60
  json_ok "reportajes-borrador/$FECHA.json" && break
  log "el borrador del reportaje no está o no es JSON válido (intento $intento)"
done
hay "reportajes-borrador/$FECHA.json" || sin "no hay borrador del reportaje"

for intento in 1 2; do
  agente "$SONNET" 9-reportaje-repaso 60
  json_ok "reportajes/$FECHA.json" && break
  log "el reportaje verificado no está o no es JSON válido (intento $intento)"
done
hay "reportajes/$FECHA.json" || sin "el verificador no lo da por bueno: $(python3 -c 'import json,sys; print(json.load(open(sys.argv[1])).get("motivo",""))' "reportajes/$FECHA.json" 2>/dev/null)"

agente "$SONNET" 10-reportaje-ilustracion 30
json_ok "reportajes/$FECHA.json" || sin "el ilustrador estropeó el JSON del reportaje"
revisar_dibujos "$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["id"])' "reportajes/$FECHA.json")"
traducir 11-reportaje-traduccion reportaje 40
log "reportaje listo: $(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["titular"])' "reportajes/$FECHA.json")"
