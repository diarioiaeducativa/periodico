#!/usr/bin/env bash
# SPDX-License-Identifier: AGPL-3.0-or-later
# Un artículo de reserva del fondo de EduMedia-IAG (ADR 0077): una herramienta o una técnica que se compartió en
# el grupo hace semanas, sigue vigente y el diario no ha contado. Lo lanza reserva.sh con una clave provisional
# (2099-01-NN), cuando a la reserva le falta del grupo; también a mano:
#
#   scripts/edumedia-fondo.sh 2099-01-NN
#
# Cuatro agentes, uno detrás de otro, como la biblioteca (ADR 0006):
#  32. documentalista (Sonnet) → elige un candidato y lo comprueba en su web: ediciones-borrador/CLAVE.json
#  33. revisor (Sonnet, no ha escrito nada) → ediciones/CLAVE.json
#  34. ilustrador (Sonnet) → un dibujo, que pasa la revisión de dibujos (ADR 0005)
#  35. traductor (Sonnet, uno por idioma) → ediciones-XX/CLAVE.json (ADR 0026)
# Después, reserva.py guardar CLAVE edumedia lo pasa a reserva/CLAVE/. Sale con 0 si hay artículo y con 2 si no.
set -uo pipefail

RAIZ="$(cd "$(dirname "$(readlink -f "$0")")/.." && pwd)"
cd "$RAIZ"
FECHA="$1"
case $FECHA in 2099-*) ;; *) echo "edumedia-fondo.sh: solo con una clave de reserva (2099-01-NN)" >&2; exit 1 ;; esac
DATOS="${DATOS_BOT:-/bot-datos}"
SONNET="${MODELO_SONNET:-claude-sonnet-5-5}"
mkdir -p registro ediciones ediciones-borrador edumedia-fondo-entrada
REG="registro/$FECHA.log"

log() { printf '%s  %s\n' "$(date '+%F %T')" "$*" | tee -a "$REG"; }

agente() {   # el mismo de noche.sh: sin terminal y sin leer fuera de la redacción (ADR 0002)
  local modelo=$1 paso=$2 minutos=$3 salida
  log "empieza $paso ($modelo)"
  salida=$(sed -e "s/{FECHA}/$FECHA/g" "encargos/pasos/$paso.md" \
    | timeout "$((minutos * 60))" claude -p --model "$modelo" \
        --permission-mode acceptEdits --mcp-config scripts/buscar-mcp.json --allowedTools WebFetch WebSearch mcp__diario \
        --disallowedTools "Bash" "Read(//home/**)" "Read(//proc/**)" "Read(//sitio/**)" "Read(//etc/**)" \
        --output-format text 2>>"$REG")
  local codigo=$?
  printf '%s\n' "$salida" >> "$REG"
  log "acaba $paso (código $codigo)"
  return $codigo
}

json_ok() { python3 -c 'import json,sys; json.load(open(sys.argv[1]))' "$1" 2>/dev/null; }
piezas() { python3 -c 'import json,sys; print(" ".join(p["id"] for p in json.load(open(sys.argv[1])).get("piezas", [])))' "$1" 2>/dev/null; }
. scripts/dibujos.sh    # revisar_dibujos (ADR 0005)
. scripts/traducir.sh   # traducir y traducidos (ADR 0026)

python3 scripts/edumedia_fondo.py "$DATOS" "$FECHA" >> "$REG" 2>&1
case $? in
  0) ;;
  3) log "edumedia-fondo: no queda ningún candidato"; exit 2 ;;
  *) log "AVISO: no se pudieron preparar los candidatos de EduMedia"; exit 2 ;;
esac
log "=== fondo de EduMedia: $(tail -1 "$REG" | sed 's/^edumedia-fondo: //')"
rm -f "ediciones-borrador/$FECHA.json" "ediciones/$FECHA.json" $(traducidos ediciones)

for intento in 1 2; do
  agente "$SONNET" 32-edumedia-fondo-articulo 40
  json_ok "ediciones-borrador/$FECHA.json" && break
  log "el borrador del fondo de EduMedia no está o no es JSON válido (intento $intento)"
done
[ -n "$(piezas "ediciones-borrador/$FECHA.json")" ] || { log "edumedia-fondo: ningún candidato vale"; exit 2; }
for intento in 1 2; do
  agente "$SONNET" 33-edumedia-fondo-repaso 40
  json_ok "ediciones/$FECHA.json" && break
  log "el artículo repasado no está o no es JSON válido (intento $intento)"
done
ids=$(piezas "ediciones/$FECHA.json")
[ -n "$ids" ] || { log "edumedia-fondo: el revisor no da el artículo por bueno"; exit 2; }
python3 scripts/forma.py "ediciones/$FECHA.json" >> "$REG" 2>&1 || true   # el cuerpo, lista de párrafos, antes de dibujar y traducir

cp "ediciones/$FECHA.json" "ediciones-borrador/$FECHA-antes-dibujo.json"
agente "$SONNET" 34-edumedia-fondo-ilustracion 30
if ! json_ok "ediciones/$FECHA.json"; then   # el ilustrador lo ha roto: sin descripción del dibujo, pero sin perder la pieza
  log "AVISO: el ilustrador estropeó ediciones/$FECHA.json; vuelve a como estaba"
  cp "ediciones-borrador/$FECHA-antes-dibujo.json" "ediciones/$FECHA.json"
fi
rm -f "ediciones-borrador/$FECHA-antes-dibujo.json"
# shellcheck disable=SC2086
revisar_dibujos $ids
traducir 35-edumedia-fondo-traduccion edicion 30
log "edumedia-fondo listo: $ids"
