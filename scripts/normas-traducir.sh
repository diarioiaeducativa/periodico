#!/usr/bin/env bash
# SPDX-License-Identifier: AGPL-3.0-or-later
# Traduce las normas públicas del diario que han cambiado o no están traducidas (ADR 0085): un agente por documento y
# lengua, con encargos/pasos/37-normas-traduccion.md, y después scripts/normas_traducir.py comprueba cada traducción
# (mismos títulos, puntos, tablas, enlaces y nombres de archivo); la que no vale se quita y esa lengua enlaza al
# castellano. Lo lanza noche.sh cada noche: casi siempre no hay nada que hacer. También a mano:
#
#   scripts/normas-traducir.sh
set -uo pipefail
RAIZ="$(cd "$(dirname "$(readlink -f "$0")")/.." && pwd)"
cd "$RAIZ"
SONNET="${MODELO_SONNET:-claude-sonnet-5-5}"
mkdir -p registro
REG="registro/normas-traduccion.log"
log() { printf '%s  %s\n' "$(date '+%F %T')" "$*" | tee -a "$REG"; }

python3 scripts/normas_traducir.py pendientes > /tmp/normas-pendientes.$$ || exit 1
n=$(grep -c . /tmp/normas-pendientes.$$)
[ "$n" -gt 0 ] || { rm -f /tmp/normas-pendientes.$$; exit 0; }
log "=== normas por traducir: $n"
# Una tanda por lengua, las cuatro a la vez; dentro de cada una, un documento detrás de otro
traducir_lengua() {
while read -r origen destino huella lengua; do
  mkdir -p "$(dirname "$destino")"
  tmp="_37-normas-traduccion-$lengua"
  python3 scripts/idiomas.py encargo 37-normas-traduccion "$lengua" \
    | sed -e "s|{ORIGEN}|$origen|g" -e "s|{DESTINO}|$destino|g" -e "s|{HASH}|$huella|g" \
          -e "s|{TITULO}|$(python3 -c 'import sys, generar; print(generar.IDIOMAS[sys.argv[1]]["titulo"])' "$lengua")|g" > "encargos/pasos/$tmp.md"
  log "empieza $destino"
  sed '' "encargos/pasos/$tmp.md" | timeout 2400 claude -p --model "$SONNET" \
    --permission-mode acceptEdits --allowedTools WebFetch WebSearch \
    --disallowedTools "Bash" "Read(//home/**)" "Read(//proc/**)" "Read(//sitio/**)" "Read(//etc/**)" \
    --output-format text >> "$REG" 2>&1
  rm -f "encargos/pasos/$tmp.md"
  python3 scripts/normas_traducir.py comprobar "$origen" "$destino" "$huella" >> "$REG" 2>&1 \
    && log "$destino: traducido" || log "AVISO: $destino no ha pasado la comprobación: esa lengua enlaza al castellano"
done
}
for c in $(cut -d' ' -f4 /tmp/normas-pendientes.$$ | sort -u); do
  grep " $c\$" /tmp/normas-pendientes.$$ | traducir_lengua &
done
wait
rm -f /tmp/normas-pendientes.$$
