# 90. Compartir un artículo como imagen, dibujada en el navegador

Fecha: 2026-11-18 · Estado: aceptado

## Contexto

Juanjo pidió poder compartir una noticia como imagen, igual que se comparte en X la captura de un mensaje, sin que
el sitio ocupe más («sin incrementar el espacio que ocupa todo que ya es mucho»). La imagen al compartir que ya hay
(ADR 0010, `og/piezas/`) lleva el titular y el dibujo, pero no la entradilla, y él la quería («si falta la
entradilla, no»). Añadírsela no convenía: esa imagen es la de la vista previa de los enlaces, y X, Telegram,
WhatsApp y LinkedIn ya ponen la entradilla en texto al lado, que saldría dos veces, y el titular se leería peor en
la miniatura. Decidió que la tarjeta se dibujara en el navegador («vale, hazlo dibujado en el navegador») y que,
además, se copiara («se tiene que copiar también para poder pegarlo facilmente»). La primera versión copiaba sola al
pulsar; él propuso que quien pulsa elija («no es mejor que permita guardar o copiar?») y lo aprobó con un menú.

## Decisión

Un botón «Imagen» (`como-imagen`) en las acciones de cada artículo y reportaje (`acciones()` en `generar.py`), con
sus textos en los cinco idiomas (`imagen`, `imagen_t`, `imagen_copiada`). El código está en
`estaticos/compartir-imagen.js`, un archivo común que solo cargan las páginas con el botón:

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
- El botón despliega un menú, con el aspecto del de «Para tu web» (`llevar-menu`, `llevar-op`): «Compartir…», que
  abre el menú del dispositivo con la imagen, el titular y el enlace y solo sale donde lo hay (móvil, app);
  «Copiar la imagen», que la pone en el portapapeles y dice «Imagen copiada», y no sale si el navegador no deja
  copiar imágenes; y «Guardar la imagen», que la descarga como PNG. Si compartir o copiar fallan, se descarga.

## Alternativas descartadas

- Reutilizar la imagen de la vista previa (`og/piezas/`): sin entradilla.
- Añadir la entradilla a esa imagen: repetida en las vistas previas y peor legible en las miniaturas.
- Una segunda imagen por artículo y lengua hecha en el NAS: unos 5 MB más a la semana en el repositorio del sitio.
- Copiar sin preguntar al pulsar (la primera versión): quien pulsa no sabe qué ha pasado y en el ordenador no
  había forma de guardarla.
- Elegir un trozo del texto y compartirlo como cita: queda para cuando se pida.

## Consecuencias

El sitio no guarda ninguna imagen nueva: solo crece en el archivo de código (unos 11 kB) y una línea por página.
No se conecta con nadie: todo sale de la página y de las letras del propio sitio. La privacidad no cambia.

## Evidencia

Web Share API con archivos (`navigator.canShare({files})`): Chrome para Android, Safari de iOS y macOS y Chrome de
Windows; exige HTTPS. Escribir una imagen en el portapapeles (`ClipboardItem` con `image/png`): Chrome, Safari y
Firefox desde la 127.

## Riesgos y limitaciones

- Firefox de escritorio no tiene menú de compartir: solo copiar y guardar. Firefox para Android no está comprobado.
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
