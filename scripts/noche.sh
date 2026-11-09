#!/usr/bin/env bash
# SPDX-License-Identifier: AGPL-3.0-or-later
# La redacción nocturna: prepara el número con las conversaciones del día FECHA, que sale a
# las 7:00 del día siguiente. Lo lanza reloj.sh a la 1:00; también se puede lanzar a mano:
#
#   scripts/noche.sh [AAAA-MM-DD]        (por defecto, ayer)
#
# Ocho agentes, en este orden (los que no dependen entre sí, a la vez):
#   1. redactor (Sonnet) → ediciones-borrador/FECHA.json; revisor (Sonnet, otro agente que no ha
#      escrito nada) → ediciones/FECHA.json
#   2. ilustrador (Sonnet)  ‖  guionista (Opus, cinco guiones); después, el revisor de dibujos
#      (un programa que los mira en la página y Sonnet), con una vuelta al ilustrador (ADR 0005)
#   3. juez de humor (Opus) → vinetas/FECHA.json
#   4. traductor (Sonnet, una vez por idioma: catalán, gallego, euskera e inglés, ADR 0026)  ‖  avisos
#      (Sonnet) → avisos/PUBLICA.json
# El sábado, después, el guionista del reel de la semana (Sonnet) y el vídeo (scripts/reel-semana.sh, ADR 0016).
# Si FECHA es domingo, entre el 3 y el 4 va el comentario de la semana (scripts/comentario-semana.sh, tres
# agentes más, ADR 0038), para la página semana/AAAA-WW/.
# Si FECHA es sábado, entre el 3 y el 4 va el reportaje del domingo (scripts/reportaje.sh, cinco
# agentes más, ADR 0004): los avisos del domingo ya lo pueden anunciar. Si no sale, el número sale igual.
# Si ese día entró algún documento en la Biblioteca digital de ChatGPT-IA-edu, después va su artículo
# (scripts/biblioteca.sh, documentalista y revisor, ADR 0006); un día sin más que eso también es número.
# Después, los recursos del Repositorio de Vibe Coding Educativo (scripts/repositorio.sh, ADR 0008):
# los días con menos de cuatro piezas, los de la cola; el viernes, la semana; con la cola vacía, uno
# del fondo. Así un día sin apenas mensajes también tiene número.
# Los agentes solo pueden escribir en esta carpeta y no tienen terminal: los mensajes de los
# grupos son texto de terceros y no deben poder llevarlos a otra parte (ADR 0002).
# Deja estado/FECHA.listo si hay número (o estado/FECHA.sin-numero) y sale con 0; si falla
# algo imprescindible, sale con 1 y reloj.sh avisa a Juanjo.
set -uo pipefail

RAIZ="$(cd "$(dirname "$(readlink -f "$0")")/.." && pwd)"
cd "$RAIZ"
FECHA="${1:-$(date -d yesterday +%F)}"
PUBLICA=$(date -d "$FECHA + 1 day" +%F)
DATOS="${DATOS_BOT:-/bot-datos}"
SONNET="${MODELO_SONNET:-claude-sonnet-5-5}"
OPUS="${MODELO_OPUS:-claude-opus-5-5}"
mkdir -p registro estado ediciones-borrador vinetas/candidatas avisos
REG="registro/$FECHA.log"

log() { printf '%s  %s\n' "$(date '+%F %T')" "$*" | tee -a "$REG"; }

# agente <modelo> <paso> <minutos>: lanza un agente con el encargo encargos/pasos/<paso>.md.
agente() {
  local modelo=$1 paso=$2 minutos=$3 salida
  log "empieza $paso ($modelo)"
  salida=$(sed -e "s/{FECHA}/$FECHA/g" -e "s/{PUBLICA}/$PUBLICA/g" "encargos/pasos/$paso.md" \
    | timeout "$((minutos * 60))" claude -p --model "$modelo" \
        --permission-mode acceptEdits --allowedTools WebFetch WebSearch \
        --disallowedTools "Bash" "Read(//home/**)" "Read(//proc/**)" "Read(//sitio/**)" "Read(//etc/**)" \
        --output-format text 2>>"$REG")
  local codigo=$?
  printf '%s\n' "$salida" >> "$REG"
  log "acaba $paso (código $codigo)"
  return $codigo
}

