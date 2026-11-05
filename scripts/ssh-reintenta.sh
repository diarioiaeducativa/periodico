#!/usr/bin/env bash
# SPDX-License-Identifier: AGPL-3.0-or-later
# ssh para git (core.sshCommand de los dos repositorios del NAS) que vuelve a probar si la
# conexión falla. El 04-11-2026, durante una incidencia de GitHub, la mitad de las conexiones
# se rechazaban («Permission denied (publickey)» con la clave buena). El número se publica con
# un solo intento a las 6:55 y necesita tres conexiones seguidas (traer el sitio, subirlo y
# subir la redacción): con un fallo, ni número ni avisos (ADR 0012). ssh devuelve 255 solo si
# falla él (conexión o autenticación), antes de que git envíe nada, así que repetir es seguro;
# cualquier otro código es de git en el servidor y se devuelve tal cual.
# Uso: core.sshCommand = /proyecto/scripts/ssh-reintenta.sh -i ~/.ssh/<clave> -o IdentitiesOnly=yes …
INTENTOS=${SSH_INTENTOS:-8}
for ((i = 1; i <= INTENTOS; i++)); do
  ssh -o ConnectTimeout=10 "$@"
  rc=$?
  [ "$rc" -ne 255 ] && exit "$rc"
  [ "$i" -lt "$INTENTOS" ] && sleep 3
done
exit 255
