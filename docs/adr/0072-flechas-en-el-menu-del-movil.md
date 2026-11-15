# 72. Flechas en el menú del móvil

Fecha: 2026-11-15 · Estado: aceptado

## Contexto

En el móvil, la barra de secciones va en una sola fila que se desliza (ADR 0041), pero nada indicaba que quedaban
secciones ocultas: solo la última palabra cortada en el borde. Y en una sección del final (Biblioteca, La viñeta) la
activa quedaba fuera de la vista. Juanjo pidió algo en el margen derecho que ayude a ver que hay que deslizar.

## Decisión

- En el borde por el que quedan secciones ocultas, un degradado hacia el color del papel con una flecha (Lucide
  `chevron-right` y `chevron-left`). Al tocarla, el menú avanza o retrocede un 70 % de su ancho. Al llegar a un
  extremo, la de ese lado desaparece. Las crea el script común (`SCRIPT_TEMA`); estilos `.desliza` en
  `estaticos/diario.css`, solo por debajo de 40rem.
- El menú se abre desplazado hasta la sección en la que se está, si quedaba fuera.
- Las flechas no reciben el foco ni las lee el lector de pantalla: con el teclado se recorren los enlaces, que ya
  desplazan el menú.

## Consecuencias

- En el ordenador el menú cabe entero y no sale nada.

## Validación

- Chromium, Firefox y WebKit, en móvil y escritorio, tema claro y oscuro, con `scripts/revisar-maqueta.js` sin avisos
  (15-11-2026). En el WebKit de Linux que simula Safari, el degradado claro dibuja unas rayas muy tenues: sin
  comprobar en un iPhone real. Juanjo lo probó en su móvil antes de publicarlo.