# Las viñetas en que habla primero el de la derecha van con los globos en escalera (vineta.py). Si con
# esos textos no caben, salen lado a lado, como antes: los textos no se acortan. Solo se anota.
comprobar_vineta() {
  [ -e "$1" ] || return 0
  local m
  m=$(python3 vineta.py --comprobar "$1") || log "comprobación de la viñeta en $1: $(echo "$m" | tr '\n' ' ')"
}

json_ok() { python3 -c 'import json,sys; json.load(open(sys.argv[1]))' "$1" 2>/dev/null; }

# Un día sin piezas de la redacción: si entró un documento en la Biblioteca digital (ADR 0006) o
# toca un recurso del repositorio (ADR 0008), eso es el número del día. Si tampoco sale nada de
# ahí, una pieza de reserva (ADR 0021): no puede haber ningún día sin número.
solo_anexos() {
  local hay=0
  python3 scripts/publicado.py >> "$REG" 2>&1
  bash scripts/biblioteca.sh "$FECHA" && hay=1
  bash scripts/repositorio.sh "$FECHA" && hay=1
  if [ $hay = 0 ] && python3 scripts/reserva.py usar "$FECHA" relleno >> "$REG" 2>&1; then
    log "sin piezas propias: sale la pieza de reserva"
    hay=1
  fi
  if [ $hay = 1 ]; then
    agente "$SONNET" 6-avisos 20
    revisar_dibujos_ca
    [ "$(date -d "$FECHA" +%u)" = 6 ] && bash scripts/reel-semana.sh "$FECHA"
    python3 generar.py >> "$REG" 2>&1 || { log "ERROR: el generador falla con la biblioteca o el repositorio"; exit 1; }
    touch "estado/$FECHA.listo"
    log "listo: número del $PUBLICA, sin piezas de la redacción"
    exit 0
  fi
  log "ERROR: ni piezas, ni repositorio, ni reserva: hoy no hay número"
  avisar-juanjo --de "Diario de IA Educativa" "Hoy no hay número: no había nada que contar, no ha salido nada del repositorio y no queda ninguna pieza de reserva. Registro: /volume1/docker/diario-ia-educativa/repo/registro/$FECHA.log" >> "$REG" 2>&1
  touch "estado/$FECHA.sin-numero"
  exit 0
}
. scripts/dibujos.sh   # revisar_dibujos y revisar_dibujos_traducidos (ADR 0005)
. scripts/traducir.sh   # traducir (ADR 0026)

log "=== número del $PUBLICA, con las conversaciones del $FECHA"
# Lo que se haya cambiado desde el portátil (encargos, generador) llega solo antes de empezar.
antes=$(git rev-parse HEAD)
git pull -q --ff-only >> "$REG" 2>&1 || log "AVISO: no se pudo traer lo último de GitHub; sigo con lo que hay"
# Bash ya ha leído este script: si el pull lo ha cambiado, seguiría el viejo con los encargos
# nuevos. Se relanza una vez con la versión recién traída.
if [ "$(git rev-parse HEAD)" != "$antes" ] && [ -z "${NOCHE_RELANZADO:-}" ] \
   && ! git diff --quiet "$antes" HEAD -- scripts/noche.sh; then
  log "noche.sh ha cambiado con el pull: se relanza con la versión nueva"
  NOCHE_RELANZADO=1 exec bash "$RAIZ/scripts/noche.sh" "$FECHA"
