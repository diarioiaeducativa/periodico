# SPDX-License-Identifier: AGPL-3.0-or-later
# Las traducciones de la redacción (ADR 0026), para cargar con «. scripts/traducir.sh» desde noche.sh,
# reportaje.sh, biblioteca.sh, repositorio.sh y dibujar.sh, que ponen agente(), log(), FECHA, SONNET y REG.
#
#   traducir PASO TIPO MINUTOS
#
# Antes de nada, scripts/forma.py deja el original con la forma debida (el cuerpo, lista de párrafos): si el
# original está mal formado, fallan a la vez todas las traducciones. Después lanza el encargo
# encargos/pasos/PASO.md una vez por idioma (scripts/idiomas.py pone los datos de cada uno), de dos en dos
# para no pasar de tres agentes a la vez con el que vaya en paralelo, y comprueba lo traducido sin IA
# (scripts/idiomas.py comprobar TIPO).
#
# Una traducción que no vale, o que el traductor no ha llegado a escribir, se repite una vez, diciéndole al
# traductor qué falló. Si la segunda tampoco vale entera, se conserva lo que vale: salen en castellano solo
# las piezas que fallan, no el número (idiomas.py comprobar --conservar). Lo que al final queda en castellano
# se apunta en registro/FECHA-traduccion.txt, y noche.sh avisa. El 17-11-2026 una sola pieza mal formada en
# el original dejó sin traducir el número entero en las cuatro lenguas, sin reintento (ADR 0026).
TRADUCCIONES="${TRADUCCIONES:-$(python3 scripts/idiomas.py lista)}"

_traducir_uno() {
  local paso=$1 tipo=$2 minutos=$3 c=$4 tmp m="" intento conservar=""
  tmp="_$paso-$c"
  for intento in 1 2; do
    python3 scripts/idiomas.py encargo "$paso" "$c" > "encargos/pasos/$tmp.md" || { log "sin encargo de $paso para $c"; return; }
    if [ "$intento" = 2 ]; then
      conservar=--conservar
      printf '\n\nEs el segundo intento. El primero no valió: %s. Vuelve a hacer la traducción entera a partir del original, con su misma estructura: las mismas piezas en el mismo orden y, en cada una, los mismos párrafos, los mismos enlaces y los mismos breves.\n' \
        "$(printf '%s' "$m" | tr '\n' ' ')" >> "encargos/pasos/$tmp.md"
    fi
    agente "$SONNET" "$tmp" "$minutos"
    rm -f "encargos/pasos/$tmp.md"
    m=$( { python3 scripts/idiomas.py comprobar "$tipo" "$FECHA" "$c" $conservar; python3 scripts/idiomas.py falta "$tipo" "$FECHA" "$c"; } 2>&1 )
    if [ -z "$m" ]; then
      [ "$intento" = 2 ] && log "traducción ($tipo, $c): bien al segundo intento"
      return
    fi
    log "$m"
    [ "$intento" = 1 ] && log "traducción ($tipo, $c): no vale o no está; se repite una vez"
  done
  mkdir -p registro && printf '%s\n' "$m" >> "registro/$FECHA-traduccion.txt"
}

traducir() {
  local paso=$1 tipo=$2 minutos=$3 c n=0 orig="" m
  case $tipo in
    edicion) orig="ediciones/$FECHA.json" ;;
    biblioteca|repositorio|hace-un-ano) orig="$tipo/$FECHA.json" ;;
  esac
  if [ -n "$orig" ]; then   # la forma del original, antes de traducirlo (scripts/forma.py)
    m=$(python3 scripts/forma.py "$orig" 2>&1)
    [ -n "$m" ] && log "$m"
  fi
  for c in $TRADUCCIONES; do
    _traducir_uno "$paso" "$tipo" "$minutos" "$c" &
    n=$((n + 1))
    [ $((n % 2)) = 0 ] && wait
  done
  wait
}

# traducidos CARPETA: los archivos traducidos del día en esa carpeta (CARPETA-XX/FECHA.json), para borrarlos
# junto con el original. Sin comodines: biblioteca-entrada/ o repositorio-borrador/ no son traducciones.
traducidos() {
  local c
  for c in $TRADUCCIONES; do printf '%s-%s/%s.json\n' "$1" "$c" "$FECHA"; done
}
