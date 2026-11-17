# 86. La viñeta la escribe y la elige Fable

Fecha: 2026-11-17 · Estado: aceptado

## Contexto

La viñeta diaria la escribían y la elegían dos agentes con Opus 5.5 (ADR 0001): el guionista, que
propone cinco guiones, y el juez, que elige uno y lo retoca. La del número del 17-11-2026, sobre la
parada de emergencia de una celda robotizada, no se entendía al leerla en la vista previa, aunque
el juez le había puesto un 8 en claridad. Se rehízo a mano antes de publicar, con Fable 5.2, sobre
otro artículo del número (el catálogo de lecturas del Repositorio), y esa fue la que salió.

## Decisión

El guionista (`3-guiones`), el juez (`4-juez`) y el humorista de la viñeta de reserva
(`30-vineta-reserva`) usan Fable 5.2, fijado por su nombre exacto (`claude-fable-5-2`), en la variable
`FABLE` de `scripts/noche.sh` y `scripts/vineta-reserva.sh` (`MODELO_FABLE` la cambia). Los encargos
no cambian. El resto de los agentes sigue como estaba: Sonnet 5.5 para escribir y revisar cada día,
y Opus 5.5 para elegir el reportaje y para los textos largos.

## Alternativas descartadas

- **Cambiar solo el juez**: el chiste que no se entendía ya venía así del guionista; el juez elige
  entre lo que hay.
- **Pasar a Fable todos los agentes que usan Opus**: no se ha visto ningún problema en ellos, y Fable
  gasta más de la suscripción.

## Consecuencias

- Dos agentes cada noche, y uno más cuando se repone la viñeta de reserva, pasan a un modelo que
  consume más de la misma suscripción; sin coste nuevo.
- La nota del modelo de los commits del NAS nombra también a Fable, y «Cómo se hace» dice quién hace
  la viñeta; sus traducciones se rehacen solas (ADR 0085).
- Las viñetas de reserva ya escritas con Opus salen cuando toque; las nuevas, con Fable.

## Evidencia

- `registro/2026-11-16.log` del NAS: `3-guiones` y `4-juez` con `claude-opus-5-5`; el juez puntuó la
  elegida con claridad 8.
- La viñeta sustituida, en `vinetas/sustituidas/2026-11-16.json`; la nueva, en `vinetas/2026-11-16.json`.
- En el contenedor del NAS (Claude Code 2.1.316), `claude -p --model claude-fable-5-2` responde con
  ese modelo (`modelUsage`), aunque avisa de que no reconoce el nombre.

## Riesgos y limitaciones

- No se ha hecho una prueba a ciegas entre Opus y Fable como la del 01-11-2026 entre Sonnet y Opus:
  que Fable haga viñetas más claras es una hipótesis, apoyada en una sola viñeta.
- La versión de Claude Code del contenedor no reconoce el nombre del modelo, aunque lo usa. Si un día
  lo rechazara, `noche.sh` sale sin guiones válidos y la viñeta la pone la reserva (ADR 0068).

## Validación

Pendiente: la viñeta del número del 18-11-2026, la primera con el cambio; en su registro tienen que
figurar `3-guiones` y `4-juez` con `claude-fable-5-2`.
