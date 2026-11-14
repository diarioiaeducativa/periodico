#!/usr/bin/env bash
# SPDX-License-Identifier: AGPL-3.0-or-later
# «Hace un año» (ADR 0040): lo que se hablaba en los grupos el mismo día del año anterior, contado desde
# hoy. Lo lanza noche.sh cada noche, cuando las piezas del día ya están; también a mano:
#
#   scripts/hace-un-ano.sh AAAA-MM-DD      (la fecha de las conversaciones del número, como noche.sh)
#
# Cuatro pasos: el redactor (Opus, que comprueba en internet cómo está hoy cada cosa) → hace-un-ano-borrador/;
# el verificador (Sonnet, no ha escrito nada) → hace-un-ano/; el ilustrador (Sonnet), el díptico «Entonces /
# Ahora», con la revisión de dibujos de siempre (ADR 0005); el traductor (Sonnet, uno por idioma) →
# hace-un-ano-XX/ e ilustraciones-XX/ (ADR 0026). Un programa comprueba la medida y los campos (scripts/hace_un_ano.py). Si no
# hay nada que valga la pena o no pasa el repaso, el número sale sin ella: nunca impide el número.
# Sale con 0 si hay pieza y con 2 si no.
set -uo pipefail

RAIZ="$(cd "$(dirname "$(readlink -f "$0")")/.." && pwd)"
cd "$RAIZ"
FECHA="$1"
PUBLICA=$(date -d "$FECHA + 1 day" +%F)
DATOS="${DATOS_BOT:-/bot-datos}"
SONNET="${MODELO_SONNET:-claude-sonnet-5-5}"
OPUS="${MODELO_OPUS:-claude-opus-5-5}"
mkdir -p registro hace-un-ano hace-un-ano-borrador
REG="registro/$FECHA.log"

log() { printf '%s  %s\n' "$(date '+%F %T')" "$*" | tee -a "$REG"; }

agente() {   # el mismo de noche.sh: sin terminal y sin leer fuera de la redacción (ADR 0002)
  local modelo=$1 paso=$2 minutos=$3 salida
  log "empieza $paso ($modelo)"
  salida=$(sed -e "s/{FECHA}/$FECHA/g" -e "s/{PUBLICA}/$PUBLICA/g" "encargos/pasos/$paso.md" \
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
. scripts/dibujos.sh    # revisar_dibujos (ADR 0005)
. scripts/traducir.sh   # traducir y traducidos (ADR 0026)
sin() { log "sin «Hace un año»: $*"; rm -f "hace-un-ano/$FECHA.json" $(traducidos hace-un-ano); exit 2; }
hay() { python3 -c 'import json,sys; sys.exit(0 if json.load(open(sys.argv[1])).get("hay_pieza") else 1)' "$1" 2>/dev/null; }

log "=== «Hace un año» del número del $PUBLICA"
python3 scripts/hace_un_ano.py entrada "$DATOS" "$FECHA" >> "$REG" 2>&1 || sin "no hay mensajes de hace un año"

rm -f "hace-un-ano-borrador/$FECHA.json" "hace-un-ano/$FECHA.json" $(traducidos hace-un-ano)
for intento in 1 2; do
  agente "$OPUS" 23-hace-un-ano 25
  json_ok "hace-un-ano-borrador/$FECHA.json" && break
  log "el borrador no está o no es JSON válido (intento $intento)"
done
json_ok "hace-un-ano-borrador/$FECHA.json" || sin "no hay borrador"
hay "hace-un-ano-borrador/$FECHA.json" || sin "el redactor no ha encontrado nada que valga la pena"

for intento in 1 2; do
  agente "$SONNET" 24-hace-un-ano-repaso 25
  if json_ok "hace-un-ano/$FECHA.json"; then
    hay "hace-un-ano/$FECHA.json" || sin "el verificador no la da por buena"
    m=$(python3 scripts/hace_un_ano.py comprobar "$FECHA") && break
    log "$m (intento $intento)"
    rm -f "hace-un-ano/$FECHA.json"
  else
    log "el verificador no dejó un JSON válido (intento $intento)"
  fi
done
json_ok "hace-un-ano/$FECHA.json" || sin "no ha pasado el repaso"

# El díptico «Entonces / Ahora», con la misma revisión que los demás dibujos (ADR 0005): si no pasa, sin dibujo
id=$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["piezas"][0]["id"])' "hace-un-ano/$FECHA.json")
cp "hace-un-ano/$FECHA.json" "registro/$FECHA-hace-un-ano-antes.json"
agente "$SONNET" 26-hace-un-ano-ilustracion 20
if json_ok "hace-un-ano/$FECHA.json" && [ "$(python3 scripts/hace_un_ano.py comprobar "$FECHA" >/dev/null; echo $?)" = 0 ]; then
  revisar_dibujos "$id"
else
  log "el ilustrador estropeó la pieza: sale sin dibujo"
  cp "registro/$FECHA-hace-un-ano-antes.json" "hace-un-ano/$FECHA.json"
  rm -f "ilustraciones/$FECHA-$id.svg"
fi

traducir 25-hace-un-ano-traduccion hace-un-ano 15
log "«Hace un año» listo: $(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["piezas"][0]["titular"])' "hace-un-ano/$FECHA.json")"
exit 0
