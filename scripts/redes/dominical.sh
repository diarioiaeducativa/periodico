#!/usr/bin/env bash
# SPDX-License-Identifier: AGPL-3.0-or-later
# El dominical en X, Bluesky y LinkedIn (ADR 0027): el domingo a las 12:00, el vídeo de la semana con
# el reportaje y el texto que dejó reel-semana.py en dominical/<sábado>.json. Instagram lo publica el
# propio diario (scripts/instagram.py reel).
#
# Corre en el contenedor del BOLETÍN, no en el del diario: allí están las sesiones de las tres redes y
# sus programas (scripts/redes/ del boletín, que ya publican cada lunes). Su reloj lo llama cada cuarto
# de hora; el diario está montado en /diario, solo para leer. Una red que falle no para las demás: se
# reintenta en la vuelta siguiente, dos veces como mucho, y después se avisa a Juanjo.
#
#   /diario/scripts/redes/dominical.sh               lo que toque ahora (lo normal)
#   /diario/scripts/redes/dominical.sh --comprobar   sesiones, textos y vídeo, sin publicar nada
set -u
DIARIO="${DIARIO:-/diario}"
ESTADO="$HOME/.local/state/diario-dominical"
mkdir -p "$ESTADO"
COMPROBAR=0; [ "${1:-}" = "--comprobar" ] && COMPROBAR=1
SAB="${SABADO:-$(date -d yesterday +%F)}"
F="$DIARIO/dominical/$SAB.json"
REG="$ESTADO/$SAB.log"
log() { printf '%s  %s\n' "$(date '+%F %T')" "$*" | tee -a "$REG"; }
avisar() { avisar-juanjo --de "Diario de IA Educativa" "$1" >/dev/null 2>&1 || true; }

if [ "$COMPROBAR" = 0 ]; then
  [ "$(date +%u)" = 7 ] || exit 0
  [ -f "$F" ] || exit 0
  ahora=$(( 10#$(date +%H) * 60 + 10#$(date +%M) ))
  hora=$(python3 -c 'import json,sys; h,m=json.load(open(sys.argv[1]))["hora"].split(":"); print(int(h)*60+int(m))' "$F")
  [ "$ahora" -ge "$hora" ] || exit 0
  # Pasadas seis horas ya no se publica: un vídeo del domingo a medianoche no sirve
  if [ "$ahora" -ge $((hora + 360)) ]; then exit 0; fi
elif [ ! -f "$F" ]; then
  echo "dominical: no hay $F; para comprobar con otro sábado, SABADO=AAAA-MM-DD"; exit 1
fi

campo() { python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))[sys.argv[2]])' "$F" "$1"; }
VIDEO="$DIARIO/$(campo video)"
campo corto > "$ESTADO/$SAB-corto.txt"
campo largo > "$ESTADO/$SAB-largo.txt"
if [ ! -s "$VIDEO" ]; then
  [ -e "$ESTADO/$SAB.sin-video" ] || { touch "$ESTADO/$SAB.sin-video"; log "no está el vídeo $VIDEO"; avisar "El dominical no puede salir en X, Bluesky ni LinkedIn: falta el vídeo ($VIDEO). Registro: /volume1/docker/boletin-semanal/home/.local/state/diario-dominical/$SAB.log"; }
  exit 0
fi
cd /proyecto
PY=.venv/bin/python
CHROME=$(ls -d /opt/playwright/chromium-*/chrome-linux64/chrome 2>/dev/null | tail -1)
curl -s -m 3 127.0.0.1:9222/json/version >/dev/null && YA_HABIA=1

red() {   # red NOMBRE: publica en esa red si no está hecha; dos intentos como mucho
  local r=$1 n
  [ -e "$ESTADO/$SAB.$r" ] && return 0
  n=$(cat "$ESTADO/$SAB.$r-intentos" 2>/dev/null || echo 0)
  [ "$COMPROBAR" = 0 ] && [ "$n" -ge 2 ] && return 0
  local pub=(); [ "$COMPROBAR" = 0 ] && pub=(--publicar)
  log "=== $r$([ "$COMPROBAR" = 1 ] && echo ' (comprobación)')"
  case $r in
    bluesky)  $PY scripts/redes/publicar_bluesky.py "$ESTADO/$SAB-corto.txt" --video "$VIDEO" "${pub[@]}" >> "$REG" 2>&1 ;;
    x)        $PY scripts/redes/publicar_x_suelto.py "$ESTADO/$SAB-corto.txt" --video "$VIDEO" --chrome "$CHROME" "${pub[@]}" >> "$REG" 2>&1 ;;
    linkedin) $PY "$DIARIO/scripts/redes/dominical_linkedin.py" "$ESTADO/$SAB-largo.txt" "$VIDEO" \
                $([ "$COMPROBAR" = 1 ] && echo --comprobar) >> "$REG" 2>&1 ;;
  esac
  local codigo=$?
  [ "$COMPROBAR" = 1 ] && { log "$r: código $codigo"; return 0; }
  if [ $codigo = 0 ]; then
    touch "$ESTADO/$SAB.$r"; log "$r: publicado"
  else
    echo $((n + 1)) > "$ESTADO/$SAB.$r-intentos"
    log "$r: falló (intento $((n + 1)))"
    [ $((n + 1)) -ge 2 ] && avisar "El dominical no ha podido salir en $r tras dos intentos; las demás redes no se ven afectadas. Registro: /volume1/docker/boletin-semanal/home/.local/state/diario-dominical/$SAB.log"
  fi
}
red bluesky
red x
red linkedin
[ -z "${YA_HABIA:-}" ] && ./scripts/navegador-linkedin.sh cerrar >/dev/null 2>&1
exit 0
