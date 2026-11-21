# 97. Tiza y Algoritmo con gorro en las vacaciones de Navidad

Fecha: 2026-11-21 · Estado: aceptado

## Contexto

Juanjo pidió el 21-11-2026 un gorro de Papá Noel para Tiza y Algoritmo, los bots y las fotos de los grupos
desde que empiezan las vacaciones de Navidad hasta Reyes, como hacía otros años con las fotos de los grupos
(las de los bots y los grupos, en el ADR 0051 del repositorio del bot). Al ver las imágenes preguntó si también
lo llevarían los de la cabecera: «tiza y algoritmo que están en la parte superior del diario… tambien tendran
gorro, no?».

## Decisión

- **Cuándo**: los números que salen del 22 de diciembre al 6 de enero, ambos incluidos (las vacaciones escolares
  de Cataluña, Orden EDF/66/2026), cada año. `vineta.navidad(AAAA-MM-DD)` lo decide por la fecha de
  publicación (`publicacion()`), así que la hemeroteca enseña cada número como salió.
- **Dónde**: en la viñeta (`vineta.tira()` y `vineta.panel()`, también en el carrusel de Instagram), en los dos
  personajes de la cabecera (`orejas()`) y en el icono de la web (`estaticos/favicon-navidad.svg` y su PNG de 32,
  que `generar.py` pone en lugar de los de siempre si el día en que se genera cae en esas fechas). El icono de la
  app de Android no cambia: pediría una versión nueva y dos revisiones de Google. La foto de Instagram tampoco
  (Juanjo: «en instagram no hace falta cambiarlo»).
- **El dibujo**: `vineta.gorro()`, rojo y blanco fijos en los dos temas y el contorno con la tinta del tema. En
  la cabecera, el trazo engorda con `--k` como el resto; el SVG deja ver lo que sale por arriba, así que la caja
  de los personajes no cambia.

## Evidencia y validación

- `navidad()`: el 21-12 no, el 22-12 y el 6-1 sí, el 7-1 no.
- La viñeta del 20-11 y una tira de prueba con las posturas que se acercan a la cabeza (`cabeza`, `arriba`,
  `pensar`, `cruzar`) y la expresión `cargando`, en tema claro y oscuro: el gorro no tapa la cara.
- El sitio entero generado como si fuera Navidad, con `probar-web` en Chromium, Firefox y WebKit, en
  escritorio, móvil y tableta y en los dos temas: sin errores ni desbordamiento. Generado con la fecha de hoy,
  sale igual que antes.
- Con un bocadillo de cinco líneas, la cola llega al gorro de quien habla; Juanjo lo vio y no pidió cambiarlo.
