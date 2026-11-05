# Encargo: ilustraciones del periódico

Dibuja una ilustración SVG para cada pieza de las ediciones de
`ediciones/*.json`. Guarda cada una en `ilustraciones/<fecha>-<id>.svg` y añade a la pieza
(en el mismo JSON) el campo `"ilustracion_alt"`: una frase que describa el dibujo para
quien no lo ve y que diga, tal cual, el texto de todos sus rótulos (un lector de pantalla lee
esa frase, no los rótulos del dibujo). No cambies nada más de los JSON.

## Qué tiene que ser

- **Explica la noticia, no la decora.** Un esquema del proceso, una comparación, una
  metáfora visual clara o un pequeño gráfico con lo esencial. Nada de robots, cerebros
  brillantes ni manos humanas tocando circuitos: son el tópico de la IA. Piensa en las
  infografías dibujadas a tinta de un buen diario.
- Si la pieza tiene campo `ilustracion` con una idea, úsala como punto de partida; si no,
  propón tú la idea a partir del titular y el cuerpo.
- Fiel al objeto real: si dibujas un teclado, un libro o una pantalla, con sus
  proporciones y sus elementos reales.
- Con los rótulos que necesite para entenderse sin leer la pieza: nombran las partes y
  los pasos del esquema.

## Cómo se dibuja (obligatorio, lo exige la hoja de estilo)

- `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 340">`, sin `width` ni `height`.
- Solo estas clases, sin colores escritos a mano (`fill`/`stroke` con valor) ni `style`:
  - `t`: trazo de tinta (el principal), `a`: trazo azul (lo que se quiere destacar),
    `r`: trazo rojo (como mucho un detalle por dibujo: una marca, una flecha clave),
  - `fa`: relleno azul pálido (fondos de formas), `ft`: relleno de tinta (puntos,
    detalles macizos pequeños), `fz`: relleno azul,
  - `lbl`: rótulos de texto (como mucho cinco, de una a tres palabras, en castellano).
- Trazo de línea limpia, como dibujado con rotulador fino; la hoja ya pone grosor 2,5 y
  extremos redondeados. Formas sencillas, mucho aire, composición equilibrada que use
  todo el ancho.
- Nada de degradados, filtros, sombras, imágenes, fuentes externas ni `<style>`.
- **Iconos de Lucide, solo cuando vengan bien.** Para un objeto concreto y reconocible (un
  portátil, un documento, un móvil, un candado, una persona), antes de dibujarlo a mano
  mira si Lucide tiene un icono que lo represente, y úsalo si así se reconoce mejor. Usarlo
  no es obligatorio y el dibujo no se hace a base de iconos: la idea, la composición y lo
  demás siguen siendo tuyos, y si ningún icono encaja, dibújalo como siempre. Búscalo con
  Grep en `lucide/iconos.txt` por su nombre o sus etiquetas, en inglés (una línea
  por icono: nombre | etiquetas en inglés | formas, en una cuadrícula de 24 × 24) y copia
  sus formas dentro de un grupo así:
  `<g class="t li3" transform="translate(X Y) scale(3)"><!-- Lucide: laptop (ISC) -->…formas…</g>`
  - escala 2, 3 o 4 (el icono mide 48, 72 o 96 de lado), con la clase `li2`, `li3` o
    `li4` que corresponda: así el trazo tiene el mismo grosor que el resto del dibujo;
  - la clase de color va en el `<g>` (`t`, `a` o `r`), no en cada forma; las formas del
    icono se copian sin tocar, y las que traen `class="ft"` la conservan;
  - el comentario con el nombre del icono, que acredita su origen.
- Cada archivo, válido y de menos de 12 KB.

Al terminar, responde con la lista de archivos y una línea por dibujo con la idea.
