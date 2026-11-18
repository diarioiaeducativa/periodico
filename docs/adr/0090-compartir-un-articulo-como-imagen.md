# 90. Compartir un artículo como imagen, dibujada en el navegador, desde el botón «Compartir»

Fecha: 2026-11-18 · Estado: aceptado

## Contexto

Juanjo pidió poder compartir una noticia como imagen, igual que se comparte en X la captura de un mensaje, sin que
el sitio ocupe más («sin incrementar el espacio que ocupa todo que ya es mucho»). La imagen al compartir que ya hay
(ADR 0010, `og/piezas/`) lleva el titular y el dibujo, pero no la entradilla, y él la quería («si falta la
entradilla, no»). Añadírsela no convenía: esa imagen es la de la vista previa de los enlaces, y X, Telegram,
WhatsApp y LinkedIn ya ponen la entradilla en texto al lado, que saldría dos veces, y el titular se leería peor en
la miniatura. Decidió que la tarjeta se dibujara en el navegador («vale, hazlo dibujado en el navegador») y que,
además, se copiara («se tiene que copiar también para poder pegarlo facilmente»). La primera versión copiaba sola al
pulsar; él propuso que quien pulsa elija («no es mejor que permita guardar o copiar?»), y la segunda, un botón
«Imagen» con su menú junto a «Compartir». Al final propuso juntarlo todo («quizás se podria unificar todo en el
botón compartir, poniendo allí todas las opciones») y lo aprobó. También pidió que cada opción dijera lo que hace:
«con el menú del dispositivo» no lo entendía («yo no sabía lo que era y la mayoria tampoco»).

## Decisión

Todo lo de compartir un artículo o un reportaje va en su botón «Compartir», que despliega un menú con el aspecto
del de «Para tu web» (`llevar-menu`, `llevar-op`), generado por `acciones()` en `generar.py` con sus textos en los
cinco idiomas. Cada opción dice lo que hace, sin nombres técnicos:

- «Compartir el enlace» («Envía el enlace del artículo a la app que elijas») y «Compartir como imagen» («Envía una
  imagen del artículo, con el enlace, a la app que elijas»): el menú de compartir del sistema. Solo salen donde lo
  hay: el móvil, la app y el ordenador con Windows, Mac o ChromeOS; no en Linux ni en Firefox de ordenador.
- «Copiar el enlace», solo donde no hay menú de compartir, y dice «Enlace copiado».
- «Copiar la imagen» («Para pegarla en un mensaje o una publicación»), que no sale si el navegador no deja copiar
  imágenes, y dice «Imagen copiada».
- «Guardar la imagen» («Se descarga como archivo PNG»).

Si compartir o copiar la imagen fallan, se descarga. Los breves conservan su botón de compartir, solo con el enlace.

**La viñeta** (`boton_vineta()`, debajo de cada tira: portada, día, «La viñeta» y bajo su artículo; no en la edición en
papel) lleva el mismo botón. Su enlace va a la página del número, a la tira (`FECHA/#t-vineta-FECHA`), porque no tiene
página propia. Su imagen es siempre horizontal, como la tira en el ordenador (Juanjo: «siempre deberia compartirse en
horizontal»): 1920 de ancho, con el nombre del diario, el título de la viñeta y la fecha en una línea, los tres paneles
en fila, «A partir de «titular».» debajo («eso situa la accion de la tira comica») y el nombre del sitio al pie. El
titular va entre comillas de su lengua, en redonda (`entre_comillas()`): comillas como pide la RAE para el título de
un artículo, que dejan ver dónde empieza; sin dos puntos, que la RAE no admite entre la preposición y su término.
Los paneles se dibujan con las reglas «.vineta …» de las hojas de la página, copiadas dentro de cada SVG con los
colores del tema claro. En el móvil los bocadillos se leen al ampliar la imagen; en el ordenador y la tableta, a la
primera.

El código está en `estaticos/compartir.js`, un archivo común que solo cargan las páginas con el botón (si sale dos veces,
se ejecuta una). La imagen de un artículo:

- Dibuja en un lienzo de 1080 × 1350 (4:5, el formato vertical que X, Instagram y WhatsApp enseñan entero) la
  cabecera del diario, el número y la fecha, la sección con su color, el titular, la entradilla y el dibujo, con la
  dirección del diario al pie. Todo se lee de la página (y el dibujo, de la meta `imagen` de Pagefind); los colores
  de sección son los del tema claro aunque quien lee tenga el oscuro.
