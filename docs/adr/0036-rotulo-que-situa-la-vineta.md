# 36. Un rótulo en la primera viñeta que sitúa la escena

Fecha: 2026-11-09 · Estado: aceptado

## Contexto

La tira se lee a menudo sin haber leído la noticia de la que trata (en la portada, en la página de
viñetas, en Instagram). El 9 de noviembre, la que eligió el juez de humor (el detector que, al pedirle que
se explique, responde «88 %») no se entendía, y Juanjo la cambió a mano por otro de los cinco guiones. Al
ver las descartadas con la idea de cada una encima, preguntó si una frase que situara al lector, sin
contar el chiste, estaría bien en el diario. La idea que escribe el guionista no sirve para eso: casi
siempre cuenta el remate. Se le propuso un rótulo dentro de la primera viñeta, como en los cómics, y
que el juez lo quitara cuando la primera frase ya situara la escena; Juanjo prefirió ponerlo siempre
(«no dice nada pero da contexto») y pidió que el juez revisara también la frase.

## Decisión

- **Toda tira lleva en la primera viñeta un rótulo** (`cartela`, que el dibujo ya admitía) que dice dónde
  están y de qué va, sin contar ni adelantar el chiste. Por ejemplo: «De noche, en casa, dándole vueltas
  a los detectores de IA.» Como mucho 55 caracteres (`encargos/vineta.md`).
- **El guionista lo escribe en cada guion** (`encargos/pasos/3-guiones.md`) y **el juez lo revisa**: que
  esté, que sitúe sin adelantar el remate y que quepa; si no, lo reescribe y lo dice en «retoques»
  (`encargos/pasos/4-juez.md`). El traductor lo traduce con el mismo límite (`5-traduccion.md`).
- **Va dentro de la imagen**, no en el texto de la página, para que viaje con la tira a todas partes.
- **Si un rótulo se pasa de 58 caracteres**, el dibujo lo estrecha hasta el ancho del recuadro en vez
  de dejar que se corte (`vineta.cartela`), y `vineta.py --comprobar` lo apunta en el registro, igual que
  un rótulo que falta.
- Las tiras ya publicadas se quedan como salieron.

## Validación

El rótulo de 58 caracteres del número del 9 de noviembre cabe en una línea, con algo de margen, en
Firefox y Chromium, escritorio y móvil, claro y oscuro (`probar-web`); las versiones en catalán, gallego,
euskera e inglés son más cortas. El límite de 58 está medido con ese caso, no con letras anchas: por eso
los encargos piden 55 y el dibujo tiene el estrechamiento de reserva.
