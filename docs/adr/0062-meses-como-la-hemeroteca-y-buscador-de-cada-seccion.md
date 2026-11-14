# 62. Los meses, como la hemeroteca; el mes, como índice; un buscador en cada sección y miniaturas en los resultados

Fecha: 2026-11-14 · Estado: aceptado

## Contexto

Desde el ADR 0050, las secciones, «Breves», «Reportajes» y «La viñeta» enseñan lo más reciente y, al pie,
«Por meses», una línea con un enlace por mes. Juanjo (14-11-2026) señaló que esas páginas siguen creciendo y
preguntó si no sería mejor un formato como el de la hemeroteca (ADR 0053), «una cuestión de formato de
presentación», con meses y años en lugar de días, a punto de cambiar de año. Al repasarlo se vio además que lo
que de verdad crece es la página de cada mes: la de noviembre de «Vibe coding» llevaba 33 piezas con su dibujo
y llegaría a unas 60. Juanjo propuso también un buscador que busque solo en cada sección y, al verlo, una
miniatura en cada resultado del buscador «para darle algo de colorido».

## Decisión

- **«Por meses», como el calendario de la hemeroteca** (`selector_meses()`): un año cada vez, con flechas, y
  sus doce meses en una rejilla de 4 × 3 con las abreviaturas de `MESES_ABREV` (las de castellano y gallego,
  con su punto). Los meses con algo enlazan a su página; los demás, en gris; el que se está viendo, en azul;
  el mes en curso, rodeado con el bolígrafo rojo (lo pone `SCRIPT_MESES` con la fecha de quien mira, como
  «hoy» en la hemeroteca). Sin script se ven todos los años, uno debajo de otro. Va al pie de la página
  principal de cada sección, donde iba la línea, y arriba en cada página de mes, en lugar de
  «← Mes anterior · Mes siguiente →».
- **La página de un mes, como índice** (`indice_mes()`), en las secciones (también «Hace un año») y en
  «Reportajes»: los titulares agrupados por día de publicación, del más reciente al más antiguo, con su
  entradilla y sin dibujos; cada día enlaza a su número. En pantalla ancha, como la hemeroteca: a la izquierda
  el rótulo de la sección, el mes, el buscador y los meses, que acompañan al bajar; a la derecha, el índice. En
  el móvil, todo seguido. «Breves» y «La viñeta» conservan su página de mes: cada breve ya es una o dos frases
  agrupadas por día, y la viñeta no tiene titular que listar.
- **Un buscador en cada sección** (`buscador_lista()`), en su página y en las de sus meses, también en
  «Breves» y «Reportajes»: un formulario corriente que abre el buscador del diario con la sección elegida
  (`buscar.html?q=…&seccion=…`, el filtro que Pagefind ya tiene de cada pieza, con el nombre de la sección en
  cada idioma). Funciona sin script.
- **La sección elegida se mantiene** al escribir otra búsqueda, hasta pulsar «Todas». Antes se quitaba al
  escribir, y la segunda búsqueda desde una sección buscaba en todo el diario (lo vio Juanjo al probarlo).
- **Una miniatura en cada resultado del buscador**: pequeña (8 rem; 5,5 en el móvil), con la proporción de
  los dibujos, **bajo el titular**, que no cambia, y con el texto alrededor (Juanjo: «que empiece bajo el
  titulo, donde está el texto, así el titulo no se modifica»). Es el dibujo suelto de la pieza o la captura de
  su recurso, marcado al indexar (`imagen_buscador()`, meta `imagen` de Pagefind, con la dirección desde la
  raíz del sitio). Sin imagen (los breves), el icono de la sección sobre su color.
- **Puntos suspensivos en los fragmentos** donde cortan el texto: delante si el fragmento no empieza al
  principio de la pieza y detrás si no llega al final, comparándolo con el texto entero que da Pagefind, para
  que se vea que no es el principio del artículo (Juanjo, 14-11-2026). Sin corchetes, que en castellano marcan
  un corte dentro de una cita, y unidos a la palabra con un espacio que no se parte.
- **Los enlaces no se indexan**: los de la conversación de origen (`origen()`) y los de las fichas del documento
  y del recurso llevan `data-pagefind-ignore`, como ya llevaban las fuentes y los botones. Salían en los
  fragmentos («Abrir el recurso · Su ficha en el…»).

## Alternativas descartadas

- **Un calendario de días en cada sección**: una sección no sale todos los días, y en ella se busca por
  tema, no por fecha. Juanjo aclaró que no lo pedía: el formato, con meses y años.
- **Un selector de año desplegable**, como el de meses de la hemeroteca: con pocos años, las flechas bastan.
- **La miniatura a todo el alto del resultado, a la izquierda**: recortaba los dibujos, que son apaisados, o
  los dejaba con franjas en el tema oscuro, porque el dibujo suelto lleva su fondo claro dentro. Juanjo: «así
  no queda bien». **Empezando en el titular**: lo partía; se bajó bajo él.

## Consecuencias

- La página de un mes pesa poco aunque el mes tenga muchas piezas: no carga dibujos.
- El selector no crece con el tiempo: un año a la vista.
- Cada resultado del buscador descarga su miniatura (unos 4 KB un dibujo; una captura, hasta 144 KB), solo
  de los diez que se ven.
- En el tema oscuro, la miniatura conserva el fondo claro de su dibujo, como una tarjeta de color.

## Validación

Probado el 14-11-2026 en una copia generada con los números publicados y en otra con un número simulado del
1 de enero de 2027, para el cambio de año: las flechas pasan de 2027 a 2026 en Chromium y Firefox. El
buscador de cada sección filtra bien en los cinco idiomas (castellano, catalán, gallego, euskera e inglés), y
la segunda búsqueda sigue en la sección hasta pulsar «Todas». Miniaturas vistas en Chromium y Firefox, en
ordenador y móvil y en tema claro y oscuro. `scripts/revisar-maqueta.js` en las páginas de sección, de mes,
de pieza, de reportaje, de breve, la hemeroteca y el buscador, en los cinco idiomas, Chromium y Firefox y
ordenador, tableta y móvil.

Un primer intento dejó sin cerrar la etiqueta oculta de la marca de imagen y escondía el texto de todas las
piezas; lo vio Juanjo al abrir un resultado. Se corrigió y se comprobó que ninguna página tiene un
`<span hidden>` sin cerrar.
