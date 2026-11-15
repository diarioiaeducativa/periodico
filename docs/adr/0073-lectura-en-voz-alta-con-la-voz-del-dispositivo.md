# 73. Lectura en voz alta con la voz del dispositivo

Fecha: 2026-11-15 · Estado: aceptado

## Contexto

Juanjo preguntó si se podía añadir un lector a los artículos. Sirve sobre todo a quien lee con dificultad (dislexia,
baja visión) o prefiere escuchar; quien usa lector de pantalla ya tiene su propia voz. El diario no tiene servidor
propio, no recoge datos de quien lee (ADR 0033 y 0070) y se publica en GitHub Pages, con espacio limitado.

## Decisión

- Un botón «Escuchar» en la línea de la sección de cada artículo y reportaje, junto a «Una columna», visible también
  en el móvil. Lee el titular, la entradilla y el texto con sus ladillos y listas; no lee dibujos, tablas, fichas ni
  lo que solo va en papel. Lo hace la voz del propio dispositivo, con la Web Speech API del navegador
  (`speechSynthesis`): no hay audios guardados ni servidor.
- **Solo voces locales** (`localService`): las de red, como las «Google …» de Chrome o las «Online» de Edge, mandan el
  texto y la conexión de quien escucha a un tercero. Si en el idioma de la página no hay ninguna, el botón no sale.
  Excepción: Firefox marca como no locales las voces de speech-dispatcher en Linux, que funcionan en el equipo, y no
  tiene voces de red; en Firefox valen todas.
- Mientras lee, el párrafo se marca y una barra fija abajo deja pausar, cambiar la velocidad y parar sin volver arriba.
  Pausar es callar y recordar la frase (`cancel()`), porque `pause()` y `resume()` fallan en Chrome de Android; el texto
  se trocea en frases agrupadas hasta unos 250 caracteres, y la pausa vuelve a la frase, no al párrafo.
- **Lo que se lee queda siempre a la vista** (Juanjo, 15-11-2026: «lee texto que queda oculto y no se ve»): cada
  párrafo se centra si cabe; dentro, cada frase, y cada palabra donde la voz avisa (`boundary`), se lleva a la parte
  alta de lo que se ve, por encima de la barra. Sigue aunque quien lee se haya movido (Juanjo lo aprobó así).
- **Velocidad** (0,75×, 1×, 1,25×, 1,5× y 2×), en un menú que se abre encima del botón; se aplica en el acto desde la
  frase que suena y se recuerda en el dispositivo (`diario.velocidad`, solo si no es 1×). La página de privacidad lo
  dice en los cinco idiomas, y que la lectura usa solo voces del propio dispositivo.
- **Teclado y lector de pantalla**: botones de verdad, en orden de tabulación; el menú, con flechas, Inicio y Fin;
  Escape cierra el menú o para la lectura. Los cambios («Leyendo en voz alta», «Lectura en pausa», «Lectura parada»,
  la velocidad) se anuncian en una región viva. Al parar, si el foco estaba en la barra, vuelve a «Escuchar» sin mover
  la página. Sin atajos de una letra: chocan con los lectores de pantalla (NVDA usa la P para ir al párrafo siguiente)
  y WCAG 2.1.4 solo los admite si se pueden desactivar o cambiar.
- Código: `boton_escuchar()`, `boton_velocidad()` y `SCRIPT_LECTOR` en `generar.py`, solo en `articulo()` y
  `articulo_reportaje()`; estilos tras los de `.columnas-boton` en `estaticos/diario.css`.

## Alternativas descartadas

- **Audio generado en el NAS con Piper** (libre y gratis): voz igual en todas partes, pero sin voz gallega (sí
  castellano, catalán, euskera e inglés) y con cinco audios por artículo cada día, que en pocos meses pasan del límite
  de 1 GB de GitHub Pages; habría que guardarlos fuera (Internet Archive) y añadir un paso más que puede fallar cada
  madrugada.
- **Aceptar las voces de red**: suenan mejor en Chrome de escritorio, pero mandan el texto y la conexión a Google o a
  Microsoft, contra lo que promete la página de privacidad.
- **Teclas de atajo** (P para pausa…): ver arriba.

## Consecuencias

- El botón sale o no según el aparato: no hay forma de garantizarlo desde la web.
- En la edición en papel no sale (`@media print`), y el papel del número no carga el script.

## Evidencia

- Voces de Piper: `voices.json` de `rhasspy/piper-voices` en Hugging Face (15-11-2026): `ca_ES`, `es_ES`, `eu_ES` y
  `en_*`, ninguna `gl_ES`.
- Chrome 124 de Android (emulador `prueba-twa`, motor de voz de Google): voces locales `ca_ES`, `es_ES`, `es_US` y
  varias `en_*`; ninguna gallega ni vasca.
- Chrome de escritorio en Linux (el de Juanjo): solo «Google …», todas de red (`localService: false`).
- Firefox en Linux: `ca-ES` y `es-ES` de speech-dispatcher, marcadas como no locales.

## Riesgos y limitaciones

- En gallego y en euskera el botón no saldrá en la mayoría de móviles Android ni en Chrome de Linux.
- En Chrome de Linux no sale en ningún idioma. En Windows y en Mac, Chrome trae voces locales: hipótesis sin comprobar.
- iPhone y Safari reales sin probar: hipótesis de que funcionan (sus voces son locales).
- La calidad y la velocidad real dependen de la voz de cada aparato; las de speech-dispatcher en Linux suenan robóticas.

## Validación

- Android real (emulador, Chrome 124 y voz de Google): lee, marca el párrafo, la pausa queda quieta, «Seguir» retoma
  la misma frase y «Parar» lo deja limpio.
- Con una voz simulada que avisa palabra a palabra, en Chromium y Firefox, ordenador y móvil, en un artículo y en el
  reportaje de casi 2.000 palabras: ninguna palabra fuera de la vista ni bajo la barra, con y sin avisos por palabra.
- Velocidad, teclado y anuncios, en Chromium, Firefox y WebKit, en castellano (0,75×) y en inglés (0.75×); la barra
  cabe a 320 px.
- axe-core (WCAG 2.0, 2.1 y 2.2 A y AA, y buenas prácticas), en reposo, leyendo, con el menú abierto y en pausa, en
  Chromium y Firefox, ordenador y móvil, tema claro y oscuro: sin fallos; se comprobó que axe detecta un botón sin
  nombre metido a propósito.
- `scripts/revisar-maqueta.js` con el botón visible, en cinco páginas (artículo, reportaje, Biblioteca; castellano,
  catalán y euskera), tres anchuras y dos temas: sin avisos.
- Juanjo lo probó en su Firefox y lo aprobó para publicar (15-11-2026).
