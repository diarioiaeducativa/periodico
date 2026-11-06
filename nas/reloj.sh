#!/usr/bin/env bash
# SPDX-License-Identifier: AGPL-3.0-or-later
# El reloj del diario dentro de su contenedor del NAS. Cada cinco minutos mira qué toca:
#
#   desde la 1:00   preparar el número con las conversaciones de ayer (scripts/noche.sh),
#                   dos intentos como mucho
#   plan B          si los dos intentos fallan, o a las 6:30 si aún no está, para la redacción y
#                   saca el número con una pieza de reserva (scripts/reserva.py, ADR 0021), y avisa
#   desde las 5:00  montar la vista previa del número y mandar a Juanjo el enlace para revisarlo
#                   antes de que salga (ADR 0025); si aún no está, decírselo y mandarlo al estar
#   desde las 6:55  publicarlo (scripts/publicar-nas.sh); si se prepara tarde, en cuanto esté;
#                   si falla, otra vez cada 10 minutos hasta las 9:00 (ADR 0021)
#   desde las 8:00  si faltan piezas de reserva, escribir una (scripts/reserva.sh)
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
      # En un grupo de procesos propio (setsid), para poder pararlo entero con sus agentes; en
      # en-marcha queda su número
      ( setsid timeout 5h scripts/noche.sh "$F" & echo $! > "$E.en-marcha"; wait $!; rm -f "$E.en-marcha" ) &
    fi
  fi
  # Plan B (ADR 0021): no puede haber ningún día sin número. Si los dos intentos han fallado, o a
  # las 6:30 si aún no está, se para la redacción y sale lo que haya o una pieza de reserva.
  intentos=$(cat "$E.intentos" 2>/dev/null || echo 0)
  if [ "$m" -ge 60 ] && [ ! -e "$E.listo" ] && [ ! -e "$E.sin-numero" ] && [ ! -e "$E.avisado" ] \
     && { [ "$m" -ge 390 ] || { [ "$intentos" -ge 2 ] && [ ! -e "$E.en-marcha" ]; }; }; then
    touch "$E.avisado"
    if [ -e "$E.en-marcha" ]; then
      pg=$(cat "$E.en-marcha")
      [ -n "$pg" ] && { kill -TERM -- "-$pg" 2>/dev/null; sleep 10; kill -KILL -- "-$pg" 2>/dev/null; }
      rm -f "$E.en-marcha"
    fi
    python3 scripts/reserva.py usar "$F" fallo >> "registro/$F.log" 2>&1
    case $? in
      0) touch "$E.listo"
         avisar "La redacción no ha podido preparar el número de hoy ($intentos intentos): sale con una pieza de reserva, y las noticias de ayer salen mañana. Registro: /volume1/docker/diario-ia-educativa/repo/registro/$F.log" ;;
      4) touch "$E.listo"
         avisar "La redacción se ha atascado después del repaso ($intentos intentos): el número sale con lo que estaba hecho. Registro: /volume1/docker/diario-ia-educativa/repo/registro/$F.log" ;;
      *) avisar "Hoy no hay número: la redacción ha fallado ($intentos intentos) y no queda ninguna pieza de reserva. Registro: /volume1/docker/diario-ia-educativa/repo/registro/$F.log" ;;
    esac
  fi
  # La vista previa (ADR 0025): desde las 5:00 y hasta que se publica, el número tal como saldrá,
  # en la red de casa (servicio vista-previa de compose.yml). Si a las 5:00 aún no está, se dice una vez.
  if [ "$m" -ge 300 ] && [ "$m" -lt 415 ] && [ ! -e "$E.publicado" ] && [ ! -e "$E.vista-previa" ]; then
    if [ -e "$E.listo" ]; then
      touch "$E.vista-previa"
      if python3 generar.py >> "registro/$F.log" 2>&1; then
        python3 -m pagefind --site sitio >> "registro/$F.log" 2>&1
        avisar "El número de hoy ya se puede revisar, tal como saldrá a las 6:55 (desde la red de casa): ${VISTA_PREVIA:-http://192.168.1.113:8770/} · en catalán: ${VISTA_PREVIA:-http://192.168.1.113:8770/}ca/ · Si hay que cambiar algo, dímelo antes desde el portátil."
      else
        avisar "No se ha podido montar la vista previa del número de hoy; sale igual a las 6:55. Registro: /volume1/docker/diario-ia-educativa/repo/registro/$F.log"
      fi
    elif [ ! -e "$E.vista-previa-espera" ] && [ ! -e "$E.sin-numero" ]; then
      touch "$E.vista-previa-espera"
      avisar "El número de hoy aún no está listo para revisar: la redacción sigue trabajando. Te mando el enlace en cuanto esté; si a las 6:30 no ha acabado, sale con lo que haya o con una pieza de reserva."
    fi
  fi
  # Publicar: a las 6:55 y, si falla, cada 10 minutos hasta las 9:00 (ADR 0021)
  if [ "$m" -ge 415 ] && [ -e "$E.listo" ] && [ ! -e "$E.publicado" ] && [ ! -e "$E.publicando" ] \
     && [ "$m" -ge $(( $(cat "$E.publicar-fallo" 2>/dev/null || echo -100) + 10 )) ]; then
    touch "$E.publicando"
    if scripts/publicar-nas.sh "$F"; then
      [ -e "$E.publicar-fallo" ] && avisar "Ya está: el número de hoy se ha publicado, con retraso."
    elif [ "$m" -ge 540 ]; then
      avisar "No se ha podido publicar el número de hoy: lo he intentado desde las 6:55 hasta las 9:00. Queda a mano. Registro: /volume1/docker/diario-ia-educativa/repo/registro/$F.log"
      touch "$E.publicado"
    else
      [ -e "$E.publicar-fallo" ] || avisar "No se ha podido publicar el número de hoy a su hora: lo reintento cada 10 minutos hasta las 9:00. Registro: /volume1/docker/diario-ia-educativa/repo/registro/$F.log"
      echo "$m" > "$E.publicar-fallo"
    fi
    rm -f "$E.publicando"
  fi
  # La reserva (ADR 0021): con el número ya publicado, una pieza más si faltan. Una vez al día.
  R=estado/reserva-$(date +%F)
  if [ "$m" -ge 480 ] && [ -e "$E.publicado" ] && [ ! -e "$R" ]; then
    touch "$R"
    ( scripts/reserva.sh >/dev/null 2>&1
      [ "$(python3 scripts/reserva.py cuantas)" -gt 0 ] || avisar "No queda ninguna pieza de reserva del diario y hoy no se ha podido escribir otra. Registro: /volume1/docker/diario-ia-educativa/repo/registro/reserva-$(date +%F).log" ) &
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
