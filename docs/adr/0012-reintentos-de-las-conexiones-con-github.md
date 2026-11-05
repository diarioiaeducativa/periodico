# 12. Reintentos de las conexiones con GitHub

Fecha: 2026-11-04 · Estado: aceptado

## Contexto

El 04-11-2026, durante una incidencia de GitHub («Incident with Pull Requests, Git Operations
and Issues», githubstatus.com), más o menos la mitad de las conexiones SSH se rechazaban con
«Permission denied (publickey)» aunque la clave fuera la buena. En Temps a Montflorit, que
publica con un solo intento por pasada, la web se quedó de 10:32 a 12:07 sin subir.

El diario está más expuesto: `publicar-nas.sh` se lanza una sola vez, a las 6:55, y necesita
tres conexiones seguidas (traer el sitio, subirlo y subir la redacción). Si falla la de subir el
sitio, no sale el número ni el bot recibe los avisos de las 7:00, y el reloj no lo reintenta:
avisa a Juanjo y queda para hacerlo a mano. Con la mitad de las conexiones rechazadas, solo una
de cada ocho mañanas saldría bien. Juanjo preguntó si había que hacer lo mismo que en Temps a
Montflorit y lo aprobó («hazlo»), con la condición de que no hubiera peligro de bloqueo.

## Decisión

Toda conexión de git con GitHub en el NAS pasa por `scripts/ssh-reintenta.sh`, puesto como
`core.sshCommand` de los dos repositorios (`/proyecto` y `/sitio`), con la clave de cada uno:
si ssh falla (código 255), vuelve a probar cada 3 segundos, hasta 8 veces, con 10 segundos como
mucho para conectar. Así lo cubren a la vez el `git pull` de `noche.sh`, el de `publicar-nas.sh`
y sus `git push`, sin tocar los scripts. El resto del proceso no cambia.

## Alternativas descartadas

- **Un segundo intento automático de toda la publicación unos minutos después**: más cambios en
  el reloj y repetiría pasos que ya habían salido bien (los avisos al bot).
- **`GIT_SSH_COMMAND` en cada script**: los dos repositorios usan claves distintas y habría que
  repetir la de cada uno; `core.sshCommand` ya las tiene.

## Consecuencias

- Una incidencia de GitHub como la del 04-11-2026 ya no deja el número sin publicar.
- El `core.sshCommand` vive en la configuración de cada clon del NAS, no en el repositorio: al
  volver a montar el NAS hay que ponerlo así (paso 4 del README).

## Evidencia

- Temps a Montflorit (`meteo-montflorit/meteo-local`, `eines/ssh-reintenta.sh`, 3.212.1, ADR
  0020): el 04-11-2026, la subida que fallaba en cada pasada entró al primer intento con
  reintentos.
- Prueba del 04-11-2026: 5 conexiones desde el NAS con la clave buena, 2 aceptadas y 3
  rechazadas.

## Riesgos y limitaciones

- **Bloqueo por GitHub**: GitHub no publica un límite de conexiones SSH. Aquí son unas pocas
  conexiones al día (un pull por la noche, un pull y unos push por la mañana), y como mucho 8 por
  cada una solo cuando GitHub falla: muy por debajo de lo que hace cualquier integración continua.
- Sin red, cada conexión tarda como mucho unos dos minutos en rendirse.
- Solo se repite lo que falla en ssh; un rechazo de git en el servidor (por ejemplo, un push no
  fast-forward) se devuelve tal cual, como antes.

## Validación

- `bash -n scripts/ssh-reintenta.sh`.
- En el NAS, `git ls-remote` de los dos repositorios con el `core.sshCommand` nuevo.
