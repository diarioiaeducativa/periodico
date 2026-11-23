#!/usr/bin/env bash
# SPDX-License-Identifier: AGPL-3.0-or-later
# El reloj del diario dentro de su contenedor del NAS. Cada cinco minutos en punto (:00, :05…) mira qué toca:
#
#   desde la 1:00   preparar el número con las conversaciones de ayer (scripts/noche.sh),
#                   dos intentos como mucho
#   plan B          si los dos intentos fallan, o a las 6:30 si aún no está, para la redacción y
#                   saca el número con una pieza de reserva (scripts/reserva.py, ADR 0021), y avisa
#   desde las 5:00  montar la vista previa del número y mandar a Juanjo el enlace para revisarlo
#                   antes de que salga (ADR 0025); si aún no está, decírselo y mandarlo al estar
#   desde las 6:50  publicarlo (scripts/publicar-nas.sh); si se prepara tarde, en cuanto esté;
#                   si falla, otra vez cada 10 minutos hasta las 9:00 (ADR 0021)
#   desde las 8:00  si faltan piezas de reserva, escribir una (scripts/reserva.sh)
#   desde las 7:05  publicarlo en Instagram (scripts/instagram.py publicar), un solo intento (ADR 0015)
#   a las 12:00     renovar el permiso de Instagram si tiene más de 7 días y comprobar que vale
#   el domingo, desde las 9:00, publicar en Instagram «La semana en vídeo» (ADR 0016 y 0027), un solo intento
#   cada 2 minutos copiar los comentarios de giscus al sitio, para leerlos sin pulsar nada (scripts/copiar-comentarios.sh,
#                  ADR 0030), en un bucle aparte
#   cuando llega   el pódcast y el vídeo de la semana del boletín (multimedia/*.json), con el número del día ya
#                  publicado, volver a publicar solo la web (scripts/publicar-web.sh, ADR 0034)
#
# Lo que falla no se le avisa directamente a Juanjo: pasa por el reparador (scripts/reparador.py, ADR 0087), que
# lanza un agente que lo arregla y avisa después; si no puede, llega el aviso de siempre. `avisar` queda para lo
# que solo informa (la vista previa, «ya está publicado»).
#
# Todo lo que decide se apunta en estado/, así que reiniciar el contenedor no repite nada.
set -u
cd /proyecto