fi
# Si ese número ya está publicado (su edición está en GitHub), no se rehace: pasa al restaurar
# el contenedor en otra máquina, donde estado/ empieza vacío.
if git ls-files --error-unmatch "ediciones/$FECHA.json" >/dev/null 2>&1 && [ "${REHACER:-0}" != 1 ]; then
  log "el número con las conversaciones del $FECHA ya está publicado: no se rehace (REHACER=1 para forzarlo)"
  touch "estado/$FECHA.listo" "estado/$FECHA.publicado"
  exit 0
fi
rm -f "estado/$FECHA.listo" "estado/$FECHA.sin-numero"

# Si el número de ayer salió con la reserva porque la redacción falló, sus conversaciones se cuentan hoy (ADR 0021)
ANT=$(date -d "$FECHA - 1 day" +%F)
RECUPERA=$(python3 -c 'import json,sys; print(1 if json.load(open(sys.argv[1])).get("reserva") in ("fallo", True) else 0)' "ediciones/$ANT.json" 2>/dev/null || echo 0)
[ "$RECUPERA" = 1 ] && log "el número de ayer salió con la reserva: hoy se cuentan también sus conversaciones"
RECUPERA=$RECUPERA python3 scripts/preparar.py "$DATOS" dias "$FECHA" >> "$REG" 2>&1
case $? in
  0) ;;
  3) log "ningún mensaje en ningún grupo"
     # Sin conversaciones, el número puede ser solo del repositorio (ADR 0008)
     printf '{"fecha": "%s", "hay_edicion": false, "motivo": "ningún mensaje en ningún grupo", "piezas": [], "breves": []}\n' "$FECHA" > "ediciones/$FECHA.json"
     solo_anexos ;;
  *) log "ERROR: no se pudieron leer los mensajes de $DATOS"; exit 1 ;;
esac
python3 scripts/publicado.py >> "$REG" 2>&1

# 1. Redacción y repaso, por dos agentes distintos: el revisor no ha escrito nada (ADR 0001).
# Es lo único imprescindible: cada paso se reintenta una vez, y sin repaso no hay número.
rm -f "ediciones-borrador/$FECHA.json" "ediciones/$FECHA.json"
for intento in 1 2; do
  agente "$SONNET" 1-redaccion 40
  json_ok "ediciones-borrador/$FECHA.json" && break
  log "el borrador no está o no es JSON válido (intento $intento)"
done
json_ok "ediciones-borrador/$FECHA.json" || { log "ERROR: no hay borrador"; exit 1; }
if python3 -c 'import json,sys; d=json.load(open(sys.argv[1])); sys.exit(0 if d.get("hay_edicion") and d.get("piezas") else 1)' "ediciones-borrador/$FECHA.json"; then
  for intento in 1 2; do
    agente "$SONNET" 1-repaso 40
    json_ok "ediciones/$FECHA.json" && break
    log "la edición repasada no está o no es JSON válido (intento $intento)"
  done
  json_ok "ediciones/$FECHA.json" || { log "ERROR: el revisor no dejó la edición: sin repaso no se publica"; exit 1; }
else
  cp "ediciones-borrador/$FECHA.json" "ediciones/$FECHA.json"   # sin número: no hay nada que repasar
fi
if ! python3 -c 'import json,sys; d=json.load(open(sys.argv[1])); sys.exit(0 if d.get("hay_edicion") and d.get("piezas") else 1)' "ediciones/$FECHA.json"; then
  log "la redacción decide que hoy no hay número: $(python3 -c 'import json,sys; print(json.load(open(sys.argv[1])).get("motivo",""))' "ediciones/$FECHA.json")"
  solo_anexos
fi

# Lo publicado, con las piezas de hoy: la Biblioteca, el Repositorio y el reportaje las enlazan (encargos/enlaces.md)
python3 scripts/publicado.py >> "$REG" 2>&1

# 2. Ilustraciones y guiones, a la vez. Antes, lo que salió en las viñetas de los tres números
# anteriores, para que el guionista y el juez no repitan escenario ni caras (ADR 0024).
mkdir -p vinetas/recientes
python3 vineta.py --recientes "$FECHA" > "vinetas/recientes/$FECHA.md" 2>>"$REG"
agente "$SONNET" 2-ilustraciones 40 & p1=$!
agente "$OPUS" 3-guiones 40 & p2=$!
wait $p1 $p2
# 2 bis. Los dibujos, vistos en la página en claro y oscuro: programa, revisor y una vuelta más.
revisar_dibujos

