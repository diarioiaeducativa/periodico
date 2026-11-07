# 10. Avisos con formato y una imagen de vista previa para cada número

Fecha: 2026-11-04 · Estado: aceptado

## Contexto

El aviso de cada mañana en los tres grupos era un bloque de texto plano de 250 a 450 caracteres
con el enlace a la portada al final. La vista previa del enlace usaba siempre la misma imagen
genérica (`og-es.png`: la mancheta y los dos personajes), y Telegram, que guarda la vista previa
de cada dirección, la enseñaba igual todos los días, pequeña y casi en blanco en el móvil. Juanjo,
04-11-2026, con una captura del aviso del número 3: «esto es muy simplón, ¿se podría mejorar el
aspecto visual? que resulte más agradable y fácil de leer».

## Decisión

Recomendado y aceptado por Juanjo el 04-11-2026:

- **El agente de los avisos escribe solo el saludo y de dos a tres puntos** por grupo
  (`encargos/avisos.md`), y el bot monta el mensaje (`diario_grupos.py`, ADR 0029 del bot): el
  nombre del diario con el número en negrita, la fecha, el saludo, los puntos con su marca y el
  enlace con el 👉 de siempre. Así el formato no depende de que el agente escriba bien el HTML.
  `noche.sh` comprueba la forma (saludo y de dos a tres puntos) y repite el paso una vez si falla.
- **Cada número tiene su imagen de vista previa** (`scripts/og-numero.py`): la mancheta, el
  número, la fecha, la sección y el titular de la pieza que abre la portada, con su dibujo. Se
  guarda en `og/numeros/<fecha>-<es|ca>.png`; `generar.py` la copia a `sitio/og/` y la pone en la
  portada y en la página de ese día. Las demás páginas siguen con la genérica. El titular ajusta su
  tamaño a la columna (de 34 a 66 px; casi siempre unos 50) para que no quede hueco entre la fecha y
  la sección: con un tamaño fijo de 40 px quedaba un espacio en blanco grande con los titulares
  cortos (Juanjo, 07-11-2026, al ver el aviso del número 6: «tiene un gran espacio en blanco»; de
  tres variantes eligió la del titular grande pegado a la fecha). Probado con los seis primeros
  números en castellano, euskera e inglés.
- **Una imagen por grupo** (07-11-2026): además de la del número, `og-numero.py` hace para cada grupo
  la de su primera pieza (`og/numeros/<fecha>-es-<grupo>.png`, sin contar la Biblioteca), salvo que
  sea la misma que abre el número; `generar.py` escribe la página de entrada `n/<número>-<grupo>.html`,
  que solo lleva esa imagen y redirige al instante a la portada del número, y `avisos-cabecera.py`
  pone ese enlace en el aviso del grupo (el bot lo usa desde su 1.9.1, ADR 0029). Un grupo sin pieza
  propia ese día lleva el enlace general. Juanjo: «yo pensaba que cada una tenía la suya»; eligió que
  la página lleve a la portada y no a la pieza.
- **El enlace del aviso lleva el número** (`https://diarioiaeducativa.github.io/?n=3`, puesto por
  `scripts/avisos-cabecera.py` junto con el título y la fecha): es la misma portada, pero Telegram
  la trata como una dirección nueva y lee la imagen del día. El bot pide la vista previa grande y
  encima del texto.
- `publicar-nas.sh` hace la imagen y la cabecera antes de generar el sitio. Si alguna falla, el
  sitio sale con la imagen genérica y el aviso sin cabecera, pero sale.

## Alternativas descartadas

- **Que el agente escriba el mensaje con formato**: un error de etiquetas haría que Telegram
  rechazara el mensaje y el grupo se quedara sin aviso.
- **Enlazar la página del día** (`/2026-11-03/`) en vez de la portada: cambiaría la vista previa,
  pero el 02-11 se decidió enlazar la portada.
- **Una imagen hecha con IA**: coste por número y resultado sin revisar. La imagen sale del propio
  número con un programa normal (Chromium de Playwright, ya en la imagen del contenedor por el
  ADR 0005), sin coste.

## Consecuencias

- Unos segundos más al publicar y unos 60 kB por número e idioma en el repositorio.
- Los avisos en el formato anterior (texto) se siguen publicando tal cual: el bot acepta los dos.

## Evidencia

- Bot API de Telegram, `sendMessage` con `parse_mode` HTML y `link_preview_options` (`url`,
  `prefer_large_media`, `show_above_text`): https://core.telegram.org/bots/api#linkpreviewoptions
- Imágenes de los números 2 y 3 generadas en local el 04-11-2026 y revisadas a la vista.

## Riesgos y limitaciones

- Si la vista previa de `?n=` no saliera grande (lo decide el cliente de Telegram), el aviso se
  lee igual; la imagen es un añadido.

## Validación

- `og-numero.py` con los números 2 y 3 en castellano y catalán; `generar.py` pone la imagen de su
  número en la portada y en la página del día, y la genérica en los artículos.
- Pruebas del bot (`pruebas/test_diario_grupos.py`): formato nuevo, signos escapados, aviso sin
  cabecera y formato anterior.
- Un aviso de prueba enviado por el bot solo a Juanjo, antes del primer número con el formato.
