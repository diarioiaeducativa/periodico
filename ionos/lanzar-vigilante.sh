#!/bin/sh
# SPDX-License-Identifier: AGPL-3.0-or-later
# Lanzador del vigilante desde el hosting de IONOS (ADR 0021). GitHub Actions retrasa horas, o se
# salta, las pasadas programadas del vigilante; desde aquí se lanzan a su hora. No publica nada: si
# el número de hoy no está en la web, pide a GitHub que ejecute el vigilante (workflow_dispatch con
# simular=false), que lo saca con la reserva y avisa a Juanjo. Si GitHub no lo acepta, avisa él.
#
#   lanzar-vigilante.sh              mira la web y, si falta el número de hoy, lanza el vigilante
#   lanzar-vigilante.sh --comprobar  el token sirve y no caduca pronto (avisa a 30, 14, 7, 3 y 1 días)
#   lanzar-vigilante.sh --probar     lo mismo que sin opciones, sin lanzar nada ni avisar
#   HOY_PRUEBA=2099-01-01 lanzar-vigilante.sh --probar   el camino de cuando falta el número
#
# En sh, sin PHP (el php de esta shell es el 4.4.9). Vive en ~/.diario-vigilante/ con:
#   token        token de GitHub de grano fino, solo con «Actions: read and write» en
#                diarioiaeducativa/periodico (nada más)
#   config.json  el del bot «Agentes IA», copiado de ~/.vigilancia-nas/config.json
#   .htaccess    la carpeta está dentro de la web: nada de aquí se sirve
#
# crontab (la hora del hosting es la de Madrid):
#   12 9,10,12,16 * * * $HOME/.diario-vigilante/lanzar-vigilante.sh >>$HOME/.diario-vigilante/cron.log 2>&1
#   40 8 * * *          $HOME/.diario-vigilante/lanzar-vigilante.sh --comprobar >>$HOME/.diario-vigilante/cron.log 2>&1
set -u
BASE=$(dirname "$0")
TOKEN=$(cat "$BASE/token" 2>/dev/null)
CONFIG="$BASE/config.json"
WEB="https://diarioiaeducativa.github.io/"
API="https://api.github.com/repos/diarioiaeducativa/periodico/actions/workflows/vigilante.yml"
MODO="${1:-}"
export TZ=Europe/Madrid
HOY=$(date +%F)
[ "$MODO" = --probar ] && HOY=${HOY_PRUEBA:-$HOY}
ahora() { date '+%F %T'; }

leer() {   # leer <clave>: mismo formato que avisar-juanjo y latido.sh
  sed -n 's/.*"'"$1"'"[[:space:]]*:[[:space:]]*"\{0,1\}\([^",}]*\)"\{0,1\}.*/\1/p' "$CONFIG" 2>/dev/null | head -1
}
avisar() {
  echo "$(ahora) AVISO: $1"
  [ "$MODO" = --probar ] && return 0
  curl -s -o /dev/null --max-time 30 "https://api.telegram.org/bot$(leer token)/sendMessage" \
    --data-urlencode "chat_id=$(leer chat_id)" \
    --data-urlencode "text=Diario de IA Educativa · lanzador del vigilante (IONOS): $1"
}

if [ "$MODO" = --comprobar ]; then
  [ -n "$TOKEN" ] || { avisar "Falta el token de GitHub en ~/.diario-vigilante/token del hosting: si el NAS cae, el número puede no salir hasta que GitHub pase solo."; exit 1; }
  cab=$(curl -s -D - -o /dev/null --max-time 30 -H "Authorization: Bearer $TOKEN" \
    -H "Accept: application/vnd.github+json" "$API")
  cod=$(printf '%s' "$cab" | sed -n '1s/^HTTP[^ ]* \([0-9]*\).*/\1/p')
  if [ "$cod" != 200 ]; then
    avisar "El token de GitHub con el que se lanza el vigilante ya no sirve (HTTP ${cod:-sin respuesta}). Si el NAS cae, el número puede no salir hasta que GitHub pase solo. Hay que crear otro (ionos/lanzar-vigilante.sh lo explica)."
    exit 1
  fi
  # GitHub dice en cada respuesta cuándo caduca un token: «2027-11-08 11:30:00 +0100»
  cad=$(printf '%s' "$cab" | tr -d '\r' | sed -n 's/^[Gg]ithub-[Aa]uthentication-[Tt]oken-[Ee]xpiration: //p')
  if [ -n "$cad" ]; then
    dias=$(( ($(date -d "$cad" +%s) - $(date +%s)) / 86400 ))
    echo "$(ahora) token válido; caduca el $cad (quedan $dias días)"
    case $dias in 30|14|7|3|1|0)
      avisar "El token de GitHub del lanzador del vigilante caduca el $(date -d "$cad" +%d-%m-%Y) (quedan $dias días). Hay que crear otro y dejarlo en ~/.diario-vigilante/token del hosting." ;;
    esac
  else
    echo "$(ahora) token válido, sin caducidad"
  fi
  exit 0
fi

portada=$(curl -s --max-time 60 "$WEB") || { echo "$(ahora) no se puede leer la web; no se hace nada"; exit 1; }
sale=$(printf '%s' "$portada" | grep -o '<time datetime="[0-9-]*">' | head -1 | grep -o '[0-9]\{4\}-[0-9-]*')
if [ "$sale" = "$HOY" ]; then
  echo "$(ahora) el número de hoy ($HOY) ya está en la web"
  exit 0
fi
echo "$(ahora) en la web, el número del ${sale:-?}; falta el de hoy ($HOY): se lanza el vigilante"
[ "$MODO" = --probar ] && { echo "$(ahora) (prueba: no se lanza)"; exit 0; }
cod=$(curl -s -o /dev/null -w '%{http_code}' --max-time 30 -X POST \
  -H "Authorization: Bearer $TOKEN" -H "Accept: application/vnd.github+json" \
  "$API/dispatches" -d '{"ref":"main","inputs":{"simular":"false"}}')
if [ "$cod" = 204 ]; then
  echo "$(ahora) vigilante lanzado"
else
  avisar "Hoy ($HOY) no hay número en la web a las $(date +%H:%M) y GitHub no acepta lanzar el vigilante (HTTP $cod). Queda a mano: Actions › Vigilante del número de hoy › Run workflow, sin marcar «Simular»."
  exit 1
fi
