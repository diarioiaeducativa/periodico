#!/usr/bin/env bash
# SPDX-License-Identifier: AGPL-3.0-or-later
# El columnista de la columna de opinión (ADR 0092), en el NAS y fuera del contenedor del diario: cada minuto
# (crontab del NAS) mira si scripts/columna.sh ha dejado un «pedido» en columnas-trabajo/<clave>/ y, si lo hay,
# lanza Codex en la caja del agente de noticias (noticias-chatgpt-ia-edu: sistema de archivos de solo lectura,
# sin privilegios, con su cuenta de ChatGPT), sin terminal y con la búsqueda en la web, con el encargo y el
# material de prompt.md y la forma de la respuesta de esquema.json. Deja la respuesta en columna.json, el
# registro en codex.log y el código de salida en «hecho», que es lo que espera columna.sh.
#
#   * * * * * /usr/bin/bash /volume1/docker/diario-ia-educativa/repo/nas/columnista.sh # diario-columnista
set -uo pipefail
REPO="${REPO_DIARIO:-/volume1/docker/diario-ia-educativa/repo}"   # otra copia, para probar
NOTICIAS=/volume1/docker/noticias-chatgpt-ia-edu
exec 9>/tmp/diario-columnista.lock
flock -n 9 || exit 0   # uno cada vez: comparten la cuenta de ChatGPT
for p in "$REPO"/columnas-trabajo/*/pedido; do
  [ -e "$p" ] || continue
  t=$(dirname "$p")
  modelo=$(tr -cd 'a-z0-9.-' < "$p"); rm -f "$p"
  cd "$NOTICIAS" || { echo 1 > "$t/hecho"; continue; }
  timeout 2700 docker compose run --rm -T --no-deps -v "$t":/trabajo codex \
    -a never --disable shell_tool -c 'web_search="live"' \
    exec --ignore-user-config --ephemeral --skip-git-repo-check --sandbox read-only \
    -m "${modelo:-gpt-6.2-astra}" -c 'model_reasoning_effort="high"' \
    --output-schema /trabajo/esquema.json -o /trabajo/columna.json - < "$t/prompt.md" > "$t/codex.log" 2>&1
  echo $? > "$t/hecho"
done