- El titular se ajusta entre 66 y 44 px hasta caber en cinco líneas; la entradilla, entre 36 y 28 en seis. El
  dibujo ocupa el hueco que quede y, si es de menos de 220 px, no sale. Si ni así cabe, se acorta la entradilla con
  puntos suspensivos; el titular, nunca.
- Un SVG dibujado como imagen no ve las letras de la página: se le meten dentro las de Newsreader (latin), leídas
  de `fuentes/`.
- Se prepara cuando el botón está a punto de verse, no al pulsarlo: Safari solo abre el menú de compartir dentro
  del gesto de quien pulsa.

## Alternativas descartadas

- Reutilizar la imagen de la vista previa (`og/piezas/`): sin entradilla.
- Añadir la entradilla a esa imagen: repetida en las vistas previas y peor legible en las miniaturas.
- Una segunda imagen por artículo y lengua hecha en el NAS: unos 5 MB más a la semana en el repositorio del sitio.
- Copiar sin preguntar al pulsar (la primera versión): quien pulsa no sabe qué ha pasado y en el ordenador no
  había forma de guardarla.
- Un botón «Imagen» aparte, con su menú (la segunda versión, publicada unas horas): no se entendía qué hacía
  y repartía en dos lo que es una sola cosa. Unificado, compartir el enlace en el móvil pasa de uno a dos toques.
- Un menú propio con enlaces a X, Bluesky, LinkedIn, WhatsApp o Telegram donde no hay menú del sistema: solo
  llevarían el texto, no la imagen, y habría que mantenerlos si cambian esas webs.
- La dirección completa de la página en la imagen: nadie la escribe a mano («si a alguien le interesa la busca»);
  basta el nombre del sitio.
- Elegir un trozo del texto y compartirlo como cita: queda para cuando se pida.

## Consecuencias

El sitio no guarda ninguna imagen nueva: solo crece en el archivo de código (unos 11 kB) y una línea por página.
No se conecta con nadie: todo sale de la página y de las letras del propio sitio. La privacidad no cambia.

## Evidencia

Web Share API con archivos (`navigator.canShare({files})`): Chrome para Android, Safari de iOS y macOS y Chrome de
Windows; exige HTTPS. Escribir una imagen en el portapapeles (`ClipboardItem` con `image/png`): Chrome, Safari y
Firefox desde la 127.

## Riesgos y limitaciones

- Linux y Firefox de escritorio no tienen menú de compartir: solo copiar y guardar. Firefox para Android no está comprobado.
- En WebKitGTK (el WebKit de las pruebas) el lienzo no aplica todos los pesos de la letra variable y la cabecera
  sale menos gruesa; en Safari de verdad, por comprobar.
- Un artículo sin dibujo ni captura sale sin imagen, solo con el texto.

## Validación

18-11-2026, en local con Playwright (Chromium, Firefox y WebKit): la tarjeta sale en castellano, catalán, gallego y
euskera, con dibujo SVG, con captura JPG y con el titular más largo publicado (131 caracteres, cinco líneas); la
menú enseña «Compartir…» solo donde hay menú del dispositivo (simulado en las pruebas de móvil); «Copiar» deja en
el portapapeles un `image/png` (unos 150 kB) y dice «Image copied»; «Guardar» descarga
`diario-ia-educativa-2026-11-17-agente-clima-ies.png`; «Compartir…» recibe la imagen y el texto «titular + enlace»;
el menú se cierra tras cada acción. La fila de botones cabe a 360 px sin desbordar, en claro
y oscuro, y `revisar-maqueta.js` sale sin avisos en escritorio, tableta y móvil. Publicado el mismo día a petición de Juanjo
(«y publicalo ya»), sin esperar a su prueba en el móvil, que queda pendiente.

Con el botón único, el mismo día, en local y en los tres navegadores: en el ordenador salen «Copiar el enlace»,
«Copiar la imagen» y «Guardar la imagen»; con el menú de compartir simulado, «Compartir el enlace», «Compartir como
imagen», «Copiar la imagen» y «Guardar la imagen», y cada una hace lo suyo (el enlace que se comparte o se copia es
la dirección pública del artículo); el menú se cierra tras cada una. Los breves siguen compartiendo su enlace. La
maqueta, sin avisos.

La viñeta, el mismo día, en local y en los tres navegadores: la imagen en castellano, catalán, euskera e inglés, con
los colores claros también con el tema oscuro, y el «A partir de» más largo publicado (130 caracteres) en una línea;
en una página con el botón de un artículo y el de su viñeta, cada uno comparte lo suyo.
