# 23. Siempre hay viñeta: el juez elige el mejor guion aunque no llegue al 7

Fecha: 2026-11-06 · Estado: aceptado

## Contexto

El juez de humor (`encargos/pasos/4-juez.md`) puntúa los cinco guiones del guionista y solo
elegía uno si su gracia llegaba al 7; si no, el número salía sin viñeta. No había pasado en los
9 primeros números (28-10 a 05-11-2026), pero podía pasar. Juanjo, al preguntar si podía haber
un día sin viñeta, aprobó cambiarlo el 06-11-2026 («sí, cámbialo»). Es la misma regla que el
plan B del número (ADR 0021): lo que la gente espera sale siempre, y si nada alcanza el nivel,
se usa la mejor versión.

## Decisión

- El juez **elige siempre el mejor** de los guiones que respetan las prohibiciones de
  `encargos/vineta.md`. Si su gracia no llega a 7, lo afina más a fondo y lo dice en `motivo`.
- `elegida` solo es `null` si los cinco incumplen las prohibiciones (por ejemplo, se inventan
  datos de la noticia): esas reglas protegen la exactitud y no ceden.
- El número sigue saliendo sin viñeta si fallan el guionista o el juez (`scripts/noche.sh`,
  paso 3); no se reintenta, porque el número no puede esperar.
- «La redacción» ya no dice que el juez puede no elegir ninguno, y la presentación de la página
  de la viñeta no explica cómo se elige el guion (quitado el mismo día a petición de Juanjo).

## Validación

Pendiente de ver en los números siguientes: `motivo` de `vinetas/<fecha>.json` dice cuándo la
elegida no llegó al 7.
