# 75. Papeles, libro y pizarra de la viñeta, redibujados

Fecha: 2026-11-15 · Estado: aceptado

## Contexto

El 15-11-2026 Juanjo preguntó si había que mejorar el dibujo de algún objeto de la viñeta. Se
dibujaron todos en las manos de cada personaje, con escenario y en tema claro y oscuro. Tres no
se leían bien:

- **Papeles** (7 viñetas hasta el 14-11): un montoncito diminuto que parecía un sobre o escombro.
- **Libro** (3 viñetas): abierto y visto de frente, tan pequeño que parecía un mapa plegado.
- **Pizarra** (ninguna): blanca y de caballete, con las patas en el aire; chocaba con Algoritmo
  y, en el escenario aula, se ponía encima de la pizarra verde de la pared.

Los demás (portátil, reloj, exámenes, móvil, folio, taza y notificaciones) se entienden bien.

## Decisión

En `objeto()` de `vineta.py`:

- **Papeles:** seis hojas revueltas, del tamaño de un folio respecto a los personajes, con
  líneas de texto.
- **Libro:** abierto, más grande (44 px de ancho), con las páginas curvadas y el texto.
- **Pizarra:** verde, como la del aula, de 96 px de ancho para no tocar a nadie, sobre un
  caballete con las patas en el suelo. En el escenario `aula`, `panel()` no la dibuja: ya hay una.

Se aplica también a lo ya publicado cuando se regenera la web: es el mismo dibujo, mejor hecho.

## Validación

Dibujados en una copia del sitio sobre las tiras del 30-10 y el 12-11 (papeles), el 01-11
(libro) y el 05-11 (pizarra en lugar del portátil, solo para verla), en tema claro y oscuro;
Juanjo los vio en la red de casa antes de publicar.
