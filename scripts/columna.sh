#!/usr/bin/env bash
# SPDX-License-Identifier: AGPL-3.0-or-later
# La columna de opinión de los miércoles (ADR 0092). La lanza noche.sh la noche del martes al miércoles (o con
# COLUMNA=1); también a mano:
#
#   scripts/columna.sh AAAA-MM-DD            (la fecha de las conversaciones del número, como noche.sh: el martes)
#   RESERVA=1 scripts/columna.sh AAAA-MM-DD  (la de reserva, con esa clave; la lanza reserva.sh si no hay ninguna)
#
# El columnista es un modelo de otra casa, GPT-6.2-Astra con Codex, que elige el tema, se documenta en la web y
# escribe (columnas-trabajo/FECHA/columna.json). No corre aquí: este script deja el encargo con todo el material
# (prompt.md) y un «pedido», y el NAS lo lanza en la caja cerrada del agente de noticias, con su cuenta de ChatGPT,
# sin terminal ni archivos (nas/columnista.sh, cada minuto en el crontab del NAS). Después, el
# verificador (Sonnet, no ha escrito nada) contrasta los datos sin tocar la tesis → columnas-borrador/FECHA-verificada.json,
# y un programa comprueba la medida y la forma (scripts/columna.py). Si hay una de reserva, el juez (Opus) elige entre
# las dos y la otra se descarta; si la nueva no vale, sale la de reserva. Al final, el traductor (Sonnet, uno por
# idioma) → columnas-XX/. Sin columna, el número sale igual: nunca lo impide. Sale con 0 si hay columna y con 2 si no.
set -uo pipefail

RAIZ="$(cd "$(dirname "$(readlink -f "$0")")/.." && pwd)"
cd "$RAIZ"
FECHA="$1"
PUBLICA=$(date -d "$FECHA + 1 day" +%F)
SONNET="${MODELO_SONNET:-claude-sonnet-5-5}"
OPUS="${MODELO_OPUS:-claude-opus-5-5}"
COLUMNISTA="${MODELO_COLUMNA:-gpt-6.2-astra}"            # por su nombre exacto
AUTOR="${AUTOR_COLUMNA:-GPT-6.2-Astra (OpenAI)}"          # la firma: el mismo modelo, como lo nombra su casa
mkdir -p registro columnas columnas-borrador
REG="${REG_COLUMNA:-registro/$FECHA.log}"
# La de reserva trabaja aparte (reserva-FECHA): la mañana del miércoles se escribe con la fecha del martes
if [ "${RESERVA:-0}" = 1 ]; then CLAVE="reserva-$FECHA"; MARCA=--reserva; else CLAVE="$FECHA"; MARCA=""; fi
B="columnas-borrador/$CLAVE"

log() { printf '%s  %s\n' "$(date '+%F %T')" "$*" | tee -a "$REG"; }

agente() {   # el mismo de noche.sh: sin terminal y sin leer fuera de la redacción (ADR 0002)
  local modelo=$1 paso=$2 minutos=$3 extra=${4:-} salida
  log "empieza $paso ($modelo)"
  salida=$( { sed -e "s/{FECHA}/$CLAVE/g" -e "s/{PUBLICA}/$PUBLICA/g" "encargos/pasos/$paso.md"; [ -n "$extra" ] && printf '\n%s\n' "$extra"; } \
    | timeout "$((minutos * 60))" claude -p --model "$modelo" \
        --permission-mode acceptEdits --mcp-config scripts/buscar-mcp.json --allowedTools WebFetch WebSearch mcp__diario \
        --disallowedTools "Bash" "Read(//home/**)" "Read(//proc/**)" "Read(//sitio/**)" "Read(//etc/**)" \
        --output-format text 2>>"$REG")
  local codigo=$?
  printf '%s\n' "$salida" >> "$REG"
  log "acaba $paso (código $codigo)"
  return $codigo
}

columnista() {   # lo lanza el NAS, fuera de este contenedor (nas/columnista.sh): aquí solo se pide y se espera
  local t="columnas-trabajo/$CLAVE" n=0 codigo
  rm -f "$t/hecho" "$t/columna.json"
  printf '%s\n' "$COLUMNISTA" > "$t/pedido"
  log "empieza el columnista ($COLUMNISTA, por nas/columnista.sh)"
  while [ ! -e "$t/hecho" ] && [ $n -lt 300 ]; do sleep 10; n=$((n + 1)); done   # 50 minutos como mucho
  if [ ! -e "$t/hecho" ]; then
    rm -f "$t/pedido"
    log "el columnista no ha respondido en 50 minutos (¿está la tarea de nas/columnista.sh en el crontab del NAS?)"
    return 1
  fi
  codigo=$(cat "$t/hecho")
  tail -n 40 "$t/codex.log" >> "$REG" 2>/dev/null
  log "acaba el columnista (código $codigo)"
  return "$codigo"
}

