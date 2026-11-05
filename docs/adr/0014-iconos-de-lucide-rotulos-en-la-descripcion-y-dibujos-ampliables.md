# 14. Iconos de Lucide en los dibujos, rótulos en la descripción y dibujos ampliables

Fecha: 2026-11-04 · Estado: aceptado

## Contexto

El 02-11-2026, en Vibe Coding Educativo, un miembro elogió los dibujos del número 1
(https://t.me/vceduca/14501 y siguientes): SVG con formas e iconos, adaptados al tema claro y
oscuro, legibles por un lector de pantalla y con un «libro de estilo» común. El diario ya
hacía casi todo eso (ADR 0005 y 0009), pero al repasarlo salieron tres huecos:

- **El lector de pantalla no lee los rótulos.** El dibujo se inserta con `role="img"` y la
  descripción de `ilustracion_alt`, que tapa el texto de dentro; el encargo no pedía que esa
  descripción dijera los rótulos. El 04-11, 40 de los 56 dibujos publicados (contando las dos
  ediciones) dejaban fuera al menos uno.
- **Los dibujos no se amplían.** Las capturas del repositorio sí (ADR 0008), pero los dibujos
  no, y en el móvil sus rótulos quedan pequeños.
- **Los objetos se dibujan a mano.** El miembro supuso que los dibujos usaban iconos de
  Lucide; no es así, y un portátil o un documento dibujados a mano salen a veces poco fieles.

Juanjo pidió las tres cosas, con una condición para los iconos: «el ilustrador no tiene que
limitarse a estos iconos, los usará cuando vengan bien y si no seguirá como hasta ahora, no
quiero uniformizar los dibujos y que salgan todos iguales».

## Decisión

- **La descripción dice los rótulos.** `encargos/ilustraciones.md` pide que
  `ilustracion_alt` recoja, tal cual, el texto de todos los rótulos, y que el dibujo lleve
  los rótulos que necesite para entenderse sin leer la pieza. Las descripciones publicadas que
  no los recogían se completaron a mano, en los dos idiomas.
- **Los dibujos se amplían al pulsarlos** en la página de cada artículo, en el reportaje y en
  «La redacción», con el mismo visor de las capturas: sobre la página, al mayor tamaño que
  quepa, con los colores de su sección y la X arriba a la derecha. Al abrirse, la imagen crece
  desde su sitio y el fondo se oscurece, y al cerrarse vuelve (0,3 s; Juanjo: «el cambio es
  muy brusco»), también en las capturas; sin animación si el sistema pide reducir el
  movimiento. El visor es modal: el foco va a la X, el tabulador no lo saca de ella y
  Esc lo cierra y devuelve el foco a la imagen (05-11-2026). En la portada y las
  secciones, el dibujo sigue llevando a la pieza. El botón repite en su nombre la descripción
  del dibujo, que de otro modo quedaría tapada para el lector de pantalla.
- **Iconos de Lucide, cuando vengan bien.** `lucide/iconos.txt` reúne los 1.899 iconos de
  Lucide 1.60.0 (ISC), una línea por icono con su nombre, sus etiquetas y sus formas, para que
  el ilustrador, que no tiene terminal (ADR 0002), los busque con Grep. Lo prepara
  `scripts/lucide.py VERSIÓN`. Antes de dibujar a mano un objeto concreto, el ilustrador mira
  si hay un icono que lo represente y lo usa si así se reconoce mejor, sin obligación y sin
  que el dibujo se haga a base de iconos; la orden va también en el texto de cada paso de
  dibujo (2, 2d, 10 y 14), no solo en el encargo. El icono va en un `<g>` con la clase de
  color y una de escala (`li2`, `li3`, `li4`, para ×2, ×3 y ×4), que ajusta el grosor del
  trazo al del resto del dibujo (2,5), y un comentario con su nombre que acredita su origen.
  El crédito de Lucide ya estaba en el pie.
- `scripts/revisar-dibujos.py` acepta que una forma tome la clase de su `<g>`.

## Alternativas descartadas

- **Dibujos hechos de iconos o con una lista cerrada de iconos**: uniformizaría los dibujos,
  justo lo que Juanjo no quiere.
- **Copiar los 2.167 archivos SVG del paquete**: un archivo de texto se busca de una vez y
  ocupa 517 KB.
- **Trazo sin escalar (`vector-effect: non-scaling-stroke`)**: fija el grosor en píxeles de
  pantalla y no en los del dibujo, así que el icono no tendría el trazo del resto.
- **Plegables, lectura con desplazamiento (scrollytelling) y el «cursor IA»** que se citaron en
  el grupo: no aportan a una noticia, o piden una IA por lector, con coste y servidor.

## Consecuencias

- El ilustrador tiene un recurso más; la idea y la composición siguen siendo suyas.
- Si se actualiza Lucide, `scripts/lucide.py` con la versión nueva (de al menos dos semanas).

## Evidencia

- Lucide: https://lucide.dev, licencia ISC (`lucide/LICENSE`); paquete `lucide-static` 1.60.0
  de npm (20-10-2026).

## Riesgos y limitaciones

- El ilustrador puede abusar de los iconos; el revisor de dibujos lo juzga como cualquier otro
  dibujo, y el encargo dice que no es obligatorio.

## Validación

04-11-2026, en una copia aparte, el ilustrador real (scripts/dibujar.sh, con la revisión de
cada noche) redibujó las ocho piezas de los números del 2 y el 3 de noviembre, sin su
descripción anterior, como una pieza nueva:

- Primera versión del encargo: seis de ocho con iconos, pero perdían rótulos.
- Con los rótulos pedidos dentro del apartado de iconos y después en los criterios generales:
  rótulos sí, iconos ninguno; el ilustrador no llegaba a consultar el repertorio.
- Con la orden de mirarlo antes de dibujar a mano un objeto, también en el texto de cada paso:
  ocho de ocho con iconos (de dos a cinco cada uno) y de tres a cinco rótulos; revisión
  superada. Juanjo los vio en la copia y dio el visto bueno. Los dibujos publicados no se
  sustituyeron por estos ejemplos.
- La ampliación con transición se probó en Chromium, Firefox y WebKit (Playwright): abre,
  cierra con Escape y deja la página como estaba, sin errores de JavaScript.

Riesgo observado: en la última ronda todos los dibujos llevaban iconos; hay que vigilar en los
próximos números que no se uniformicen.
