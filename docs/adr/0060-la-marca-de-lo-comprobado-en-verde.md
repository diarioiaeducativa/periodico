# 60. La marca de lo comprobado, en verde

Fecha: 2026-11-14 · Estado: aceptado

## Contexto

Desde la primera maqueta, la marca de trazo a mano que encabeza «Comprobado en» era roja: la paleta imita
el papel con dos bolígrafos, el azul y el rojo de corregir, y `estaticos/comun.css` lo decía en su cabecera
(«el rojo marca solo lo comprobado y el número de la edición»). No había ADR. El 14-11-2026 Juanjo, viendo
la marca en el tema oscuro, preguntó: «este tic que está en la base de los artículos, no debería ser verde?».

Tres razones le daban la razón: para cualquier lector una marca verde significa «verificado» y el rojo avisa
de un error; el mismo rojo marca las correcciones (`.correccion`, ADR 0055), lo contrario de lo comprobado; y
en el tema oscuro el rojo se aclara a un rosa (`#ff6e6e`) que se lee todavía más como alerta.

## Decisión

- La marca de «Comprobado en» usa un color propio, `--verde`: `#1a7f37` en el tema claro y `#5fd07f` en el
  oscuro. La forma del trazo no cambia.
- El rojo queda para el número de la edición y las correcciones.
- En papel sigue saliendo en negro, como el resto de colores (`@media print`).

## Alternativas descartadas

- **Dejarla roja**, por coherencia con la idea de los dos bolígrafos: la idea es del diario, la convención
  es del lector.
- **Usar el verde de la sección Vibe coding** (`--c-comunidad`): ataría el significado de la marca a una
  sección.

## Consecuencias

- El verde de la marca se parece al de la sección Vibe coding (`#1d7547` y `#6fd4a0`), así que en sus piezas
  la marca y el rótulo «Más en Vibe coding» comparten tono. Son elementos distintos, cada uno con su forma y
  su texto.

## Evidencia

- Contraste del trazo sobre el fondo: 4,9:1 en el tema claro (sobre `#fbfbf9`) y 9,4:1 en el oscuro (sobre
  `#13151a`), por encima del 3:1 que pide WCAG 2.1 (1.4.11) para elementos gráficos.

## Validación

- `probar-web` con `sitio/2026-11-11/prompt-propiedad-codigo-fable.html`, servido en la red de casa, en
  Chromium, Firefox y WebKit, escritorio y móvil, tema claro y oscuro: el color calculado de la marca es
  `rgb(26, 127, 55)` en claro y `rgb(95, 208, 127)` en oscuro en las doce combinaciones; revisadas las
  capturas de Chromium en escritorio claro y Firefox en móvil oscuro. El único error de las pruebas, la
  copia de los comentarios que no existe en local (404), no tiene que ver con el cambio.
- Publicado sin vista previa, a petición de Juanjo («no hace falta vista previa»).
