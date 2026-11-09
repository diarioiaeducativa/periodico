# 41. La portada, sin huecos: cada bloque de sección, con sus tres piezas más recientes

Fecha: 2026-11-09 · Estado: aceptado

## Contexto

La portada tomaba las piezas de los últimos 7 días con un tope de 10 para toda ella (más 3 de la Biblioteca):
lo del último número arriba y el resto repartido en el bloque de su sección. Con un número de varias piezas,
el tope se agotaba con lo de hoy y ayer, y bloques como Herramientas o Debates salían con una pieza y dos
huecos, aunque la sección tuviera más de días anteriores. Juanjo (09-11-2026): «no he visto nunca un diario
con espacios vacíos».

## Decisión

- **Todo lo del último número arriba**, como hasta ahora, sin tope.
- **Cada bloque de sección, con sus tres piezas más recientes de días anteriores** (`POR_SECCION`),
  retrocediendo lo que haga falta, sin límite de días. Solo queda con menos si la sección no tiene más.
  Vale también para la Biblioteca, que antes tenía su propio tope (`BIBLIOTECA_PORTADA`, ADR 0006).
- **Los breves y el reportaje** siguen siendo de los últimos 7 días (`DIAS_PORTADA`).
- **Regla para lo que venga**: ninguna composición del diario puede dejar huecos con ninguna cantidad de
  piezas; se comprueba con pocas y con muchas, no solo con las de hoy (así se resolvió también «Hace un año»,
  ADR 0040).

## Alternativas descartadas

- **Subir el tope global**: los huecos seguirían, solo que en otros días.
- **Bloques de ancho variable según las piezas**: un bloque de una pieza a todo el ancho rompe la rejilla.

## Consecuencias

- Los bloques pasan de unas 10 piezas a 18 (seis secciones de tres), pero la portada casi no crece: cada fila
  ya ocupaba la altura de su pieza más larga.
- Lo que está en la portada ya no es solo de la última semana: una sección con poco movimiento enseña
  piezas más antiguas, cada una con su fecha.

## Validación

Portada del 09-11-2026 generada: los seis bloques con tres piezas cada uno. Probada con `probar-web` en
Chromium y Firefox, escritorio y móvil.
