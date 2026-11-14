# 50. Las páginas que acumulan, con lo reciente y el resto por meses

Fecha: 2026-11-11 · Estado: aceptado

## Contexto

«La viñeta», las secciones, «Breves» y «Reportajes» mostraban todo lo publicado en una sola página, que crecía
cada día. Con 14 números, «La viñeta» pesaba 146 KB, unos 10 KB por tira, y en un año pasaría de 3,5 MB con un
scroll interminable. Juanjo (11-11-2026) preguntó qué pasaría con las viñetas cuando hubiera muchos números.
Se le propuso dejar en cada página lo reciente y el resto por meses, y pidió prepararlo y verlo.

## Decisión

- **Cada página enseña lo más reciente**: las 7 últimas viñetas, los breves de los 7 últimos números que los
  tienen, las 12 últimas piezas de cada sección (cuatro filas de tres) y los 4 últimos reportajes, un mes
  (`RECIENTES` en `generar.py`).
- **Al pie, «Por meses»**: cada mes con algo publicado, también el mes en curso, en un selector como el
  calendario de la hemeroteca, un año cada vez (ADR 0062; antes, una línea con un enlace por mes). Solo sale
  cuando hay más de lo que cabe en la página: mientras no, la página lo enseña todo.
- **Cada mes, en su página** (`<carpeta>/AAAA-MM.html`: `vineta/`, `breves/`, `reportajes/` y una carpeta por
  sección), con todo lo que salió ese mes, la misma composición que la página principal y, arriba, el rótulo de
  la página de la que cuelga y el mismo selector de meses. En las secciones y «Reportajes», el mes es un índice de
  titulares por días, sin dibujos, con un buscador de la sección (ADR 0062).
- **El mes es el de publicación**, el de la fecha que ve el lector junto a cada pieza, no el de las
  conversaciones: lo que cuenta el 31 de octubre sale el 1 de noviembre y va en noviembre.
- Las páginas de mes entran en el mapa del sitio. Una sola función (`pagina_lista()`) hace las principales y
  las de mes; cada página dice en `lista_*()` qué recoge y cómo lo pinta.

## Alternativas descartadas

- **Páginas numeradas (1, 2, 3…)**: lo que está en cada una cambia cada día, así que sus enlaces no sirven para
  volver a algo. Un mes cerrado no cambia.
- **Solo la semana en curso en la página principal**: el lunes quedaría una sola viñeta.
- **Cargar más al bajar**: es el scroll interminable que se quería evitar.

## Consecuencias

- Las páginas principales dejan de crecer: su peso depende de `RECIENTES`, no de los números publicados.
- «Vídeos» sigue con todo en su página: sale uno o dos por semana. Si crece, se le aplica lo mismo.
- Los nombres de las páginas principales no cambian.

## Validación

Probado el 11-11-2026 en una copia generada con los 14 números publicados: salen octubre y noviembre en
«La viñeta», «Vibe coding» y «Breves», y las demás páginas siguen enteras. Sin enlaces rotos en las 45 páginas
nuevas o cambiadas de los cinco idiomas. `scripts/revisar-maqueta.js` sin avisos en Chromium y Firefox, en
escritorio, tableta y móvil y en cuatro idiomas, salvo el de «fecha sola» de las tiras, que ya salía antes
(ADR 0049). `scripts/revisar-anchos.js`, sin avisos.

En el mismo cambio, el pie de las versiones en catalán, gallego, euskera e inglés enlazaba las licencias de la
letra (`fuentes/OFL.txt`) y de los iconos (`LICENSE-LUCIDE.txt`) dentro de la carpeta del idioma, donde no
están, y daba error 404. Ahora apuntan a la raíz del sitio: los 1.292 enlaces de las 679 páginas llevan a un
archivo que existe.
