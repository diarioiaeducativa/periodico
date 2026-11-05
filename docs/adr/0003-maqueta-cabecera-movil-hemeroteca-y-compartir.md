# 3. Maqueta: cabecera móvil, piezas solas, hemeroteca y compartir

Fecha: 2026-11-02 · Estado: aceptado

## Contexto

Con el número 1 publicado, se revisó el sitio en escritorio y móvil, claro y oscuro, en
Chromium y Firefox. No había nada roto (sin errores de JavaScript, sin desbordamiento,
contrastes entre 5,5:1 y 8,7:1), pero sí cosas que afeaban y tres piezas habituales de un
periódico que faltaban y sirven al lector.

## Decisión

Lo que afeaba:

- **Cabecera móvil.** Antes de la primera noticia había unos 520 px de cabecera (número,
  idioma, tema, fecha, mancheta, lema en dos líneas, secciones en tres filas y «La
  redacción»). En pantallas de 40 rem o menos el lema no se muestra, las secciones van en una
  sola fila que se desliza (con la sección abierta centrada por un script al cargar) y «La
  redacción» va al final de esa fila, además de en el pie. Al principio quedaba solo en el pie,
  pero así no se encontraba desde la barra (04-11-2026).
- **Partición de palabras** (`hyphens: auto`) solo en el cuerpo de los artículos y en «La
  redacción»: en entradillas y breves partía nombres propios («Es-cola Ramon Pont»).
- **Una pieza sola no se estira.** En un bloque de sección con una pieza, la pieza tiene un
  tope de 38 rem (líneas de lectura de columna, no de 950 px). Una destacada sola (un día de
  archivo con dos piezas) se compone como la apertura, texto y dibujo a dos columnas
  (`.fila.sola`), en vez de un dibujo a todo el ancho.
- **Apertura a 6/6** entre texto y dibujo, en lugar de 5/7: el titular cabe en cuatro líneas.
- **En una columna, el dibujo siempre antes del titular**, como en el papel: la apertura lo
  ponía después y las destacadas antes.
- **«Año I · Núm. 1»** en la cabecera: el año cuenta desde el del número 1, en romanos; el
  círculo rojo rodea solo el número.
- **La mancheta es el `h1` de la portada y de la página de cada número** (05-11-2026, por el
  aviso de axe-core de la evaluación VCER): en la página de un número lleva el enlace a la
  portada y, solo para el lector de pantalla, la fecha del número. Se ve igual que con el `<p>`
  de antes: la comparación de capturas de las 16 páginas de día, en Chromium, Firefox y WebKit,
  a 320, 390, 768 y 1280 px y en los dos temas, no dio ningún píxel distinto. En los artículos y
  el resto de páginas el `h1` es su propio título y la mancheta sigue siendo un `<p>`.

Lo que faltaba:

- **Hemeroteca** (`archivo.html`, en los dos idiomas): todos los números por meses, cada uno
  con su fecha, su número y el titular de la apertura. El pie lista solo los últimos 7 días
  (`DIAS_PIE`) y enlaza a la hemeroteca: antes crecía una línea por día en todas las páginas.
- **Compartir** en cada artículo: abre el menú del dispositivo (`navigator.share`) y, si el
  navegador no lo tiene, copia el enlace y lo dice en el propio botón durante dos segundos.
  Nunca pide copiar a mano.
- **Compartir un breve** (añadido el mismo día, a petición de Juanjo): cada breve tiene su
  página, `AAAA-MM-DD/breve-N.html` (N, su orden en la edición), con su primera frase como
  título y vista previa. En la portada y en cada día, al final de sus enlaces, un botón de solo
  icono, discreto, que comparte esa página; al copiar, dice «Enlace copiado» a su lado. Una
  página propia y no un ancla en el día, para que al compartirlo en Telegram la vista previa
  sea la del breve y no la del número entero.
- **«Más en esta sección»** al pie de cada artículo: las tres piezas más recientes de la misma
  sección; si no hay ninguna, las del diario. Quien llega desde un aviso de Telegram a un
  artículo tenía solo «Volver a la portada».
- **`404.html`** propia (GitHub Pages solo admite una, en la raíz: en castellano con una línea
  en catalán, y con rutas absolutas porque se sirve en cualquier nivel) y **`sitemap.xml`**
  con todas las páginas de los dos idiomas.

El artículo lleva ahora la clase de su sección, así que su dibujo se tiñe con el color de la
sección, igual que en la portada.

## Alternativas descartadas

- **Secciones en varias filas en el móvil**, que no ocultan nada: dejaban la noticia fuera de
  la primera pantalla. La fila deslizable deja ver que hay más (el último rótulo sale cortado).
- **Buscador**: sin contenido suficiente aún; se verá cuando haya meses de archivo.
- **«Lo más leído»**: exigiría contadores, que este sitio no lleva.
- **Boletín por correo**: el aviso diario de Telegram hace ese papel.

## Consecuencias

- Las hojas de estilo se piden con la huella de su contenido (`diario.css?v=…`, `version_estatico`):
  el 02-11-2026, tras publicar el icono de compartir de los breves, el móvil de Juanjo enseñó la
  página nueva con la hoja antigua, que GitHub Pages deja guardar 10 minutos, y el icono salió
  como un botón grande con borde. Con la huella, una hoja cambiada es otra dirección.

- `generar.py` escribe además `archivo.html` (por idioma), `404.html` y `sitemap.xml`.
- El número cambia de clase en la cabecera (`.edicion-num` envuelve año y número): las reglas
  de móvil apuntan a esa clase.

## Validación

Capturas con `probar-web` del sitio generado y servido en local (02-11-2026): portada en
escritorio y móvil, artículo, día de archivo con destacada sola (31-10), hemeroteca, 404 en
tema oscuro y sección catalana en Firefox móvil. Sin errores de JavaScript ni desbordamiento.
Lo visto antes del cambio y después, en la conversación de ese día.

## Ampliación (03-11-2026): los breves

El bloque se llama «Breves» («Breus»), el término de los periódicos: «En breve» se leía
también como «dentro de poco». Los breves antiguos solo se encontraban día a día en la
hemeroteca, así que tienen una página propia (`breves.html`), con todos del más reciente al
más antiguo agrupados por día, enlazada desde el título del bloque en la portada y en cada
número (no en la barra de secciones, que ya tiene nueve entradas). El RSS los incluye, con su
página como enlace.

## Ampliación (04-11-2026): iconos de Breves, Reportaje y Viñeta

Las seis secciones llevaban icono en el título de su bloque, en el de su página y en el rótulo de
cada pieza; los Breves, el Reportaje y la Viñeta, no, y en la portada se veían como bloques de
otro tipo. Juanjo pidió el de los Breves y, al proponérselo, también los otros dos. Son de Lucide,
como los demás: `zap` (el rayo de la noticia breve, la «flash»), `file-text` y `pen-tool` (la
plumilla). Se descartó `newspaper` para los Breves porque se leería como el diario entero. Van en
los mismos sitios que los de las secciones; el rótulo de un breve y el del reportaje enlazan a su
página (`breves.html`, `reportajes.html`), como el de una pieza enlaza a su sección, y el título de la viñeta en la portada, a `vineta.html`, como los de los bloques de sección. La barra de
secciones sigue sin iconos, para todos.

La regla de la tira, `.vineta svg { width: 100% }`, agrandaba también el icono del título; ahora
se limita a `.vineta .tira svg`.

Validación: sitio generado en una copia y revisado a 1280 y 375 píxeles (portada, `breves.html`,
página de un breve, `reportajes.html`, el reportaje del 01-11 y `vineta.html`).
