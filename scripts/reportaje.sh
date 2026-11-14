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
# El reportaje sale siempre (ADR 0028): el jefe elige siempre un tema; si el verificador no lo da por
# bueno, el reportero lo corrige con sus motivos y se verifica otra vez; si el ilustrador estropea el
# archivo, sale sin infografía. Si aun así no hay, sale con 2 y noche.sh pone el reportaje de reserva
# (scripts/reserva_reportaje.py). Este guion nunca impide que salga el número.
#
# Con RESERVA=1 y una clave 2099-02-NN escribe un reportaje de reserva, sobre un tema que no caduque:
#   RESERVA=1 scripts/reportaje.sh 2099-02-01      (lo lanza reserva.sh; después, reserva_reportaje.py guardar)
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

agente() {   # el mismo de noche.sh, con un añadido opcional al encargo: sin terminal y sin leer fuera de la redacción (ADR 0002)
  local modelo=$1 paso=$2 minutos=$3 extra=${4:-} salida
  extra=${extra//\{FECHA\}/$FECHA}
  log "empieza $paso ($modelo)"
  salida=$({ sed -e "s/{FECHA}/$FECHA/g" -e "s/{PUBLICA}/$PUBLICA/g" "encargos/pasos/$paso.md"; if [ -n "$extra" ]; then printf '\n%s\n' "$extra"; fi; } \
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
. scripts/dibujos.sh   # revisar_dibujos (ADR 0005)
. scripts/traducir.sh   # traducir y traducidos (ADR 0026)
hay() { python3 -c 'import json,sys; sys.exit(0 if json.load(open(sys.argv[1])).get("hay_reportaje") else 1)' "$1" 2>/dev/null; }
sin() { log "sin reportaje: $*"; rm -f reportajes/"$FECHA".json $(traducidos reportajes); exit 2; }

log "=== reportaje del domingo $PUBLICA, con la semana que acaba el $FECHA"
if [ "${RESERVA:-0}" = 1 ]; then   # un reportaje de reserva: sin semana, sobre un tema que no caduque
  cat > "semanas/$FECHA.md" <<'RES'
# Reportaje de reserva (no hay mensajes de esta semana)

Este reportaje no sale de una semana concreta: se guarda de reserva y saldrá un domingo en que el
reportaje de la semana no haya podido salir, dentro de un mes como mucho. Elige un tema que no caduque
en ese tiempo: un documento de la Biblioteca digital (biblioteca/*.json) que merezca explicarse a fondo
y no haya tenido reportaje, o un asunto de fondo de lo ya publicado (ediciones/, reportajes/). Nada
que dependa de la fecha: ni «esta semana», ni «ayer», ni novedades que puedan cambiar en días. Sin
mensajes de los grupos («mensajes»: []), salvo que enlaces piezas ya publicadas del diario.
RES
else
  python3 scripts/semana.py "$DATOS" semanas "$FECHA" >> "$REG" 2>&1 || sin "la semana no tiene mensajes o no se pudieron leer"
fi
rm -f "reportajes-borrador/$FECHA-tema.json" "reportajes-borrador/$FECHA.json" "reportajes/$FECHA.json" $(traducidos reportajes)

agente "$OPUS" 7-reportaje-tema 20
json_ok "reportajes-borrador/$FECHA-tema.json" || sin "el jefe de reportajes no dejó el tema"
if ! hay "reportajes-borrador/$FECHA-tema.json"; then   # siempre hay reportaje: el jefe elige otro tema
  log "el jefe de reportajes no ve tema en la semana: se le pide otro"
  agente "$OPUS" 7-reportaje-tema 20 "Has dicho que la semana no da para un reportaje, pero el reportaje del domingo sale siempre. Elige un tema de las semanas anteriores que siga vivo (ediciones/, semanas/) o un documento de la Biblioteca digital (biblioteca/) que no haya tenido reportaje, y escribe de nuevo reportajes-borrador/{FECHA}-tema.json con \"hay_reportaje\": true."
  hay "reportajes-borrador/$FECHA-tema.json" || sin "el jefe de reportajes no ha encontrado tema ni a la segunda"
fi

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
if ! hay "reportajes/$FECHA.json"; then   # una segunda vuelta: el reportero lo corrige con los motivos del verificador
  motivo=$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1])).get("motivo",""))' "reportajes/$FECHA.json" 2>/dev/null)
  log "el verificador no lo da por bueno ($motivo): el reportero lo corrige y se verifica otra vez"
  rm -f "reportajes/$FECHA.json"
  agente "$OPUS" 8-reportaje-redaccion 60 "El verificador no ha dado por bueno tu primer borrador. Su motivo: «$motivo». Corrígelo a fondo con eso (quita o sustituye lo que no se pueda confirmar, con fuentes oficiales) y vuelve a escribir reportajes-borrador/{FECHA}.json."
  json_ok "reportajes-borrador/$FECHA.json" && agente "$SONNET" 9-reportaje-repaso 60
  hay "reportajes/$FECHA.json" || sin "el verificador no lo da por bueno ni a la segunda: $(python3 -c 'import json,sys; print(json.load(open(sys.argv[1])).get("motivo",""))' "reportajes/$FECHA.json" 2>/dev/null)"
fi

cp "reportajes/$FECHA.json" "reportajes-borrador/$FECHA-verificado.json"
agente "$SONNET" 10-reportaje-ilustracion 30
json_ok "reportajes/$FECHA.json" || { log "el ilustrador estropeó el JSON del reportaje: sale el verificado, sin infografía"; cp "reportajes-borrador/$FECHA-verificado.json" "reportajes/$FECHA.json"; }
# Uno de reserva no tiene número ni página donde mirar su infografía: se mira con el programa el
# domingo en que salga (noche.sh), y si falla sale sin ella
[ "${RESERVA:-0}" = 1 ] || revisar_dibujos "$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["id"])' "reportajes/$FECHA.json")"
# 11b. Si hay uno de reserva, el juez de reportajes elige el mejor de los dos (ADR 0028). Si gana el de
# reserva, se publica ese y el nuevo se guarda aparte, sin traducir; si no, el de reserva sigue guardado.
if [ "${RESERVA:-0}" != 1 ] && cand=$(python3 scripts/reserva_reportaje.py candidato 2>>"$REG") && [ -n "$cand" ]; then
  rm -f "reportajes-borrador/$FECHA-eleccion.json"
  agente "$OPUS" 11b-reportaje-eleccion 20 "El de reserva: $cand/reportajes.json (su infografía, en $cand/ilustraciones/)."
  elegido=$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1])).get("elegido",""))' "reportajes-borrador/$FECHA-eleccion.json" 2>/dev/null)
  log "juez de reportajes: ${elegido:-sin decisión (gana el nuevo)}"
  if [ "$elegido" = reserva ]; then
    rid=$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["id"])' "reportajes/$FECHA.json")
    mv -f "reportajes/$FECHA.json" "reportajes-borrador/$FECHA-descartado.json"
    for f in ilustraciones/"$FECHA-$rid".svg; do [ -e "$f" ] && mv -f "$f" "reportajes-borrador/$FECHA-descartado-$rid.svg"; done
    if python3 scripts/reserva_reportaje.py usar "$FECHA" >> "$REG" 2>&1; then
      # Su infografía no se pudo mirar en su página al escribirla: ahora sí, con revisor y una vuelta
      revisar_dibujos "$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["id"])' "reportajes/$FECHA.json")"
      log "reportaje listo (el de reserva): $(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["titular"])' "reportajes/$FECHA.json")"
      exit 0
    fi
    # Si al final no se pudo poner el de reserva, vuelve el nuevo
    log "no se pudo poner el de reserva: sale el nuevo"
    mv -f "reportajes-borrador/$FECHA-descartado.json" "reportajes/$FECHA.json"
    [ -e "reportajes-borrador/$FECHA-descartado-$rid.svg" ] && mv -f "reportajes-borrador/$FECHA-descartado-$rid.svg" "ilustraciones/$FECHA-$rid.svg"
  fi
fi
traducir 11-reportaje-traduccion reportaje 40
log "reportaje listo: $(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["titular"])' "reportajes/$FECHA.json")"