avisar() { avisar-juanjo --de "Diario de IA Educativa" "$1" >/dev/null 2>&1 || true; }
# incidencia [--sin-aviso] [--bloqueo] "qué ha fallado": al reparador; si el reparador no responde, el aviso de siempre
incidencia() { python3 scripts/reparador.py incidencia "$@" >/dev/null 2>&1 || avisar "${!#}"; }
minutos() { echo $(( 10#$(date +%H) * 60 + 10#$(date +%M) )); }

# La copia de los comentarios (ADR 0030), aparte: no espera a la vuelta de cinco minutos ni la retrasa
( while true; do scripts/copiar-comentarios.sh; sleep 120; done ) &

while true; do
  F=$(date -d yesterday +%F)
  E=estado/$F
  m=$(minutos)
  # Mientras el reparador arregla lo que impidió preparar el número, la noche no se repite (ADR 0087). Una marca
  # de más de una hora es de un reparador que murió: no cuenta.
  find estado/reparador/bloqueo -mmin +60 -delete 2>/dev/null
  if [ "$m" -ge 60 ] && [ ! -e "$E.listo" ] && [ ! -e "$E.sin-numero" ] && [ ! -e "$E.en-marcha" ] \
     && [ ! -e estado/reparador/bloqueo ]; then
    intentos=$(cat "$E.intentos" 2>/dev/null || echo 0)
    if [ "$intentos" -lt 2 ]; then
      echo $((intentos + 1)) > "$E.intentos"
      touch "$E.en-marcha"
      # En un grupo de procesos propio (setsid), para poder pararlo entero con sus agentes; en
      # en-marcha queda su número
      # Si acaba mal y sin número, al reparador, antes de quitar la marca: el segundo intento espera a que acabe
      ( setsid timeout 5h scripts/noche.sh "$F" & echo $! > "$E.en-marcha"; wait $!; c=$?
        if [ "$c" != 0 ] && [ ! -e "$E.listo" ] && [ ! -e "$E.sin-numero" ] && [ ! -e "$E.avisado" ]; then   # si la paró el plan B, avisa él
          incidencia --bloqueo --fecha "$F" "La redacción no ha podido preparar el número de hoy: scripts/noche.sh ha acabado con el código $c. Final del registro registro/$F.log: $(tail -12 "registro/$F.log" 2>/dev/null | cut -c1-260 | tr '\n' '|')"
        fi
        rm -f "$E.en-marcha" ) &
    fi
  fi
  # Plan B (ADR 0021): no puede haber ningún día sin número. Si los dos intentos han fallado, o a
  # las 6:30 si aún no está, se para la redacción y sale lo que haya o una pieza de reserva.
  intentos=$(cat "$E.intentos" 2>/dev/null || echo 0)
  if [ "$m" -ge 60 ] && [ ! -e "$E.listo" ] && [ ! -e "$E.sin-numero" ] && [ ! -e "$E.avisado" ] \
     && { [ "$m" -ge 390 ] || { [ "$intentos" -ge 2 ] && [ ! -e "$E.en-marcha" ] && [ ! -e estado/reparador/bloqueo ]; }; }; then
    touch "$E.avisado"
    if [ -e "$E.en-marcha" ]; then
      pg=$(cat "$E.en-marcha")
      [ -n "$pg" ] && { kill -TERM -- "-$pg" 2>/dev/null; sleep 10; kill -KILL -- "-$pg" 2>/dev/null; }
      rm -f "$E.en-marcha"
    fi
    python3 scripts/reserva.py usar "$F" fallo >> "registro/$F.log" 2>&1
    case $? in
      0) touch "$E.listo"
         incidencia "La redacción no ha podido preparar el número de hoy ($intentos intentos): sale con el número de reserva, y las noticias de ayer salen mañana. Registro: /volume1/docker/diario-ia-educativa/repo/registro/$F.log" ;;
      4) touch "$E.listo"
         incidencia "La redacción se ha atascado después del repaso ($intentos intentos): el número sale con lo que estaba hecho. Registro: /volume1/docker/diario-ia-educativa/repo/registro/$F.log" ;;
      *) incidencia "Hoy no hay número: la redacción ha fallado ($intentos intentos) y no queda ningún artículo de reserva. Registro: /volume1/docker/diario-ia-educativa/repo/registro/$F.log" ;;
    esac
  fi
  # La vista previa (ADR 0025): desde las 5:00 y hasta que se publica, el número tal como saldrá,
  # en la red de casa (servicio vista-previa de compose.yml). Si a las 5:00 aún no está, se dice una vez.
  if [ "$m" -ge 300 ] && [ "$m" -lt 410 ] && [ ! -e "$E.publicado" ] && [ ! -e "$E.vista-previa" ]; then
    if [ -e "$E.listo" ]; then
      touch "$E.vista-previa"
      if python3 generar.py >> "registro/$F.log" 2>&1; then
        python3 -m pagefind --site sitio >> "registro/$F.log" 2>&1
        # El domingo, también el texto del dominical que sale a las 9:00 en las redes (ADR 0027)
        dom=""
        [ -f "dominical/$F.json" ] && dom=" · Redes del dominical, a las 9:00: $(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["corto"])' "dominical/$F.json" 2>/dev/null)"
        # Y qué reportaje eligió el juez entre el nuevo y los de reserva (ADR 0028)
        [ -f "reportajes-borrador/$F-eleccion.json" ] && dom="$dom · Reportaje: $(python3 -c 'import json,sys; d=json.load(open(sys.argv[1])); n=len(d.get("puntuaciones") or {}); print(("uno de los de reserva" if d.get("elegido") not in ("nuevo", "", None) else "el nuevo") + (f", entre {n}" if n > 2 else "") + ", porque " + d.get("motivo", "").rstrip(".") + ".")' "reportajes-borrador/$F-eleccion.json" 2>/dev/null)"
        avisar "El número de hoy ya se puede revisar, tal como saldrá a las 6:50 (desde la red de casa): ${VISTA_PREVIA:-http://192.168.1.113:8770/} · en catalán: ${VISTA_PREVIA:-http://192.168.1.113:8770/}ca/ · Si hay que cambiar algo, dímelo antes desde el portátil.$dom"
        # Y la maqueta (ADR 0041): la portada de cada idioma y la página del número a nueve anchuras; si queda un
        # hueco, otro aviso con la captura, a tiempo de arreglarlo antes de las 6:50
        python3 scripts/revisar-maqueta.py "$F" >> "registro/$F.log" 2>&1 || true
        # Los huecos ya le han llegado con su captura: al reparador van sin aviso, por si tienen arreglo
        if [ -s "registro/$F-maqueta.json" ] && [ "$(tr -d ' \n' < "registro/$F-maqueta.json")" != "[]" ]; then
          incidencia --sin-aviso --fecha "$F" "La revisión de maqueta ha encontrado huecos en el número de hoy (registro/$F-maqueta.json): $(cut -c1-700 "registro/$F-maqueta.json" | tr '\n' ' ')"
        fi
      else
        incidencia "No se ha podido montar la vista previa del número de hoy; sale igual a las 6:50. Registro: /volume1/docker/diario-ia-educativa/repo/registro/$F.log"
      fi
    elif [ ! -e "$E.vista-previa-espera" ] && [ ! -e "$E.sin-numero" ]; then
      touch "$E.vista-previa-espera"
      avisar "El número de hoy aún no está listo para revisar: la redacción sigue trabajando. Te mando el enlace en cuanto esté; si a las 6:30 no ha acabado, sale con lo que haya o con el número de reserva."
    fi
  fi
  # Publicar: a las 6:50 y, si falla, cada 10 minutos hasta las 9:00 (ADR 0021)
  if [ "$m" -ge 410 ] && [ -e "$E.listo" ] && [ ! -e "$E.publicado" ] && [ ! -e "$E.publicando" ] \
     && [ "$m" -ge $(( $(cat "$E.publicar-fallo" 2>/dev/null || echo -100) + 10 )) ]; then
    touch "$E.publicando"
    if scripts/publicar-nas.sh "$F"; then
      [ -e "$E.publicar-fallo" ] && avisar "Ya está: el número de hoy se ha publicado, con retraso."
    elif [ "$m" -ge 540 ]; then
      incidencia "No se ha podido publicar el número de hoy: lo he intentado desde las 6:50 hasta las 9:00. Queda a mano. Registro: /volume1/docker/diario-ia-educativa/repo/registro/$F.log"
      touch "$E.publicado"
    else
      [ -e "$E.publicar-fallo" ] || incidencia "No se ha podido publicar el número de hoy a su hora: lo reintento cada 10 minutos hasta las 9:00. Registro: /volume1/docker/diario-ia-educativa/repo/registro/$F.log"
      echo "$m" > "$E.publicar-fallo"
    fi
    rm -f "$E.publicando"
  fi
  # La reserva (ADR 0021): con el número ya publicado, una pieza más si faltan. Una vez al día.
  R=estado/reserva-$(date +%F)
  if [ "$m" -ge 480 ] && [ -e "$E.publicado" ] && [ ! -e "$R" ]; then
    touch "$R"
    ( scripts/reserva.sh >/dev/null 2>&1
      [ "$(python3 scripts/reserva.py cuantas)" -gt 0 ] || incidencia "No queda ningún artículo de reserva del diario y hoy no se ha podido escribir otro. Registro: /volume1/docker/diario-ia-educativa/repo/registro/reserva-$(date +%F).log" ) &
  fi
  # Instagram (ADR 0015): solo si el número salió y hay permiso guardado. Un intento: si falla, a mano.
  if [ "$m" -ge 425 ] && [ -e "$E.publicado" ] && [ -d "instagram/$F" ] && [ -e "$HOME/.config/diario-instagram.json" ] \
     && [ ! -e "$E.instagram" ] && [ ! -e "$E.instagram-intento" ]; then
    touch "$E.instagram-intento"
    if ! python3 scripts/instagram.py publicar "$F" >> "registro/$F.log" 2>&1; then
      incidencia "No se ha podido publicar el número de hoy en Instagram. Registro: /volume1/docker/diario-ia-educativa/repo/registro/$F.log"
    fi
  fi
  # El informe del día para Juanjo (ADR 0069): en cuanto ha salido todo (entre semana, hacia las 7:10; el domingo,
  # después del dominical), una vez. Si algo se atasca, sale igual a las 9:05 (el domingo, a las 11:00) diciendo qué falta.
  limite=545; [ "$(date +%u)" = 7 ] && limite=660
  if [ "$m" -ge 425 ] && [ ! -e "$E.informe" ] && { python3 scripts/informe-dia.py "$F" --listo || [ "$m" -ge "$limite" ]; }; then
    touch "$E.informe"
    python3 scripts/informe-dia.py "$F" --enviar >> "registro/$F.log" 2>&1
  fi
  # El reel de la semana (ADR 0016 y 0027): el domingo a las 9:00, con el dominical en las demás redes
  if [ "$(date +%u)" = 7 ] && [ "$m" -ge 540 ] && [ -e "instagram/reel-$F/reel.mp4" ] && [ -e "$HOME/.config/diario-instagram.json" ] \
     && [ ! -e "$E.instagram-reel" ] && [ ! -e "$E.instagram-reel-intento" ]; then
    touch "$E.instagram-reel-intento"
    if ! python3 scripts/instagram.py reel "$F" >> "registro/$F.log" 2>&1; then
      incidencia "No se ha podido publicar en Instagram el reel de la semana. Registro: /volume1/docker/diario-ia-educativa/repo/registro/$F.log"
    fi
  fi
  H=estado/instagram-permiso-$(date +%F)
  if [ "$m" -ge 720 ] && [ -e "$HOME/.config/diario-instagram.json" ] && [ ! -e "$H" ]; then
    touch "$H"
    if ! { python3 scripts/instagram.py renovar && python3 scripts/instagram.py comprobar; } >> "registro/instagram-permiso.log" 2>&1; then
      incidencia "El permiso de Instagram del diario falla al renovarlo o comprobarlo; mañana no se publicará el carrusel si no se arregla. Registro: /volume1/docker/diario-ia-educativa/repo/registro/instagram-permiso.log"
    fi
  fi
  # El pódcast y el vídeo de la semana (ADR 0034): cuando el boletín deja o cambia un multimedia/*.json, se
  # publica otra vez solo la web. Nunca mientras se prepara o se publica el número: con el de hoy ya fuera.
  if [ -e "$E.publicado" ] && [ ! -e "$E.publicando" ] && [ ! -e estado/multimedia.publicando ] \
     && ls multimedia/*.json >/dev/null 2>&1 \
     && { [ ! -e estado/multimedia.publicado ] || [ -n "$(find multimedia -name '*.json' -newer estado/multimedia.publicado)" ]; } \
     && [ "$(date +%s)" -ge $(( $(cat estado/multimedia.fallo 2>/dev/null || echo 0) + 1800 )) ]; then
    touch estado/multimedia.publicando
    marca=$(mktemp -p estado)   # la hora de antes de empezar: lo que llegue mientras tanto se publica en la siguiente vuelta
    if scripts/publicar-web.sh; then
      mv "$marca" estado/multimedia.publicado
      rm -f estado/multimedia.fallo
    else
      rm -f "$marca"
      [ -e estado/multimedia.fallo ] || incidencia "No se ha podido publicar en la web el pódcast y el vídeo de la semana; lo reintento cada media hora. Registro: /volume1/docker/diario-ia-educativa/repo/registro/multimedia.log"
      date +%s > estado/multimedia.fallo
    fi
    rm -f estado/multimedia.publicando
  fi
  # Hasta el siguiente múltiplo de cinco minutos (las 6:50 en punto, no hasta cinco minutos después): con un
  # «sleep 300» fijo, la vuelta caía donde la dejaba el arranque del contenedor y la publicación de las 6:50
  # empezaba entre las 6:51 y las 6:55 (Juanjo, 23-11-2026). Los husos de Madrid son de horas enteras, así que
  # los múltiplos en UTC lo son también en hora local.
  sleep $(( 300 - $(date +%s) % 300 ))
done
