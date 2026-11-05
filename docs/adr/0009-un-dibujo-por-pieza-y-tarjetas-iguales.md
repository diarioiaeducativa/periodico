# 9. Un dibujo para cada pieza y tarjetas iguales en las páginas de sección

Fecha: 2026-11-03 · Estado: aceptado

## Contexto

El ilustrador dibujaba solo las piezas de importancia 1 y 2. En la página de cada sección, las
piezas iban en una cuadrícula de tres columnas: las que tenían dibujo, como destacadas, y las
demás, como menores, sin imagen y con el titular más pequeño. Cada fila toma la altura de la
pieza más alta, así que una fila con un dibujo y dos piezas sin él dejaba un hueco grande debajo
de estas (Juanjo, 03-11-2026, en Vibe coding: «¿por qué hay este hueco?»).

Se le propuso una lista, una pieza por fila, y la rechazó («en forma de lista no me gusta»).
Después vio en local tarjetas iguales con un recuadro con el icono de la sección en lugar del
dibujo, y preguntó cuánto costaría un dibujo para cada pieza.

## Decisión

- **El ilustrador dibuja todas las piezas**, sea cual sea su importancia (`encargos/ilustraciones.md`,
  paso 2). La portada no cambia: las piezas menores siguen sin imagen en sus bloques; el dibujo
  se ve en la página de la sección y en el artículo.
- **En la página de cada sección, todas las piezas son tarjetas iguales**, con la imagen arriba y
  el mismo tamaño de titular. La que no tiene imagen lleva un recuadro de la misma proporción
  (380 × 223) con el icono de su sección, teñido con su color. Es la reserva para cuando el
  revisor de dibujos retira uno (ADR 0005).
- **Las 5 piezas publicadas sin dibujo** (del 28-10 al 02-11) se dibujan una vez con
  `scripts/dibujar.sh FECHA [id ...]`, que pasa la misma revisión de cada noche y traduce los
  rótulos y el texto alternativo al catalán (pasos 2d y 2e). Sirve también para volver a
  intentar un dibujo retirado.

## Alternativas descartadas

- **Una lista, una pieza por fila**: rechazada por Juanjo.
- **Un mosaico sin huecos** (columnas que se rellenan de arriba abajo): rompe el orden por fecha.
- **Solo el recuadro con el icono, sin dibujar más**: quita el hueco, pero llena la sección de
  recuadros iguales; un dibujo explica la pieza.

## Consecuencias

- Un dibujo más cada noche (de 18 piezas publicadas hasta el 02-11, 5 eran de importancia 3): unos
  20 o 30 segundos del ilustrador, a partir de los 98 segundos que tardó en 4 dibujos el 03-11,
  más su revisión. Sin coste nuevo.

## Validación

Página de Vibe coding con las piezas del 03-11, generada en una copia y revisada en tema claro y
oscuro, a 1280 y 390 píxeles: todas las filas alineadas y sin huecos.
