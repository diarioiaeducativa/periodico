# 74. Variedad de posturas en la viñeta y tres gestos nuevos

Fecha: 2026-11-15 · Estado: aceptado

## Contexto

El 15-11-2026 Juanjo preguntó si convenía dar más gestos a Tiza y Algoritmo. Se contaron las
posturas de las 18 tiras publicadas (del 28-10 al 14-11-2026):

- Tiza, en 54 apariciones: abajo 24, sostener 15, señalar 8, pensar 6, encoger 1, arriba 0.
- Algoritmo, en 53: arriba 17, abajo 16, señalar 11, pensar 4, encoger 3, sostener 2.

Pasaba lo mismo que con las caras antes del ADR 0024: el resumen de los números anteriores
hablaba de caras, escenarios y objetos, pero no de posturas, y el encargo no pedía variarlas.
Además, el repertorio no tenía gestos para los remates que más se repiten (Tiza harta, el chasco,
la riña), que solo se notaban en la cara.

## Decisión

- **Tres posturas nuevas** en `vineta.py`, dibujadas para los dos personajes: `cruzar` (brazos
  cruzados), `cabeza` (las manos a la cabeza) y `jarras` (manos en la cintura). Las dos primeras
  pasan por delante del cuerpo y van sobre el borde del color del papel, como `pensar` y `sostener`
  (`CRUZAN`). No más de tres: con más, el guionista elige peor y no varía más.
- **Las posturas, en la memoria de los números anteriores**: `vineta.py --recientes` dice las
  tres más repetidas de cada personaje y las que no ha usado.
- **Regla de variedad** (`encargos/vineta.md`, «La variedad»): las posturas, como las caras;
  «abajo» solo si el chiste no pide otra. El juez (`encargos/pasos/4-juez.md`) puede cambiar
  también las posturas repetidas de la elegida.

## Validación

Dibujadas en una copia del sitio sobre las tiras del 13-11 (Tiza con las manos a la cabeza al leer
el acta) y del 14-11 (en jarras y con los brazos cruzados), en tema claro y oscuro; Juanjo las
vio en la red de casa antes de publicar. La primera versión llevaba una mano a la frente: «parece un
saludo militar o que se protege del Sol»; taparse los ojos con la mano parecía una venda. Las manos
a la cabeza se entienden a la primera. `--recientes` probado con el número del 16-11.

## Riesgos

- Que el guionista fuerce una postura nueva sin que el chiste la pida. El encargo pone la gracia
  por delante; vigilarlo en los números siguientes.
