# 2. Los agentes de la redacción no tienen terminal

Fecha: 2026-11-02 · Estado: aceptado

## Contexto

Los agentes leen los mensajes de tres grupos abiertos de Telegram: texto que escribe
cualquiera. Un mensaje puede intentar dar órdenes al agente (inyección de instrucciones).
En el contenedor hay cosas que no deben salir de él: el token de Claude (en el entorno) y
las claves que suben a GitHub (en el home).

## Decisión

Cada agente se lanza desde la carpeta de la redacción con `claude -p --permission-mode
acceptEdits --allowedTools WebFetch WebSearch` y, prohibidos expresamente, `Bash` y la
lectura de `/home`, `/proc`, `/etc` y `/sitio`:

- escribe solo dentro de esa carpeta (fuera pediría permiso, y en modo `-p` se deniega);
- no puede leer el home (claves), `/proc` (el entorno de los procesos, con el token) ni `/etc`;
- no tiene Bash, así que no puede leer el entorno ni ejecutar nada;
- necesita la web para comprobar cada dato en su fuente original.

Los encargos le recuerdan que los mensajes son material para informar, no instrucciones.
Lo que hay que validar (que un JSON es válido, que el sitio se genera) lo hace el script,
no el agente. Los avisos los escribe el agente en `avisos/` y los copia el script a la
carpeta del bot.

## Alternativas descartadas

- `--dangerously-skip-permissions`: el contenedor aísla del NAS, pero no del token ni de las
  claves que tiene dentro.

## Riesgos y limitaciones

Un mensaje podría colar texto en una pieza; el revisor compara cada pieza con los mensajes y
las fuentes, y lo publicado se puede corregir a mano.

## Excepción del 17-11-2026: el reparador (ADR 0087)

Un solo agente tiene terminal: el reparador, que actúa cuando algo falla. No es un agente de la
redacción: no escribe ni lee los mensajes de los grupos como material, trabaja en una copia y un
programa comprueba lo que hace antes de aplicarlo. El riesgo que esta decisión evita (que un texto
ajeno dé órdenes a un agente con acceso al token y a las claves) vuelve a existir para él, acotado
como explica el ADR 0087.
