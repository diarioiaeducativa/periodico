# 41. La portada, sin huecos: maqueta de periódico y revisión automática

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

Después, el mismo día, tras mirar las portadas de The Guardian, Le Monde y La Vanguardia (las piezas pequeñas
solo con titular o miniatura, imágenes del mismo tamaño, filetes entre columnas y la disposición cambiando de
una sección a otra), y a partir de lo que Juanjo fue señalando en la vista previa:

- **El nombre de la sección, encima de sus piezas**, sobre su filete, y las piezas a todo el ancho. A la
  izquierda dejaba una columna vacía hasta el final de cada bloque.
- **Dos disposiciones que se alternan** en los bloques de la portada (`bloque_alterno`): A, la pieza más reciente
  con su dibujo y su entradilla y, tras un filete vertical, las otras dos con miniatura, titular y entradilla,
  con el texto rodeando la miniatura; B, las tres en fila con miniaturas del mismo tamaño. Tras una A va una B si
  los titulares de la sección tienen un largo parecido (`titulares_parejos`, como mucho una línea de diferencia);
  si no, otra A, porque en una fila de tres un titular con dos líneas más deja un blanco que nada arregla.
- **Las filas acaban a la misma altura** (`SCRIPT_FILAS`, en el navegador): en cada fila, cada pieza enseña de su
  entradilla entre dos líneas y la entera, hasta la altura a la que pueden acabar todas; en la A, lo que queda lo
  absorbe el dibujo de la pieza grande. Vale para destacadas, «Más del día», las dos disposiciones, la página de
  cada sección, la fila de los breves con «Hace un año» y los resúmenes de los vídeos de la semana. Se rehace al
  cambiar el ancho o el grupo elegido. La entradilla entera está en el artículo.
- **La fecha, nunca sola en su línea**: sin el nombre de la sección, va a la derecha en la línea del antetítulo,
  flotando para que el antetítulo la rodee. Todas las fechas, del mismo tamaño (la de la viñeta heredaba el del
  título). El tiempo de lectura del reportaje, fuera del rótulo, que en el móvil no lo dejaba caber.
- **Los breves, con el título encima y en columnas** que se reparten solas; cada breve entero en su columna
  (partido, Firefox dejaba sus enlaces sueltos arriba de la siguiente y Chrome no lo partía).
- **En la página de cada número**, lo no destacado en un solo bloque, «Más en este número», en columnas, cada
  pieza con su sección: un bloque por sección tenía casi siempre una sola pieza.
- **En la tableta**, las filas de tres y las destacadas, en una columna con la miniatura a la izquierda: las
  columnas eran tan estrechas que los titulares cambiaban mucho de largo. **En el móvil**, como antes: una
  columna, sin miniaturas en los bloques y con la entradilla entera.
- **El pie**, como el de un periódico: tres columnas iguales con su título y su lista (los grupos, el archivo y
  el diario, con los créditos en letra pequeña bajo los enlaces del diario, para que las tres midan parecido). El
  número que se está viendo, con una franja roja y «(este número)», no en negrita.
- **Revisión automática de la maqueta** (`scripts/revisar-maqueta.js`, para `probar-web -s`): huecos de más de
  90 px en una fila, fechas solas en su línea o pisando texto, miniaturas de una fila con distinta altura, fechas
  de distinto tamaño, columnas vacías bajo un título y bloques pegados. Se pasa por todas las páginas, idiomas y
  anchuras antes de enseñar o publicar un cambio de maqueta.

## Alternativas descartadas

- **Subir el tope global**: los huecos seguirían, solo que en otros días.
- **Bloques de ancho variable según las piezas**: un bloque de una pieza a todo el ancho rompe la rejilla.
- **Dibujos grandes en todas las piezas de los bloques**: alargaban la portada un 40 % en el ordenador y la
  duplicaban en el móvil, y en la A la columna de las pequeñas quedaba corta.
- **Partir los breves entre columnas**: véase arriba.
- **Los créditos del pie en una franja aparte**: dejaba la columna «El diario» con cinco enlaces y un hueco.

## Consecuencias

- Los bloques pasan de unas 10 piezas a 18 (seis secciones de tres), pero la portada casi no crece: cada fila
  ya ocupaba la altura de su pieza más larga.
- Lo que está en la portada ya no es solo de la última semana: una sección con poco movimiento enseña
  piezas más antiguas, cada una con su fecha.

## Validación

Portada del 09-11-2026 generada: los seis bloques con tres piezas cada uno. Después, `scripts/revisar-maqueta.js`
en 20 páginas (portada, secciones, números, la semana, un artículo, el reportaje, breves, reportajes, la
redacción, la hemeroteca y otros idiomas), en Chromium y Firefox, escritorio, tableta y móvil: sin ningún aviso.
Al empezar daba 75: huecos de hasta 225 px, fechas solas, miniaturas de 334 y 369 px en la misma fila y la
viñeta pegada al reportaje. La portada mide unos 7.070 px en el ordenador (4.950 antes de llenar los bloques).
