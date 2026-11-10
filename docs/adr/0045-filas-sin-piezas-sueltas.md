# 45. Filas sin piezas sueltas: reparto fijo según el número de piezas

Fecha: 2026-11-10 · Estado: aceptado

## Contexto

El ADR 0041 dejó sin huecos los bloques de sección de la portada, pero no las rejillas que reciben un número
variable de piezas: «Más del día» (lo de hoy que no cabe en las tres destacadas) y la página de cada sección iban
en filas de tres sin mirar cuántas había. La vista previa del número del 10-11-2026 tenía cinco piezas: apertura,
tres destacadas y una sola en «Más del día», con dos columnas vacías a su derecha. Juanjo: «hay que buscar
disposiciones que completen los huecos y tenerlas ya predefinidas», y que la próxima vez, con cuatro o cinco
noticias en vez de tres o seis, se arregle solo.

La revisión automática no lo vio por dos motivos: medía solo blancos verticales dentro de una fila, no filas que
no llegan al borde derecho, y descartaba las rejillas con un solo hijo. Tampoco se había probado entre 832 y
960 px (52 y 60 rem), donde las filas de tres pasaban a dos columnas y dejaban la tercera pieza sola: ahí la
vista previa real tenía filas incompletas en la portada y en las páginas de sección, fechas solas en su línea en
los bloques A y en «Hace un año».

## Decisión

- **Reparto fijo** (`reparto()` y `en_filas()` en `generar.py`): n piezas de una rejilla de tres columnas van en
  filas de tres y, al final, de dos; nunca una sola salvo que solo haya una. 4 → 2+2, 5 → 3+2, 7 → 3+2+2,
  8 → 3+3+2. Cada fila lleva sus columnas (`--n`) y las que siguen a otra (`fila-sigue`) se separan con un filete
  fino. Se usa en «Más del día» y en la página de cada sección.
- **Una sola pieza de más en la portada** sube a las destacadas, con su dibujo, y las destacadas se reparten igual
  (cuatro, en dos filas de dos). Se probó primero a bajar la tercera destacada a «Más del día», pero perdía su
  dibujo: Juanjo, al verlo, preguntó dónde estaba.
- **La cabecera de un artículo sin dibujo**, en el ordenador, a todo el ancho: el titular llena las líneas
  (`text-wrap: pretty`, y en Firefox, que no lo tiene, el reparto normal) y la entradilla va en dos columnas para
  no pasar de 75 caracteres por línea. Antes, titular equilibrado y entradilla con un tope de 52 rem dejaban vacía
  la derecha (Juanjo: «cuando una noticia no tiene imagen el título debería ocupar el espacio vacío también»). Las
  dos últimas palabras del titular van unidas (`sin_viuda`), para que la última no quede sola en su línea.
- **De 40 a 60 rem, la composición de tableta** (antes hasta 52 rem): destacadas, «Más del día», páginas de
  sección y bloques B en una columna con la miniatura a la izquierda; el bloque A, en una columna; «Breves» y
  «Hace un año», uno debajo del otro. Se quita la regla que pasaba las filas a dos columnas por debajo de 60 rem.
- **En el bloque A**, si el dibujo grande ya está en su tope y la lista sigue más larga, sus entradillas se
  recortan línea a línea, como mucho hasta dos.
- **El dibujo de una pieza de la portada lleva a su artículo** (también el del reportaje y el de «Hace un año»), como el titular (Juanjo: «cuando se hace clic en
  las imágenes de la portada no pasa nada… el comportamiento que se espera es entrar a leer el artículo»). Lo hace
  el script de la portada, sin envolver el dibujo en un enlace: la maqueta cuenta con que el dibujo cuelga
  directamente de la pieza, y el teclado y el lector de pantalla ya entran por el titular sin un enlace
  repetido. Con Ctrl, Mayúsculas o la rueda, en otra pestaña. En el artículo, el dibujo se sigue ampliando.
- **«Día anterior» y «Día siguiente» son dos flechas** (`circle-arrow-left` y `circle-arrow-right`, con su rótulo
  emergente y para el lector de pantalla) delante de «Portada», en la barra de secciones, como los botones de atrás y
  adelante del navegador, en vez de ocupar una línea propia debajo. Van en la portada (solo la de atrás) y en la página
  de cada número, en el mismo sitio. Las dos al principio y no una a cada extremo porque en el móvil la barra se
  desliza y la del final quedaría fuera de la pantalla.
- **Lo que mide la página para igualar las filas** (`fondo()` en `SCRIPT_FILAS`) no cuenta las líneas que oculta
  una entradilla recortada; contándolas, el bloque A recortaba la lista de más y dejaba un blanco de 97 px a
  1100 px.
- **La revisión automática** (`scripts/revisar-maqueta.js`) avisa de «fila incompleta» (la última fila de una
  rejilla de piezas deja más de 90 px vacíos a la derecha) y de «cabecera sin dibujo» (el titular o la entradilla
  de un artículo sin dibujo deja más de 250 px vacíos a la derecha), mira también las rejillas de un solo hijo y no cuenta
  las líneas que oculta una entradilla recortada (daba blancos que en pantalla no había).

## Alternativas descartadas

- **Una pieza sola a todo el ancho** (texto y dibujo uno al lado del otro): con dos y dos el resultado es más
  regular y no hace falta otra composición.
- **Bajar la tercera destacada a «Más del día»**: perdía su dibujo.
- **Mantener dos columnas entre 52 y 60 rem y repartir para dos**: obligaba a dos repartos según el ancho y las
  columnas seguían siendo estrechas para los bloques A.

## Consecuencias

- Ninguna cantidad de piezas deja una fila incompleta, sin intervención: el reparto se calcula cada noche.
- Entre 832 y 960 px la portada es más larga (una columna), como ya lo era en la tableta.

## Evidencia

- Vista previa del 10-11-2026 (`http://192.168.1.113:8770/`), con la revisión nueva: «fila incompleta (1 de 3
  columnas, 836 px vacíos) en fila-menores mas-dia» a 1366 px, y filas incompletas de destacadas, «Más del día» y
  la página de Vibe coding entre 700 y 960 px.

## Riesgos y limitaciones

- La revisión mide a anchuras fijas; las intermedias se cubren con una lista de nueve (390 a 1366 px).

## Validación

Variantes del número del 10-11-2026 con 1 a 10 piezas, generadas con `generar.py`: portada, Vibe coding, Debates
y la página del número en Chromium y Firefox a 1366, 1100, 960, 900, 840, 800, 700, 640 y 390 px; y portada (en
castellano, catalán e inglés), Vibe coding, Breves y «La redacción» con los dispositivos de `probar-web`
(escritorio, tableta y móvil) en Chromium, Firefox y WebKit: sin ningún aviso. Con el código anterior, las mismas
variantes daban filas incompletas en «Más del día» y en las páginas de sección, y fechas solas entre 840 y 960 px.
El clic en los dibujos de la portada (apertura, destacadas, bloques A y B y reportaje) lleva al artículo de su
titular en Chromium, Firefox y WebKit, en escritorio y móvil. La vista previa del NAS, regenerada con este código,
pasa `revisar-anchos.js` sin avisos en la portada, el artículo de «Hace un año» y Vibe coding.
