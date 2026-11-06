# SPDX-License-Identifier: AGPL-3.0-or-later
# La revisión de los dibujos (ADR 0005). Lo cargan noche.sh y reportaje.sh, que ponen log,
# agente, REG, FECHA y SONNET.
#
#   revisar_dibujos [id ...]    los dibujos del día en castellano (o solo esos): programa,
#                               revisor visual y, si hace falta, una vuelta al ilustrador; lo que
#                               sigue mal sale sin dibujo y se avisa a Juanjo
#   revisar_dibujos_ca          los de la edición catalana, solo con el programa: si uno falla,
#                               la página catalana usa el castellano, ya revisado

_ronda_dibujos() {   # deja revision/FECHA/rehacer.json con lo que no pasa; vacío si todo pasa
  python3 generar.py >> "$REG" 2>&1 || { log "AVISO: el generador falla: los dibujos no se revisan"; return 1; }
  python3 scripts/revisar-dibujos.py "$FECHA" es "$@" >> "$REG" 2>&1
  case $? in
    0|4) ;;
    *) log "AVISO: no se pudieron revisar los dibujos (navegador): salen sin revisión"; return 1 ;;
  esac
  rm -f "revision/$FECHA/visual.json"
  python3 -c 'import json,sys; sys.exit(0 if json.load(open(sys.argv[1]))["dibujos"] else 1)' "revision/$FECHA/es.json" || return 0
  agente "$SONNET" 2b-revision-dibujos 15
  python3 - "$FECHA" <<'PY'
import json, pathlib, sys
d = pathlib.Path("revision") / sys.argv[1]
prog = json.loads((d / "es.json").read_text())["dibujos"]
try:
    vis = {x["id"]: x for x in json.loads((d / "visual.json").read_text())["dibujos"]}
except Exception:
    vis = {}
rehacer = []
for x in prog:
    motivos = list(x.get("problemas") or [])
    v = vis.get(x["id"])
    if v and v.get("veredicto") == "rehacer" and v.get("motivo"):
        motivos.append(v["motivo"])
    if motivos:
        rehacer.append({"id": x["id"], "titular": x["titular"], "svg": x["svg"], "capturas": x.get("capturas", []), "motivos": motivos})
(d / "rehacer.json").write_text(json.dumps({"dibujos": rehacer}, ensure_ascii=False, indent=1))
print(" ".join(r["id"] for r in rehacer))
PY
}

revisar_dibujos() {
  local malos retirados="" id
  malos=$(_ronda_dibujos "$@" | tail -1) || return 0
  [ -z "$malos" ] && { log "dibujos revisados: todos bien"; return 0; }
  log "dibujos que vuelven al ilustrador: $malos"
  agente "$SONNET" 2c-ilustraciones-rehacer 25
  # shellcheck disable=SC2086
  malos=$(_ronda_dibujos $malos | tail -1) || return 0
  [ -z "$malos" ] && { log "dibujos rehechos: todos bien"; return 0; }
  mkdir -p "revision/$FECHA/retirados"
  for id in $malos; do
    mv -f "ilustraciones/$FECHA-$id.svg" "revision/$FECHA/retirados/es-$FECHA-$id.svg" 2>/dev/null
    for f in ilustraciones-*/"$FECHA-$id.svg"; do   # sus traducciones, también (ADR 0026)
      [ -e "$f" ] && mv -f "$f" "revision/$FECHA/retirados/${f%%/*}-$FECHA-$id.svg"
    done
    retirados="$retirados $id"
  done
  log "sin dibujo, porque sigue mal tras rehacerlo:$retirados"
  avisar-juanjo --de "Diario de IA Educativa" "Sale sin dibujo, porque el revisor lo rechazó dos veces:$retirados. Motivos en /volume1/docker/diario-ia-educativa/repo/revision/$FECHA/rehacer.json" >/dev/null 2>&1 || true
  python3 generar.py >> "$REG" 2>&1
}

revisar_dibujos_traducidos() {   # cada idioma, solo con el programa: el dibujo que falle sale en castellano
  local id c
  python3 generar.py >> "$REG" 2>&1 || return 0
  for c in ${TRADUCCIONES:-ca}; do
    python3 scripts/revisar-dibujos.py "$FECHA" "$c" >> "$REG" 2>&1
    [ $? = 4 ] || continue
    for id in $(python3 -c 'import json,sys; print(" ".join(x["id"] for x in json.load(open(sys.argv[1]))["dibujos"] if x.get("problemas")))' "revision/$FECHA/$c.json"); do
      mkdir -p "revision/$FECHA/retirados"
      mv -f "ilustraciones-$c/$FECHA-$id.svg" "revision/$FECHA/retirados/$c-$FECHA-$id.svg"
      log "el dibujo en $c de $id falla la revisión: esa página usa el castellano"
    done
  done
  python3 generar.py >> "$REG" 2>&1
}
