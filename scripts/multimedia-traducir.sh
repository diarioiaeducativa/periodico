#!/usr/bin/env bash
# SPDX-License-Identifier: AGPL-3.0-or-later
# El resumen del vídeo semanal de cada grupo, a las otras lenguas (ADR 0057). El boletín lo deja en castellano
# en multimedia/AAAA-WW.json; aquí un traductor por idioma (Sonnet) escribe multimedia-XX/AAAA-WW.json, y un
# programa comprueba cada uno (scripts/multimedia.py). Lo lanza publicar-web.sh antes de montar la web, cuando
# llega o cambia el archivo de la semana; también a mano:
#
#   scripts/multimedia-traducir.sh
#
# Solo traduce lo que falta: las semanas y los idiomas cuya traducción no existe o salió de un resumen que el
# boletín ha cambiado después. Si un idioma no sale, su edición enseña el resumen en castellano y lo dice,
# como antes: nunca impide publicar. Sale con 0 si no queda nada por traducir y con 2 si queda algo.
set -uo pipefail

RAIZ="$(cd "$(dirname "$(readlink -f "$0")")/.." && pwd)"
cd "$RAIZ"
SONNET="${MODELO_SONNET:-claude-sonnet-5-5}"
mkdir -p registro
REG="registro/multimedia.log"

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

TRADUCCIONES=""
. scripts/traducir.sh   # traducir (ADR 0026); TRADUCCIONES se pone en cada semana con los idiomas que faltan

for intento in 1 2; do
  falta=$(python3 scripts/multimedia.py pendientes)
  [ -z "$falta" ] && break
  while read -r FECHA TRADUCCIONES; do   # traducir() llama FECHA a la clave del archivo: aquí, la semana
    [ -n "$FECHA" ] || continue
    log "resúmenes de los vídeos de la semana $FECHA: se traducen a $TRADUCCIONES (intento $intento)"
    for c in $TRADUCCIONES; do
      mkdir -p "multimedia-$c"
      rm -f "multimedia-$c/$FECHA.json"   # la anterior salió de otro texto: no puede darse por buena
    done
    traducir 27-multimedia-traduccion multimedia 8 < /dev/null
  done <<< "$falta"
done

falta=$(python3 scripts/multimedia.py pendientes)
if [ -n "$falta" ]; then
  log "resúmenes de los vídeos sin traducir (salen en castellano): $(printf '%s' "$falta" | tr '\n' ';')"
  exit 2
fi
exit 0