json_ok() { python3 -c 'import json,sys; json.load(open(sys.argv[1]))' "$1" 2>/dev/null; }
. scripts/traducir.sh   # traducir y traducidos (ADR 0026)

# La nueva: columnista, programa, verificador y programa otra vez. Deja $B-verificada.json o nada.
nueva() {
  rm -f "$B.json" "$B-verificada.json" "$B-nota.md" "$B-eleccion.json"
  python3 scripts/columna.py preparar "$FECHA" $MARCA >> "$REG" 2>&1 || { log "sin columna nueva: no hay material"; return 1; }
  local intento m
  for intento in 1 2; do
    rm -f "columnas-trabajo/$CLAVE/columna.json"
    columnista
    if json_ok "columnas-trabajo/$CLAVE/columna.json"; then
      python3 scripts/columna.py importar "$FECHA" "$AUTOR" $MARCA >> "$REG" 2>&1
      m=$(python3 scripts/columna.py comprobar "$B.json") && break
      log "$m (intento $intento)"
      case $m in *"no hay columna"*) return 1 ;; esac
      printf '\n\n# SEGUNDO INTENTO\n\nEl primero no valió: %s. Vuelve a escribir la columna entera con lo que pide el encargo.\n' "$m" >> "columnas-trabajo/$CLAVE/prompt.md"
    else
      log "el columnista no dejó columna.json válido (intento $intento)"
    fi
    rm -f "$B.json"
  done
  [ -f "$B.json" ] || return 1
  for intento in 1 2; do
    agente "$SONNET" 39-columna-verificacion 30
    if json_ok "$B-verificada.json"; then
      m=$(python3 scripts/columna.py comprobar "$B-verificada.json") && return 0
      log "$m (verificación, intento $intento)"
      case $m in *"no hay columna"*) return 1 ;; esac
      rm -f "$B-verificada.json"
    else
      log "el verificador no dejó un JSON válido (intento $intento)"
    fi
  done
  return 1
}

if [ "${RESERVA:-0}" = 1 ]; then
  log "=== columna de opinión de reserva (con los mensajes hasta el $FECHA)"
  if nueva && python3 scripts/columna.py guardar "$FECHA" >> "$REG" 2>&1; then
    log "columna de reserva lista: $(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["piezas"][0]["titular"])' "$B-verificada.json")"
    exit 0
  fi
  log "sin columna de reserva esta vez"
  exit 2
fi

log "=== columna de opinión del número del $PUBLICA"
rm -f "columnas/$FECHA.json" $(traducidos columnas)
hay_nueva=0; nueva && hay_nueva=1
RES=$(python3 scripts/columna.py reserva)
elegida=""
if [ "$hay_nueva" = 1 ] && [ -n "$RES" ]; then
  agente "$OPUS" 40-columna-eleccion 20 "La de reserva: $RES"
  elegida=$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1])).get("elegido",""))' "$B-eleccion.json" 2>/dev/null)
  log "juez de la columna: ${elegida:-sin decisión (la nueva)}"
  [ "$elegida" = reserva ] || elegida=nueva
elif [ "$hay_nueva" = 1 ]; then
  elegida=nueva
elif [ -n "$RES" ]; then
  elegida=reserva
  log "la columna nueva no ha salido: sale la de reserva"
fi
case $elegida in
  nueva)
    cp "$B-verificada.json" "columnas/$FECHA.json"
    python3 scripts/columna.py descartar >> "$REG" 2>&1 ;;
  reserva)
    python3 scripts/columna.py usar "$FECHA" >> "$REG" 2>&1 || { log "sin columna: no se pudo poner la de reserva"; exit 2; } ;;
  *)
    log "sin columna: ni la nueva vale ni queda una de reserva"
    exit 2 ;;
esac
traducir 38-columna-traduccion columna 15
log "columna lista ($elegida): $(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["piezas"][0]["titular"])' "columnas/$FECHA.json")"
exit 0
