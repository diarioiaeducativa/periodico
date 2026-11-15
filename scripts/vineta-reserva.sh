#!/usr/bin/env bash
# SPDX-License-Identifier: AGPL-3.0-or-later
# Escribe una viñeta de reserva (ADR 0068): una tira de Tiza y Algoritmo sobre un asunto que no caduca, para el
# día en que el número no pueda tener la suya. La lanza reserva.sh cuando no queda ninguna vigente; también a mano:
#
#   scripts/vineta-reserva.sh
#
# El humorista (Opus) piensa cinco ideas y deja la mejor en vinetas/CLAVE.json; los traductores (Sonnet, uno por
# idioma) la pasan a vinetas-XX/; reserva_vineta.py la guarda en reserva/vinetas/CLAVE/. Sale con 0 si la guarda.
set -uo pipefail
RAIZ="$(cd "$(dirname "$(readlink -f "$0")")/.." && pwd)"
cd "$RAIZ"
FECHA=$(python3 scripts/reserva_vineta.py clave) || exit 1
PUBLICA="$FECHA"
SONNET="${MODELO_SONNET:-claude-sonnet-5-5}"
OPUS="${MODELO_OPUS:-claude-opus-5-5}"
mkdir -p registro vinetas
REG="registro/$FECHA.log"

log() { printf '%s  %s\n' "$(date '+%F %T')" "$*" | tee -a "$REG"; }

agente() {   # el mismo de noche.sh: sin terminal y sin leer fuera de la redacción (ADR 0002)
  local modelo=$1 paso=$2 minutos=$3 salida
  log "empieza $paso ($modelo)"
  salida=$(sed -e "s/{FECHA}/$FECHA/g" -e "s/{PUBLICA}/$PUBLICA/g" "encargos/pasos/$paso.md" \
    | timeout "$((minutos * 60))" claude -p --model "$modelo" \
        --permission-mode acceptEdits --mcp-config scripts/buscar-mcp.json --allowedTools WebFetch WebSearch mcp__diario \
        --disallowedTools "Bash" "Read(//home/**)" "Read(//proc/**)" "Read(//sitio/**)" "Read(//etc/**)" \
        --output-format text 2>>"$REG")
  local codigo=$?
  printf '%s\n' "$salida" >> "$REG"
  log "acaba $paso (código $codigo)"
  return $codigo
}
. scripts/traducir.sh   # traducir (ADR 0026)

log "=== viñeta de reserva, con la clave $FECHA"
rm -f vinetas/"$FECHA".json $(traducidos vinetas)
agente "$OPUS" 30-vineta-reserva 20
if ! python3 -c 'import json,sys; sys.exit(0 if json.load(open(sys.argv[1])).get("elegida") else 1)' "vinetas/$FECHA.json" 2>/dev/null; then
  log "sin viñeta de reserva: el humorista no dejó una válida"
  rm -f vinetas/"$FECHA".json
  exit 2
fi
m=$(python3 vineta.py --comprobar "vinetas/$FECHA.json") || log "comprobación de la viñeta de reserva: $(echo "$m" | tr '\n' ' ')"
traducir 31-vineta-reserva-traduccion vineta 10
python3 scripts/reserva_vineta.py guardar "$FECHA"
