#!/usr/bin/env bash
# SPDX-License-Identifier: AGPL-3.0-or-later
# Los artículos de la Biblioteca digital de ChatGPT-IA-edu (ADR 0006): uno por cada documento
# que entró en ella el día FECHA. Lo lanza noche.sh después de la viñeta; también a mano, para
# documentos anteriores, que salen con el número de FECHA:
#
#   scripts/biblioteca.sh AAAA-MM-DD [id del mensaje ...]
#   BIBLIOTECA_MODO=fondo scripts/biblioteca.sh 2099-01-NN     una pieza de reserva (lo hace reserva.sh)
#
# Cuatro agentes, uno detrás de otro:
#  12. documentalista (Sonnet) → lee cada documento en su fuente oficial: biblioteca-borrador/FECHA.json
#  13. revisor (Sonnet, no ha escrito nada) → biblioteca/FECHA.json
#  14. ilustrador (Sonnet) → un dibujo por artículo, que pasa la revisión de dibujos (ADR 0005)
#  15. traductor (Sonnet, uno por idioma) → biblioteca-XX/FECHA.json (ADR 0026)
# Un documento que el diario ya contó como noticia no lleva artículo: va a `ya_contado` y la pieza
# de entonces pasa a la sección Biblioteca (lo hace generar.py).
# Nunca impide el número. Sale con 0 si hay artículos y con 2 si no.
set -uo pipefail

RAIZ="$(cd "$(dirname "$(readlink -f "$0")")/.." && pwd)"
cd "$RAIZ"
FECHA="$1"; shift
DATOS="${DATOS_BOT:-/bot-datos}"
SONNET="${MODELO_SONNET:-claude-sonnet-5-5}"
mkdir -p registro biblioteca biblioteca-borrador biblioteca-entrada
REG="registro/$FECHA.log"

log() { printf '%s  %s\n' "$(date '+%F %T')" "$*" | tee -a "$REG"; }

agente() {   # el mismo de noche.sh: sin terminal y sin leer fuera de la redacción (ADR 0002)
  local modelo=$1 paso=$2 minutos=$3 salida
  log "empieza $paso ($modelo)"
  salida=$(sed -e "s/{FECHA}/$FECHA/g" "encargos/pasos/$paso.md" \
    | timeout "$((minutos * 60))" claude -p --model "$modelo" \
        --permission-mode acceptEdits --mcp-config scripts/buscar-mcp.json --allowedTools WebFetch WebSearch mcp__diario \
        --disallowedTools "Bash" "Read(//home/**)" "Read(//proc/**)" "Read(//sitio/**)" "Read(//etc/**)" \
        --output-format text 2>>"$REG")
  local codigo=$?
  printf '%s\n' "$salida" >> "$REG"
  log "acaba $paso (código $codigo)"
  return $codigo
}

json_ok() { python3 -c 'import json,sys; json.load(open(sys.argv[1]))' "$1" 2>/dev/null; }
piezas() { python3 -c 'import json,sys; print(" ".join(p["id"] for p in json.load(open(sys.argv[1])).get("piezas", [])))' "$1" 2>/dev/null; }
contados() { python3 -c 'import json,sys; print(" ".join(str((y.get("mensaje") or {}).get("id")) for y in json.load(open(sys.argv[1])).get("ya_contado", [])))' "$1" 2>/dev/null; }
. scripts/dibujos.sh   # revisar_dibujos (ADR 0005)
. scripts/traducir.sh   # traducir y traducidos (ADR 0026)

# BIBLIOTECA_MODO=fondo: una pieza de reserva del fondo de la biblioteca (ADR 0021), con clave provisional
if [ "${BIBLIOTECA_MODO:-}" = fondo ]; then set -- fondo; fi
python3 scripts/biblioteca.py "$DATOS" biblioteca-entrada "$FECHA" "$@" >> "$REG" 2>&1
case $? in
  0) ;;
  3) exit 2 ;;   # ningún documento nuevo: lo normal casi todos los días
  *) log "AVISO: no se pudo leer la Biblioteca digital"; exit 2 ;;