# 3. El juez. Sin guiones o sin juez, el número sale sin viñeta.
if json_ok "vinetas/candidatas/$FECHA.json"; then
  agente "$OPUS" 4-juez 30
  json_ok "vinetas/$FECHA.json" || { log "el juez no dejó una viñeta válida: sale sin ella"; rm -f "vinetas/$FECHA.json"; }
  comprobar_vineta "vinetas/$FECHA.json"
  [ -e "vinetas/$FECHA.json" ] && { m=$(python3 vineta.py --repite "$FECHA" "vinetas/$FECHA.json") || log "variedad de la viñeta: $m"; }
else
  log "no hay guiones válidos: sale sin viñeta"
fi

# 3 bis. El reportaje del domingo, si la semana acaba hoy (sábado). Nunca impide el número.
if [ "$(date -d "$FECHA" +%u)" = 6 ] || [ "${REPORTAJE:-0}" = 1 ]; then
  if [ -e "estado/$FECHA.reportaje-reserva" ]; then   # decisión de la redacción: sale el de reserva (ADR 0028)
    log "reportaje: se ha pedido publicar el de reserva; no se escribe uno nuevo"
    log "sin reportaje: se ha pedido publicar el de reserva"
    codigo=2
  else
    bash scripts/reportaje.sh "$FECHA"
    codigo=$?
  fi
  if [ "$codigo" != 0 ]; then   # el reportaje sale siempre (ADR 0028): si no ha podido ser, el de reserva
    [ "$codigo" = 2 ] || { log "el reportaje falló de forma inesperada"; rm -f reportajes/"$FECHA".json $(traducidos reportajes); }
    porque=$(grep 'sin reportaje: ' "$REG" | tail -1 | sed 's/.*sin reportaje: //')
    if python3 scripts/reserva_reportaje.py usar "$FECHA" >> "$REG" 2>&1; then
      log "el domingo sale con el reportaje de reserva"
      # Su infografía, mirada con el programa en su página (no se pudo al escribirla): si falla, sale sin ella
      rid=$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["id"])' "reportajes/$FECHA.json")
      python3 generar.py >> "$REG" 2>&1 && python3 scripts/revisar-dibujos.py "$FECHA" es "$rid" >> "$REG" 2>&1
      if [ $? = 4 ]; then
        mkdir -p "revision/$FECHA/retirados"
        for f in ilustraciones/"$FECHA-$rid".svg $(for c in $TRADUCCIONES; do printf 'ilustraciones-%s/%s-%s.svg ' "$c" "$FECHA" "$rid"; done); do
          [ -e "$f" ] && mv -f "$f" "revision/$FECHA/retirados/${f%%/*}-$FECHA-$rid.svg"
        done
        log "la infografía del reportaje de reserva falla la revisión: sale sin ella"
      fi
      if [ -e "estado/$FECHA.reportaje-reserva" ]; then
        avisar-juanjo --de "Diario de IA Educativa" "Como pediste, el domingo sale con el reportaje de reserva, y mañana se escribe otro de reserva. Registro: /volume1/docker/diario-ia-educativa/repo/registro/$FECHA.log" >/dev/null 2>&1 || true
      else
        avisar-juanjo --de "Diario de IA Educativa" "El reportaje de esta semana no ha podido salir (${porque:-fallo inesperado}): el domingo sale con el reportaje de reserva, y mañana se escribe otro de reserva. Registro: /volume1/docker/diario-ia-educativa/repo/registro/$FECHA.log" >/dev/null 2>&1 || true
      fi
    else
      avisar-juanjo --de "Diario de IA Educativa" "El número del domingo sale sin reportaje: no ha podido salir (${porque:-fallo inesperado}) y no queda ningún reportaje de reserva que valga. Registro: /volume1/docker/diario-ia-educativa/repo/registro/$FECHA.log" >/dev/null 2>&1 || true
    fi
  fi
