# SPDX-License-Identifier: AGPL-3.0-or-later
# Las traducciones de la redacción (ADR 0026), para cargar con «. scripts/traducir.sh» desde noche.sh,
# reportaje.sh, biblioteca.sh, repositorio.sh y dibujar.sh, que ponen agente(), log(), FECHA, SONNET y REG.
#
#   traducir PASO TIPO MINUTOS
#
# Lanza el encargo encargos/pasos/PASO.md una vez por idioma (scripts/idiomas.py pone los datos de cada
# uno), de dos en dos para no pasar de tres agentes a la vez con el que vaya en paralelo, y después
# comprueba lo traducido sin IA (scripts/idiomas.py comprobar TIPO): lo que no vale se quita y esa
# edición sale con el castellano. Lo quitado se apunta en registro/FECHA-traduccion.txt, y noche.sh avisa.
TRADUCCIONES="${TRADUCCIONES:-$(python3 scripts/idiomas.py lista)}"

_traducir_uno() {
  local paso=$1 tipo=$2 minutos=$3 c=$4 tmp m
  tmp="_$paso-$c"
  python3 scripts/idiomas.py encargo "$paso" "$c" > "encargos/pasos/$tmp.md" || { log "sin encargo de $paso para $c"; return; }
  agente "$SONNET" "$tmp" "$minutos"
  rm -f "encargos/pasos/$tmp.md"
  if ! m=$(python3 scripts/idiomas.py comprobar "$tipo" "$FECHA" "$c" 2>&1); then
    log "$m"
    printf '%s\n' "$m" >> "registro/$FECHA-traduccion.txt"
  fi
}

traducir() {
  local paso=$1 tipo=$2 minutos=$3 c n=0
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
