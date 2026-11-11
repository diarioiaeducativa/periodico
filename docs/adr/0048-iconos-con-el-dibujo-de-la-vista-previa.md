# 48. Los iconos, con el dibujo de la imagen de vista previa

Fecha: 2026-11-11 · Estado: aceptado

## Contexto

Los iconos de la app (web instalable, iPhone, Android y Google Play) salían de `estaticos/favicon.svg`: Tiza
y Algoritmo macizos, simplificados, sobre un cuadrado oscuro (ADR 0013). La imagen de vista previa (`og/`)
los dibuja en cambio como en la viñeta, de línea y cogidos de la mano.
Juanjo (11-11-2026) preguntó si los iconos podían ser así, pidió que se hicieran bien, sin partir de una
captura, y, vista la prueba a tamaño real, eligió el dibujo nuevo para todo y, para la pestaña del navegador, la
versión simplificada que se le propuso: «me gusta, en la pestaña deja la versión más simple».

## Decisión

- **El dibujo de la imagen de vista previa, redibujado en vectorial** por `scripts/iconos.py` con las mismas
  formas y posiciones (las manos se juntan) que `og/og-es.html` (las de `vineta.py`), sobre el papel del diario (`#fbfbf9`), con los
  trazos 2,2 veces más gruesos que en la viñeta para que se lea a 48 px.
- **Tres encuadres de un mismo dibujo**: el de la web instalable (`icono-192.png`, `icono-512.png`), con las
  esquinas redondeadas como el anterior; el adaptable (`icono-maskable-512.png`), dentro de la zona segura,
  un círculo del 80 %, porque el sistema lo recorta; y el del iPhone (`apple-touch-icon.png`) y el de la ficha
  de Google Play (`android/fitxa/icono-512.png`), cuadrados, porque los redondea cada uno. Este último es
  también el avatar de la organización en GitHub.
- **La pestaña del navegador, con el mismo dibujo simplificado** (`favicon.svg`, hecho a mano, y
  `favicon-32.png`): las dos figuras cogidas de la mano y el otro brazo de Algoritmo levantado, con las caras
  reducidas a ojos y sonrisa, sin piernas, polvo ni rayas, y los trazos más gruesos. Los brazos de Algoritmo
  salen de los costados, como en el dibujo: desde las esquinas de arriba parecían cuernos. Con el dibujo
  entero, a 16 px los trazos se quedaban en dos manchas.
- **La app de Android** toma los suyos de la web publicada con `bubblewrap update` (ADR 0042), y por eso
  pasa a la versión 1.0.1.

## Alternativas descartadas

- **El mismo dibujo con los trazos de la viñeta** (2,5): a 32 y 48 px las líneas, los ojos y las rayas de
  debajo de Algoritmo desaparecen.
- **También en la pestaña, el dibujo entero con los trazos aún más gruesos** (3,4): a 16 px no se
  reconocía; hacía falta quitar detalle.
- **Seguir con el icono macizo en la pestaña**: el diario se identificaría con dos dibujos distintos.

## Consecuencias

- Todos los iconos son claros y con el mismo dibujo; el de la pestaña, simplificado.
- Para cambiar el dibujo, se edita `scripts/iconos.py` y se ejecuta; luego, publicar la web, `bubblewrap
  update` y subir el paquete a Play, y cambiar a mano el icono de la ficha y el avatar de GitHub, que no
  tienen API.
- Sobre fondos muy claros (GitHub, una pantalla de inicio blanca) el icono tiene menos contraste que el
  oscuro de antes.

## Validación

Página de prueba en local con el icono anterior y el nuevo a tamaño real: pantalla de inicio de Android con el
recorte redondo, iPhone, GitHub a 130, 40 y 20 px, pestaña del navegador y tamaño grande, en Chromium y
Firefox, y el de la pestaña en una pestaña de Chrome con el diario servido en local. El adaptable, medido: lo más alejado del centro queda a 204 px, dentro de la zona segura de 205.
