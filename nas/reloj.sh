#!/usr/bin/env bash
# SPDX-License-Identifier: AGPL-3.0-or-later
# El reloj del diario dentro de su contenedor del NAS. Cada cinco minutos mira qué toca:
#
#   desde la 1:00   preparar el número con las conversaciones de ayer (scripts/noche.sh),
#                   dos intentos como mucho
#   a las 6:30      si no está listo, avisar a Juanjo por Telegram
#   desde las 6:55  publicarlo (scripts/publicar-nas.sh); si se prepara tarde, en cuanto esté
#   desde las 7:05  publicarlo en Instagram (scripts/instagram.py publicar), un solo intento (ADR 0015)
#   a las 12:00     renovar el permiso de Instagram si tiene más de 7 días y comprobar que vale
#   el domingo, desde las 12:00, publicar en Instagram «La semana en vídeo» (ADR 0016), un solo intento
#
# Todo lo que decide se apunta en estado/, así que reiniciar el contenedor no repite nada.
set -u
cd /proyecto

avisar() { avisar-juanjo --de "Diario de IA Educativa" "$1" >/dev/null 2>&1 || true; }
minutos() { echo $(( 10#$(date +%H) * 60 + 10#$(date +%M) )); }

while true; do
  F=$(date -d yesterday +%F)
  E=estado/$F
  m=$(minutos)
  if [ "$m" -ge 60 ] && [ ! -e "$E.listo" ] && [ ! -e "$E.sin-numero" ] && [ ! -e "$E.en-marcha" ]; then
    intentos=$(cat "$E.intentos" 2>/dev/null || echo 0)
    if [ "$intentos" -lt 2 ]; then
      echo $((intentos + 1)) > "$E.intentos"
      touch "$E.en-marcha"
      ( timeout 5h scripts/noche.sh "$F"; rm -f "$E.en-marcha" ) &
    fi
  fi
  if [ "$m" -ge 390 ] && [ ! -e "$E.listo" ] && [ ! -e "$E.sin-numero" ] && [ ! -e "$E.avisado" ]; then
    touch "$E.avisado"
    avisar "El número de hoy no está listo a las 6:30 ($(cat "$E.intentos" 2>/dev/null || echo 0) intentos). Registro: /volume1/docker/diario-ia-educativa/repo/registro/$F.log"
  fi
  if [ "$m" -ge 415 ] && [ -e "$E.listo" ] && [ ! -e "$E.publicado" ] && [ ! -e "$E.publicando" ]; then
    touch "$E.publicando"
    if scripts/publicar-nas.sh "$F"; then
      [ -e "$E.avisado" ] && avisar "Ya está: el número de hoy se ha publicado, con retraso."
    else
      avisar "No se ha podido publicar el número de hoy. Registro: /volume1/docker/diario-ia-educativa/repo/registro/$F.log"
      touch "$E.publicado"   # un solo intento automático: el resto, a mano
    fi
    rm -f "$E.publicando"
  fi
  # Instagram (ADR 0015): solo si el número salió y hay permiso guardado. Un intento: si falla, a mano.
  if [ "$m" -ge 425 ] && [ -e "$E.publicado" ] && [ -d "instagram/$F" ] && [ -e "$HOME/.config/diario-instagram.json" ] \
     && [ ! -e "$E.instagram" ] && [ ! -e "$E.instagram-intento" ]; then
    touch "$E.instagram-intento"
    if ! python3 scripts/instagram.py publicar "$F" >> "registro/$F.log" 2>&1; then
      avisar "No se ha podido publicar el número de hoy en Instagram. Registro: /volume1/docker/diario-ia-educativa/repo/registro/$F.log"
    fi
  fi
  # El reel de la semana (ADR 0016): el domingo a mediodía, separado del carrusel de las 7:05
  if [ "$(date +%u)" = 7 ] && [ "$m" -ge 720 ] && [ -e "instagram/reel-$F/reel.mp4" ] && [ -e "$HOME/.config/diario-instagram.json" ] \
     && [ ! -e "$E.instagram-reel" ] && [ ! -e "$E.instagram-reel-intento" ]; then
    touch "$E.instagram-reel-intento"
    if ! python3 scripts/instagram.py reel "$F" >> "registro/$F.log" 2>&1; then
      avisar "No se ha podido publicar en Instagram el reel de la semana. Registro: /volume1/docker/diario-ia-educativa/repo/registro/$F.log"
    fi
  fi
  H=estado/instagram-permiso-$(date +%F)
  if [ "$m" -ge 720 ] && [ -e "$HOME/.config/diario-instagram.json" ] && [ ! -e "$H" ]; then
    touch "$H"
    if ! { python3 scripts/instagram.py renovar && python3 scripts/instagram.py comprobar; } >> "registro/instagram-permiso.log" 2>&1; then
      avisar "El permiso de Instagram del diario falla al renovarlo o comprobarlo; mañana no se publicará el carrusel si no se arregla. Registro: /volume1/docker/diario-ia-educativa/repo/registro/instagram-permiso.log"
    fi
  fi
  sleep 300
done
