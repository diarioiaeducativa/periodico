#!/usr/bin/env bash
# SPDX-License-Identifier: AGPL-3.0-or-later
# Los recursos del Repositorio de Vibe Coding Educativo, en la sección Vibe coding (ADR 0008).
# Lo lanza noche.sh después de la Biblioteca; también a mano, con recursos concretos, que salen
# con el número de FECHA:
#
#   scripts/repositorio.sh AAAA-MM-DD [url ...]
#
# Un programa (scripts/repositorio.py) decide qué toca: los días flojos, recursos de la cola; el
# viernes, la semana entera para el número del sábado; con la cola vacía, uno del fondo. Abre
# cada recurso y guarda su captura. Después, tres agentes:
#  16. documentalista (Sonnet) → repositorio-borrador/FECHA.json
#  17. revisor (Sonnet, no ha escrito nada) → repositorio/FECHA.json
#  18. traductor (Sonnet, uno por idioma) → repositorio-XX/FECHA.json (ADR 0026)
# Sin ilustrador: la imagen es la captura del propio recurso. Nunca impide el número. Sale con 0
# si hay artículos y con 2 si no.
set -uo pipefail

RAIZ="$(cd "$(dirname "$(readlink -f "$0")")/.." && pwd)"
cd "$RAIZ"
FECHA="$1"; shift
DATOS="${DATOS_BOT:-/bot-datos}"
SONNET="${MODELO_SONNET:-claude-sonnet-5-5}"
mkdir -p registro repositorio repositorio-borrador repositorio-entrada
REG="registro/$FECHA.log"

log() { printf '%s  %s\n' "$(date '+%F %T')" "$*" | tee -a "$REG"; }

agente() {   # el mismo de noche.sh: sin terminal y sin leer fuera de la redacción (ADR 0002)
  local modelo=$1 paso=$2 minutos=$3 salida
  log "empieza $paso ($modelo)"
  salida=$(sed -e "s/{FECHA}/$FECHA/g" "encargos/pasos/$paso.md" \
    | timeout "$((minutos * 60))" claude -p --model "$modelo" \
        --permission-mode acceptEdits --allowedTools WebFetch WebSearch \
        --disallowedTools "Bash" "Read(//home/**)" "Read(//proc/**)" "Read(//sitio/**)" "Read(//etc/**)" \
        --output-format text 2>>"$REG")
  local codigo=$?
  printf '%s\n' "$salida" >> "$REG"
  log "acaba $paso (código $codigo)"
  return $codigo
}

json_ok() { python3 -c 'import json,sys; json.load(open(sys.argv[1]))' "$1" 2>/dev/null; }
. scripts/traducir.sh   # traducir y traducidos (ADR 0026)
piezas() { python3 -c 'import json,sys; print(" ".join(p["id"] for p in json.load(open(sys.argv[1])).get("piezas", [])))' "$1" 2>/dev/null; }

# Lo que el programa descarta (lo que sigue sin abrir el sábado) sale de la cola aunque no haya artículo
descartes() {
  python3 - "repositorio-entrada/$FECHA.json" "repositorio/$FECHA.json" <<'PY'
import json, pathlib, sys
ent = pathlib.Path(sys.argv[1])
d = json.loads(ent.read_text()).get("descartes", []) if ent.exists() else []
if not d:
    sys.exit(0)
f = pathlib.Path(sys.argv[2])
fin = json.loads(f.read_text()) if f.exists() else {"fecha": json.loads(ent.read_text())["fecha"], "piezas": []}
ya = {x.get("url") for x in fin.get("descartado", []) if isinstance(x, dict)}
fin["descartado"] = fin.get("descartado", []) + [x for x in d if x["url"] not in ya]
f.write_text(json.dumps(fin, ensure_ascii=False, indent=1))
PY
}

[ -e "repositorio/$FECHA.json" ] && [ $# -eq 0 ] && { log "repositorio: ya hay artículos del $FECHA; no se rehacen"; exit 0; }
rm -f "repositorio-entrada/$FECHA.json" "repositorio-entrada/$FECHA.md"
python3 scripts/repositorio.py "$DATOS" repositorio-entrada "$FECHA" "$@" >> "$REG" 2>&1
case $? in
  0) ;;
  3) descartes; exit 2 ;;   # no toca nada hoy: lo normal los días con número completo
  *) log "AVISO: no se pudo preparar el repositorio (hoja o navegador)"; exit 2 ;;
esac
log "=== repositorio: $(grep '^repositorio: ' "$REG" | tail -1 | sed 's/^repositorio: //')"
trap descartes EXIT
rm -f "repositorio-borrador/$FECHA.json" "repositorio/$FECHA.json" $(traducidos repositorio)

for intento in 1 2; do
  agente "$SONNET" 16-repositorio-articulos 40
  json_ok "repositorio-borrador/$FECHA.json" && break
  log "el borrador del repositorio no está o no es JSON válido (intento $intento)"
done
if [ -z "$(piezas "repositorio-borrador/$FECHA.json")" ]; then
  log "repositorio: sin artículos"
  # Lo que el documentalista descarta tampoco vuelve: se guarda solo el descarte
  json_ok "repositorio-borrador/$FECHA.json" && python3 -c '
import json, sys
d = json.load(open(sys.argv[1]))
if d.get("descartado"):
    json.dump({"fecha": d.get("fecha"), "piezas": [], "descartado": d["descartado"]}, open(sys.argv[2], "w"), ensure_ascii=False, indent=1)
' "repositorio-borrador/$FECHA.json" "repositorio/$FECHA.json"
  exit 2
fi
for intento in 1 2; do
  agente "$SONNET" 17-repositorio-repaso 40
  json_ok "repositorio/$FECHA.json" && break
  log "el repositorio repasado no está o no es JSON válido (intento $intento)"
done
ids=$(piezas "repositorio/$FECHA.json")
[ -n "$ids" ] || { log "repositorio: el revisor no da ningún artículo por bueno"; exit 2; }
# Lo ya contado en la semana lo pone el programa, no el agente: la pieza del sábado lo lista con el
# enlace a su artículo (ADR 0008)
python3 - "$FECHA" <<'PY'
import json, pathlib, sys
fecha = sys.argv[1]
ent = pathlib.Path(f"repositorio-entrada/{fecha}.json")
ya = json.loads(ent.read_text()).get("ya_contados", []) if ent.exists() else []
if ya:
    f = pathlib.Path(f"repositorio/{fecha}.json")
    d = json.loads(f.read_text())
    for p in d.get("piezas", []):
        if p.get("repositorio") == "semana":
            p["ya_contados"] = ya
    f.write_text(json.dumps(d, ensure_ascii=False, indent=1))
PY
# Las capturas que no se usan no se publican ni se guardan
python3 - "$FECHA" <<'PY'
import json, pathlib, sys
fecha = sys.argv[1]
usadas = {pathlib.Path(x.get("captura") or "").name for p in json.loads(pathlib.Path(f"repositorio/{fecha}.json").read_text()).get("piezas", [])
          for x in p.get("recursos", [])}
for f in pathlib.Path("repositorio/capturas").glob(f"{fecha}-*.jpg"):
    if f.name not in usadas:
        f.unlink()
PY
traducir 18-repositorio-traduccion repositorio 40
log "repositorio listo: $ids"
