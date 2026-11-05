#!/usr/bin/env bash
# SPDX-License-Identifier: AGPL-3.0-or-later
# Prepara una pieza de reserva si faltan (ADR 0021). Lo lanza reloj.sh por la mañana, con el número
# ya publicado; también a mano:
#
#   scripts/reserva.sh
#
# Escribe un artículo del fondo del Repositorio de VCE con repositorio.sh (documentalista, revisor y
# traductor) con una clave provisional y lo guarda en reserva/ (scripts/reserva.py), y lo sube a
# GitHub para que también pueda usarlo el vigilante de fuera de casa (.github/workflows/vigilante.yml).
# Una pieza cada vez: si faltan varias, la siguiente sale al día siguiente.
set -uo pipefail
RAIZ="$(cd "$(dirname "$(readlink -f "$0")")/.." && pwd)"
cd "$RAIZ"
mkdir -p registro
REG="registro/reserva-$(date +%F).log"
log() { printf '%s  %s\n' "$(date '+%F %T')" "$*" | tee -a "$REG"; }

faltan=$(python3 scripts/reserva.py faltan)
[ "$faltan" -gt 0 ] || { log "reserva: completa"; exit 0; }
git pull -q --rebase >> "$REG" 2>&1 || log "AVISO: no se pudo traer lo último de GitHub; sigo con lo que hay"
CLAVE=$(python3 scripts/reserva.py clave)
log "reserva: faltan $faltan; se escribe una con la clave $CLAVE"
REPOSITORIO_MODO=fondo bash scripts/repositorio.sh "$CLAVE" >> "$REG" 2>&1
python3 scripts/reserva.py guardar "$CLAVE" >> "$REG" 2>&1
codigo=$?
cat "registro/$CLAVE.log" >> "$REG" 2>/dev/null; rm -f "registro/$CLAVE.log"
git add -A reserva
if ! git diff --cached --quiet; then
  git commit -qm "Reserva: $CLAVE" && git pull -q --rebase &&
  git notes --ref=ia add -f -m "Modelo: Claude Sonnet 5.5 (claude-sonnet-5-5) · Claude Code, reserva en el NAS" HEAD &&
  git push -q && git push -q origin refs/notes/ia || log "AVISO: no se pudo subir la reserva a GitHub"
fi
log "reserva: $(python3 scripts/reserva.py cuantas) listas"
exit $codigo
