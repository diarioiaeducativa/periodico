#!/usr/bin/env bash
# SPDX-License-Identifier: AGPL-3.0-or-later
# El vigilante de fuera de casa (ADR 0021): lo lanza GitHub Actions (.github/workflows/vigilante.yml),
# por su horario y desde el hosting de IONOS (ionos/lanzar-vigilante.sh). Si a partir de las 9:10 de Madrid el número de hoy no está en la web (el NAS está
# caído o no ha podido publicar, y ya ha dejado de reintentar a las 9:00), lo saca con una pieza de
# reserva, lo publica y avisa a Juanjo. Sin IA: la reserva ya está escrita y repasada.
#
#   scripts/vigilante.sh             lo que hace GitHub Actions
#   SIMULAR=1 scripts/vigilante.sh   todo menos subir nada y avisar, aunque no sea la hora
#   SIMULAR=1 FECHA=AAAA-MM-DD …     lo mismo, como si faltara el número de esas conversaciones
#
# Necesita, en GitHub Actions: SITIO_KEY (clave de despliegue con escritura en el repositorio del
# sitio) y TELEGRAM_TOKEN y TELEGRAM_CHAT (el bot «Agentes IA», para avisar a Juanjo).
set -uo pipefail
RAIZ="$(cd "$(dirname "$(readlink -f "$0")")/.." && pwd)"
cd "$RAIZ"
SIMULAR="${SIMULAR:-0}"
WEB="https://diarioiaeducativa.github.io/"

export TZ=Europe/Madrid
HOY=$(date +%F)
F=$(date -d yesterday +%F)
[ "$SIMULAR" = 1 ] && [ -n "${FECHA:-}" ] && F=$FECHA
m=$(( 10#$(date +%H) * 60 + 10#$(date +%M) ))

avisar() {
  echo "AVISO: $1"
  [ "$SIMULAR" = 1 ] && return 0
  [ -n "${TELEGRAM_TOKEN:-}" ] && curl -s -o /dev/null --max-time 30 "https://api.telegram.org/bot$TELEGRAM_TOKEN/sendMessage" \
    --data-urlencode "chat_id=$TELEGRAM_CHAT" --data-urlencode "text=Diario de IA Educativa · vigilante de GitHub: $1"
}

# Desde las 9:10, cuando el NAS ya ha dejado de reintentar, y hasta el final del día: GitHub retrasa
# horas su horario (el 06 y el 07-11-2026 entró a las 15:57 y a las 14:56), y mejor tarde que sin número
if [ "$SIMULAR" != 1 ] && [ "$m" -lt 550 ]; then
  echo "vigilante: son las $(date +%H:%M) en Madrid; solo actúa desde las 9:10"
  exit 0
fi
portada=$(curl -s --max-time 60 "$WEB") || { echo "vigilante: no se puede leer la web; no se hace nada"; exit 1; }
sale=$(printf '%s' "$portada" | grep -o '<time datetime="[0-9-]*">' | head -1 | grep -o '[0-9]\{4\}-[0-9-]*')
if [ "$sale" = "$HOY" ] && [ "$SIMULAR" != 1 ]; then
  echo "vigilante: el número de hoy ($HOY) ya está en la web"
  exit 0
fi
# Ya en el repositorio: el NAS o una pasada anterior lo han publicado (el sitio se sube antes que la
# redacción) y GitHub Pages aún no lo sirve. Pasa cuando se juntan la pasada de IONOS y la de GitHub.
if [ -e "ediciones/$F.json" ] && [ "$SIMULAR" != 1 ]; then
  echo "vigilante: el número de hoy ya está en el repositorio (ediciones/$F.json); la web se está actualizando"
  exit 0
fi
echo "vigilante: en la web, el número del ${sale:-?}; falta el de hoy ($HOY), con las conversaciones del $F"

python3 scripts/reserva.py usar "$F" fallo
case $? in
  0|4) ;;
  *) avisar "Hoy ($HOY) no hay número en la web a las $(date +%H:%M) y no queda ninguna pieza de reserva para sacarlo. Mira si el NAS está encendido."
     exit 1 ;;
esac
python3 scripts/publicado.py
python3 generar.py || { avisar "Hoy ($HOY) no hay número en la web y el generador falla con la reserva: queda a mano."; exit 1; }
python3 -m pagefind --site sitio >/dev/null || echo "vigilante: sin índice nuevo del buscador; queda el anterior"

# El sitio: lo mismo que publicar-nas.sh, con la clave de despliegue del vigilante
if [ -n "${SITIO_KEY:-}" ]; then
  mkdir -p ~/.ssh && printf '%s\n' "$SITIO_KEY" > ~/.ssh/sitio && chmod 600 ~/.ssh/sitio
  ssh-keyscan -t ed25519 github.com >> ~/.ssh/known_hosts 2>/dev/null
  export GIT_SSH_COMMAND="ssh -i $HOME/.ssh/sitio -o IdentitiesOnly=yes"
fi
git clone -q --depth 1 git@github.com:diarioiaeducativa/diarioiaeducativa.github.io.git /tmp/sitio ||
  { avisar "Hoy ($HOY) no hay número en la web y no puedo descargar el repositorio del sitio: queda a mano."; exit 1; }
if [ "$SIMULAR" = 1 ]; then   # se comprueban las credenciales sin subir nada ni avisar
  echo "vigilante (simulación): el sitio está montado con la reserva y la clave del sitio descarga su repositorio; no se sube nada"
  git -C /tmp/sitio push --dry-run -q 2>&1 | tail -1
  [ -n "${TELEGRAM_TOKEN:-}" ] && curl -s --max-time 30 "https://api.telegram.org/bot$TELEGRAM_TOKEN/getMe" | grep -o '"ok":[a-z]*' | sed 's/^/vigilante (simulación): bot de avisos /'
  exit 0
fi
rsync -a --delete --exclude .git --exclude .github --exclude README.md --exclude LICENSE --exclude LICENSE-CODIGO \
  --exclude .nojekyll --exclude fuentes/OFL.txt sitio/ /tmp/sitio/
git config --global user.name "Diario de IA Educativa (vigilante)"
git config --global user.email "diarioiaeducativa@users.noreply.github.com"
git -C /tmp/sitio add -A
git -C /tmp/sitio commit -qm "Número del $HOY, con la pieza de reserva (vigilante, ADR 0021)" &&
  git -C /tmp/sitio push -q ||
  { avisar "Hoy ($HOY) no hay número en la web y no puedo subir el sitio con la reserva: queda a mano."; exit 1; }
unset GIT_SSH_COMMAND

# La redacción: lo que ha cambiado la reserva, para que el NAS no lo rehaga y mañana recupere el día
git add -A ediciones repositorio reserva avisos publicado.txt $(ls -d repositorio-?? reportajes reportajes-?? ilustraciones ilustraciones-?? 2>/dev/null)   # ADR 0026 y 0028
git commit -qm "Número del $HOY, con la pieza de reserva (vigilante, ADR 0021)" && git push -q ||
  echo "vigilante: AVISO: no se pudo subir la redacción"
avisar "A las $(date +%H:%M) el número de hoy ($HOY) no estaba en la web: lo he publicado con una pieza de reserva. Los grupos no reciben aviso, porque el bot está en el NAS. Mira si el NAS está encendido o por qué no publicó."