esac
log "=== biblioteca: $(tail -1 "$REG" | sed 's/^biblioteca: //')"
# A mano, con documentos concretos, se añaden a los artículos que ya tenga ese día (al final se juntan)
if [ $# -gt 0 ] && [ "$1" != fondo ] && [ -e "biblioteca/$FECHA.json" ]; then
  mv -f "biblioteca/$FECHA.json" "biblioteca-borrador/$FECHA-anterior.json"
  for c in $TRADUCCIONES; do
    [ -e "biblioteca-$c/$FECHA.json" ] && mv -f "biblioteca-$c/$FECHA.json" "biblioteca-borrador/$FECHA-anterior-$c.json"
  done
fi
juntar() {   # los artículos anteriores del día, delante; los nuevos, detrás (si repiten documento, mandan los nuevos)
  local c
  for c in "" $(for x in $TRADUCCIONES; do printf ' -%s' "$x"; done); do
    [ -e "biblioteca-borrador/$FECHA-anterior$c.json" ] || continue
    python3 - "biblioteca-borrador/$FECHA-anterior$c.json" "biblioteca$c/$FECHA.json" <<'PY'
import json, pathlib, sys
viejo = json.loads(pathlib.Path(sys.argv[1]).read_text())
nuevo_f = pathlib.Path(sys.argv[2])
nuevo = json.loads(nuevo_f.read_text()) if nuevo_f.exists() else {"fecha": viejo.get("fecha"), "piezas": []}
ids = {(p.get("mensaje") or {}).get("id") for p in nuevo.get("piezas", [])}
nuevo["piezas"] = [p for p in viejo.get("piezas", []) if (p.get("mensaje") or {}).get("id") not in ids] + nuevo.get("piezas", [])
nuevo["descartado"] = viejo.get("descartado", []) + nuevo.get("descartado", [])
ya = {(y.get("mensaje") or {}).get("id") for y in nuevo.get("ya_contado", [])} | ids
nuevo["ya_contado"] = [y for y in viejo.get("ya_contado", []) if (y.get("mensaje") or {}).get("id") not in ya] + nuevo.get("ya_contado", [])
nuevo_f.write_text(json.dumps(nuevo, ensure_ascii=False, indent=1))
PY
    rm -f "biblioteca-borrador/$FECHA-anterior$c.json"
  done
}
trap juntar EXIT
rm -f "biblioteca-borrador/$FECHA.json" "biblioteca/$FECHA.json" $(traducidos biblioteca)

for intento in 1 2; do
  agente "$SONNET" 12-biblioteca-articulos 40
  json_ok "biblioteca-borrador/$FECHA.json" && break
  log "el borrador de la biblioteca no está o no es JSON válido (intento $intento)"
done
[ -n "$(piezas "biblioteca-borrador/$FECHA.json")$(contados "biblioteca-borrador/$FECHA.json")" ] || { log "biblioteca: sin artículos"; exit 2; }
for intento in 1 2; do
  agente "$SONNET" 13-biblioteca-repaso 40
  json_ok "biblioteca/$FECHA.json" && break
  log "la biblioteca repasada no está o no es JSON válida (intento $intento)"
done
ids=$(piezas "biblioteca/$FECHA.json")
ya=$(contados "biblioteca/$FECHA.json")
[ -n "$ya" ] && log "biblioteca: ya contados en el diario, sin artículo nuevo: $ya"
if [ -z "$ids" ]; then
  # Sin artículos, el archivo se queda solo si guarda documentos ya contados (los lee generar.py)
  [ -n "$ya" ] || { log "biblioteca: el revisor no da ningún artículo por bueno"; rm -f "biblioteca/$FECHA.json"; }
  exit 2
fi

agente "$SONNET" 14-biblioteca-ilustraciones 30
json_ok "biblioteca/$FECHA.json" || { log "ERROR: el ilustrador estropeó biblioteca/$FECHA.json"; exit 2; }
# shellcheck disable=SC2086
revisar_dibujos $ids
traducir 15-biblioteca-traduccion biblioteca 40
log "biblioteca lista: $ids"