fi

# 3 ter. La Biblioteca digital: un artículo por cada documento que entró hoy (ADR 0006). Nunca impide el número.
bash scripts/biblioteca.sh "$FECHA"
[ $? -le 2 ] || { log "la biblioteca falló de forma inesperada: sale sin ella"; rm -f biblioteca/"$FECHA".json $(traducidos biblioteca); }

# 3 quater. El repositorio de Vibe Coding Educativo, si el número se queda corto o es viernes (ADR 0008). Nunca impide el número.
bash scripts/repositorio.sh "$FECHA"
[ $? -le 2 ] || { log "el repositorio falló de forma inesperada: sale sin él"; rm -f repositorio/"$FECHA".json $(traducidos repositorio); }

# 3 quinquies. El domingo cierra la semana de los mensajes: el comentario de la semana para su página (ADR 0038).
# Nunca impide el número.
if [ "$(date -d "$FECHA" +%u)" = 7 ] || [ "${COMENTARIO:-0}" = 1 ]; then
  bash scripts/comentario-semana.sh "$(date -d "$FECHA" +%G-%V)"
  [ $? -le 2 ] || log "el comentario de la semana falló de forma inesperada: la semana sale sin él"
fi

# 4. Traducción y avisos, a la vez.
traducir 5-traduccion edicion 50 & p1=$!
agente "$SONNET" 6-avisos 20 & p2=$!
wait $p1 $p2
for c in $TRADUCCIONES; do
  comprobar_vineta "vinetas-$c/$FECHA.json"
done
if ! python3 -c '
import json, sys
d = json.load(open(sys.argv[1]))["avisos"]
assert set(d) == {"chatgpt", "vce", "edumedia"}
for a in d.values():   # saludo y de dos a tres puntos (ADR 0010)
    assert a["saludo"].strip() and 2 <= len(a["puntos"]) <= 3 and all(p.strip() for p in a["puntos"])
' "avisos/$PUBLICA.json" 2>/dev/null; then
  log "avisos inválidos: se reintenta una vez"
  agente "$SONNET" 6-avisos 20
fi

# 4 bis. Los dibujos traducidos, solo con el programa: el que falle, en castellano.
revisar_dibujos_traducidos
# Lo que se quitó de alguna traducción esta noche, en un solo aviso (ADR 0026): esa edición sale con el castellano
if [ -s "registro/$FECHA-traduccion.txt" ]; then
  avisar-juanjo --de "Diario de IA Educativa" "Alguna traducción del número de hoy no ha pasado la comprobación y esa parte sale en castellano: $(sort -u "registro/$FECHA-traduccion.txt" | tr '\n' ' ')Registro: /volume1/docker/diario-ia-educativa/repo/registro/$FECHA.log" >/dev/null 2>&1 || true
fi

# 4 ter. El sábado, «La semana en vídeo» para el número del domingo (ADR 0016). Nunca impide el número.
reel_semana() {
  if [ "$(date -d "$FECHA" +%u)" = 6 ] || [ "${REEL:-}" = 1 ]; then
    bash scripts/reel-semana.sh "$FECHA" || log "sin reel de la semana"
  fi
}
reel_semana
# Lo que no llegó a Internet Archive otra noche se vuelve a probar (ADR 0037); sin pendientes, no hace nada.
python3 scripts/subir-videos.py --minutos 15 >> "$REG" 2>&1 || log "AVISO: queda algún vídeo sin subir a Internet Archive"

# 5. Que el sitio se genere con todo esto antes de darlo por listo.
if ! python3 generar.py >> "$REG" 2>&1; then
  log "ERROR: el generador falla con la edición nueva"
  exit 1
fi
touch "estado/$FECHA.listo"
log "listo: número del $PUBLICA preparado"
