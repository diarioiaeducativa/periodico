#!/usr/bin/env bash
# SPDX-License-Identifier: AGPL-3.0-or-later
# Prepara lo que falte de la reserva (ADR 0021 y 0028). Lo lanza reloj.sh por la mañana, con el número
# ya publicado; también a mano:
#
#   scripts/reserva.sh
#
# Primero retira lo que ha caducado: las piezas, a los 60 días sin usarse; el reportaje, a las 4
# semanas (scripts/reserva.py y scripts/reserva_reportaje.py). Después escribe lo que falte, una cosa
# cada vez:
# - una pieza: un artículo del fondo del Repositorio de VCE con repositorio.sh (documentalista,
#   revisor y traductores) o del fondo de la Biblioteca digital con biblioteca.sh (documentalista,
#   revisor, ilustrador y traductores), alternándolos, con una clave provisional, guardado en reserva/;
# - el reportaje de reserva: con reportaje.sh y RESERVA=1 (jefe de reportajes, reportero,
#   verificador, ilustrador y traductores), sobre un tema que no caduque, guardado en reserva/reportajes/.
# Y lo sube a GitHub para que también pueda usarlo el vigilante de fuera de casa (.github/workflows/vigilante.yml).
set -uo pipefail
RAIZ="$(cd "$(dirname "$(readlink -f "$0")")/.." && pwd)"
cd "$RAIZ"
mkdir -p registro
REG="registro/reserva-$(date +%F).log"
log() { printf '%s  %s\n' "$(date '+%F %T')" "$*" | tee -a "$REG"; }

git pull -q --rebase >> "$REG" 2>&1 || log "AVISO: no se pudo traer lo último de GitHub; sigo con lo que hay"
python3 scripts/reserva.py caducar >> "$REG" 2>&1
python3 scripts/reserva_reportaje.py caducar >> "$REG" 2>&1
codigo=0

faltan=$(python3 scripts/reserva.py faltan)
if [ "$faltan" -gt 0 ]; then
  CLAVE=$(python3 scripts/reserva.py clave)
  # Del repositorio o de la biblioteca, la que tenga menos en la reserva (se alternan)
  FUENTE=$(python3 scripts/reserva.py siguiente)
  log "reserva: faltan $faltan piezas; se escribe una del fondo de $FUENTE con la clave $CLAVE"
  if [ "$FUENTE" = biblioteca ]; then
    BIBLIOTECA_MODO=fondo bash scripts/biblioteca.sh "$CLAVE" >> "$REG" 2>&1
  else
    REPOSITORIO_MODO=fondo bash scripts/repositorio.sh "$CLAVE" >> "$REG" 2>&1
  fi
  if ! python3 scripts/reserva.py guardar "$CLAVE" "$FUENTE" >> "$REG" 2>&1; then
    cat "registro/$CLAVE.log" >> "$REG" 2>/dev/null; rm -f "registro/$CLAVE.log"
    if [ "$FUENTE" = biblioteca ]; then
      # La biblioteca no ha dado pieza (ningún candidato vigente o legible): ese día, una del repositorio
      CLAVE=$(python3 scripts/reserva.py clave)
      log "reserva: la biblioteca no ha dado pieza; se escribe una del fondo del repositorio con la clave $CLAVE"
      REPOSITORIO_MODO=fondo bash scripts/repositorio.sh "$CLAVE" >> "$REG" 2>&1
      python3 scripts/reserva.py guardar "$CLAVE" repositorio >> "$REG" 2>&1 || codigo=1
    else
      codigo=1
    fi
  fi
  cat "registro/$CLAVE.log" >> "$REG" 2>/dev/null; rm -f "registro/$CLAVE.log"
else
  log "reserva: piezas completas"
fi

if [ "$(python3 scripts/reserva_reportaje.py faltan)" -gt 0 ]; then
  CLAVE=$(python3 scripts/reserva_reportaje.py clave)
  log "reserva: falta el reportaje de reserva; se escribe con la clave $CLAVE"
  RESERVA=1 bash scripts/reportaje.sh "$CLAVE" >> "$REG" 2>&1
  python3 scripts/reserva_reportaje.py guardar "$CLAVE" >> "$REG" 2>&1 || codigo=1
  cat "registro/$CLAVE.log" >> "$REG" 2>/dev/null; rm -f "registro/$CLAVE.log"
else
  log "reserva: reportaje de reserva listo"
fi

git add -A reserva
if ! git diff --cached --quiet; then
  git commit -qm "Reserva: $(date +%F)" && git pull -q --rebase &&
  git notes --ref=ia add -f -m "Modelo: Claude Sonnet 5.5 (claude-sonnet-5-5) y Claude Opus 5.5 (claude-opus-5-5) · Claude Code, reserva en el NAS" HEAD &&
  git push -q && git push -q origin refs/notes/ia || log "AVISO: no se pudo subir la reserva a GitHub"
fi
log "reserva: $(python3 scripts/reserva.py cuantas) piezas y $(python3 scripts/reserva_reportaje.py cuantos) reportaje listos"
exit $codigo
